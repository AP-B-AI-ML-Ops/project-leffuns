<div align="center">

# MLOps Project

<img src=".\public\img\wind-turbine-future-energy.2e16d0ba.fill-933x525-c100.png">

<img src="./public/img/china.png" height="14px"> [简体中文](./README.zh-CN.md) | <img src="./public/img/usa.png" height="13px"> [English](./README.md) | <img src="./public/img/belgium.png" height="14px"> [Nederlands](./README.nl.md)

**An end-to-end ML system that predicts wind energy production (in MW) for the Antwerp region over the next 24 hours, using weather forecast data as input.**

If this project was helpful or educational in any way, please drop a star ⭐️.

</div>

IF THE CODE DOESNT WORK, USE THIS VERSION INSTEAD:
```
git checkout 3cbad7376aa0efe1d3a76c265fe9056e2b7a0572
```

## 📊 Datasets

This project uses a variety of datasets all related to wind energy in Belgium at differing periods of times.

#### For wind speed:
- Open Meteo ECMWF
- Geo.be
- Kaggle Uccle

> ℹ️ **Note**: *Kaggle Antwerp was dropped from the project due to a lack of data.*

#### For wind production:
- Energie Vlaanderen
- Elia

## 📅 Project Explanation

This project seeks to predict the next 24 hours of wind energy production for Antwerp. With the results, you can figure out the optimal time to charge devices or appliances (take energy off the grid). Sometimes there is an abundance of energy on the grid, so taking energy off during those peaks can actually be profitable! 

This basically means that energy, at certain timestamps, will be incredibly cheap. This project is meant to find that exact optimal time.

**Model Details & Features:**
The system utilizes a Random Forest model trained on historical data. 
* **Inputs:** Weather forecast features specifically `ecmwf_windspeed_10m` (wind speed), `hour`, and `month`.
* **Output:** The predicted wind energy production for the grid (in MW).

## 🛠️ Architecture & Technologies

* **Experiment Tracking:** MLflow
* **Workflow Orchestration:** Prefect
* **Monitoring:** Evidently & Grafana
* **Deployment:** FastAPI (Web Service) & Prefect Scheduled Runs (Batch Service)
* **Containerization:** Docker Compose

## 🌊 Automated Flows & Actions

The project uses ML to predict an output based on the datasets. The automated pipeline actions are:
* **Train & Deploy:** Automatically load data, engineer features, train models, and register the best one via MLflow.
* **Batch Scoring:** A scheduled pipeline fetches new data, runs inferences, and compares predictions to actuals.
* **Monitoring:** Error metrics (RMSE) and data drift are computed by Evidently and visualized in Grafana.

## 📂 Data Prerequisites
To run the project, please ensure a local ./data/ folder exists in the root directory containing the following CSV files:

* ./data/wind.csv (Wind speed data)

* ./data/productie.csv (Energy production data)

Ensure these files are formatted correctly to match the expected input schema for the feature engineering pipeline.

## 🗺️ Navigation & Execution Guide (For Peer Reviewers)

To evaluate and run this project, clone the repository and run:
```bash
docker-compose up --build
```

Here is a quick breakdown of the active services:

* **`docker-compose.yml`**: Orchestrates the entire environment.
* **`train-deploy/`**: Runs the training pipeline automatically on startup.
* **`deployment-web-api/`**: On-demand FastAPI application available at `http://localhost:8000/docs`
* **`deployment-batch/`**: Scheduled Prefect flow. Prefect UI is available at `http://localhost:4200`
* **`Monitoring`**: Grafana dashboards available at `http://localhost:3400` (Login: `admin` / `admin`). 
  > 💡 **Note**: *Since this is a time-series dashboard, the monitoring panel will initially show only a single data point. To see the RMSE trend line materialize, allow the scheduled Prefect batch process to run multiple times, or trigger the `Batch Scoring Flow` manually via the Prefect UI.*

To run the API unit tests locally:

```bash
pytest deployment-web-api/
```
