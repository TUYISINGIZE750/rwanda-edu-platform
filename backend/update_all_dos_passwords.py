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

# Generate hash for dos12024
password = "dos12024"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Update ALL DOS users
cursor.execute("UPDATE users SET hashed_password = %s WHERE role = 'ADMIN'", (hashed,))
conn.commit()

print(f"Updated {cursor.rowcount} DOS users")
print(f"Password: {password}")

# Verify
cursor.execute("SELECT email FROM users WHERE role = 'ADMIN' LIMIT 5")
print("\nSample DOS users:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

cursor.close()
conn.close()
