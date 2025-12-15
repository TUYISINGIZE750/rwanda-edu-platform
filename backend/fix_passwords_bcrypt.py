import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')
import bcrypt

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=== Fixing Passwords ===\n")

# Generate correct hash using bcrypt directly
password = 'password123'.encode('utf-8')
correct_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
print(f"New hash generated (length={len(correct_hash)})\n")

# Fix test students
for i in range(1, 4):
    email = f'teststudent{i}@school.rw'
    cursor.execute("UPDATE users SET hashed_password = ? WHERE email = ?", (correct_hash, email))
    print(f"✓ Fixed password for {email}")

# Fix teacher
cursor.execute("UPDATE users SET hashed_password = ? WHERE email = ?", (correct_hash, 'Elam@gmail.com'))
print(f"✓ Fixed password for Elam@gmail.com")

conn.commit()

# Verify
print("\n=== Verifying ===")
for i in range(1, 4):
    email = f'teststudent{i}@school.rw'
    cursor.execute("SELECT hashed_password FROM users WHERE email = ?", (email,))
    stored_hash = cursor.fetchone()[0]
    result = bcrypt.checkpw(password, stored_hash.encode('utf-8'))
    print(f"{email}: {'✓ WORKS' if result else '✗ FAILS'}")

cursor.execute("SELECT hashed_password FROM users WHERE email = 'Elam@gmail.com'")
stored_hash = cursor.fetchone()[0]
result = bcrypt.checkpw(password, stored_hash.encode('utf-8'))
print(f"Elam@gmail.com: {'✓ WORKS' if result else '✗ FAILS'}")

conn.close()
print("\n=== All passwords updated to 'password123' ===")
