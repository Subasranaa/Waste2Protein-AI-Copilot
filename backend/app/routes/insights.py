from fastapi import APIRouter
from app.schemas import PredictionInput
from app.services.dependencies import (
    prediction_service,
    llm_service,
    cost_tracker,
    cache_service,
    economics_service,
)
from app.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.post("/")
def generate_prediction_insight(input_data: PredictionInput):
    payload = input_data.model_dump()
    cache_key = cache_service.make_key(payload)

    # Check cache first
    cached_response = cache_service.get(cache_key)
    if cached_response:
        logger.info(f"Cache hit | key={cache_key}")
        return cached_response

    logger.info(f"Cache miss | waste_type={input_data.waste_type} | generating fresh response")

    # Run pipeline
    prediction_result = prediction_service.predict(input_data)
    # LLM service now returns insight + real token usage
    llm_response = llm_service.generate_insight(input_data, prediction_result)

    # Calculate real cost from real token counts
    if "token_usage" in llm_response:
        usage = llm_response["token_usage"]
        cost_info = cost_tracker.calculate_real_cost(
            prompt_tokens=usage["prompt_tokens"],
            completion_tokens=usage["completion_tokens"],
        )
        llm_insight = llm_response["insight"]
    else:
        # Fallback was used — no real LLM call
        cost_info = cost_tracker.estimate_mock_cost(0, 0)
        llm_insight = llm_response

    
    economic_estimate = economics_service.estimate(
        input_data=input_data,
        predicted_protein_yield=prediction_result["predicted_protein_yield"],
    )
    
    response = {
        "prediction": prediction_result,
        "insight": llm_insight,
        "economic_estimate": economic_estimate,
        "llm_cost": cost_info,
    }

    cache_service.set(cache_key, response)
    return response
