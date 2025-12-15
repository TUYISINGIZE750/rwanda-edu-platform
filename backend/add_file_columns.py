"""Add file columns to messages table"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Add file columns
columns = [
    "ALTER TABLE messages ADD COLUMN file_url TEXT",
    "ALTER TABLE messages ADD COLUMN file_name TEXT",
    "ALTER TABLE messages ADD COLUMN file_type TEXT",
    "ALTER TABLE messages ADD COLUMN file_size INTEGER"
]

for sql in columns:
    try:
        cursor.execute(sql)
        print(f"[OK] {sql}")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print(f"  Column already exists: {sql}")
        else:
            print(f"[ERROR] {e}")

conn.commit()
conn.close()

print("\nDone! File upload columns added to messages table.")
