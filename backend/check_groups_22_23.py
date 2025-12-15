"""Check groups 22 and 23 details"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("="*80)
print("GROUP DETAILS")
print("="*80)

for group_id in [22, 23]:
    cursor.execute("SELECT id, name, type, department, school_id FROM groups WHERE id = ?", (group_id,))
    group = cursor.fetchone()
    
    if group:
        g_id, name, g_type, dept, school = group
        print(f"\nGroup {g_id}: {name}")
        print(f"  Type: {g_type}")
        print(f"  Department: {dept}")
        print(f"  School: {school}")
        
        # Count matching students
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE role = 'STUDENT' 
            AND school_id = ?
            AND selected_level LIKE '%3%'
        """, (school,))
        level_match = cursor.fetchone()[0]
        print(f"  Students with Level 3 in school {school}: {level_match}")
        
        # Check channels
        cursor.execute("SELECT id, name, type FROM channels WHERE group_id = ?", (group_id,))
        channels = cursor.fetchall()
        print(f"  Channels: {len(channels)}")
        for ch in channels:
            print(f"    - {ch[1]} ({ch[2]})")

print("\n" + "="*80)
print("L3 LAND SURVEYING STUDENTS IN EACH SCHOOL")
print("="*80)

cursor.execute("""
    SELECT school_id, COUNT(*) 
    FROM users 
    WHERE role = 'STUDENT' 
    AND selected_level LIKE '%3%'
    AND (selected_trade LIKE '%Land%' OR selected_trade LIKE '%surveying%' OR selected_trade LIKE '%LSV%')
    GROUP BY school_id
""")

for row in cursor.fetchall():
    print(f"School {row[0]}: {row[1]} students")

conn.close()
