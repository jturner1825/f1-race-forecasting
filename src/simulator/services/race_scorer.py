class RaceScorer:
    POINTS_TABLE = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

    def __init__(self, results, teams):
        self.results = results
        self.teams = teams
        self.winner = None

    def apply_points(self):
        if not self.results:
            self.winner = None
            return

        self.winner = self.results[0][0]
        self.winner.add_win()

        # Award driver + constructor points
        for i, (driver, _) in enumerate(self.results, start=1):
            points = self.POINTS_TABLE.get(i,0)

            driver.add_points(points)

            driver.team.add_points(points)

        self.winner.team.add_win()