from race_sim import simulate_race

def simulate_season(drivers: list):
    results = {}
    
    for race in range(1,25):
        race_results = simulate_race(drivers)
        for r in race_results:
            driver = r['Driver']
            points = r['Points']
            results[driver.name] = results.get(driver.name, 0) + points

    return results
        

if __name__ == "__main__":
    from services.loader import load_teams, load_drivers
    from pathlib import Path

    DATA_DIR = Path(__file__).parents[1] / "simulator" / "data"
    RATINGS_CSV = Path(__file__).parents[1] / "models" / "data" / "driver_predicted_position.csv"

    teams_by_id = load_teams(DATA_DIR / "teams.json")
    drivers = load_drivers(DATA_DIR / "drivers.json", RATINGS_CSV, teams_by_id)
    
    print(simulate_season(drivers))