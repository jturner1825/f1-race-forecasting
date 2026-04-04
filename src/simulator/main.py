from pathlib import Path
from sim.season import Season
from services.loader import load_teams, load_drivers, load_circuits

DATA_DIR = Path(__file__).parent / "data"
MODELS_DATA_DIR = Path(__file__).parent.parent / "models" / "data" / "driver_predicted_position.csv"


def print_menu():
    lines = []

    lines.append("\n2025 F1 Season Menu")
    lines.append("-------------------------------")
    lines.append("1. Run next race")
    lines.append("2. Show last race results")
    lines.append("3. Show WDC Standings")
    lines.append("4. Show Constructors Standings")
    lines.append("5. Run entire season")
    lines.append("6. Quit\n")

    return "\n".join(lines)

def main():  
    teams_by_id = load_teams(DATA_DIR / "teams.json")
    teams = list(teams_by_id.values())
    drivers = load_drivers(DATA_DIR / "drivers.json", MODELS_DATA_DIR, teams_by_id)
    circuits = load_circuits(DATA_DIR / "circuits_2025.json")
    round = 0

    season = Season(drivers, teams, circuits)
    
    while True:
        print(print_menu())
        user_input = input("Enter an option to advance: ").strip()
        match user_input:
            case "1":
                print(season.run_next_race())
            case "2":
                print(season.return_race_results())
            case "3":
                print(season.return_wdc_standings())
            case "4":
                print(season.return_constructors_standings())
            case "5":
                print(season.run_entire_season())
            case "6":
                break
            case _:
                print("Invalid input! Please Try again!")


if __name__ == "__main__":
    main()