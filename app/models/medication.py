from sqlalchemy import Column, Integer, String, DateTime, func
from app.utils.db import Base

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    generic_name = Column(String(120), nullable=False, index=True)     # e.g., "acetaminophen"
    brand_name   = Column(String(120), nullable=True)                  # e.g., "Tylenol"
    rxnorm_id    = Column(String(50),  nullable=True, index=True)      # optional code
    form         = Column(String(60),  nullable=True)                  # tablet, solution, etc.
    strength     = Column(String(60),  nullable=True)                  # "500 mg"
    route        = Column(String(60),  nullable=True)                  # oral, IV, IM...
    created_at   = Column(DateTime, server_default=func.now())
