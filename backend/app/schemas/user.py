from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from ..models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    school_id: int
    province: str
    district: str
    grade: Optional[int] = None
    selected_trade: Optional[str] = None
    selected_level: Optional[str] = None
    locale: str = "rw"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: int
    is_class_teacher: Optional[int] = 0
    managed_class_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
