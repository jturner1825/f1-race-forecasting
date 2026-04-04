class Team:
    def __init__(self, id, name, dnf_rate):
        self.id = id
        self.name = name
        self.drivers = []
        self.points = 0
        self.wins = 0
        self.dnf_rate = dnf_rate

    def __str__(self):
        driver_names = ", ".join(driver.name for driver in self.drivers)
        return(
            f"Team Name: {self.name}\n"
            f"Drivers: {driver_names}\n"
            f"Constructors Points: {self.points}\n"
            f"Total Team Wins: {self.wins}\n"
        )
        
    def add_points(self, n):
        self.points += n

    def add_win(self):
        self.wins += 1