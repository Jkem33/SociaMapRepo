from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace values with your own info
DATABASE_URL = "postgresql://postgres:databasePassword33@localhost:5432/SocioMap"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# ✅ Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()