import sqlite3
import bcrypt
from datetime import datetime

# Connect to database
conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# Hash password
password = "test123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Create test users
test_users = [
    {
        'email': 'student@test.com',
        'password': hashed,
        'full_name': 'Test Student',
        'role': 'student',
        'school_id': 1,
        'province': 'Kigali City',
        'district': 'Gasabo',
        'selected_trade': 'Electronics',
        'selected_level': 'Level 2',
        'locale': 'en'
    },
    {
        'email': 'teacher@test.com', 
        'password': hashed,
        'full_name': 'Test Teacher',
        'role': 'teacher',
        'school_id': 1,
        'province': 'Kigali City',
        'district': 'Gasabo',
        'locale': 'en'
    },
    {
        'email': 'admin@test.com',
        'password': hashed, 
        'full_name': 'Test Admin',
        'role': 'admin',
        'school_id': 1,
        'province': 'Kigali City',
        'district': 'Gasabo',
        'locale': 'en'
    }
]

# Insert test users
for user in test_users:
    try:
        cursor.execute("""
            INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, 
                             selected_trade, selected_level, locale, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (
            user['email'], user['password'], user['full_name'], user['role'], 
            user['school_id'], user['province'], user['district'],
            user.get('selected_trade'), user.get('selected_level'), user['locale'],
            datetime.now(), datetime.now()
        ))
        print(f"Created user: {user['email']} ({user['role']})")
    except sqlite3.IntegrityError:
        print(f"User {user['email']} already exists")

conn.commit()
conn.close()

print("\nTest users created!")
print("Login credentials:")
print("Student: student@test.com / test123")
print("Teacher: teacher@test.com / test123") 
print("Admin: admin@test.com / test123")