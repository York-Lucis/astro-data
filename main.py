from skyfield.api import load, Topos, load_file
from skyfield.almanac import find_discrete, moon_phases, oppositions_conjunctions
from skyfield.data import mpc
from skyfield.jpllib import SpiceKernel
from datetime import datetime, timedelta
import argparse

def get_astronomical_events(date, location, eph, ts, target_name):
    t = ts.utc(date.year, date.month, date.day)
    
    # Define the timespan to search for events (one year)
    t0 = t - 365.25
    t1 = t + 365.25
    
    events = {}

    # Find moon phases
    f_moon = moon_phases(eph)
    times, phases = find_discrete(t0, t1, f_moon)
    events['moon_phases'] = list(zip(times.utc_iso(), phases))

    # Find conjunctions and oppositions
    target = eph[target_name]  # Usar o nome do corpo celeste fornecido
    f_opconj = oppositions_conjunctions(eph, target)
    times, bodies = find_discrete(t0, t1, f_opconj)
    events['oppositions_conjunctions'] = list(zip(times.utc_iso(), bodies))

    return events

def print_events(events, date):
    print(f"\nAstronomical events around {date}:\n")
    for event_type, event_list in events.items():
        print(f"{event_type.replace('_', ' ').capitalize()}:")
        for event in event_list:
            print(f"  - {event[0]}: {event[1]}")
        print()

def main():
    parser = argparse.ArgumentParser(description='Find astronomical events for a specific date and celestial body.')
    parser.add_argument('date', type=str, help='The date to search for events (YYYY-MM-DD).')
    parser.add_argument('target', type=str, help='The celestial body to search for (e.g., "mars", "venus", "jupiter").')
    args = parser.parse_args()

    input_date = datetime.strptime(args.date, '%Y-%m-%d')

    eph = load('de421.bsp')
    ts = load.timescale()
    location = Topos('0 N', '0 E')  # Using Equator and Prime Meridian for simplicity

    events = get_astronomical_events(input_date, location, eph, ts, args.target)  # Passar o corpo celeste
    print_events(events, input_date)

    # Check for future occurrences
    future_date = datetime.now() + timedelta(days=365)
    future_events = get_astronomical_events(future_date, location, eph, ts, args.target)  # Passar o corpo celeste

    print("\nFuture Astronomical Events:")
    print_events(future_events, future_date)

if __name__ == "__main__":
    main()