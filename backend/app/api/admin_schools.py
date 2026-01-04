from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..core.database import get_db
from ..models.school import School
import pandas as pd
import os
from collections import defaultdict

router = APIRouter(prefix="/admin/schools", tags=["admin-schools"])

@router.post("/schools/add-columns")
def add_missing_columns(db: Session = Depends(get_db)):
    """Add missing school_code and gender columns - ADMIN ONLY"""
    try:
        # Execute raw SQL to add columns
        db.execute(text("ALTER TABLE schools ADD COLUMN IF NOT EXISTS school_code VARCHAR"))
        db.execute(text("ALTER TABLE schools ADD COLUMN IF NOT EXISTS gender VARCHAR"))
        db.commit()
        
        return {"success": True, "message": "Columns added successfully"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

@router.post("/reload-from-excel")
def reload_schools_from_excel(db: Session = Depends(get_db)):
    """Reload schools from Excel file - ADMIN ONLY"""
    # Try multiple possible paths
    possible_paths = [
        "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx",
        "../10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx",
        "/app/10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx",
        os.path.join(os.path.dirname(__file__), "../../10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx")
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
    
    if not file_path:
        raise HTTPException(status_code=404, detail=f"Excel file not found in any of the expected locations")
    
    try:
        # Read Excel
        df = pd.read_excel(file_path, header=1)
        df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
        
        # Group trades by school
        schools_data = defaultdict(lambda: {
            'trades': [],
            'school_code': None,
            'name': None,
            'province': None,
            'district': None,
            'gender': None
        })
        
        for idx, row in df.iterrows():
            if pd.isna(row['School Name']) or pd.isna(row['District']):
                continue
            
            school_key = (str(row['School Name']).strip(), str(row['District']).strip())
            school_data = schools_data[school_key]
            
            school_data['school_code'] = str(row['School code']).strip() if pd.notna(row['School code']) else None
            school_data['name'] = str(row['School Name']).strip()
            school_data['province'] = str(row['Province']).strip()
            school_data['district'] = str(row['District']).strip()
            school_data['gender'] = str(row['Gender']).strip() if pd.notna(row['Gender']) else 'Mixt'
            
            if pd.notna(row['Trade in full']):
                trade = str(row['Trade in full']).strip()
                if trade and trade not in school_data['trades']:
                    school_data['trades'].append(trade)
        
        # Clear existing schools
        db.query(School).delete()
        db.commit()
        
        # Insert schools
        schools_added = 0
        for (school_name, district), school_data in schools_data.items():
            school = School(
                school_code=school_data['school_code'],
                name=school_data['name'],
                type='TVET',
                category='Public',
                province=school_data['province'],
                district=school_data['district'],
                trades=school_data['trades'],
                gender=school_data['gender']
            )
            db.add(school)
            schools_added += 1
        
        db.commit()
        
        # Verify RUNDA TVET
        runda = db.query(School).filter(School.name.ilike('%RUNDA%')).first()
        runda_info = None
        if runda:
            runda_info = {
                "id": runda.id,
                "name": runda.name,
                "district": runda.district,
                "trades_count": len(runda.trades) if runda.trades else 0,
                "trades": runda.trades
            }
        
        return {
            "success": True,
            "schools_loaded": schools_added,
            "runda_tvet_verification": runda_info
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error reloading schools: {str(e)}")
