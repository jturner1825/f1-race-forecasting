from pathlib import Path
import sys
import streamlit as st
import pandas as pd
import base64
import plotly.express as px

sys.path.append(str(Path(__file__).parents[2] / 'src' / 'simulator'))
sys.path.append(str(Path(__file__).parents[2] / 'src' / 'monte_carlo'))

from services.loader import load_drivers, load_teams
from src.monte_carlo.aggregator import run_aggregations

DATA_DIR = Path(__file__).parents[2] / 'src' / 'simulator' / 'data'
RATINGS_CSV = Path(__file__).parents[2] / "src" / "models" / "data" / "driver_predicted_position.csv"

LOGO_DIR = Path(__file__).parents[1] / "F1 Team Logos"
TEAM_LOGOS = {
    "Red Bull": LOGO_DIR / "Red Bull.png",
    "McLaren": LOGO_DIR / "McLaren.png",
    "Mercedes": LOGO_DIR / "Mercedes.png",
    "Ferrari": LOGO_DIR / "Ferrari.png",
    "Alpine": LOGO_DIR / "Alpine.png",
    "Aston Martin": LOGO_DIR / "Aston Martin.png",
    "Williams": LOGO_DIR / "Williams.png",
    "Haas": LOGO_DIR / "Haas.png",
    "Kick Sauber": LOGO_DIR / "Stake.png",
    "Racing Bulls": LOGO_DIR / "Racing Bulls.png",
}

TEAM_COLORS = {
    "Mercedes": "#00D7B6",
    "Red Bull": "#4781D7",
    "Ferrari": "#ED1131",
    "McLaren": "#F47600",
    "Alpine": "#00A1E8",
    "Racing Bulls": "#6C98FF",
    "Aston Martin": "#229971",
    "Williams": "#1868DB",
    "Kick Sauber": "#01C00E",
    "Haas": "#9C9FA2",
}

F1_LOGO = LOGO_DIR / "F1_Logo.png"

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

teams_by_id = load_teams(DATA_DIR / "teams.json")
teams = list(teams_by_id.values())
drivers = load_drivers(DATA_DIR / "drivers.json", RATINGS_CSV, teams_by_id)

# Streamlit App
st.set_page_config(page_title="Formula 1 Monte Carlo Analysis", page_icon=str(F1_LOGO))
st.title("Formula 1 Monte Carlo Analysis")

# Sidebar for simulation controls
with st.sidebar:    
    selected_driver = st.selectbox('Selected Driver', options=[driver.name for driver in drivers], key="selected_driver")
    N = st.slider("Number of Simulations", 100, 10000, 1000, key="sim_slider")
    if st.button("Run Monte Carlo Simulation"):
        st.session_state['results'] = run_aggregations(drivers, teams, N)
        st.session_state['N'] = N
        st.success("Simulations complete!")
        
# Create top level tabs for different analyses
col1, col2, col3, col4 = st.columns(4)
driver_to_team = {d.name: d.team.name for d in drivers}

team_name = driver_to_team[selected_driver]
logo_path = TEAM_LOGOS[team_name]

with col1:
    with st.container(border=True, height=100):
        logo_b64 = img_to_base64(logo_path)
        st.markdown(f"""
            <p style='margin:0'><b>Selected Driver</b></p>
            <div style='display:flex; align-items:center; gap:8px; margin-top:4px'>
                <div style='background-color:white; border-radius:4px; padding:2px'>
                    <img src='data:image/png;base64,{logo_b64}' width='30'/>
                </div>
                <p style='margin:0; font-size:1.5em'>{selected_driver}</p>
            </div>
        """, unsafe_allow_html=True)


            
with col2:
    if 'results' in st.session_state:
        race_df = st.session_state['results']['race']
        row = race_df[race_df['Driver'] == selected_driver]
        win_pct = row['Win %'].values[0]
        
        with st.container(border=True, height=100):
            st.markdown(f"<p style='margin:0'><b>Win Probability</b></p><p style='margin:0; font-size:1.4em'>{win_pct}</p>", unsafe_allow_html=True)
    else:
        st.info("Run the simulation to see results.")
    
with col3:
    if 'results' in st.session_state:
        race_df = st.session_state['results']['race']
        row = race_df[race_df['Driver'] == selected_driver]
        podium_pct = row['Podium %'].values[0]

        with st.container(border=True, height=100):
            st.markdown(f"<p style='margin:0'><b>Podium Probability</b></p><p style='margin:0; font-size:1.4em'>{podium_pct}</p>", unsafe_allow_html=True)
    else:
        st.info("Run the simulation to see results.")
    
with col4:
    if 'results' in st.session_state:
        season_df = st.session_state['results']['season']
        row = season_df[season_df['Driver'] == selected_driver]
        champ_pct = season_df.set_index('Driver')['Championship %'].get(selected_driver, 0)
        if isinstance(champ_pct, str):
            champ_pct = champ_pct
        elif pd.isna(champ_pct):
            champ_pct = "0%"
        else:
            champ_pct = f"{champ_pct:.0%}"
        
        with st.container(border=True, height=100):
            st.markdown(f"<p style='margin:0'><b>Championship Probability</b></p><p style='margin:0; font-size:1.4em'>{champ_pct}</p>", unsafe_allow_html=True)
    else:
        st.info("Run the simulation to see results.")

if 'results' in st.session_state:      
    # Display race outcome distribution graph
    pos_df = st.session_state['results']['position_dist'].set_index('Driver').T

    # Filter top 5 positions for better visualization
    top_positions = race_df['Driver'].head(5).tolist()
    pos_df = pos_df[top_positions]
    
    # Create frequency columns instead of probability for better visualization
    pos_df = pos_df * st.session_state['N']

    # Create stacked bar chart w/ Plotly
    fig = px.bar(pos_df, x=pos_df.index, y=pos_df.columns.tolist(), barmode='stack', title="Monte Carlo Simulation - Race Outcome Distribution", labels={'value': 'Frequency', 'index': 'Position'}, color_discrete_map=TEAM_COLORS)
    fig.update_xaxes(title="Finishing Position", tickmode='linear', tick0=1, dtick=1)
    
    chart_col, champ_col = st.columns([2,1])
    with chart_col:
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)
    with champ_col:
        with st.container(border=True, height=300):
            st.markdown('**Championship Probabilities**')
            for _, row in season_df.head(5).iterrows():
                # get team logo for driver
                driver = row['Driver']
                team = driver_to_team.get(driver, "Unknown")
                logo_path = TEAM_LOGOS.get(team, "")
                logo_b64 = img_to_base64(logo_path) if logo_path else ""
                pct_value = float(row['Championship %'].strip('%'))
                st.markdown(f"""
                    <div style='display:flex; align-items:center; gap:8px; margin-bottom:4px'>
                        <div style='background-color:white; border-radius:4px; padding:2px'>
                            <img src='data:image/png;base64,{logo_b64}' width='20'/>
                        </div>
                        <p style='margin:0; font-size:1.2em'><b>{driver}</b>: {row['Championship %']}</p>
                    </div>
                    <div style='height:3px; width:{pct_value}%; background-color:#e10600; border-radius:2px; margin-bottom:10px'></div>
                """, unsafe_allow_html=True)
else:
    st.info("Run the Monte Carlo simulation to see the race outcome distribution.")

with st.container(border=True):
    st.markdown("**Raw Race Outcome Probabilities**")
    st.dataframe(race_df, use_container_width=True, hide_index=True)
