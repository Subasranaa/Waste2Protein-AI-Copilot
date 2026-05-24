# backend/app/database.py
import os
from sqlalchemy import create_engine, Column, Float, String, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from app.logger import setup_logger

logger = setup_logger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    logger.info("Database connection established")
else:
    engine = None
    SessionLocal = None
    logger.warning("No DATABASE_URL set — running without database")

Base = declarative_base()

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    # Inputs — matches your PredictionInput exactly
    waste_type = Column(String)
    sugar_content = Column(Float)
    nitrogen_content = Column(Float)
    moisture = Column(Float)
    ph = Column(Float)
    temperature = Column(Float)
    fermentation_time = Column(Float)
    waste_volume_kg = Column(Float)
    location = Column(String)

    # Outputs — matches your PredictionOutput exactly
    predicted_protein_yield = Column(Float)
    uncertainty = Column(Float)
    confidence_level = Column(String)
    model_version = Column(String)

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)

def create_tables():
    if engine:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
