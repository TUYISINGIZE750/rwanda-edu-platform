"""DOS (Deputy in charge of studies) Admin API"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List
import secrets
import string
from datetime import datetime
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.group import Group
from ..models.teacher_class_access import TeacherClassAccess
from ..core.security import get_current_user, get_password_hash

router = APIRouter(prefix="/dos", tags=["dos-admin"])

class CreateTeacherRequest(BaseModel):
    full_name: str
    email: str
    is_class_teacher: bool = False
    managed_class_id: Optional[str] = None  # Now accepts class name

class BulkUploadResponse(BaseModel):
    success: int
    failed: int
    credentials: List[dict]

def generate_password(length=8):
    """Generate a random password"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@router.get("/dashboard")
def get_dos_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get DOS dashboard data"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="DOS/Admin only")
    
    from ..models.school import School
    
    # Get statistics
    total_teachers = db.query(func.count(User.id)).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.TEACHER
    ).scalar()
    
    total_students = db.query(func.count(User.id)).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.STUDENT
    ).scalar()
    
    total_classes = db.query(func.count(Group.id)).filter(
        Group.school_id == current_user.school_id
    ).scalar()
    
    class_teachers_count = db.query(func.count(User.id)).filter(
        User.school_id == current_user.school_id,
        User.is_class_teacher == 1
    ).scalar()
    
    # Get recent teachers
    recent_teachers = db.query(User).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.TEACHER
    ).order_by(User.created_at.desc()).limit(10).all()
    
    teachers_data = []
    for teacher in recent_teachers:
        managed_class = None
        if teacher.managed_class_id:
            group = db.query(Group).filter(Group.id == teacher.managed_class_id).first()
            managed_class = group.name if group else None
        
        teachers_data.append({
            "id": teacher.id,
            "full_name": teacher.full_name,
            "email": teacher.email,
            "is_class_teacher": bool(teacher.is_class_teacher),
            "managed_class": managed_class,
            "created_at": teacher.created_at.isoformat() if teacher.created_at else None
        })
    
    return {
        "stats": {
            "total_teachers": total_teachers,
            "total_students": total_students,
            "total_classes": total_classes,
            "class_teachers": class_teachers_count
        },
        "recent_teachers": teachers_data
    }

@router.post("/create-teacher")
def create_teacher(
    request: CreateTeacherRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new teacher with generated credentials"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="DOS/Admin only")
    
    # Validate: if class teacher, must have managed_class_id
    if request.is_class_teacher and not request.managed_class_id:
        raise HTTPException(status_code=400, detail="Class teacher must be assigned to a class")
    
    # Check if email already exists
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Find or create the group for the class
    group_id = None
    if request.is_class_teacher and request.managed_class_id:
        group = db.query(Group).filter(
            Group.name == request.managed_class_id,
            Group.school_id == current_user.school_id
        ).first()
        
        if not group:
            # Create the group/class
            from ..models.group import GroupType
            group = Group(
                name=request.managed_class_id,
                school_id=current_user.school_id,
                type=GroupType.CLASS
            )
            db.add(group)
            db.flush()
        
        group_id = group.id
    
    # Generate password
    password = generate_password()
    
    # Create teacher
    teacher = User(
        email=request.email,
        hashed_password=get_password_hash(password),
        full_name=request.full_name,
        role=UserRole.TEACHER,
        school_id=current_user.school_id,
        province=current_user.province,
        district=current_user.district,
        is_class_teacher=1 if request.is_class_teacher else 0,
        managed_class_id=group_id,
        generated_password=password,
        is_active=1
    )
    
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    
    # If class teacher, auto-join the managed class
    if request.is_class_teacher and group_id:
        from ..models.group_member import GroupMember
        existing_member = db.query(GroupMember).filter(
            GroupMember.user_id == teacher.id,
            GroupMember.group_id == group_id
        ).first()
        
        if not existing_member:
            member = GroupMember(
                user_id=teacher.id,
                group_id=group_id
            )
            db.add(member)
            db.commit()
    
    return {
        "success": True,
        "teacher_id": teacher.id,
        "credentials": {
            "email": teacher.email,
            "password": password,
            "full_name": teacher.full_name,
            "is_class_teacher": bool(teacher.is_class_teacher)
        }
    }

@router.get("/teachers")
def get_all_teachers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all teachers in the school"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="DOS/Admin only")
    
    teachers = db.query(User).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.TEACHER
    ).all()
    
    result = []
    for teacher in teachers:
        managed_class = None
        if teacher.managed_class_id:
            group = db.query(Group).filter(Group.id == teacher.managed_class_id).first()
            managed_class = {"id": group.id, "name": group.name} if group else None
        
        result.append({
            "id": teacher.id,
            "full_name": teacher.full_name,
            "email": teacher.email,
            "is_class_teacher": bool(teacher.is_class_teacher),
            "managed_class": managed_class,
            "is_active": bool(teacher.is_active),
            "created_at": teacher.created_at.isoformat() if teacher.created_at else None
        })
    
    return result

