# Project Memory Bank

## Architecture Decisions

### Data Processing Pipeline
- **Decision**: Use CSV as intermediate format, then convert to JSON
- **Rationale**: CSV provides easy debugging, JSON optimizes web performance
- **Impact**: Clean separation between data collection and presentation

### Product Matching Strategy
- **iPhone**: Standardized name matching (regex-based normalization)
- **iPad**: SKU-based matching (simpler, more reliable)
- **Rationale**: Different Apple naming conventions require different approaches

### Regional Configuration
- **Pattern**: Dictionary-based region config with locale, currency, symbol
- **Extensibility**: New regions require only config addition
- **Current**: US (reference) and Taiwan

## Common Patterns

### Error Handling
- Graceful fallbacks for network issues
- Default values for missing data
- Debug mode for troubleshooting
- Rate limiting for respectful scraping

### Frontend Architecture
- Bootstrap 5 for responsive design
- Vanilla JavaScript for simplicity
- Local storage for user preferences
- Progressive enhancement approach

## Technical Gotchas

### Apple Website Structure
- Product data in `<script id="metrics">` JSON block
- Dynamic model detection from main category pages
- Regional URL patterns: `/{region_code}/shop/buy-{product}/`

### Exchange Rate Integration
- Cathay Bank as primary source
- Fallback to cached rates if fetch fails
- Manual override capability in web interface

### Build Process
- Vite for modern build tooling
- GitHub Actions for automation
- Source maps disabled for production

## Debugging Workflows

### Scraper Issues
1. Enable DEBUG=True in Python scripts
2. Check Apple's page structure changes
3. Verify model detection logic
4. Test with single region first

### Frontend Issues
1. Check browser console for errors
2. Verify JSON data structure
3. Test responsive design breakpoints
4. Validate local storage functionality

## Recent Updates (2025-11-28)

### Robust Scraping Architecture
- **Dual-Strategy Extraction**: All scrapers (iPhone, iPad, Mac, Watch, AirPods, TV) now implement a fallback mechanism. They first attempt to parse the standard `metrics` JSON. If that fails or yields no products, they gracefully switch to parsing the `window.PRODUCT_SELECTION_BOOTSTRAP` object using a robust brace-counting parser. This ensures compatibility with newer "selection-style" product pages (e.g., AirPods Pro 3, Apple Watch Series 11).
- **Dynamic Model Discovery**: Refactored `get_available_models` in `watch.py` and `tvhome.py` to scrape marketing pages (`/watch/`, `/tv-home/`) instead of store hubs. Implemented intelligent mapping to convert marketing names (e.g., `apple_watch_series_11`) to canonical store URL slugs (`apple-watch`), resolving 404 errors for unreleased or redirected models.

### Data Processing & Quality
- **Smart Consolidation**: 
    - Enhanced `smart_consolidate_colors.py` with an expanded color list (including "Ultramarine", "Desert", "Sage").
    - Improved name cleaning logic to strip trailing dashes and aggressively remove colors from the start of names (fixing "Silver iMac" splitting).
    - Mac products are now grouped by Price + Specs, ensuring identical configurations with different colors are merged into single rows.
- **Data Sanitization**: Updated `convert_to_json.py` to replace `NaN` values with empty strings, preventing invalid JSON output that previously crashed the frontend.
- **Correct Naming**: Implemented logic in `airpods.py` to map internal IDs (like `airpodspro`) to their true marketing titles ("AirPods Pro 3") by parsing page titles.

### Frontend & Build
- **Mac Specs Display**: Refactored `src/main.js` to elegantly display technical specifications (Chip, CPU/GPU, Memory, Storage) directly under the product name for Mac items, removing the need for empty/sparse columns.
- **Local Development**: Configured `vite.config.js` to support dynamic base URLs, allowing the site to be served locally (`python3 -m http.server`) without path errors.

## Future Considerations

### Scalability
- Current: 2 regions × 4-5 models = ~10-15 second execution
- Additional regions scale linearly
- Consider caching for repeated runs

### Maintenance
- Apple may change website structure
- Exchange rate sources may become unavailable
- Monitor for breaking changes in dependencies

## Knowledge Gaps
- Performance optimization opportunities for large-scale scrapes
- Advanced filtering/sorting requirements
- Historical data tracking needs