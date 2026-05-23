"""
On-demand forecast API.
"""

import os
import time
from typing import List

import mlflow
import pandas as pd
from fastapi import FastAPI
from mlflow.exceptions import RestException
from pydantic import BaseModel

app = FastAPI(title="Energy Forecast API")

mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://experiment-tracking:5000")
)


def load_model_with_retry(uri: str, max_retries: int = 30, wait_seconds: int = 10):
    """Wait for the model artifacts to be fully uploaded before loading."""
    for attempt in range(max_retries):
        try:
            print(
                f"Attempting to load model from {uri} (Attempt {attempt + 1}/{max_retries})..."
            )
            return mlflow.pyfunc.load_model(model_uri=uri)
        except Exception as e:
            print(f"Model artifacts not fully ready yet ({str(e)}). Sleeping...")
            time.sleep(wait_seconds)
    raise TimeoutError("Model failed to load in time.")


model = load_model_with_retry("models:/wind-production-model/1")


class WeatherForecast(BaseModel):
    """Defines the expected input format for each weather forecast."""

    ecmwf_windspeed_10m: float
    hour: int
    month: int


class ForecastRequest(BaseModel):
    """Defines the expected input format for the prediction endpoint."""

    features: List[WeatherForecast]


@app.post("/predict")
def predict(request: ForecastRequest):
    """Takes weather data and returns MW production predictions."""
    df = pd.DataFrame([dict(f) for f in request.features])

    predictions = model.predict(df)

    return {"predictions": predictions.tolist()}
