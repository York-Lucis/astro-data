from skyfield.api import load, Topos, load_file
from skyfield.almanac import find_discrete, moon_phases, oppositions_conjunctions
from skyfield.data import mpc
from skyfield.jpllib import SpiceKernel
from datetime import datetime, timedelta
import argparse
import pytz

def convert_to_timezone(utc_time_str, timezone_name):
    """Convert UTC time string to specified timezone"""
    try:
        # Parse UTC time
        utc_dt = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        
        # Get timezone
        tz = pytz.timezone(timezone_name)
        
        # Convert to timezone
        local_dt = utc_dt.astimezone(tz)
        
        return local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception as e:
        return f"{utc_time_str} (conversion failed: {str(e)})"

def get_moon_phase_name(phase_number):
    """Convert moon phase number to descriptive name"""
    phase_names = {
        0: "New Moon",
        1: "First Quarter", 
        2: "Full Moon",
        3: "Last Quarter"
    }
    return phase_names.get(phase_number, f"Unknown Phase ({phase_number})")

def get_opposition_conjunction_name(event_number, target_name):
    """Convert opposition/conjunction number to descriptive name"""
    if target_name.lower() == 'moon':
        return "Conjunction with Sun" if event_number == 0 else "Opposition to Sun"
    else:
        return "Conjunction with Sun" if event_number == 0 else "Opposition to Sun"

def generate_explanation(events, target_name, timezone_name, start_date=None, end_date=None):
    """Generate human-readable explanations for astronomical events"""
    explanations = []
    
    # Header explanation
    if start_date and end_date:
        explanations.append(f"🌙 Astronomical Summary for {target_name.title()} ({start_date.strftime('%B %Y')} - {end_date.strftime('%B %Y')})")
    else:
        explanations.append(f"🌙 Astronomical Summary for {target_name.title()}")
    
    explanations.append(f"📍 All times shown in {timezone_name}")
    explanations.append("")
    
    # Moon phases explanation
    if 'moon_phases' in events and events['moon_phases']:
        explanations.append("🌕 MOON PHASES:")
        for utc_time, phase in events['moon_phases']:
            local_time = convert_to_timezone(utc_time, timezone_name)
            phase_name = get_moon_phase_name(phase)
            explanations.append(f"  • {phase_name} on {local_time}")
        explanations.append("")
    
    # Oppositions/conjunctions explanation
    if 'oppositions_conjunctions' in events and events['oppositions_conjunctions']:
        explanations.append("🪐 PLANETARY ALIGNMENTS:")
        for utc_time, event_type in events['oppositions_conjunctions']:
            local_time = convert_to_timezone(utc_time, timezone_name)
            event_name = get_opposition_conjunction_name(event_type, target_name)
            explanations.append(f"  • {event_name} on {local_time}")
        explanations.append("")
    
    # Add general astronomical information
    explanations.append("ℹ️  ASTRONOMICAL NOTES:")
    if target_name.lower() == 'moon':
        explanations.append("  • Moon phases occur approximately every 7.4 days")
        explanations.append("  • New Moon: Moon is between Earth and Sun (not visible)")
        explanations.append("  • Full Moon: Moon is opposite the Sun (fully illuminated)")
        explanations.append("  • First/Last Quarter: Half of the Moon is illuminated")
    else:
        explanations.append(f"  • {target_name.title()} conjunctions occur when it aligns with the Sun")
        explanations.append(f"  • {target_name.title()} oppositions occur when it's opposite the Sun")
        explanations.append("  • Oppositions are best times for observation (planet is closest to Earth)")
    
    return explanations

def get_astronomical_events(date, location, eph, ts, target_name, start_date=None, end_date=None):
    if start_date and end_date:
        # Use custom date range
        t0 = ts.utc(start_date.year, start_date.month, start_date.day)
        t1 = ts.utc(end_date.year, end_date.month, end_date.day)
    else:
        # Use default behavior (one year around the given date)
        t = ts.utc(date.year, date.month, date.day)
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

def print_events(events, date, timezone_name, start_date=None, end_date=None):
    # Print raw data first
    if start_date and end_date:
        print(f"\n=== RAW ASTRONOMICAL DATA ===")
        print(f"Events for {date} between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')} (UTC):\n")
    else:
        print(f"\n=== RAW ASTRONOMICAL DATA ===")
        print(f"Events around {date} (UTC):\n")
    
    for event_type, event_list in events.items():
        print(f"{event_type.replace('_', ' ').capitalize()}:")
        for event in event_list:
            print(f"  - {event[0]}: {event[1]}")
        print()
    
    # Print explanations
    print("=" * 50)
    explanations = generate_explanation(events, date, timezone_name, start_date, end_date)
    for explanation in explanations:
        print(explanation)

def main():
    parser = argparse.ArgumentParser(description='Find astronomical events for a specific date and celestial body.')
    
    # Create mutually exclusive group for single date vs date range
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--date', type=str, help='The date to search for events (YYYY-MM-DD).')
    group.add_argument('--range', nargs=3, metavar=('START_DATE', 'END_DATE', 'TARGET'), 
                      help='Date range mode: START_DATE END_DATE TARGET (all in YYYY-MM-DD format)')
    
    # For single date mode, we still need the target
    parser.add_argument('--target', type=str, help='The celestial body to search for (e.g., "mars", "venus", "jupiter").')
    
    # Timezone argument
    parser.add_argument('--timezone', type=str, default='UTC', 
                       help='Timezone for displaying times (e.g., "America/Sao_Paulo", "Europe/London", "UTC"). Default: UTC')
    
    args = parser.parse_args()

    eph = load('de421.bsp')
    ts = load.timescale()
    location = Topos('0 N', '0 E')  # Using Equator and Prime Meridian for simplicity

    if args.range:
        # Date range mode
        start_date_str, end_date_str, target = args.range
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        if start_date >= end_date:
            print("Error: Start date must be before end date.")
            return
            
        events = get_astronomical_events(None, location, eph, ts, target, start_date, end_date)
        print_events(events, target, args.timezone, start_date, end_date)
        
    else:
        # Single date mode (original behavior)
        if not args.date or not args.target:
            print("Error: Both --date and --target are required for single date mode.")
            return
            
        input_date = datetime.strptime(args.date, '%Y-%m-%d')
        events = get_astronomical_events(input_date, location, eph, ts, args.target)
        print_events(events, input_date, args.timezone)

        # Check for future occurrences
        future_date = datetime.now() + timedelta(days=365)
        future_events = get_astronomical_events(future_date, location, eph, ts, args.target)

        print("\nFuture Astronomical Events:")
        print_events(future_events, future_date, args.timezone)

if __name__ == "__main__":
    main()