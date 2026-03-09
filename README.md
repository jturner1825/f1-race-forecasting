# F1 Race Forecasting

A Formula 1 analytics and prediction platform that combines **FastF1 data ingestion**, **machine learning**, and **Monte Carlo race simulation** to forecast race outcomes and championship standings.

This project builds a full analytics pipeline for motorsport data, including:

- Historical data ingestion from the FastF1 API  
- Feature engineering for driver and team performance  
- Machine learning models for predicting race outcomes  
- Monte Carlo simulations to estimate race and season probabilities  

The system uses historical race data to generate **probabilistic forecasts** for:

- Race winners  
- Podium finishes  
- Points finishes  
- Expected finishing position  
- Championship standings over a full season  

---

# Project Goals

The goal of this project is to demonstrate a **complete sports analytics workflow**, including:

- Data ingestion and preprocessing  
- Feature engineering  
- Predictive modeling  
- Simulation-based forecasting  
- Structured project architecture suitable for production systems  

This repository is designed to be extensible and will later support **database-backed storage (Oracle)** for scalable data pipelines.

---

# Tech Stack

- Python  
- FastF1 API  
- pandas  
- numpy  
- scikit-learn  
- matplotlib / seaborn  
- Monte Carlo simulation  

Planned future additions:

- Oracle Database integration  
- XGBoost / Gradient Boosting models  
- Visualization dashboards  

---

# Project Architecture

The repository is organized as a modular analytics pipeline.

```
f1-race-forecasting/
│
├── data/
│   ├── raw/
│   ├── processed/
│
│
├── src/
│   ├── ingest/
│   ├── processing/
│   ├── features/
│   ├── models/
│   ├── simulation/
│   ├── data_access/
│   └── common/
```

Each module handles a specific part of the pipeline.

---

# Data Pipeline

The analytics workflow follows this pipeline:

```
FastF1 API
     ↓
Data ingestion scripts
     ↓
Raw data storage
     ↓
Data cleaning & normalization
     ↓
Feature engineering
     ↓
Machine learning model training
     ↓
Race prediction
     ↓
Monte Carlo race simulation
     ↓
Season championship forecasting
```

---

# Data Ingestion

Historical Formula 1 data is collected using the **FastF1 API**.

Data sources include:

- Race results  
- Qualifying results  
- Lap times  
- Sector times  
- Tire stints  
- Session metadata  

Raw data is stored locally in the `data/raw/` directory for reproducibility.

Example ingestion scripts:

```
src/ingest/fetch_schedule.py
src/ingest/fetch_session_data.py
src/ingest/fetch_laps.py
src/ingest/fetch_results.py
```

---

# Feature Engineering

The model uses engineered features that describe driver and team performance.

Example features include:

### Driver Form

- Average finishing position over the last N races  
- Points scored in recent races  
- DNF rate  
- Teammate comparison metrics  

### Team Performance

- Constructor average points over recent races  
- Reliability metrics  
- Qualifying performance trends  

### Race Context

- Grid position  
- Qualifying delta to pole  
- Circuit characteristics  
- Weather conditions (when available)  

Feature construction scripts are located in:

```
src/features/
```

---

# Machine Learning Models

Initial models are implemented using **scikit-learn**.

Example prediction targets:

### Points Finish Classification

Predict whether a driver finishes **inside the points (top 10)**.

```
target = 1 if finish_position <= 10 else 0
```

### Finish Position Regression

Predict expected finishing position.

### DNF Probability

Estimate probability of retirement.

Models are trained using historical race data and evaluated using chronological train/test splits.

Training scripts:

```
src/models/train_points_classifier.py
src/models/train_finish_regressor.py
```

---

# Race Simulation

Predictions from the ML models are used to drive a **Monte Carlo race simulation engine**.

Each race is simulated thousands of times to estimate outcome probabilities.

Simulation factors include:

- Model-predicted driver performance  
- Grid position advantage  
- Random race variability  
- Reliability / DNF probability  
- Team performance adjustments  

Example simulation outputs:

- Win probability  
- Podium probability  
- Points probability  
- Expected finishing order  

Simulation modules:

```
src/simulation/
```

---

# Season Simulation

The simulator can extend race forecasts into **full-season projections**.

For each race weekend:

1. Generate race predictions  
2. Simulate the race thousands of times  
3. Update driver and constructor standings  
4. Estimate championship probabilities  

Outputs include:

- Driver Championship odds  
- Constructor Championship odds  
- Projected season points totals  

---

# Example Outputs

Example race prediction output:

| Driver | Win % | Podium % | Points % | Avg Finish |
|------|------|------|------|------|
| Verstappen | 45% | 82% | 97% | 2.1 |
| Leclerc | 22% | 61% | 93% | 3.8 |
| Norris | 10% | 39% | 78% | 5.7 |

Example championship forecast:

| Driver | Championship Probability |
|------|------|
| Verstappen | 63% |
| Leclerc | 18% |
| Norris | 9% |

---

# Future Improvements

Planned improvements include:

### Database Integration

Support for **Oracle Database** storage and feature queries.

```
FastF1 → Oracle DB → ML pipeline
```

### Advanced Models

Potential additions:

- XGBoost  
- Gradient boosting  
- Neural networks  

### Telemetry Features

Integration of additional features from telemetry data:

- sector performance  
- long-run pace  
- tire degradation  

### Visualization

Possible additions:

- race prediction dashboards  
- championship probability charts  
- driver/team performance visualizations  

---

# Installation

Clone the repository:

```
git clone https://github.com/yourusername/f1-race-forecasting.git
cd f1-race-forecasting
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Running the Pipeline

Example workflow:

### 1. Collect FastF1 data

```
python src/ingest/fetch_session_data.py
```

### 2. Build features

```
python src/features/build_race_features.py
```

### 3. Train models

```
python src/models/train_points_classifier.py
```

### 4. Predict race outcomes

```
python src/models/predict_race.py
```

### 5. Run race simulation

```
python src/simulation/race_simulator.py
```

---

# Repository Structure

```
data/
|
├── raw/
└── processed/

src/
│
├── ingest/        # FastF1 data ingestion
├── processing/    # Data cleaning
├── features/      # Feature engineering
├── models/        # ML training & prediction
├── simulation/    # Race and season simulation
├── data_access/   # Data loading abstraction layer
└── common/        # Shared utilities
```

---

# License

This project is provided for educational and research purposes.

---

# Acknowledgements

- FastF1 library for providing accessible Formula 1 timing data  
- Formula 1 official data sources  
- Open-source Python data science ecosystem  
