# --- IMPORTS ---
from skyfield.api import load, Topos
from skyfield.almanac import find_discrete, moon_phases, oppositions_conjunctions
from datetime import datetime, timedelta
import argparse
import pytz
import sys
try:
    from Levenshtein import distance as levenshtein_distance
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
except ImportError:
    print("Required packages 'python-Levenshtein' and 'rich' are not installed.")
    print("Please install them by running: pip install -r requirements.txt")
    sys.exit(1)

# --- CONSTANTS ---
console = Console()
SUPPORTED_BODIES = [
    'mars', 'venus', 'jupiter', 'saturn', 'mercury', 
    'neptune', 'uranus', 'pluto', 'moon', 'sun'
]

# --- HELPER & CONVERSION FUNCTIONS ---

def convert_to_timezone(utc_time_str, timezone_name):
    """Convert UTC time string to the specified timezone."""
    try:
        utc_dt = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        tz = pytz.timezone(timezone_name)
        local_dt = utc_dt.astimezone(tz)
        return local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception as e:
        return f"[bold red]Conversion failed: {str(e)}[/bold red]"

def get_moon_phase_details(phase_number):
    """Convert moon phase number to a descriptive name and an ASCII symbol."""
    phase_map = {
        0: ("New Moon", "🌑"),
        1: ("First Quarter", "🌓"),
        2: ("Full Moon", "🌕"),
        3: ("Last Quarter", "🌗")
    }
    return phase_map.get(phase_number, (f"Unknown Phase ({phase_number})", "❓"))

def get_opposition_conjunction_name(event_number, target_name):
    """Convert opposition/conjunction event number to a descriptive name."""
    return "Conjunction with Sun" if event_number == 0 else "Opposition to Sun"

# --- CORE LOGIC ---

def get_astronomical_events(eph, ts, target_name, start_date, end_date):
    """
    Calculates astronomical events for a given target and date range.
    """
    t0 = ts.from_datetime(pytz.utc.localize(start_date))
    t1 = ts.from_datetime(pytz.utc.localize(end_date))
    
    events = {}
    
    # Only calculate moon phases if the target is the moon.
    if target_name.lower() == 'moon':
        f_moon = moon_phases(eph)
        times, phases = find_discrete(t0, t1, f_moon)
        events['moon_phases'] = list(zip(times.utc_iso(), phases))
    else:
        events['moon_phases'] = []

    # Find conjunctions and oppositions for planets.
    try:
        target = eph[target_name]
        f_opconj = oppositions_conjunctions(eph, target)
        times, bodies = find_discrete(t0, t1, f_opconj)
        events['oppositions_conjunctions'] = list(zip(times.utc_iso(), bodies))
    except (KeyError, ValueError):
        # Handle cases where a target like the 'sun' cannot have these events.
        events['oppositions_conjunctions'] = []

    return events

# --- OUTPUT & DISPLAY FUNCTIONS ---

def print_events_rich(events, target_name, timezone_name, start_date, end_date):
    """Displays events using the rich library for beautiful terminal formatting."""
    
    # --- Part 1: Human-Readable Summary Panel ---
    summary_panel_content = [f"🔭 [bold cyan]Astronomical Summary for {target_name.title()}[/bold cyan]"]
    summary_panel_content.append(f"🗓️ [dim]{start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}[/dim]")
    summary_panel_content.append(f"📍 All times shown in [bold yellow]{timezone_name}[/bold yellow]")
    
    console.print(Panel("\n".join(summary_panel_content), expand=False, border_style="green"))

    # --- Part 2: Moon Phases Table ---
    if 'moon_phases' in events and events['moon_phases']:
        moon_table = Table(title="🌕 Moon Phases", show_header=True, header_style="bold magenta")
        moon_table.add_column("Date & Time", style="dim", width=30)
        moon_table.add_column("Phase", justify="right")
        moon_table.add_column("Symbol", justify="center")

        for utc_time, phase in events['moon_phases']:
            local_time = convert_to_timezone(utc_time, timezone_name)
            phase_name, phase_symbol = get_moon_phase_details(phase)
            moon_table.add_row(local_time, phase_name, phase_symbol)
        console.print(moon_table)

    # --- Part 3: Planetary Alignments Table ---
    if 'oppositions_conjunctions' in events and events['oppositions_conjunctions']:
        align_table = Table(title="🪐 Planetary Alignments", show_header=True, header_style="bold green")
        align_table.add_column("Date & Time", style="dim", width=30)
        align_table.add_column("Event", justify="right")

        for utc_time, event_type in events['oppositions_conjunctions']:
            local_time = convert_to_timezone(utc_time, timezone_name)
            event_name = get_opposition_conjunction_name(event_type, target_name)
            align_table.add_row(local_time, event_name)
        console.print(align_table)
    
    # --- Part 4: Astronomical Notes ---
    notes = ["[bold]ℹ️ Astronomical Notes[/bold]"]
    if target_name.lower() == 'moon':
        notes.extend([
            "  • [bold]New Moon[/bold]: Moon is between Earth and Sun (not visible).",
            "  • [bold]Full Moon[/bold]: Moon is opposite the Sun (fully illuminated).",
            "  • [bold]First/Last Quarter[/bold]: Half of the Moon is illuminated."
        ])
    else:
        notes.extend([
            f"  • [bold]Conjunction[/bold]: {target_name.title()} aligns with the Sun from our perspective.",
            f"  • [bold]Opposition[/bold]: Earth is between the Sun and {target_name.title()}.",
            "  • Oppositions are generally the best times for observation."
        ])
    console.print("\n".join(notes))
    
