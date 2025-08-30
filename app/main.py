from fastapi import FastAPI

app = FastAPI(title="MediDose API")

@app.get("/health")
def health():
    return {"status": "ok"}
