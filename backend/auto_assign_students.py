#!/usr/bin/env python3
"""
Automatic Student Assignment System
Matches students to classes based on trade and level
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.group import Group
from app.models.group_member import GroupMember
from sqlalchemy import or_

def auto_assign_students():
    """Automatically assign students to matching classes"""
    db = SessionLocal()
    
    try:
        print("[*] Starting automatic student assignment...\n")
        
        # Get all classes
        classes = db.query(Group).filter_by(type='CLASS').all()
        
        if not classes:
            print("[!] No classes found!")
            return
        
        total_assigned = 0
        
        for group in classes:
            print(f"[+] Processing: {group.name}")
            
            # Extract level and trade from class name
            # Format examples: "L5 SWD", "Level 5 Software Development", "L4 Electronics"
            name_upper = group.name.upper()
            
            # Extract level
            level = None
            for num in ['1', '2', '3', '4', '5', '6']:
                if f'L{num}' in name_upper or f'LEVEL {num}' in name_upper or f'LEVEL{num}' in name_upper:
                    level = f'Level {num}'
                    break
            
            # Extract trade keywords
            trade_keywords = []
            if 'SWD' in name_upper or 'SOFTWARE' in name_upper:
                trade_keywords = ['Software Development', 'SWD', 'Software']
            elif 'ELECTRONICS' in name_upper or 'ELECTRONIC' in name_upper:
                trade_keywords = ['Electronics', 'Electronic']
            elif 'ELECTRICAL' in name_upper:
                trade_keywords = ['Electrical']
            elif 'MECHANICAL' in name_upper:
                trade_keywords = ['Mechanical']
            elif 'CIVIL' in name_upper:
                trade_keywords = ['Civil']
            elif 'PLUMBING' in name_upper:
                trade_keywords = ['Plumbing']
            
            # Require BOTH level AND trade for auto-assignment
            if not level or not trade_keywords:
                print(f"   [!] Skipping - need both level and trade (found: level={level}, trade={trade_keywords})")
                continue
            
            print(f"   Level: {level}")
            print(f"   Trade: {', '.join(trade_keywords)}")
            
            # Find matching students (BOTH level AND trade must match)
            query = db.query(User).filter_by(role='student')
            query = query.filter(User.selected_level == level)
            
            # Match any of the trade keywords
            trade_filters = [User.selected_trade.ilike(f'%{keyword}%') for keyword in trade_keywords]
            query = query.filter(or_(*trade_filters))
            
            matching_students = query.all()
            
            print(f"   Found {len(matching_students)} matching students")
            
            assigned_count = 0
            for student in matching_students:
                # Check if already a member
                existing = db.query(GroupMember).filter_by(
                    group_id=group.id,
                    user_id=student.id
                ).first()
                
                if not existing:
                    # Add to class
                    member = GroupMember(
                        group_id=group.id,
                        user_id=student.id
                    )
                    db.add(member)
                    assigned_count += 1
                    print(f"   [+] Added: {student.full_name}")
            
            if assigned_count > 0:
                db.commit()
                total_assigned += assigned_count
                print(f"   [+] Assigned {assigned_count} new students")
            else:
                print(f"   [i] No new students to assign")
            
            print()
        
        print(f"[+] COMPLETE! Total students assigned: {total_assigned}")
    
    finally:
        db.close()

if __name__ == '__main__':
    auto_assign_students()
