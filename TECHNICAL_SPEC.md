# Apple Store Scraper - Technical Specification

## Overview

Apple Store Scraper is a Python tool for scraping product information from the Apple online store. The tool focuses on automating the collection of iPhone and iPad product prices and details, and performing cross-region comparisons with support for multiple configurable regions (currently US and Taiwan).

## System Requirements

- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Python Version**: Python 3.6 or higher
- **Memory Requirements**: Minimum 512MB RAM
- **Storage Space**: Minimum 10MB available space
- **Node.js Version**: 14.x or higher (for web interface)

## Dependencies

### Python Dependencies

| Package Name | Version | Purpose |
|---------|------|------|
| requests | 2.32.3 | Handling HTTP requests |
| beautifulsoup4 | 4.12.3 | HTML parsing |
| pandas | 2.2.3 | Data processing and analysis |

### Frontend Dependencies

| Package Name | Version | Purpose |
|---------|------|------|
| bootstrap | 5.3.3 | Responsive UI framework |
| @popperjs/core | 2.11.8 | Positioning engine for UI components |
| vite | 6.2.2 | Build tool and development server |

## Architecture

### Region Configuration

The system uses a flexible region configuration system:

```python
# Format: region_code: [display_name, currency_code, locale, currency_symbol]
REGIONS = {
    "": ["US", "USD", "en-us", "$"],       # United States
    "tw": ["TW", "TWD", "zh-tw", "NT$"],   # Taiwan
    # Additional regions can be added here
}
```

- Region codes are used in URL paths (`/tw/` for Taiwan, empty for US)
- Display names are used for column headers
- Currency information is used for price formatting and conversions

## Module Descriptions

### iphone.py

iPhone product information scraping module with multi-region support and dynamic model detection.

#### Main Functions

- `standardize_product_name(name)`:
  - **Purpose**: Creates a standardized product name for matching across regions
  - **Process**: 
    - Uses regex to extract model, capacity, and color information
    - Creates a consistent format like "iphone16pro_256gb_blacktitanium"
    - Allows matching equivalent products across regions with different naming

- `get_available_models(region_code="")`:
  - **Purpose**: Dynamically detects available iPhone models from Apple's website
  - **Process**:
    - Scrapes the main iPhone page
    - Extracts model identifiers from URLs
    - Provides fallback to default models if detection fails

- `extract_product_details(url, region_code="")`:
  - **Purpose**: Scrapes product information from a specific URL
  - **Process**:
    - Extracts product data from the JSON in the metrics script tag
    - Standardizes product names for matching
    - Includes region-specific information

- `get_all_products()`:
  - **Purpose**: Aggregates products from all configured regions
  - **Process**:
    - Gets unique models across all regions
    - Scrapes each model for each region
    - Returns a combined list of products

- `merge_product_data(product_data)`:
  - **Purpose**: Merges products from different regions using standardized names
  - **Process**:
    - Groups products by region
    - Creates region-specific columns for SKUs and prices
    - Merges products based on standardized name matching
    - Organizes columns in the preferred order

### ipad.py

iPad product information scraping module with multi-region support and dynamic model detection.

#### Main Functions

- `get_available_models(region_code="")`:
  - **Purpose**: Dynamically detects available iPad models from Apple's website
  - **Process**:
    - Scrapes the main iPad page
    - Extracts model identifiers from URLs
    - Provides fallback to default models if detection fails

- `extract_product_details(url, region_code="")`:
  - **Purpose**: Scrapes product information from a specific URL
  - **Process**:
    - Extracts product data from the JSON in the metrics script tag
    - Includes region-specific information

- `get_all_products()`:
  - **Purpose**: Aggregates products from all configured regions
  - **Process**:
    - Gets unique models across all regions
    - Scrapes each model for each region
    - Returns a combined list of products

- `merge_product_data(product_data)`:
  - **Purpose**: Merges products from different regions using SKU
  - **Process**:
    - Groups products by region
    - Creates a single SKU column and region-specific price columns
    - Merges products based on SKU matching
    - Organizes columns in the preferred order

### convert_to_json.py

Data processing module that converts CSV data to JSON format and fetches exchange rates.

#### Main Functions

