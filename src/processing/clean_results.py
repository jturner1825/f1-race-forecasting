import pandas as pd
from pathlib import Path
from src.common.setup_directories import setup_directories, PROCESSED_DIR, RAW_DIR

def clean_race_results(results_df: pd.DataFrame) -> pd.DataFrame:
    # Drop duplicate results (e.g. where Year, RoundNumber & DriverNumber are same)
    cleaned_results = results_df.drop_duplicates(subset=['Year', 'RoundNumber', 'DriverNumber']).copy()
    
    # Cast Position and GridPosition to numeric values, coercing errors to NaN
    cleaned_results['Position'] = pd.to_numeric(cleaned_results['Position'], errors='coerce')
    cleaned_results['GridPosition'] = pd.to_numeric(cleaned_results['GridPosition'], errors='coerce')

    # Add finished boolean column based on Status
    cleaned_results['Finished'] = cleaned_results['Status'].isin(['Finished', 'Lapped'])
    
    # Sort results by Year, RoundNumber, and Position
    cleaned_results = cleaned_results.sort_values(by=['Year', 'RoundNumber', 'Position']).reset_index(drop=True)
    
    return cleaned_results

def clean_qualifying_results(results_df: pd.DataFrame) -> pd.DataFrame:
    # Duplicate on year, round number, and driver number
    cleaned_quali_results = results_df.drop_duplicates(subset=['Year', 'RoundNumber', 'DriverNumber']).copy()

    # Cast Position to numeric
    cleaned_quali_results['Position'] = pd.to_numeric(cleaned_quali_results['Position'], errors='coerce')
    
    # Store Q1 / Q2 / Q3 as timedelta strings
    qualifying_cols = ['Q1', 'Q2', 'Q3']
    for col in qualifying_cols:
        cleaned_quali_results[col] = pd.to_timedelta(cleaned_quali_results[col]).dt.total_seconds()
    
    return cleaned_quali_results

if __name__ == "__main__":
    setup_directories()
    
    race_results_df = pd.read_csv(RAW_DIR / 'Race_results.csv')
    cleaned_race_results_df = clean_race_results(race_results_df)
    cleaned_race_results_df.to_csv(PROCESSED_DIR / 'Race_results_cleaned.csv', index=False)  
    
    qualifying_results_df = pd.read_csv(RAW_DIR / 'Qualifying_results.csv')
    cleaned_qualifying_results_df = clean_qualifying_results(qualifying_results_df)
    cleaned_qualifying_results_df.to_csv(PROCESSED_DIR / 'Qualifying_results_cleaned.csv', index=False)
    