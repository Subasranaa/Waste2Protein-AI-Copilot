from app.schemas import PredictionInput

class PredictionService:
    def __init__(self):
        self.model_version ="baseline-rule-v0.1"

    def predict(self, data: PredictionInput):
        """
        Temporary rule-based baseline.
        Later we will replace this with a trained ML model.
        """

        base_yield = 10.0

        
        sugar_effect = data.sugar_content * 0.8
        nitrogen_effect = data.nitrogen_content * 3.0
        time_effect = min(data.fermentation_time * 0.25, 15)
        temperature_effect = max(0, 10 - abs(data.temperature - 30) * 0.6)
        ph_effect = max(0, 8 - abs(data.ph - 6.0) * 2)

        predicted_yield = (
            base_yield
            + sugar_effect
            + nitrogen_effect
            + time_effect
            + temperature_effect
            + ph_effect
        )

        predicted_yield = round(predicted_yield, 2)

        uncertainty = round(max(2.0, abs(data.temperature - 30) * 0.3 + abs(data.ph - 6.0)),2)

        if uncertainty <= 3:
            confidence = "high"
        elif uncertainty <= 6:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "predicted_protein_yield": predicted_yield,
            "uncertainty" : uncertainty,
            "confidence_level": confidence,
            "model_version": self.model_version,
            }
