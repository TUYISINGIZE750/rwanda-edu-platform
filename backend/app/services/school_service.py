"""School and trade validation service"""
from sqlalchemy.orm import Session
from ..models.school import School
from fastapi import HTTPException

def validate_trade_for_school(db: Session, school_id: int, trade: str) -> bool:
    """Validate that a trade is offered by a school"""
    school = db.query(School).filter(School.id == school_id).first()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    if not school.trades:
        return True  # If no trades specified, allow any
    
    if trade and trade not in school.trades:
        raise HTTPException(
            status_code=400, 
            detail=f"Trade '{trade}' is not offered by {school.name}. Available trades: {', '.join(school.trades)}"
        )
    
    return True

def get_school_trades(db: Session, school_id: int) -> list:
    """Get all trades offered by a school"""
    school = db.query(School).filter(School.id == school_id).first()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    return school.trades or []
