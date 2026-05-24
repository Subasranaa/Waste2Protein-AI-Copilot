import json
import os
from typing import Dict, Any
from groq import Groq
from app.schemas import PredictionInput
from app.logger import setup_logger

logger = setup_logger(__name__)

class LLMService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "mock")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        logger.info(f"LLMService initialised | provider={self.provider} | model={self.groq_model}")

    def generate_insight(self, input_data: PredictionInput, prediction_result: dict) -> dict:
        if self.provider == "groq" and self.groq_api_key:
            try:
                logger.info("Generating insight via Groq API")
                result = self._generate_with_groq(input_data, prediction_result)
                logger.info("Groq insight generated successfully")
                return result
            except Exception as e:
                # Previously this was silent — now you'll see exactly what failed
                logger.error(f"Groq API failed: {e} | falling back to rule-based response")
                return self._fallback_response(input_data, prediction_result)

        logger.info("Using rule-based fallback | reason: provider not groq or no API key")
        return self._fallback_response(input_data, prediction_result)

    def _generate_with_groq(self, input_data, prediction_result):
        client = Groq(api_key=self.groq_api_key)
        prompt = self._build_prompt(input_data, prediction_result)

        logger.debug(f"Sending prompt to Groq | model={self.groq_model}")

        completion = client.chat.completions.create(
            model=self.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI assistant for microbial protein "
                        "production from agri-food waste streams. "
                        "Use cautious scientific language such as "
                        "'may be suitable', 'could be explored', or "
                        "'requires validation'. "
                        "Do not claim biological suitability as fact unless "
                        "it is directly supported by the input. "
                        "Do not invent laboratory results or scientific evidence. "
                        "Treat all outputs as decision-support suggestions only. "
                        "Return only valid JSON. "
                        "Do not include markdown."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        # Groq gives you real token counts — use them
        usage = completion.usage
        logger.info(f"Groq usage | prompt_tokens={usage.prompt_tokens} | completion_tokens={usage.completion_tokens}")
        

        raw_text = completion.choices[0].message.content
        
        try:
            insight= json.loads(raw_text)
        except json.JSONDecodeError as e:
            insight= self._fallback_response(input_data, prediction_result)
        return {
        "insight": insight,
        "token_usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens
        }
    }

    def _build_prompt(
        self,
        input_data: PredictionInput,
        prediction_result: dict,
    ) -> str:
        return f"""
Given the following agri-food waste stream and protein yield prediction,
generate practical decision-support insights.

Input conditions:
- Waste type: {input_data.waste_type}
- Sugar content: {input_data.sugar_content}
- Nitrogen content: {input_data.nitrogen_content}
- Moisture: {input_data.moisture}
- pH: {input_data.ph}
- Temperature: {input_data.temperature}
- Fermentation time: {input_data.fermentation_time}
- Waste volume kg: {input_data.waste_volume_kg}
- Location: {input_data.location}

ML prediction:
- Predicted protein yield: {prediction_result["predicted_protein_yield"]}
- Uncertainty: {prediction_result["uncertainty"]}
- Confidence level: {prediction_result["confidence_level"]}

Return valid JSON with this exact structure:

{{
  "summary": "short non-technical explanation",

  "microbial_recommendations": [
    {{
      "microbe": "candidate name",
      "type": "yeast/fungi/bacteria/algae",
      "reason": "why this microbe may be suitable",
      "risk": "what should be validated experimentally"
    }}
  ],

  "limiting_factors": [
    "factor 1",
    "factor 2"
  ],

  "recommendations": [
    "recommendation 1",
    "recommendation 2"
  ],

  "r_and_d_roadmap": [
    "step 1",
    "step 2",
    "step 3"
  ],

  "confidence_note": "short note explaining uncertainty"
}}

Do not invent laboratory results.
Treat the prediction as decision-support only.
"""

    def _fallback_response(
        self,
        input_data: PredictionInput,
        prediction_result: dict,
    ) -> Dict[str, Any]:
        predicted_yield = prediction_result["predicted_protein_yield"]
        uncertainty = prediction_result["uncertainty"]

        if predicted_yield >= 55:
            summary = "The predicted protein yield is relatively strong, but experimental validation is required."
        elif predicted_yield >= 35:
            summary = "The predicted protein yield is moderate and could be improved through process optimisation."
        else:
            summary = "The predicted protein yield is low and may require additional optimisation before scale-up."

        limiting_factors = []

        if input_data.ph < 5.5 or input_data.ph > 7.0:
            limiting_factors.append("pH may be outside a suitable fermentation range.")

        if input_data.temperature < 28 or input_data.temperature > 35:
            limiting_factors.append("Temperature may need further optimisation.")

        if input_data.nitrogen_content < 1.5:
            limiting_factors.append("Nitrogen content may limit microbial protein formation.")

        if input_data.sugar_content < 10:
            limiting_factors.append("Sugar content may be insufficient for efficient microbial growth.")

        if not limiting_factors:
            limiting_factors.append("No major limiting factor was detected from the provided inputs.")

        return {
            "summary": summary,
            "microbial_recommendations": [
                {
                    "microbe": "Saccharomyces cerevisiae",
                    "type": "yeast",
                    "reason": (
                        "This candidate could be explored for sugar-rich waste streams, "
                        "but suitability must be validated experimentally."
                    ),
                    "risk": "Performance and safety should be tested on the specific waste stream.",
                }
            ],
            "limiting_factors": limiting_factors,
            "recommendations": [
                "Run small-scale fermentation trials before industrial scaling.",
                "Monitor pH, nitrogen balance, and temperature during fermentation.",
                "Compare yeast, fungal, bacterial, or algal candidates experimentally.",
                "Track yield consistency across repeated batches.",
            ],
            "r_and_d_roadmap": [
                "Validate waste composition experimentally.",
                "Perform bench-scale fermentation.",
                "Optimise environmental and nutrient conditions.",
                "Evaluate microbial candidate performance.",
                "Estimate technical and economic feasibility before scale-up.",
            ],
            "confidence_note": f"Estimated model uncertainty is ±{uncertainty}. Results should be treated as decision-support only.",
        }
