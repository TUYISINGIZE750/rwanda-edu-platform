import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Get teacher with user_id 389 (from JWT token)
cur.execute("SELECT id, email, full_name, school_id, role FROM users WHERE id = 389")
teacher = cur.fetchone()

if teacher:
    print(f"\n=== TEACHER INFO ===")
    print(f"ID: {teacher[0]}")
    print(f"Email: {teacher[1]}")
    print(f"Name: {teacher[2]}")
    print(f"School ID: {teacher[3]}")
    print(f"Role: {teacher[4]}")
    
    # Check if school exists
    cur.execute("SELECT id, name, trades FROM schools WHERE id = %s", (teacher[3],))
    school = cur.fetchone()
    
    if school:
        print(f"\n=== SCHOOL INFO ===")
        print(f"ID: {school[0]}")
        print(f"Name: {school[1]}")
        print(f"Trades: {school[2]}")
        print(f"Number of trades: {len(school[2]) if school[2] else 0}")
    else:
        print(f"\n❌ School with ID {teacher[3]} NOT FOUND in database!")
        print("\nFinding valid schools...")
        cur.execute("SELECT id, name, school_code FROM schools ORDER BY id LIMIT 5")
        schools = cur.fetchall()
        print("\nFirst 5 schools in database:")
        for s in schools:
            print(f"  ID: {s[0]}, Name: {s[1]}, Code: {s[2]}")
else:
    print("Teacher with ID 389 not found!")

cur.close()
conn.close()
