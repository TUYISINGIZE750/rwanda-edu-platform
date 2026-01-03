#!/usr/bin/env python3
"""
Direct production database fix for DOS password
Run this on the production server to fix the DOS password issue
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import bcrypt

# Production database URL (from environment or default)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/db")

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def fix_dos_password():
    """Fix the DOS password in production database"""
    try:
        # Create engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Find the DOS user
        result = db.execute(
            text("SELECT id, email, full_name FROM users WHERE email = :email"),
            {"email": "dos.rundatvet.kamonyi@iprc.ac.rw"}
        )
        user = result.fetchone()
        
        if not user:
            print("[ERROR] DOS user not found")
            return False
        
        print(f"[FOUND] User: {user.email} (ID: {user.id})")
        
        # Hash the new password
        new_password = "dos123"
        hashed_password = hash_password(new_password)
        
        # Update the password
        db.execute(
            text("UPDATE users SET hashed_password = :password WHERE id = :user_id"),
            {"password": hashed_password, "user_id": user.id}
        )
        db.commit()
        
        print(f"[SUCCESS] Password updated for {user.email}")
        print(f"New password: {new_password}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to fix password: {e}")
        return False

if __name__ == "__main__":
    print("=== Production DOS Password Fix ===")
    success = fix_dos_password()
    
    if success:
        print("\n✅ DOS password fixed successfully!")
        print("You can now login with:")
        print("Email: dos.rundatvet.kamonyi@iprc.ac.rw")
        print("Password: dos123")
    else:
        print("\n❌ Failed to fix DOS password")
        sys.exit(1)