- `fetch_exchange_rate(debug=False)`:
  - **Purpose**: Fetches the current USD/TWD exchange rate from Cathay Bank's website
  - **Process**:
    - Makes HTTP request to Cathay Bank's exchange rate page
    - Parses HTML content using BeautifulSoup
    - Extracts the USD/TWD selling rate
    - Returns the rate as a float value

- `get_exchange_rates(debug=False)`:
  - **Purpose**: Gets exchange rates for use in price comparisons
  - **Process**:
    - Attempts to fetch the latest exchange rate from Cathay Bank
    - If successful, saves the rate to exchange_rate.json
    - If fetching fails, tries to use previously saved rates
    - Provides fallback default values if all else fails
    - Returns exchange rate data structure

- `csv_to_json(csv_file, json_file, product_type, exchange_rates)`:
  - **Purpose**: Converts CSV product data to structured JSON format
  - **Process**:
    - Reads CSV file using pandas
    - Processes price difference calculations using exchange rates
    - Creates structured JSON with metadata and product array
    - Writes JSON output to the specified file

### main.js

Frontend JavaScript code that handles the web interface functionality.

#### Main Functions

- `loadProductData(product)`:
  - **Purpose**: Loads product data from JSON files
  - **Process**:
    - Fetches product JSON data
    - Updates exchange rate if available in metadata
    - Adds calculated price differences with fees
    - Returns structured data for rendering

- `renderProductTable(products)`:
  - **Purpose**: Renders product data into the HTML table
  - **Process**:
    - Creates table rows for each product
    - Formats prices and calculations
    - Adds visual indicators for price comparisons
    - Applies recommendation badges

- `updateSummaryStats(data)`:
  - **Purpose**: Updates summary statistics display
  - **Process**:
    - Calculates overall statistics like average price differences
    - Updates UI elements with formatted values
    - Applies appropriate styling based on values

- `initSettings()`:
  - **Purpose**: Initializes exchange rate and fee settings
  - **Process**:
    - Loads saved settings from local storage
    - Sets up event listeners for settings changes
    - Handles updates to the UI when settings change

## Data Structures

### Configuration Data

```python
# Define regions to scrape
REGIONS = {
    "": ["US", "USD", "en-us", "$"],       # United States
    "tw": ["TW", "TWD", "zh-tw", "NT$"],   # Taiwan
}

# Reference region for product naming
REFERENCE_REGION = list(REGIONS.keys())[0]
```

### Input Data

Example of JSON structure scraped from the webpage (simplified):
```json
{
  "data": {
    "products": [
      {
        "sku": "MYMG3",
        "name": "iPhone 16 Pro 256GB Black Titanium",
        "price": {
          "fullPrice": 1099.0
        },
        "category": "iphone",
        "partNumber": "MYMG3LL/A"
      }
    ]
  }
}
```

### Exchange Rate Data Structure

```json
{
  "rates": {
    "USD": 1.0,
    "TWD": 31.53
  },
  "lastUpdated": "2025-03-30T14:30:22.456789",
  "source": "Cathay Bank"
}
```

### Product Matching Strategies

#### iPhone - Standardized Name Matching

The iPhone script uses a regex-based approach to standardize product names:
1. Extract model information (e.g., "iphone16pro" from "iPhone 16 Pro")
2. Extract capacity (e.g., "256gb")
3. Extract color (e.g., "blacktitanium")
4. Create a standardized key like "iphone16pro_256gb_blacktitanium"
5. Match products across regions using this key

This approach overcomes differences in naming conventions between regions.

#### iPad - SKU Matching

The iPad script uses a simpler SKU-based matching approach:
1. Use the SKU as a common identifier across regions
2. Merge data using SKU as the key

### Output Data Formats

#### iPhone Output Structure
```
SKU_US,SKU_TW,Price_US,Price_TW,PRODUCT_NAME
MLG33LL/A,MLG33ZP/A,999.0,31900.0,iPhone 16 Pro 128GB Natural Titanium
```

#### iPad Output Structure
```
SKU,Price_US,Price_TW,PRODUCT_NAME
MPMJ3LL/A,599.0,18900.0,iPad Air Wi-Fi 64GB - Space Gray
```

