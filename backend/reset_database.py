#!/usr/bin/env python3
"""Reset database with correct schema"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from app.models import Base

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables with new schema...")
    Base.metadata.create_all(bind=engine)
    
    print("Database reset complete!")

if __name__ == "__main__":
    reset_database()