"""Test script for TVET integration"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.school import School
from app.models.user import User, UserRole
from app.services.school_service import validate_trade_for_school, get_school_trades

def test_tvet_integration():
    """Test TVET schools and trades integration"""
    db = SessionLocal()
    
    print("=" * 60)
    print("TVET INTEGRATION TEST")
    print("=" * 60)
    
    try:
        # Test 1: Check if schools have trades
        print("\n1. Testing Schools with Trades:")
        print("-" * 60)
        schools = db.query(School).limit(5).all()
        
        if not schools:
            print("❌ No schools found in database. Run seed_tvet_schools.py first!")
            return
        
        for school in schools:
            print(f"\n✓ {school.name}")
            print(f"  Type: {school.type}")
            print(f"  Location: {school.district}, {school.province}")
            print(f"  Trades: {', '.join(school.trades) if school.trades else 'None'}")
        
        # Test 2: Get trades for a specific school
        print("\n\n2. Testing Get School Trades:")
        print("-" * 60)
        test_school = schools[0]
        trades = get_school_trades(db, test_school.id)
        print(f"School: {test_school.name}")
        print(f"Available Trades: {', '.join(trades) if trades else 'None'}")
        
        # Test 3: Validate trade for school
        print("\n\n3. Testing Trade Validation:")
        print("-" * 60)
        if trades:
            valid_trade = trades[0]
            print(f"Testing valid trade '{valid_trade}' for {test_school.name}...")
            try:
                validate_trade_for_school(db, test_school.id, valid_trade)
                print(f"✓ Valid trade accepted")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print(f"\nTesting invalid trade 'InvalidTrade' for {test_school.name}...")
            try:
                validate_trade_for_school(db, test_school.id, "InvalidTrade")
                print(f"❌ Invalid trade was accepted (should have failed)")
            except Exception as e:
                print(f"✓ Invalid trade rejected: {e}")
        
        # Test 4: Check users with trades
        print("\n\n4. Testing Users with Selected Trades:")
        print("-" * 60)
        users_with_trades = db.query(User).filter(User.selected_trade.isnot(None)).limit(5).all()
        
        if users_with_trades:
            for user in users_with_trades:
                print(f"\n✓ {user.full_name}")
                print(f"  Email: {user.email}")
                print(f"  Role: {user.role.value}")
                print(f"  School ID: {user.school_id}")
                print(f"  Selected Trade: {user.selected_trade}")
        else:
            print("No users with selected trades found yet.")
        
        # Test 5: Statistics
        print("\n\n5. Statistics:")
        print("-" * 60)
        total_schools = db.query(School).count()
        tvet_schools = db.query(School).filter(School.type == "TVET").count()
        tss_schools = db.query(School).filter(School.type == "TSS").count()
        schools_with_trades = db.query(School).filter(School.trades.isnot(None)).count()
        
        print(f"Total Schools: {total_schools}")
        print(f"TVET Schools: {tvet_schools}")
        print(f"TSS Schools: {tss_schools}")
        print(f"Schools with Trades: {schools_with_trades}")
        
        # Get unique trades
        all_schools = db.query(School).all()
        all_trades = set()
        for school in all_schools:
            if school.trades:
                all_trades.update(school.trades)
        
        print(f"\nUnique Trades Available: {len(all_trades)}")
        if all_trades:
            print("Trades:")
            for trade in sorted(all_trades):
                print(f"  - {trade}")
        
        print("\n" + "=" * 60)
        print("✓ TVET INTEGRATION TEST COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_tvet_integration()
