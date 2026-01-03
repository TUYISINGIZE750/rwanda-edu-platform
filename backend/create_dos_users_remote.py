import json
import requests
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load credentials
with open('dos_credentials_from_excel.json', 'r', encoding='utf-8') as f:
    credentials = json.load(f)

# Remote API base URL
BASE_URL = "https://rwanda-edu-platform.onrender.com/api/v1"

print(f"Creating {len(credentials)} DOS users on remote server...")

# Create DOS users via API or direct database
for idx, cred in enumerate(credentials, 1):
    user_data = {
        "email": cred['username'],
        "password": cred['password'],
        "full_name": f"DOS - {cred['school_name']}",
        "role": "dos",
        "school_name": cred['school_name'],
        "province": cred['province'],
        "district": cred['district'],
        "school_code": cred['school_code']
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/create-dos", json=user_data, timeout=10)
        if response.status_code in [200, 201]:
            print(f"✓ {idx}/{len(credentials)}: {cred['username']}")
        else:
            print(f"✗ {idx}/{len(credentials)}: {cred['username']} - {response.status_code}")
    except Exception as e:
        print(f"✗ {idx}/{len(credentials)}: {cred['username']} - {str(e)[:50]}")

print("\nDone!")
