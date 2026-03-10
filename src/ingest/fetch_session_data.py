import fastf1
import pandas as pd
from pathlib import Path

CACHE_DIR = Path('C:/VS Code/f1-race-forecasting/data/cache')
RAW_DIR = Path('C:/VS Code/f1-race-forecasting/data/raw')

fastf1.Cache.enable_cache(CACHE_DIR)


def fetch_session_data(year: int, round_number: int, session_type: str = 'R'):
    session = fastf1.get_session(year, round_number, session_type)
    session.load(weather=True, laps=True)

    session_data = {
        'Year': year,
        'Event': session.event['EventName'].replace(' Grand Prix', ""),
        'RoundNumber': session.event['RoundNumber'],
        'SessionType': session.name,
        'TotalLaps': session.laps['LapNumber'].max(),
        'TrackTemp': session.weather_data['TrackTemp'].mean().round(2),
        'AirTemp': session.weather_data['AirTemp'].mean().round(2),
        'Rainfall': session.weather_data['Rainfall'].mean().round(2),
        'SafetyCar': (session.track_status['Status'] == '4').any(),
        'VirtualSafetyCar': (session.track_status['Status'] == '6').any(),
        'RedFlag': (session.track_status['Status'] == '5').any()
    }
    
    session_df = pd.DataFrame([session_data])
    
    try:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f'Error occurred while creating directory: {e}')
        
    if (RAW_DIR / f'{session_type}_session_data.csv').exists():
        session_df.to_csv(RAW_DIR / f'{session_type}_session_data.csv', mode='a', header=False, index=False)
    else:
        session_df.to_csv(RAW_DIR / f'{session_type}_session_data.csv', index=False)
