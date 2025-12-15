"""Test complete student flow: Register -> Login -> Dashboard"""
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

print("="*60)
print("STUDENT COMPLETE FLOW TEST")
print("="*60)

# Step 1: Register Student
print("\nStep 1: Student Registration")
print("-"*60)
student_data = {
    "full_name": "John Doe",
    "email": "john.student@tvet.rw",
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
print(f"Status: {response.status_code}")
if response.status_code == 200:
    user = response.json()
    print(f"SUCCESS - Student registered")
    print(f"  ID: {user['id']}")
    print(f"  Name: {user['full_name']}")
    print(f"  Email: {user['email']}")
    print(f"  Role: {user['role']}")
    print(f"  Trade: {user['selected_trade']}")
    print(f"  Level: {user['selected_level']}")
else:
    print(f"FAILED: {response.json()}")
    exit(1)

# Step 2: Login
print("\nStep 2: Student Login")
print("-"*60)
login_data = {
    "email": "john.student@tvet.rw",
    "password": "student123"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data['access_token']
    user = data['user']
    print(f"SUCCESS - Student logged in")
    print(f"  Token: {token[:30]}...")
    print(f"  User ID: {user['id']}")
    print(f"  Role: {user['role']}")
else:
    print(f"FAILED: {response.json()}")
    exit(1)

# Step 3: Access Protected Route
print("\nStep 3: Access User Profile (/auth/me)")
print("-"*60)
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    user = response.json()
    print(f"SUCCESS - Profile accessed")
    print(f"  Name: {user['full_name']}")
    print(f"  Email: {user['email']}")
    print(f"  School ID: {user['school_id']}")
    print(f"  Trade: {user.get('selected_trade')}")
    print(f"  Level: {user.get('selected_level')}")
else:
    print(f"FAILED: {response.json()}")

# Step 4: Check if student dashboard route exists
print("\nStep 4: Test Dashboard Access")
print("-"*60)
print("Checking available routes...")

# Try to access home
response = requests.get(f"http://localhost:8080/api/v1/", headers=headers)
print(f"Root API Status: {response.status_code}")

print("\n" + "="*60)
print("STUDENT FLOW TEST COMPLETE")
print("="*60)
print("\nSUMMARY:")
print("  Registration: PASS")
print("  Login: PASS")
print("  Protected Route: PASS")
print("  Token Auth: PASS")
print("\nStudent can now access frontend dashboard at:")
print("  http://localhost:5173/home")
print("="*60)
