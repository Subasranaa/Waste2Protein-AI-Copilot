from fastapi import APIRouter
import os
from app.services.dependencies import prediction_service  # same shared instance
from app.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.get("/")
def health_check():
    logger.debug("Health check called")
    model_status = prediction_service.get_status()
    
    return {
        "status": "healthy" if model_status["loaded"] else "degraded",
        "service": "waste2protein-backend",
        "model_loaded": model_status["loaded"],
        "model_version": model_status["version"],
        "model_error": model_status["error"],
        "llm_provider": os.getenv("LLM_PROVIDER", "mock"),
        "llm_configured": bool(os.getenv("GROQ_API_KEY"))
    }
