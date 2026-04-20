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
- Streamlit
- Monte Carlo simulation  

Planned future additions:

- Oracle Database integration  
- XGBoost / Gradient Boosting models

---

# Project Architecture

The repository is organized as a modular analytics pipeline.

```
f1-race-forecasting/
│
├── data/
│   ├── cache/
│   ├── raw/
│   ├── processed/
│   └── features/
│
├── notebooks/
│   ├── finish_position_regressor.ipynb
│   └── team_consistency_regressor.ipynb
│
├── src/
│   ├── common/
│   ├── features/
│   ├── ingest/
│   ├── models/
│   ├── monte_carlo/
│   ├── processing/
│   └── simulatator/
│
├── main.py
└── requirements.txt
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

Ingestion scripts:

```
src/ingest/fetch_schedule.py
src/ingest/fetch_session_data.py
src/ingest/fetch_laps.py
src/ingest/fetch_results.py
src/ingest/fetch_circuit_info.py
```

---

# Feature Engineering

The model uses engineered features that describe driver and team performance.

Features include:

### Driver Form

- Average finishing position over the last N races  
- DNF rate  
- Average lap time over the last N races
- Average pit time over the last N races

### Team Performance

- Average team finishing position over the last N races
- Team DNF rate
- Average team pit time over the last N races


### Race Context

- Grid position  
- Qualifying delta to pole  
- Circuit information
- Weather conditions (when available)  

Feature construction scripts are located in:

```
src/features/
```

---

# Machine Learning Models

Initial models are implemented using **scikit-learn**.

Two models, both Random Forest Regressors trainer on 2023-2024 data, tested on 2025:


### 1. Finish Position Regressor
(finish_position_regressor.ipynb)

* Target: driver finishing position (1-20)
* Features: driver form metrics + race context (21 features)
* Results: MAE 2.93, RMSE 3.96, R² 0.51
* Saved as: finish_position_model.pkl

### 2. Team Consistency Regressor
(team_consistency_regressor.ipynb)

* Target: AvgTeamFinishLast5 (team's rolling 5-race avg finishing position)
* Features: team performance metrics + circuit/session conditions (11 features)
* Results: MAE 1.25, RMSE 1.59, R² 0.84
* Saved as: team_consistency_model.pkl

## Inference (src/models/predict_race.py) combines both:

* Driver prediction weighted at 70%, team prediction at 30%
* Outputs a **rating** per driver, averaged across all rounds -> driver_predicted_position.csv

Model scripts:

```
notebooks/finish_position_regressor.ipynb
notebooks/team_consisteny_regressor.ipynb

predict_race.py
```

---

# Race Simulation

Predictions from the ML models are used to drive a **Monte Carlo race simulation engine**.

Each race is simulated thousands of times to estimate outcome probabilities.

Simulation factors include:

- Model-predicted driver performance 
- Random race variability  
- Reliability / DNF probability  
- Race incident simulation (Red Flag, Safety Car, VSC)  

Example simulation outputs:

- Win probability  
- Podium probability  
- Points probability  
- Average finishing position
- Position distribution across all simulations
- Driver championship probability
- Constructor championship probability
- Team DNF rates

Simulation modules:

```
src/monte_carlo/race_sim.py
src/monte_carlo/season_sim.py
src/monte_carlo/aggregator.py
```

---

# Season Simulation

The simulator can extend race forecasts into **full-season projections**.

For each simulation run, all 24 rounds of the season are simulated sequentially. Points are accumulated per driver across every race, and the driver/constructor with the most points at the end is recorded as the champion. This is repeated N times to estimate championship probabilities.
 

Outputs include:

- Driver Championship probability  
- Constructor Championship probability  

---

# Example Outputs

Example race prediction output:

| Driver | Win % | Podium % | Points % | Avg_Position |
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

---

# Installation

Clone the repository:

```
git clone https://github.com/jturner1825/f1-race-forecasting.git
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
├── features/
└── processed/

src/
│
├── ingest/        # FastF1 data ingestion
├── processing/    # Data cleaning
├── features/      # Feature engineering
├── models/        # ML training & prediction
├── simulation/    # Race and season simulation
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
