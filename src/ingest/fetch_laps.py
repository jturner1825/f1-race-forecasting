import fastf1
from src.common.setup_directories import setup_directories, setup_cache, RAW_DIR

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
        
    if (RAW_DIR / f'{session.name}_laps.csv').exists():
        laps_df.to_csv(RAW_DIR / f'{session.name}_laps.csv', mode='a', header=False, index=False)
    else:
        laps_df.to_csv(RAW_DIR / f'{session.name}_laps.csv', index=False)
        
if __name__ == "__main__":
    setup_directories()
    setup_cache()
    for year in [2023, 2024]:
        schedule = fastf1.get_event_schedule(year)
        schedule = schedule[~schedule['EventName'].str.contains('Test')]
        for round_number in schedule['RoundNumber']:
            fetch_laps(year, round_number)
        print(f'{year} laps saved.')