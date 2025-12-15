#!/usr/bin/env python3
"""
STEP 1: Identify and display all schools organized by district
This script shows the current school data structure for registration flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.school import School
from app.core.database import Base
import json

# Database setup
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def show_schools_by_district():
    """Display all schools organized by district for registration flow"""
    
    db = SessionLocal()
    try:
        # Get all schools
        schools = db.query(School).all()
        
        if not schools:
            print("No schools found in database")
            return
        
        # Organize schools by province and district
        provinces_data = {}
        
        for school in schools:
            province = school.province
            district = school.district
            
            if province not in provinces_data:
                provinces_data[province] = {}
            
            if district not in provinces_data[province]:
                provinces_data[province][district] = []
            
            # Get trades for the school
            trades = school.trades if hasattr(school, 'trades') and school.trades else []
            
            school_info = {
                'id': school.id,
                'name': school.name,
                'type': school.type,
                'category': school.category,
                'trades': trades,
                'trades_count': len(trades)
            }
            
            provinces_data[province][district].append(school_info)
        
        # Display organized data
        print("RWANDA TVET/TSS SCHOOLS BY DISTRICT")
        print("=" * 60)
        
        total_schools = 0
        
        for province, districts in provinces_data.items():
            print(f"\nPROVINCE: {province}")
            print("-" * 40)
            
            for district, schools_list in districts.items():
                print(f"\n  DISTRICT: {district}")
                print(f"     Schools: {len(schools_list)}")
                
                for school in schools_list:
                    print(f"     - {school['name']}")
                    print(f"       Type: {school['type']} | Category: {school['category']}")
                    print(f"       Trades: {school['trades_count']} available")
                    if school['trades']:
                        trades_preview = school['trades'][:3]  # Show first 3 trades
                        trades_text = ", ".join(trades_preview)
                        if len(school['trades']) > 3:
                            trades_text += f" (+{len(school['trades']) - 3} more)"
                        print(f"       -> {trades_text}")
                    print()
                
                total_schools += len(schools_list)
        
        print(f"\nSUMMARY:")
        print(f"   Total Provinces: {len(provinces_data)}")
        print(f"   Total Districts: {sum(len(districts) for districts in provinces_data.values())}")
        print(f"   Total Schools: {total_schools}")
        
        # Create registration flow data structure
        registration_data = {
            'provinces': []
        }
        
        for province, districts in provinces_data.items():
            province_data = {
                'name': province,
                'districts': []
            }
            
            for district, schools_list in districts.items():
                district_data = {
                    'name': district,
                    'schools_count': len(schools_list),
                    'schools': schools_list
                }
                province_data['districts'].append(district_data)
            
            registration_data['provinces'].append(province_data)
        
        # Save to JSON file for frontend use
        with open('schools_by_district.json', 'w', encoding='utf-8') as f:
            json.dump(registration_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nRegistration data saved to: schools_by_district.json")
        print("\nREGISTRATION FLOW READY:")
        print("   1. User selects Province -> District")
        print("   2. System auto-displays all schools in that district")
        print("   3. User selects school -> System shows trades")
        print("   4. User selects trade -> System shows levels")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    show_schools_by_district()