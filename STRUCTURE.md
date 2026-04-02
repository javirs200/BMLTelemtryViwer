# BML Telemetry Viewer - Project Structure

## Overview
A modern, professional aviation telemetry viewer for analyzing flight landing data with real-time visualization.

## Folder Structure

```
BMLTelemtryViwer/
├── main.py                    # Application entry point
├── src/
│   ├── __init__.py           # Package initializer
│   ├── page_manager.py       # Page navigation & data loading
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── theme.py          # Design tokens (colors, fonts, spacing)
│   │   └── components.py     # Reusable UI components (Button, Label, Card, etc.)
│   └── pages/
│       ├── __init__.py
│       ├── main_page.py      # Landing list page
│       └── detail_page.py    # Landing detail page with charts
├── .gitignore
└── README.md
```

## Key Components

### UI System (`src/ui/`)
- **theme.py**: Centralized design system with dark aviation theme
  - Colors: Dark backgrounds with cyan/blue/orange accents
  - Fonts: Clean, professional typography
  - Spacing: Consistent 4px, 8px, 12px, 16px, 24px scale

- **components.py**: Reusable styled components
  - `StyledButton`: Primary, secondary, danger button styles
  - `StyledLabel`: Header, title, body, muted text styles
  - `StyledFrame`: Background variants
  - `Card`: Reusable card container with titles

### Pages (`src/pages/`)
- **main_page.py**: 
  - Modern header with app title
  - Scrollable list of landings grouped by date
  - Cards showing flight time, vertical speed, aircraft type
  - Click to navigate to details

- **detail_page.py**:
  - Two-column layout with aircraft info and scores
  - Dual-axis chart (Vertical Speed vs Ground Speed)
  - Real data extracted from JSON touchdown & rollout profiles
  - Back navigation

### Core Logic (`src/page_manager.py`)
- Manages page switching
- Loads JSON landing data from config.location
- Handles landing selection and navigation

## Design Features

### Dark Aviation Theme
- Background: `#0f1419` (dark navy)
- Primary Accent: `#00d4ff` (cyan)
- Secondary Accent: `#ffa502` (orange)
- Text: `#ffffff` (white)

### Modern UI Elements
- Emoji icons for visual indicators (✈, 🛬, 📅, 📊, 📈)
- Smooth transitions between pages
- Clickable cards with hover effects
- Professional monospace font for telemetry data

## Running the App

```bash
python main.py
```

The app loads all `.json` files from `config.location` (default: `demoData` folder) and displays them organized by date.

## Data Format

Landing files are JSON with:
- `timestamp_zulu`: Flight time (ISO format)
- `aircraft_title`: Aircraft model
- `airport_icao`: Landing airport code
- `touchdown_profile[]`: Array of landing approach data (vertical speed, g-force, etc.)
- `rollout_track[]`: Array of landing rollout data (groundspeed, heading, etc.)

## Future Enhancements
- [ ] Export landing reports
- [ ] Compare multiple landings side-by-side
- [ ] Statistics dashboard
- [ ] Video sync integration
- [ ] Custom chart types
