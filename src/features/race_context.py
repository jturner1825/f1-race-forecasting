import pandas as pd
from src.common.setup_directories import RAW_DIR, PROCESSED_DIR, FEATURES_DIR

def qualifying_delta_to_pole(results_df: pd.DataFrame) -> pd.DataFrame:
    results_df = results_df.sort_values(by=['Year', 'RoundNumber']).reset_index(drop=True)
    
    # Determine each driver's best qualifying time
    results_df['BestQualiTime'] = results_df['Q3'].fillna(results_df['Q2'].fillna(results_df['Q1']))
    
    # Find the pole time per round
    filtered_results_df = results_df[results_df['Position'] == 1]
    filtered_results_df = filtered_results_df[['Year', 'RoundNumber', 'BestQualiTime']]
    filtered_results_df = filtered_results_df.rename(columns={'BestQualiTime': 'PoleTime'})
    
    # Merge on Year & RoundNumber
    results_df= results_df.merge(filtered_results_df, on=['Year','RoundNumber'], how='left')
    
    # Compute quali delta
    results_df['QualiDelta'] = results_df['BestQualiTime'] - results_df['PoleTime']
    
    # Penalize drivers w/ NaN QualiDelta
    penalty_series = results_df.groupby(['Year', 'RoundNumber'])['QualiDelta'].transform(lambda x: x.max() * 1.2)
    results_df['QualiDelta'] = results_df['QualiDelta'].fillna(penalty_series)
    
    results_df['QualiDelta'] = results_df['QualiDelta'].round(3)
    
    return results_df[['Abbreviation', 'Year', 'RoundNumber', 'Event', 'QualiDelta']]

def build_race_context():
    # Load all dataframes
    race_results_df = pd.read_csv(PROCESSED_DIR / 'Race_results_cleaned.csv')
    session_data_df = pd.read_csv(PROCESSED_DIR / 'Race_session_data_cleaned.csv')
    circuit_info_df = pd.read_csv(RAW_DIR / '2025_circuit_info.csv')
    quali_results_df = pd.read_csv(PROCESSED_DIR / 'Qualifying_results_cleaned.csv')
    
    # Store quali delta results
    quali_delta_df = qualifying_delta_to_pole(quali_results_df)
    
    # Create race context dataframe
    race_context_df = race_results_df[['Abbreviation', 'Year', 'RoundNumber', 'Event', 'GridPosition']]
    race_context_df = race_context_df.merge(quali_delta_df.drop(columns=['Event']) , on=['Abbreviation', 'Year', 'RoundNumber'], how='left')
    race_context_df = race_context_df.merge(circuit_info_df.drop(columns=['RoundNumber']), on=['Event'], how='left')
    race_context_df = race_context_df.merge(session_data_df.drop(columns=['Event']), on=['Year', 'RoundNumber'], how='left')
    race_context_df = race_context_df.drop(columns=['SessionType'])
    
    return race_context_df
    

if __name__ == "__main__":
    race_context = build_race_context()
    race_context.to_csv(FEATURES_DIR / 'race_features.csv', index=False)
    