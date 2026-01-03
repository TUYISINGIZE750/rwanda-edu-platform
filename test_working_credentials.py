#!/usr/bin/env python3
"""
Test the working admin credentials
"""
import requests
import json

# Test with the created admin account
test_credentials = {
    "email": "admin@test.com",
    "password": "admin123"
}

print("Testing admin login...")
print(f"Credentials: {test_credentials}")

# Try to login
response = requests.post(
    "https://rwanda-edu-platform.onrender.com/api/v1/auth/login",
    headers={"Content-Type": "application/json"},
    json=test_credentials
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    data = response.json()
    print(f"SUCCESS! Login successful!")
    print(f"User role: {data.get('user', {}).get('role')}")
    print(f"User name: {data.get('user', {}).get('full_name')}")
    print(f"School ID: {data.get('user', {}).get('school_id')}")
else:
    print("Login failed!")
    
    # Also test other credentials
    other_creds = [
        {"email": "teacher@test.com", "password": "teacher123"},
        {"email": "student@test.com", "password": "student123"}
    ]
    
    for creds in other_creds:
        print(f"\nTesting {creds['email']}...")
        resp = requests.post(
            "https://rwanda-edu-platform.onrender.com/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json=creds
        )
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"SUCCESS! {creds['email']} works!")
            print(f"Role: {data.get('user', {}).get('role')}")
        else:
            print(f"Failed: {creds['email']}")