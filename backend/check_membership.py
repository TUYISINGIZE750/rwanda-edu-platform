"""Check group membership structure"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Check if group_members table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='group_members'")
result = cursor.fetchone()

if result:
    print("group_members table EXISTS")
    print("\nTable structure:")
    cursor.execute("PRAGMA table_info(group_members)")
    for row in cursor.fetchall():
        print(f"  {row[1]} ({row[2]})")
    
    print("\nSample data:")
    cursor.execute("SELECT * FROM group_members LIMIT 10")
    for row in cursor.fetchall():
        print(f"  {row}")
else:
    print("group_members table DOES NOT EXIST")
    print("\nNeed to create membership system!")

conn.close()
