"""
Parse TVET Schools Excel and Seed Database
Reads: 10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os
import sys

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@host/db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def parse_excel_and_seed():
    """Parse Excel file and seed schools with trades"""
    
    # Read Excel file
    excel_file = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"ERROR: Excel file not found: {excel_file}")
        print("Please place the Excel file in the same directory as this script")
        sys.exit(1)
    
    print(f"Reading Excel file: {excel_file}")
    df = pd.read_excel(excel_file)
    
    print(f"\nColumns found: {df.columns.tolist()}")
    print(f"Total rows: {len(df)}")
    
    # Group by school and collect trades
    schools_data = {}
    
    for idx, row in df.iterrows():
        # Extract school info (adjust column names based on actual Excel)
        school_name = str(row.get('SCHOOL NAME', row.get('School', ''))).strip()
        trade = str(row.get('TRADE', row.get('Trade', row.get('OPTION', '')))).strip()
        province = str(row.get('PROVINCE', row.get('Province', ''))).strip()
        district = str(row.get('DISTRICT', row.get('District', ''))).strip()
        
        if not school_name or school_name == 'nan':
            continue
        
        # Create unique key for school
        school_key = f"{school_name}_{province}_{district}"
        
        if school_key not in schools_data:
            schools_data[school_key] = {
                'name': school_name,
                'province': province,
                'district': district,
                'trades': []
            }
        
        if trade and trade != 'nan':
            if trade not in schools_data[school_key]['trades']:
                schools_data[school_key]['trades'].append(trade)
    
    print(f"\nParsed {len(schools_data)} unique schools")
    
    # Show sample
    print("\nSample schools:")
    for i, (key, data) in enumerate(list(schools_data.items())[:3]):
        print(f"{i+1}. {data['name']} - {data['province']}, {data['district']}")
        print(f"   Trades: {', '.join(data['trades'][:5])}")
    
    # Connect to database
    print(f"\nConnecting to database...")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Update schools with trades
        updated_count = 0
        not_found = []
        
        for school_key, data in schools_data.items():
            school_name = data['name']
            trades_json = '{' + ','.join([f'"{t}"' for t in data['trades']]) + '}'
            
            # Try to find and update school
            result = conn.execute(text("""
                UPDATE schools 
                SET trades = :trades::text[]
                WHERE LOWER(name) LIKE LOWER(:name)
                RETURNING id, name
            """), {"trades": trades_json, "name": f"%{school_name}%"})
            
            updated = result.fetchone()
            if updated:
                updated_count += 1
                if 'RUNDA' in school_name.upper():
                    print(f"\n✓ Updated: {updated[1]}")
                    print(f"  Trades: {data['trades']}")
            else:
                not_found.append(school_name)
        
        conn.commit()
        
        print(f"\n{'='*60}")
        print(f"✓ Updated {updated_count} schools with trades")
        print(f"✗ {len(not_found)} schools not found in database")
        
        if not_found[:5]:
            print(f"\nSample not found: {not_found[:5]}")
        
        # Show RUNDA TVET specifically
        result = conn.execute(text("""
            SELECT id, name, province, district, trades
            FROM schools
            WHERE LOWER(name) LIKE '%runda%'
        """))
        
        runda_schools = result.fetchall()
        if runda_schools:
            print(f"\n{'='*60}")
            print("RUNDA TVET Schools:")
            for school in runda_schools:
                print(f"\nID: {school[0]}")
                print(f"Name: {school[1]}")
                print(f"Location: {school[2]}, {school[3]}")
                print(f"Trades: {school[4]}")

if __name__ == "__main__":
    print("="*60)
    print("  TVET Schools Excel Parser & Database Seeder")
    print("="*60)
    
    if len(sys.argv) > 1:
        DATABASE_URL = sys.argv[1]
    else:
        print("\nUsage: python parse_schools_excel.py [DATABASE_URL]")
        print("\nOr set DATABASE_URL environment variable")
        DATABASE_URL = input("\nEnter DATABASE_URL: ").strip()
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    try:
        parse_excel_and_seed()
        print("\n✓ SUCCESS: Schools updated with trades from Excel!")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
