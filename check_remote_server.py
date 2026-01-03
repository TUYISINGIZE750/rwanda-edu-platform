#!/usr/bin/env python3
"""
Check remote server status and find correct endpoints
"""
import requests

REMOTE_URL = "https://rwanda-edu-backend.onrender.com"

print("Checking Remote Server Status...")
print("=" * 50)
print(f"Remote URL: {REMOTE_URL}")
print()

# Test different endpoints to find the correct one
endpoints_to_test = [
    "/",
    "/health",
    "/docs",
    "/api/v1/auth/login",
    "/auth/login",
    "/login"
]

for endpoint in endpoints_to_test:
    try:
        print(f"Testing {endpoint}...")
        response = requests.get(f"{REMOTE_URL}{endpoint}", timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {response.text[:100]}...")
        print()
    except Exception as e:
        print(f"  Error: {e}")
        print()

# Test DOS login with different paths
dos_credentials = {
    "email": "dos@iprc.ac.rw", 
    "password": "dos123"
}

login_paths = [
    "/api/v1/auth/login",
    "/auth/login", 
    "/login"
]

print("Testing DOS login with different paths...")
for path in login_paths:
    try:
        print(f"Testing POST {path}...")
        response = requests.post(
            f"{REMOTE_URL}{path}",
            headers={"Content-Type": "application/json"},
            json=dos_credentials,
            timeout=15
        )
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  LOGIN SUCCESSFUL!")
            data = response.json()
            print(f"  User: {data.get('user', {}).get('full_name')}")
            print(f"  Role: {data.get('user', {}).get('role')}")
        else:
            print(f"  Response: {response.text[:200]}")
        print()
    except Exception as e:
        print(f"  Error: {e}")
        print()