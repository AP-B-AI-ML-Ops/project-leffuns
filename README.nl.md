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


> ℹ️**Opmerking**: *Kaggle Antwerpen is uit het project verwijderd wegens gebrek aan gegevens.*

#### Voor windproductie:
- Energie Vlaanderen
- Elia

## 📅Projectuitleg

Dit project beoogt de windenergieproductie voor Antwerpen voor de komende 24 uur te voorspellen. Met de resultaten is het de bedoeling dat je het optimale tijdstip kunt bepalen om apparaten op te laden (energie van het net halen). Soms is er te veel energie op het net, dus wanneer je energie verbruikt op een moment van overvloed, kun je daarvoor betaald krijgen.

Dit alles betekent in feite dat energie op bepaalde tijdstippen ongelooflijk goedkoop, of zelfs winstgevend zal zijn, en dit project is bedoeld om dat tijdstip te vinden (optimaal tijdstip = output).

## 🌊Flows & Acties

Het project maakt gebruik van ML om een output te voorspellen op basis van de datasets. De vereiste acties zijn:
- Het laden van de datasets.
- Een model trainen op de data.
- Het model automatisch laten trainen op automatisch gedownloade data.
- De uitkomsten van elk getraind model bekijken.
- Gebruikmaken van Grafana voor een visuele weergave van de output.
