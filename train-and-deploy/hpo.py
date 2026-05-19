"""
This module defines a Prefect task for performing hyperparameter optimization (HPO)
on a Random Forest Regressor using the Hyperopt library.
The task loads training and validation data,
defines an objective function for optimization,
and runs the HPO process while logging results to MLflow.
"""

import os
import pickle

import mlflow
import numpy as np
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll import scope
from prefect import task
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error


def load_pickle(filename: str):
    """
    Load from a pickle file.
    """
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@task(name="Hyperparameter Optimization")
def run_optimization(data_path: str, num_trials: int):
    """
    Runs hyperparameter optimization using Hyperopt and logs results to MLflow.
    Args:
        data_path: Path where the preprocessed training and validation data are stored.
        num_trials: Number of HPO trials to run.
    """
    mlflow.set_tracking_uri("http://experiment-tracking:5000")
    mlflow.set_experiment("wind-production-hpo")

    x_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    x_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    def objective(params):
        with mlflow.start_run(nested=True):
            mlflow.log_params(params)

            rf = RandomForestRegressor(**params, random_state=42)
            rf.fit(x_train, y_train)

            y_pred = rf.predict(x_val)
            rmse = root_mean_squared_error(y_val, y_pred)

            mlflow.log_metric("rmse", rmse)
            return {"loss": rmse, "status": STATUS_OK}

    search_space = {
        "max_depth": scope.int(hp.quniform("max_depth", 5, 50, 1)),
        "n_estimators": scope.int(hp.quniform("n_estimators", 10, 200, 10)),
        "min_samples_split": scope.int(hp.quniform("min_samples_split", 2, 10, 1)),
        "min_samples_leaf": scope.int(hp.quniform("min_samples_leaf", 1, 4, 1)),
    }

    rstate = np.random.default_rng(42)
    fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=num_trials,
        trials=Trials(),
        rstate=rstate,
    )
    print(f"Completed {num_trials} HPO trials.")
