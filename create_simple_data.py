import sqlite3
from datetime import datetime

conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# Create simple groups
try:
    cursor.execute("INSERT OR REPLACE INTO groups (id, name, type, school_id, created_at) VALUES (1, 'Electronics Level 2', 'class', 1, ?)", (datetime.now(),))
    cursor.execute("INSERT OR REPLACE INTO groups (id, name, type, school_id, created_at) VALUES (2, 'Welding Basics', 'class', 1, ?)", (datetime.now(),))
    cursor.execute("INSERT OR REPLACE INTO groups (id, name, type, school_id, created_at) VALUES (3, 'Automotive Repair', 'class', 1, ?)", (datetime.now(),))
    print("Groups created successfully")
except Exception as e:
    print(f"Error creating groups: {e}")

# Create simple channels
try:
    cursor.execute("INSERT OR REPLACE INTO channels (id, name, type, group_id, created_at) VALUES (1, 'general', 'text', 1, ?)", (datetime.now(),))
    cursor.execute("INSERT OR REPLACE INTO channels (id, name, type, group_id, created_at) VALUES (2, 'assignments', 'text', 1, ?)", (datetime.now(),))
    cursor.execute("INSERT OR REPLACE INTO channels (id, name, type, group_id, created_at) VALUES (3, 'practice', 'text', 2, ?)", (datetime.now(),))
    cursor.execute("INSERT OR REPLACE INTO channels (id, name, type, group_id, created_at) VALUES (4, 'repairs', 'text', 3, ?)", (datetime.now(),))
    print("Channels created successfully")
except Exception as e:
    print(f"Error creating channels: {e}")

conn.commit()
conn.close()
print("Sample data created!")