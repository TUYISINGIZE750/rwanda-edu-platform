from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.school import School
from pydantic import BaseModel


router = APIRouter(prefix="/locations", tags=["locations"])

class ProvinceResponse(BaseModel):
    name: str

class DistrictResponse(BaseModel):
    name: str

class SectorResponse(BaseModel):
    name: str

class SchoolResponse(BaseModel):
    id: int
    school_code: str | None = None
    name: str
    type: str
    category: str
    province: str
    district: str
    trades: List[str] = []
    gender: str | None = None
    
    @classmethod
    def from_orm(cls, obj):
        trades = obj.trades if hasattr(obj, 'trades') else []
        return cls(
            id=obj.id,
            school_code=getattr(obj, 'school_code', None),
            name=obj.name,
            type=obj.type,
            category=obj.category,
            province=obj.province,
            district=obj.district,
            trades=trades,
            gender=getattr(obj, 'gender', None)
        )
    
    class Config:
        from_attributes = True

# Rwanda locations data - SIMPLIFIED to match database values
RWANDA_DATA = {
    "provinces": [
        {
            "name": "Kigali city",
            "districts": [
                {"name": "Gasabo"},
                {"name": "Kicukiro"},
                {"name": "Nyarugenge"}
            ]
        },
        {
            "name": "South",
            "districts": [
                {"name": "Gisagara"}, {"name": "Huye"}, {"name": "Kamonyi"}, 
                {"name": "Muhanga"}, {"name": "Nyamagabe"}, {"name": "Nyanza"}, 
                {"name": "Nyaruguru"}, {"name": "Ruhango"}
            ]
        },
        {
            "name": "West",
            "districts": [
                {"name": "Karongi"}, {"name": "Nyabihu"}, {"name": "Ngororero"}, 
                {"name": "Rubavu"}, {"name": "Rusizi"}, {"name": "Nyamasheke"}, 
                {"name": "Rutsiro"}
            ]
        },
        {
            "name": "North",
            "districts": [
                {"name": "Burera"}, {"name": "Gakenke"}, {"name": "Gicumbi"}, 
                {"name": "Musanze"}, {"name": "Rulindo"}
            ]
        },
        {
            "name": "East",
            "districts": [
                {"name": "Bugesera"}, {"name": "Gatsibo"}, {"name": "Kayonza"}, 
                {"name": "Kirehe"}, {"name": "Ngoma"}, {"name": "Nyagatare"}, 
                {"name": "Rwamagana"}
            ]
        }
    ]
}

@router.get("/provinces", response_model=List[ProvinceResponse])
def get_provinces():
    """Get all provinces in Rwanda"""
    provinces = RWANDA_DATA.get("provinces", [])
    return [{"name": province["name"]} for province in provinces]

@router.get("/districts/{province_name}", response_model=List[DistrictResponse])
def get_districts(province_name: str):
    """Get all districts in a province"""
    from urllib.parse import unquote
    province_name = unquote(province_name)
    provinces = RWANDA_DATA.get("provinces", [])
    for province in provinces:
        if province["name"] == province_name:
            districts = province.get("districts", [])
            return [{"name": district["name"]} for district in districts]
    raise HTTPException(status_code=404, detail=f"Province '{province_name}' not found")

@router.get("/sectors/{province_name}/{district_name}", response_model=List[SectorResponse])
def get_sectors(province_name: str, district_name: str):
    """Get all sectors in a district"""
    from urllib.parse import unquote
    print(f"DEBUG: Raw params - province: '{province_name}', district: '{district_name}'")
    province_name = unquote(province_name)
    district_name = unquote(district_name)
    print(f"DEBUG: Decoded params - province: '{province_name}', district: '{district_name}'")
    
    provinces = RWANDA_DATA.get("provinces", [])
    print(f"DEBUG: Available provinces: {[p['name'] for p in provinces]}")
    
    for province in provinces:
        if province["name"] == province_name:
            print(f"DEBUG: Found province '{province_name}'")
            districts = province.get("districts", [])
            print(f"DEBUG: Available districts: {[d['name'] for d in districts]}")
            for district in districts:
                if district["name"] == district_name:
                    print(f"DEBUG: Found district '{district_name}'")
                    sectors = district.get("sectors", [])
                    return [{"name": sector["name"]} for sector in sectors]
            print(f"DEBUG: District '{district_name}' not found")
            break
    else:
        print(f"DEBUG: Province '{province_name}' not found")
    
    raise HTTPException(status_code=404, detail=f"District '{district_name}' not found in province '{province_name}'")

@router.get("/schools/district/{province_name}/{district_name}", response_model=List[SchoolResponse])
def get_schools_by_district(
    province_name: str,
    district_name: str,
    db: Session = Depends(get_db)
):
    """Get all TVET/TSS schools in a district"""
    from urllib.parse import unquote
    from sqlalchemy import func
    try:
        province_name = unquote(province_name)
        district_name = unquote(district_name)
        
        schools = db.query(School).filter(
            func.lower(School.province) == province_name.lower(),
            func.lower(School.district) == district_name.lower()
        ).all()
        return [SchoolResponse.from_orm(school) for school in schools]
    except Exception as e:
        print(f"Error fetching schools: {str(e)}")
        return []

@router.get("/schools/sector/{province_name}/{district_name}/{sector_name}", response_model=List[SchoolResponse])
def get_schools_by_sector(
    province_name: str,
    district_name: str,
    sector_name: str,
    db: Session = Depends(get_db)
):
    """Get all TVET/TSS schools in a sector"""
    from urllib.parse import unquote
    from sqlalchemy import func
    province_name = unquote(province_name)
    district_name = unquote(district_name)
    sector_name = unquote(sector_name)
    # For now, return schools by district since we don't have sector field in School model
    schools = db.query(School).filter(
        func.lower(School.province) == province_name.lower(),
        func.lower(School.district) == district_name.lower()
    ).all()
    return [SchoolResponse.from_orm(school) for school in schools]

@router.get("/schools", response_model=List[SchoolResponse])
def get_all_schools(db: Session = Depends(get_db)):
    """Get all TVET/TSS schools"""
    schools = db.query(School).all()
    return [SchoolResponse.from_orm(school) for school in schools]

@router.get("/schools/{school_id}/trades")
def get_school_trades(school_id: int, db: Session = Depends(get_db)):
    """Get all trades offered by a specific school"""
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return {"school_id": school_id, "school_name": school.name, "trades": school.trades or []}

@router.get("/levels")
def get_tvet_levels():
    """Get all available TVET levels"""
    return {
        "levels": ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"]
    }
