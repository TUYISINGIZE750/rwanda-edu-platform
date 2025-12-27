import sys
import os
sys.path.append(os.path.dirname(__file__))

import pandas as pd
from app.core.database import SessionLocal, engine, Base
from app.models.school import School
from collections import defaultdict

def seed_schools():
    file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    print("Reading Excel...")
    df = pd.read_excel(file_path, engine='openpyxl')
    
    # Skip first row (headers)
    df = df.iloc[1:]
    
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)
    
    # Clear existing
    db.query(School).delete()
    db.commit()
    
    # Group by school
    schools_dict = defaultdict(lambda: {'trades': [], 'info': {}})
    
    for _, row in df.iterrows():
        province = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else None
        district = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else None
        school_code = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else None
        school_name = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else None
        trade_full = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else None
        trade_code = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else None
        gender = str(row.iloc[6]).strip() if pd.notna(row.iloc[6]) else None
        
        if school_name and province and district:
            key = f"{school_code}_{school_name}"
            schools_dict[key]['info'] = {
                'name': school_name,
                'code': school_code,
                'province': province,
                'district': district,
                'gender': gender
            }
            if trade_full and trade_full != 'nan':
                schools_dict[key]['trades'].append(trade_full)
    
    # Add to database
    count = 0
    for key, data in schools_dict.items():
        info = data['info']
        trades = list(set(data['trades']))  # Remove duplicates
        
        school = School(
            name=info['name'],
            type='TVET',
            category='Public',
            province=info['province'],
            district=info['district'],
            trades=trades
        )
        db.add(school)
        count += 1
        print(f"Added: {info['name']} ({info['district']}) - {len(trades)} trades")
    
    db.commit()
    print(f"\nTotal schools added: {count}")
    
    # Verify
    total = db.query(School).count()
    print(f"Database total: {total}")
    
    db.close()

if __name__ == "__main__":
    seed_schools()
