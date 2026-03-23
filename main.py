import fastf1
import pandas as pd

from src.common.setup_directories import setup_directories, setup_cache, RAW_DIR, PROCESSED_DIR, FEATURES_DIR, START_YEAR, END_YEAR
from src.ingest.fetch_schedule import fetch_schedule
from src.ingest.fetch_laps import fetch_laps
from src.ingest.fetch_results import fetch_session_results
from src.ingest.fetch_session_data import fetch_session_data
from src.ingest.fetch_circuit_info import fetch_circuit_info
from src.processing.clean_laps import clean_laps
from src.processing.clean_results import clean_race_results
from src.processing.clean_session_data import clean_session_data
from src.features.driver_form import build_driver_form
from src.features.team_performance import build_team_performance


def run_ingest():
    for year in range(START_YEAR, END_YEAR + 1):
        fetch_schedule(year)
        schedule = fastf1.get_event_schedule(year)
        schedule = schedule[~schedule['EventName'].str.contains('Test') & (schedule['RoundNumber'] > 0)]
        for round_number in schedule['RoundNumber']:
            fetch_laps(year, round_number)
            fetch_session_results(year, round_number)
            fetch_session_data(year, round_number)
        print(f'{year} ingest complete.')

    fetch_circuit_info_all()


def fetch_circuit_info_all():
    schedule = fastf1.get_event_schedule(END_YEAR)
    schedule = schedule[~schedule['EventName'].str.contains('Test')]
    for round_number in schedule['RoundNumber']:
        fetch_circuit_info(END_YEAR, round_number)
    print('Circuit info ingest complete.')


def run_processing():
    laps_df = pd.read_csv(RAW_DIR / 'Race_laps.csv')
    cleaned_laps = clean_laps(laps_df)
    cleaned_laps.to_csv(PROCESSED_DIR / 'Race_laps_cleaned.csv', index=False)

    results_df = pd.read_csv(RAW_DIR / 'Race_results.csv')
    cleaned_race_results = clean_race_results(results_df)
    cleaned_race_results.to_csv(PROCESSED_DIR / 'Race_results_cleaned.csv', index=False)

    session_data_df = pd.read_csv(RAW_DIR / 'Race_session_data.csv')
    cleaned_session_data = clean_session_data(session_data_df)
    cleaned_session_data.to_csv(PROCESSED_DIR / 'Race_session_data_cleaned.csv', index=False)

    print('Processing complete.')


def run_features():
    results_df = pd.read_csv(PROCESSED_DIR / 'Race_results_cleaned.csv')
    laps_df = pd.read_csv(PROCESSED_DIR / 'Race_laps_cleaned.csv')

    driver_form_df = build_driver_form(results_df, laps_df)
    driver_form_df.to_csv(FEATURES_DIR / 'Driver_form.csv', index=False)

    team_performance_df = build_team_performance(results_df, laps_df)
    team_performance_df.to_csv(FEATURES_DIR / 'Team_form.csv', index=False)

    print('Feature engineering complete.')


if __name__ == "__main__":
    setup_directories()
    setup_cache()

    run_ingest()
    run_processing()
    run_features()
