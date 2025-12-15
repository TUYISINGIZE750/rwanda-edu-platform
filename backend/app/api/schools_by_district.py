"""
Enhanced Schools by District API
Provides clean district-to-schools mapping for registration flow
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from ..core.database import get_db
from ..models.school import School
from sqlalchemy import func

router = APIRouter(prefix="/schools-by-district", tags=["schools-by-district"])

class SchoolInfo(BaseModel):
    id: int
    name: str
    type: str
    category: str
    trades: List[str]
    trades_count: int

class DistrictSchools(BaseModel):
    district: str
    province: str
    schools_count: int
    schools: List[SchoolInfo]

class ProvinceData(BaseModel):
    province: str
    districts: List[DistrictSchools]
    total_schools: int

@router.get("/all", response_model=List[ProvinceData])
def get_all_schools_by_district(db: Session = Depends(get_db)):
    """Get all schools organized by province and district"""
    
    schools = db.query(School).all()
    
    if not schools:
        return []
    
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
        
        school_info = SchoolInfo(
            id=school.id,
            name=school.name,
            type=school.type,
            category=school.category,
            trades=trades,
            trades_count=len(trades)
        )
        
        provinces_data[province][district].append(school_info)
    
    # Convert to response format
    result = []
    
    for province, districts in provinces_data.items():
        province_districts = []
        total_schools = 0
        
        for district, schools_list in districts.items():
            district_data = DistrictSchools(
                district=district,
                province=province,
                schools_count=len(schools_list),
                schools=schools_list
            )
            province_districts.append(district_data)
            total_schools += len(schools_list)
        
        province_data = ProvinceData(
            province=province,
            districts=province_districts,
            total_schools=total_schools
        )
        result.append(province_data)
    
    return result

@router.get("/district/{province}/{district}", response_model=DistrictSchools)
def get_schools_in_district(
    province: str, 
    district: str, 
    db: Session = Depends(get_db)
):
    """Get all schools in a specific district"""
    
    from urllib.parse import unquote
    province = unquote(province)
    district = unquote(district)
    
    # Case-insensitive search
    schools = db.query(School).filter(
        func.lower(School.province) == province.lower(),
        func.lower(School.district) == district.lower()
    ).all()
    
    if not schools:
        raise HTTPException(
            status_code=404, 
            detail=f"No schools found in {district}, {province}"
        )
    
    schools_list = []
    for school in schools:
        trades = school.trades if hasattr(school, 'trades') and school.trades else []
        
        school_info = SchoolInfo(
            id=school.id,
            name=school.name,
            type=school.type,
            category=school.category,
            trades=trades,
            trades_count=len(trades)
        )
        schools_list.append(school_info)
    
    return DistrictSchools(
        district=district,
        province=province,
        schools_count=len(schools_list),
        schools=schools_list
    )

@router.get("/summary")
def get_schools_summary(db: Session = Depends(get_db)):
    """Get summary statistics of schools by district"""
    
    schools = db.query(School).all()
    
    if not schools:
        return {
            "total_schools": 0,
            "total_provinces": 0,
            "total_districts": 0,
            "districts_by_province": {}
        }
    
    provinces = set()
    districts = set()
    districts_by_province = {}
    
    for school in schools:
        provinces.add(school.province)
        districts.add(f"{school.province}:{school.district}")
        
        if school.province not in districts_by_province:
            districts_by_province[school.province] = set()
        districts_by_province[school.province].add(school.district)
    
    # Convert sets to counts
    districts_by_province_counts = {}
    for province, district_set in districts_by_province.items():
        districts_by_province_counts[province] = len(district_set)
    
    return {
        "total_schools": len(schools),
        "total_provinces": len(provinces),
        "total_districts": len(districts),
        "districts_by_province": districts_by_province_counts
    }