"""
AirPods scraper — fetches AirPods product data from Apple Store across regions.
"""

from scraper_base import (
    AppleStoreScraper, REGIONS, discover_models_from_goto,
)


class AirPodsScraper(AppleStoreScraper):
    product_name = "AirPods"
    output_file = "airpods_products_merged.csv"

    # Last-resort fallback — only used if Apple's website is completely unreachable.
    DEFAULT_MODELS = ["airpods-4", "airpods-pro-3", "airpods-max-2"]

    def get_models(self):
        all_models = set()
        for region_code in REGIONS:
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/airpods/"
            models = discover_models_from_goto(
                region_code, url,
                goto_pattern='/shop/goto/buy_airpods/',
                default_models=self.DEFAULT_MODELS,
            )
            all_models.update(models)
        return list(all_models)

    def build_product_url(self, model, region_code):
        region_prefix = f"/{region_code}" if region_code else ""
        return f"https://www.apple.com{region_prefix}/shop/buy-airpods/{model}"


def get_available_models(region_code=""):
    """Backward-compatible function for tests."""
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/airpods/"
    return discover_models_from_goto(
        region_code, url,
        goto_pattern='/shop/goto/buy_airpods/',
        default_models=AirPodsScraper.DEFAULT_MODELS,
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
    scraper = AirPodsScraper()
    scraper.run()


if __name__ == "__main__":
    main()
