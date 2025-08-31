from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, func
from app.utils.db import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    full_name = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    sex = Column(String(10), nullable=True)
    weight_kg = Column(Integer, nullable=True)
    height_cm = Column(Integer, nullable=True)
    allergies = Column(String(1000), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
