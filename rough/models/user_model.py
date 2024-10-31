from sqlalchemy import Column, Date, Enum, String

from rough.utils.db import Base
from rough.models.ancestor import AncestorModel
from rough.utils.globals import USER_ROLES


class User(Base, AncestorModel):
    __tablename__ = 'users'
    
    ref = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)
    role = Column(Enum(*USER_ROLES, name='role'), default='USER', nullable=False)
    preferred_categories = Column(String, nullable=True)
