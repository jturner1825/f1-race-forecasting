import fastf1
from pathlib import Path

CACHE_DIR = Path('C:/VS Code/f1-race-forecasting/data/cache')
RAW_DIR = Path('C:/VS Code/f1-race-forecasting/data/raw')

fastf1.Cache.enable_cache(CACHE_DIR)

COLS = [
      'Driver', 'DriverNumber', 'Team',
      'LapNumber', 'LapTime', 'Stint',
      'Sector1Time', 'Sector2Time', 'Sector3Time',
      'PitInTime', 'PitOutTime',
      'Compound', 'TyreLife', 'FreshTyre',
      'TrackStatus', 'Position',
      'IsAccurate', 'Deleted'
  ]

def fetch_laps(year: int, round_number: int, session_type: str = 'R'):
    session = fastf1.get_session(year, round_number, session_type)
    session.load(laps=True)

    laps_df = session.laps[COLS].copy()
    laps_df['Year'] = year
    laps_df['Event'] = session.event['EventName'].replace(' Grand Prix', "")
    laps_df['RoundNumber'] = session.event['RoundNumber']
    laps_df['SessionType'] = session.name
    
    try: 
        RAW_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f'Error occurred while creating directory: {e}')
        
    if (RAW_DIR / f'{session.name}_laps.csv').exists():
        laps_df.to_csv(RAW_DIR / f'{session.name}_laps.csv', mode='a', header=False, index=False)
    else:
        laps_df.to_csv(RAW_DIR / f'{session.name}_laps.csv', index=False)
        
if __name__ == "__main__":
    for year in [2023, 2024]:
        schedule = fastf1.get_event_schedule(year)
        schedule = schedule[~schedule['EventName'].str.contains('Test')]
        for round_number in schedule['RoundNumber']:
            fetch_laps(year, round_number)
        print(f'{year} laps saved.')