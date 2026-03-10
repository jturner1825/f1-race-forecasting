from sim.race import Race
from services.race_scorer import RaceScorer

class Season:
    def __init__(self, drivers, teams, circuits):
        self.drivers = drivers
        self.teams = teams
        self.circuits = circuits

        self.current_round = 1
        self.last_race_results = None
        self.winner = None

    def run_next_race(self):
        # Guard: season finished
        if self.current_round > len(self.circuits):
            return "Season Finished. No more races to run!\n"
        
        circuit = self.circuits[self.current_round - 1] # Pick current circuit for this round (0-indexed)
        r = Race(self.drivers, circuit)
        results = r.simulate_race()
        
        scorer = RaceScorer(results, self.teams)
        scorer.apply_points()

        self.last_race_results = results
        self.winner = results[0] if results else None

        self.current_round += 1
        return f"Race complete: {circuit.name}"
    
    def run_entire_season(self):
        if self.current_round > len(self.circuits):
            return "Season Finished. No more races to run!\n"

        while self.current_round <= len(self.circuits):
            circuit = self.circuits[self.current_round - 1]

            r = Race(self.drivers, circuit)
            results = r.simulate_race()

            scorer = RaceScorer(results, self.teams)
            scorer.apply_points()

            self.last_race_results = results
            self.winner = results[0] if results else None

            self.current_round += 1
        return "\nSeason Finished!"

    def return_race_results(self):
        if not self.last_race_results:
            return "No races have been run yet.\n"
        
        lines = []
        lines.append(f"Final Grid of {self.circuits[self.current_round - 2].name}")
        lines.append("--------------------------------------")

        for i, driver in enumerate(self.last_race_results, start=1):
            lines.append(f"{i}. {driver[0].name}")
        lines.append("")
        return "\n".join(lines)

    def return_winner(self):
        if not self.winner:
            return "No races have been run yet.\n"
        return f"{self.winner[0].name} has won the race!\n"

    def return_podium(self):
        if not self.last_race_results:
            return "No races have been run yet.\n"
        
        lines = []
        lines.append("Final Podium")
        lines.append("-------------------")

        for i, driver in enumerate(self.results[:3], start=1):
            lines.append(f"{i}. {driver[0].name}")
        lines.append("")
        return "\n".join(lines)

    def return_wdc_standings(self):
        drivers_sorted = sorted(self.drivers, key=lambda d: d.points, reverse=True)
        lines = []
        lines.append("\nCurrent WDC Standings")
        lines.append("-------------------------------")

        for i, driver in enumerate(drivers_sorted, start=1):
            lines.append(f"{i}. {driver.name} — {driver.points} ({driver.wins} wins)")
        lines.append("")
        return "\n".join(lines)

    def return_constructors_standings(self):
        teams_sorted = sorted(self.teams, key=lambda t: t.points, reverse=True)
        lines = []
        lines.append("\nConstructors Standings")
        lines.append("-------------------------------")

        for i, team in enumerate(teams_sorted, start=1):
            lines.append(f"{i}. {team.name} — {team.points} ({team.wins} wins)")
        return "\n".join(lines)
    


        