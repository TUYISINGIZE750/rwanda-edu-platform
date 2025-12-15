"""Seed database with TVET and TSS schools data"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.models.school import School
from tvet_schools_data import TVET_TSS_SCHOOLS

def seed_schools():
    """Seed the database with TVET/TSS schools"""
    db = SessionLocal()
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Check if schools already exist
        existing_count = db.query(School).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} schools. Clearing...")
            db.query(School).delete()
            db.commit()
        
        # Add all schools
        for school_data in TVET_TSS_SCHOOLS:
            school = School(
                id=school_data["id"],
                name=school_data["name"],
                type=school_data["type"],
                category=school_data["category"],
                province=school_data["province"],
                district=school_data["district"],
                trades=school_data["trades"]
            )
            db.add(school)
        
        db.commit()
        print(f"✓ Successfully seeded {len(TVET_TSS_SCHOOLS)} TVET/TSS schools")
        
        # Print statistics
        tvet_count = db.query(School).filter(School.type == "TVET").count()
        tss_count = db.query(School).filter(School.type == "TSS").count()
        
        print(f"\nStatistics:")
        print(f"  - TVET Schools: {tvet_count}")
        print(f"  - TSS Schools: {tss_count}")
        print(f"  - Total: {tvet_count + tss_count}")
        
        # Print schools by province
        print(f"\nSchools by Province:")
        provinces = db.query(School.province).distinct().all()
        for (province,) in provinces:
            count = db.query(School).filter(School.province == province).count()
            print(f"  - {province}: {count} schools")
        
    except Exception as e:
        print(f"Error seeding schools: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding TVET/TSS schools...")
    seed_schools()
