#!/usr/bin/env python3
"""
Simple script to fix DOS login system based on Excel file
Creates DOS accounts for all TVET schools from the Excel file
"""

import pandas as pd
import sqlite3
from werkzeug.security import generate_password_hash
import re
import json

def clean_school_name(name):
    """Clean and normalize school name"""
    if pd.isna(name) or not name:
        return None
    
    name = str(name).strip()
    if not name or name.lower() in ['nan', 'none', '']:
        return None
    
    # Remove extra spaces and normalize
    name = re.sub(r'\s+', ' ', name)
    return name.title()

def generate_dos_email(school_name, district):
    """Generate DOS email from school name and district"""
    if not school_name or not district:
        return None
    
    # Clean school name for email
    school_clean = re.sub(r'[^a-zA-Z0-9\s]', '', school_name.lower())
    school_clean = re.sub(r'\s+', '', school_clean)
    
    # Clean district name
    district_clean = re.sub(r'[^a-zA-Z0-9]', '', district.lower())
    
    # Create email
    email = f"dos.{school_clean}.{district_clean}@iprc.ac.rw"
    return email

def main():
    print("Starting DOS login system fix...")
    
    # Read Excel file
    excel_file = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    try:
        df = pd.read_excel(excel_file)
        print(f"Excel file loaded with {len(df)} rows")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return
    
    # Connect to database
    try:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        print("Connected to database")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return
    
    # Process schools
    schools_created = 0
    dos_accounts = []
    
    # Get unique schools from the Excel data
    # Assuming columns are: Province, School Name, District, etc.
    for index, row in df.iterrows():
        try:
            # Skip header rows and empty rows
            if index < 2:  # Skip first 2 rows (headers)
                continue
            
            province = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else None
            school_name = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else None
            district = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else None
            
            # Skip if essential data is missing
            if not school_name or not district or not province:
                continue
            
            # Clean school name
            school_name = clean_school_name(school_name)
            if not school_name:
                continue
            
            # Generate DOS email
            dos_email = generate_dos_email(school_name, district)
            if not dos_email:
                continue
            
            # Check if school already exists
            cursor.execute("SELECT id FROM schools WHERE name = ? AND district = ?", (school_name, district))
            school_row = cursor.fetchone()
            
            if not school_row:
                # Create school
                cursor.execute("""
                    INSERT INTO schools (name, district, province, type, trades)
                    VALUES (?, ?, ?, 'TVET', '["General"]')
                """, (school_name, district, province))
                school_id = cursor.lastrowid
                print(f"Created school: {school_name} in {district}")
            else:
                school_id = school_row[0]
            
            # Check if DOS user already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (dos_email,))
            user_row = cursor.fetchone()
            
            if not user_row:
                # Create DOS user
                password = "dos123"  # Simple default password
                hashed_password = generate_password_hash(password)
                
                cursor.execute("""
                    INSERT INTO users (email, hashed_password, full_name, role, school_id, 
                                     province, district, is_active, generated_password)
                    VALUES (?, ?, ?, 'admin', ?, ?, ?, 1, ?)
                """, (dos_email, hashed_password, f"DOS {school_name}", school_id, 
                      province, district, password))
                
                dos_accounts.append({
                    "school": school_name,
                    "district": district,
                    "email": dos_email,
                    "password": password
                })
                
                schools_created += 1
                print(f"Created DOS account: {dos_email}")
        
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\nCompleted! Created {schools_created} DOS accounts")
    
    # Save credentials to file
    with open('dos_credentials_simple.json', 'w') as f:
        json.dump(dos_accounts, f, indent=2)
    
    print(f"Credentials saved to dos_credentials_simple.json")
    
    # Print some sample credentials
    print("\nSample DOS credentials:")
    for i, account in enumerate(dos_accounts[:5]):
        print(f"{i+1}. {account['school']} ({account['district']})")
        print(f"   Email: {account['email']}")
        print(f"   Password: {account['password']}")
        print()

if __name__ == "__main__":
    main()