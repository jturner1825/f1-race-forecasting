import random

class Race():
    def __init__(self, drivers, round, noise_range=(-10,10)):
        self.drivers = drivers
        self.round = round
        self.noise_range = noise_range
        self.results = []
        
    def simulate_race(self):
        print(f"Simulating Round {self.round}")

        # Result results each race
        self.results = []

        # Compute performance = rating + noise
        for driver in self.drivers:
            noise = random.uniform(self.noise_range[0], self.noise_range[1])
            performance = driver.rating + noise
            self.results.append((driver, performance))
        
        # Sort drivers by  performance (descending)
        self.results.sort(key=lambda x: x[1], reverse=True)
        print("Race Complete!")
            
        return self.results
