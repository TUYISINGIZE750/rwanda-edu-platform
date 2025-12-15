#!/usr/bin/env python3
"""
Script to add Solange to L5 SWD class
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, Group, GroupMember

def add_student_to_class():
    app = create_app()
    
    with app.app_context():
        # Find Solange
        solange = User.query.filter(
            (User.email.ilike('%solange%')) | 
            (User.full_name.ilike('%solange%'))
        ).first()
        
        if not solange:
            print("❌ Solange not found!")
            print("\nSearching for all students with 'Software Development'...")
            students = User.query.filter(
                User.role == 'student',
                User.selected_trade.ilike('%software%')
            ).all()
            
            if students:
                print(f"\n✅ Found {len(students)} Software Development students:")
                for s in students:
                    print(f"  - {s.full_name} ({s.email}) - Level: {s.selected_level}")
                    
                    # Find L5 SWD class
                    l5_swd = Group.query.filter(Group.name.ilike('%L5%SWD%')).first()
                    if not l5_swd:
                        l5_swd = Group.query.filter(Group.name.ilike('%L5%software%')).first()
                    
                    if l5_swd:
                        # Check if already a member
                        existing = GroupMember.query.filter_by(
                            group_id=l5_swd.id,
                            user_id=s.id
                        ).first()
                        
                        if existing:
                            print(f"    ℹ️  Already in {l5_swd.name}")
                        else:
                            # Add to class
                            member = GroupMember(
                                group_id=l5_swd.id,
                                user_id=s.id,
                                role='member'
                            )
                            db.session.add(member)
                            print(f"    ✅ Added to {l5_swd.name}")
                
                db.session.commit()
                print("\n✅ All Software Development students added to L5 SWD class!")
            else:
                print("❌ No Software Development students found!")
            return
        
        print(f"✅ Found student: {solange.full_name} ({solange.email})")
        print(f"   Trade: {solange.selected_trade}")
        print(f"   Level: {solange.selected_level}")
        
        # Find L5 SWD class
        l5_swd = Group.query.filter(Group.name.ilike('%L5%SWD%')).first()
        if not l5_swd:
            l5_swd = Group.query.filter(Group.name.ilike('%L5%software%')).first()
        
        if not l5_swd:
            print("\n❌ L5 SWD class not found!")
            print("\nAvailable classes:")
            classes = Group.query.all()
            for c in classes:
                print(f"  - {c.name} (ID: {c.id}, Type: {c.type})")
            return
        
        print(f"\n✅ Found class: {l5_swd.name} (ID: {l5_swd.id})")
        
        # Check if already a member
        existing = GroupMember.query.filter_by(
            group_id=l5_swd.id,
            user_id=solange.id
        ).first()
        
        if existing:
            print(f"\nℹ️  {solange.full_name} is already a member of {l5_swd.name}")
            return
        
        # Add to class
        member = GroupMember(
            group_id=l5_swd.id,
            user_id=solange.id,
            role='member'
        )
        db.session.add(member)
        db.session.commit()
        
        print(f"\n✅ SUCCESS! {solange.full_name} has been added to {l5_swd.name}")
        print(f"\nShe should now see the class on her dashboard!")

if __name__ == '__main__':
    add_student_to_class()
