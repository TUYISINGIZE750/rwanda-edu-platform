import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=== Verifying Passwords ===\n")

# Check test students
for i in range(1, 4):
    email = f'teststudent{i}@school.rw'
    cursor.execute("SELECT id, email, hashed_password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user:
        user_id, user_email, hashed_pw = user
        print(f"Student {i}: {user_email} (ID={user_id})")
        print(f"  Hash exists: {bool(hashed_pw)}")
        print(f"  Hash length: {len(hashed_pw) if hashed_pw else 0}")
        
        # Test password
        try:
            result = pwd_context.verify('password123', hashed_pw)
            print(f"  Password 'password123': {'CORRECT' if result else 'WRONG'}")
        except Exception as e:
            print(f"  Error verifying: {e}")
        print()

# Check teacher
cursor.execute("SELECT id, email, hashed_password FROM users WHERE email = 'Elam@gmail.com'")
teacher = cursor.fetchone()
if teacher:
    user_id, user_email, hashed_pw = teacher
    print(f"Teacher: {user_email} (ID={user_id})")
    print(f"  Hash exists: {bool(hashed_pw)}")
    print(f"  Hash length: {len(hashed_pw) if hashed_pw else 0}")
    
    try:
        result = pwd_context.verify('password123', hashed_pw)
        print(f"  Password 'password123': {'CORRECT' if result else 'WRONG'}")
    except Exception as e:
        print(f"  Error verifying: {e}")

conn.close()
