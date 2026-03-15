import pandas as pd
from pathlib import Path
from src.common.setup_directories import setup_directories, PROCESSED_DIR, RAW_DIR

def clean_session_data(session_data_df: pd.DataFrame) -> pd.DataFrame:
    # Drop duplicate sessions (e.g. where Year & RoundNumber are same)
    cleaned_session_data = session_data_df.drop_duplicates(subset=['Year', 'RoundNumber']).copy()
    
    # Cast SafetyCar, VirtualSafetyCar and RedFlag columns to boolean values
    cleaned_session_data['SafetyCar'] = cleaned_session_data['SafetyCar'].astype(bool)
    cleaned_session_data['VirtualSafetyCar'] = cleaned_session_data['VirtualSafetyCar'].astype(bool)
    cleaned_session_data['RedFlag'] = cleaned_session_data['RedFlag'].astype(bool)
    
    # Sort by Year and RoundNumber
    cleaned_session_data = cleaned_session_data.sort_values(by=['Year', 'RoundNumber']).reset_index(drop=True)

    return cleaned_session_data

if __name__ == "__main__":
    setup_directories()
    session_data_df = pd.read_csv(RAW_DIR / 'Race_session_data.csv')
    cleaned_session_data_df = clean_session_data(session_data_df)
    cleaned_session_data_df.to_csv(PROCESSED_DIR / 'Race_session_data_cleaned.csv', index=False)
    
