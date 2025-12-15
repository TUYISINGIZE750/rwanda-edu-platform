"""Setup database for cascading registration system"""
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
        # Check if trades column exists
        print("\n[STEP 1] Checking database schema...")
        
        try:
            # Try to query trades column
            result = db.execute(text("SELECT trades FROM schools LIMIT 1"))
            print("✓ Trades column already exists")
        except Exception:
            print("Adding trades column to schools table...")
            # Add trades column
            db.execute(text("ALTER TABLE schools ADD COLUMN trades TEXT"))
            db.commit()
            print("✓ Trades column added successfully")
        
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
        schools_with_trades = db.query(School).filter(School.trades.isnot(None)).all()
        print(f"✓ {len(schools_with_trades)} schools have trades configured")
        
        if schools_with_trades:
            sample = schools_with_trades[0]
            trades_list = json.loads(sample.trades) if isinstance(sample.trades, str) else sample.trades
            print(f"✓ Sample school: {sample.name}")
            print(f"✓ Sample trades: {trades_list[:3] if trades_list else 'None'}")
        
        print("\n" + "=" * 80)
        print("✅ CASCADING DATABASE SETUP COMPLETE!")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
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
    print(f"✓ Created {len(sample_schools)} sample TVET/TSS schools")

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
    
    for school in schools:
        if not school.trades:
            # Assign trades based on school type
            if "TVET" in school.type.upper():
                school.trades = json.dumps(tvet_trades[:6])  # First 6 trades
            elif "TSS" in school.type.upper():
                school.trades = json.dumps(tss_trades[:4])   # First 4 trades
            else:
                school.trades = json.dumps(tvet_trades[:4])  # Default trades
    
    db.commit()
    print(f"✓ Updated {len(schools)} schools with trades")

if __name__ == "__main__":
    success = setup_cascading_database()
    
    if success:
        print("\n🎯 Database ready for cascading registration!")
        print("   Run: python test_cascading_simple.py")
    else:
        print("\n❌ Database setup failed!")
    
    sys.exit(0 if success else 1)