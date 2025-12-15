"""Create test group for teacher and student to chat"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("="*80)
print("CREATING TEST CHAT GROUP")
print("="*80)

# Find teacher HAKIZIMANA Elam
cursor.execute("SELECT id, full_name, email, school_id FROM users WHERE full_name LIKE '%HAKIZIMANA%' AND role = 'TEACHER'")
teacher = cursor.fetchone()

if not teacher:
    print("\nTeacher HAKIZIMANA not found. Looking for any teacher in school 63...")
    cursor.execute("SELECT id, full_name, email, school_id FROM users WHERE role = 'TEACHER' AND school_id = 63 LIMIT 1")
    teacher = cursor.fetchone()

# Find student KAMANYOLA Isdore
cursor.execute("SELECT id, full_name, email, school_id FROM users WHERE id = 97")
student = cursor.fetchone()

if not teacher:
    print("\nERROR: No teacher found!")
    conn.close()
    exit(1)

if not student:
    print("\nERROR: Student KAMANYOLA not found!")
    conn.close()
    exit(1)

print(f"\nTeacher: {teacher[1]} (ID: {teacher[0]}, School: {teacher[3]})")
print(f"Student: {student[1]} (ID: {student[0]}, School: {student[3]})")

# Use the same school as the student
school_id = student[3]

# Create group
cursor.execute("""
    INSERT INTO groups (name, type, department, school_id, created_at)
    VALUES ('L3 LSV Test Chat', 'CLASS', 'Land Surveying', ?, datetime('now'))
""", (school_id,))

group_id = cursor.lastrowid
print(f"\nCreated group: L3 LSV Test Chat (ID: {group_id}, School: {school_id})")

# Create channels
channels = [
    ('General Discussion', 'DISCUSSION'),
    ('Announcements', 'ANNOUNCEMENTS'),
    ('Resources', 'RESOURCES')
]

for channel_name, channel_type in channels:
    cursor.execute("""
        INSERT INTO channels (name, type, group_id, created_at)
        VALUES (?, ?, ?, datetime('now'))
    """, (channel_name, channel_type, group_id))
    print(f"  Created channel: {channel_name} ({channel_type})")

# Enroll teacher
cursor.execute("""
    INSERT OR IGNORE INTO group_members (group_id, user_id, joined_at)
    VALUES (?, ?, datetime('now'))
""", (group_id, teacher[0]))
print(f"\nEnrolled teacher: {teacher[1]}")

# Enroll student
cursor.execute("""
    INSERT OR IGNORE INTO group_members (group_id, user_id, joined_at)
    VALUES (?, ?, datetime('now'))
""", (group_id, student[0]))
print(f"Enrolled student: {student[1]}")

# Also enroll other L3 Land surveying students
cursor.execute("""
    SELECT id, full_name FROM users 
    WHERE role = 'STUDENT' 
    AND school_id = ?
    AND selected_level LIKE '%3%'
    AND selected_trade LIKE '%Land%'
    AND id != ?
""", (school_id, student[0]))

other_students = cursor.fetchall()
for s_id, s_name in other_students:
    cursor.execute("""
        INSERT OR IGNORE INTO group_members (group_id, user_id, joined_at)
        VALUES (?, ?, datetime('now'))
    """, (group_id, s_id))
    print(f"Enrolled student: {s_name}")

conn.commit()

# Verify
cursor.execute("""
    SELECT u.full_name, u.role, u.email
    FROM group_members gm
    JOIN users u ON gm.user_id = u.id
    WHERE gm.group_id = ?
    ORDER BY u.role DESC, u.full_name
""", (group_id,))

members = cursor.fetchall()

print("\n" + "="*80)
print("GROUP MEMBERS:")
print("="*80)
for name, role, email in members:
    print(f"  {role.upper()}: {name} ({email})")

print("\n" + "="*80)
print("TEST INSTRUCTIONS:")
print("="*80)
print(f"\nTeacher Login:")
print(f"  Email: {teacher[2]}")
print(f"  Password: password123")
print(f"  Go to: http://localhost:5173/hubs/{group_id}")

print(f"\nStudent Login:")
print(f"  Email: {student[2]}")
print(f"  Password: password123")
print(f"  Go to: http://localhost:5173/hubs/{group_id}")

print("\nBoth users can now chat in real-time!")
print("="*80)

conn.close()
