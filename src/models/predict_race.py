import pandas as pd 
import joblib 
from pathlib import Path
from src.common.setup_directories import FEATURES_DIR, MODELS_DIR

driver_model = joblib.load(MODELS_DIR / 'finish_position_model.pkl')
team_model = joblib.load(MODELS_DIR / 'team_consistency_model.pkl')

