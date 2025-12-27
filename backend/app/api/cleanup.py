"""
Add this endpoint to remove duplicates via API call
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.school import School

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/remove-duplicate-schools")
def remove_duplicate_schools(db: Session = Depends(get_db)):
    """Remove duplicate schools from database"""
    
    all_schools = db.query(School).all()
    
    seen = {}
    duplicates = []
    
    for s in all_schools:
        key = (s.name.strip().lower(), s.province.lower(), s.district.lower())
        if key in seen:
            duplicates.append(s.id)
        else:
            seen[key] = s.id
    
    if duplicates:
        for dup_id in duplicates:
            school = db.query(School).filter(School.id == dup_id).first()
            if school:
                db.delete(school)
        db.commit()
    
    remaining = db.query(School).count()
    
    return {
        "success": True,
        "duplicates_removed": len(duplicates),
        "remaining_schools": remaining
    }
