"""
Apple Watch scraper — fetches Watch product data from Apple Store across regions.

Watch pages often use the bootstrap strategy with dimension-based names
(case size, material). This scraper enriches product names from bootstrap
dimension data when available.
"""

from scraper_base import (
    AppleStoreScraper, REGIONS, REFERENCE_REGION,
    discover_models_from_goto, extract_products_from_metrics,
    extract_products_from_bootstrap, debug_print, REQUEST_DELAY,
)
import requests
from bs4 import BeautifulSoup
import time


class WatchScraper(AppleStoreScraper):
    product_name = "Apple Watch"
    output_file = "watch_products_merged.csv"

    # Last-resort fallback — only used if Apple's website is completely unreachable.
    DEFAULT_MODELS = ["apple-watch-series-11", "apple-watch-se", "apple-watch-ultra-3"]

    def get_models(self):
        all_models = set()
        for region_code in REGIONS:
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/watch/"
            models = discover_models_from_goto(
                region_code, url,
                goto_pattern='/shop/goto/buy_watch/',
                default_models=self.DEFAULT_MODELS,
            )
            # Keep discovered names as-is (e.g. apple-watch-series-11, apple-watch-ultra-3)
            all_models.update(models)
        return list(all_models)

    def build_product_url(self, model, region_code):
        region_prefix = f"/{region_code}" if region_code else ""
        return f"https://www.apple.com{region_prefix}/shop/buy-watch/{model}"

    def post_process_products(self, products, soup):
        """Enrich Watch product names with case size and material from bootstrap dimensions."""
        for p in products:
            bp = p.get('_bootstrap_product')
            if not bp:
                continue
            dimensions = bp.get('dimensions', {})
            case_size = dimensions.get('watch_cases-dimensionCaseSize', '')
            case_material = dimensions.get('watch_cases-dimensionCaseMaterial', '')
            if case_size or case_material:
                name = p.get('Name', '')
                p['Name'] = f"{name} {case_size} {case_material}".strip()
        return products


def get_available_models(region_code=""):
    """Backward-compatible function for tests."""
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/watch/"
    return discover_models_from_goto(
        region_code, url,
        goto_pattern='/shop/goto/buy_watch/',
        default_models=WatchScraper.DEFAULT_MODELS,
    )


def extract_product_details(url, region_code=""):
    """Backward-compatible function for tests."""
    from scraper_base import fetch_product_page
    return fetch_product_page(url, region_code)


def merge_product_data(product_data):
    """Backward-compatible function for tests."""
    from scraper_base import merge_product_data as _merge
    return _merge(product_data)


def main():
    scraper = WatchScraper()
    scraper.run()


if __name__ == "__main__":
    main()
