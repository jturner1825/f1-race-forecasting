class Circuit:
    def __init__(self, name, location, round, laps, difficulty):
        self.name = name
        self.location = location
        self.round = round
        self.laps = laps
        self.difficulty = difficulty
        
    def __str__(self):
        return(
            f"Round {self.round}\n"
            f"Name: {self.name}, "
            f"Location: {self.location}\n"
            f"{self.laps} Laps\n"
            f"Difficult: {self.difficulty}\n"
        )
        