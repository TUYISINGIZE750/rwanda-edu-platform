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

cursor.execute("SELECT email, full_name, role FROM users WHERE email = 'kayenzi_tvet_school@tssanywhere.rw'")
row = cursor.fetchone()
if row:
    print(f"User found: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"Role: {row[2]}")
else:
    print("User not found!")

cursor.close()
conn.close()
