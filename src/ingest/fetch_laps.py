import fastf1
import pandas as pd
from src.common.setup_directories import setup_directories, setup_cache, RAW_DIR, START_YEAR, END_YEAR

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
    try:
        session = fastf1.get_session(year, round_number, session_type)
        session.load(laps=True)
    except Exception as e:
        print(f'Skipping {year} round {round_number}: {e}')
        return

    laps_df = session.laps[COLS].copy()
    laps_df['Year'] = year
    laps_df['Event'] = session.event['EventName'].replace(' Grand Prix', "")
    laps_df['RoundNumber'] = session.event['RoundNumber']
    laps_df['SessionType'] = session.name
        
    csv_path = RAW_DIR / f'{session.name}_laps.csv'
    if csv_path.exists():
        existing_df = pd.read_csv(csv_path)
        if not ((existing_df['Year'] == year) & (existing_df['RoundNumber'] == round_number)).any():
            laps_df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        laps_df.to_csv(csv_path, index=False)
        
if __name__ == "__main__":
    setup_directories()
    setup_cache()
    for year in range(START_YEAR, END_YEAR + 1):
        schedule = fastf1.get_event_schedule(year)
        schedule = schedule[~schedule['EventName'].str.contains('Test') & (schedule['RoundNumber'] > 0)]
        for round_number in schedule['RoundNumber']:
            fetch_laps(year, round_number)
        print(f'{year} laps saved.')