import fastf1
import pandas as pd
from src.common.setup_directories import setup_directories, setup_cache, RAW_DIR

def fetch_session_results(year: int, round_number: int, session_type: str = 'R'):
    session = fastf1.get_session(year, round_number, session_type)
    session.load()
    
    results_df = session.results[['DriverNumber', 'Abbreviation', 'TeamName', 'GridPosition', 'Position', 'Status']].copy()
    results_df['Year'] = year
    results_df['Event'] = session.event['EventName'].replace(' Grand Prix', "")
    results_df['RoundNumber'] = session.event['RoundNumber']
    results_df['SessionType'] = session.name
        
    if (RAW_DIR / f'{session.name}_results.csv').exists():
        results_df.to_csv(RAW_DIR / f'{session.name}_results.csv', mode='a', header=False, index=False)
    else:
        results_df.to_csv(RAW_DIR / f'{session.name}_results.csv', index=False)

if __name__ == "__main__":
    setup_directories()
    setup_cache()
    for year in [2023, 2024]:
        schedule = fastf1.get_event_schedule(year)
        schedule = schedule[~schedule['EventName'].str.contains('Test')]
        for round_number in schedule['RoundNumber']:
            fetch_session_results(year, round_number)
        print(f'{year} results saved.')