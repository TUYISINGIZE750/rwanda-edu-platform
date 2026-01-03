#!/usr/bin/env python3
"""
Test the documented working credentials
"""
import requests
import json

# Test credentials from WORKING_CREDENTIALS.md
test_accounts = [
    {
        "email": "Elam@gmail.com",
        "password": "password123",
        "type": "TEACHER"
    },
    {
        "email": "teststudent1@school.rw", 
        "password": "password123",
        "type": "STUDENT"
    },
    {
        "email": "teststudent2@school.rw",
        "password": "password123", 
        "type": "STUDENT"
    },
    {
        "email": "teststudent3@school.rw",
        "password": "password123",
        "type": "STUDENT"
    }
]

print("Testing documented working credentials...")
print("=" * 50)

for account in test_accounts:
    print(f"\nTesting {account['type']}: {account['email']}")
    
    # Try to login
    response = requests.post(
        "https://rwanda-edu-platform.onrender.com/api/v1/auth/login",
        headers={"Content-Type": "application/json"},
        json={"email": account["email"], "password": account["password"]}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS! Login successful!")
        print(f"  User role: {data.get('user', {}).get('role')}")
        print(f"  User name: {data.get('user', {}).get('full_name')}")
        print(f"  School ID: {data.get('user', {}).get('school_id')}")
        print(f"  User ID: {data.get('user', {}).get('id')}")
        
        # Check if this is an admin
        if data.get('user', {}).get('role') == 'admin':
            print(f"  *** ADMIN ACCOUNT FOUND! ***")
            
    else:
        print(f"Failed: {response.text}")

print("\n" + "=" * 50)
print("Testing complete!")