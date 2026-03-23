import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
sys.path.append(str(Path(__file__).parents[2] / 'src' / 'simulator'))

from services.loader import load_teams, load_drivers, load_circuits # type: ignore
from sim.season import Season  # type: ignore

DATA_DIR = Path(__file__).parents[2] / 'src' / 'simulator' / 'data'

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


teams_by_id = load_teams(DATA_DIR / "teams.json")
teams = list(teams_by_id.values())
drivers = load_drivers(DATA_DIR / "drivers.json", teams_by_id)
circuits = load_circuits(DATA_DIR / "circuits_2025.json")

if "season" not in st.session_state:
    st.session_state.season = Season(drivers, teams, circuits)

if "points_history" not in st.session_state:
    st.session_state.points_history = [] # to track points after each race

drivers_sorted = sorted(st.session_state.season.drivers, key=lambda d: d.points, reverse=True)

st.title('F1 Season Simulator')
if st.session_state.season.current_round > len(st.session_state.season.circuits):
    st.success(f"🏆 {drivers_sorted[0].name} is the 2025 World Champion!")
    st.balloons()

with st.sidebar:
    races_done = st.session_state.season.current_round - 1
    total = len(st.session_state.season.circuits)
    st.write(f"Round {min(races_done, total)} of {total} complete")
 
    if st.button("Simulate Next Race"):
        st.session_state.season.run_next_race()
        circuit_name = st.session_state.season.circuits[st.session_state.season.current_round - 2].name
        snapshot = {'round': circuit_name}
        for t in st.session_state.season.teams:
            snapshot[t.name] = t.points
        st.session_state.points_history.append(snapshot)
        st.rerun()  # to update the sidebar info immediately after sim

    if st.button("Simulate Full Season"):
        while st.session_state.season.current_round <= len(st.session_state.season.circuits):
            st.session_state.season.run_next_race()
            circuit_name = st.session_state.season.circuits[st.session_state.season.current_round - 2].name
            snapshot = {'round': circuit_name}
            for t in st.session_state.season.teams:
                snapshot[t.name] = t.points
            st.session_state.points_history.append(snapshot)
        st.rerun()
            
    if st.button("Reset Season"):
        st.session_state.season = Season(drivers, teams, circuits)
        st.session_state.points_history = []
        st.rerun()

# Display Last Race Results
if st.session_state.season.last_race_results:
    st.subheader(f'Last Race Results - {st.session_state.season.circuits[st.session_state.season.current_round - 2].name}')
    results_data = [
        {"Pos": i, "Driver": d[0].name, "Team": d[0].team.name, "Points": d[0].points}
        for i, d in enumerate(st.session_state.season.last_race_results, start=1)
    ]
    st.dataframe(pd.DataFrame(results_data), hide_index=True)
else:
    st.subheader("Last Race Results")
    st.write("No races run yet.")

col1, col2 = st.columns(2)

# Display WDC Standings
with col1:
    st.subheader("Driver Standings")
    wdc_data = [
        {"Pos": i, "Driver": d.name, "Team": d.team.name, "Points": d.points, "Wins": d.wins}
        for i, d in enumerate(drivers_sorted, start=1)
    ]
    st.dataframe(pd.DataFrame(wdc_data), hide_index=True)

# Display Constructors Standings
with col2:
    st.subheader("Constructor Standings")
    teams_sorted = sorted(st.session_state.season.teams, key=lambda t: t.points, reverse=True)
    constructor_data = [
        {"Pos": i, "Team": t.name, "Points": t.points, "Wins": t.wins}
        for i, t in enumerate(teams_sorted, start=1)
    ]
    st.dataframe(pd.DataFrame(constructor_data), hide_index=True)

st.subheader("Points Progression")
if st.session_state.points_history:
    points_df = pd.DataFrame(st.session_state.points_history)
    points_df.set_index('round', inplace=True)
    fig = px.line(points_df, markers=True, color_discrete_map=TEAM_COLORS)
    fig.update_layout(xaxis_title="Round", yaxis_title="Points")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No points history available yet. Simulate some races to see the progression!")