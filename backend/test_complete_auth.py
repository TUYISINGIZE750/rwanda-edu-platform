"""Test complete authentication flow for all roles"""
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

def test_student_registration():
    print("\n" + "="*60)
    print("TEST 1: Student Registration")
    print("="*60)
    
    payload = {
        "full_name": "Test Student",
        "email": "student.test@tvet.rw",
        "password": "student123",
        "role": "student",
        "school_id": 2,
        "province": "Kigali city",
        "district": "GASABO",
        "locale": "en",
        "selected_trade": "Computer system and architecture (CSA)",
        "selected_level": "Level 1"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_teacher_registration():
    print("\n" + "="*60)
    print("TEST 2: Teacher Registration")
    print("="*60)
    
    payload = {
        "full_name": "Test Teacher",
        "email": "teacher.test@tvet.rw",
        "password": "teacher123",
        "role": "teacher",
        "school_id": 2,
        "province": "Kigali city",
        "district": "GASABO",
        "locale": "en",
        "grade": 1
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_student_login():
    print("\n" + "="*60)
    print("TEST 3: Student Login")
    print("="*60)
    
    payload = {
        "username": "student.test@tvet.rw",
        "password": "student123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if response.status_code == 200:
        print(f"\n✅ Student logged in successfully")
        print(f"   Role: {data['user']['role']}")
        print(f"   Trade: {data['user'].get('selected_trade', 'N/A')}")
        print(f"   Level: {data['user'].get('selected_level', 'N/A')}")
        return data['access_token']
    return None

def test_teacher_login():
    print("\n" + "="*60)
    print("TEST 4: Teacher Login")
    print("="*60)
    
    payload = {
        "username": "teacher.test@tvet.rw",
        "password": "teacher123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if response.status_code == 200:
        print(f"\n✅ Teacher logged in successfully")
        print(f"   Role: {data['user']['role']}")
        print(f"   Grade: {data['user'].get('grade', 'N/A')}")
        return data['access_token']
    return None

def test_protected_route(token, role):
    print("\n" + "="*60)
    print(f"TEST 5: Protected Route Access ({role})")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if response.status_code == 200:
        print(f"\n✅ {role} can access protected routes")
        return True
    return False

def main():
    print("\n" + "="*60)
    print("RWANDA TVET AUTHENTICATION TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test registrations
    results.append(("Student Registration", test_student_registration()))
    results.append(("Teacher Registration", test_teacher_registration()))
    
    # Test logins
    student_token = test_student_login()
    results.append(("Student Login", student_token is not None))
    
    teacher_token = test_teacher_login()
    results.append(("Teacher Login", teacher_token is not None))
    
    # Test protected routes
    if student_token:
        results.append(("Student Protected Access", test_protected_route(student_token, "Student")))
    
    if teacher_token:
        results.append(("Teacher Protected Access", test_protected_route(teacher_token, "Teacher")))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)

if __name__ == "__main__":
    main()
