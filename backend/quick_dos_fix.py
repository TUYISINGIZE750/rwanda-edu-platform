import sqlite3
import pandas as pd
import hashlib
import json

def create_dos_login():
    # Read Excel file
    df = pd.read_excel('10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx')
    
    # Connect to database
    conn = sqlite3.connect('education_platform.db')
    cursor = conn.cursor()
    
    # Create DOS users table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dos_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            school_name TEXT NOT NULL,
            province TEXT,
            district TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Clear existing DOS users
    cursor.execute('DELETE FROM dos_users')
    
    credentials = []
    count = 0
    
    # Process each row
    for index, row in df.iterrows():
        if index == 0:  # Skip header
            continue
            
        try:
            province = str(row.iloc[0]) if pd.notna(row.iloc[0]) else 'Unknown'
            school_name = str(row.iloc[1]) if pd.notna(row.iloc[1]) else f'School_{index}'
            district = str(row.iloc[2]) if pd.notna(row.iloc[2]) else 'Unknown'
            
            if school_name and school_name != 'nan' and len(school_name) > 3:
                # Create username from school name
                username = school_name.lower().replace(' ', '_').replace('-', '_')[:20] + f'_{index}'
                password = f'dos{index}2024'
                password_hash = hashlib.md5(password.encode()).hexdigest()
                
                # Insert DOS user
                cursor.execute('''
                    INSERT INTO dos_users (username, password, school_name, province, district)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password_hash, school_name, province, district))
                
                credentials.append({
                    'username': username,
                    'password': password,
                    'school_name': school_name,
                    'province': province,
                    'district': district
                })
                count += 1
                
        except Exception as e:
            continue
    
    conn.commit()
    conn.close()
    
    # Save credentials
    with open('dos_login_credentials.json', 'w') as f:
        json.dump(credentials, f, indent=2)
    
    print(f"SUCCESS! Created {count} DOS login accounts")
    print(f"Credentials saved to dos_login_credentials.json")
    
    # Show first 5 credentials
    print("\nFirst 5 DOS Login Credentials:")
    for i, cred in enumerate(credentials[:5]):
        print(f"{i+1}. Username: {cred['username']}")
        print(f"   Password: {cred['password']}")
        print(f"   School: {cred['school_name']}")
        print()

if __name__ == "__main__":
    create_dos_login()