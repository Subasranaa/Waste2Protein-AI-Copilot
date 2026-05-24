from fastapi import APIRouter
from app.schemas import PredictionInput, PredictionOutput
from app.services.dependencies import prediction_service
from app.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.post("/", response_model=PredictionOutput)
def predict_protein_yield(input_data: PredictionInput):
    logger.info(f"POST /predict | waste_type={input_data.waste_type}")
    return prediction_service.predict(input_data)
