import pandas as pd
from src.common.setup_directories import PROCESSED_DIR, FEATURES_DIR

def build_features():
    driver_form_df = pd.read_csv(FEATURES_DIR / 'Driver_form.csv').drop(columns=['Position', 'GridPosition'])
    team_form_df = pd.read_csv(FEATURES_DIR / 'Team_form.csv').drop(columns=['Position', 'GridPosition'])
    race_context_df = pd.read_csv(FEATURES_DIR / 'race_context.csv')
    
    target_df = pd.read_csv(PROCESSED_DIR / 'Race_results_cleaned.csv')
    target_df = target_df[['Position', 'Abbreviation', 'Year', 'RoundNumber']]
    
    