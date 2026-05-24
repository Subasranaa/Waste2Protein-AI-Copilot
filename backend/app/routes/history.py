from fastapi import APIRouter
from app.database import SessionLocal, PredictionRecord
from app.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.get("/")
def get_prediction_history(limit: int = 20):
    if not SessionLocal:
        return {"error": "Database not configured"}
    try:
        db = SessionLocal()
        records = db.query(PredictionRecord)\
            .order_by(PredictionRecord.timestamp.desc())\
            .limit(limit)\
            .all()
        db.close()
        logger.info(f"History requested | returning {len(records)} records")
        return [
            {
                "id": r.id,
                "waste_type": r.waste_type,
                "location": r.location,
                "predicted_protein_yield": r.predicted_protein_yield,
                "confidence_level": r.confidence_level,
                "timestamp": r.timestamp,
            }
            for r in records
        ]
    except Exception as e:
        logger.error(f"History fetch failed: {e}")
        return {"error": "Could not fetch history"}
