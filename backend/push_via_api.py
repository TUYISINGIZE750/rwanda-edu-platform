import requests
import base64
import json

# Read the fixed file
with open('app/api/locations.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Encode to base64
encoded_content = base64.b64encode(content.encode()).decode()

# GitHub API details
GITHUB_TOKEN = input("Enter your GitHub Personal Access Token: ")
REPO = "TUYISINGIZE750/rwanda-edu-platform"
FILE_PATH = "backend/app/api/locations.py"
BRANCH = "main"

# Get current file SHA
url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    current_sha = response.json()['sha']
    print(f"Current SHA: {current_sha}")
    
    # Update file
    data = {
        "message": "Fix schools dropdown - API query bug",
        "content": encoded_content,
        "sha": current_sha,
        "branch": BRANCH
    }
    
    update_response = requests.put(url, headers=headers, json=data)
    if update_response.status_code == 200:
        print("SUCCESS! File updated on GitHub")
        print("Render will auto-deploy in ~2 minutes")
    else:
        print(f"Error: {update_response.status_code}")
        print(update_response.text)
else:
    print(f"Error getting file: {response.status_code}")
    print(response.text)
