from sqlalchemy import Column, TIMESTAMP, Integer, text

class ParentModel():
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'),
                        onupdate=text('now()'))
