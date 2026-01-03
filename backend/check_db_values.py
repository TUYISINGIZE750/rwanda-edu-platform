import psycopg2

DB_CONFIG = {
    'host': 'dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com',
    'port': 5432,
    'database': 'rwanda_edu_db',
    'user': 'rwanda_edu_db_user',
    'password': 'NJmoQ8ze9kV53DT6OB6AAMsa7qetokba'
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Check what's actually in the database
cursor.execute("SELECT DISTINCT province FROM schools ORDER BY province")
print("Provinces in DB:")
for row in cursor.fetchall():
    print(f"  '{row[0]}'")

cursor.execute("SELECT province, district, name FROM schools WHERE district = 'Gasabo'")
print("\nGasabo schools:")
for row in cursor.fetchall():
    print(f"  Province: '{row[0]}' | District: '{row[1]}' | School: {row[2]}")

cursor.close()
conn.close()
