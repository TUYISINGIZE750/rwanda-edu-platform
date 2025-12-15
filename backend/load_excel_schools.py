"""Load schools from Excel file with all required info"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.school import School
import json

def load_excel_schools():
    """Load schools from Excel with district, code, name, trades, gender"""
    db = SessionLocal()
    
    try:
        import pandas as pd
        
        # Read Excel file
        df = pd.read_excel("10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx")
        
        print(f"Excel columns: {list(df.columns)}")
        print(f"Total rows: {len(df)}")
        
        # Clear existing schools
        db.query(School).delete()
        db.commit()
        
        schools_added = 0
        
        for index, row in df.iterrows():
            try:
                # Extract school info
                school_code = str(row.get('School Code', '')).strip()
                school_name = str(row.get('School Name', '')).strip()
                district = str(row.get('District', '')).strip()
                trade_full = str(row.get('Trade (Full)', '')).strip()
                trade_short = str(row.get('Trade (Short)', '')).strip()
                gender = str(row.get('Gender', 'Mixed')).strip()
                
                if not school_name or school_name == 'nan':
                    continue
                
                # Check if school already exists
                existing_school = db.query(School).filter(
                    School.name == school_name,
                    School.district == district
                ).first()
                
                if existing_school:
                    # Add trade to existing school
                    existing_trades = json.loads(existing_school.trades) if existing_school.trades else []
                    if trade_full not in existing_trades:
                        existing_trades.append(trade_full)
                        existing_school.trades = json.dumps(existing_trades)
                else:
                    # Create new school
                    school = School(
                        name=school_name,
                        type="TVET",
                        category="Public",
                        province=get_province_for_district(district),
                        district=district,
                        trades=json.dumps([trade_full]),
                        school_code=school_code,
                        gender_policy=gender
                    )
                    db.add(school)
                    schools_added += 1
                
                if schools_added % 10 == 0:
                    db.commit()
                    
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                continue
        
        db.commit()
        
        print(f"Successfully loaded {schools_added} schools from Excel")
        
        # Verify
        total_schools = db.query(School).count()
        print(f"Total schools in database: {total_schools}")
        
        return True
        
    except ImportError:
        print("pandas not installed. Installing...")
        os.system("pip install pandas openpyxl")
        return load_excel_schools()
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        db.close()

def get_province_for_district(district):
    """Map district to province"""
    district_province_map = {
        # Kigali City
        "Gasabo": "Kigali City", "Kicukiro": "Kigali City", "Nyarugenge": "Kigali City",
        
        # Southern Province
        "Gisagara": "Southern Province", "Huye": "Southern Province", "Kamonyi": "Southern Province",
        "Muhanga": "Southern Province", "Nyamagabe": "Southern Province", "Nyanza": "Southern Province",
        "Nyaruguru": "Southern Province", "Ruhango": "Southern Province",
        
        # Western Province
        "Karongi": "Western Province", "Nyabihu": "Western Province", "Ngororero": "Western Province",
        "Rubavu": "Western Province", "Rusizi": "Western Province", "Nyamasheke": "Western Province",
        "Rutsiro": "Western Province",
        
        # Northern Province
        "Burera": "Northern Province", "Gakenke": "Northern Province", "Gicumbi": "Northern Province",
        "Musanze": "Northern Province", "Rulindo": "Northern Province",
        
        # Eastern Province
        "Bugesera": "Eastern Province", "Gatsibo": "Eastern Province", "Kayonza": "Eastern Province",
        "Kirehe": "Eastern Province", "Ngoma": "Eastern Province", "Nyagatare": "Eastern Province",
        "Rwamagana": "Eastern Province"
    }
    
    return district_province_map.get(district, "Unknown Province")

if __name__ == "__main__":
    success = load_excel_schools()
    if success:
        print("Schools loaded successfully!")
    else:
        print("Failed to load schools!")