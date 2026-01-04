import pandas as pd
import psycopg2
import re

DATABASE_URL = "postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db"

df = pd.read_excel("10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx", skiprows=1)

schools_data = {}

for idx, row in df.iterrows():
    code = str(row.get('School code ', '')).strip()
    name = str(row.get('School Name ', '')).strip()
    trade = str(row.get('Trade in full', '')).strip()
    province = str(row.get('Province', '')).strip()
    district = str(row.get('District ', '')).strip()
    
    if not code or code == 'nan' or not name or name == 'nan':
        continue
    
    if code not in schools_data:
        schools_data[code] = {'name': name, 'province': province, 'district': district, 'trades': []}
    
    if trade and len(trade) > 2 and trade != 'nan':
        trade = re.sub(r'\s+', ' ', trade).strip()
        if trade not in schools_data[code]['trades']:
            schools_data[code]['trades'].append(trade)

print(f"Seeding {len(schools_data)} schools...")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

for code, data in schools_data.items():
    try:
        cur.execute("""
            INSERT INTO schools (name, type, category, province, district, trades)
            VALUES (%s, 'TVET', 'PUBLIC', %s, %s, %s)
        """, (data['name'], data['province'], data['district'], data['trades']))
    except Exception as e:
        pass

conn.commit()

cur.execute("SELECT COUNT(*) FROM schools")
print(f"Total schools: {cur.fetchone()[0]}")

cur.execute("SELECT id, name, trades FROM schools WHERE UPPER(name) LIKE '%RUNDA%'")
runda = cur.fetchall()
if runda:
    for s in runda:
        print(f"\nRUNDA TVET (ID: {s[0]})")
        print(f"Trades: {s[2]}")

cur.close()
conn.close()
print("\nDONE!")
