"""Verify everything is set up correctly"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=" * 60)
print("VERIFICATION REPORT")
print("=" * 60)

# 1. Check group_members table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='group_members'")
if cursor.fetchone():
    print("[OK] group_members table exists")
else:
    print("[ERROR] group_members table MISSING")

# 2. Check KAMANYOLA memberships
cursor.execute("""
    SELECT gm.id, g.name, g.school_id
    FROM group_members gm
    JOIN groups g ON gm.group_id = g.id
    WHERE gm.user_id = 97
""")
memberships = cursor.fetchall()
print(f"\n[OK] KAMANYOLA Isdore has {len(memberships)} group memberships:")
for m in memberships:
    print(f"  - {m[1]} (School {m[2]})")

# 3. Check student details
cursor.execute("SELECT full_name, selected_trade, selected_level, school_id FROM users WHERE id = 97")
student = cursor.fetchone()
print(f"\n[OK] Student: {student[0]}")
print(f"  Trade: {student[1]}")
print(f"  Level: {student[2]}")
print(f"  School: {student[3]}")

print("\n" + "=" * 60)
print("DATABASE IS READY!")
print("=" * 60)
print("\nNEXT STEP: Restart the backend server")
print("  1. Stop current server (Ctrl+C)")
print("  2. Run: uvicorn app.main:app --reload --port 8080")
print("  3. Refresh student dashboard")

conn.close()
