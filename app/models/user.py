from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.utils.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="patient")  # patient | doctor | admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
