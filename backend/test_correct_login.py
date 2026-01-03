import requests

url = "https://rwanda-edu-platform.onrender.com/api/v1/auth/login"
data = {
    "email": "nyamata_tvet_school_1@tssanywhere.rw",
    "password": "dos12024"
}

print("Testing DOS login with correct email...")
r = requests.post(url, json=data)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print("SUCCESS!")
    print(f"User: {r.json().get('user', {}).get('full_name')}")
else:
    print(f"Error: {r.text}")
