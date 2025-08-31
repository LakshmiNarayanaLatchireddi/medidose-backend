from sqlalchemy import Column, Integer, String, DateTime, func
from app.utils.db import Base

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True)
    rxnorm_id = Column(String(50), index=True)
    generic_name = Column(String(255), index=True)
    brand_name = Column(String(255), nullable=True)
    form = Column(String(100), nullable=True)
    strength = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
