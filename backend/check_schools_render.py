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

cursor.execute("SELECT COUNT(*) FROM schools")
print(f"Total schools: {cursor.fetchone()[0]}")

cursor.execute("SELECT province, district, COUNT(*) FROM schools GROUP BY province, district ORDER BY province, district")
for row in cursor.fetchall():
    print(f"{row[0]} - {row[1]}: {row[2]} schools")

cursor.close()
conn.close()
