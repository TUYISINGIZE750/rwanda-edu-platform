"""
TVET Schools Excel Parser - Uses school codes for accurate identification
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os
import sys
import re

def parse_excel(excel_file):
    """Parse Excel using school codes for accurate identification"""
    
    print(f"Reading: {excel_file}")
    df = pd.read_excel(excel_file, skiprows=1)
    print(f"Total rows: {len(df)}")
    
    schools_data = {}
    
    for idx, row in df.iterrows():
        school_code = str(row.get('School code ', '')).strip()
        school_name = str(row.get('School Name ', '')).strip()
        trade = str(row.get('Trade in full', '')).strip()
        province = str(row.get('Province', '')).strip()
        district = str(row.get('District ', '')).strip()
        
        if not school_code or school_code == 'nan' or not school_name or school_name == 'nan':
            continue
        
        # Use school code as unique identifier
        if school_code not in schools_data:
            schools_data[school_code] = {
                'name': school_name,
                'province': province,
                'district': district,
                'trades': []
            }
        
        # Add trade
        if trade and len(trade) > 2 and trade != 'nan':
            trade = re.sub(r'\s+', ' ', trade).strip()
            if trade not in schools_data[school_code]['trades']:
                schools_data[school_code]['trades'].append(trade)
    
    return schools_data

def update_database(schools_data, database_url):
    """Update database with all schools"""
    
    print(f"\nParsed {len(schools_data)} unique schools (by school code)")
    
    print("\nFirst 5 schools:")
    for i, (code, data) in enumerate(list(schools_data.items())[:5]):
        print(f"  {i+1}. [{code}] {data['name']} ({len(data['trades'])} trades)")
    
    print(f"\nConnecting to database...")
    engine = create_engine(database_url)
    
    updated_count = 0
    not_found = []
    
    with engine.connect() as conn:
        for school_code, data in schools_data.items():
            if not data['trades']:
                continue
            
            trades_list = data['trades']
            school_name = data['name']
            
            # Try exact match
            result = conn.execute(text("""
                UPDATE schools 
                SET trades = ARRAY[:trades]
                WHERE LOWER(TRIM(name)) = LOWER(TRIM(:name))
                RETURNING id, name
            """), {"trades": trades_list, "name": school_name})
            
            updated = result.fetchone()
            
            # Try fuzzy match
            if not updated:
                words = school_name.upper().split()
                main_words = [w for w in words if len(w) > 3 and w not in ['TVET', 'SCHOOL', 'COLLEGE', 'LYCEE']]
                
                if main_words:
                    pattern = '%' + '%'.join(main_words[:2]) + '%'
                    result = conn.execute(text("""
                        UPDATE schools 
                        SET trades = ARRAY[:trades]
                        WHERE UPPER(name) LIKE :pattern
                        RETURNING id, name
                    """), {"trades": trades_list, "pattern": pattern})
                    
                    updated = result.fetchone()
            
            if updated:
                updated_count += 1
                if updated_count <= 5 or 'RUNDA' in school_name.upper():
                    print(f"  [OK] {updated[1]} -> {len(trades_list)} trades")
            else:
                not_found.append(school_name)
        
        conn.commit()
    
    print(f"\n{'='*60}")
    print(f"[SUCCESS] Updated {updated_count}/{len(schools_data)} schools")
    
    if not_found:
        print(f"[INFO] {len(not_found)} schools from Excel not in database")
    
    # Show RUNDA
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, name, province, district, trades
            FROM schools
            WHERE UPPER(name) LIKE '%RUNDA%'
        """))
        
        runda = result.fetchall()
        if runda:
            print(f"\n{'='*60}")
            print("RUNDA TVET:")
            for school in runda:
                print(f"  ID: {school[0]}")
                print(f"  Name: {school[1]}")
                print(f"  Location: {school[2]}, {school[3]}")
                print(f"  Trades: {school[4]}")

if __name__ == "__main__":
    print("="*60)
    print("  TVET Schools Excel Parser (164 Schools)")
    print("="*60)
    
    if len(sys.argv) > 1:
        DATABASE_URL = sys.argv[1]
    else:
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            DATABASE_URL = input("\nEnter DATABASE_URL: ").strip()
    
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and 'TVET' in f.upper()]
    
    if not excel_files:
        print("\n[ERROR] No TVET Excel file found")
        sys.exit(1)
    
    excel_file = excel_files[0]
    
    try:
        schools_data = parse_excel(excel_file)
        update_database(schools_data, DATABASE_URL)
        print("\n" + "="*60)
        print(f"[COMPLETE] Processed all {len(schools_data)} schools from Excel")
        print("="*60)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
