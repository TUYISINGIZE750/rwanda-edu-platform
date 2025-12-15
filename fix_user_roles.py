import sqlite3

conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# Update test user roles to uppercase
updates = [
    ('STUDENT', 'student@test.com'),
    ('TEACHER', 'teacher@test.com'), 
    ('ADMIN', 'admin@test.com')
]

for role, email in updates:
    cursor.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
    print(f"Updated {email} role to {role}")

conn.commit()

# Verify the changes
cursor.execute("SELECT email, role FROM users WHERE email IN ('student@test.com', 'teacher@test.com', 'admin@test.com')")
users = cursor.fetchall()

print("\nUpdated user roles:")
for user in users:
    print(f"{user[0]}: {user[1]}")

conn.close()