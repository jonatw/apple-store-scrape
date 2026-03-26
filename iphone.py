"""
iPhone scraper — fetches iPhone product data from Apple Store across regions.
"""

from scraper_base import (
    AppleStoreScraper, REGIONS, REFERENCE_REGION,
    discover_models, debug_print,
)


class IPhoneScraper(AppleStoreScraper):
    product_name = "iPhone"
    output_file = "iphone_products_merged.csv"

    # Last-resort fallback — only used if Apple's website is completely unreachable.
    DEFAULT_MODELS = ["iphone-17-pro", "iphone-17", "iphone-air", "iphone-16e", "iphone-16"]

    def get_models(self):
        all_models = set()
        for region_code in REGIONS:
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/shop/buy-iphone"
            models = discover_models(
                region_code, url,
                link_pattern='/shop/buy-iphone/',
                default_models=self.DEFAULT_MODELS,
            )
            all_models.update(models)
        # Filter: only keep links that look like iPhone product slugs
        return [m for m in all_models if m.startswith('iphone')]

    def build_product_url(self, model, region_code):
        region_prefix = f"/{region_code}" if region_code else ""
        return f"https://www.apple.com{region_prefix}/shop/buy-iphone/{model}"


def get_available_models(region_code=""):
    """Backward-compatible function for tests."""
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/shop/buy-iphone"
    return discover_models(
        region_code, url,
        link_pattern='/shop/buy-iphone/',
        default_models=IPhoneScraper.DEFAULT_MODELS,
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
    scraper = IPhoneScraper()
    scraper.run()


if __name__ == "__main__":
    main()
