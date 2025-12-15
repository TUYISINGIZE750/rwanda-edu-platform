import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=== Checking Test Users ===\n")

# Check teacher
cursor.execute("SELECT id, email, full_name, role, school_id FROM users WHERE email = 'Elam@gmail.com'")
teacher = cursor.fetchone()
if teacher:
    print(f"✓ Teacher: {teacher[1]} (ID={teacher[0]}, Name={teacher[2]}, School={teacher[4]})")
else:
    print("✗ Teacher Elam@gmail.com NOT FOUND")

print()

# Check test students
for i in range(1, 4):
    email = f'teststudent{i}@school.rw'
    cursor.execute("SELECT id, email, full_name, role, school_id FROM users WHERE email = ?", (email,))
    student = cursor.fetchone()
    if student:
        print(f"✓ Student {i}: {student[1]} (ID={student[0]}, Name={student[2]}, School={student[4]})")
    else:
        print(f"✗ Student {email} NOT FOUND")

print("\n=== All users with 'test' in email ===")
cursor.execute("SELECT id, email, full_name, role, school_id FROM users WHERE email LIKE '%test%'")
for row in cursor.fetchall():
    print(f"ID={row[0]}, Email={row[1]}, Name={row[2]}, Role={row[3]}, School={row[4]}")

conn.close()
