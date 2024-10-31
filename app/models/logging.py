from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text

from app.utils.database import Base

class LoginModel(Base):
    __tablename__ = 'login_stamp'

    id = Column(Integer, primary_key=True, nullable=False)
    user_ref = Column(String, ForeignKey('users.ref', ondelete="NO ACTION"), nullable=False)
    token = Column(String, nullable=False)
    # expiration = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'))
    location = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'))