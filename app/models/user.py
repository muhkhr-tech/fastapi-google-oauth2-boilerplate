from sqlalchemy import Column, Integer, String, DateTime, func

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    refresh_token = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # UTC by PostgreSQL
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # UTC by PostgreSQL
        nullable=False
    )
    deleted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # UTC by PostgreSQL
        nullable=False
    )
