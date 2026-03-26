"""
Apple TV & HomePod scraper — fetches TV and Home product data from Apple Store.

This scraper handles two product categories (TV and HomePod) that live
under different buy URLs but are combined into a single output file.
"""

from scraper_base import (
    AppleStoreScraper, REGIONS, debug_print, REQUEST_DELAY,
    extract_products_from_metrics, extract_products_from_bootstrap,
)
import requests
from bs4 import BeautifulSoup
import time


class TVHomeScraper(AppleStoreScraper):
    product_name = "Apple TV & Home"
    output_file = "tvhome_products_merged.csv"

    DEFAULT_TV_MODELS = ['apple-tv-4k']
    DEFAULT_HOMEPOD_MODELS = ['homepod', 'homepod-mini']

    def get_models(self):
        """Not used directly — see fetch_all_products override."""
        return []

    def build_product_url(self, model, region_code):
        """Not used directly — see fetch_all_products override."""
        return ""

    def _discover_all_models(self):
        """Discover TV and HomePod models from all regions."""
        tv_models = set()
        homepod_models = set()

        for region_code in REGIONS:
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/tv-home/"

            try:
                response = requests.get(url, timeout=30)
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    if '/shop/goto/buy_tv/' in href:
                        parts = href.split('buy_tv/')
                        if len(parts) > 1:
                            model = parts[1].split('?')[0].split('#')[0].replace('_', '-')
                            if model:
                                tv_models.add(model)
                    elif '/shop/goto/buy_homepod/' in href:
                        parts = href.split('buy_homepod/')
                        if len(parts) > 1:
                            model = parts[1].split('?')[0].split('#')[0].replace('_', '-')
                            if model:
                                homepod_models.add(model)

            except Exception as e:
                debug_print(f"Error accessing {url}: {e}")

        return (
            list(tv_models) if tv_models else self.DEFAULT_TV_MODELS,
            list(homepod_models) if homepod_models else self.DEFAULT_HOMEPOD_MODELS,
        )

    def fetch_all_products(self):
        """Override to handle two product categories with different URL patterns."""
        tv_models, homepod_models = self._discover_all_models()
        debug_print(f"TV models: {', '.join(tv_models)}")
        debug_print(f"HomePod models: {', '.join(homepod_models)}")

        all_products = []

        # Fetch TV products
        for model in tv_models:
            for region_code in REGIONS:
                region_prefix = f"/{region_code}" if region_code else ""
                url = f"https://www.apple.com{region_prefix}/shop/buy-tv/{model}"
                all_products.extend(self._fetch_url(url, region_code))

        # Fetch HomePod products
        for model in homepod_models:
            for region_code in REGIONS:
                region_prefix = f"/{region_code}" if region_code else ""
                url = f"https://www.apple.com{region_prefix}/shop/buy-homepod/{model}"
                all_products.extend(self._fetch_url(url, region_code))

        return all_products

    def _fetch_url(self, url, region_code):
        """Fetch products from a single URL using the shared dual strategy."""
        time.sleep(REQUEST_DELAY)
        region_display = REGIONS.get(region_code, ["Unknown"])[0]
        debug_print(f"Fetching products from {url} for region {region_display}")

        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                debug_print(f"Failed to retrieve {url}. Status code: {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            products = extract_products_from_metrics(soup, region_code)
            if not products:
                debug_print("Metrics found no products, trying bootstrap")
                products = extract_products_from_bootstrap(soup, region_code)

            return products

        except Exception as e:
            debug_print(f"Error fetching {url}: {e}")
            return []


def get_available_models(region_code=""):
    """Backward-compatible function for tests."""
    scraper = TVHomeScraper()
    return scraper._discover_all_models()


def extract_product_details(url, region_code=""):
    """Backward-compatible function for tests."""
    from scraper_base import fetch_product_page
    return fetch_product_page(url, region_code)


def merge_product_data(product_data):
    """Backward-compatible function for tests."""
    from scraper_base import merge_product_data as _merge
    return _merge(product_data)


def main():
    scraper = TVHomeScraper()
    scraper.run()


if __name__ == "__main__":
    main()
