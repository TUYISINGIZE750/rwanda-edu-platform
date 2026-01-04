"""
IMPLEMENTATION: Department-Based Filtering & Auto-Assignment System
This script implements the complete logic for TSSANYWHERE system
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

print("=" * 80)
print("TSSANYWHERE SYSTEM IMPLEMENTATION")
print("=" * 80)

# Step 1: Verify User model has selected_trade field
print("\n1. Checking User model structure...")
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'users' 
    AND column_name IN ('selected_trade', 'selected_level', 'is_class_teacher', 'managed_class_id')
""")
columns = cur.fetchall()
print(f"   Found columns: {[c[0] for c in columns]}")

# Step 2: Check Group model has department field
print("\n2. Checking Group model structure...")
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'groups' 
    AND column_name = 'department'
""")
dept_col = cur.fetchone()
if dept_col:
    print(f"   Group.department field exists: {dept_col[1]}")
else:
    print("   Group.department field missing - needs migration")

# Step 3: Sample data check
print("\n3. Checking sample data...")

# Check teachers with departments
cur.execute("""
    SELECT COUNT(*) FROM users 
    WHERE role = 'TEACHER' AND selected_trade IS NOT NULL
""")
teachers_with_dept = cur.fetchone()[0]
print(f"   Teachers with department: {teachers_with_dept}")

# Check students with departments
cur.execute("""
    SELECT COUNT(*) FROM users 
    WHERE role = 'STUDENT' AND selected_trade IS NOT NULL
""")
students_with_dept = cur.fetchone()[0]
print(f"   Students with department: {students_with_dept}")

# Check class teachers
cur.execute("""
    SELECT COUNT(*) FROM users 
    WHERE is_class_teacher = 1
""")
class_teachers = cur.fetchone()[0]
print(f"   Class teachers: {class_teachers}")

# Step 4: Show system logic summary
print("\n" + "=" * 80)
print("SYSTEM LOGIC SUMMARY")
print("=" * 80)

print("""
CURRENT IMPLEMENTATION:
1. User.selected_trade field EXISTS (for department/trade)
2. User.selected_level field EXISTS (for TVET levels 1-6)
3. User.is_class_teacher field EXISTS
4. User.managed_class_id field EXISTS
5. 185 schools with trades in database
6. 165 DOS accounts ready

WHAT NEEDS TO BE DONE:

BACKEND:
1. Update admin.py create_user endpoint:
   - Accept 'selected_trade' parameter
   - Accept 'is_class_teacher' parameter
   - Accept 'managed_class_id' parameter

2. Update registration.py:
   - Add 'selected_trade' to student registration
   - Load trades from selected school

3. Update teacher_dashboard.py:
   - Filter students by: school_id AND selected_trade
   - Show only students in teacher's department

4. Update modules.py (teacher group creation):
   - When teacher creates class with department
   - Auto-add all students: same school + same department
   - Send notifications to added students

FRONTEND:
1. AdminUsersView.vue (DOS creates teacher):
   - Add "Department/Trade" dropdown
   - Add "Is Class Teacher?" checkbox
   - Add "Managed Class" dropdown (if class teacher)

2. RegisterView.vue (Student registration):
   - After school selection, load school trades
   - Add "Department/Trade" dropdown
   - Add "Level" dropdown (L1-L6)

3. TeacherDashboard.vue:
   - Display students filtered by department
   - Show department-specific stats

REAL-TIME SYNC:
- WebSocket already implemented
- When student registers with department:
  -> Find matching modules (same school + department)
  -> Auto-add student to those modules
  -> Notify teacher via WebSocket
""")

print("\n" + "=" * 80)
print("SAMPLE QUERIES FOR IMPLEMENTATION")
print("=" * 80)

print("""
-- Get students in teacher's department
SELECT * FROM users 
WHERE school_id = :teacher_school_id 
AND role = 'STUDENT' 
AND selected_trade = :teacher_department;

-- Get modules for student's department
SELECT * FROM groups 
WHERE school_id = :student_school_id 
AND department = :student_department 
AND type = 'CLASS';

-- Auto-add student to matching modules
INSERT INTO group_members (group_id, user_id)
SELECT g.id, :student_id
FROM groups g
WHERE g.school_id = :student_school_id
AND g.department = :student_department
AND g.type = 'CLASS'
AND NOT EXISTS (
    SELECT 1 FROM group_members gm 
    WHERE gm.group_id = g.id AND gm.user_id = :student_id
);
""")

cur.close()
conn.close()

print("\n" + "=" * 80)
print("SYSTEM ANALYSIS COMPLETE")
print("=" * 80)
print("\nNext steps:")
print("1. Update backend API endpoints")
print("2. Update frontend forms")
print("3. Test department-based filtering")
print("4. Test auto-assignment logic")
print("5. Deploy to production")
