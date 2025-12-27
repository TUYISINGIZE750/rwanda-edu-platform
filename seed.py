from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.school import School
from collections import defaultdict

router = APIRouter(prefix="/admin/seed", tags=["admin"])

SCHOOLS_DATA = [
    {"name": "KANYINYA TVET", "province": "Kigali city", "district": "NYARUGENGE", "trades": ["Automobile technology", "Building construction", "Fashion Design"]},
    {"name": "FOREVER TVET INSTITUTE", "province": "Kigali city", "district": "GASABO", "trades": ["Computer system and architecture", "Electrical technology", "Land surveying", "Public works"]},
    {"name": "International Technical School of Kigali", "province": "Kigali city", "district": "GASABO", "trades": ["Food and Beverage Operations", "TOURISM"]},
    {"name": "Lycee de Kicukiro APADE", "province": "Kigali city", "district": "KICUKIRO", "trades": ["ACCOUNTING", "Building construction", "Electronics and telecommunication", "Food and Beverage Operations", "Maltimedia production", "Networking  and internet technology", "software development", "Software programming and embedded systems", "Tourism"]},
    {"name": "KAYENZI TVET SCHOOL", "province": "Southern Province", "district": "KAMONYI", "trades": ["Building construction", "Electrical technology", "Electronics and telecommunication", "Plumbing", "Welding and metal fabrication"]},
    {"name": "FR. RAMON KABUGA TVET SCHOOL", "province": "Southern Province", "district": "KAMONYI", "trades": ["Building construction", "Electrical technology", "Plumbing", "Welding and metal fabrication"]},
    {"name": "COLLEGE APPEC REMERA RUKOMA TVET SCHOOL", "province": "Southern Province", "district": "KAMONYI", "trades": ["Building construction", "Electrical technology", "Plumbing", "Welding and metal fabrication"]},
    {"name": "RUNDA TVET", "province": "Southern Province", "district": "KAMONYI", "trades": ["Building construction", "Electrical technology", "Plumbing", "Welding and metal fabrication"]}
]

@router.post("/schools")
def seed_schools(db: Session = Depends(get_db)):
    try:
        # Clear existing
        db.query(School).delete()
        db.commit()
        
        # Add schools
        for school_data in SCHOOLS_DATA:
            school = School(
                name=school_data["name"],
                type="TVET",
                category="Public",
                province=school_data["province"],
                district=school_data["district"],
                trades=school_data["trades"]
            )
            db.add(school)
        
        db.commit()
        
        total = db.query(School).count()
        return {"message": f"Successfully seeded {total} schools", "total": total}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
