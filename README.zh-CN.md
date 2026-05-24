<div align="center">

# MLOps 项目

<img src=".\public\img\wind-turbine-future-energy.2e16d0ba.fill-933x525-c100.png">

<img src="./public/img/china.png" height="14px"> [简体中文](./README.zh-CN.md) | <img src="./public/img/usa.png" height="13px"> [English](./README.md) | <img src="./public/img/belgium.png" height="14px"> [Nederlands](./README.nl.md)

**一个端到端的机器学习系统，利用天气预报数据作为输入，预测安特卫普地区未来 24 小时的风能产量（单位：兆瓦/MW）。**

如果这个项目对您有帮助或具有教育意义，请点个 Star ⭐️。

</div>

## 📊 数据集

本项目使用了多种与比利时不同时期风能相关的数据集。

#### 风速数据：
- Open Meteo ECMWF
- Geo.be
- Kaggle Uccle

> ℹ️ **注意**：*由于数据缺失，本项目已弃用 Kaggle Antwerp 数据集。*

#### 风能产量数据：
- Energie Vlaanderen
- Elia

## 📅 项目说明

本项目旨在预测安特卫普未来 24 小时的风能产量。根据预测结果，您可以了解为设备/电器充电（从电网取电）的最佳时间。有时电网能量过剩，当您在电力充足时从电网取电，甚至可以获得报酬。

简而言之，这意味着在特定的时间点，电价会非常便宜，甚至是盈利的。本项目的目的就是准确找到那个最佳时间点。

**模型详细信息与特征：**
该系统使用基于历史数据训练的随机森林 (Random Forest) 模型。
* **输入：** 天气预报特征，具体为 `ecmwf_windspeed_10m`（风速）、`hour`（小时）和 `month`（月份）。
* **输出：** 电网的预测风能产量（单位：MW）。

## 🛠️ 架构与技术栈

* **实验跟踪 (Experiment Tracking)：** MLflow
* **工作流编排 (Workflow Orchestration)：** Prefect
* **监控 (Monitoring)：** Evidently & Grafana
* **部署 (Deployment)：** FastAPI（Web 服务）& Prefect 定时任务（批处理服务）
* **容器化 (Containerization)：** Docker Compose

## 🌊 自动化流程与操作

本项目使用机器学习根据数据集预测输出。自动化的流水线操作包括：
* **训练与部署：** 自动加载数据、进行特征工程、训练模型，并通过 MLflow 注册最佳模型。
* **批处理评分：** 定时流水线获取新数据，运行推理，并将预测结果与实际数据进行比较。
* **监控：** Evidently 计算误差指标 (RMSE) 和数据漂移，并在 Grafana 中进行可视化。

## 🗺️ 导航与执行指南（供同行评审参考）

要评估和运行此项目，请克隆仓库并运行：
```bash
docker-compose up --build
```

以下是各项运行中服务的快速概览：

* **`docker-compose.yml`**：编排整个环境。
* **`train-deploy/`**：启动时自动运行训练流水线。
* **`deployment-web-api/`**：按需提供服务的 FastAPI 应用程序，访问地址：`http://localhost:8000/docs`
* **`deployment-batch/`**：定时运行的 Prefect 工作流。Prefect UI 访问地址：`http://localhost:4200`
* **`Monitoring`**：Grafana 仪表板访问地址：`http://localhost:3400`（登录名/密码：`admin` / `admin`）。MLflow 跟踪界面访问地址：`http://localhost:5000`。
  > 💡 **注意**：*由于这是一个时间序列仪表板，监控面板最初只会显示一个数据点。要查看 RMSE 趋势线，请等待预设的 Prefect 批处理流程多次运行，或者通过 Prefect UI 手动触发 `Batch Scoring Flow`。*

要在本地运行 API 单元测试：

```bash
pytest deployment-web-api/
```
