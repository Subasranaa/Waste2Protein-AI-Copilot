from fastapi import APIRouter
from app.schemas import PredictionInput, PredictionOutput
from app.services.prediction_service import PredictionService

router = APIRouter()
prediction_service = PredictionService()

@router.post("/", response_model=PredictionOutput)
def predict_protein_yield(input_data: PredictionInput):
    return prediction_service.predict(input_data)


