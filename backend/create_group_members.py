"""Create group_members table and add KAMANYOLA to group 22"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Create group_members table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS group_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES groups(id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        UNIQUE(group_id, user_id)
    )
""")

print("Created group_members table")

# Add KAMANYOLA Isdore (ID: 97) to group 22 (L3 Land surveying)
cursor.execute("""
    INSERT OR IGNORE INTO group_members (group_id, user_id)
    VALUES (22, 97)
""")

# Also add to the new group 23 we created
cursor.execute("""
    INSERT OR IGNORE INTO group_members (group_id, user_id)
    VALUES (23, 97)
""")

# Add KANSI Malu (ID: 96) as well
cursor.execute("""
    INSERT OR IGNORE INTO group_members (group_id, user_id)
    VALUES (22, 96), (23, 96)
""")

# Add kubana james (ID: 95)
cursor.execute("""
    INSERT OR IGNORE INTO group_members (group_id, user_id)
    VALUES (22, 95), (23, 95)
""")

conn.commit()
print("Added Land surveying students to groups")

# Verify
cursor.execute("""
    SELECT gm.id, g.name, u.full_name 
    FROM group_members gm
    JOIN groups g ON gm.group_id = g.id
    JOIN users u ON gm.user_id = u.id
    WHERE gm.group_id IN (22, 23)
""")

print("\nGroup memberships:")
for row in cursor.fetchall():
    print(f"  {row[1]}: {row[2]}")

conn.close()
