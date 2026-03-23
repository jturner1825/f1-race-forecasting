# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Simulator

The simulator must be run from the `src/simulator/` directory due to relative imports:

```bash
cd src/simulator
python main.py
```

The entry point presents an interactive CLI menu to run races, view standings, and simulate full seasons.

## Installing Dependencies

```bash
pip install -r requirements.txt
```

## Running Ingest Scripts

FastF1 ingest scripts run from the repo root. The cache is hardcoded to `data/cache/`:

```bash
python src/ingest/fetch_schedule.py
```

## Architecture

The project has two distinct parts at different stages of development:

### 1. Rule-Based Simulator (`src/simulator/`) — Implemented

A self-contained season simulator with a CLI. Data is loaded from static JSON files (`src/simulator/data/`).

- **`main.py`** — CLI entry point; loads data and drives the `Season` loop
- **`models/`** — Plain Python classes: `Driver` (rating, points, wins), `Team` (points, wins, drivers list), `Circuit` (round, laps, difficulty)
- **`services/loader.py`** — Reads `drivers.json`, `teams.json`, `circuits_2025.json` into model instances
- **`services/race_scorer.py`** — Applies F1 points (25/18/15/...) to race results; updates driver and team totals
- **`sim/race.py`** — Simulates a single race: `performance = driver.rating + random noise`, sort descending
- **`sim/season.py`** — Manages round progression, delegates to `Race` + `RaceScorer`, exposes standings formatters

### 2. ML Analytics Pipeline (`src/`) — Planned / In Progress

Modular pipeline following: FastF1 ingest → feature engineering → ML training → Monte Carlo simulation.

- **`src/ingest/`** — FastF1 data fetching scripts (fetch_schedule, fetch_session_data, fetch_laps, fetch_results)
- **`src/processing/`** — Data cleaning and normalization
- **`src/features/`** — Feature engineering (driver form, team performance, circuit context)
- **`src/models/`** — scikit-learn model training and prediction
- **`src/simulation/`** — Monte Carlo race/season simulation driven by ML predictions
- **`src/data_access/`** — Data loading abstraction (planned Oracle DB support)
- **`src/common/`** — Shared utilities

Raw FastF1 data is cached locally in `data/raw/`; processed outputs go to `data/processed/`. The FastF1 cache directory is `data/cache/`.
