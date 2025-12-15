"""Load TVET schools from Excel file with proper structure"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import pandas as pd
import json
from collections import defaultdict
from app.core.database import SessionLocal, engine, Base
from app.models.school import School

def load_tvet_schools():
    """Load TVET schools from Excel file"""
    file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    if not os.path.exists(file_path):
        print(f"Excel file not found: {file_path}")
        return
    
    print("Reading Excel file...")
    try:
        # Read with header=1 since row 1 contains the actual headers
        df = pd.read_excel(file_path, header=1)
        print(f"Found {len(df)} rows in Excel")
        print(f"Columns: {list(df.columns)}")
        
        # Clean column names
        df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
        
        db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        
        # Clear existing schools
        db.query(School).delete()
        db.commit()
        
        # Group trades by school
        schools_data = defaultdict(lambda: {
            'trades_full': [],
            'trades_short': [],
            'school_code': None,
            'name': None,
            'province': None,
            'district': None,
            'gender': None
        })
        
        for idx, row in df.iterrows():
            # Skip rows with missing essential data
            if pd.isna(row['School Name']) or pd.isna(row['District']):
                continue
            
            school_key = (str(row['School Name']).strip(), str(row['District']).strip())
            school_data = schools_data[school_key]
            
            # Set basic school info (same for all trades of this school)
            school_data['school_code'] = str(row['School code']).strip() if pd.notna(row['School code']) else None
            school_data['name'] = str(row['School Name']).strip()
            school_data['province'] = str(row['Province']).strip()
            school_data['district'] = str(row['District']).strip()
            school_data['gender'] = str(row['Gender']).strip() if pd.notna(row['Gender']) else 'Mixt'
            
            # Add trades
            if pd.notna(row['Trade in full']):
                trade_full = str(row['Trade in full']).strip()
                if trade_full and trade_full not in school_data['trades_full']:
                    school_data['trades_full'].append(trade_full)
            
            if pd.notna(row['Trades']):
                trade_short = str(row['Trades']).strip()
                if trade_short and trade_short not in school_data['trades_short']:
                    school_data['trades_short'].append(trade_short)
        
        schools_added = 0
        
        for (school_name, district), school_data in schools_data.items():
            school = School(
                school_code=school_data['school_code'],
                name=school_data['name'],
                type="TVET",
                category="Public",  # Default, can be updated later
                province=school_data['province'],
                district=school_data['district'],
                trades_full=json.dumps(school_data['trades_full']) if school_data['trades_full'] else None,
                trades_short=json.dumps(school_data['trades_short']) if school_data['trades_short'] else None,
                gender=school_data['gender']
            )
            db.add(school)
            schools_added += 1
            print(f"  Added: {school_data['name']} ({school_data['district']}) - {len(school_data['trades_full'])} trades - Gender: {school_data['gender']}")
        
        db.commit()
        print(f"\nSuccessfully added {schools_added} schools from Excel")
        
        # Show statistics
        total = db.query(School).count()
        print(f"\nDatabase Statistics:")
        print(f"  Total schools: {total}")
        
        # Show sample data
        sample_schools = db.query(School).limit(3).all()
        print(f"\nSample schools:")
        for school in sample_schools:
            trades_full = json.loads(school.trades_full) if school.trades_full else []
            trades_short = json.loads(school.trades_short) if school.trades_short else []
            print(f"  - {school.name} ({school.school_code})")
            print(f"    District: {school.district}, Gender: {school.gender}")
            print(f"    Trades: {len(trades_full)} ({', '.join(trades_full[:3])}{'...' if len(trades_full) > 3 else ''})")
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    load_tvet_schools()