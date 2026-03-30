import pandas as pd 
import joblib 
from pathlib import Path
from src.common.setup_directories import FEATURES_DIR, MODELS_DIR

def predict_race():
    # Load models and model dataset
    driver_model = joblib.load(MODELS_DIR / 'finish_position_model.pkl')
    team_model = joblib.load(MODELS_DIR / 'team_consistency_model.pkl')
    model_df = pd.read_csv(FEATURES_DIR / 'model_dataset.csv')
    
    # One-hot encode SafetyCar, VirtualSafetyCar, RedFlag
    model_df[['SafetyCar', 'VirtualSafetyCar', 'RedFlag']] = model_df[['SafetyCar', 'VirtualSafetyCar', 'RedFlag']].astype(int)
    
    # Prepare driver & team features
    driver_features = model_df.drop(columns=['Abbreviation', 'Year', 'RoundNumber', 'Event', 'Position', 'AvgTeamFinishLast3', 'AvgTeamFinishLast5', 'TeamDNFRateLast5', 'AvgTeamPitTime', 'AvgTeamPitTimeLast3', 'AvgTeamPitTimeLast5'])
    team_features = model_df[['AvgTeamFinishLast3', 'TeamDNFRateLast5', 'Corners', 'TrackLength', 'TotalLaps', 'TrackTemp', 'AirTemp', 'Rainfall', 'SafetyCar', 'VirtualSafetyCar', 'RedFlag']]

    # Generate predictions
    driver_pred = driver_model.predict(driver_features)
    team_pred = team_model.predict(team_features)
    
    model_df['DriverPrediction'] = driver_pred
    model_df['TeamPrediction'] = team_pred
    
    model_df['FinalScore'] = model_df['DriverPrediction'] * 0.7 + model_df['TeamPrediction'] * 0.3
    
    predicted_position = model_df.groupby('Abbreviation')['FinalScore'].mean().reset_index()
    
    return predicted_position
    
if __name__ == "__main__":
    prediction_df = round(predict_race().sort_values(by='FinalScore'), 2)
    prediction_df.to_csv(MODELS_DIR / 'driver_predicted_position.csv', index=False)
    print('Predictions Complete!')