import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env at runtime
load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret")
    ENV: str = os.getenv("ENV", "development")

settings = Settings()

# Debug prints
print("🔍 Loaded DATABASE_URL:", settings.DATABASE_URL)
print("🔍 Loaded ENV:", settings.ENV)
