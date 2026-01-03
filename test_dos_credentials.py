#!/usr/bin/env python3
"""
Test DOS credentials and dashboard access
"""
import requests
import json

# DOS credentials from the system
dos_credentials = {
    "email": "dos@iprc.ac.rw",
    "password": "dos123"
}

print("Testing DOS Admin Credentials...")
print("=" * 50)
print(f"Email: {dos_credentials['email']}")
print(f"Password: {dos_credentials['password']}")
print()

# Test login
print("1. Testing login...")
try:
    response = requests.post(
        "http://localhost:8080/api/v1/auth/login",
        headers={"Content-Type": "application/json"},
        json=dos_credentials,
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("LOGIN SUCCESSFUL!")
        print(f"   User ID: {data.get('user', {}).get('id')}")
        print(f"   Full Name: {data.get('user', {}).get('full_name')}")
        print(f"   Role: {data.get('user', {}).get('role')}")
        print(f"   School ID: {data.get('user', {}).get('school_id')}")
        print(f"   Email: {data.get('user', {}).get('email')}")
        
        # Get the token for further testing
        token = data.get('access_token')
        if token:
            print(f"   Token: {token[:20]}...")
            
            # Test DOS dashboard access
            print("\n2. Testing DOS Dashboard Access...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            dashboard_response = requests.get(
                "http://localhost:8080/api/v1/dos/dashboard",
                headers=headers,
                timeout=10
            )
            
            print(f"Dashboard Status: {dashboard_response.status_code}")
            
            if dashboard_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                print("DOS DASHBOARD ACCESS SUCCESSFUL!")
                print("   Dashboard Stats:")
                stats = dashboard_data.get('stats', {})
                print(f"     - Total Teachers: {stats.get('total_teachers', 0)}")
                print(f"     - Total Students: {stats.get('total_students', 0)}")
                print(f"     - Total Classes: {stats.get('total_classes', 0)}")
                print(f"     - Class Teachers: {stats.get('class_teachers', 0)}")
                
                recent_teachers = dashboard_data.get('recent_teachers', [])
                print(f"     - Recent Teachers: {len(recent_teachers)}")
                
            else:
                print("DOS DASHBOARD ACCESS FAILED!")
                print(f"   Error: {dashboard_response.text}")
        
    else:
        print("LOGIN FAILED!")
        print(f"   Error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("CONNECTION ERROR!")
    print("   Backend server is not running on http://localhost:8080")
    print("   Please start the backend server first:")
    print("   cd backend && uvicorn app.main:app --reload --port 8080")
    
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 50)
print("SUMMARY:")
print("- DOS credentials should work for login")
print("- After login, user should be redirected to DOS Dashboard")
print("- DOS Dashboard should show school statistics and teacher management")
print("- Frontend URL: http://localhost:5173")
print("- Backend URL: http://localhost:8080")