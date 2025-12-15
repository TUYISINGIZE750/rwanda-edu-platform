import requests

BASE_URL = "http://localhost:8080"

print("=== Testing Login Credentials ===\n")

# Test teacher
print("Testing teacher: Elam@gmail.com")
response = requests.post(f"{BASE_URL}/api/auth/login", json={
    "email": "Elam@gmail.com",
    "password": "password123"
})
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✓ Login SUCCESS")
    data = response.json()
    print(f"  User: {data.get('user', {}).get('full_name')}")
else:
    print(f"✗ Login FAILED: {response.text}")

print()

# Test students
for i in range(1, 4):
    email = f"teststudent{i}@school.rw"
    print(f"Testing student {i}: {email}")
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": email,
        "password": "password123"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Login SUCCESS")
    else:
        print(f"✗ Login FAILED: {response.text}")
    print()
