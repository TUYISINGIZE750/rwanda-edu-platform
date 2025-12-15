"""Simple authentication test"""
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

print("="*60)
print("AUTHENTICATION TEST")
print("="*60)

# Test 1: Teacher Registration
print("\n1. Teacher Registration...")
teacher_data = {
    "full_name": "Test Teacher",
    "email": "teacher.new@tvet.rw",
    "password": "teacher123",
    "role": "teacher",
    "school_id": 2,
    "province": "Kigali city",
    "district": "GASABO",
    "locale": "en",
    "grade": 1
}

response = requests.post(f"{BASE_URL}/auth/register", json=teacher_data)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print("   PASS - Teacher registered")
else:
    print(f"   FAIL - {response.json()}")

# Test 2: Student Registration
print("\n2. Student Registration...")
student_data = {
    "full_name": "Test Student",
    "email": "student.new@tvet.rw",
    "password": "student123",
    "role": "student",
    "school_id": 2,
    "province": "Kigali city",
    "district": "GASABO",
    "locale": "en",
    "selected_trade": "Computer system and architecture",
    "selected_level": "Level 1"
}

response = requests.post(f"{BASE_URL}/auth/register", json=student_data)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print("   PASS - Student registered")
else:
    print(f"   FAIL - {response.json()}")

# Test 3: Teacher Login
print("\n3. Teacher Login...")
login_data = {
    "email": "teacher.new@tvet.rw",
    "password": "teacher123"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print("   PASS - Teacher logged in")
    print(f"   Role: {data['user']['role']}")
    teacher_token = data['access_token']
else:
    print(f"   FAIL - {response.json()}")
    teacher_token = None

# Test 4: Student Login
print("\n4. Student Login...")
login_data = {
    "email": "student.new@tvet.rw",
    "password": "student123"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print("   PASS - Student logged in")
    print(f"   Role: {data['user']['role']}")
    print(f"   Trade: {data['user'].get('selected_trade')}")
    print(f"   Level: {data['user'].get('selected_level')}")
    student_token = data['access_token']
else:
    print(f"   FAIL - {response.json()}")
    student_token = None

# Test 5: Protected Route
if teacher_token:
    print("\n5. Teacher Protected Route...")
    headers = {"Authorization": f"Bearer {teacher_token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   PASS - Teacher can access protected routes")
    else:
        print("   FAIL")

if student_token:
    print("\n6. Student Protected Route...")
    headers = {"Authorization": f"Bearer {student_token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   PASS - Student can access protected routes")
    else:
        print("   FAIL")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
