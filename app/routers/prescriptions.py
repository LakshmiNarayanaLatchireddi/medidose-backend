from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.utils.db import SessionLocal
from app.models.prescription import Prescription
from app.models.patient import Patient
from app.models.medication import Medication
from app.models.user import User

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])

# ---------- Schemas ----------
class PrescriptionCreate(BaseModel):
    patient_id: int
    medication_id: int
    prescribed_by: int = Field(..., description="User ID of prescriber (doctor)")
    dose: str
    units: Optional[str] = None
    frequency: Optional[str] = None   # e.g., q8h, BID
    duration: Optional[int] = None    # days
    notes: Optional[str] = None

class PrescriptionOut(BaseModel):
    id: int
    patient_id: int
    medication_id: int
    prescribed_by: int
    dose: str
    units: Optional[str]
    frequency: Optional[str]
    duration: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True

# ---------- DB dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Endpoints ----------
@router.post("", response_model=PrescriptionOut, status_code=status.HTTP_201_CREATED)
def create_prescription(payload: PrescriptionCreate, db: Session = Depends(get_db)):
    # FK checks
    if not db.query(Patient).filter(Patient.id == payload.patient_id).first():
        raise HTTPException(404, "Patient not found")
    if not db.query(Medication).filter(Medication.id == payload.medication_id).first():
        raise HTTPException(404, "Medication not found")
    prescriber = db.query(User).filter(User.id == payload.prescribed_by).first()
    if not prescriber:
        raise HTTPException(404, "Prescriber (user) not found")
    if prescriber.role != "doctor":
        raise HTTPException(400, "Prescriber must have role 'doctor'")

    rx = Prescription(
        patient_id=payload.patient_id,
        medication_id=payload.medication_id,
        prescribed_by=payload.prescribed_by,
        dose=payload.dose,
        units=payload.units,
        frequency=payload.frequency,
        duration=payload.duration,
        notes=payload.notes,
    )
    db.add(rx)
    db.commit()
    db.refresh(rx)
    return rx


@router.get("", response_model=List[PrescriptionOut])
def list_prescriptions(
    db: Session = Depends(get_db),
    patient_id: Optional[int] = Query(None),
    prescriber_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    q = db.query(Prescription)
    if patient_id:
        q = q.filter(Prescription.patient_id == patient_id)
    if prescriber_id:
        q = q.filter(Prescription.prescribed_by == prescriber_id)
    return q.order_by(Prescription.id.desc()).offset(offset).limit(limit).all()
