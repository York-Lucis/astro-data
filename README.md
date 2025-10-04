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
   pip install skyfield
   ```

3. **First Run**: The application will automatically download the required ephemeris data (de421.bsp) on first use.

### Dependencies

- `skyfield` - Astronomical calculation library
- `datetime` - Date and time handling
- `argparse` - Command-line interface

## Usage Guide

### Basic Usage

The application requires two command-line arguments: a date and a celestial body.

```bash
python main.py <date> <celestial_body>
```

### Parameters

- **Date**: Format YYYY-MM-DD (e.g., 2023-10-01)
- **Celestial Body**: One of the supported celestial bodies (see list below)

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

#### Calculate Mars events for a specific date:
```bash
python main.py 2023-10-01 mars
```

#### Find Venus events for today:
```bash
python main.py 2024-01-15 venus
```

#### Check Jupiter events for a future date:
```bash
python main.py 2024-12-25 jupiter
```

### Output

The application provides detailed output including:

1. **Moon Phases**: All moon phases (new, first quarter, full, last quarter) around the specified date
2. **Conjunctions**: When the target celestial body aligns with the Sun
3. **Oppositions**: When the target celestial body is opposite the Sun (for outer planets)
4. **Future Events**: Additional events up to one year in the future

### Sample Output

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