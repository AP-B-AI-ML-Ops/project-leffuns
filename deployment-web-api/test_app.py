"""
This module is for unit testing the FastAPI in app.py.
"""

from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_predict_endpoint_success():
    """Test that the API correctly returns a prediction."""
    payload = {"features": [{"ecmwf_windspeed_10m": 15.5, "hour": 12, "month": 5}]}
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert isinstance(data["predictions"], list)
    assert len(data["predictions"]) == 1


def test_predict_endpoint_validation_error():
    """Test that the API rejects bad data (missing 'month')."""
    payload = {"features": [{"ecmwf_windspeed_10m": 15.5, "hour": 12}]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # FastAPI standard validation error code
