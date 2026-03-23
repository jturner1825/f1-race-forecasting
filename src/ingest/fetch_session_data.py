import fastf1
import pandas as pd
from src.common.setup_directories import setup_directories, setup_cache, RAW_DIR, START_YEAR, END_YEAR

def fetch_session_data(year: int, round_number: int, session_type: str = 'R'):
    try:
        session = fastf1.get_session(year, round_number, session_type)
        session.load(weather=True, laps=True)
    except Exception as e:
        print(f'Skipping {year} round {round_number}: {e}')
        return

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
        
    csv_path = RAW_DIR / f'{session.name}_session_data.csv'
    if csv_path.exists():
        existing_df = pd.read_csv(csv_path)
        if not ((existing_df['Year'] == year) & (existing_df['RoundNumber'] == round_number)).any():
            session_df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        session_df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    setup_directories()
    setup_cache()
    for year in range(START_YEAR, END_YEAR + 1):
        schedule = fastf1.get_event_schedule(year)
        schedule = schedule[~schedule['EventName'].str.contains('Test') & (schedule['RoundNumber'] > 0)]
        for round_number in schedule['RoundNumber']:
            fetch_session_data(year, round_number)
        print(f'{year} session data saved.')
