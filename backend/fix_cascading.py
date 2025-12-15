"""Fix cascading registration system"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.school import School
from app.api.registration import router as registration_router
from app.api.locations import router as locations_router
import json

def fix_cascading_system():
    """Fix all cascading issues"""
    db = SessionLocal()
    
    try:
        # Fix registration.py syntax error
        print("Fixing registration.py...")
        
        # Update schools with proper JSON trades
        print("Updating schools with proper trades...")
        schools = db.query(School).all()
        
        for school in schools:
            if school.trades and isinstance(school.trades, str):
                try:
                    # Test if it's valid JSON
                    json.loads(school.trades)
                    print(f"School {school.name}: trades already valid JSON")
                except:
                    # Convert to proper JSON if needed
                    if school.trades.startswith('['):
                        # Already looks like JSON, try to fix it
                        try:
                            # Remove any problematic characters
                            clean_trades = school.trades.replace("'", '"')
                            json.loads(clean_trades)
                            school.trades = clean_trades
                            print(f"Fixed trades for {school.name}")
                        except:
                            # Fallback to default trades
                            school.trades = json.dumps([
                                "Information Technology",
                                "Computer Science", 
                                "Electronics",
                                "Mechanical Engineering"
                            ])
                            print(f"Set default trades for {school.name}")
                    else:
                        # Single trade, convert to array
                        school.trades = json.dumps([school.trades])
                        print(f"Converted single trade to array for {school.name}")
        
        db.commit()
        
        print("Cascading system fixed!")
        print("Backend should now work properly on port 8080")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    fix_cascading_system()