import psycopg2
import bcrypt

DB_CONFIG = {
    'host': 'dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com',
    'port': 5432,
    'database': 'rwanda_edu_db',
    'user': 'rwanda_edu_db_user',
    'password': 'NJmoQ8ze9kV53DT6OB6AAMsa7qetokba'
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Delete old DOS user
cursor.execute("DELETE FROM users WHERE email = 'dos@tssanywhere.rw'")

# Create new DOS user with exact same structure as working students
password = "dos123"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

cursor.execute("""
    INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, is_active)
    VALUES ('dos@tssanywhere.rw', %s, 'DOS Admin', 'ADMIN', 1, 'East', 'Bugesera', 1)
""", (hashed,))

conn.commit()
print("DOS user created: dos@tssanywhere.rw / dos123")

# Test it works
cursor.execute("SELECT email, role, is_active FROM users WHERE email = 'dos@tssanywhere.rw'")
row = cursor.fetchone()
print(f"Verified: {row[0]} | Role: {row[1]} | Active: {row[2]}")

cursor.close()
conn.close()
