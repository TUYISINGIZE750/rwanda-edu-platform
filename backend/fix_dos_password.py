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

# Generate fresh hash
password = "dos12024"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Update or insert user
cursor.execute("""
    INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, is_active)
    VALUES ('nyamata_tvet_school_1@tssanywhere.rw', %s, 'DOS - NYAMATA TVET SCHOOL', 'ADMIN', 570702, 'East', 'Bugesera', 1)
    ON CONFLICT (email) DO UPDATE SET hashed_password = EXCLUDED.hashed_password
""", (hashed,))

conn.commit()

# Verify
cursor.execute("SELECT email, role FROM users WHERE email = 'nyamata_tvet_school_1@tssanywhere.rw'")
row = cursor.fetchone()
print(f"User: {row[0]}, Role: {row[1]}")

cursor.close()
conn.close()
print("Password updated!")
