import pandas as pd
from src.common.setup_directories import RAW_DIR, PROCESSED_DIR, FEATURES_DIR

def circuit_score():
    circuit_df = pd.read_csv(RAW_DIR / '2025_circuit_info.csv')
    session_df = pd.read_csv(PROCESSED_DIR / 'Race_session_data_cleaned.csv')
    results_df = pd.read_csv(PROCESSED_DIR / 'Race_results_cleaned.csv')

    dnf_per_race = results_df.groupby(['Event', 'Year'])['Status'].apply(lambda x: (x == 'Retired').mean())
    AvgDNFRate = dnf_per_race.groupby(['Event']).mean()
    
    
    
    
    