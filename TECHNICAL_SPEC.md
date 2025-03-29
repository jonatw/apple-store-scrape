# Apple Store Scraper - Technical Specification

## Overview

Apple Store Scraper is a Python tool for scraping product information from the Apple online store. The tool focuses on automating the collection of iPhone and iPad product prices and details, and performing cross-region comparisons with support for multiple configurable regions (currently US and Taiwan).

## System Requirements

- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Python Version**: Python 3.6 or higher
- **Memory Requirements**: Minimum 512MB RAM
- **Storage Space**: Minimum 10MB available space

## Dependencies

| Package Name | Version | Purpose |
|---------|------|------|
| requests | 2.32.3 | Handling HTTP requests |
| beautifulsoup4 | 4.12.3 | HTML parsing |
| pandas | 2.2.3 | Data processing and analysis |

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
- Currency information is available for future features

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

## API and Data Sources

### Source Endpoints

#### iPhone
- Base URL pattern: `https://www.apple.com/{region_code}/shop/buy-iphone/{model}`
- Models: Dynamically detected or fallback to ["iphone-16-pro", "iphone-16", "iphone-16e", "iphone-15"]

#### iPad
- Base URL pattern: `https://www.apple.com/{region_code}/shop/buy-ipad/{model}`
- Models: Dynamically detected or fallback to ["ipad-pro", "ipad-air", "ipad", "ipad-mini"]

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

5. **Output Generation**:
   - Organize columns in a standardized format
   - Save to CSV with appropriate encoding

## Performance Considerations

- **Execution Time**: Scales linearly with number of models and regions
  - With 2 regions and 5 models: Approximately 10-15 seconds
  - Additional regions will increase time proportionally

- **Resource Usage**:
  - Memory Usage: Peak approximately a few hundred MB
  - CPU Usage: Low to moderate
  - Network Usage: Approximately 5-10MB data transfer per execution

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

### Future Enhancement Opportunities

- Currency conversion to facilitate direct price comparisons
- Historical data tracking to monitor price changes over time
- Visualization components for price comparison
- API endpoint for programmatic access to data
- Additional product metadata fields (e.g., specifications, availability)

## Version Changelog

### Version 1.1.0 (Current)
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