import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=== Activating Accounts ===\n")

# Activate test students
for i in range(1, 4):
    email = f'teststudent{i}@school.rw'
    cursor.execute("UPDATE users SET is_active = 1 WHERE email = ?", (email,))
    print(f"✓ Activated {email}")

# Activate teacher
cursor.execute("UPDATE users SET is_active = 1 WHERE email = ?", ('Elam@gmail.com',))
print(f"✓ Activated Elam@gmail.com")

conn.commit()

# Verify
print("\n=== Verification ===")
for i in range(1, 4):
    email = f'teststudent{i}@school.rw'
    cursor.execute("SELECT is_active FROM users WHERE email = ?", (email,))
    is_active = cursor.fetchone()[0]
    print(f"{email}: {'✓ ACTIVE' if is_active else '✗ INACTIVE'}")

cursor.execute("SELECT is_active FROM users WHERE email = 'Elam@gmail.com'")
is_active = cursor.fetchone()[0]
print(f"Elam@gmail.com: {'✓ ACTIVE' if is_active else '✗ INACTIVE'}")

conn.close()
print("\n=== All accounts activated ===")
