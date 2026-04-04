from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1] / "simulator"))

from services.loader import load_teams, load_drivers
from race_sim import simulate_race
from season_sim import simulate_season

DATA_DIR = Path(__file__).parents[1] / "simulator" / "data"
RATINGS_CSV = Path(__file__).parents[1] / "models" / "data" / "driver_predicted_position.csv"



def aggregate_races(race_results: list, N: int):
    race_counts = {}
    
    # Aggregate results across all simulations
    for sim in race_results:
        for driver in sim:
            if driver['Driver'].name not in race_counts:
                name = driver['Driver'].name
                race_counts[name] = {'wins': 0, 'podiums': 0, 'points_finishes': 0, 'Avg_Position': 0}
            if driver['Position'] == 1:
                race_counts[driver['Driver'].name]['wins'] += 1
            if driver['Position'] <= 3:
                race_counts[driver['Driver'].name]['podiums'] += 1
            if driver['Position'] <= 10:
                race_counts[driver['Driver'].name]['points_finishes'] += 1
            race_counts[driver['Driver'].name]['Avg_Position'] += driver['Position']

    # Convert counts to probabilities
    probabilities = pd.DataFrame.from_dict(race_counts, orient='index')
    probabilities['win_prob'] = round(probabilities['wins'] / N, 2)
    probabilities['podium_prob'] = round(probabilities['podiums'] / N, 2)
    probabilities['points_prob'] = round(probabilities['points_finishes'] / N, 2)
    probabilities['Avg_Position'] = round(probabilities['Avg_Position'] / N, 1)
    
    probabilities = probabilities.sort_values('win_prob', ascending=False)
     
    # Format DataFrame for race display
    probabilities['Win %'] = probabilities['win_prob'].apply(lambda x: f"{x:.0%}")
    probabilities['Podium %'] = probabilities['podium_prob'].apply(lambda x: f"{x:.0%}")
    probabilities['Points %'] = probabilities['points_prob'].apply(lambda x: f"{x:.0%}")
    probabilities['Avg_Position'] = probabilities['Avg_Position'].apply(lambda x: f"{x:.1f}")

    probabilities.drop(columns=['wins', 'podiums', 'points_finishes'], inplace=True)
    probabilities = probabilities.reset_index().rename(columns={'index': 'Driver'})



    return probabilities[['Driver', 'Win %', 'Podium %', 'Points %', 'Avg_Position']] 

def aggregate_season(season_results: list, N: int):
    season_counts = {}
     
    for sim in season_results:
        key = max(sim, key=sim.get)  # driver with most points in this simulation
        season_counts[key] = season_counts.get(key, 0) + 1  

    championship_prob = pd.DataFrame.from_dict(season_counts, orient='index')
    championship_prob['championship_prob'] = round(championship_prob[0] / N, 2)
    championship_prob = championship_prob.sort_values('championship_prob', ascending=False)
    
    championship_prob['Championship %'] = championship_prob['championship_prob'].apply(lambda x: f"{x:.0%}")
    championship_prob = championship_prob.reset_index().rename(columns={'index': 'Driver'})
    
    return championship_prob[['Driver', 'Championship %']]

def aggregate_teams(teams: list):
    team_dnf_rates = {}
    for team in teams:
        team_dnf_rates[team.name] = team.dnf_rate
        
    team_dnf_df = pd.DataFrame.from_dict(team_dnf_rates, orient='index', columns=['DNF Rate'])
    team_dnf_df = team_dnf_df.sort_values('DNF Rate')
    team_dnf_df['DNF Rate'] = team_dnf_df['DNF Rate'].apply(lambda x: f"{x:.1%}")
    team_dnf_df = team_dnf_df.reset_index().rename(columns={'index': 'Team'})
    
    return team_dnf_df[['Team', 'DNF Rate']]
    
if __name__ == "__main__":
    teams_by_id = load_teams(DATA_DIR / "teams.json")
    drivers = load_drivers(DATA_DIR / "drivers.json", RATINGS_CSV, teams_by_id)

    N = 10000
    race_results = []
    season_results = []
    for _ in range(N):
        race_results.append(simulate_race(drivers))
        season_results.append(simulate_season(drivers))

    print("Race Win / Podium / Points Probabilities:\n")
    print(aggregate_races(race_results, N).to_markdown(index=False))
    print("\nSeason Championship Probabilities:\n")
    print(aggregate_season(season_results, N).to_markdown(index=False))
    print("\nTeam DNF Rates:\n")
    print(aggregate_teams(list(teams_by_id.values())).to_markdown(index=False))


