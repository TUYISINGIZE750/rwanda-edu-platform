"""Create test group for KANSI Malu"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Create L3 LSV group for school 63
cursor.execute("""
    INSERT INTO groups (name, type, department, school_id, created_at)
    VALUES ('L3 LSV', 'CLASS', 'Land Surveying', 63, datetime('now'))
""")

group_id = cursor.lastrowid
print(f"Created group ID: {group_id}")

# Create a general channel for this group
cursor.execute("""
    INSERT INTO channels (name, type, group_id, created_at)
    VALUES ('General', 'TEXT', ?, datetime('now'))
""", (group_id,))

print(f"Created channel ID: {cursor.lastrowid}")

conn.commit()
conn.close()

print("\nGroup created successfully!")
print("Group: L3 LSV")
print("School: 63")
print("Department: Land Surveying")