# --- INPUT VALIDATION FUNCTIONS ---

def validate_celestial_body(body_name):
    """Validates celestial body names and suggests corrections for typos."""
    if body_name.lower() in SUPPORTED_BODIES:
        return body_name.lower()
    
    closest_match = min(SUPPORTED_BODIES, key=lambda x: levenshtein_distance(body_name.lower(), x))
    
    if levenshtein_distance(body_name.lower(), closest_match) <= 2:
        if Confirm.ask(f"[yellow]Invalid body '{body_name}'. Did you mean '[bold green]{closest_match}[/bold green]'?", default=True):
            return closest_match
    
    console.print(f"[red]Error: '{body_name}' is not a supported celestial body.[/red]")
    console.print(f"Supported bodies are: {', '.join(SUPPORTED_BODIES)}")
    return None

def validate_date(date_str, prompt_text):
    """Prompts for a date until a valid format (YYYY-MM-DD) is entered."""
    while True:
        if not date_str:
            date_str = Prompt.ask(prompt_text)
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            console.print("[red]Invalid date format. Please use YYYY-MM-DD.[/red]")
            date_str = ""

def validate_timezone(tz_name):
    """Prompts for a timezone until a valid one is entered."""
    while True:
        if not tz_name:
            tz_name = Prompt.ask("Enter timezone (e.g., 'America/Sao_Paulo', 'UTC')", default="UTC")
        if tz_name in pytz.all_timezones:
            return tz_name
        else:
            console.print(f"[red]Invalid timezone '{tz_name}'. Please try again.[/red]")
            tz_name = ""

# --- INTERACTIVE MODE ---

def interactive_mode(eph, ts):
    """Guides the user through an interactive session to get event data."""
    console.print(Panel("[bold green]Welcome to AstroData Interactive Mode! ✨[/bold green]"))

    target_name = None
    while not target_name:
        raw_target = Prompt.ask("🔭 Which celestial body are you interested in?", choices=SUPPORTED_BODIES)
        target_name = validate_celestial_body(raw_target)

    mode = Prompt.ask("🗓️ Do you want events for a [bold](s)[/bold]ingle day or a date [bold](r)[/bold]ange?", choices=["s", "r"], default="r")

    if mode == 's':
        date = validate_date(None, "Enter the date (YYYY-MM-DD)")
        start_date = date
        end_date = date
    else:
        start_date = validate_date(None, "Enter the start date (YYYY-MM-DD)")
        end_date = None
        while not end_date or end_date <= start_date:
            end_date = validate_date(None, "Enter the end date (YYYY-MM-DD)")
            if end_date <= start_date:
                console.print("[red]End date must be after the start date.[/red]")

    timezone = validate_timezone(None)

    with console.status("[bold green]Calculating astronomical events...[/bold green]"):
        events = get_astronomical_events(eph, ts, target_name, start_date, end_date)
    
    print_events_rich(events, target_name, timezone, start_date, end_date)

# --- MAIN EXECUTION ---

def main():
    parser = argparse.ArgumentParser(
        description='Find astronomical events. Run without arguments for interactive mode.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('--interactive', action='store_true', help='Start the application in interactive mode.')
    parser.add_argument('--target', type=str, help='The celestial body (e.g., "mars", "moon").')
    parser.add_argument('--start', type=str, help='The start date for the search (YYYY-MM-DD).')
    parser.add_argument('--end', type=str, help='The end date for the search (YYYY-MM-DD). If omitted, defaults to start date.')
    parser.add_argument('--timezone', type=str, default='UTC', help='Timezone for displaying times (e.g., "America/Sao_Paulo").')
    
    args = parser.parse_args()

    try:
        eph = load('de421.bsp')
        ts = load.timescale()
    except Exception as e:
        console.print(f"[bold red]Error loading ephemeris data: {e}[/bold red]")
        console.print("Please ensure you have an internet connection for the first run.")
        sys.exit(1)

    if args.interactive or not (args.target and args.start):
        interactive_mode(eph, ts)
    else:
        target_name = validate_celestial_body(args.target)
        if not target_name:
            sys.exit(1)

        try:
            start_date = datetime.strptime(args.start, '%Y-%m-%d')
            end_date = datetime.strptime(args.end, '%Y-%m-%d') if args.end else start_date
        except ValueError:
            console.print("[red]Error: Invalid date format in arguments. Use YYYY-MM-DD.[/red]")
            sys.exit(1)
            
        if end_date < start_date:
            console.print("[red]Error: End date must not be before start date.[/red]")
            sys.exit(1)
        
        if args.timezone not in pytz.all_timezones:
            console.print(f"[red]Error: Invalid timezone '{args.timezone}'.[/red]")
            sys.exit(1)
        
        with console.status("[bold green]Calculating astronomical events...[/bold green]"):
            events = get_astronomical_events(eph, ts, target_name, start_date, end_date)
        
        print_events_rich(events, target_name, args.timezone, start_date, end_date)

if __name__ == "__main__":
    main()