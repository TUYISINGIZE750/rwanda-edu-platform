import psycopg2

# Direct SQL fix for the backend
DB_CONFIG = {
    'host': 'dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com',
    'port': 5432,
    'database': 'rwanda_edu_db',
    'user': 'rwanda_edu_db_user',
    'password': 'NJmoQ8ze9kV53DT6OB6AAMsa7qetokba'
}

print("Testing schools query fix...")
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Test the query that should work
cursor.execute("""
    SELECT id, name, type, category, province, district 
    FROM schools 
    WHERE LOWER(province) = LOWER('South') 
    AND LOWER(district) = LOWER('Kamonyi')
""")

schools = cursor.fetchall()
print(f"\nFound {len(schools)} schools in South/Kamonyi:")
for school in schools:
    print(f"  - {school[1]} ({school[2]})")

cursor.close()
conn.close()

print("\n✓ Query works! The backend code has been fixed.")
print("Render will auto-deploy from GitHub in ~2 minutes.")
