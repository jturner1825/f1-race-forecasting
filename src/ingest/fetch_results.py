import fastf1
import pandas as pd
from pathlib import Path

CACHE_DIR = Path('C:/VS Code/f1-race-forecasting/data/cache')
RAW_DIR = Path('C:/VS Code/f1-race-forecasting/data/raw')

fastf1.Cache.enable_cache(CACHE_DIR)

def fetch_session_results(year: int, round_number: int, session_type: str = 'R'):
    session = fastf1.get_session(year, round_number, session_type)
    session.load()
    
    results_df = session.results[['DriverNumber', 'Abbreviation', 'TeamName', 'GridPosition', 'Position', 'Status']].copy()
    results_df['Year'] = year
    results_df['Event'] = session.event['EventName'].replace(' Grand Prix', "")
    results_df['RoundNumber'] = session.event['RoundNumber']
    results_df['SessionType'] = session.name
    
    try:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f'Error occurred while creating directory: {e}')
        
    if (RAW_DIR / f'{session.name}_results.csv').exists():
        results_df.to_csv(RAW_DIR / f'{session.name}_results.csv', mode='a', header=False, index=False)
    else:
        results_df.to_csv(RAW_DIR / f'{session.name}_results.csv', index=False)

if __name__ == "__main__":
    for year in [2023, 2024]:
        schedule = fastf1.get_event_schedule(year)
        schedule = schedule[~schedule['EventName'].str.contains('Test')]
        for round_number in schedule['RoundNumber']:
            fetch_session_results(year, round_number)
        print(f'{year} results saved.')