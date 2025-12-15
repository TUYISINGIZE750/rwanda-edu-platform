"""Test the actual API endpoint"""
import requests

# Login as KAMANYOLA Isdore
login_response = requests.post('http://localhost:8080/api/v1/auth/login', json={
    'email': 'isdore@gmail.com',
    'password': 'password123'
})

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f"Logged in successfully")
    
    # Get dashboard
    headers = {'Authorization': f'Bearer {token}'}
    dashboard_response = requests.get('http://localhost:8080/api/v1/student/dashboard', headers=headers)
    
    if dashboard_response.status_code == 200:
        data = dashboard_response.json()
        print(f"\nGroups count: {data['stats']['groups_count']}")
        print(f"Groups: {len(data['groups'])}")
        for g in data['groups']:
            print(f"  - {g['name']}")
    else:
        print(f"Dashboard error: {dashboard_response.status_code}")
        print(dashboard_response.text)
else:
    print(f"Login failed: {login_response.status_code}")
    print(login_response.text)
