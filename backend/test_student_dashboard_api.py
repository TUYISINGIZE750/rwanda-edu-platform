"""Test student dashboard API"""
import requests

BASE_URL = "http://localhost:8080/api/v1"

# Login as student
print("="*60)
print("STUDENT DASHBOARD API TEST")
print("="*60)

print("\n1. Login as student...")
login_data = {
    "email": "john.student@tvet.rw",
    "password": "student123"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code == 200:
    data = response.json()
    token = data['access_token']
    print("   SUCCESS - Logged in")
    print(f"   Token: {token[:30]}...")
else:
    print(f"   FAILED: {response.json()}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Test dashboard endpoint
print("\n2. Get Dashboard Data...")
response = requests.get(f"{BASE_URL}/student/dashboard", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print("   SUCCESS - Dashboard loaded")
    print(f"\n   Student Info:")
    print(f"     Name: {data['student_info']['name']}")
    print(f"     Trade: {data['student_info']['trade']}")
    print(f"     Level: {data['student_info']['level']}")
    print(f"\n   Stats:")
    print(f"     Groups: {data['stats']['groups_count']}")
    print(f"     Unread Messages: {data['stats']['unread_messages']}")
    print(f"     Resources: {data['stats']['resources_count']}")
    print(f"     Active Sessions: {data['stats']['active_sessions']}")
    print(f"\n   Groups: {len(data['groups'])} groups")
    for group in data['groups']:
        print(f"     - {group['name']} ({group['member_count']} members, {group['unread_count']} unread)")
    print(f"\n   Resources: {len(data['resources'])} resources")
    for resource in data['resources']:
        print(f"     - {resource['title']} ({resource['type']})")
    print(f"\n   Sessions: {len(data['sessions'])} sessions")
    for session in data['sessions']:
        print(f"     - {session['title']} with {session['instructor']}")
else:
    print(f"   FAILED: {response.json()}")

# Test individual endpoints
print("\n3. Get My Groups...")
response = requests.get(f"{BASE_URL}/student/groups", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    groups = response.json()
    print(f"   SUCCESS - {len(groups)} groups")

print("\n4. Get Unread Messages...")
response = requests.get(f"{BASE_URL}/student/messages/unread", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   SUCCESS - {data['total_unread']} unread messages")

print("\n5. Get Resources...")
response = requests.get(f"{BASE_URL}/student/resources", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   SUCCESS - {data['total']} resources")

print("\n6. Get Active Sessions...")
response = requests.get(f"{BASE_URL}/student/sessions", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   SUCCESS - {data['total']} sessions")

print("\n" + "="*60)
print("ALL TESTS COMPLETE")
print("="*60)
