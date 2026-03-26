"""
iPad scraper — fetches iPad product data from Apple Store across regions.
"""

from scraper_base import (
    AppleStoreScraper, REGIONS, REFERENCE_REGION,
    discover_models, debug_print,
)


class IPadScraper(AppleStoreScraper):
    product_name = "iPad"
    output_file = "ipad_products_merged.csv"

    # Last-resort fallback — only used if Apple's website is completely unreachable.
    DEFAULT_MODELS = ["ipad-pro", "ipad-air", "ipad", "ipad-mini"]

    def get_models(self):
        all_models = set()
        for region_code in REGIONS:
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/shop/buy-ipad"
            models = discover_models(
                region_code, url,
                link_pattern='/shop/buy-ipad/',
                default_models=self.DEFAULT_MODELS,
            )
            # Filter to valid iPad models
            for m in models:
                if m.startswith('ipad-') or m == 'ipad':
                    all_models.add(m)
        return list(all_models)

    def build_product_url(self, model, region_code):
        region_prefix = f"/{region_code}" if region_code else ""
        return f"https://www.apple.com{region_prefix}/shop/buy-ipad/{model}"


def get_available_models(region_code=""):
    """Backward-compatible function for tests."""
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/shop/buy-ipad"
    return discover_models(
        region_code, url,
        link_pattern='/shop/buy-ipad/',
        default_models=IPadScraper.DEFAULT_MODELS,
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
    scraper = IPadScraper()
    scraper.run()


if __name__ == "__main__":
    main()
