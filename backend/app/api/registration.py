"""Registration flow API with innovative cascading data selection"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, configure_mappers
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from ..core.database import get_db
from ..models.school import School

# Ensure all mappers are configured
try:
    configure_mappers()
except Exception:
    pass

router = APIRouter(prefix="/registration", tags=["registration"])

# TVET Levels - Default system levels
TVET_LEVELS = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"]

@router.get("/health")
def registration_health_check():
    """Health check for registration API"""
    return {"status": "healthy", "service": "registration"}

class SchoolOption(BaseModel):
    id: int
    name: str
    type: str
    category: str
    trades: List[str]
    total_trades: int
    location: str

class TradeOption(BaseModel):
    name: str
    school_count: int
    available_levels: List[str]

class LevelOption(BaseModel):
    name: str
    description: str
    is_default: bool

class CascadingRegistrationResponse(BaseModel):
    step: str
    province: Optional[str] = None
    district: Optional[str] = None
    schools: Optional[List[SchoolOption]] = None
    selected_school: Optional[SchoolOption] = None
    trades: Optional[List[TradeOption]] = None
    selected_trade: Optional[str] = None
    levels: Optional[List[LevelOption]] = None
    total_schools: Optional[int] = None
    total_trades: Optional[int] = None
    message: Optional[str] = None

@router.get("/cascade", response_model=CascadingRegistrationResponse)
def get_cascading_data(
    province: str,
    district: str,
    school_id: Optional[int] = None,
    trade: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    INNOVATIVE CASCADING REGISTRATION SYSTEM
    Step 1: Province + District → Auto-display all TVET/TSS schools
    Step 2: School Selection → Auto-display all trades in that school
    Step 3: Trade Selection → Auto-display all levels (Level 1-6)
    """
    from sqlalchemy import func, or_, select
    
    try:
        # Map province variations
        province_variations = [province, province.replace(' Province', ''), province.replace(' City', '')]
        province_filters = [func.lower(School.province) == p.lower() for p in province_variations]
        
        # STEP 1: Get all TVET/TSS schools in the district
        stmt = select(School).filter(
            or_(*province_filters),
            func.lower(School.district) == district.lower()
        )
        schools = db.execute(stmt).scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    if not schools:
        return CascadingRegistrationResponse(
            step="no_schools",
            province=province,
            district=district,
            message=f"No TVET/TSS schools found in {district}, {province}"
        )
    
    # Create school options with enhanced info
    school_options = []
    for s in schools:
        trades = s.trades if hasattr(s, 'trades') and s.trades else []
        
        school_options.append(SchoolOption(
            id=s.id,
            name=s.name,
            type=s.type,
            category=s.category,
            trades=trades,
            total_trades=len(trades),
            location=f"{s.district}, {s.province}"
        ))
    
    response = CascadingRegistrationResponse(
        step="schools_loaded",
        province=province,
        district=district,
        schools=school_options,
        total_schools=len(schools),
        message=f"Found {len(schools)} TVET/TSS schools in {district}"
    )
    
    # STEP 2: If school selected, auto-display trades
    if school_id:
        selected_school = next((s for s in schools if s.id == school_id), None)
        if not selected_school:
            raise HTTPException(status_code=404, detail="School not found")
        
        # Create trade options with metadata
        selected_trades = selected_school.trades if hasattr(selected_school, 'trades') and selected_school.trades else []
        
        trade_options = []
        for trade_name in selected_trades:
            # Count how many schools offer this trade
            schools_with_trade = 0
            for s in schools:
                s_trades = s.trades if hasattr(s, 'trades') and s.trades else []
                if trade_name in s_trades:
                    schools_with_trade += 1
            
            trade_options.append(TradeOption(
                name=trade_name,
                school_count=schools_with_trade,
                available_levels=TVET_LEVELS
            ))
        
        response.step = "trades_loaded"
        response.selected_school = SchoolOption(
            id=selected_school.id,
            name=selected_school.name,
            type=selected_school.type,
            category=selected_school.category,
            trades=selected_trades,
            total_trades=len(selected_trades),
            location=f"{selected_school.district}, {selected_school.province}"
        )
        response.trades = trade_options
        response.total_trades = len(trade_options)
        response.message = f"Found {len(trade_options)} trades in {selected_school.name}"
    
    # STEP 3: If trade selected, auto-display levels
    if trade:
        level_options = [
            LevelOption(
                name="Level 1",
                description="Foundation Level - Basic skills and knowledge",
                is_default=True
            ),
            LevelOption(
                name="Level 2",
                description="Intermediate Level - Building on foundation",
                is_default=False
            ),
            LevelOption(
                name="Level 3",
                description="Advanced Level - Specialized skills",
                is_default=False
            ),
            LevelOption(
                name="Level 4",
                description="Professional Level - Industry-ready skills",
                is_default=False
            ),
            LevelOption(
                name="Level 5",
                description="Expert Level - Leadership and management",
                is_default=False
            ),
            LevelOption(
                name="Level 6",
                description="Master Level - Innovation and research",
                is_default=False
            )
        ]
        
        response.step = "levels_loaded"
        response.selected_trade = trade
        response.levels = level_options
        response.message = f"All 6 levels available for {trade}"
    
    return response

