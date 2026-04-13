import streamlit as st
import base64
import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1] / 'src' / 'simulator'))
sys.path.append(str(Path(__file__).parents[1] / 'src' / 'monte_carlo'))

from services.loader import load_drivers, load_teams

F1_LOGO = Path(__file__).parent / "F1 Team Logos" / "F1 Logo.png"
DATA_DIR = Path(__file__).parent.parent / "src" / "simulator" / "data"
RATINGS_CSV = Path(__file__).parent.parent / "src" / "models" / "data" / "driver_predicted_position.csv"

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

st.set_page_config(layout="wide", page_title="Formula 1 Race Forecasting")

# Section 1 - Formula 1 Logo & App Title 
left_col, cen_col, right_col = st.columns([1, 2, 1])
with cen_col:
    formula1_logo = img_to_base64(F1_LOGO)
    st.markdown(f"<div style='text-align: center; margin-top: -125px;margin-bottom: -125px;'><img src='data:image/png;base64,{formula1_logo}' width='400'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; margin-top: -20px; margin-bottom: -10px;'>Formula 1 Race Forecasting</h1>", unsafe_allow_html=True)
    
# Section 2 - App Description
description = """
                F1 Race Forecasting is a data-driven application for simulating and predicting 
                Formula 1 race and season outcomes. It combines a rule-based race simulator with 
                a machine learning analytics pipeline to generate probabilistic forecasts across 
                the 2025 season. Using Monte Carlo simulation, the app runs thousands of race 
                scenarios to produce win probabilities, podium likelihoods, and championship odds 
                for every driver and constructor. Lap and session data is sourced from FastF1, and 
                predictions are generated using scikit-learn models trained on historical race results.
            """
st.markdown(f'<div style="text-align: center; max-width: 800px; margin: auto;">{description}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<h3 style='text-align: center;'> Explore the App </h3>", unsafe_allow_html=True)

# Section 3 - Navigation Cards
card1, card2, card3 = st.columns(3)

with card1:
    with st.container(border=True):
        st.markdown("### 🏁 Season Simulation")
        st.write("Simulate the entire 2025 F1 season and view driver & constructor standings.")
        
with card2:
    with st.container(border=True):
        st.markdown("###  📊 CSV Data Viewer")
        st.write("Explore the datasets used for model training and feature engineering.")
        
with card3:
    with st.container(border=True):
        st.markdown("### 🎲 Monte Carlo Analysis")
        st.write("Run Monte Carlo simulations to generate probabilistic forecasts for races and championships.")
        
# Section 4 - 2025 Season at a Glance
teams_by_id = load_teams(DATA_DIR / "teams.json")
teams = list(teams_by_id.values())
drivers = load_drivers(DATA_DIR / "drivers.json", RATINGS_CSV, teams_by_id)
circuits = json.load(open(DATA_DIR / "circuits_2025.json"))

st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Season", "2025")
with m2:
    st.metric("Rounds", len(circuits))
with m3:
    st.metric("Drivers", len(drivers))
with m4:
    st.metric("Teams", len(teams))
