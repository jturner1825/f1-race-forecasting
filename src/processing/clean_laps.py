import pandas as pd
from pathlib import Path
from src.common.setup_directories import setup_directories, PROCESSED_DIR, RAW_DIR

def clean_laps(laps_df: pd.DataFrame) -> pd.DataFrame:
    # Drop deleted / inaccurate laps
    cleaned_laps = laps_df[~laps_df['Deleted'] & (laps_df['IsAccurate'] | (laps_df['PitInTime'].notna() | laps_df['PitOutTime'].notna()))].copy()
    
    # Convert time columns to seconds
    time_cols = ['LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']
    for col in time_cols:
        cleaned_laps[col] = pd.to_timedelta(cleaned_laps[col]).dt.total_seconds()
        
    # Determine if the lap was a pit lap
    cleaned_laps['IsPitLap'] = cleaned_laps['PitInTime'].notna() | cleaned_laps['PitOutTime'].notna()
    
    # Calculate total pit time for pit laps
    # Group by driver and shift PitOutTime up by one row
    next_pit_out = cleaned_laps.groupby('Driver')['PitOutTime'].shift(-1)
    cleaned_laps['PitTime'] = (pd.to_timedelta(next_pit_out) - pd.to_timedelta(cleaned_laps['PitInTime'])).dt.total_seconds()
    
    # Drop original time columns that are no longer needed
    cleaned_laps = cleaned_laps.drop(columns=['PitInTime', 'PitOutTime', 'Deleted', 'IsAccurate'])
    
    # Determine if the lap contained a safety car or virtual safety car
    cleaned_laps['IsSafetyCarLap'] = cleaned_laps['TrackStatus'].isin(['4', '6'])
    
    # Determine if the lap had a red flag
    cleaned_laps['RedFlagLap'] = cleaned_laps['TrackStatus'] == '5' 
    
    return cleaned_laps

if __name__ == "__main__":
    setup_directories()
    laps_df = pd.read_csv(RAW_DIR / 'Race_laps.csv')
    cleaned_laps_df = clean_laps(laps_df)
    cleaned_laps_df.to_csv(PROCESSED_DIR / 'Race_laps_cleaned.csv', index=False)

