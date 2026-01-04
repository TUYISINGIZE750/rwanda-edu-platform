"""
Seed Production Database with 164 TVET Schools
Run this to populate the production database
"""

import pandas as pd
import psycopg2
import re

# Production database URL
DATABASE_URL = "postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db"

excel_file = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"

print("="*60)
print("SEEDING PRODUCTION DATABASE")
print("="*60)

# Parse Excel
print(f"\nReading: {excel_file}")
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
    
    if school_code not in schools_data:
        schools_data[school_code] = {
            'code': school_code,
            'name': school_name,
            'province': province,
            'district': district,
            'trades': []
        }
    
    if trade and len(trade) > 2 and trade != 'nan':
        trade = re.sub(r'\s+', ' ', trade).strip()
        if trade not in schools_data[school_code]['trades']:
            schools_data[school_code]['trades'].append(trade)

print(f"\nParsed {len(schools_data)} unique schools")

# Connect to production database
print("\nConnecting to production database...")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Insert schools
inserted = 0
updated = 0

for school_code, data in schools_data.items():
    try:
        # Check if school exists
        cur.execute("SELECT id FROM schools WHERE school_code = %s", (school_code,))
        existing = cur.fetchone()
        
        if existing:
            # Update
            cur.execute("""
                UPDATE schools 
                SET name = %s, province = %s, district = %s, trades = %s
                WHERE school_code = %s
            """, (data['name'], data['province'], data['district'], data['trades'], school_code))
            updated += 1
        else:
            # Insert
            cur.execute("""
                INSERT INTO schools (school_code, name, type, category, province, district, trades)
                VALUES (%s, %s, 'TVET', 'PUBLIC', %s, %s, %s)
            """, (school_code, data['name'], data['province'], data['district'], data['trades']))
            inserted += 1
        
        if (inserted + updated) <= 5 or 'RUNDA' in data['name'].upper():
            print(f"  [OK] {data['name']} ({len(data['trades'])} trades)")
    
    except Exception as e:
        print(f"  [ERROR] {data['name']}: {e}")

conn.commit()

print(f"\n{'='*60}")
print(f"[SUCCESS] Inserted: {inserted}, Updated: {updated}")
print(f"Total: {inserted + updated} schools")

# Verify RUNDA
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

print(f"\n{'='*60}")
print("[COMPLETE] Production database seeded!")
print("="*60)