@router.put("/teachers/{teacher_id}/set-class-teacher")
def set_class_teacher(
    teacher_id: int,
    class_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Designate a teacher as class teacher for a specific class"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="DOS/Admin only")
    
    teacher = db.query(User).filter(
        User.id == teacher_id,
        User.school_id == current_user.school_id
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Find or create group
    group = db.query(Group).filter(
        Group.name == class_name,
        Group.school_id == current_user.school_id
    ).first()
    
    if not group:
        from ..models.group import GroupType
        group = Group(
            name=class_name,
            school_id=current_user.school_id,
            type=GroupType.CLASS
        )
        db.add(group)
        db.flush()
    
    teacher.is_class_teacher = 1
    teacher.managed_class_id = group.id
    
    # Auto-join the teacher to the class
    from ..models.group_member import GroupMember
    existing_member = db.query(GroupMember).filter(
        GroupMember.user_id == teacher_id,
        GroupMember.group_id == group.id
    ).first()
    
    if not existing_member:
        member = GroupMember(
            user_id=teacher_id,
            group_id=group.id
        )
        db.add(member)
    
    db.commit()
    
    return {"success": True, "message": f"{teacher.full_name} is now class teacher"}

@router.delete("/teachers/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deactivate a teacher"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="DOS/Admin only")
    
    teacher = db.query(User).filter(
        User.id == teacher_id,
        User.school_id == current_user.school_id
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teacher.is_active = 0
    db.commit()
    
    return {"success": True, "message": "Teacher deactivated"}

@router.post("/teachers/{teacher_id}/reset-password")
def reset_teacher_password(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reset teacher password and generate new credentials"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="DOS/Admin only")
    
    teacher = db.query(User).filter(
        User.id == teacher_id,
        User.school_id == current_user.school_id
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Generate new password
    new_password = generate_password()
    teacher.hashed_password = get_password_hash(new_password)
    teacher.generated_password = new_password
    db.commit()
    
    return {
        "success": True,
        "credentials": {
            "email": teacher.email,
            "password": new_password,
            "full_name": teacher.full_name
        }
    }

@router.get("/school-classes")
def get_school_classes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all classes/trades for the current DOS's school"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="DOS/Admin only")
    
    from ..models.school import School
    from sqlalchemy import distinct
    
    school = db.query(School).filter(School.id == current_user.school_id).first()
    
    if not school:
        return {"classes": []}
    
    trades = school.trades if school.trades else []
    
    # Default to L1-L5 for all TVET schools
    levels = ['L1', 'L2', 'L3', 'L4', 'L5']
    
    classes = []
    for trade in trades:
        for level in levels:
            classes.append({
                "name": f"{level} {trade}",
                "trade": trade,
                "level": level
            })
    
    return {"classes": classes}

@router.post("/fix-password")
def fix_dos_password(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fix DOS password - emergency endpoint"""
    # Find the DOS user for RUNDA TVET
    dos_user = db.query(User).filter(User.email == "dos.rundatvet.kamonyi@iprc.ac.rw").first()
    
    if not dos_user:
        raise HTTPException(status_code=404, detail="DOS user not found")
    
    # Update password
    new_password = "dos123"
    dos_user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return {
        "message": "DOS password updated successfully",
        "email": dos_user.email,
        "password": new_password
    }
