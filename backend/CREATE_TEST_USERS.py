"""Create 3 test users: Admin, Teacher, Student"""
import sqlite3
import sys
sys.path.insert(0, '.')
from app.core.security import get_password_hash

def hash_password(password: str) -> str:
    return get_password_hash(password)

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Delete existing test users
cursor.execute("DELETE FROM users WHERE email IN ('admin@test.com', 'teacher@test.com', 'student@test.com')")

# Get a school ID (KAYENZI TVET SCHOOL in KAMONYI)
cursor.execute("SELECT id FROM schools WHERE name = 'KAYENZI TVET SCHOOL' LIMIT 1")
school = cursor.fetchone()
school_id = school[0] if school else 59

print("=" * 60)
print("CREATING TEST USERS")
print("=" * 60)

# 1. ADMIN USER
admin_password = hash_password("admin123")
cursor.execute("""
    INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, locale, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ("admin@test.com", admin_password, "Test Admin (DOS)", "admin", school_id, "South", "KAMONYI", "en", 1))
print("✅ Admin created: admin@test.com / admin123")

# 2. TEACHER USER
teacher_password = hash_password("teacher123")
cursor.execute("""
    INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, locale, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ("teacher@test.com", teacher_password, "Test Teacher", "teacher", school_id, "South", "KAMONYI", "en", 1))
print("✅ Teacher created: teacher@test.com / teacher123")

# 3. STUDENT USER
student_password = hash_password("student123")
cursor.execute("""
    INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, grade, selected_trade, selected_level, locale, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ("student@test.com", student_password, "Test Student", "student", school_id, "South", "KAMONYI", 1, "Building construction", "Level 1", "en", 1))
print("✅ Student created: student@test.com / student123")

conn.commit()
conn.close()

print("\n" + "=" * 60)
print("TEST USERS CREATED SUCCESSFULLY!")
print("=" * 60)
print("\nCREDENTIALS:")
print("-" * 60)
print("ADMIN (DOS):")
print("  URL: http://localhost:5173/admin-login")
print("  Email: admin@test.com")
print("  Password: admin123")
print("  School: KAYENZI TVET SCHOOL (KAMONYI)")
print()
print("TEACHER:")
print("  URL: http://localhost:5173/login")
print("  Email: teacher@test.com")
print("  Password: teacher123")
print("  School: KAYENZI TVET SCHOOL (KAMONYI)")
print()
print("STUDENT:")
print("  URL: http://localhost:5173/login")
print("  Email: student@test.com")
print("  Password: student123")
print("  School: KAYENZI TVET SCHOOL (KAMONYI)")
print("  Trade: Building construction")
print("  Level: Level 1")
print("=" * 60)
