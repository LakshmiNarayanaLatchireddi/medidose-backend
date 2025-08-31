from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from app.utils.settings import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
