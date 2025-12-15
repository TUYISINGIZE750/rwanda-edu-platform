from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..core.database import get_db
from ..models.user import User, UserRole
from ..core.security import get_current_user

router = APIRouter(prefix="/admin", tags=["modules"])

@router.get("/modules")
def get_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Mock modules data for now
    modules = [
        {
            "id": 1,
            "name": "Basic Electronics",
            "trade": "Electronics",
            "level": "1",
            "description": "Introduction to electronic components and circuits",
            "assigned_teacher": "John Doe",
            "lessons": ["Ohm's Law", "Resistors", "Capacitors"]
        },
        {
            "id": 2,
            "name": "Advanced Welding",
            "trade": "Welding",
            "level": "2", 
            "description": "Advanced welding techniques and safety",
            "assigned_teacher": None,
            "lessons": ["TIG Welding", "MIG Welding", "Safety Protocols"]
        }
    ]
    return modules

@router.post("/modules")
def create_module(
    module_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Mock module creation
    new_module = {
        "id": 999,
        "name": module_data["name"],
        "trade": module_data["trade"],
        "level": module_data["level"],
        "description": module_data.get("description", ""),
        "assigned_teacher": None,
        "lessons": [],
        "created_at": datetime.now().isoformat()
    }
    
    return {"message": "Module created successfully", "module": new_module}

@router.get("/teachers")
def get_teachers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get teachers from database
    teachers = db.query(User).filter(
        User.role == UserRole.TEACHER,
        User.school_id == current_user.school_id
    ).all()
    
    return [
        {
            "id": teacher.id,
            "full_name": teacher.full_name,
            "email": teacher.email
        }
        for teacher in teachers
    ]

@router.post("/modules/{module_id}/assign")
def assign_module(
    module_id: int,
    assignment_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    teacher_id = assignment_data["teacher_id"]
    
    # Verify teacher exists and is in same school
    teacher = db.query(User).filter(
        User.id == teacher_id,
        User.role == UserRole.TEACHER,
        User.school_id == current_user.school_id
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Mock assignment (in real implementation, create assignment record)
    return {
        "message": f"Module {module_id} assigned to {teacher.full_name}",
        "notification_sent": True
    }

@router.get("/school-trades/{school_id}")
def get_school_trades(
    school_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Import School model
    from ..models.school import School
    
    # Get real trades from the schools database
    school = db.query(School).filter(School.id == school_id).first()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Return the trades from the school
    return school.trades if school.trades else []

# Teacher endpoints
teacher_router = APIRouter(prefix="/teacher", tags=["teacher-modules"])

@teacher_router.get("/assigned-modules")
def get_assigned_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teacher access required")
    
    # Mock assigned modules for teacher
    assigned_modules = [
        {
            "id": 1,
            "name": "Basic Electronics",
            "trade": "Electronics", 
            "level": "1",
            "description": "Introduction to electronic components and circuits",
            "assigned_date": "2024-01-15T10:00:00Z"
        }
    ]
    
    return assigned_modules