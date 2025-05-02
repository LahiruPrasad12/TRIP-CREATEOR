from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:Lahiru12@database.cf0gmcqgug2m.ap-south-1.rds.amazonaws.com:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ Add this get_db function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
