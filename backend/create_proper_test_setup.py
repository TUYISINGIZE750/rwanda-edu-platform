"""Create proper test setup with teacher and students in same school"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("="*80)
print("CREATING PROPER TEST SETUP")
print("="*80)

# Find teacher HAKIZIMANA Elam
cursor.execute("SELECT id, full_name, email, school_id FROM users WHERE id = 94")
teacher = cursor.fetchone()

if not teacher:
    print("ERROR: Teacher not found!")
    conn.close()
    exit(1)

teacher_school = teacher[3]
print(f"\nTeacher: {teacher[1]} (School: {teacher_school})")

# Create 3 test students in the same school as teacher
test_students = [
    ("Test Student 1", "teststudent1@school.rw", "Land surveying", "Level 3"),
    ("Test Student 2", "teststudent2@school.rw", "Land surveying", "Level 3"),
    ("Test Student 3", "teststudent3@school.rw", "Land surveying", "Level 3")
]

student_ids = []
for name, email, trade, level in test_students:
    # Check if exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    existing = cursor.fetchone()
    
    if existing:
        student_ids.append(existing[0])
        print(f"Student exists: {name} (ID: {existing[0]})")
    else:
        # Create student
        cursor.execute("""
            INSERT INTO users (full_name, email, hashed_password, role, school_id, 
                             selected_trade, selected_level, province, district, created_at)
            VALUES (?, ?, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfYGEujnK2', 
                    'STUDENT', ?, ?, ?, 'Kigali', 'Gasabo', datetime('now'))
        """, (name, email, teacher_school, trade, level))
        student_ids.append(cursor.lastrowid)
        print(f"Created student: {name} (ID: {cursor.lastrowid})")

conn.commit()

# Create test group
cursor.execute("""
    INSERT INTO groups (name, type, department, school_id, created_at)
    VALUES ('L3 LSV - Teacher Test Group', 'CLASS', 'Land Surveying', ?, datetime('now'))
""", (teacher_school,))

group_id = cursor.lastrowid
print(f"\nCreated group: L3 LSV - Teacher Test Group (ID: {group_id})")

# Create channels
channels = [
    ('General Discussion', 'DISCUSSION'),
    ('Announcements', 'ANNOUNCEMENTS'),
    ('Resources', 'RESOURCES')
]

channel_ids = []
for channel_name, channel_type in channels:
    cursor.execute("""
        INSERT INTO channels (name, type, group_id, created_at)
        VALUES (?, ?, ?, datetime('now'))
    """, (channel_name, channel_type, group_id))
    channel_ids.append(cursor.lastrowid)
    print(f"  Created channel: {channel_name}")

# Enroll teacher
cursor.execute("""
    INSERT OR IGNORE INTO group_members (group_id, user_id, joined_at)
    VALUES (?, ?, datetime('now'))
""", (group_id, teacher[0]))
print(f"\nEnrolled teacher: {teacher[1]}")

# Enroll students
for student_id in student_ids:
    cursor.execute("""
        INSERT OR IGNORE INTO group_members (group_id, user_id, joined_at)
        VALUES (?, ?, datetime('now'))
    """, (group_id, student_id))
    cursor.execute("SELECT full_name FROM users WHERE id = ?", (student_id,))
    student_name = cursor.fetchone()[0]
    print(f"Enrolled student: {student_name}")

conn.commit()

# Get all members
cursor.execute("""
    SELECT u.full_name, u.role, u.email, u.school_id
    FROM group_members gm
    JOIN users u ON gm.user_id = u.id
    WHERE gm.group_id = ?
    ORDER BY u.role DESC, u.full_name
""", (group_id,))

members = cursor.fetchall()

print("\n" + "="*80)
print("GROUP MEMBERS:")
print("="*80)
for name, role, email, school in members:
    print(f"  {role}: {name} ({email}) - School {school}")

print("\n" + "="*80)
print("TEST CREDENTIALS:")
print("="*80)
print(f"\nTeacher Login:")
print(f"  Email: {teacher[2]}")
print(f"  Password: password123")
print(f"  URL: http://localhost:5173/hubs/{group_id}")

print(f"\nStudent Logins (all use password: password123):")
for name, email, _, _ in test_students:
    print(f"  {name}: {email}")

print(f"\nGroup URL: http://localhost:5173/hubs/{group_id}")
print("="*80)

conn.close()
