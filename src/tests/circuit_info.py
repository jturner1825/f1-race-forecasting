import fastf1 as f1

session = f1.get_session(2025, 24, 'R')
session.load()

circuit_info = session.get_circuit_info()

schedule = f1.get_event_schedule(2025)



print (round(max(session.get_circuit_info().corners['Distance']), 2))