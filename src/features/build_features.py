import pandas as pd
from src.common.setup_directories import PROCESSED_DIR, FEATURES_DIR

def build_features():
    # Build featured dataframes & drop unnecessary columns
    driver_form_df = pd.read_csv(FEATURES_DIR / 'Driver_form.csv').drop(columns=['Position', 'GridPosition', 'SessionType', 'Status', 'Finished', 'DriverNumber', 'TeamName', 'Event'])
    team_form_df = pd.read_csv(FEATURES_DIR / 'Team_form.csv').drop(columns=['Position', 'GridPosition', 'SessionType', 'Status', 'Finished', 'DriverNumber', 'TeamName', 'Event'])
    race_context_df = pd.read_csv(FEATURES_DIR / 'race_context.csv')
    
    # Create target dataframe
    target_df = pd.read_csv(PROCESSED_DIR / 'Race_results_cleaned.csv')
    target_df = target_df[['Position', 'Abbreviation', 'Year', 'RoundNumber']]
    
    # Merge dataframes into one feature dataframe
    features_df = driver_form_df.merge(team_form_df, on=['Abbreviation', 'Year', 'RoundNumber'], how='left')
    features_df = features_df.merge(race_context_df, on=['Abbreviation', 'Year', 'RoundNumber'], how='left')
    features_df = features_df.merge(target_df, on=['Abbreviation', 'Year', 'RoundNumber'], how='left')
    
    # Drop NaN rows
    features_df = features_df.dropna()
    
    return features_df

if __name__ == "__main__":
    built_features_df = build_features()
    built_features_df.to_csv(FEATURES_DIR / 'model_dataset.csv', index=False)
    
    
    
    