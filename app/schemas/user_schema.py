from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    id: int
    ref: str
    username: Optional[str] = None
    email: EmailStr
    
    class Config:
        from_attributes = True

class UserFullSchema(UserBaseSchema):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    birthdate: Optional[date] = None
    role: Optional[str] = None
    preferred_categories: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    birthdate: Optional[date] = None

class UserUpdateSchema(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    birthdate: Optional[date] = None