from pathlib import Path
import joblib
import pandas as pd
from app.schemas import PredictionInput
from app.logger import setup_logger
from app.database import SessionLocal, PredictionRecord, create_tables

logger = setup_logger(__name__)  # __name__ = "app.services.prediction_service"

class PredictionService:
    def __init__(self):
        self.model_version = "random-forest-v1.0"
        self.model_path = Path(__file__).resolve().parents[1] / "model" / "protein_model.pkl"
        self.model = None #start as none
        self.model_load_error = None #track any error


        logger.info(f"Initialising PredictionService | model_path={self.model_path}")

        try:
            self.model = self._load_model()
        except Exception as e:
            self.model_load_error = str(e)
            logger.error(f"Model failed to load: {e}")
        # Create database tables on startup if they don't exist
        create_tables()
            
    def _load_model(self):
        if not self.model_path.exists():
            logger.error(f"Model file not found at {self.model_path}")
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. "
                "Please run: python ml/train_model.py"
            )
        model = joblib.load(self.model_path)
        logger.info(f"Model loaded successfully | version={self.model_version}")

        return model

    def predict(self, data: PredictionInput):
        logger.info(
            f"Prediction requested | "
            f"waste_type={data.waste_type} | "
            f"volume={data.waste_volume_kg}kg | "
            f"location={data.location}"
        )
        try:
            input_df = pd.DataFrame([{
                    "waste_type": data.waste_type,
                    "sugar_content": data.sugar_content,
                    "nitrogen_content": data.nitrogen_content,
                    "moisture": data.moisture,
                    "ph": data.ph,
                    "temperature": data.temperature,
                    "fermentation_time": data.fermentation_time,
                    "waste_volume_kg": data.waste_volume_kg,
                    "location": data.location,
                }])

            prediction = float(self.model.predict(input_df)[0])

            uncertainty = self._estimate_uncertainty(input_df)

            confidence = self._confidence_from_uncertainty(uncertainty)

            result = {
                    "predicted_protein_yield": round(prediction, 2),
                    "uncertainty": round(uncertainty, 2),
                    "confidence_level": confidence,
                    "model_version": self.model_version,
                }
            logger.info(
                    f"Prediction complete | "
                    f"yield={result['predicted_protein_yield']} | "
                    f"confidence={result['confidence_level']} | "
                    f"uncertainty={result['uncertainty']}"
                )
            self._save_to_db(data, result)

            return result
        
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise  # re-raise so FastAPI returns a proper 500 error

    def _save_to_db(self, data: PredictionInput, result: dict):
        if not SessionLocal:
            logger.debug("No database configured — skipping save")
            return
        try:
            db = SessionLocal()
            record = PredictionRecord(
                waste_type=data.waste_type,
                sugar_content=data.sugar_content,
                nitrogen_content=data.nitrogen_content,
                moisture=data.moisture,
                ph=data.ph,
                temperature=data.temperature,
                fermentation_time=data.fermentation_time,
                waste_volume_kg=data.waste_volume_kg,
                location=data.location,
                predicted_protein_yield=result["predicted_protein_yield"],
                uncertainty=result["uncertainty"],
                confidence_level=result["confidence_level"],
                model_version=result["model_version"],
            )
            db.add(record)
            db.commit()
            logger.info(f"Prediction saved to database | id={record.id}")
            db.close()
        except Exception as e:
            logger.error(f"Database save failed (non-critical): {e}")
            # Never crash the prediction over a DB failure

            

    def _estimate_uncertainty(self, input_df: pd.DataFrame) -> float:
       
        preprocessor = self.model.named_steps["preprocessor"]
        rf_model = self.model.named_steps["model"]

        transformed_input = preprocessor.transform(input_df)

        tree_predictions = [
            tree.predict(transformed_input)[0]
            for tree in rf_model.estimators_
        ]
        uncertainty = float(pd.Series(tree_predictions).std())

        logger.debug(f"Uncertainty estimated across {len(rf_model.estimators_)} trees | std={uncertainty:.3f}")
        return uncertainty

    def _confidence_from_uncertainty(self, uncertainty: float) -> str:
        if uncertainty <= 3:
            return "high"
        if uncertainty <= 6:
            return "medium"
        return "low"
    
    def get_status(self) -> dict:
        return {
            "loaded": self.model is not None,
            "version": self.model_version if self.model else None,
            "error": self.model_load_error
        }
