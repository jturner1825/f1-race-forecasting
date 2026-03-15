import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path('C:/VS Code/f1-race-forecasting/data/processed')
FEATURES_DIR = Path('C:/VS Code/f1-race-forecasting/data/features')

def calc_team_finish_features(results_df: pd.DataFrame) -> pd.DataFrame:
    pass

def calc_team_pit_features(laps_df: pd.DataFrame) -> pd.DataFrame:
    pass

def build_team_performance(results_df: pd.DataFrame, laps_df: pd.DataFrame) -> pd.DataFrame:
    pass
    