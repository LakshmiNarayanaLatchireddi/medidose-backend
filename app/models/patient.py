# app/models/patient.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.utils.db import Base


class Patient(Base):
    __tablename__ = "patients"

    # Keys
    id = Column(Integer, primary_key=True, index=True)

    # CASCADE so deleting a user removes their patient records in dev/prod
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Core identity
    full_name = Column(String(200), nullable=False)
    dob = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)  # male | female | other

    # Vitals / anthropometrics
    weight_kg = Column(Float, nullable=True)
    height_cm = Column(Float, nullable=True)
    blood_type = Column(String(5), nullable=True)  # e.g., O+, A-, etc.

    # Contact
    phone = Column(String(30), nullable=True)
    address_line1 = Column(String(200), nullable=True)
    address_line2 = Column(String(200), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)

    # Medical / admin
    allergies = Column(String(500), nullable=True)
    conditions = Column(String(1000), nullable=True)
    insurance_provider = Column(String(200), nullable=True)
    insurance_policy_number = Column(String(100), nullable=True)
    emergency_contact_name = Column(String(200), nullable=True)
    emergency_contact_phone = Column(String(30), nullable=True)

    notes = Column(String(2000), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="patients", lazy="joined")
