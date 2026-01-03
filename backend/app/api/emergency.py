"""
Emergency DOS Password Fix Endpoint
This is a temporary endpoint to fix the DOS password issue
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.user import User
from ..core.security import get_password_hash

router = APIRouter(prefix="/emergency", tags=["emergency"])

@router.post("/fix-dos-runda")
def emergency_fix_dos_password(db: Session = Depends(get_db)):
    """Emergency fix for DOS RUNDA password - no auth required"""
    try:
        # Find the DOS user
        dos_user = db.query(User).filter(User.email == "dos.rundatvet.kamonyi@iprc.ac.rw").first()
        
        if not dos_user:
            return {"error": "DOS user not found", "email": "dos.rundatvet.kamonyi@iprc.ac.rw"}
        
        # Update password
        new_password = "dos123"
        dos_user.hashed_password = get_password_hash(new_password)
        db.commit()
        
        return {
            "success": True,
            "message": "DOS password updated successfully",
            "email": dos_user.email,
            "password": new_password,
            "user_id": dos_user.id
        }
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

@router.get("/check-dos-runda")
def check_dos_user(db: Session = Depends(get_db)):
    """Check if DOS user exists"""
    try:
        dos_user = db.query(User).filter(User.email == "dos.rundatvet.kamonyi@iprc.ac.rw").first()
        
        if not dos_user:
            return {"found": False, "email": "dos.rundatvet.kamonyi@iprc.ac.rw"}
        
        return {
            "found": True,
            "email": dos_user.email,
            "user_id": dos_user.id,
            "full_name": dos_user.full_name,
            "role": dos_user.role.value if dos_user.role else None,
            "school_id": dos_user.school_id,
            "is_active": dos_user.is_active
        }
    except Exception as e:
        return {"error": str(e)}