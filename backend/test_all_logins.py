"""Test all user logins"""
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

test_users = [
    {"email": "admin@test.com", "password": "test123", "expected_role": "admin"},
    {"email": "teacher@test.com", "password": "test123", "expected_role": "teacher"},
    {"email": "student@test.com", "password": "test123", "expected_role": "student"},
]

print("=" * 80)
print("TESTING ALL USER LOGINS")
print("=" * 80)

for user in test_users:
    print(f"\nTesting {user['expected_role'].upper()} login...")
    print(f"Email: {user['email']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": user["email"], "password": user["password"]}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            user_data = data.get("user", {})
            role = user_data.get("role", "").lower()
            
            if role == user["expected_role"]:
                print(f"[SUCCESS] Login successful!")
                print(f"  Role: {role}")
                print(f"  Name: {user_data.get('full_name', 'N/A')}")
                print(f"  Token: {token[:20]}...")
            else:
                print(f"[ERROR] Role mismatch! Expected {user['expected_role']}, got {role}")
        else:
            print(f"[ERROR] Login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Exception: {e}")

print("\n" + "=" * 80)
print("LOGIN TEST COMPLETE")
print("=" * 80)
print("\nYou can now:")
print("1. Admin: http://localhost:5173/admin-login")
print("2. Teacher/Student: http://localhost:5173/login")
