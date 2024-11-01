from datetime import date
from typing import Optional
from pydantic import BaseModel


class PostBaseSchema(BaseModel):
    ref: str
    owner_ref: str
    content: str
    pub_date: Optional[date] = None
    type: Optional[str] = None
    categories: Optional[str] = None

class PostCreateSchema(BaseModel):
    content: str
    author: Optional[str] = None
    pub_date: Optional[date] = None
    type: Optional[str] = None
    categories: Optional[str] = None

class PostUpdateSchema(BaseModel):
    content: Optional[str] = None
    author: Optional[str] = None
    pub_date: Optional[date] = None
    type: Optional[str] = None
    categories: Optional[str] = None
