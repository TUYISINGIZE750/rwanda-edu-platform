"""Debug script to check groups and student data"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=" * 60)
print("STUDENTS:")
print("=" * 60)
cursor.execute("SELECT id, full_name, email, selected_trade, selected_level, school_id FROM users WHERE role='STUDENT'")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
    print(f"  Trade: {row[3]}, Level: {row[4]}, School: {row[5]}")
    print()

print("=" * 60)
print("GROUPS:")
print("=" * 60)
cursor.execute("SELECT id, name, type, department, school_id FROM groups")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}")
    print(f"  Department: {row[3]}, School: {row[4]}")
    print()

conn.close()
