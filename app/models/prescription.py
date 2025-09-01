from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.utils.db import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)

    # who is it for and what medication
    patient_id    = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False, index=True)

    # dose & schedule
    dosage        = Column(String(80),  nullable=False)   # "500 mg"
    route         = Column(String(60),  nullable=True)    # "oral"
    frequency     = Column(String(100), nullable=True)    # "TID", "every 8 hours"
    duration      = Column(String(100), nullable=True)    # "5 days"
    notes         = Column(String(300), nullable=True)

    created_at    = Column(DateTime, server_default=func.now())

    # optional ORM relationships
    patient       = relationship("Patient", backref="prescriptions")
    medication    = relationship("Medication")
