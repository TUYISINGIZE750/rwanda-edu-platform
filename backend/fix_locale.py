import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=== Fixing Locale Values ===\n")

# Fix test students
for i in range(1, 4):
    email = f'teststudent{i}@school.rw'
    cursor.execute("UPDATE users SET locale = 'en' WHERE email = ?", (email,))
    print(f"✓ Fixed locale for {email}")

# Fix teacher
cursor.execute("UPDATE users SET locale = 'en' WHERE email = ?", ('Elam@gmail.com',))
print(f"✓ Fixed locale for Elam@gmail.com")

conn.commit()
conn.close()

print("\n=== All locales set to 'en' ===")
