import psycopg2

DB_CONFIG = {
    'host': 'dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com',
    'port': 5432,
    'database': 'rwanda_edu_db',
    'user': 'rwanda_edu_db_user',
    'password': 'NJmoQ8ze9kV53DT6OB6AAMsa7qetokba'
}

print("Adding DOS users...")
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

with open('insert_dos_users_fixed.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

cursor.execute(sql)
conn.commit()

cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'ADMIN'")
print(f"Total DOS users: {cursor.fetchone()[0]}")

cursor.close()
conn.close()
print("Done!")
