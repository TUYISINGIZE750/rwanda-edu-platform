import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=== Channels in Group 26 ===\n")

cursor.execute("""
    SELECT id, name, type, group_id 
    FROM channels 
    WHERE group_id = 26
    ORDER BY id
""")

for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}, Group: {row[3]}")

print("\n=== All Messages ===\n")

cursor.execute("""
    SELECT m.id, m.channel_id, c.name as channel_name, m.content, m.status
    FROM messages m
    JOIN channels c ON m.channel_id = c.id
    ORDER BY m.id DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(f"Msg ID: {row[0]}, Channel: {row[1]} ({row[2]}), Content: {row[3][:30]}..., Status: {row[4]}")

conn.close()
