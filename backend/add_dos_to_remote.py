"""Create DOS users from Excel file"""
import json
import os
import sys

# Set database URL to remote
os.environ['DATABASE_URL'] = 'postgresql://rwanda_edu_db_user:kcXqPqxqJLqGLqxqJLqGLqxqJLqGLqxq@dpg-ctalmhij1k6c73f6pu50-a.oregon-postgres.render.com/rwanda_edu_db'

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_dos_users():
    # Load credentials
    with open('dos_credentials_from_excel.json', 'r', encoding='utf-8') as f:
        credentials = json.load(f)
    
    db = SessionLocal()
    
    try:
        print(f"Creating {len(credentials)} DOS users...")
        
        created = 0
        skipped = 0
        
        for cred in credentials:
            # Check if user exists
            existing = db.query(User).filter_by(email=cred['username']).first()
            if existing:
                skipped += 1
                continue
            
            # Create DOS user
            dos_user = User(
                email=cred['username'],
                hashed_password=get_password_hash(cred['password']),
                full_name=f"DOS - {cred['school_name']}",
                role=UserRole.ADMIN,
                school_id=int(cred['school_code']),
                province=cred['province'],
                district=cred['district'],
                is_active=1
            )
            
            db.add(dos_user)
            created += 1
            
            if created % 10 == 0:
                db.commit()
                print(f"Created {created}/{len(credentials)}...")
        
        db.commit()
        
        print(f"\n{'='*50}")
        print(f"SUCCESS!")
        print(f"Created: {created} DOS users")
        print(f"Skipped: {skipped} (already exist)")
        print(f"Total: {len(credentials)}")
        print(f"{'='*50}")
        
        # Show sample credentials
        print("\nSample DOS Credentials:")
        for i in range(min(5, len(credentials))):
            c = credentials[i]
            print(f"\n{c['province']} - {c['district']}")
            print(f"  School: {c['school_name']}")
            print(f"  Email: {c['username']}")
            print(f"  Password: {c['password']}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_dos_users()
