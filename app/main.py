from fastapi import FastAPI
from sqlalchemy import text
from app.utils.db import engine
from app.routers import users as users_router
from app.routers import patients as patients_router   # 👈 moved up here
from app.routers import medications as medications_router
from app.routers import prescriptions as prescriptions_router


app = FastAPI(title="MediDose API")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        v = conn.execute(text("select 1")).scalar_one()
        return {"db": "ok", "value": v}

# 👇 Routers registered once at the bottom
app.include_router(users_router.router)
app.include_router(patients_router.router)
app.include_router(medications_router.router)
app.include_router(prescriptions_router.router)

