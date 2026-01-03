#!/usr/bin/env python3
"""
Simple DOS login fix - creates accounts from Excel file
"""

import pandas as pd
import sqlite3
import hashlib
import re
import json

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def clean_school_name(name):
    """Clean school name"""
    if pd.isna(name) or not name:
        return None
    name = str(name).strip()
    if not name or name.lower() in ['nan', 'none', '']:
        return None
    return re.sub(r'\s+', ' ', name).title()

def generate_dos_email(school_name, district):
    """Generate DOS email"""
    if not school_name or not district:
        return None
    
    school_clean = re.sub(r'[^a-zA-Z0-9\s]', '', school_name.lower())
    school_clean = re.sub(r'\s+', '', school_clean)
    district_clean = re.sub(r'[^a-zA-Z0-9]', '', district.lower())
    
    return f"dos.{school_clean}.{district_clean}@iprc.ac.rw"

def main():
    print("Fixing DOS login system...")
    
    # Read Excel file
    excel_file = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    try:
        df = pd.read_excel(excel_file)
        print(f"Loaded Excel with {len(df)} rows")
    except Exception as e:
        print(f"Excel error: {e}")
        return
    
    # Connect to database
    try:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                district TEXT NOT NULL,
                province TEXT NOT NULL,
                type TEXT DEFAULT 'TVET',
                trades TEXT DEFAULT '["General"]'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT DEFAULT 'admin',
                school_id INTEGER,
                province TEXT,
                district TEXT,
                is_active INTEGER DEFAULT 1,
                generated_password TEXT,
                FOREIGN KEY (school_id) REFERENCES schools (id)
            )
        ''')
        
        print("Database connected")
    except Exception as e:
        print(f"Database error: {e}")
        return
    
    # Process Excel data
    dos_accounts = []
    created_count = 0
    
    for index, row in df.iterrows():
        if index < 2:  # Skip headers
            continue
        
        try:
            province = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else None
            school_name = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else None
            district = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else None
            
            if not all([province, school_name, district]):
                continue
            
            school_name = clean_school_name(school_name)
            if not school_name:
                continue
            
            dos_email = generate_dos_email(school_name, district)
            if not dos_email:
                continue
            
            # Check if school exists
            cursor.execute("SELECT id FROM schools WHERE name = ? AND district = ?", 
                         (school_name, district))
            school_row = cursor.fetchone()
            
            if not school_row:
                cursor.execute('''
                    INSERT INTO schools (name, district, province, type, trades)
                    VALUES (?, ?, ?, 'TVET', '["General"]')
                ''', (school_name, district, province))
                school_id = cursor.lastrowid
            else:
                school_id = school_row[0]
            
            # Check if DOS user exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (dos_email,))
            if cursor.fetchone():
                continue  # User already exists
            
            # Create DOS user
            password = "dos123"
            hashed_password = hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (email, hashed_password, full_name, role, school_id,
                                 province, district, is_active, generated_password)
                VALUES (?, ?, ?, 'admin', ?, ?, ?, 1, ?)
            ''', (dos_email, hashed_password, f"DOS {school_name}", school_id,
                  province, district, password))
            
            dos_accounts.append({
                "school": school_name,
                "district": district,
                "province": province,
                "email": dos_email,
                "password": password
            })
            
            created_count += 1
            print(f"Created: {school_name} - {dos_email}")
            
        except Exception as e:
            print(f"Error row {index}: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\nSUCCESS! Created {created_count} DOS accounts")
    
    # Save credentials
    with open('dos_credentials_working.json', 'w') as f:
        json.dump(dos_accounts, f, indent=2)
    
    print("Credentials saved to dos_credentials_working.json")
    
    # Show sample accounts
    print("\nSample DOS Login Credentials:")
    for i, account in enumerate(dos_accounts[:3]):
        print(f"{i+1}. {account['school']} ({account['district']})")
        print(f"   Email: {account['email']}")
        print(f"   Password: {account['password']}")
        print()
    
    print(f"Total accounts created: {len(dos_accounts)}")

if __name__ == "__main__":
    main()