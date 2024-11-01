from sqlalchemy import Column, Date, Enum, ForeignKey, String, Integer

from app.models.parent import ParentModel
from app.utils.database import Base

class PostModel(Base, ParentModel):
    __tablename__ = 'posts'
    
    ref = Column(String, nullable=False, unique=True)
    owner_ref = Column(String, ForeignKey('users.ref', ondelete='SET NULL'), nullable=True)
    content = Column(String, nullable=False)
    author = Column(String, server_default='Unknown', nullable=False)
    pub_date = Column(Date, nullable=True)
    type = Column(Enum('POEME', 'PROVERB', 'CITATION', name='type'), default='CITATION', nullable=False)
    categories = Column(String, default='', nullable=False)
    # likes = Column()
    # seen = Column()
    