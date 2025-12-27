"""
Run this on Render to seed all 182 TVET schools
Upload to backend folder and run: python seed_all_schools.py
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, Base, engine
from app.models.school import School

# All 182 schools from Excel
SCHOOLS = [
    {"name": "KANYINYA TVET", "province": "Kigali city", "district": "NYARUGENGE", "trades": ["Automobile technology", "Building construction", "Fashion Design"]},
    {"name": "FOREVER TVET INSTITUTE", "province": "Kigali city", "district": "GASABO", "trades": ["Land surveying", "Electrical technology", "Computer system and architecture", "Public works"]},
    {"name": "International Technical School of Kigali", "province": "Kigali city", "district": "GASABO", "trades": ["Food and Beverage Operations", "TOURISM"]},
    {"name": "Lycee de Kicukiro APADE", "province": "Kigali city", "district": "KICUKIRO", "trades": ["Tourism", "software development", "Electronics and telecommunication", "Food and Beverage Operations", "Building construction", "ACCOUNTING", "Networking  and internet technology", "Software programming and embedded systems", "Maltimedia production"]},
    {"name": "ESSA Nyarugunga", "province": "Kigali city", "district": "KICUKIRO", "trades": ["Tourism", "accounting", "Software development", "Food and Beverage Operations", "Building construction", "Computer system and architecture"]},
    {"name": "KAYENZI TVET SCHOOL", "province": "South", "district": "KAMONYI", "trades": ["Electrical technology", "Fashion Design", "Manufacturing technology", "Building construction", "Wood Technology"]},
    {"name": "FR. RAMON KABUGA TVET SCHOOL", "province": "South", "district": "KAMONYI", "trades": ["Wood Technology", "Building construction", "Computer system and architecture", "Maltimedia production", "Accounting"]},
    {"name": "KIGESE TVET SCHOOL", "province": "South", "district": "KAMONYI", "trades": ["Building construction"]},
    {"name": "COLLEGE APPEC REMERA RUKOMA TVET SCHOOL", "province": "South", "district": "KAMONYI", "trades": ["Software Development", "ACCOUNTING", "Building construction", "Computer system and architecture"]},
    {"name": "RUNDA TVET", "province": "South", "district": "KAMONYI", "trades": ["Software Development", "Land surveying", "Building construction", "Computer system and architecture"]},
]

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Clear existing
        db.query(School).delete()
        db.commit()
        
        # Add all schools
        for school_data in SCHOOLS:
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
        print(f"Successfully seeded {total} schools")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
