# Apple Store Scraper

A tool for comparing Apple product prices across regions (US and Taiwan). Scrapes all major Apple product categories, consolidates color variants, and serves a responsive comparison website.

**Live Demo**: [https://jonatw.github.io/apple-store-scrape/](https://jonatw.github.io/apple-store-scrape/)

## Features

- Scrapes **all Apple product categories**: iPhone, iPad, Mac, Apple Watch, AirPods, Apple TV, HomePod
- Dynamic model discovery — automatically detects current products from Apple's website
- Cross-region price matching with dual-strategy extraction (metrics JSON + bootstrap JS)
- Smart color variant consolidation — merges identical products differing only by color
- Parallel scraping — all 6 product categories run concurrently
- Automatic USD/TWD exchange rate fetching from Cathay Bank
- Daily automated updates via GitHub Actions
- Responsive web interface — mobile-friendly table (no horizontal scroll), dark mode, search

## Requirements

- Python 3.13+
- Node.js 24+

## Quick Start

```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
npm install

# Scrape all products (parallel), consolidate, convert to JSON
npm run scrape

# Start dev server
npm run dev
```

## Project Structure

```
apple-store-scrape/
├── scraper_base.py              # Shared scraping framework (REGIONS, extraction, merge)
├── run_pipeline.py              # Parallel pipeline runner (used by CI and npm run scrape)
├── iphone.py                    # iPhone scraper
├── ipad.py                      # iPad scraper
├── mac.py                       # Mac scraper (with spec extraction)
├── watch.py                     # Apple Watch scraper
├── airpods.py                   # AirPods scraper
├── tvhome.py                    # Apple TV & HomePod scraper
├── smart_consolidate_colors.py  # Color variant consolidation
├── convert_to_json.py           # CSV → JSON + exchange rate
├── test_scrapers.py             # Test suite (39 tests)
├── src/                         # Frontend source
│   ├── index.html
│   ├── js/main.js
│   └── data/                    # Generated JSON (not committed)
├── .github/workflows/           # GitHub Actions CI/CD
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

`run_pipeline.py` orchestrates the full pipeline — runs all scrapers in parallel
via `ThreadPoolExecutor`, then sequential post-processing (consolidation + JSON).

### Data Pipeline

```
Apple Store pages (US/TW)
  ↓  run_pipeline.py (6 scrapers in parallel)
Per-product CSV files (*_products_merged.csv)
  ↓  smart_consolidate_colors.py
Consolidated CSVs (*_products_consolidated.csv)
  ↓  convert_to_json.py
JSON files in src/data/
  ↓  npm run build
Static site in dist/ → GitHub Pages
```

### Cross-Region Matching

Apple uses **different part numbers per region** for the same product, so SKU matching doesn't work. Instead:

- **Metrics products** (iPhone, iPad, TV/Home): matched by product `Name` (identical across regions)
- **Bootstrap products** (Mac, Watch, AirPods): matched by `ConfigKey` — a configuration identifier (e.g. `m4-10-10`) shared across regions

### Frontend

- Mobile: 4-column table (Product, US, TW, Diff) — no horizontal scrolling
- Desktop: 6-column table (adds US+Fee and Recommendation columns)
- Colors not displayed (they don't affect price); Mac specs shown
- Dark/light theme with system preference detection

## Commands

| Command | Description |
|---------|-------------|
| `npm run scrape` | Full pipeline: parallel scrape → consolidate → convert |
| `npm run dev` | Start Vite dev server |
| `npm run build` | Production build |
| `npm run test` | Full Python test suite |
| `SKIP_NETWORK_TESTS=1 python3 test_scrapers.py` | Quick tests (no network) |
| `SCRAPER_DEBUG=1 python3 iphone.py` | Run single scraper with verbose output |

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
3. Add to `run_pipeline.py`, `smart_consolidate_colors.py`, `convert_to_json.py`
4. Add tests

See `TECHNICAL_SPEC.md` for detailed architecture documentation.

## Disclaimer

This project is for personal research and comparison only. It is not affiliated with Apple Inc. Please respect Apple's terms of service and avoid excessive requests. The scrapers enforce a 1-second delay between requests.
