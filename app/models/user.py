# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.utils.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Auth / identity
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # RBAC
    # Allowed values: "patient", "doctor", "admin"
    role = Column(String(50), nullable=False, default="patient")

    # Status & timestamps
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    # One user can have 0..N patient profiles (e.g., assistant creating records),
    # or simply 1 profile if they are the patient themself.
    patients = relationship(
        "Patient",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
