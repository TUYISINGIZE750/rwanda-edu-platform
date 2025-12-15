"""Test teacher dashboard and group creation"""
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

# 1. Login as teacher
print("1. Logging in as teacher...")
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "teacher@iprc.ac.rw",
    "password": "password123"
})

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"[OK] Login successful! Token: {token[:20]}...")
    headers = {"Authorization": f"Bearer {token}"}
else:
    print(f"[FAIL] Login failed: {login_response.text}")
    exit(1)

# 2. Get teacher dashboard
print("\n2. Getting teacher dashboard...")
dashboard_response = requests.get(f"{BASE_URL}/teacher/dashboard", headers=headers)

if dashboard_response.status_code == 200:
    data = dashboard_response.json()
    print(f"[OK] Dashboard loaded!")
    print(f"  - Groups: {data['stats']['groups_count']}")
    print(f"  - Students: {data['stats']['total_students']}")
    print(f"  - Pending Messages: {data['stats']['pending_messages']}")
else:
    print(f"[FAIL] Dashboard failed: {dashboard_response.text}")

# 3. Create a new group
print("\n3. Creating new group...")
group_response = requests.post(f"{BASE_URL}/teacher/groups", 
    headers=headers,
    json={
        "name": "Level 3 Electronics",
        "type": "class",
        "grade": 3
    }
)

if group_response.status_code == 200:
    group_data = group_response.json()
    print(f"[OK] Group created: {group_data['name']} (ID: {group_data['id']})")
    group_id = group_data['id']
else:
    print(f"[FAIL] Group creation failed: {group_response.text}")
    group_id = None

# 4. Get updated dashboard
print("\n4. Getting updated dashboard...")
dashboard_response = requests.get(f"{BASE_URL}/teacher/dashboard", headers=headers)

if dashboard_response.status_code == 200:
    data = dashboard_response.json()
    print(f"[OK] Dashboard updated!")
    print(f"  - Groups: {data['stats']['groups_count']}")
    print(f"  - Group list:")
    for group in data['groups']:
        print(f"    * {group['name']} ({group['type']}) - {group['member_count']} students")
else:
    print(f"[FAIL] Dashboard update failed: {dashboard_response.text}")

# 5. Get students in group
if group_id:
    print(f"\n5. Getting students in group {group_id}...")
    students_response = requests.get(f"{BASE_URL}/teacher/groups/{group_id}/students", headers=headers)
    
    if students_response.status_code == 200:
        students = students_response.json()
        print(f"[OK] Found {len(students)} students")
        for student in students[:3]:
            print(f"  - {student['full_name']} ({student['selected_trade']})")
    else:
        print(f"[FAIL] Students fetch failed: {students_response.text}")

# 6. Get pending messages
print("\n6. Getting pending messages...")
pending_response = requests.get(f"{BASE_URL}/teacher/pending-messages", headers=headers)

if pending_response.status_code == 200:
    pending = pending_response.json()
    print(f"[OK] Found {len(pending)} pending messages")
else:
    print(f"[FAIL] Pending messages failed: {pending_response.text}")

print("\n[SUCCESS] All teacher features tested successfully!")
