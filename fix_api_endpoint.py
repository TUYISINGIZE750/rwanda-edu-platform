import sqlite3

# Check what role format is actually in the database
conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

cursor.execute("SELECT email, role FROM users WHERE email = 'student@test.com'")
result = cursor.fetchone()

if result:
    print(f"Student user role in database: '{result[1]}'")
    print(f"Role type: {type(result[1])}")
    print(f"Role length: {len(result[1])}")
else:
    print("Student user not found")

conn.close()