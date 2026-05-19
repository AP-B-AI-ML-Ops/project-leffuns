"""
This is the main script, from here it calls the other modules as a central command.
It orchestrates the entire pipeline:
1. Data preparation
2. Model training
3. Hyperparameter optimization
4. Model evaluation and registration
"""

from hpo import run_optimization
from prefect import flow
from preprocess import run_data_prep
from register import run_register_model
from train import run_train


@flow
def training_flow():
    """
    Calls the other modules in sequence.
    """
    run_data_prep("./data/", "./models/")
    run_train("./models/")
    run_optimization("./models/", 5)
    run_register_model("./models/", 5)


if __name__ == "__main__":
    training_flow()
