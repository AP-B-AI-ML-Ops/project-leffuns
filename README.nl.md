<div align="center">

# MLOps Project

<img src=".\public\img\wind-turbine-future-energy.2e16d0ba.fill-933x525-c100.png">

<img src="./public/img/china.png" height="14px"> [简体中文](./README.zh-CN.md) | <img src="./public/img/usa.png" height="13px"> [English](./README.md) | <img src="./public/img/belgium.png" height="14px"> [Nederlands](./README.nl.md)

**Een end-to-end ML-systeem dat de windenergieproductie (in MW) voor de regio Antwerpen voorspelt voor de komende 24 uur, met weersvoorspellingsgegevens als invoer.**

Als dit project op wat voor manier dan ook nuttig of leerzaam was, laat dan een ster achter ⭐️.

</div>

## 📊Datasets

Dit project maakt gebruik van verschillende datasets die allemaal gerelateerd zijn aan windenergie in België in verschillende periodes.

#### Voor windsnelheid:
- Open Meteo ECMWF
- Geo.be
- Kaggle Uccle


> ℹ️ **Opmerking**: *Kaggle Antwerpen is uit het project verwijderd wegens een gebrek aan gegevens.*

#### Voor windproductie:
- Energie Vlaanderen
- Elia

## 📅Projectuitleg

Dit project beoogt de windenergieproductie voor Antwerpen voor de komende 24 uur te voorspellen. Met de resultaten is het de bedoeling dat je het optimale tijdstip kunt bepalen om apparaten op te laden (energie van het net halen). Soms is er te veel energie op het net, dus wanneer je energie verbruikt op een moment van overvloed, kun je daarvoor betaald krijgen.

Dit alles betekent in feite dat energie op bepaalde tijdstippen ongelooflijk goedkoop, of zelfs winstgevend zal zijn. Dit project is bedoeld om dat exacte tijdstip te vinden (optimaal tijdstip = output).

**Modeldetails & Kenmerken:**
Het systeem maakt gebruik van een Random Forest model dat is getraind op historische gegevens.
* **Inputs:** Weersvoorspellingskenmerken, specifiek `ecmwf_windspeed_10m` (windsnelheid), `hour` (uur), en `month` (maand).
* **Output:** De voorspelde windenergieproductie voor het netwerk (in MW).

## 🛠️ Architectuur & Technologieën

* **Experiment Tracking:** MLflow
* **Workflow Orkestratie:** Prefect
* **Monitoring:** Evidently & Grafana
* **Implementatie:** FastAPI (Web Service) & Prefect Geplande Runs (Batch Service)
* **Containerisatie:** Docker Compose

## 🌊Flows & Acties

Het project maakt gebruik van ML om een output te voorspellen op basis van de datasets. De geautomatiseerde pipeline-acties zijn:
* **Train & Deploy:** Automatisch gegevens laden, features ontwikkelen, modellen trainen en de beste registreren via MLflow.
* **Batch Scoring:** Een geplande pipeline haalt nieuwe gegevens op, voert voorspellingen uit en vergelijkt deze met actuele waarden.
* **Monitoring:** Foutstatistieken (RMSE) en data drift worden berekend door Evidently en gevisualiseerd in Grafana.

## 🗺️ Navigatie & Uitvoeringsgids (Voor Peer Reviewers)

Om dit project te evalueren en uit te voeren, kloon je de repository en voer je het volgende uit:
```bash
docker-compose up --build
```

Hier is een kort overzicht van de actieve diensten:

* **`docker-compose.yml`**: Orkestreert de volledige omgeving.
* **`train-deploy/`**: Voert de trainingspipeline automatisch uit bij het opstarten.
* **`deployment-web-api/`**: On-demand FastAPI-applicatie beschikbaar op `http://localhost:8000/docs`
* **`deployment-batch/`**: Geplande Prefect flow. De Prefect UI is beschikbaar op `http://localhost:4200`
* **`Monitoring`**: Grafana-dashboards zijn beschikbaar op `http://localhost:3400` (Login: `admin` / `admin`). MLflow-tracking is te vinden op `http://localhost:5000`.
  > 💡 **Let op**: *Omdat dit een tijdreeks-dashboard is, zie je in het begin slechts één datapunt. Om de RMSE-trendlijn te zien verschijnen, moet je het geplande Prefect-batchproces meerdere keren laten uitvoeren of de `Batch Scoring Flow` handmatig activeren via de Prefect UI.*

Om de tests manueel te testen:

```bash
pytest deployment-web-api/
```
