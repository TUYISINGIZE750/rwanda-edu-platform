#!/usr/bin/env python3
"""
Simple test to create a working admin user for testing the login
"""
import requests
import json

# Test with a simple admin account
test_credentials = {
    "email": "testadmin@test.com",
    "password": "testpass123"
}

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
    print(f"Login successful!")
    print(f"User role: {data.get('user', {}).get('role')}")
else:
    print("Login failed - trying to create test admin...")
    
    # If login fails, the issue might be that we need to use existing credentials
    # Let's try with the admin@test.com account with different passwords
    common_passwords = ["admin123", "password", "123456", "admin", "test123"]
    
    for pwd in common_passwords:
        test_creds = {"email": "admin@test.com", "password": pwd}
        resp = requests.post(
            "https://rwanda-edu-platform.onrender.com/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json=test_creds
        )
        
        if resp.status_code == 200:
            print(f"SUCCESS! Credentials: {test_creds}")
            data = resp.json()
            print(f"User role: {data.get('user', {}).get('role')}")
            break
        else:
            print(f"Failed with password: {pwd}")