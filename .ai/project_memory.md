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
- Mac product scraping implementation details
- Performance optimization opportunities
- Advanced filtering/sorting requirements
- Historical data tracking needs