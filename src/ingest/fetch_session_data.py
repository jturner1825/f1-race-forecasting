import fastf1
import pandas as pd
from src.common.setup_directories import setup_directories, setup_cache, RAW_DIR

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
        
    if (RAW_DIR / f'{session.name}_session_data.csv').exists():
        session_df.to_csv(RAW_DIR / f'{session.name}_session_data.csv', mode='a', header=False, index=False)
    else:
        session_df.to_csv(RAW_DIR / f'{session.name}_session_data.csv', index=False)

if __name__ == "__main__":
    setup_directories()
    setup_cache()
    for year in [2023, 2024]:
        schedule = fastf1.get_event_schedule(year)
        schedule = schedule[~schedule['EventName'].str.contains('Test')]
        for round_number in schedule['RoundNumber']:
            fetch_session_data(year, round_number)
        print(f'{year} session data saved.')
