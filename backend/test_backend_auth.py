import sqlite3
import bcrypt

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Get a test student
cursor.execute("SELECT email, hashed_password FROM users WHERE email = 'teststudent1@school.rw'")
email, stored_hash = cursor.fetchone()

print(f"Email: {email}")
print(f"Stored hash: {stored_hash[:20]}...")
print(f"Hash length: {len(stored_hash)}")

# Test verification
password = 'password123'.encode('utf-8')
try:
    result = bcrypt.checkpw(password, stored_hash.encode('utf-8'))
    print(f"\nPassword verification: {'✓ SUCCESS' if result else '✗ FAILED'}")
except Exception as e:
    print(f"\nPassword verification ERROR: {e}")

conn.close()
