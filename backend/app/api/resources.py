from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.user import User
from ..core.security import get_current_user

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("/")
def get_resources(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Mock resources data for now
    resources = [
        {
            "id": 1,
            "title": "Electronics Fundamentals",
            "type": "PDF",
            "url": "/files/electronics_basics.pdf",
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "id": 2,
            "title": "Welding Safety Guide",
            "type": "Video",
            "url": "/files/welding_safety.mp4",
            "created_at": "2024-01-14T14:30:00Z"
        },
        {
            "id": 3,
            "title": "Circuit Analysis Worksheet",
            "type": "Document",
            "url": "/files/circuit_analysis.docx",
            "created_at": "2024-01-13T09:15:00Z"
        }
    ]
    return resources