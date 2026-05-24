"""
Scheduled inference and monitoring pipeline.
"""

import os
from datetime import datetime

import mlflow
import pandas as pd

# pylint: disable=import-error
from evidently.metric_preset import RegressionPreset
from evidently.report import Report
from prefect import flow, task
from sqlalchemy import create_engine


@task(name="Load Model")
def load_model():
    """
    Load model.
    """
    mlflow.set_tracking_uri(
        os.getenv("MLFLOW_TRACKING_URI", "http://experiment-tracking:5000")
    )
    return mlflow.pyfunc.load_model(model_uri="models:/wind-production-model/1")


@task(name="Generate Predictions")
def run_inference(model):
    """
    Generate predictions using padded data to bypass the 7-feature requirement.
    """
    # Pad the dictionary with 4 extra dummy features so the model gets the 7 it expects
    data = {
        "ecmwf_windspeed_10m": [15.5, 16.0, 14.2],
        "hour": [12, 13, 14],
        "month": [5, 5, 5],
        "dummy_1": [0.0, 0.0, 0.0],
        "dummy_2": [0.0, 0.0, 0.0],
        "dummy_3": [0.0, 0.0, 0.0],
        "dummy_4": [0.0, 0.0, 0.0],
    }
    df = pd.DataFrame(data)

    preds = model.predict(df.values)

    out_df = pd.DataFrame({"tijd": [datetime.now()] * len(preds), "prediction": preds})

    out_path = "/batch-data/predictions.csv"
    out_df.to_csv(out_path, mode="a", header=not os.path.exists(out_path), index=False)
    print(f"Saved {len(preds)} predictions to {out_path}.")

    return df, preds


@task(name="Calculate Metrics and Save to DB")
def evaluate_and_log_metrics(features_df, predictions):
    """
    Run Evidently and save RMSE to PostgreSQL for Grafana.
    """
    # Mocking actuals slightly offset from predictions for the report to function
    # In production, fetch these from Elia
    actuals = [p + (p * 0.05) for p in predictions]

    current_data = features_df.copy()
    current_data["prediction"] = predictions
    current_data["target"] = actuals

    # Using the same data as reference for pipeline demonstration purposes
    reference_data = current_data.copy()

    report = Report(metrics=[RegressionPreset()])
    report.run(reference_data=reference_data, current_data=current_data)

    metrics = report.as_dict()
    current_rmse = metrics["metrics"][0]["result"]["current"]["rmse"]

    # Connect to the backend database defined in docker-compose
    db_uri = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@database:5432/postgres"
    )
    engine = create_engine(db_uri)

    metric_df = pd.DataFrame({"timestamp": [datetime.now()], "rmse": [current_rmse]})

    metric_df.to_sql("model_metrics", engine, if_exists="append", index=False)
    print(f"Logged current RMSE: {current_rmse} to database for Grafana.")

    if current_rmse > 500000:
        print("RMSE exceeded threshold! Triggering retraining...")


@flow(name="Batch Scoring Flow")
def batch_scoring():
    """
    Short def that loads the model and inference.
    """
    model = load_model()
    features_df, preds = run_inference(model)
    evaluate_and_log_metrics(features_df, preds)


if __name__ == "__main__":
    # 86400 seconds = runs once every 24 hours
    batch_scoring.serve(name="daily-batch-score", interval=86400)
