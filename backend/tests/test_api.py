from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction_endpoint():
    payload = {
        "waste_type": "fruit_waste",
        "sugar_content": 18.5,
        "nitrogen_content": 2.1,
        "moisture": 72,
        "ph": 5.8,
        "temperature": 32,
        "fermentation_time": 48,
        "waste_volume_kg": 100,
        "location": "Leeds"
    }

    response = client.post("/predict/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "predicted_protein_yield" in data
    assert "uncertainty" in data
    assert "confidence_level" in data
    assert data["model_version"] == "random-forest-v1.0"

def test_insights_endpoint():
    payload = {
        "waste_type": "fruit_waste",
        "sugar_content": 18.5,
        "nitrogen_content": 2.1,
        "moisture": 72,
        "ph": 5.8,
        "temperature": 32,
        "fermentation_time": 48,
        "waste_volume_kg": 100,
        "location": "Leeds"
    }

    response = client.post("/insights/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "prediction" in data
    assert "insight" in data
    assert "economic_estimate" in data
    assert "llm_cost" in data
