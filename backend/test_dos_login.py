import requests

url = "https://rwanda-edu-platform.onrender.com/api/v1/auth/login"
data = {
    "email": "kayenzi_tvet_school@tssanywhere.rw",
    "password": "dos12024"
}

print("Testing DOS login...")
r = requests.post(url, json=data)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:500]}")