#### JSON Output Structure
```json
{
  "metadata": {
    "lastUpdated": "2025-03-30T14:30:22.456789",
    "exchangeRates": {
      "USD": 1.0,
      "TWD": 31.53
    },
    "regions": ["US", "TW"],
    "productType": "iphone",
    "totalProducts": 40,
    "lastExchangeRateUpdate": "2025-03-30T14:30:22.456789",
    "exchangeRateSource": "Cathay Bank"
  },
  "products": [
    {
      "SKU_US": "MLG33LL/A",
      "SKU_TW": "MLG33ZP/A",
      "Price_US": 999.0,
      "Price_TW": 31900.0,
      "PRODUCT_NAME": "iPhone 16 Pro 128GB Natural Titanium",
      "price_difference_percent": 0.8,
      "product_type": "iphone"
    }
  ]
}
```

## Frontend Architecture

### Core Components

1. **Settings Panel**:
   - Exchange rate input with auto-population from backend data
   - Foreign transaction fee adjustment
   - Collapsible interface for better mobile experience
   - Local storage persistence for user preferences

2. **Price Summary Cards**:
   - Product count display
   - Average price difference (with and without fees)
   - Last updated timestamp
   - Visual indicators for favorable pricing regions

3. **Product Table**:
   - Responsive design with horizontal scrolling on mobile
   - Search functionality for filtering products
   - Sortable columns (using native JavaScript)
   - Color-coded price differences
   - Purchase recommendation badges

4. **Theme System**:
   - Light/dark mode toggle
   - System preference detection
   - Local storage persistence
   - Dynamic styling adaptation

### UI Interactions

1. **Settings Update Flow**:
   - User changes exchange rate or fee
   - Values validated and stored in local storage
   - Real-time recalculation of all price differences
   - Update of all affected UI elements
   - Temporary confirmation badge display

2. **Product Category Switching**:
   - User selects product category (iPhone/iPad)
   - Data fetched for selected category
   - Table and summary statistics updated
   - Search field cleared
   - Page title updated

3. **Search Functionality**:
   - Real-time filtering as user types
   - Case-insensitive search
   - Matches against product name
   - Dynamic table updates

## API and Data Sources

### Source Endpoints

#### iPhone
- Base URL pattern: `https://www.apple.com/{region_code}/shop/buy-iphone/{model}`
- Models: Dynamically detected or fallback to ["iphone-16-pro", "iphone-16", "iphone-16e", "iphone-15"]

#### iPad
- Base URL pattern: `https://www.apple.com/{region_code}/shop/buy-ipad/{model}`
- Models: Dynamically detected or fallback to ["ipad-pro", "ipad-air", "ipad", "ipad-mini"]

#### Exchange Rate
- Base URL: `https://accessibility.cathaybk.com.tw/exchange-rate-search.aspx`
- Data location: Table row containing `美元(USD)` in the first column
- Target data: Selling rate in the third column

### Data Extraction Location

In the HTML, product information is contained in the following tag:
```
<script type="application/json" id="metrics">...</script>
```

## Execution Flow

### Common Pattern

1. **Model Detection**:
   - Dynamically identify available models from Apple's website
   - Combine models from all regions to ensure complete coverage

2. **Data Collection**:
   - For each model and region, scrape the corresponding page
   - Rate-limited requests (1 second between requests)

3. **Data Processing**:
   - Extract product information from JSON data
   - Apply region-specific metadata

4. **Data Merging**:
   - Apply product matching strategy (standardized names for iPhone, SKU for iPad)
   - Create multi-region output format
   - Handle missing values

5. **Exchange Rate Fetching**:
   - Request Cathay Bank's exchange rate page
   - Parse HTML to extract USD/TWD exchange rate
   - Apply fallback mechanisms if fetching fails

6. **JSON Conversion**:
   - Read CSV product data
   - Calculate price differences using exchange rates
   - Generate structured JSON with metadata
   - Save to src/data directory for web access

7. **Web Initialization**:
   - Load product data based on selected category
   - Initialize UI components and event listeners
   - Apply stored settings from local storage
   - Render product table and summary statistics

## Performance Considerations

- **Execution Time**: Scales linearly with number of models and regions
  - With 2 regions and 5 models: Approximately 10-15 seconds
  - Additional regions will increase time proportionally

- **Resource Usage**:
  - Memory Usage: Peak approximately a few hundred MB
  - CPU Usage: Low to moderate
  - Network Usage: Approximately 5-10MB data transfer per execution

