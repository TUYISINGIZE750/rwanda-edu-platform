"""Class Teacher API - For managing teacher access to classes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.group import Group
from ..models.teacher_class_access import TeacherClassAccess
from ..core.security import get_current_user

router = APIRouter(prefix="/class-teacher", tags=["class-teacher"])

class GrantAccessRequest(BaseModel):
    teacher_id: int
    module_name: Optional[str] = None

@router.get("/my-class")
def get_my_managed_class(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the class managed by current class teacher"""
    if not current_user.is_class_teacher or not current_user.managed_class_id:
        raise HTTPException(status_code=403, detail="Not a class teacher")
    
    group = db.query(Group).filter(Group.id == current_user.managed_class_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Managed class not found")
    
    # Get teachers with access
    accesses = db.query(TeacherClassAccess).filter(
        TeacherClassAccess.group_id == group.id
    ).all()
    
    teachers_with_access = []
    for access in accesses:
        teacher = db.query(User).filter(User.id == access.teacher_id).first()
        if teacher:
            teachers_with_access.append({
                "id": teacher.id,
                "full_name": teacher.full_name,
                "email": teacher.email,
                "module_name": access.module_name,
                "granted_at": access.created_at.isoformat() if access.created_at else None
            })
    
    return {
        "class": {
            "id": group.id,
            "name": group.name,
            "type": group.type.value if hasattr(group.type, 'value') else str(group.type)
        },
        "teachers_with_access": teachers_with_access
    }

@router.post("/grant-access")
def grant_teacher_access(
    request: GrantAccessRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Grant another teacher access to your managed class"""
    if not current_user.is_class_teacher or not current_user.managed_class_id:
        raise HTTPException(status_code=403, detail="Not a class teacher")
    
    # Check if teacher exists
    teacher = db.query(User).filter(
        User.id == request.teacher_id,
        User.school_id == current_user.school_id,
        User.role == UserRole.TEACHER
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Check if access already exists
    existing = db.query(TeacherClassAccess).filter(
        TeacherClassAccess.teacher_id == request.teacher_id,
        TeacherClassAccess.group_id == current_user.managed_class_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Teacher already has access")
    
    # Grant access
    access = TeacherClassAccess(
        teacher_id=request.teacher_id,
        group_id=current_user.managed_class_id,
        granted_by=current_user.id,
        module_name=request.module_name
    )
    
    db.add(access)
    
    # Also add teacher to GroupMember so they can see the class
    from ..models.group_member import GroupMember
    existing_member = db.query(GroupMember).filter(
        GroupMember.user_id == request.teacher_id,
        GroupMember.group_id == current_user.managed_class_id
    ).first()
    
    if not existing_member:
        member = GroupMember(
            user_id=request.teacher_id,
            group_id=current_user.managed_class_id
        )
        db.add(member)
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Access granted to {teacher.full_name}"
    }

@router.delete("/revoke-access/{teacher_id}")
def revoke_teacher_access(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoke a teacher's access to your managed class"""
    if not current_user.is_class_teacher or not current_user.managed_class_id:
        raise HTTPException(status_code=403, detail="Not a class teacher")
    
    access = db.query(TeacherClassAccess).filter(
        TeacherClassAccess.teacher_id == teacher_id,
        TeacherClassAccess.group_id == current_user.managed_class_id
    ).first()
    
    if not access:
        raise HTTPException(status_code=404, detail="Access not found")
    
    db.delete(access)
    
    # Also remove from GroupMember
    from ..models.group_member import GroupMember
    member = db.query(GroupMember).filter(
        GroupMember.user_id == teacher_id,
        GroupMember.group_id == current_user.managed_class_id
    ).first()
    
    if member:
        db.delete(member)
    
    db.commit()
    
    return {"success": True, "message": "Access revoked"}

@router.get("/available-teachers")
def get_available_teachers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of teachers who don't have access yet"""
    if not current_user.is_class_teacher or not current_user.managed_class_id:
        raise HTTPException(status_code=403, detail="Not a class teacher")
    
    # Get teachers with access
    teachers_with_access = db.query(TeacherClassAccess.teacher_id).filter(
        TeacherClassAccess.group_id == current_user.managed_class_id
    ).all()
    
    access_ids = [t[0] for t in teachers_with_access]
    
    # Get all teachers except those with access and current user
    available_teachers = db.query(User).filter(
        User.school_id == current_user.school_id,
        User.role == UserRole.TEACHER,
        User.id != current_user.id,
        User.id.notin_(access_ids) if access_ids else True
    ).all()
    
    return [{
        "id": t.id,
        "full_name": t.full_name,
        "email": t.email
    } for t in available_teachers]
