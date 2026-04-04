import json
from pathlib import Path
import pandas as pd

from models.team import Team
from models.driver import Driver
from models.circuit import Circuit


def load_teams(path: str | Path) -> dict[str, Team]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    
    team_df = pd.read_csv(Path(__file__).parents[3] / "data" / "features" / "team_features.csv")
    team_df = team_df[team_df['Year'] == 2025]
    team_df = team_df.sort_values('RoundNumber').groupby('TeamName').last().reset_index()
    
    dnf_lookup = team_df.set_index('TeamName')['TeamDNFRate'].to_dict()
    
    return {t["id"]: Team(id=t["id"], name=t["name"], dnf_rate=dnf_lookup.get(t["csv_name"], 0.05)) for t in data}



def load_drivers(json_path: str | Path, csv_path: str | Path, teams_by_id: dict[str, Team]) -> list[Driver]:
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    drivers: list[Driver] = []
    
    csv_ratings = pd.read_csv(csv_path)
    for _, row in csv_ratings.iterrows():
        driver_id = row['Abbreviation']
        rating = row['rating']
        for d in data:
            if d["id"] == driver_id:
                d["rating"] = rating
                break

    for d in data:
        team = teams_by_id[d["team_id"]]  # keep it simple; let it KeyError if wrong for now
        driver = Driver(
            id=d["id"],
            name=d["name"],
            rating=d['rating'],
            team=team
        )
        drivers.append(driver)

        # optional: if you want team -> drivers relationship
        if hasattr(team, "drivers"):
            team.drivers.append(driver)

    return drivers


def load_circuits(path: str | Path) -> list[Circuit]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        Circuit(
            round=c["round"],
            name=c["name"],
            location=c["location"],
            laps=c["laps"],
            difficulty=c.get("difficulty", 1.0)
        )
        for c in data
    ]