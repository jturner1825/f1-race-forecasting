import pandas as pd
from src.common.setup_directories import PROCESSED_DIR, FEATURES_DIR

def calc_team_finish_features(results_df: pd.DataFrame) -> pd.DataFrame:
    results_df = results_df.sort_values(by=['Year', 'RoundNumber']).reset_index(drop=True)
    
    # Group by TeamName & calculate finishing position in previous 3 races
    results_df['AvgTeamFinishLast3'] = results_df.groupby(['TeamName', 'Year'])['Position'].transform(lambda x: x.shift(1).rolling(3).mean())
    
    # Group by TeamName & calculate finishing position in previous 5 races
    results_df['AvgTeamFinishLast5'] = results_df.groupby(['TeamName', 'Year'])['Position'].transform(lambda x: x.shift(1).rolling(5).mean())
    
    # Group by TeamName & calculate DNF Rate in previous 5 races
    results_df['TeamDNFRateLast5'] = results_df.groupby(['TeamName', 'Year'])['Finished'].transform(lambda x: (~x).shift(1).rolling(5).mean()).round(2)
    
    return results_df

def calc_team_pit_features(laps_df: pd.DataFrame) -> pd.DataFrame:
    pit_laps_df = laps_df[laps_df['IsPitLap']].copy()
    
    # Calculate average pit time for each team (between both drivers) for each race
    pit_laps_df = pit_laps_df.groupby(['Team', 'Year', 'RoundNumber'])['PitTime'].agg('mean').reset_index().round(2)
    pit_laps_df = pit_laps_df.rename(columns={'PitTime': 'AvgTeamPitTime'})
    
    # Sort by Year & RoundNumber
    pit_laps_df = pit_laps_df.sort_values(by=['Year', 'RoundNumber']).reset_index(drop=True)
    
    # Calculate average pit time by team for previous 3 races
    pit_laps_df['AvgTeamPitTimeLast3'] = pit_laps_df.groupby(['Team', 'Year'])['AvgTeamPitTime'].transform(lambda x: x.shift(1).rolling(3).mean().round(2))
    
    # Calculate average pit time by team for previous 5 races
    pit_laps_df['AvgTeamPitTimeLast5'] = pit_laps_df.groupby(['Team', 'Year'])['AvgTeamPitTime'].transform(lambda x: x.shift(1).rolling(5).mean().round(2))
    
    return pit_laps_df
    
def build_team_performance(results_df: pd.DataFrame, laps_df: pd.DataFrame) -> pd.DataFrame:
    finish_features = calc_team_finish_features(results_df)
    pit_features = calc_team_pit_features(laps_df)
    
    pit_features = pit_features.rename(columns={'Team': 'TeamName'})
    
    team_form_df = finish_features.merge(pit_features, on=['TeamName', 'Year', 'RoundNumber'], how='left')

    return team_form_df.round(3)

if __name__ == "__main__":
    results_df = pd.read_csv(PROCESSED_DIR / 'Race_results_cleaned.csv')
    laps_df = pd.read_csv(PROCESSED_DIR / 'Race_laps_cleaned.csv')
    
    team_form_df = build_team_performance(results_df, laps_df)
    team_form_df.to_csv(FEATURES_DIR / 'team_features.csv', index=False)
    
    