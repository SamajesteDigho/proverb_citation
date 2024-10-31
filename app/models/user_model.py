from sqlalchemy import Column, Date, Enum, String

from app.models.parent import ParentModel
from app.utils.database import Base

class UserModel(Base, ParentModel):
    __tablename__ = 'users'
    
    ref = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)
    role = Column(Enum('ADMIN', 'AGENT', 'USER', name='role'), default='USER', nullable=False)
    preferred_categories = Column(String, nullable=True)
