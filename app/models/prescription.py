from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.utils.db import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), index=True)
    medication_id = Column(Integer, ForeignKey("medications.id", ondelete="RESTRICT"), index=True)
    dose = Column(String(100), nullable=False)      # e.g., 500 mg
    route = Column(String(50), nullable=True)       # PO, IV, etc.
    frequency = Column(String(100), nullable=False) # e.g., TID
    duration = Column(String(100), nullable=True)   # e.g., 5 days
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
