import pandas as pd 
import joblib 
from pathlib import Path
from src.common.setup_directories import FEATURES_DIR, MODELS_DIR

def predict_race():
    # Load models and model dataset
    driver_model = joblib.load(MODELS_DIR / 'finish_position_model.pkl')
    team_model = joblib.load(MODELS_DIR / 'team_consistency_model.pkl')
    model_df = pd.read_csv(FEATURES_DIR / 'model_dataset.csv')
    team_info_df = pd.read_csv(FEATURES_DIR / 'team_features.csv').drop_duplicates(subset=['Abbreviation'])
    team_info_df = team_info_df[['Abbreviation', 'TeamName']]
    
    # One-hot encode SafetyCar, VirtualSafetyCar, RedFlag
    model_df[['SafetyCar', 'VirtualSafetyCar', 'RedFlag']] = model_df[['SafetyCar', 'VirtualSafetyCar', 'RedFlag']].astype(int)
    
    # Prepare driver & team features
    driver_features = model_df.drop(columns=['Abbreviation', 'Year', 'RoundNumber', 'Event', 'Position', 'AvgTeamFinishLast3', 'AvgTeamFinishLast5', 'TeamDNFRate', 'AvgTeamPitTime', 'AvgTeamPitTimeLast3', 'AvgTeamPitTimeLast5'])
    team_features = model_df[['AvgTeamFinishLast3', 'TeamDNFRate', 'Corners', 'TrackLength', 'TotalLaps', 'TrackTemp', 'AirTemp', 'Rainfall', 'SafetyCar', 'VirtualSafetyCar', 'RedFlag']]

    # Generate predictions
    driver_pred = driver_model.predict(driver_features)
    team_pred = team_model.predict(team_features)
    
    model_df['DriverPrediction'] = driver_pred
    model_df['TeamPrediction'] = team_pred
    
    model_df['rating'] = model_df['DriverPrediction'] * 0.7 + model_df['TeamPrediction'] * 0.3
    
    predicted_position = model_df.groupby('Abbreviation')['rating'].mean().reset_index()
    predicted_position = predicted_position.merge(team_info_df, on=['Abbreviation'], how='left')
    
    return predicted_position
    
if __name__ == "__main__":
    prediction_df = round(predict_race().sort_values(by='rating'), 2)
    prediction_df.to_csv(MODELS_DIR / 'driver_predicted_position.csv', index=False)
    print('Predictions Complete!')