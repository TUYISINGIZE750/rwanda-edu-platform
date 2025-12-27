"""Simple seed script for schools"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.models.school import School

SIMPLE_SCHOOLS = [
    {"id": 60, "name": "KAYENZI TVET SCHOOL", "type": "TVET", "category": "Public", "province": "South", "district": "Kamonyi", "trades": ["Building construction", "Electrical technology", "Fashion Design"]},
    {"id": 61, "name": "FR. RAMON KABUGA TVET SCHOOL", "type": "TVET", "category": "Public", "province": "South", "district": "Kamonyi", "trades": ["Building construction", "Computer system and architecture"]},
    {"id": 64, "name": "COLLEGE APPEC REMERA RUKOMA TVET SCHOOL", "type": "TVET", "category": "Public", "province": "South", "district": "Kamonyi", "trades": ["ACCOUNTING", "Building construction"]},
    {"id": 65, "name": "RUNDA TVET", "type": "TVET", "category": "Public", "province": "South", "district": "Kamonyi", "trades": ["Building construction", "Computer system and architecture"]},
    {"id": 2, "name": "FOREVER TVET INSTITUTE", "type": "TVET", "category": "Public", "province": "Kigali city", "district": "Gasabo", "trades": ["Computer system and architecture", "Electrical technology"]},
    {"id": 3, "name": "International Technical School of Kigali", "type": "TSS", "category": "Public", "province": "Kigali city", "district": "Gasabo", "trades": ["Food and Beverage Operations", "TOURISM"]},
]

def seed():
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        db.query(School).delete()
        
        for s in SIMPLE_SCHOOLS:
            school = School(**s)
            db.add(school)
        
        db.commit()
        print(f"Seeded {len(SIMPLE_SCHOOLS)} schools")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
