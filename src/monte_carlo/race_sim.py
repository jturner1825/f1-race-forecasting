import random

POINTS_TABLE = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
INCIDENT_THRESHOLDS = [
    (0.10, 0.6),  # Red Flag
    (0.45, 0.5),  # Safety Car
    (0.80, 0.4),  # VSC
]


def simulate_race(drivers, k=0.3):
    # Step 1: Determine race incidents
    roll = random.random()
    for threshold, incident_k in INCIDENT_THRESHOLDS:
        if roll < threshold:
            k = incident_k
            break
    
    # Step 2: Roll DNF for each driver
    finishers = []
    dnf_drivers = []
    
    for d in drivers:
        if random.random() < d.team.dnf_rate:
            dnf_drivers.append(d)
        else:
            finishers.append(d)
    dnf_drivers.sort(key=lambda d: d.rating)
    
    # Step 3: Calculate performance for finishers
    performances = []
    
    for driver in finishers:
        performance = driver.rating + random.gauss(0, driver.rating * k)
        performances.append((driver, performance))
        
        
    # Step 4: Sort finishers by performance
    performances.sort(key=lambda x: x[1], reverse=False)
    
    # Step 5: Build result & return
    results = []
    for i, (driver, perf) in enumerate(performances, start=1):
        results.append({'Driver': driver,
                        'Position': i,
                        'DNF': False,
                        'Points': POINTS_TABLE.get(i, 0)})
        
    for i, driver in enumerate(dnf_drivers, start=len(performances) + 1):
        results.append({'Driver': driver,
                        'Position': i,
                        'DNF': True,
                        'Points': 0})
            
    return results