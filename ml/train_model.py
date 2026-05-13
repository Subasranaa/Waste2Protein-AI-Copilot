import joblib
import pandas as pd
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DATA_PATH = Path("ml/sample_protein_data.csv")
MODEL_PATH = Path("backend/app/model/protein_model.pkl")


def train_model():
    df = pd.read_csv(DATA_PATH)

    target = "protein_yield"

    feature_cols = [
        "waste_type",
        "sugar_content",
        "nitrogen_content",
        "moisture",
        "ph",
        "temperature",
        "fermentation_time",
        "waste_volume_kg",
        "location",
    ]

    X = df[feature_cols]
    y = df[target]

    categorical_features = ["waste_type", "location"]
    numeric_features = [
        "sugar_content",
        "nitrogen_content",
        "moisture",
        "ph",
        "temperature",
        "fermentation_time",
        "waste_volume_kg",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numeric_features),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print("Model trained successfully")
    print(f"Saved model to: {MODEL_PATH}")
    print(f"MAE: {mae:.3f}")
    print(f"R2: {r2:.3f}")


if __name__ == "__main__":
    train_model()
