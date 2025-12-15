import sqlite3

conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# Get table schemas
tables = ['users', 'groups', 'channels', 'messages', 'resources', 'sessions']

for table in tables:
    try:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        print(f"\n{table.upper()} table columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    except Exception as e:
        print(f"Error checking {table}: {e}")

conn.close()