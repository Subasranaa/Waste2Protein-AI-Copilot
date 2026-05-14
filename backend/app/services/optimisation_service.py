import pandas as pd
from app.schemas import PredictionInput


class OptimisationService:
    def recommend_parameters(self, input_data: PredictionInput, prediction_service):
        candidate_rows = []

        ph_values = [5.5, 5.8, 6.0, 6.2, 6.5, 6.8]
        temperature_values = [28, 30, 32, 34, 36]
        fermentation_times = [36, 48, 60, 72, 84]

        for ph in ph_values:
            for temperature in temperature_values:
                for fermentation_time in fermentation_times:
                    candidate = {
                        "waste_type": input_data.waste_type,
                        "sugar_content": input_data.sugar_content,
                        "nitrogen_content": input_data.nitrogen_content,
                        "moisture": input_data.moisture,
                        "ph": ph,
                        "temperature": temperature,
                        "fermentation_time": fermentation_time,
                        "waste_volume_kg": input_data.waste_volume_kg,
                        "location": input_data.location,
                    }

                    prediction_input = PredictionInput(**candidate)
                    prediction = prediction_service.predict(prediction_input)

                    candidate_rows.append({
                        "ph": ph,
                        "temperature": temperature,
                        "fermentation_time": fermentation_time,
                        "predicted_protein_yield": prediction["predicted_protein_yield"],
                        "uncertainty": prediction["uncertainty"],
                        "confidence_level": prediction["confidence_level"],
                    })

        candidates = pd.DataFrame(candidate_rows)

        best = candidates.sort_values(
            by=["predicted_protein_yield", "uncertainty"],
            ascending=[False, True],
        ).iloc[0]

        top_candidates = (
            candidates.sort_values(
                by=["predicted_protein_yield", "uncertainty"],
                ascending=[False, True],
            )
            .head(5)
            .to_dict(orient="records")
        )

        return {
            "best_parameters": {
                "ph": float(best["ph"]),
                "temperature": float(best["temperature"]),
                "fermentation_time": float(best["fermentation_time"]),
                "predicted_protein_yield": float(best["predicted_protein_yield"]),
                "uncertainty": float(best["uncertainty"]),
                "confidence_level": best["confidence_level"],
            },
            "top_candidate_conditions": top_candidates,
            "method": "model-based grid search using trained protein-yield predictor",
        }
