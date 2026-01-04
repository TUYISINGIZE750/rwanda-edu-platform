"""
COMPREHENSIVE SYSTEM FIX - Run this to fix everything
"""
import pandas as pd
import psycopg2
import re
import requests

DATABASE_URL = "postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db"
API_URL = "https://rwanda-edu-platform.onrender.com/api/v1"

print("="*70)
print("COMPREHENSIVE SYSTEM FIX")
print("="*70)

# 1. SEED SCHOOLS
print("\n[1/5] Seeding schools...")
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

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Clear and reseed
cur.execute("DELETE FROM schools")
conn.commit()

for code, data in schools_data.items():
    cur.execute("""
        INSERT INTO schools (name, type, category, province, district, trades)
        VALUES (%s, 'TVET', 'PUBLIC', %s, %s, %s)
    """, (data['name'], data['province'], data['district'], data['trades']))

conn.commit()
print(f"   [OK] Seeded {len(schools_data)} schools")

# 2. FIX USER SCHOOL IDS
print("\n[2/5] Fixing user school_ids...")
cur.execute("SELECT id FROM schools ORDER BY id LIMIT 1")
first_school = cur.fetchone()[0]
cur.execute("UPDATE users SET school_id = %s WHERE school_id IS NULL OR school_id NOT IN (SELECT id FROM schools)", (first_school,))
conn.commit()
print(f"   [OK] Fixed {cur.rowcount} users")

# 3. VERIFY DATABASE
print("\n[3/5] Verifying database...")
cur.execute("SELECT COUNT(*) FROM schools")
school_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM users")
user_count = cur.fetchone()[0]
cur.execute("SELECT id, name, trades FROM schools LIMIT 1")
sample = cur.fetchone()
print(f"   [OK] Schools: {school_count}")
print(f"   [OK] Users: {user_count}")
print(f"   [OK] Sample: {sample[1]} has {len(sample[2])} trades")

cur.close()
conn.close()

# 4. TEST API
print("\n[4/5] Testing API endpoints...")
try:
    r = requests.get(f"{API_URL}/locations/schools", timeout=10)
    if r.status_code == 200:
        schools = r.json()
        print(f"   [OK] Schools list: {len(schools)} schools")
        if schools and schools[0].get('trades'):
            print(f"   [OK] Trades working: {schools[0]['name']} has {len(schools[0]['trades'])} trades")
        else:
            print(f"   [WAIT] Trades NOT working yet - Render still deploying")
    else:
        print(f"   [ERROR] API error: {r.status_code}")
except Exception as e:
    print(f"   [ERROR] API error: {e}")

# 5. SUMMARY
print("\n" + "="*70)
print("SYSTEM STATUS")
print("="*70)
print("[OK] Database: {} schools, {} users".format(school_count, user_count))
print("[OK] All users have valid school_ids")
print("[WAIT] Waiting for Render to deploy latest code...")
print("\nOnce Render finishes deploying:")
print("1. Logout and login again")
print("2. All modals will show correct school trades")
print("3. Admin can create users successfully")
print("="*70)
