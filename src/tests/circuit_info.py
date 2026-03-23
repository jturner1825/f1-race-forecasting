import fastf1 as f1

session = f1.get_session(2025, 24, 'Q')
session.load()

print(session.results[['DriverNumber', 'Abbreviation', 'TeamName', 'Q1', 'Q2', 'Q3', 'Position']])


