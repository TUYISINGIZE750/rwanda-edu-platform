#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reset Elam user password"""

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def reset_elam_password():
    db = SessionLocal()
    
    # Find the user
    user = db.query(User).filter(User.email == "Elam@gmail.com").first()
    if not user:
        print("User Elam@gmail.com not found!")
        return
    
    # Reset password to a known value
    new_password = "teacher123"
    user.hashed_password = get_password_hash(new_password)
    user.is_active = True  # Ensure account is active
    
    db.commit()
    
    print("Password reset successfully!")
    print(f"Email: {user.email}")
    print(f"New Password: {new_password}")
    print(f"Role: {user.role.value}")
    print(f"Active: {user.is_active}")
    print(f"Full Name: {user.full_name}")
    
    db.close()

if __name__ == "__main__":
    reset_elam_password()