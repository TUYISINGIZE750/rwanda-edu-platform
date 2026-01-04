"""
Seed Production Database - Simple version
"""

import pandas as pd
import psycopg2
import re

DATABASE_URL = "postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db"

excel_file = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"

print("="*60)
print("SEEDING PRODUCTION DATABASE")
print("="*60)

# Parse Excel
print(f"\nReading: {excel_file}")
df = pd.read_excel(excel_file, skiprows=1)

schools_data = {}

for idx, row in df.iterrows():
    school_code = str(row.get('School code ', '')).strip()
    school_name = str(row.get('School Name ', '')).strip()
    trade = str(row.get('Trade in full', '')).strip()
    province = str(row.get('Province', '')).strip()
    district = str(row.get('District ', '')).strip()
    
    if not school_code or school_code == 'nan' or not school_name or school_name == 'nan':
        continue
    
    if school_code not in schools_data:
        schools_data[school_code] = {
            'name': school_name,
            'province': province,
            'district': district,
            'trades': []
        }
    
    if trade and len(trade) > 2 and trade != 'nan':
        trade = re.sub(r'\s+', ' ', trade).strip()
        if trade not in schools_data[school_code]['trades']:
            schools_data[school_code]['trades'].append(trade)

print(f"Parsed {len(schools_data)} unique schools\n")

# Connect
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

inserted = 0

for school_code, data in schools_data.items():
    try:
        # Insert directly
        cur.execute("""
            INSERT INTO schools (name, type, category, province, district, trades)
            VALUES (%s, 'TVET', 'PUBLIC', %s, %s, %s)
            ON CONFLICT (name) DO UPDATE 
            SET trades = EXCLUDED.trades
        """, (data['name'], data['province'], data['district'], data['trades']))
        
        inserted += 1
        if inserted <= 5 or 'RUNDA' in data['name'].upper():
            print(f"  [OK] {data['name']} ({len(data['trades'])} trades)")
    
    except Exception as e:
        print(f"  [ERROR] {data['name']}: {e}")

conn.commit()

print(f"\n{'='*60}")
print(f"[SUCCESS] Processed {inserted} schools")

# Verify
cur.execute("SELECT COUNT(*) FROM schools")
total = cur.fetchone()[0]
print(f"Total schools in database: {total}")

cur.execute("SELECT id, name, trades FROM schools WHERE UPPER(name) LIKE '%RUNDA%'")
runda = cur.fetchall()

if runda:
    print(f"\nRUNDA TVET:")
    for school in runda:
        print(f"  ID: {school[0]}")
        print(f"  Name: {school[1]}")
        print(f"  Trades: {school[2]}")

cur.close()
conn.close()

print(f"\n{'='*60}")
print("[COMPLETE]")
print("="*60)
