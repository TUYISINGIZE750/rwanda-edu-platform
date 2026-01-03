#!/usr/bin/env python3
"""
Create DOS accounts from Excel file
Based on 10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx
"""

import pandas as pd
import json
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.school import School
from app.core.security import get_password_hash

def parse_excel_schools():
    """Parse Excel file and extract unique schools"""
    file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    try:
        df = pd.read_excel(file_path)
        print(f"Loaded Excel with {len(df)} rows")
        
        schools = {}
        
        for idx, row in df.iterrows():
            # Skip header row
            if idx == 0:
                continue
                
            province = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
            district = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
            school_code = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
            school_name = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            trade_full = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ""
            trade_code = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ""
            gender = str(row.iloc[6]).strip() if pd.notna(row.iloc[6]) else ""
            
            # Skip empty rows
            if not school_name or not school_code or school_name == "nan":
                continue
                
            # Create unique school key
            school_key = f"{school_code}_{school_name}"
            
            if school_key not in schools:
                schools[school_key] = {
                    'province': province,
                    'district': district,
                    'school_code': school_code,
                    'school_name': school_name,
                    'trades': [],
                    'gender': gender
                }
            
            # Add trade if valid
            if trade_code and trade_code != "nan":
                schools[school_key]['trades'].append({
                    'trade_full': trade_full,
                    'trade_code': trade_code
                })
        
        school_list = list(schools.values())
        print(f"Extracted {len(school_list)} unique schools")
        
        return school_list
        
    except Exception as e:
        print(f"Error parsing Excel: {e}")
        return []

def create_school_in_db(school_data, db: Session):
    """Create or update school in database"""
    try:
        # Check if school exists
        existing = db.query(School).filter(
            School.name == school_data['school_name']
        ).first()
        
        if existing:
            # Update trades
            trades = [t['trade_code'] for t in school_data['trades']]
            existing.trades = trades
            db.commit()
            return existing.id
        
        # Create new school
        trades = [t['trade_code'] for t in school_data['trades']]
        school = School(
            name=school_data['school_name'],
            province=school_data['province'],
            district=school_data['district'],
            trades=trades,
            type="TVET"
        )
        
        db.add(school)
        db.commit()
        db.refresh(school)
        
        print(f"Created school: {school.name}")
        return school.id
        
    except Exception as e:
        print(f"Error creating school {school_data['school_name']}: {e}")
        db.rollback()
        return None

def generate_dos_credentials(school_data):
    """Generate DOS credentials for a school"""
    # Clean school name for email
    clean_name = school_data['school_name'].lower()
    clean_name = clean_name.replace(' ', '').replace('-', '').replace('_', '')
    clean_name = ''.join(c for c in clean_name if c.isalnum())
    
    # Clean district name
    district_clean = school_data['district'].lower().replace(' ', '')
    
    # Generate email
    email = f"dos.{clean_name}@{district_clean}.tvet.rw"
    
    # Generate username
    username = f"dos_{school_data['school_code']}"
    
    # Default password
    password = "dos123"
    
    # Full name
    full_name = f"DOS - {school_data['school_name']}"
    
    return {
        'username': username,
        'email': email,
        'password': password,
        'full_name': full_name
    }

def create_dos_account(school_data, school_id, db: Session):
    """Create DOS account for a school"""
    try:
        credentials = generate_dos_credentials(school_data)
        
        # Check if DOS already exists
        existing = db.query(User).filter(User.email == credentials['email']).first()
        if existing:
            print(f"DOS already exists: {credentials['email']}")
            return credentials
        
        # Create DOS user
        dos_user = User(
            email=credentials['email'],
            hashed_password=get_password_hash(credentials['password']),
            full_name=credentials['full_name'],
            role=UserRole.ADMIN,
            school_id=school_id,
            province=school_data['province'],
            district=school_data['district'],
            is_active=1
        )
        
        db.add(dos_user)
        db.commit()
        
        print(f"Created DOS: {credentials['email']}")
        return credentials
        
    except Exception as e:
        print(f"Error creating DOS for {school_data['school_name']}: {e}")
        db.rollback()
        return None

def main():
    """Main function to create DOS accounts from Excel"""
    print("Creating DOS accounts from Excel file")
    print("=" * 60)
    
    # Parse Excel
    schools = parse_excel_schools()
    if not schools:
        print("No schools found in Excel file")
        return
    
    # Database session
    db = SessionLocal()
    
    try:
        created_credentials = []
        
        for school_data in schools:
            print(f"\nProcessing: {school_data['school_name']}")
            
            # Create/update school
            school_id = create_school_in_db(school_data, db)
            if not school_id:
                continue
            
            # Create DOS account
            credentials = create_dos_account(school_data, school_id, db)
            if credentials:
                created_credentials.append({
                    'school': school_data['school_name'],
                    'district': school_data['district'],
                    'province': school_data['province'],
                    **credentials
                })
        
        # Save credentials to JSON
        with open('dos_credentials_all.json', 'w') as f:
            json.dump(created_credentials, f, indent=2)
        
        print(f"\nSuccessfully processed {len(schools)} schools")
        print(f"Created {len(created_credentials)} DOS accounts")
        print(f"Credentials saved to: dos_credentials_all.json")
        
        # Print summary
        print("\nDOS Login Summary:")
        print("-" * 40)
        for cred in created_credentials[:5]:  # Show first 5
            print(f"School: {cred['school']}")
            print(f"Email: {cred['email']}")
            print(f"Password: {cred['password']}")
            print("-" * 40)
        
        if len(created_credentials) > 5:
            print(f"... and {len(created_credentials) - 5} more schools")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()