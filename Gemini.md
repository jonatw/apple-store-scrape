# Gemini Project Context (apple-store-scrape)

> 🤖 **Instructions for Gemini**: This document is designed for knowledge transfer to Gemini, helping new sessions quickly understand the project context, architecture, and business logic.

## 📋 **Project Summary**

### Core Function
Apple Store Scraper is a Python-based toolset for scraping product information from Apple's online store. It performs cross-region price comparisons (specifically US vs. Taiwan) for iPhone and iPad products, presenting the data via a responsive web interface.

### Main Goals
1.  **Data Collection**: Scrape product details (Price, SKU, Name) from Apple's website.
2.  **Cross-Region Comparison**: Compare prices between US and Taiwan regions, accounting for exchange rates.
3.  **Data Visualization**: Provide a user-friendly web dashboard to view and analyze the price differences.
4.  **Automation**: Ensure daily data updates via GitHub Actions.

## 🏗️ **Architecture Decisions**

### File Structure
```
iphone.py                 # Scraper for iPhone
ipad.py                   # Scraper for iPad
mac.py                    # Scraper for Mac (In Development)
convert_to_json.py        # Data processing and JSON conversion
src/                      # Frontend source code
  main.js                 # Core JS logic
  index.html              # Web interface
  data/                   # JSON data storage
.github/workflows/        # Automation workflows
AI_CONTEXT.md             # Legacy AI context
```

### Core Component Design
-   **Scrapers (Python)**: Independent scripts for each product line using `requests`, `BeautifulSoup`, and `pandas`.
-   **Data Pipeline**: Scrape -> Raw CSV -> Processed JSON (with exchange rates).
-   **Frontend**: Vite + Bootstrap 5 for a responsive, server-less architecture (data driven by JSON).

### Tech Stack
-   **Python 3.x**: Core scraping and data processing.
-   **Pandas**: Data manipulation and CSV handling.
-   **Vite**: Frontend build tool.
-   **Bootstrap 5**: UI framework.
-   **Playwright**: E2E testing.

## 💼 **Business Logic**

### Data Structures
-   **iPhone**: Uses standardized product name matching (Regex-based normalization).
-   **iPad**: Uses SKU-based matching (More reliable for this category).
-   **Mac**: (Work in progress).

### Key Logic
1.  **Exchange Rate**: Fetched from Cathay Bank API. Includes fallback caching mechanisms and manual override in the UI.
2.  **Regional Configuration**: Dictionary-based config for easy expansion (currently US & TW).
3.  **Scraping Strategy (Dual-Layer)**:
    -   **Primary**: Extracts data from `<script id="metrics">` JSON block (standard pages).
    -   **Fallback**: Parses `window.PRODUCT_SELECTION_BOOTSTRAP` for newer "selection" pages (e.g., AirPods Pro 3, Watch Series 11).
    -   **Discovery**: Dynamically scans marketing pages to find new models and maps them to canonical store URLs to prevent 404s.
    -   **Rate Limits**: Implemented explicit delays.

### Data Processing
-   **Smart Consolidation**: Merges products with identical specs but different colors (using fuzzy matching and price tiers).
-   **Mac Specs**: Extracts detailed specs (Chip, CPU/GPU, Memory) from HTML and matches them to products based on price.

## 🔧 **Known Edge Cases**

### Apple Website Specifics
-   **Data Source**: Most reliable data is found in the JSON payload within the page source, not just the DOM.
-   **URL Patterns**: `/{region_code}/shop/buy-{product}/`
-   **Dynamic Content**: Some elements load asynchronously; the scraper targets the initial state payload.

### Error Handling
-   **Network**: Graceful fallbacks for connection issues.
-   **Missing Data**: Default values or skip logic to prevent pipeline failure (sanitizes `NaN` to empty strings).
-   **Rate Limits**: Implemented explicit delays.

## 🧪 **Test Cases**

### Testing Strategy
-   **Unit/Integration**: `test_scrapers.py` checks scraping logic.
-   **E2E**: `test_e2e.py` (Playwright) verifies the full web flow.
-   **Data Validation**: `test_data_validator.py` ensures JSON output integrity.

### Verification
-   Run `pytest` for python logic.
-   Run `npm test` (or playwright commands) for frontend validation.

## 🚨 **Critical Notes**

### UX Design
-   **Responsive**: Mobile-first design using Bootstrap grid.
-   **PWA**: Includes `manifest.json` for app-like installation.
-   **Performance**: Data is pre-processed into JSON; frontend is static and fast.

### Security & Safety
-   **Secrets**: No API keys currently required (public scraping).
-   **Environment**: Virtual environment (`.venv`) used and ignored.

## 🔄 **Recent Changes**

### Latest Updates
-   **Robust Scrapers**: Upgraded all scrapers to handle new page structures (Bootstrap JSON) and future products.
-   **Smart Aggregation**: Improved logic to group iPhone/Mac colors and clean up product names.
-   **Mac Specs**: Added detailed spec extraction and frontend display.
-   **Local Build**: Fixed relative paths for easy local testing.

## 🎯 **Tips for Gemini**

### 🛠️ **CLI Acceleration Tools**
To improve efficiency, prefer using these high-performance CLI tools when operating via shell:
-   **Search Content**: Use `rg` (ripgrep) instead of `grep` (faster, automatic .gitignore respect).
-   **Find Files**: Use `fd` instead of `find` (faster, simpler syntax).
-   **View Content**: Use `bat` instead of `cat` (syntax highlighting).
-   **List Files**: Use `eza` instead of `ls` (richer info, icons).
-   **JSON Processing**: Use `jq` (format and query JSON).
-   **Fuzzy Search**: Use `fzf` (quick filtering).
-   **Code Packing**: Use `repomix` (pack repository for AI context).

*Note: If these tools are unavailable, fall back to standard equivalents or native agent tools.*

### Quick Start
1.  Read `AI_CONTEXT.md` for historical context.
2.  Check `test_results/` or run tests to verify current state.
3.  Review `src/data/` to understand the data schema.

### Common Tasks
-   **New Region**: Update `REGIONS` dict in scraper files.
-   **New Product**: Create new scraper file (copy `iphone.py` pattern) and update `convert_to_json.py`.
-   **Debug Scraper**: Set `DEBUG=True` in the python script.

---

*📝 Last Updated: 2025-11-28*
