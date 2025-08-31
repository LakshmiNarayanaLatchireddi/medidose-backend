from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.utils.db import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["users"])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # "doctor" or "patient"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    class Config:
        from_attributes = True

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    # check unique email
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=payload.email,
        hashed_password=pwd.hash(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id).limit(50).all()
