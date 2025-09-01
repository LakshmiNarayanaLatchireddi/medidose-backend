from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.db import SessionLocal
from app.models.medication import Medication

router = APIRouter(prefix="/medications", tags=["medications"])

# ---------- Schemas ----------
class MedicationCreate(BaseModel):
    generic_name: str
    brand_name: Optional[str] = None
    rxnorm_id: Optional[str] = None
    strength: Optional[str] = None
    form: Optional[str] = None
    route: Optional[str] = None

class MedicationOut(BaseModel):
    id: int
    generic_name: str
    brand_name: Optional[str]
    rxnorm_id: Optional[str]
    strength: Optional[str]
    form: Optional[str]
    route: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2

# ---------- DB dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Endpoints ----------
@router.post("", response_model=MedicationOut, status_code=status.HTTP_201_CREATED)
def create_medication(payload: MedicationCreate, db: Session = Depends(get_db)):
    # Optional uniqueness guard
    existing = (
        db.query(Medication)
        .filter(
            Medication.generic_name.ilike(payload.generic_name),
            Medication.strength == payload.strength,
            Medication.form == payload.form,
        )
        .first()
    )
    if existing:
        raise HTTPException(400, "Medication with same generic/strength/form already exists.")

    med = Medication(
        generic_name=payload.generic_name.strip(),
        brand_name=payload.brand_name,
        rxnorm_id=payload.rxnorm_id,
        strength=payload.strength,
        form=payload.form,
        route=payload.route,
    )
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


@router.get("", response_model=List[MedicationOut])
def list_medications(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Search generic/brand"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    query = db.query(Medication)
    if q:
        like = f"%{q}%"
        query = query.filter((Medication.generic_name.ilike(like)) | (Medication.brand_name.ilike(like)))
    return query.order_by(Medication.generic_name.asc()).offset(offset).limit(limit).all()