@router.get("/schools/{province}/{district}")
def get_schools_by_location(province: str, district: str, db: Session = Depends(get_db)):
    """STEP 1: Auto-display all TVET/TSS schools when province + district selected"""
    from sqlalchemy import func, or_, select
    
    try:
        # Map province names to database format - try multiple variations
        province_variations = [
            province,
            province.replace(' Province', ''),
            province.replace(' City', ''),
        ]
        
        # Add common mappings
        province_map = {
            'Southern Province': ['South', 'Southern', 'Southern Province'],
            'Western Province': ['West', 'Western', 'Western Province'],
            'Northern Province': ['North', 'Northern', 'Northern Province'],
            'Eastern Province': ['East', 'Eastern', 'Eastern Province'],
            'Kigali City': ['Kigali city', 'Kigali', 'Kigali City']
        }
        
        if province in province_map:
            province_variations.extend(province_map[province])
        
        # Build query with multiple province variations
        province_filters = [func.lower(School.province) == p.lower() for p in province_variations]
        
        # Case-insensitive search with multiple province options - use execute to avoid mapper issues
        stmt = select(School).filter(
            or_(*province_filters),
            func.lower(School.district) == district.lower()
        )
        schools = db.execute(stmt).scalars().all()
        
        if not schools:
            return {
                "success": False,
                "message": f"No TVET/TSS schools found in {district}, {province}",
                "schools": [],
                "total": 0
            }
        
        school_data = []
        for s in schools:
            trades = s.trades if hasattr(s, 'trades') and s.trades else []
            
            school_data.append({
                "id": s.id,
                "name": s.name,
                "type": s.type,
                "category": s.category,
                "trades": trades,
                "total_trades": len(trades),
                "location": f"{s.district}, {s.province}",
                "display_name": f"{s.name} ({s.type} - {len(trades)} trades)"
            })
        
        return {
            "success": True,
            "message": f"Found {len(schools)} TVET/TSS schools in {district}",
            "schools": school_data,
            "total": len(schools),
            "location": f"{district}, {province}"
        }
    except Exception as e:
        # Return error response instead of raising exception
        return {
            "success": False,
            "message": f"Error loading schools: {str(e)}",
            "schools": [],
            "total": 0
        }

@router.get("/trades/{school_id}")
def get_trades_by_school(school_id: int, db: Session = Depends(get_db)):
    """STEP 2: Auto-display all trades when school is selected"""
    from sqlalchemy import select
    stmt = select(School).filter(School.id == school_id)
    school = db.execute(stmt).scalars().first()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    trades = school.trades if school.trades else []
    
    if not trades:
        return {
            "success": False,
            "message": f"No trades available in {school.name}",
            "school_id": school_id,
            "school_name": school.name,
            "trades": [],
            "total": 0
        }
    
    # Enhanced trade data
    trade_data = []
    for trade in trades:
        trade_data.append({
            "name": trade,
            "display_name": trade,
            "levels_available": TVET_LEVELS,
            "total_levels": len(TVET_LEVELS)
        })
    
    return {
        "success": True,
        "message": f"Found {len(trades)} trades in {school.name}",
        "school_id": school_id,
        "school_name": school.name,
        "school_type": school.type,
        "trades": trade_data,
        "total": len(trades)
    }

@router.get("/levels")
def get_levels():
    """STEP 3: Auto-display all levels when trade is selected"""
    level_names = {
        'Level 1': 'Foundation',
        'Level 2': 'Intermediate', 
        'Level 3': 'Advanced',
        'Level 4': 'Professional',
        'Level 5': 'Expert',
        'Level 6': 'Master'
    }
    
    levels_data = []
    for i, level in enumerate(TVET_LEVELS, 1):
        levels_data.append({
            "name": level,
            "value": level,
            "number": i,
            "description": {
                "Level 1": "Foundation Level - Basic skills and knowledge",
                "Level 2": "Intermediate Level - Building on foundation", 
                "Level 3": "Advanced Level - Specialized skills",
                "Level 4": "Professional Level - Industry-ready skills",
                "Level 5": "Expert Level - Leadership and management",
                "Level 6": "Master Level - Innovation and research"
            }.get(level, "TVET Level"),
            "is_default": level == "Level 1",
            "display_name": f"{level} - {level_names.get(level, 'TVET')}"
        })
    
    return {
        "success": True,
        "message": "All TVET levels available (Default: Level 1-6)",
        "levels": levels_data,
        "total": len(TVET_LEVELS),
        "default_level": "Level 1",
        "system_note": "System uses Level 1, Level 2, Level 3, Level 4, Level 5, Level 6 as default"
    }

@router.get("/complete-flow/{province}/{district}/{school_id}/{trade}")
def get_complete_registration_flow(
    province: str, 
    district: str, 
    school_id: int, 
    trade: str, 
    db: Session = Depends(get_db)
):
    """Complete registration flow validation - all steps in one call"""
    
    # Validate school exists in location
    from sqlalchemy import select
    stmt = select(School).filter(
        School.id == school_id,
        School.province == province,
        School.district == district
    )
    school = db.execute(stmt).scalars().first()
    
    if not school:
        raise HTTPException(
            status_code=404, 
            detail=f"School ID {school_id} not found in {district}, {province}"
        )
    
    # Validate trade exists in school
    school_trades = school.trades if hasattr(school, 'trades') and school.trades else []
    
    if trade not in school_trades:
        raise HTTPException(
            status_code=404,
            detail=f"Trade '{trade}' not available in {school.name}"
        )
    
    return {
        "success": True,
        "message": "Complete registration flow validated",
        "flow_summary": {
            "step_1": f"Province: {province}, District: {district}",
            "step_2": f"School: {school.name} ({school.type})",
            "step_3": f"Trade: {trade}",
            "step_4": f"Levels: {', '.join(TVET_LEVELS)}"
        },
        "registration_ready": True,
        "school": {
            "id": school.id,
            "name": school.name,
            "type": school.type,
            "category": school.category
        },
        "selected_trade": trade,
        "available_levels": TVET_LEVELS,
        "default_level": "Level 1"
    }
