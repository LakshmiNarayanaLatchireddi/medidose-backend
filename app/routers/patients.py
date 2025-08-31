from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import date
from app.utils.db import SessionLocal
from app.models.user import User
from app.models.patient import Patient

router = APIRouter(prefix="/patients", tags=["patients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------- Schemas ----------
class PatientCreate(BaseModel):
    user_id: int = Field(..., description="Existing user id (doctor or patient)")
    full_name: str
    dob: date | None = None
    gender: str | None = None
    weight_kg: float | None = None
    height_cm: float | None = None
    allergies: str | None = None
    conditions: str | None = None

class PatientOut(BaseModel):
    id: int
    user_id: int
    full_name: str
    dob: date | None = None
    gender: str | None = None
    weight_kg: float | None = None
    height_cm: float | None = None
    allergies: str | None = None
    conditions: str | None = None

    class Config:
        from_attributes = True

# --------- Routes ----------
@router.post("", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    # Ensure user exists
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Linked user not found")

    patient = Patient(
        user_id=payload.user_id,
        full_name=payload.full_name,
        dob=payload.dob,
        gender=payload.gender,
        weight_kg=payload.weight_kg,
        height_cm=payload.height_cm,
        allergies=payload.allergies,
        conditions=payload.conditions,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("", response_model=list[PatientOut])
def list_patients(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    return db.query(Patient).order_by(Patient.id).offset(offset).limit(limit).all()

@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
