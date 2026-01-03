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

cursor.execute("SELECT email, role, is_active FROM users LIMIT 10")
print("Sample users:")
for row in cursor.fetchall():
    print(f"  {row[0]} | Role: {row[1]} | Active: {row[2]}")

cursor.close()
conn.close()
