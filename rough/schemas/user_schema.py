from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: int
    ref: str
    username: str
    email: EmailStr
    
    class Config:
        from_attributes = True

class UserFull(UserBase):
    firstname: str
    lastname: str
    birthdate: datetime
    role: str
    preferred_categories: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    birthdate: Optional[datetime] = None
