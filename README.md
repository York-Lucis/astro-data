AstroData
A Python application for calculating and displaying astronomical events including moon phases, planetary conjunctions, and oppositions for any given date and celestial body. Now with an easy-to-use interactive mode!

Project Description
AstroData is a powerful astronomical calculation tool that leverages the Skyfield library to provide accurate astronomical event predictions. The application can calculate moon phases, planetary conjunctions, and oppositions for any specified date and celestial body, making it valuable for astronomers, astrologers, and astronomy enthusiasts.

Key Features
Interactive Mode: A user-friendly, guided experience. No need to memorize commands!

Enhanced Validation: Smart input checking with helpful suggestions (e.g., "Did you mean 'jupiter'?").

Beautiful Output: Clear, color-coded tables and summaries for easy reading.

Moon Phase Calculations: Accurate moon phase predictions with visual indicators.

Planetary Events: Calculate conjunctions and oppositions for all major celestial bodies.

Flexible Date Input: Support for single dates or date ranges.

High Precision: Uses JPL ephemeris data for accurate calculations.

Installation Instructions
Prerequisites
Python 3.7 or higher

Internet connection (for downloading ephemeris data on the first run)

Setup
Clone the repository:

git clone [https://github.com/York-Lucis/astro-data.git](https://github.com/York-Lucis/astro-data.git)
cd astro-data

Install dependencies:

pip install -r requirements.txt

First Run: The application will automatically download the required ephemeris data (de421.bsp) if it's not found locally.

Dependencies
skyfield - Astronomical calculation library

pytz - Timezone handling

rich - For beautiful terminal output

python-Levenshtein - For "did you mean" suggestions

Usage Guide
The application can be run in two ways: Interactive Mode (recommended) and Command-Line Mode.

Interactive Mode (Recommended)
For the best experience, simply run the script without any arguments:

python main.py

The application will guide you through a series of prompts to get the information it needs.

Command-Line Mode
You can still provide all information as command-line arguments, which is useful for scripting.

python main.py --target <celestial_body> --start <start_date> [--end <end_date>] [--timezone <timezone>]

Parameters
--target: The celestial body (e.g., mars, moon).

--start: The start date in YYYY-MM-DD format (e.g., 2025-10-01).

--end: (Optional) The end date in YYYY-MM-DD format. If omitted, events for the single start date are shown.

--timezone: (Optional) The timezone for displaying times (e.g., "America/Sao_Paulo", "Europe/London"). Defaults to UTC.

Supported Celestial Bodies
mars, venus, jupiter, saturn, mercury, neptune, uranus, pluto, moon, sun

Examples
Get events for Mars for a specific day
python main.py --target mars --start 2025-12-25

Get Moon events for October 2025 in Brasilia time
python main.py --target moon --start 2025-10-01 --end 2025-10-31 --timezone America/Sao_Paulo

Sample Output
The new output is formatted for clarity and readability.

╭──────────────────────────────────────────────────────────────────────────────────╮
│ 🔭 Astronomical Summary for Moon                                                 │
│ 🗓️ October 01, 2025 to October 31, 2025                                          │
│ 📍 All times shown in America/Sao_Paulo                                          │
╰──────────────────────────────────────────────────────────────────────────────────╯

                              🌕 Moon Phases
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Date & Time                  ┃ Phase           ┃ Symbol ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 2025-10-06 10:48:00 BRT      │   First Quarter │   🌓   │
│ 2025-10-14 00:55:00 BRT      │       Full Moon │   🌕   │
│ 2025-10-21 09:25:00 BRT      │    Last Quarter │   🌗   │
│ 2025-10-28 17:05:00 BRT      │        New Moon │   🌑   │
└──────────────────────────────┴─────────────────┴────────┘

ℹ️ Astronomical Notes
  • New Moon: Moon is between Earth and Sun (not visible).
  • Full Moon: Moon is opposite the Sun (fully illuminated).
  • First/Last Quarter: Half of the Moon is illuminated.

Technical Details
Coordinate System
The application uses the Equator and Prime Meridian (0°N, 0°E) as the reference location for calculations. This provides a standardized reference point for astronomical events.

Ephemeris Data
The application uses the JPL DE421 ephemeris, which provides high-precision planetary positions. This data is automatically downloaded on first use and cached locally.

Development
Contributing
Fork the repository

Create a feature branch

Make your changes

Test with various dates and celestial bodies

Submit a pull request

License
This project is open source and available under the MIT License.

Support
For issues, questions, or contributions, please visit the GitHub repository or create an issue.

Author: York-Lucis

Repository: astro-data