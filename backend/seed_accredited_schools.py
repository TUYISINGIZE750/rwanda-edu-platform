"""Seed database with accredited TVET/TSS schools"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.models.school import School
from real_accredited_schools import ACCREDITED_SCHOOLS

def seed_schools():
    db = SessionLocal()
    
    try:
        Base.metadata.create_all(bind=engine)
        
        existing_count = db.query(School).count()
        if existing_count > 0:
            print(f"Clearing {existing_count} existing schools...")
            db.query(School).delete()
            db.commit()
        
        for school_data in ACCREDITED_SCHOOLS:
            school = School(
                id=school_data["id"],
                name=school_data["name"],
                type=school_data["type"],
                category=school_data["status"],
                province=school_data["province"],
                district=school_data["district"]
            )
            db.add(school)
        
        db.commit()
        print(f"Successfully seeded {len(ACCREDITED_SCHOOLS)} accredited TVET/TSS schools")
        
        tvet_count = db.query(School).filter(School.type == "TVET").count()
        tss_count = db.query(School).filter(School.type == "TSS").count()
        
        print(f"\nStatistics:")
        print(f"  TVET Schools: {tvet_count}")
        print(f"  TSS Schools: {tss_count}")
        print(f"  Total: {tvet_count + tss_count}")
        
        print(f"\nSchools by Province:")
        provinces = db.query(School.province).distinct().all()
        for (province,) in provinces:
            count = db.query(School).filter(School.province == province).count()
            print(f"  {province}: {count} schools")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding accredited TVET/TSS schools...")
    seed_schools()
