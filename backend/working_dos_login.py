#!/usr/bin/env python3
import json
import hashlib

def verify_dos_login(username, password):
    """Verify DOS login credentials"""
    try:
        with open('dos_login_credentials.json', 'r') as f:
            credentials = json.load(f)
        
        for cred in credentials:
            if cred['username'] == username and cred['password'] == password:
                return True, cred['school']
        return False, None
    except:
        return False, None

def main():
    print("=== DOS LOGIN SYSTEM ===")
    print("Total schools loaded: 492")
    print("\nSample login credentials:")
    print("Username: nyarugenge_1, Password: dos12024")
    print("Username: gasabo_4, Password: dos42024")
    print("Username: kicukiro_7, Password: dos72024")
    
    while True:
        print("\n" + "="*40)
        username = input("Enter DOS Username: ").strip()
        if username.lower() == 'quit':
            break
            
        password = input("Enter DOS Password: ").strip()
        
        success, school = verify_dos_login(username, password)
        
        if success:
            print(f"✅ LOGIN SUCCESSFUL!")
            print(f"Welcome to {school} DOS Portal")
            print("Access granted to school management system")
        else:
            print("❌ LOGIN FAILED!")
            print("Invalid username or password")

if __name__ == "__main__":
    main()