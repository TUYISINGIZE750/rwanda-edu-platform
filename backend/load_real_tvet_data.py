"""Load real TVET data from Excel"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import pandas as pd
from app.core.database import SessionLocal, Base, engine
from app.models.school import School

file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"

def load_real_data():
    df = pd.read_excel(file_path, engine='openpyxl')
    
    # Skip header row
    df = df.iloc[1:]
    
    # Rename columns
    df.columns = ['Province', 'District', 'SchoolCode', 'SchoolName', 'TradeFull', 'TradeShort', 'Gender']
    
    # Group by school
    schools_dict = {}
    
    for _, row in df.iterrows():
        if pd.isna(row['SchoolCode']) or pd.isna(row['SchoolName']):
            continue
            
        code = str(row['SchoolCode']).strip()
        name = str(row['SchoolName']).strip()
        province = str(row['Province']).strip() if pd.notna(row['Province']) else ""
        district = str(row['District']).strip() if pd.notna(row['District']) else ""
        trade_full = str(row['TradeFull']).strip() if pd.notna(row['TradeFull']) else ""
        trade_short = str(row['TradeShort']).strip() if pd.notna(row['TradeShort']) else ""
        gender = str(row['Gender']).strip() if pd.notna(row['Gender']) else "Mixt"
        
        # Use code as primary key, or code+name if code is duplicate
        key = code
        
        if key not in schools_dict:
            schools_dict[key] = {
                'code': code,
                'name': name,
                'province': province,
                'district': district,
                'gender': gender,
                'trades': []
            }
        
        if trade_full and trade_short:
            schools_dict[key]['trades'].append(f"{trade_full} ({trade_short})")
    
    # Save to database
    db = SessionLocal()
    
    try:
        Base.metadata.create_all(engine)
        
        # Clear existing
        db.query(School).delete()
        db.commit()
        
        school_id = 1
        for school_data in schools_dict.values():
            if not school_data['name'] or not school_data['district']:
                continue
                
            school = School(
                id=school_id,
                name=school_data['name'],
                type="TVET",
                category="Public",
                province=school_data['province'],
                district=school_data['district']
            )
            school.trades = school_data['trades']
            
            db.add(school)
            school_id += 1
            print(f"Added: {school.name} ({school.district}) - {len(school_data['trades'])} trades")
        
        db.commit()
        
        total = db.query(School).count()
        print(f"\nTotal schools loaded: {total}")
        
        # Show by province
        provinces = db.query(School.province).distinct().all()
        for (prov,) in provinces:
            count = db.query(School).filter(School.province == prov).count()
            print(f"  {prov}: {count} schools")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        db.close()
        return False

if __name__ == "__main__":
    print("Loading real TVET data from Excel...")
    print("="*60)
    success = load_real_data()
    if success:
        print("\nDone! Schools loaded successfully.")
    else:
        print("\nFailed to load schools.")
