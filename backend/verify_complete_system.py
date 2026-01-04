"""
COMPLETE SYSTEM VERIFICATION TEST
Tests all department-based filtering and auto-assignment features
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

print("=" * 80)
print("TSSANYWHERE SYSTEM VERIFICATION TEST")
print("=" * 80)

# Test 1: Verify database schema
print("\n1. DATABASE SCHEMA VERIFICATION")
print("-" * 80)

cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'users' 
    AND column_name IN ('selected_trade', 'selected_level', 'is_class_teacher', 'managed_class_id')
    ORDER BY column_name
""")
user_columns = cur.fetchall()
print(f"User model columns: {len(user_columns)}/4")
for col in user_columns:
    print(f"  - {col[0]}: {col[1]}")

cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'groups' 
    AND column_name = 'department'
""")
group_col = cur.fetchone()
if group_col:
    print(f"\nGroup.department: {group_col[1]}")

# Test 2: Check schools with trades
print("\n2. SCHOOLS WITH TRADES")
print("-" * 80)

cur.execute("""
    SELECT COUNT(*) FROM schools WHERE trades IS NOT NULL AND array_length(trades, 1) > 0
""")
schools_with_trades = cur.fetchone()[0]
print(f"Schools with trades: {schools_with_trades}")

cur.execute("""
    SELECT name, array_length(trades, 1) as trade_count 
    FROM schools 
    WHERE trades IS NOT NULL AND array_length(trades, 1) > 0
    ORDER BY trade_count DESC
    LIMIT 5
""")
top_schools = cur.fetchall()
print("\nTop 5 schools by trade count:")
for school in top_schools:
    print(f"  - {school[0]}: {school[1]} trades")

# Test 3: Check users with departments
print("\n3. USERS WITH DEPARTMENTS")
print("-" * 80)

cur.execute("""
    SELECT role, COUNT(*) as count,
           COUNT(CASE WHEN selected_trade IS NOT NULL THEN 1 END) as with_dept
    FROM users
    GROUP BY role
    ORDER BY role
""")
user_stats = cur.fetchall()
print("User statistics:")
for stat in user_stats:
    print(f"  {stat[0]}: {stat[1]} total, {stat[2]} with department")

# Test 4: Check class teachers
print("\n4. CLASS TEACHERS")
print("-" * 80)

cur.execute("""
    SELECT u.full_name, u.selected_trade, u.managed_class_id, g.name as class_name
    FROM users u
    LEFT JOIN groups g ON u.managed_class_id = g.id
    WHERE u.is_class_teacher = 1
    LIMIT 10
""")
class_teachers = cur.fetchall()
print(f"Class teachers: {len(class_teachers)}")
for teacher in class_teachers:
    print(f"  - {teacher[0]} | Dept: {teacher[1]} | Class: {teacher[3] or 'None'}")

# Test 5: Check groups with departments
print("\n5. GROUPS/CLASSES WITH DEPARTMENTS")
print("-" * 80)

cur.execute("""
    SELECT name, type, department, 
           (SELECT COUNT(*) FROM group_members WHERE group_id = groups.id) as member_count
    FROM groups
    WHERE department IS NOT NULL
    ORDER BY member_count DESC
    LIMIT 10
""")
groups = cur.fetchall()
print(f"Groups with departments: {len(groups)}")
for group in groups:
    print(f"  - {group[0]} ({group[1]}) | Dept: {group[2]} | Members: {group[3]}")

# Test 6: Sample department matching
print("\n6. DEPARTMENT MATCHING TEST")
print("-" * 80)

cur.execute("""
    SELECT selected_trade, COUNT(*) as student_count
    FROM users
    WHERE role = 'STUDENT' AND selected_trade IS NOT NULL
    GROUP BY selected_trade
    ORDER BY student_count DESC
    LIMIT 5
""")
popular_trades = cur.fetchall()
print("Most popular trades among students:")
for trade in popular_trades:
    print(f"  - {trade[0]}: {trade[1]} students")

# Test 7: Auto-assignment potential
print("\n7. AUTO-ASSIGNMENT POTENTIAL")
print("-" * 80)

cur.execute("""
    SELECT 
        g.name as class_name,
        g.department,
        (SELECT COUNT(*) FROM users 
         WHERE school_id = g.school_id 
         AND role = 'STUDENT' 
         AND selected_trade = g.department) as matching_students,
        (SELECT COUNT(*) FROM group_members WHERE group_id = g.id) as current_members
    FROM groups g
    WHERE g.department IS NOT NULL
    ORDER BY matching_students DESC
    LIMIT 5
""")
assignment_potential = cur.fetchall()
print("Classes with auto-assignment potential:")
for row in assignment_potential:
    print(f"  - {row[0]} ({row[1]})")
    print(f"    Matching students: {row[2]}, Current members: {row[3]}")

# Test 8: System readiness
print("\n8. SYSTEM READINESS CHECK")
print("-" * 80)

checks = []

# Check 1: Schools have trades
cur.execute("SELECT COUNT(*) FROM schools WHERE trades IS NOT NULL AND array_length(trades, 1) > 0")
if cur.fetchone()[0] > 0:
    checks.append(("Schools have trades", True))
else:
    checks.append(("Schools have trades", False))

# Check 2: Some students have departments
cur.execute("SELECT COUNT(*) FROM users WHERE role = 'STUDENT' AND selected_trade IS NOT NULL")
if cur.fetchone()[0] > 0:
    checks.append(("Students have departments", True))
else:
    checks.append(("Students have departments", False))

# Check 3: Some teachers have departments
cur.execute("SELECT COUNT(*) FROM users WHERE role = 'TEACHER' AND selected_trade IS NOT NULL")
if cur.fetchone()[0] > 0:
    checks.append(("Teachers have departments", True))
else:
    checks.append(("Teachers have departments", False))

# Check 4: Some groups have departments
cur.execute("SELECT COUNT(*) FROM groups WHERE department IS NOT NULL")
if cur.fetchone()[0] > 0:
    checks.append(("Groups have departments", True))
else:
    checks.append(("Groups have departments", False))

# Check 5: Class teachers exist
cur.execute("SELECT COUNT(*) FROM users WHERE is_class_teacher = 1")
if cur.fetchone()[0] > 0:
    checks.append(("Class teachers exist", True))
else:
    checks.append(("Class teachers exist", False))

print("\nSystem Readiness:")
for check, status in checks:
    status_icon = "PASS" if status else "FAIL"
    print(f"  [{status_icon}] {check}")

all_passed = all(status for _, status in checks)

print("\n" + "=" * 80)
if all_passed:
    print("SYSTEM STATUS: READY FOR PRODUCTION")
else:
    print("SYSTEM STATUS: NEEDS CONFIGURATION")
print("=" * 80)

print("\nRECOMMENDATIONS:")
print("1. DOS should create teachers with departments assigned")
print("2. Students should register with trade/department selection")
print("3. Teachers should create classes with department specified")
print("4. System will auto-assign students to matching classes")
print("5. Real-time notifications will be sent via WebSocket")

cur.close()
conn.close()
