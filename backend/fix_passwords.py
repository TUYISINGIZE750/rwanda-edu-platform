import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=== Fixing Passwords ===\n")

# Generate correct hash
correct_hash = pwd_context.hash('password123')
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
conn.close()

print("\n=== All passwords updated to 'password123' ===")
