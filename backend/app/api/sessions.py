from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.user import User
from ..core.security import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.get("/active")
def get_active_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Mock active sessions data
    sessions = [
        {
            "id": 1,
            "title": "Electronics Lab Session",
            "instructor": "Mr. John Doe",
            "start_time": "2024-01-16T14:00:00Z",
            "end_time": "2024-01-16T16:00:00Z",
            "status": "active"
        },
        {
            "id": 2,
            "title": "Welding Practice",
            "instructor": "Ms. Jane Smith",
            "start_time": "2024-01-16T10:00:00Z",
            "end_time": "2024-01-16T12:00:00Z",
            "status": "scheduled"
        }
    ]
    return sessions

@router.get("/")
def get_all_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Mock all sessions data
    sessions = [
        {
            "id": 1,
            "title": "Electronics Lab Session",
            "instructor": "Mr. John Doe",
            "start_time": "2024-01-16T14:00:00Z",
            "end_time": "2024-01-16T16:00:00Z",
            "status": "active"
        },
        {
            "id": 2,
            "title": "Welding Practice", 
            "instructor": "Ms. Jane Smith",
            "start_time": "2024-01-16T10:00:00Z",
            "end_time": "2024-01-16T12:00:00Z",
            "status": "scheduled"
        },
        {
            "id": 3,
            "title": "Automotive Diagnostics",
            "instructor": "Mr. Peter Johnson",
            "start_time": "2024-01-17T09:00:00Z",
            "end_time": "2024-01-17T11:00:00Z",
            "status": "scheduled"
        }
    ]
    return sessions