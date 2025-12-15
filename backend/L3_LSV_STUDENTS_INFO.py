"""Get all L3 Land Surveying students with credentials and groups"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=" * 80)
print("L3 LAND SURVEYING STUDENTS - LOGIN CREDENTIALS & GROUPS")
print("=" * 80)

# Get all Land surveying Level 3 students
cursor.execute("""
    SELECT id, full_name, email, selected_trade, selected_level, school_id, hashed_password
    FROM users 
    WHERE role = 'STUDENT' 
    AND (selected_trade LIKE '%Land%' OR selected_trade LIKE '%LSV%')
    AND (selected_level LIKE '%3%' OR selected_level LIKE '%Level 3%')
    ORDER BY school_id, full_name
""")

students = cursor.fetchall()

print(f"\nFound {len(students)} students:\n")

for student in students:
    student_id, name, email, trade, level, school_id, hashed_pw = student
    
    print(f"{'='*80}")
    print(f"STUDENT: {name}")
    print(f"{'='*80}")
    print(f"  ID:       {student_id}")
    print(f"  Email:    {email}")
    print(f"  Trade:    {trade}")
    print(f"  Level:    {level}")
    print(f"  School:   {school_id}")
    print(f"  Password: password123  (default for all test accounts)")
    
    # Get enrolled groups
    cursor.execute("""
        SELECT g.id, g.name, g.type, g.department, g.school_id
        FROM groups g
        JOIN group_members gm ON g.id = gm.group_id
        WHERE gm.user_id = ?
        ORDER BY g.name
    """, (student_id,))
    
    groups = cursor.fetchall()
    
    if groups:
        print(f"\n  ENROLLED IN {len(groups)} GROUP(S):")
        for g in groups:
            g_id, g_name, g_type, g_dept, g_school = g
            print(f"    - {g_name} (ID: {g_id}, Type: {g_type}, School: {g_school})")
            if g_dept:
                print(f"      Department: {g_dept}")
    else:
        print(f"\n  NOT ENROLLED IN ANY GROUPS YET")
        print(f"  (Will auto-enroll on first dashboard access)")
    
    # Show matching groups in their school
    cursor.execute("""
        SELECT id, name, type, department
        FROM groups
        WHERE school_id = ?
        ORDER BY name
    """, (school_id,))
    
    available_groups = cursor.fetchall()
    
    if available_groups:
        print(f"\n  AVAILABLE GROUPS IN SCHOOL {school_id}:")
        for ag in available_groups:
            ag_id, ag_name, ag_type, ag_dept = ag
            # Check if matches
            name_lower = (ag_name or '').lower()
            dept_lower = (ag_dept or '').lower()
            
            matches = False
            if 'l3' in name_lower or 'level3' in name_lower or 'level 3' in name_lower:
                if 'land' in name_lower or 'surveying' in name_lower or 'lsv' in name_lower:
                    matches = True
                elif 'land' in dept_lower or 'surveying' in dept_lower or 'lsv' in dept_lower:
                    matches = True
            
            match_text = " [WILL AUTO-ENROLL]" if matches else ""
            print(f"    - {ag_name} (ID: {ag_id}, Type: {ag_type}){match_text}")
            if ag_dept:
                print(f"      Department: {ag_dept}")
    
    print()

print("\n" + "=" * 80)
print("QUICK LOGIN GUIDE")
print("=" * 80)
print("\n1. Go to: http://localhost:5173/login")
print("2. Use any email above with password: password123")
print("3. After login, go to dashboard - auto-enrollment will happen")
print("4. Student will see all matching groups")
print("5. Teacher can view group members to see enrolled students")
print("\n" + "=" * 80)

conn.close()
