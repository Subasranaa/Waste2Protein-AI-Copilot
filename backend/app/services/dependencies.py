# backend/app/services/dependencies.py
from app.services.prediction_service import PredictionService
from app.services.llm_service import LLMService
from app.services.cost_tracker import CostTracker
from app.services.cache_service import CacheService
from app.services.economics_service import EconomicsService
from app.logger import setup_logger

logger = setup_logger(__name__)

logger.info("Initialising shared services...")

prediction_service = PredictionService()
llm_service = LLMService()
cost_tracker = CostTracker()
cache_service = CacheService()
economics_service = EconomicsService()

logger.info("All shared services ready")
