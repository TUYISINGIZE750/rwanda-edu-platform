"""Fix DOS password via API endpoint"""
import requests
import json

def fix_remote_dos():
    base_url = "https://rwanda-edu-platform.onrender.com/api/v1"
    
    # Create a temporary admin endpoint call or use seed endpoint
    try:
        # Try to call the seed endpoint which might have admin functions
        response = requests.post(f"{base_url}/seed/fix-dos-password")
        
        if response.status_code == 200:
            print("DOS password fixed successfully")
        else:
            print(f"Failed to fix password: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_remote_dos()