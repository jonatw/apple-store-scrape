# Apple Store Scraper

A tool for comparing Apple product prices across regions (US and Taiwan). Scrapes all major Apple product categories, consolidates color variants, and serves a responsive comparison website.

**Live Demo**: [https://jonatw.github.io/apple-store-scrape/](https://jonatw.github.io/apple-store-scrape/)

## Features

- Scrapes **all Apple product categories**: iPhone, iPad, Mac, Apple Watch, AirPods, Apple TV, HomePod
- Dynamic model discovery — automatically detects current products from Apple's website
- Cross-region price matching with dual-strategy extraction (metrics JSON + bootstrap JS)
- Smart color variant consolidation — merges identical products differing only by color
- Automatic USD/TWD exchange rate fetching from Cathay Bank
- Daily automated updates via GitHub Actions
- Responsive web interface with dark mode, search, and interactive settings

## Requirements

- Python 3.10+
- Node.js 20+

## Quick Start

```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
npm install

# Scrape all products, consolidate, convert to JSON
npm run scrape

# Start dev server
npm run dev
```

## Project Structure

```
apple-store-scrape/
├── scraper_base.py              # Shared scraping framework (REGIONS, extraction, merge)
├── iphone.py                    # iPhone scraper
├── ipad.py                      # iPad scraper
├── mac.py                       # Mac scraper (with spec extraction)
├── watch.py                     # Apple Watch scraper
├── airpods.py                   # AirPods scraper
├── tvhome.py                    # Apple TV & HomePod scraper
├── smart_consolidate_colors.py  # Color variant consolidation
├── convert_to_json.py           # CSV → JSON + exchange rate
├── test_scrapers.py             # Test suite
├── src/                         # Frontend source
│   ├── index.html
│   ├── js/main.js
│   ├── scss/
│   └── data/                    # Generated JSON (not committed)
├── .github/workflows/           # GitHub Actions CI/CD
├── e2e/                         # Playwright E2E tests
├── CLAUDE.md                    # AI development guide
└── TECHNICAL_SPEC.md            # Detailed technical specification
```

## How It Works

### Architecture

All 6 scrapers inherit from a shared framework (`scraper_base.py`) that handles:
- Region configuration, rate limiting, and error handling
- Dual-strategy product extraction (metrics JSON + bootstrap JS)
- Cross-region merge with automatic alignment reporting
- Dynamic model discovery from Apple's landing pages

### Data Pipeline

```
Apple Store pages (US/TW)
  ↓  python3 iphone.py / ipad.py / mac.py / watch.py / airpods.py / tvhome.py
Per-product CSV files (*_products_merged.csv)
  ↓  python3 smart_consolidate_colors.py
Consolidated CSVs (*_products_consolidated.csv)
  ↓  python3 convert_to_json.py
JSON files in src/data/
  ↓  npm run build
Static site in dist/ → GitHub Pages
```

### Cross-Region Matching

Apple uses **different part numbers per region** for the same product, so SKU matching doesn't work. Instead:

- **Metrics products** (iPhone, iPad, TV/Home): matched by product `Name` (identical across regions)
- **Bootstrap products** (Mac, Watch, AirPods): matched by `ConfigKey` — a configuration identifier (e.g. `m4-10-10`) shared across regions

## Commands

| Command | Description |
|---------|-------------|
| `npm run scrape` | Full pipeline: scrape → consolidate → convert |
| `npm run dev` | Start Vite dev server |
| `npm run build` | Production build |
| `npm run test` | Full Python test suite |
| `SKIP_NETWORK_TESTS=1 python3 test_scrapers.py` | Quick tests (no network) |
| `npm run test:e2e` | Playwright E2E tests |

## Configuration

All scrapers share the region config in `scraper_base.py`:

```python
REGIONS = {
    "": ["US", "USD", "en-us", "$"],
    "tw": ["TW", "TWD", "zh-tw", "NT$"],
}
```

To add a region, update this single dict — all scrapers pick it up automatically.

## Extending

### Add a new product category

1. Create a scraper class inheriting from `AppleStoreScraper`
2. Implement `get_models()` and `build_product_url()`
3. Add to `smart_consolidate_colors.py`, `convert_to_json.py`, and the GitHub Actions workflow
4. Add tests

See `TECHNICAL_SPEC.md` for detailed architecture documentation.

## Disclaimer

This project is for personal research and comparison only. It is not affiliated with Apple Inc. Please respect Apple's terms of service and avoid excessive requests. The scrapers enforce a 1-second delay between requests.
