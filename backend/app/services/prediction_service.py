from pathlib import Path

import joblib
import pandas as pd

from app.schemas import PredictionInput


class PredictionService:
    def __init__(self):
        self.model_version = "random-forest-v1.0"
        self.model_path = Path(__file__).resolve().parents[1] / "model" / "protein_model.pkl"
        self.model = self._load_model()

    def _load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. "
                "Please run: python ml/train_model.py"
            )

        return joblib.load(self.model_path)

    def predict(self, data: PredictionInput):
        input_df = pd.DataFrame(
            [
                {
                    "waste_type": data.waste_type,
                    "sugar_content": data.sugar_content,
                    "nitrogen_content": data.nitrogen_content,
                    "moisture": data.moisture,
                    "ph": data.ph,
                    "temperature": data.temperature,
                    "fermentation_time": data.fermentation_time,
                    "waste_volume_kg": data.waste_volume_kg,
                    "location": data.location,
                }
            ]
        )

        prediction = float(self.model.predict(input_df)[0])

        uncertainty = self._estimate_uncertainty(input_df)

        confidence = self._confidence_from_uncertainty(uncertainty)

        return {
            "predicted_protein_yield": round(prediction, 2),
            "uncertainty": round(uncertainty, 2),
            "confidence_level": confidence,
            "model_version": self.model_version,
        }

    def _estimate_uncertainty(self, input_df: pd.DataFrame) -> float:
        """
        Random Forest uncertainty approximation:
        calculate standard deviation across individual tree predictions.
        """

        preprocessor = self.model.named_steps["preprocessor"]
        rf_model = self.model.named_steps["model"]

        transformed_input = preprocessor.transform(input_df)

        tree_predictions = [
            tree.predict(transformed_input)[0]
            for tree in rf_model.estimators_
        ]

        return float(pd.Series(tree_predictions).std())

    def _confidence_from_uncertainty(self, uncertainty: float) -> str:
        if uncertainty <= 3:
            return "high"
        if uncertainty <= 6:
            return "medium"
        return "low"
