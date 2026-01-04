from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import verify_password, get_password_hash, create_access_token, get_current_user
from ..models.user import User, UserRole
from ..schemas.user import UserCreate, UserLogin, Token, UserResponse
from ..services.school_service import validate_trade_for_school

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate trade for TVET students
    if user_data.role == UserRole.STUDENT and user_data.selected_trade:
        validate_trade_for_school(db, user_data.school_id, user_data.selected_trade)
    
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role,
        school_id=user_data.school_id,
        province=user_data.province,
        district=user_data.district,
        grade=user_data.grade,
        selected_trade=user_data.selected_trade,
        selected_level=user_data.selected_level,
        locale=user_data.locale
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # AUTO-ASSIGN to matching modules if student
    if user.role == UserRole.STUDENT and user.selected_trade:
        from ..models.group import Group
        from ..models.group_member import GroupMember
        from ..models.notification import NotificationType
        from .notifications import create_notification
        
        # Find all classes with matching department
        matching_groups = db.query(Group).filter(
            Group.school_id == user.school_id,
            Group.department == user.selected_trade,
            Group.type == 'CLASS'
        ).all()
        
        for group in matching_groups:
            # Check if not already member
            existing = db.query(GroupMember).filter(
                GroupMember.group_id == group.id,
                GroupMember.user_id == user.id
            ).first()
            
            if not existing:
                member = GroupMember(
                    group_id=group.id,
                    user_id=user.id
                )
                db.add(member)
                
                # Notify student
                await create_notification(
                    db=db,
                    user_id=user.id,
                    notification_type=NotificationType.CLASS_ASSIGNED,
                    title=f"Added to {group.name}",
                    message=f"You've been automatically added to {group.name} based on your department",
                    link=f"/hubs/{group.id}",
                    related_id=group.id,
                    related_type="group"
                )
        
        db.commit()
    
    return user

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account inactive")
    
    role_value = user.role.value if hasattr(user.role, 'value') else str(user.role)
    token = create_access_token({"sub": str(user.id), "role": role_value})
    return Token(access_token=token, token_type="bearer", user=user)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
