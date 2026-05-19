"""
This module is responsible for evaluating the top N models from the HPO experiment,
selecting the best one based on test RMSE,
and registering it in the MLflow Model Registry.
It connects to the MLflow Tracking Server to fetch the HPO runs,
retrains each candidate model on the training data, evaluates it on the test set,
and logs the best model to a dedicated registry experiment.
"""

import os
import pickle

import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from prefect import task
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error


def load_pickle(filename: str):
    """
    Load from a pickle file.
    """
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@task(name="Evaluate and Register Best Model")
def run_register_model(data_path: str, top_n: int):
    """
    Fetches the top N HPO runs, evaluates them on the test set, and registers the best model.
    Args:
        data_path: Path where the preprocessed data and DictVectorizer are stored.
        top_n: Number of top HPO runs to evaluate.
    """
    client = MlflowClient("http://experiment-tracking:5000")
    mlflow.set_tracking_uri("http://experiment-tracking:5000")

    mlflow.set_experiment("wind-production-registry")

    x_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    x_test, y_test = load_pickle(os.path.join(data_path, "test.pkl"))

    hpo_experiment = client.get_experiment_by_name("wind-production-hpo")
    runs = client.search_runs(
        experiment_ids=hpo_experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.rmse ASC"],
    )

    best_rmse = float("inf")
    best_model = None

    for run in runs:
        params = run.data.params

        parsed_params = {
            "max_depth": int(float(params["max_depth"])),
            "n_estimators": int(float(params["n_estimators"])),
            "min_samples_split": int(float(params["min_samples_split"])),
            "min_samples_leaf": int(float(params["min_samples_leaf"])),
        }

        model = RandomForestRegressor(**parsed_params, random_state=42)
        model.fit(x_train, y_train)

        y_pred = model.predict(x_test)
        test_rmse = root_mean_squared_error(y_test, y_pred)

        if test_rmse < best_rmse:
            best_rmse = test_rmse
            best_model = model

    with mlflow.start_run(run_name="best_model_registration"):
        mlflow.log_metric("test_rmse", best_rmse)

        mlflow.sklearn.log_model(
            sk_model=best_model,
            artifact_path="model",
            registered_model_name="wind-production-model",
        )
        print(f"Successfully registered model with Test RMSE: {best_rmse}")
