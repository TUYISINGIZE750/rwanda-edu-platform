"""Fix invalid channel types in database"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Check current channel types
cursor.execute("SELECT DISTINCT type FROM channels")
types = cursor.fetchall()
print("Current channel types:", types)

# Update TEXT to DISCUSSION
cursor.execute("UPDATE channels SET type = 'DISCUSSION' WHERE type = 'TEXT'")
print(f"Updated {cursor.rowcount} channels from TEXT to DISCUSSION")

conn.commit()

# Verify
cursor.execute("SELECT DISTINCT type FROM channels")
types = cursor.fetchall()
print("New channel types:", types)

conn.close()
print("\nDone! Restart backend now.")