- **Frontend Performance**:
  - Initial load time: Under 2 seconds on typical connections
  - Time to interactive: Under 3 seconds
  - Product table rendering: Under 500ms for 50 products
  - Search filtering: Under 100ms response time

## Error Handling and Resilience

The system incorporates multiple resilience features:

1. **Fallback Model Lists**:
   - When dynamic model detection fails, falls back to predefined lists
   - Ensures operation even if Apple's site structure changes

2. **Debug Mode**:
   - When enabled, provides detailed logging of operations
   - Helps diagnose issues with scraping or data processing

3. **Input Validation**:
   - Validates JSON data before processing
   - Handles missing or malformed data gracefully

4. **Missing Data Handling**:
   - Fills missing prices with zeros
   - Fills missing SKUs with empty strings
   - Ensures consistent output format regardless of data completeness

5. **Exchange Rate Fallbacks**:
   - Attempts to fetch latest rates
   - If fetching fails, tries previously saved rates
   - Provides default fallback values if all else fails

6. **Frontend Error Handling**:
   - Graceful degradation when data is missing
   - Fallback content for failed API requests
   - Input validation for user settings
   - Cross-browser compatibility measures

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. **Trigger Events**:
   - Daily scheduled runs at midnight UTC
   - Manual workflow dispatch
   - Push to main branch

2. **Build Process**:
   - Setup Python environment
   - Install dependencies
   - Run scrapers
   - Convert data to JSON
   - Setup Node.js environment
   - Build frontend
   - Deploy to GitHub Pages

3. **Deployment Strategy**:
   - Force orphan for clean GitHub Pages history
   - Automated commit messages with timestamp
   - Direct deployment from dist directory

## Extensibility

The system is designed to be modular and can be extended in the following ways:

### Adding New Regions

1. Add region entries to the `REGIONS` dictionary:
```python
"jp": ["JP", "JPY", "ja-jp", "¥"]  # Japan
```

2. No other code changes required - the system will automatically:
   - Include the new region in data collection
   - Add region-specific columns to the output

### Adding New Product Categories

1. Create a new script following the pattern of `iphone.py` or `ipad.py`
2. Update URL patterns and model detection logic as needed
3. Choose an appropriate product matching strategy
4. Update convert_to_json.py to handle the new category
5. Add navigation elements to the frontend

### Frontend Extensibility

1. **Component-Based Design**:
   - New UI elements can be added with minimal changes
   - CSS is organized to allow easy styling of new components

2. **Data-Driven Rendering**:
   - UI components adapt to data structure
   - New data fields will be automatically incorporated

3. **Settings Architecture**:
   - Settings system can be extended for additional parameters
   - Local storage persistence handles new settings automatically

## Future Enhancement Opportunities

- Support for additional currency exchange rate sources
- Historical data tracking to monitor price changes over time
- Visualization components for price comparison (charts, graphs)
- API endpoint for programmatic access to data
- Additional product metadata fields (e.g., specifications, availability)
- Support for more Apple product categories (MacBook, Apple Watch, etc.)
- User accounts for saving favorite products and receiving price alerts
- Expanded regional support for global price comparison
- Tax calculation options for more accurate total price estimates
- PWA features for offline functionality
- Localization support for multiple languages
- Product image integration from Apple's CDN
- Advanced filtering and sorting options

## Version Changelog

### Version 1.2.0 (Current)
- Fixed layout issues with settings panel and price summary display
- Removed unused test and utility HTML files
- Improved responsive design for mobile devices
- Enhanced settings panel with better visual feedback
- Updated documentation with comprehensive technical details
- Integrated exchange rate fetching directly into convert_to_json.py
- Streamlined data storage to use src/data directory exclusively
- Improved Vite build configuration for better file handling
- Enhanced GitHub Actions workflow for smoother deployments
- Updated debug logging for better troubleshooting

### Version 1.1.0
- Added dynamic model detection from Apple website
- Implemented multi-region architecture with configurable region support
- Improved product matching with standardized product names
- Added dynamic color detection from product names
- Reorganized output format for clarity
- Enhanced debugging capabilities

### Version 1.0.0
- Initial version
- Support for iPhone and iPad product information scraping
- Support for US and Taiwan region comparison