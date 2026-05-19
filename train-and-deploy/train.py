"""
This module trains a Random Forest Regressor and exports it to MLflow.
"""

import os
import pickle

import mlflow
from prefect import task
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error


def load_pickle(filename: str):
    """
    Load from a pickle file.
    """
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@task(name="Train Model")
def run_train(data_path: str):
    """
    Train a Random Forest Model.
    """
    mlflow.set_tracking_uri("http://experiment-tracking:5000")
    mlflow.set_experiment("wind-production-training")

    x_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    x_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    with mlflow.start_run(run_name="baseline_random_forest"):
        model = RandomForestRegressor(max_depth=10, random_state=42)
        model.fit(x_train, y_train)

        y_pred = model.predict(x_val)
        rmse = root_mean_squared_error(y_val, y_pred)

        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(model, artifact_path="model")

        print(f"Baseline Training Completed. RMSE: {rmse}")
