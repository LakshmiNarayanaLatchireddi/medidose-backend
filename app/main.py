from fastapi import FastAPI
from sqlalchemy import text
from app.utils.db import engine

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
from app.routers import users as users_router
app.include_router(users_router.router)
