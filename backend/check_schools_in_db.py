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

# Check schools table
cursor.execute("SELECT COUNT(*) FROM schools")
total = cursor.fetchone()[0]
print(f"Total schools in database: {total}")

# Check sample schools by province/district
cursor.execute("""
    SELECT DISTINCT province, district, COUNT(*) 
    FROM schools 
    GROUP BY province, district 
    ORDER BY province, district
    LIMIT 10
""")
print("\nSample schools by province/district:")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}: {row[2]} schools")

# Check specific district
cursor.execute("""
    SELECT id, name, province, district 
    FROM schools 
    WHERE LOWER(province) = 'east' AND LOWER(district) = 'bugesera'
    LIMIT 5
""")
print("\nSample schools in East/BUGESERA:")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, Name: {row[1]}, Province: {row[2]}, District: {row[3]}")

cursor.close()
conn.close()
