# Apple Store Scraper

Apple Store Scraper is a tool for scraping iPhone and iPad product pricing information from the Apple online store. This tool allows for comparison of Apple product prices across multiple regions (currently configured for the United States and Taiwan), helping consumers understand price differences across different markets.

**Live Demo**: [https://jonatw.github.io/apple-store-scrape/](https://jonatw.github.io/apple-store-scrape/)

## Features

- Scrapes the latest iPhone and iPad product information from Apple's online store
- Dynamically detects available iPhone and iPad models from Apple's website
- Supports multi-region comparison (configurable through REGIONS dictionary)
- Dynamically extracts colors from product names rather than using hardcoded lists
- Uses standardized product names for accurate product matching across regions
- Automatically organizes data into CSV format with region-specific columns
- Intelligent product matching system that works across different regions

## Requirements

- Python 3.6+
- Required Python packages:
  - requests==2.32.3
  - beautifulsoup4==4.12.3
  - pandas==2.2.3

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jonatw/apple-store-scrape.git
cd apple-store-scrape
```

2. Create a virtual environment and install Python dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows

pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install
```

## Usage

### Local Development

1. Run the scraper to gather the latest product data:
```bash
npm run scrape
```
This command executes both iPhone and iPad scrapers and converts the data to JSON format.

2. Start the development server:
```bash
npm run dev
```
This will start the Vite development server and open the web interface in your default browser.

3. Build for production:
```bash
npm run build
```
This will generate optimized static files in the `dist` directory.

4. Preview the production build locally:
```bash
npm run preview
```

### Automated Workflows with GitHub Actions

This project includes a GitHub Actions workflow that automatically:

1. Runs the scrapers daily to fetch the latest Apple product prices
2. Converts the data to JSON format
3. Builds the web interface
4. Deploys to GitHub Pages

You can also manually trigger the workflow from the Actions tab in your GitHub repository.

## Configuration

### Scraper Configuration

Both scraper scripts (`iphone.py` and `ipad.py`) have a configuration section at the top where you can:

- Modify the `REGIONS` dictionary to add or remove regions
- Change the `REFERENCE_REGION` for product naming
- Adjust the `REQUEST_DELAY` to control the rate of requests
- Toggle `DEBUG` mode for verbose output

Example to add Japan as a region:
```python
REGIONS = {
    "": ["US", "USD", "en-us", "$"],       # United States
    "tw": ["TW", "TWD", "zh-tw", "NT$"],   # Taiwan
    "jp": ["JP", "JPY", "ja-jp", "¥"],      # Japan
}
```

### Web Interface Configuration

You can customize the exchange rate and foreign transaction fee in the web interface. These settings are saved in the browser's local storage for future visits.

## Data Format

### Scraped CSV Data

#### iPhone CSV Format
The iPhone CSV file contains the following structure:
- Region-specific SKU columns (e.g., `SKU_US`, `SKU_TW`)
- Region-specific price columns (e.g., `Price_US`, `Price_TW`)
- `PRODUCT_NAME` - The product name from the reference region

#### iPad CSV Format
The iPad CSV file contains the following structure:
- `SKU` - Common identifier across regions
- Region-specific price columns (e.g., `Price_US`, `Price_TW`)
- `PRODUCT_NAME` - The product name from the reference region

### Converted JSON Data

The CSV data is converted to a structured JSON format for use by the web interface:

```json
{
  "metadata": {
    "lastUpdated": "2025-03-29T12:00:00.000Z",
    "exchangeRates": { "USD": 1.0, "TWD": 31.5 },
    "regions": ["US", "TW"],
    "productType": "iphone",
    "totalProducts": 40
  },
  "products": [
    {
      "SKU_US": "ABCD1234",
      "SKU_TW": "EFGH5678",
      "Price_US": 999,
      "Price_TW": 31900,
      "PRODUCT_NAME": "iPhone 16 Pro 128GB Black Titanium",
      "price_difference_percent": 0.8,
      "product_type": "iphone"
    },
    // Additional products...
  ]
}
```

## Project Structure

```
apple-store-scrape/
│
├── .github/workflows/         # GitHub Actions workflow definitions
│   └── scrape-and-deploy.yml  # Daily scraping and deployment workflow
│
├── data/                      # JSON data for web interface
│   ├── index.json             # Data index file
│   ├── iphone_data.json       # iPhone price data
│   └── ipad_data.json         # iPad price data
│
├── src/                       # Web interface source files
│   ├── icons/                 # App icons
│   ├── index.html             # Main HTML template
│   ├── main.js                # JavaScript functionality
│   └── manifest.json          # PWA manifest
│
├── .venv/                     # Python virtual environment
├── dist/                      # Compiled output (generated by build)
│
├── iphone.py                  # iPhone data scraping script
├── iphone_products_merged.csv # iPhone data output (CSV)
├── ipad.py                    # iPad data scraping script
├── ipad_products_merged.csv   # iPad data output (CSV)
├── convert_to_json.py         # Script to convert CSV to JSON
│
├── package.json               # Node.js dependencies and scripts
├── vite.config.js             # Vite configuration
├── README.md                  # Project documentation
├── TECHNICAL_SPEC.md          # Technical specifications
└── requirements.txt           # Python dependencies
```

## How It Works

### Data Collection Pipeline

1. **Model Detection**:
   - Dynamically identify available models from Apple's website
   - Fallback to default model list if website structure changes

2. **Data Scraping**:
   - Iterate through detected models for each configured region
   - Use `requests` to access Apple's official product pages
   - Parse HTML content using `BeautifulSoup`
   - Extract JSON data containing product information

3. **Data Processing**:
   - For iPhone: Use standardized product names for matching across regions
   - For iPad: Use SKU for matching products
   - Process data for each region separately
   - Handle color and model variations across regions

4. **Data Merging**:
   - Merge products from different regions based on matching strategy
   - Create region-specific columns for SKUs and prices
   - Handle missing values and duplicate data
   - Organize columns in a consistent format

5. **CSV Export**:
   - Save processed data in CSV format
   - Use `utf-8-sig` encoding to ensure proper display of characters

6. **JSON Conversion**:
   - Convert CSV data to structured JSON format
   - Add metadata like exchange rates and update timestamps
   - Calculate price difference percentages

7. **Web Interface**:
   - Dynamic rendering of product data
   - Interactive settings for exchange rates and fees
   - Search and filtering capabilities

8. **Automated Updates**:
   - GitHub Actions workflow runs the pipeline daily
   - Automatic deployment to GitHub Pages

## Extending the Project

You can extend this project in the following ways:

1. **Add More Regions**:
   - Add new entries to the `REGIONS` dictionary in the scripts
   - The format is: `"region_code": ["Display_Name", "Currency_Code", "Locale", "Currency_Symbol"]`
   - Example: `"uk": ["UK", "GBP", "en-gb", "£"]`

2. **Add More Product Categories**:
   - Create new scripts following the pattern of `iphone.py` or `ipad.py`
   - Update the URL patterns and adjust the product detection logic as needed
   - Modify `convert_to_json.py` to handle the new category
   - Update the web interface to display the new category

3. **Enhance the Web Interface**:
   - Add data visualization features like charts and graphs
   - Implement persistent comparison features
   - Add export functionality for users to download data
   - Improve the mobile experience further

4. **Add Additional Analysis**:
   - Implement historical price tracking
   - Add notifications for price changes
   - Calculate price trends over time
   - Compare with other electronics retailers

## Technical Details

### Data Sources

Data is sourced from Apple's official product pages:
- Apple Store Base URLs: 
  - US: `https://www.apple.com/shop/buy-{product}/`
  - Taiwan: `https://www.apple.com/tw/shop/buy-{product}/`
  - Other regions follow the same pattern

The scripts specifically look for a `<script>` tag with `id="metrics"` in the page, which contains complete product information, including SKU, price, and configuration details.

### Web Technologies

- **Vite**: Modern build tool and development server
- **Bootstrap 5**: Responsive UI framework
- **GitHub Actions**: CI/CD automation
- **GitHub Pages**: Static site hosting

### Error Handling

The scripts include several error handling mechanisms:
- Dynamic model detection with fallback to default lists
- HTTP response status code validation
- JSON data structure validation
- Debugging output when `DEBUG = True`
- Fill strategies for missing data
- Failsafe defaults for web interface when data is unavailable

## Notes and Limitations

- Apple may change its website structure; if scripts stop working, the HTML parsing logic may need to be updated
- This tool is for personal research and comparison only, please respect Apple's terms of service
- The scripts implement rate limiting (1 second delay between requests) to be respectful to Apple's servers
- Exchange rates are configurable in the web interface but not automatically updated from external sources
- The tool currently doesn't track historical price data
- Price comparisons don't account for tax differences between regions

## Ethical Considerations

This tool is designed for educational and personal use only. When using this scraper, please:

1. Be respectful of Apple's servers by not making excessive requests
2. Do not use this tool for commercial purposes without proper authorization
3. Respect Apple's terms of service
4. Be aware that website scraping may be against the terms of service of some websites

## Disclaimer

This project is not affiliated with, authorized by, or endorsed by Apple Inc. All product names, logos, and brands are the property of their respective owners.