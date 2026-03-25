from pathlib import Path
import streamlit as st
import pandas as pd

FEATURES_DIR = Path(__file__).parents[2] / 'data' / 'features'

CSV_DESCRIPTIONS = {
    "Driver_form.csv": """Per-driver rolling form metrics including average finishing 
                        position, DNF rate, average lap time, and pit stop times over 
                        the last 3 and 5 races.""",
    "Team_form.csv": """Per-team rolling form metrics including average finishing position, 
                        DNF rate, and average lap time over the last 3 and 5 races.""",
    "Race_context.csv": """Combined race context features including each driver's qualifying 
                        delta to pole position, circuit characteristics (track length, 
                        corners, total laps), and session conditions (track temp, air temp, 
                        rainfall. safety car deployments)."""
}

csv_files = list(FEATURES_DIR.glob("*.csv"))

st.title('CSV Data Viewer')
selected_csv = st.selectbox("Select a CSV file to view:", options=[f.name for f in csv_files], key="selected_csv")

if selected_csv:
    df = pd.read_csv(FEATURES_DIR / selected_csv)
    st.write(f"### {selected_csv}")
    st.write("##### Description")
    st.write(CSV_DESCRIPTIONS.get(selected_csv, "No description available for this file."))
    st.dataframe(df)

    
