import pandas as pd
from src.common.setup_directories import PROCESSED_DIR, FEATURES_DIR

def calc_finish_features(results_df: pd.DataFrame) -> pd.DataFrame:
    results_df = results_df.sort_values(by=['Year', 'RoundNumber']).reset_index(drop=True)
    
    # Group by Drivers & calculate finishing position in previous 3 races
    results_df['AvgFinishLast3'] = results_df.groupby('DriverNumber')['Position'].transform(lambda x: x.shift(1).rolling(3).mean())
    
    # Group by Drivers & calculate finishing position in previous 5 races
    results_df['AvgFinishLast5'] = results_df.groupby('DriverNumber')['Position'].transform(lambda x: x.shift(1).rolling(5).mean())
    
    # Group by Drivers & calculate DNF Rate in previous 5 races
    results_df['DNFRateLast5'] =  results_df.groupby('DriverNumber')['Finished'].transform(lambda x: (~x).shift(1).rolling(5).mean())
    
    return results_df

def calc_lap_time_features(laps_df: pd.DataFrame) -> pd.DataFrame:
    # Drop pit laps, safety car laps and red flag laps as they can skew the average lap time calculation
    laps_df = laps_df[~laps_df['IsPitLap'] & ~laps_df['IsSafetyCarLap'] & ~laps_df['RedFlagLap']].copy()

    # Calculate average lap time for each driver in each race
    laps_df = laps_df.groupby(['DriverNumber', 'Year', 'RoundNumber'])['LapTime'].agg('mean').reset_index()
    laps_df = laps_df.rename(columns={'LapTime': 'AvgLapTime'})
    
    # Sort by Year and RoundNumber
    laps_df = laps_df.sort_values(by=['Year', 'RoundNumber']).reset_index(drop=True)
    
    # Calculate average lap time in previous 3 races
    laps_df['AvgLapTimeLast3'] = laps_df.groupby('DriverNumber')['AvgLapTime'].transform(lambda x: x.shift(1).rolling(3).mean())
    
    # Calculate average lap time in previous 5 races
    laps_df['AvgLapTimeLast5'] = laps_df.groupby('DriverNumber')['AvgLapTime'].transform(lambda x: x.shift(1).rolling(5).mean())
    
    return laps_df

def calc_pit_features(laps_df: pd.DataFrame) -> pd.DataFrame:
    # Keep only pit laps
    pit_laps_df = laps_df[laps_df['IsPitLap']].copy()
    
    # Calculate average pit time for each driver in each race
    pit_laps_df = pit_laps_df.groupby(['DriverNumber', 'Year', 'RoundNumber'])['PitTime'].agg('mean').reset_index() 
    pit_laps_df = pit_laps_df.rename(columns={'PitTime': 'AvgPitTime'})
    
    # Sort by Year & RoundNumber
    pit_laps_df = pit_laps_df.sort_values(by=['Year', 'RoundNumber']).reset_index(drop=True)
    
    # Calculate average pit time in previous 3 races
    pit_laps_df['AvgPitTimeLast3'] = pit_laps_df.groupby('DriverNumber')['AvgPitTime'].transform(lambda x: x.shift(1).rolling(3).mean())
    
    # Calculate average pit time in previous 5 races
    pit_laps_df['AvgPitTimeLast5'] = pit_laps_df.groupby('DriverNumber')['AvgPitTime'].transform(lambda x: x.shift(1).rolling(5).mean())
    
    return pit_laps_df

def build_driver_form(results_df: pd.DataFrame, laps_df: pd.DataFrame) -> pd.DataFrame:
    finish_features = calc_finish_features(results_df)
    lap_time_features = calc_lap_time_features(laps_df)
    pit_features = calc_pit_features(laps_df)
    
    driver_form_df = finish_features.merge(lap_time_features, on=['DriverNumber', 'Year', 'RoundNumber'], how='left')
    driver_form_df = driver_form_df.merge(pit_features, on=['DriverNumber', 'Year', 'RoundNumber'], how='left')
    
    return driver_form_df

if __name__ == "__main__":
    results_df = pd.read_csv(PROCESSED_DIR / 'Race_results_cleaned.csv')
    laps_df = pd.read_csv(PROCESSED_DIR / 'Race_laps_cleaned.csv')
    driver_form_df = build_driver_form(results_df, laps_df)
    driver_form_df.to_csv(FEATURES_DIR / 'Driver_form.csv', index=False)
    