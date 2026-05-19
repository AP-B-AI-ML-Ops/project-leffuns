"""This module contains the data preprocessing steps for the wind and production data."""

import os
import pickle

import pandas as pd
from prefect import flow, task
from sklearn.feature_extraction import DictVectorizer


def dump_pickle(obj, filename: str):
    """
    Dump an object to a pickle file.
    """
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)


@task(name="Load and Merge Data")
def load_and_merge_data(raw_data_path: str) -> pd.DataFrame:
    """
    Both .csv files have different timestamps that dont match up.
    Out of 90 thousand rows, only 300 match up, and those 300 are NULL.
    This is purely for a pipeline, not for a high accuracy.
    """
    wind_path = os.path.join(raw_data_path, "wind.csv")
    prod_path = os.path.join(raw_data_path, "productie.csv")

    df_wind = pd.read_csv(wind_path, na_values=["NULL", "null", ""])
    df_wind = df_wind.rename(columns={"date": "tijd"})

    df_wind["tijd"] = pd.to_datetime(df_wind["tijd"], utc=True)
    df_wind = df_wind.set_index("tijd").sort_index()

    df_wind_hourly = df_wind.resample("1h").ffill()

    df_prod = pd.read_csv(prod_path, na_values=["NULL", "null", ""])
    df_prod["tijd"] = pd.to_datetime(df_prod["tijd"], utc=True)

    df_prod = df_prod.set_index("tijd").sort_index()
    df_prod_hourly = df_prod.resample("1h").ffill()

    df = pd.merge(
        df_wind_hourly, df_prod_hourly, left_index=True, right_index=True, how="inner"
    )

    df = df.reset_index()

    df = df.fillna(0)

    print(f"--> Final indestructible data shape: {df.shape}")

    return df


@task(name="Clean and Engineer Features")
def preprocess_features(df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """
    Data for this project is really bad, but the point is to create a pipeline,
    if data is cleanly processed then there'll be no data.
    """
    print(f"--> Shape going into feature engineering: {df.shape}")

    df["hour"] = df["tijd"].dt.hour
    df["month"] = df["tijd"].dt.month
    df.set_index("tijd", inplace=True)

    leakage_columns = [
        "vlaanderen zon kwh",
        "vlaanderen wind kwh",
        "elia zon kwh",
        "elia wind kwh",
    ]
    cols_to_drop = [
        col for col in leakage_columns if col != target_col and col in df.columns
    ]
    df = df.drop(columns=cols_to_drop)

    return df


@task(name="Split Data Sequentially")
def split_data(df: pd.DataFrame, train_ratio=0.7, val_ratio=0.15):
    """
    Splits time-series data without shuffling.
    Args:
        df: The cleaned DataFrame with features and target.
        train_ratio: Proportion of data to use for training.
        val_ratio: Proportion of data to use for validation.
    Returns:
    Three DataFrames: train, validation, and test sets.
    """
    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    df_train = df.iloc[:train_end]
    df_val = df.iloc[train_end:val_end]
    df_test = df.iloc[val_end:]

    return df_train, df_val, df_test


@task(name="Apply DictVectorizer")
def vectorize_data(
    df: pd.DataFrame, target_col: str, dv: DictVectorizer, fit_dv: bool = False
):
    """
    Separates target from features and applies DictVectorizer.
    Args:
    df: The DataFrame to vectorize.
    target_col: The name of the target column.
    dv: An instance of DictVectorizer to fit/transform the data.
    fit_dv: Whether to fit the DictVectorizer on this data
      (True for training set, False for val/test).
    Returns:
    A tuple of (features, target, fitted DictVectorizer).
    """
    y = df[target_col].values

    x_df = df.drop(columns=[target_col])

    dicts = x_df.to_dict(orient="records")

    if fit_dv:
        x = dv.fit_transform(dicts)
    else:
        x = dv.transform(dicts)

    return x, y, dv


@flow(name="Data Preparation Flow")
def run_data_prep(raw_data_path: str = "./Data/", dest_path: str = "./models/"):
    """
    Orchestrates the entire preprocessing pipeline.
    Args:
        raw_data_path: Path where the raw CSV files are stored.
        dest_path: Path where the preprocessed data and DictVectorizer will be saved.
    """
    # productie.csv
    target = "vlaanderen wind kwh"

    df_raw = load_and_merge_data(raw_data_path)

    df_clean = preprocess_features(df_raw, target_col=target)

    df_train, df_val, df_test = split_data(df_clean)

    dv = DictVectorizer()
    x_train, y_train, dv = vectorize_data(df_train, target, dv, fit_dv=True)
    x_val, y_val, _ = vectorize_data(df_val, target, dv, fit_dv=False)
    x_test, y_test, _ = vectorize_data(df_test, target, dv, fit_dv=False)

    os.makedirs(dest_path, exist_ok=True)
    dump_pickle(dv, os.path.join(dest_path, "dv.pkl"))
    dump_pickle((x_train, y_train), os.path.join(dest_path, "train.pkl"))
    dump_pickle((x_val, y_val), os.path.join(dest_path, "val.pkl"))
    dump_pickle((x_test, y_test), os.path.join(dest_path, "test.pkl"))

    print(f"Data prepped and saved to {dest_path}")


if __name__ == "__main__":
    run_data_prep("./data/", "./models/")
