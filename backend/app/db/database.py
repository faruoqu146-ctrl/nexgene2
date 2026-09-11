import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

raw_url = os.getenv("DATABASE_URL", "postgresql+psycopg://nexgene:nexgene_dev_only@localhost:5432/nexgene")

# Render provides postgresql:// — SQLAlchemy + psycopg needs postgresql+psycopg://
if raw_url.startswith("postgresql://"):
    DATABASE_URL = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    DATABASE_URL = raw_url

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
