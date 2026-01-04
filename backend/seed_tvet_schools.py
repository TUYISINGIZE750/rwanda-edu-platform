"""Seed database with TVET schools from Excel file"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import pandas as pd
from collections import defaultdict
from app.core.database import SessionLocal, engine, Base
from app.models.school import School

def seed_schools():
    """Seed the database with TVET schools from Excel"""
    file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    if not os.path.exists(file_path):
        print(f"Excel file not found: {file_path}")
        print("Skipping school seeding...")
        return
    
    db = SessionLocal()
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Add missing columns if they don't exist (PostgreSQL)
        try:
            from sqlalchemy import text
            db.execute(text("ALTER TABLE schools ADD COLUMN IF NOT EXISTS school_code VARCHAR"))
            db.execute(text("ALTER TABLE schools ADD COLUMN IF NOT EXISTS gender VARCHAR"))
            db.commit()
            print("Added missing columns (if needed)")
        except Exception as e:
            print(f"Note: Could not add columns (might already exist): {e}")
            db.rollback()
        
        # Check if schools already exist
        existing_count = db.query(School).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} schools. Skipping seed.")
            db.close()
            return
        
        print(f"Reading Excel file: {file_path}")
        df = pd.read_excel(file_path, header=1)
        df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
        
        # Group trades by school
        schools_data = defaultdict(lambda: {
            'trades': [],
            'school_code': None,
            'name': None,
            'province': None,
            'district': None,
            'gender': None
        })
        
        for idx, row in df.iterrows():
            if pd.isna(row['School Name']) or pd.isna(row['District']):
                continue
            
            school_key = (str(row['School Name']).strip(), str(row['District']).strip())
            school_data = schools_data[school_key]
            
            school_data['school_code'] = str(row['School code']).strip() if pd.notna(row['School code']) else None
            school_data['name'] = str(row['School Name']).strip()
            school_data['province'] = str(row['Province']).strip()
            school_data['district'] = str(row['District']).strip()
            school_data['gender'] = str(row['Gender']).strip() if pd.notna(row['Gender']) else 'Mixt'
            
            if pd.notna(row['Trade in full']):
                trade = str(row['Trade in full']).strip()
                if trade and trade not in school_data['trades']:
                    school_data['trades'].append(trade)
        
        # Insert schools
        schools_added = 0
        for (school_name, district), school_data in schools_data.items():
            school = School(
                school_code=school_data['school_code'],
                name=school_data['name'],
                type='TVET',
                category='Public',
                province=school_data['province'],
                district=school_data['district'],
                trades=school_data['trades'],
                gender=school_data['gender']
            )
            db.add(school)
            schools_added += 1
        
        db.commit()
        print(f"Successfully seeded {schools_added} TVET schools from Excel")
        
        # Print statistics
        print(f"\nSchools by Province:")
        provinces = db.query(School.province).distinct().all()
        for (province,) in provinces:
            count = db.query(School).filter(School.province == province).count()
            print(f"  - {province}: {count} schools")
        
    except Exception as e:
        print(f"Error seeding schools: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding TVET schools from Excel...")
    seed_schools()
