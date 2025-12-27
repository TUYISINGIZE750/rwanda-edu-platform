"""Load official TVET schools from Excel file"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    import pandas as pd
    import openpyxl
except ImportError:
    print("Installing required packages...")
    os.system("pip install pandas openpyxl")
    import pandas as pd
    import openpyxl

from app.core.database import SessionLocal, engine, Base
from app.models.school import School

def parse_and_seed_excel():
    """Parse Excel and seed database"""
    file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Excel file not found: {file_path}")
        return
    
    print("Reading Excel file...")
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        print(f"Found {len(df)} rows in Excel")
        print(f"Columns: {list(df.columns)}")
        
        db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        
        # Clear existing schools
        db.query(School).delete()
        db.commit()
        
        schools_added = 0
        
        for idx, row in df.iterrows():
            # Try to extract school info from row
            # Adjust column names based on actual Excel structure
            school_name = None
            province = None
            district = None
            trades = []
            
            # Try different possible column names
            for col in df.columns:
                col_lower = str(col).lower()
                val = row[col]
                
                if pd.notna(val):
                    val_str = str(val).strip()
                    
                    if 'school' in col_lower or 'name' in col_lower:
                        if not school_name and val_str:
                            school_name = val_str
                    elif 'province' in col_lower:
                        province = val_str
                    elif 'district' in col_lower:
                        district = val_str
                    elif 'trade' in col_lower or 'option' in col_lower:
                        if val_str and val_str not in ['nan', 'None']:
                            trades.append(val_str)
            
            # If we have minimum required info, add school
            if school_name and province and district:
                school = School(
                    name=school_name,
                    type="TVET",
                    category="Public",
                    province=province,
                    district=district,
                    trades=trades if trades else []
                )
                db.add(school)
                schools_added += 1
                print(f"  Added: {school_name} ({district}) - {len(trades)} trades")
        
        db.commit()
        print(f"\nSuccessfully added {schools_added} schools from Excel")
        
        # Show statistics
        total = db.query(School).count()
        print(f"\nDatabase Statistics:")
        print(f"  Total schools: {total}")
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parse_and_seed_excel()
