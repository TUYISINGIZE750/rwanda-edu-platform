import requests

url = "https://rwanda-edu-platform.onrender.com/api/v1/auth/login"
data = {"email": "dos@tssanywhere.rw", "password": "dos123"}

r = requests.post(url, json=data)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print("SUCCESS! Login works!")
    print(f"Token: {r.json()['access_token'][:50]}...")
else:
    print(f"Error: {r.text}")
