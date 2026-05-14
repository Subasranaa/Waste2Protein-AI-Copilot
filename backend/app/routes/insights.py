from fastapi import APIRouter

from app.schemas import PredictionInput
from app.services.prediction_service import PredictionService
from app.services.llm_service import LLMService
from app.services.cost_tracker import CostTracker
from app.services.cache_service import CacheService
from app.services.optimisation_service import OptimisationService

router = APIRouter()

prediction_service = PredictionService()
llm_service = LLMService()
cost_tracker = CostTracker()
cache_service = CacheService()
optimisation_service = OptimisationService()



@router.post("/")
def generate_prediction_insight(input_data: PredictionInput):
    payload = input_data.model_dump()
    cache_key = cache_service.make_key(payload)

    cached_response = cache_service.get(cache_key)

    if cached_response:
        cached_response["cached"] = True
        return cached_response

    prediction_result = prediction_service.predict(input_data)
    llm_insight = llm_service.generate_insight(input_data, prediction_result)

    estimated_cost = cost_tracker.estimate_mock_cost(
        prompt_tokens=450,
        completion_tokens=300,
    )
    optimised_parameters = optimisation_service.recommend_parameters(
    input_data,
    prediction_service,
)
    

    response = {
        "prediction": prediction_result,
        "insight": llm_insight,
        "estimated_llm_cost": estimated_cost,
        "cached": False,
        "llm_mode": llm_insight.get("provider", "mock"),
        "optimised_parameters": optimised_parameters
    }

    cache_service.set(cache_key, response)

    return response
