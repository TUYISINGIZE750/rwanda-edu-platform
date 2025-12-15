"""Test authentication endpoints for students and teachers"""
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

def test_student_registration_and_login():
    """Test student registration with TVET flow"""
    print("\n" + "="*80)
    print("TESTING STUDENT REGISTRATION & LOGIN")
    print("="*80)
    
    # Step 1: Get schools
    print("\n[1] Getting schools for Kigali city, GASABO...")
    try:
        response = requests.get(f"{BASE_URL}/registration/schools/Kigali city/GASABO")
        if response.status_code == 200:
            schools = response.json()["schools"]
            print(f"✓ Found {len(schools)} schools")
            if schools:
                school = schools[0]
                print(f"  Sample: {school['name']}")
            else:
                print("❌ No schools found!")
                return False
        else:
            print(f"❌ Failed to get schools: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 2: Get trades
    print(f"\n[2] Getting trades for school ID {school['id']}...")
    try:
        response = requests.get(f"{BASE_URL}/registration/trades/{school['id']}")
        if response.status_code == 200:
            data = response.json()
            trades = data["trades"]
            print(f"✓ Found {len(trades)} trades")
            if trades:
                # Extract trade name from object or use string directly
                if isinstance(trades[0], dict):
                    trade = trades[0].get("name", trades[0].get("display_name", "General Studies"))
                else:
                    trade = trades[0]
                print(f"  Sample: {trade}")
            else:
                print("⚠ No trades found, using default")
                trade = "General Studies"
        else:
            print(f"❌ Failed to get trades: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 3: Get levels
    print("\n[3] Getting TVET levels...")
    try:
        response = requests.get(f"{BASE_URL}/registration/levels")
        if response.status_code == 200:
            data = response.json()
            levels = data.get("levels", [])
            print(f"✓ Found {len(levels)} levels")
            # Extract just the name/value
            if levels and isinstance(levels[0], dict):
                level = levels[2].get("value", "Level 3")
            else:
                level = levels[2] if len(levels) > 2 else "Level 3"
            print(f"  Selected: {level}")
        else:
            print(f"❌ Failed to get levels: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 4: Register student
    print("\n[4] Registering student...")
    student_data = {
        "email": "test.student@tvet.rw",
        "password": "Student123!",
        "full_name": "Jean Claude Mugabo",
        "role": "student",
        "school_id": school["id"],
        "province": "Kigali city",
        "district": "GASABO",
        "selected_trade": trade,
        "selected_level": level,
        "locale": "rw"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=student_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            user = response.json()
            print(f"✓ Student registered successfully!")
            print(f"  ID: {user['id']}")
            print(f"  Email: {user['email']}")
            print(f"  School ID: {user['school_id']}")
        elif response.status_code == 400 and "already registered" in response.text:
            print("⚠ Student already exists (OK for testing)")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 5: Login student
    print("\n[5] Testing student login...")
    login_data = {
        "email": "test.student@tvet.rw",
        "password": "Student123!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Student login successful!")
            print(f"  Token: {data['access_token'][:50]}...")
            print(f"  User: {data['user']['full_name']}")
            print(f"  Role: {data['user']['role']}")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_teacher_registration_and_login():
    """Test teacher registration"""
    print("\n" + "="*80)
    print("TESTING TEACHER REGISTRATION & LOGIN")
    print("="*80)
    
    # Get a school
    print("\n[1] Getting schools for teacher...")
    try:
        response = requests.get(f"{BASE_URL}/registration/schools/Kigali city/GASABO")
        if response.status_code == 200:
            schools = response.json()["schools"]
            if schools:
                school = schools[0]
                print(f"✓ Using school: {school['name']}")
            else:
                print("❌ No schools found!")
                return False
        else:
            print(f"❌ Failed to get schools: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Register teacher (no trade/level required)
    print("\n[2] Registering teacher...")
    teacher_data = {
        "email": "test.teacher@tvet.rw",
        "password": "Teacher123!",
        "full_name": "Marie Uwase",
        "role": "teacher",
        "school_id": school["id"],
        "province": "Kigali city",
        "district": "GASABO",
        "locale": "rw"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=teacher_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            user = response.json()
            print(f"✓ Teacher registered successfully!")
            print(f"  ID: {user['id']}")
            print(f"  Email: {user['email']}")
            print(f"  Role: {user['role']}")
        elif response.status_code == 400 and "already registered" in response.text:
            print("⚠ Teacher already exists (OK for testing)")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Login teacher
    print("\n[3] Testing teacher login...")
    login_data = {
        "email": "test.teacher@tvet.rw",
        "password": "Teacher123!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Teacher login successful!")
            print(f"  Token: {data['access_token'][:50]}...")
            print(f"  User: {data['user']['full_name']}")
            print(f"  Role: {data['user']['role']}")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("AUTHENTICATION ENDPOINTS TEST")
    print("="*80)
    print("\nMake sure the backend server is running on http://localhost:8080")
    print("Press Enter to continue or Ctrl+C to cancel...")
    input()
    
    # Test health endpoint
    print("\n[0] Checking server health...")
    try:
        response = requests.get("http://localhost:8080/health")
        if response.status_code == 200:
            print("✓ Server is running")
        else:
            print("❌ Server health check failed")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("\nPlease start the server first:")
        print("  cd backend")
        print("  python -m uvicorn app.main:app --reload")
        return
    
    # Run tests
    student_ok = test_student_registration_and_login()
    teacher_ok = test_teacher_registration_and_login()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Student Registration & Login: {'✓ PASSED' if student_ok else '❌ FAILED'}")
    print(f"Teacher Registration & Login: {'✓ PASSED' if teacher_ok else '❌ FAILED'}")
    
    if student_ok and teacher_ok:
        print("\n✅ ALL TESTS PASSED!")
        print("\nThe system is working correctly:")
        print("  • Student registration with TVET flow ✓")
        print("  • Teacher registration ✓")
        print("  • Login for both roles ✓")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Please check the error messages above")

if __name__ == "__main__":
    main()
