#!/usr/bin/env python3

import pandas as pd
import sqlite3
import hashlib
import os
from datetime import datetime

def create_database():
    """Create DOS users database"""
    conn = sqlite3.connect('dos_users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dos_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            school_name TEXT NOT NULL,
            province TEXT,
            district TEXT,
            sector TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_username(school_name):
    """Create username from school name"""
    # Remove common words and clean up
    clean_name = school_name.upper()
    clean_name = clean_name.replace('TVET', '').replace('SCHOOL', '').replace('COLLEGE', '')
    clean_name = clean_name.replace('TECHNICAL', '').replace('VOCATIONAL', '')
    clean_name = ''.join(c for c in clean_name if c.isalnum() or c.isspace())
    
    # Take first letters of words
    words = clean_name.split()
    if len(words) >= 2:
        username = ''.join(word[0] for word in words[:3] if word)
    else:
        username = clean_name[:6].replace(' ', '')
    
    return f"DOS_{username}".upper()

def main():
    print("Setting up DOS login system...")
    
    # Create database
    conn = create_database()
    cursor = conn.cursor()
    
    # Read Excel file
    excel_file = '10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx'
    
    try:
        df = pd.read_excel(excel_file)
        print(f"Loaded {len(df)} rows from Excel")
        
        # Clean column names
        df.columns = ['Province', 'School_Name', 'District', 'Sector', 'Trade', 'Level', 'Gender']
        
        # Remove header rows and empty rows
        df = df[df['Province'].notna() & (df['Province'] != 'Province')]
        df = df[df['School_Name'].notna()]
        
        # Get unique schools
        schools = df[['Province', 'School_Name', 'District', 'Sector']].drop_duplicates()
        
        print(f"Found {len(schools)} unique schools")
        
        created_count = 0
        for _, school in schools.iterrows():
            try:
                username = create_username(school['School_Name'])
                password = "dos2024"  # Default password
                password_hash = hash_password(password)
                
                cursor.execute('''
                    INSERT OR IGNORE INTO dos_users 
                    (username, password_hash, school_name, province, district, sector)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (username, password_hash, school['School_Name'], 
                     school['Province'], school['District'], school['Sector']))
                
                if cursor.rowcount > 0:
                    created_count += 1
                    print(f"Created: {username} for {school['School_Name']}")
                
            except Exception as e:
                print(f"Error creating account for {school['School_Name']}: {e}")
        
        conn.commit()
        print(f"\nSUCCESS: Created {created_count} DOS accounts")
        
        # Show sample accounts
        cursor.execute('SELECT username, school_name FROM dos_users LIMIT 5')
        sample_accounts = cursor.fetchall()
        
        print("\nSample DOS accounts:")
        for username, school_name in sample_accounts:
            print(f"Username: {username} | School: {school_name}")
        
        print(f"\nDefault password for all accounts: dos2024")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()