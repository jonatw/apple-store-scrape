# AI Knowledge Transfer System

## Project Overview
Apple Store Scraper is a Python tool for scraping product information from Apple's online store. The project performs cross-region price comparisons for iPhone and iPad products with a web interface for displaying results.

## Core Architecture
- **Backend**: Python scrapers using requests, BeautifulSoup, and pandas
- **Frontend**: Vite + Bootstrap 5 web interface with responsive design
- **Automation**: GitHub Actions for daily data updates and deployment
- **Data Flow**: Scrape → CSV → JSON → Web Interface

## Key Components

### Python Scripts
- `iphone.py`: iPhone product scraper with standardized name matching
- `ipad.py`: iPad product scraper with SKU-based matching  
- `mac.py`: Mac product scraper (in development)
- `convert_to_json.py`: CSV to JSON converter with exchange rate fetching

### Frontend Components
- `src/main.js`: Core JavaScript functionality
- `src/index.html`: Main web interface
- `src/data/`: JSON data storage directory

## Current Configuration
- **Regions**: US (default) and Taiwan (tw)
- **Product Types**: iPhone, iPad, Mac (in progress)
- **Exchange Rate Source**: Cathay Bank USD/TWD rates
- **Update Schedule**: Daily via GitHub Actions

## Development Patterns

### Code Conventions
- All comments and documentation in English
- Consistent error handling with fallback mechanisms
- Rate limiting (1 second delay) for respectful scraping
- Debug mode available in all scripts
- Modular design for easy region/product expansion

### Data Structures
- **iPhone**: Uses standardized product name matching across regions
- **iPad**: Uses SKU-based matching
- **Output Format**: Region-specific columns (SKU_US, Price_US, etc.)

### Recent Changes
- Fixed layout issues with settings panel and summary display
- Enhanced responsive design for mobile devices
- Streamlined data storage to src/data directory
- Improved GitHub Actions workflow

## Common Tasks

### Adding New Regions
1. Update REGIONS dictionary in scraper files
2. No other code changes needed - automatic integration

### Adding New Products
1. Create new scraper following iphone.py/ipad.py pattern
2. Update convert_to_json.py to handle new category
3. Add navigation to web interface

### Debugging Issues
1. Enable DEBUG=True in scraper files
2. Check console output for detailed logging
3. Verify Apple's page structure hasn't changed

## Technical Notes
- Dynamic model detection with fallback lists
- Graceful handling of missing data
- Cross-browser compatibility considerations
- PWA manifest for mobile app-like experience

## AI Session Handoff Protocol
When starting a new AI session, review:
1. This AI_CONTEXT.md file
2. Recent git commits for changes
3. Current todo list status
4. Any pending issues or features

## Project Status
- **Stable Features**: iPhone/iPad scraping, web interface, automated deployment
- **In Development**: Mac product support
- **Known Issues**: None currently reported
- **Last Updated**: 2025-01-08