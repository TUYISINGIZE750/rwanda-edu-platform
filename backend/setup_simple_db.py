"""Setup database for cascading registration system - Simple version"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal, engine
from app.models.school import School
from app.models.user import User
from sqlalchemy import text
import json

def setup_cascading_database():
    """Setup database with trades column and sample data"""
    db = SessionLocal()
    
    print("=" * 80)
    print("SETTING UP CASCADING REGISTRATION DATABASE")
    print("=" * 80)
    
    try:
        # Add trades column to schools if it doesn't exist
        print("\n[STEP 1] Adding trades column to schools...")
        
        try:
            db.execute(text("ALTER TABLE schools ADD COLUMN trades TEXT"))
            db.commit()
            print("OK Trades column added successfully")
        except Exception as e:
            if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                print("OK Trades column already exists")
            else:
                print(f"Adding column failed: {e}")
        
        # Add cascading columns to users table
        print("\n[STEP 1.5] Adding cascading columns to users...")
        
        cascading_columns = [
            ("selected_trade", "TEXT"),
            ("selected_level", "TEXT")
        ]
        
        for column_name, column_type in cascading_columns:
            try:
                db.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"))
                db.commit()
                print(f"OK {column_name} column added successfully")
            except Exception as e:
                if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"OK {column_name} column already exists")
                else:
                    print(f"Adding {column_name} column failed: {e}")
        
        # Check if we have schools
        print("\n[STEP 2] Checking existing schools...")
        schools_count = db.query(School).count()
        print(f"Found {schools_count} existing schools")
        
        if schools_count == 0:
            print("No schools found. Creating sample TVET schools...")
            create_sample_schools(db)
        else:
            print("Updating existing schools with trades...")
            update_schools_with_trades(db)
        
        # Verify setup
        print("\n[STEP 3] Verifying cascading setup...")
        schools = db.query(School).all()
        schools_with_trades = [s for s in schools if s.trades]
        print(f"OK {len(schools_with_trades)} schools have trades configured")
        
        if schools_with_trades:
            sample = schools_with_trades[0]
            try:
                trades_list = json.loads(sample.trades) if isinstance(sample.trades, str) else sample.trades
                print(f"OK Sample school: {sample.name}")
                print(f"OK Sample trades: {trades_list[:3] if trades_list else 'None'}")
            except:
                print(f"OK Sample school: {sample.name}")
                print(f"OK Sample trades: {sample.trades}")
        
        print("\n" + "=" * 80)
        print("SUCCESS: CASCADING DATABASE SETUP COMPLETE!")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

def create_sample_schools(db):
    """Create sample TVET schools with trades"""
    
    sample_schools = [
        {
            "name": "Kigali Institute of Science and Technology (KIST)",
            "type": "TVET",
            "category": "Public",
            "province": "Kigali City",
            "district": "Gasabo",
            "trades": [
                "Information Technology",
                "Computer Science",
                "Electronics",
                "Telecommunications",
                "Software Development",
                "Network Administration"
            ]
        },
        {
            "name": "Rwanda Polytechnic - IPRC Kigali",
            "type": "TVET",
            "category": "Public", 
            "province": "Kigali City",
            "district": "Nyarugenge",
            "trades": [
                "Mechanical Engineering",
                "Civil Engineering", 
                "Electrical Engineering",
                "Automotive Technology",
                "Construction Technology",
                "Welding and Fabrication"
            ]
        },
        {
            "name": "Tumba College of Technology (TCT)",
            "type": "TSS",
            "category": "Public",
            "province": "Southern Province", 
            "district": "Rulindo",
            "trades": [
                "Agriculture Technology",
                "Animal Husbandry",
                "Crop Production",
                "Food Processing",
                "Veterinary Technology",
                "Agricultural Mechanics"
            ]
        },
        {
            "name": "IPRC Musanze",
            "type": "TVET",
            "category": "Public",
            "province": "Northern Province",
            "district": "Musanze", 
            "trades": [
                "Tourism and Hospitality",
                "Hotel Management",
                "Culinary Arts",
                "Tour Guiding",
                "Event Management",
                "Restaurant Management"
            ]
        },
        {
            "name": "IPRC Huye",
            "type": "TVET", 
            "category": "Public",
            "province": "Southern Province",
            "district": "Huye",
            "trades": [
                "Business Administration",
                "Accounting",
                "Marketing",
                "Entrepreneurship",
                "Finance",
                "Human Resources"
            ]
        },
        {
            "name": "IPRC Kitabi",
            "type": "TSS",
            "category": "Public", 
            "province": "Southern Province",
            "district": "Nyamagabe",
            "trades": [
                "Forestry Technology",
                "Environmental Science",
                "Wildlife Management",
                "Eco-Tourism",
                "Natural Resource Management",
                "Conservation Technology"
            ]
        }
    ]
    
    for school_data in sample_schools:
        school = School(
            name=school_data["name"],
            type=school_data["type"],
            category=school_data["category"],
            province=school_data["province"],
            district=school_data["district"],
            trades=json.dumps(school_data["trades"])
        )
        db.add(school)
    
    db.commit()
    print(f"OK Created {len(sample_schools)} sample TVET/TSS schools")

def update_schools_with_trades(db):
    """Update existing schools with sample trades"""
    
    # Common TVET trades by type
    tvet_trades = [
        "Information Technology",
        "Computer Science", 
        "Electronics",
        "Mechanical Engineering",
        "Civil Engineering",
        "Electrical Engineering",
        "Business Administration",
        "Accounting",
        "Marketing"
    ]
    
    tss_trades = [
        "Agriculture Technology",
        "Animal Husbandry",
        "Crop Production",
        "Food Processing",
        "Tourism and Hospitality",
        "Hotel Management"
    ]
    
    schools = db.query(School).all()
    updated_count = 0
    
    for school in schools:
        if not school.trades:
            # Assign trades based on school type
            if "TVET" in school.type.upper():
                school.trades = json.dumps(tvet_trades[:6])  # First 6 trades
            elif "TSS" in school.type.upper():
                school.trades = json.dumps(tss_trades[:4])   # First 4 trades
            else:
                school.trades = json.dumps(tvet_trades[:4])  # Default trades
            updated_count += 1
    
    db.commit()
    print(f"OK Updated {updated_count} schools with trades")

if __name__ == "__main__":
    success = setup_cascading_database()
    
    if success:
        print("\nSUCCESS: Database ready for cascading registration!")
        print("   Run: python test_cascading_simple.py")
    else:
        print("\nFAILED: Database setup failed!")
    
    sys.exit(0 if success else 1)