import os
from app.logger import setup_logger

logger = setup_logger(__name__)

# Groq pricing as of 2026 — llama-3.3-70b-versatile
# Source: https://console.groq.com/settings/billing
GROQ_PRICING = {
    "llama-3.3-70b-versatile": {
        "prompt": 0.00059,       # per 1k tokens
        "completion": 0.00079,   # per 1k tokens
    },
    "default": {
        "prompt": 0.0005,
        "completion": 0.0008,
    }
}

class CostTracker:
    def __init__(self):
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.total_cost = 0.0     # running total for this session
        self.total_calls = 0
        logger.info(f"CostTracker initialised | model={self.model}")

    def calculate_real_cost(
        self,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> dict:
        pricing = GROQ_PRICING.get(self.model, GROQ_PRICING["default"])
        
        prompt_cost = (prompt_tokens / 1000) * pricing["prompt"]
        completion_cost = (completion_tokens / 1000) * pricing["completion"]
        total_cost = prompt_cost + completion_cost
        
        # Track running totals
        self.total_cost += total_cost
        self.total_calls += 1
        
        logger.info(
            f"LLM cost | "
            f"prompt_tokens={prompt_tokens} | "
            f"completion_tokens={completion_tokens} | "
            f"cost=£{total_cost:.6f} | "
            f"session_total=£{self.total_cost:.4f}"
        )
        
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost_gbp": round(total_cost, 6),
            "session_total_gbp": round(self.total_cost, 4),
            "session_calls": self.total_calls,
            "model": self.model,
            "note": "Cost estimate based on Groq published pricing"
        }

    # Keep mock version for when LLM falls back to rule-based
    def estimate_mock_cost(self, prompt_tokens: int, completion_tokens: int) -> dict:
        logger.debug("Using mock cost estimate — no real LLM call was made")
        return {
            "cost_gbp": 0.0,
            "note": "No LLM call made — rule-based fallback used"
        }
