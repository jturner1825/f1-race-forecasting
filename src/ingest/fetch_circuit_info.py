import fastf1
import pandas as pd
from src.common.setup_directories import setup_directories, setup_cache, RAW_DIR, END_YEAR

def fetch_circuit_info(year: int, round_number: int, session_type: str = 'R'):
    session = fastf1.get_session(year, round_number, session_type)
    session.load(laps=True, telemetry=True, weather=False, messages=False)
    
    circuit_info = {
        'RoundNumber' : session.event['RoundNumber'],
        'Event': session.event['EventName'].replace(' Grand Prix', ""),
        'Corners': len(session.get_circuit_info().corners),
        'TrackLength': round(max(session.get_circuit_info().corners['Distance']), 2)
    }
    
    circuit_df = pd.DataFrame([circuit_info])
    
    if (RAW_DIR / f'{year}_circuit_info.csv').exists():
        existing_df = pd.read_csv(RAW_DIR / f'{year}_circuit_info.csv')
        if round_number not in existing_df['RoundNumber'].values:
            circuit_df.to_csv(RAW_DIR / f'{year}_circuit_info.csv', mode='a', header=False, index=False)
    else:
        circuit_df.to_csv(RAW_DIR / f'{year}_circuit_info.csv', index=False)
    
if __name__ == "__main__":
    setup_directories()
    setup_cache()
    schedule = fastf1.get_event_schedule(END_YEAR)
    schedule = schedule[~schedule['EventName'].str.contains('Test') & (schedule['RoundNumber'] > 0)]
    for round_number in schedule['RoundNumber']:
        fetch_circuit_info(2025, round_number)
    print(f'{END_YEAR} circuit information saved.')
       
