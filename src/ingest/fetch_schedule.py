import fastf1
import pandas as pd
from pathlib import Path

CACHE_DIR = Path('C:/VS Code/f1-race-forecasting/data/cache')
RAW_DIR = Path('C:/VS Code/f1-race-forecasting/data/raw')

fastf1.Cache.enable_cache(CACHE_DIR)

def fetch_schedule(year: int):
    schedule = fastf1.get_event_schedule(year)
    schedule_df = pd.DataFrame(schedule)
    
    schedule_df = schedule_df[~schedule_df['EventName'].str.contains('Test')]
    schedule_df = schedule_df[['RoundNumber', 'Country', 'Location', 'EventName']]
    
    try:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        print(f'Directory {RAW_DIR} created successfully.')
    except Exception as e:
        print(f'Error occurred while creating directory: {e}')
        
    schedule_df.to_csv(RAW_DIR / f'{year}_schedule.csv', index=False)

if __name__ == "__main__":
    fetch_schedule(2024)
    fetch_schedule(2023)