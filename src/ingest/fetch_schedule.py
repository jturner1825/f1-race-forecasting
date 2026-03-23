import fastf1
import pandas as pd
from src.common.setup_directories import setup_directories, setup_cache, RAW_DIR, START_YEAR, END_YEAR

def fetch_schedule(year: int):
    schedule = fastf1.get_event_schedule(year)
    schedule_df = pd.DataFrame(schedule)
    
    schedule_df = schedule_df[~schedule_df['EventName'].str.contains('Test')]
    schedule_df = schedule_df[['RoundNumber', 'Country', 'Location', 'EventName']]
        
    schedule_df.to_csv(RAW_DIR / f'{year}_schedule.csv', index=False)

if __name__ == "__main__":
    setup_directories()
    setup_cache()
    for year in range(START_YEAR, END_YEAR + 1):
        fetch_schedule(year)
        print(f'{year} schedule saved.')
