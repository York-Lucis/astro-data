# AstroData

A Python application for calculating and displaying astronomical events including moon phases, planetary conjunctions, and oppositions for any given date and celestial body.

## Project Description

AstroData is a powerful astronomical calculation tool that leverages the Skyfield library to provide accurate astronomical event predictions. The application can calculate moon phases, planetary conjunctions, and oppositions for any specified date and celestial body, making it valuable for astronomers, astrologers, and astronomy enthusiasts.

### Key Features

- **Moon Phase Calculations**: Accurate moon phase predictions for any date
- **Planetary Events**: Calculate conjunctions and oppositions for all major celestial bodies
- **Flexible Date Input**: Support for any date in YYYY-MM-DD format
- **Multiple Celestial Bodies**: Support for all major planets, the Moon, and the Sun
- **Future Predictions**: Calculate events up to one year in the future
- **High Precision**: Uses JPL ephemeris data for accurate calculations

## Installation Instructions

### Prerequisites

- Python 3.7 or higher
- Internet connection (for downloading ephemeris data)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/York-Lucis/astro-data.git
   cd astro-data
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **First Run**: The application will automatically download the required ephemeris data (de421.bsp) on first use.

### Dependencies

- `skyfield` - Astronomical calculation library
- `pytz` - Timezone handling and conversion
- `datetime` - Date and time handling
- `argparse` - Command-line interface

## Usage Guide

### Basic Usage

The application supports two modes of operation:

#### Single Date Mode
Find astronomical events around a specific date:

```bash
python main.py --date <date> --target <celestial_body> [--timezone <timezone>]
```

#### Date Range Mode
Find astronomical events for a specific celestial body within a date range:

```bash
python main.py --range <start_date> <end_date> <celestial_body> [--timezone <timezone>]
```

### Parameters

- **Date**: Format YYYY-MM-DD (e.g., 2023-10-01)
- **Start Date**: Format YYYY-MM-DD (e.g., 2025-09-01)
- **End Date**: Format YYYY-MM-DD (e.g., 2025-10-31)
- **Celestial Body**: One of the supported celestial bodies (see list below)
- **Timezone**: Optional timezone for displaying times (e.g., "America/Sao_Paulo", "Europe/London", "UTC"). Default: UTC

### Supported Timezones

The application supports all standard timezone names. Here are some common examples:

| Region | Timezone Name | Description |
|--------|---------------|-------------|
| Brazil | `America/Sao_Paulo` | Brasilia Time (UTC-03:00) |
| United States | `America/New_York` | Eastern Time |
| United States | `America/Los_Angeles` | Pacific Time |
| United Kingdom | `Europe/London` | Greenwich Mean Time |
| Germany | `Europe/Berlin` | Central European Time |
| Japan | `Asia/Tokyo` | Japan Standard Time |
| Australia | `Australia/Sydney` | Australian Eastern Time |
| Universal | `UTC` | Coordinated Universal Time |

### Supported Celestial Bodies

| Body | Description |
|------|-------------|
| `mars` | Mars |
| `venus` | Venus |
| `jupiter` | Jupiter |
| `saturn` | Saturn |
| `mercury` | Mercury |
| `neptune` | Neptune |
| `uranus` | Uranus |
| `pluto` | Pluto |
| `moon` | Earth's Moon |
| `sun` | The Sun |

### Examples

#### Single Date Mode Examples

Calculate Mars events for a specific date:
```bash
python main.py --date 2023-10-01 --target mars
```

Find Venus events for today:
```bash
python main.py --date 2024-01-15 --target venus
```

Check Jupiter events for a future date:
```bash
python main.py --date 2024-12-25 --target jupiter
```

#### Date Range Mode Examples

Find Earth's Moon events between September and October 2025:
```bash
python main.py --range 2025-09-01 2025-10-31 moon
```

Get Mars events for the entire year 2024 in Brasilia time:
```bash
python main.py --range 2024-01-01 2024-12-31 mars --timezone America/Sao_Paulo
```

Check Venus events for a specific month in London time:
```bash
python main.py --range 2024-06-01 2024-06-30 venus --timezone Europe/London
```

### Output

The application provides two types of output:

