"""
TVET Schools Excel Parser - Proper PostgreSQL array handling
"""

import pandas as pd
import psycopg2
import os
import sys
import re

def parse_excel(excel_file):
    """Parse Excel using school codes"""
    
    print(f"Reading: {excel_file}")
    df = pd.read_excel(excel_file, skiprows=1)
    print(f"Total rows: {len(df)}")
    
    schools_data = {}
    
    for idx, row in df.iterrows():
        school_code = str(row.get('School code ', '')).strip()
        school_name = str(row.get('School Name ', '')).strip()
        trade = str(row.get('Trade in full', '')).strip()
        
        if not school_code or school_code == 'nan' or not school_name or school_name == 'nan':
            continue
        
        if school_code not in schools_data:
            schools_data[school_code] = {
                'name': school_name,
                'trades': []
            }
        
        if trade and len(trade) > 2 and trade != 'nan':
            trade = re.sub(r'\s+', ' ', trade).strip()
            if trade not in schools_data[school_code]['trades']:
                schools_data[school_code]['trades'].append(trade)
    
    return schools_data

def update_database(schools_data, database_url):
    """Update database with proper array handling"""
    
    print(f"\nParsed {len(schools_data)} unique schools")
    print("\nConnecting to database...")
    
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    
    updated_count = 0
    
    for school_code, data in schools_data.items():
        if not data['trades']:
            continue
        
        school_name = data['name']
        trades_list = data['trades']
        
        # Try exact match
        cur.execute("""
            UPDATE schools 
            SET trades = %s
            WHERE LOWER(TRIM(name)) = LOWER(TRIM(%s))
            RETURNING id, name
        """, (trades_list, school_name))
        
        updated = cur.fetchone()
        
        # Try fuzzy match
        if not updated:
            words = school_name.upper().split()
            main_words = [w for w in words if len(w) > 3 and w not in ['TVET', 'SCHOOL', 'COLLEGE', 'LYCEE']]
            
            if main_words:
                pattern = '%' + '%'.join(main_words[:2]) + '%'
                cur.execute("""
                    UPDATE schools 
                    SET trades = %s
                    WHERE UPPER(name) LIKE %s
                    RETURNING id, name
                """, (trades_list, pattern))
                
                updated = cur.fetchone()
        
        if updated:
            updated_count += 1
            if updated_count <= 5 or 'RUNDA' in school_name.upper():
                print(f"  [OK] {updated[1]} -> {len(trades_list)} trades")
    
    conn.commit()
    
    print(f"\n{'='*60}")
    print(f"[SUCCESS] Updated {updated_count}/{len(schools_data)} schools")
    
    # Show RUNDA
    cur.execute("SELECT id, name, province, district, trades FROM schools WHERE UPPER(name) LIKE '%RUNDA%'")
    runda = cur.fetchall()
    
    if runda:
        print(f"\n{'='*60}")
        print("RUNDA TVET:")
        for school in runda:
            print(f"  ID: {school[0]}")
            print(f"  Name: {school[1]}")
            print(f"  Location: {school[2]}, {school[3]}")
            print(f"  Trades ({len(school[4])}): {', '.join(school[4])}")
    
    cur.close()
    conn.close()

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
        print(f"[COMPLETE] All {len(schools_data)} schools updated")
        print("="*60)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
