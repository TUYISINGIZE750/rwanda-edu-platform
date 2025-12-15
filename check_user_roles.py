import sqlite3

conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# Check all users and their roles
cursor.execute("SELECT email, role, full_name FROM users")
users = cursor.fetchall()

print("Current users in database:")
print("Email\t\t\tRole\t\tName")
print("-" * 50)
for user in users:
    print(f"{user[0]:<20}\t{user[1]:<10}\t{user[2]}")

conn.close()