#### 1. Raw Astronomical Data (UTC)
- **Moon Phases**: All moon phases (new, first quarter, full, last quarter) within the specified time range
- **Conjunctions**: When the target celestial body aligns with the Sun
- **Oppositions**: When the target celestial body is opposite the Sun (for outer planets)
- **Future Events**: Additional events up to one year in the future (single date mode only)

#### 2. Human-Readable Explanations
- **Localized Times**: All events converted to your specified timezone
- **Descriptive Names**: Moon phases and planetary alignments with clear descriptions
- **Educational Notes**: Astronomical information and observation tips
- **Visual Indicators**: Emojis and formatting for easy reading

### Sample Output

#### Single Date Mode
```
Astronomical events around 2023-10-01:

Moon phases:
  - 2023-09-15 01:40:00Z: 0
  - 2023-09-22 19:32:00Z: 1
  - 2023-09-29 09:58:00Z: 2
  - 2023-10-06 13:48:00Z: 3

Oppositions conjunctions:
  - 2023-11-18 05:42:00Z: 0
  - 2024-01-16 11:52:00Z: 1
```

#### Date Range Mode with Timezone
```bash
python main.py --range 2025-09-01 2025-10-31 moon --timezone America/Sao_Paulo
```

```
=== RAW ASTRONOMICAL DATA ===
Events for moon between 2025-09-01 and 2025-10-31 (UTC):

Moon phases:
  - 2025-09-01T10:26:00Z: 0
  - 2025-09-08T18:09:00Z: 1
  - 2025-09-15T01:05:00Z: 2
  - 2025-09-22T19:32:00Z: 3
  - 2025-09-29T09:58:00Z: 0
  - 2025-10-06T13:48:00Z: 1
  - 2025-10-14T03:55:00Z: 2
  - 2025-10-21T12:25:00Z: 3
  - 2025-10-28T20:05:00Z: 0

Oppositions conjunctions:
  - 2025-09-18T15:30:00Z: 0
  - 2025-10-16T08:45:00Z: 1

==================================================
🌙 Astronomical Summary for Moon (September 2025 - October 2025)
📍 All times shown in America/Sao_Paulo

🌕 MOON PHASES:
  • New Moon on 2025-09-01 07:26:00 BRT
  • First Quarter on 2025-09-08 15:09:00 BRT
  • Full Moon on 2025-09-14 22:05:00 BRT
  • Last Quarter on 2025-09-22 16:32:00 BRT
  • New Moon on 2025-09-29 06:58:00 BRT
  • First Quarter on 2025-10-06 10:48:00 BRT
  • Full Moon on 2025-10-14 00:55:00 BRT
  • Last Quarter on 2025-10-21 09:25:00 BRT
  • New Moon on 2025-10-28 17:05:00 BRT

🪐 PLANETARY ALIGNMENTS:
  • Conjunction with Sun on 2025-09-18 12:30:00 BRT
  • Opposition to Sun on 2025-10-16 05:45:00 BRT

ℹ️  ASTRONOMICAL NOTES:
  • Moon phases occur approximately every 7.4 days
  • New Moon: Moon is between Earth and Sun (not visible)
  • Full Moon: Moon is opposite the Sun (fully illuminated)
  • First/Last Quarter: Half of the Moon is illuminated
```

## Technical Details

### Coordinate System

The application uses the Equator and Prime Meridian (0°N, 0°E) as the reference location for calculations. This provides a standardized reference point for astronomical events.

### Ephemeris Data

The application uses the JPL DE421 ephemeris, which provides high-precision planetary positions. This data is automatically downloaded on first use and cached locally.

### Time Range

The application searches for events within a ±365.25 day window around the specified date, providing comprehensive coverage of astronomical events.

## Development

### Architecture

The application is built with a modular design:

- **`get_astronomical_events()`**: Core calculation function
- **`print_events()`**: Output formatting and display
- **`main()`**: Command-line interface and argument parsing

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with various dates and celestial bodies
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/York-Lucis/astro-data) or create an issue.

---

**Author**: [York-Lucis](https://github.com/York-Lucis)  
**Repository**: [astro-data](https://github.com/York-Lucis/astro-data)