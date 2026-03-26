"""
Mac scraper — fetches Mac product data from Apple Store across regions.

Mac products include spec columns (Chip, CPU_Cores, GPU_Cores, etc.)
extracted from HTML dimension elements on the product page.
"""

import re
from scraper_base import (
    AppleStoreScraper, REGIONS, REFERENCE_REGION,
    discover_models, debug_print,
)


# ==================== MAC-SPECIFIC SPEC EXTRACTION ====================

def extract_specs_from_text(text):
    """Extract detailed specifications from configuration text."""
    specs = {
        'chip': '',
        'cpu_cores': '',
        'gpu_cores': '',
        'neural_engine': '',
        'memory': '',
        'storage': '',
    }
    if not text:
        return specs

    text_lower = text.lower()

    # Chip (M1/M2/M3/M4 with optional Pro/Max/Ultra)
    for pattern in [
        r'apple\s+(m[1-9](?:\s+(?:pro|max|ultra))?)\s+chip',
        r'(m[1-9](?:\s+(?:pro|max|ultra))?)\s+chip',
    ]:
        match = re.search(pattern, text_lower)
        if match:
            specs['chip'] = match.group(1).upper().replace('  ', ' ')
            break

    # CPU cores
    cpu_match = re.search(r'(\d+)-core\s+cpu', text_lower)
    if cpu_match:
        specs['cpu_cores'] = cpu_match.group(1)

    # GPU cores
    gpu_match = re.search(r'(\d+)-core\s+gpu', text_lower)
    if gpu_match:
        specs['gpu_cores'] = gpu_match.group(1)

    # Neural Engine
    neural_match = re.search(r'(\d+)-core\s+neural\s+engine', text_lower)
    if neural_match:
        specs['neural_engine'] = neural_match.group(1)

    # Memory
    for pattern in [r'(\d+)gb\s+(?:unified\s+)?memory', r'(\d+)gb\s+memory', r'memory[:\s]*(\d+)gb']:
        match = re.search(pattern, text_lower)
        if match:
            specs['memory'] = f"{match.group(1)}GB"
            break

    # Storage
    for pattern in [r'(\d+)(gb|tb)\s+storage', r'storage[:\s]*(\d+)(gb|tb)']:
        match = re.search(pattern, text_lower)
        if match:
            amount = match.group(1)
            unit = match.group(2).upper()
            specs['storage'] = f"{amount}{unit}"
            break

    return specs


def extract_spec_variants_from_page(soup):
    """Extract spec variants from HTML dimension elements on a Mac product page."""
    config_texts = []
    dimension_elements = soup.find_all(attrs={'class': re.compile(r'.*dimension.*', re.I)})

    for elem in dimension_elements:
        text = elem.get_text(strip=True)
        if ('chip' in text.lower() or 'processor' in text.lower()) and len(text) > 30:
            clean_text = re.sub(r'(blue|purple|pink|orange|yellow|green|silver)+', '', text, flags=re.IGNORECASE)
            clean_text = re.sub(r'select a finish', '', clean_text, flags=re.IGNORECASE)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            if clean_text not in config_texts:
                config_texts.append(clean_text)
                debug_print(f"Found config: {clean_text}")

    spec_variants = []
    for config_text in config_texts:
        specs = extract_specs_from_text(config_text)
        if any(specs.values()):
            spec_variants.append(specs)

    return spec_variants


def assign_specs_to_products(products, spec_variants):
    """
    Assign spec variants to products by matching price tiers.

    Sorts products by price ascending and spec variants by
    storage > memory > CPU value ascending, then pairs them.
    """
    empty_specs = {'chip': '', 'cpu_cores': '', 'gpu_cores': '', 'neural_engine': '', 'memory': '', 'storage': ''}

    if not spec_variants:
        for p in products:
            p.update(empty_specs)
        return products

    # Group by price
    products_by_price = {}
    for p in products:
        price = p.get('Price', 0) or 0
        products_by_price.setdefault(price, []).append(p)

    sorted_prices = sorted(products_by_price.keys())

    def spec_sort_key(specs):
        storage = 0
        s = specs.get('storage', '')
        if s:
            num = re.sub(r'[^\d]', '', s.split('GB')[0].split('TB')[0])
            storage = int(num) if num else 0
            if 'TB' in s:
                storage *= 1000
        memory = int(re.sub(r'[^\d]', '', specs.get('memory', '')) or 0)
        cpu = int(specs.get('cpu_cores', '') or 0)
        return (storage, memory, cpu)

    sorted_specs = sorted(spec_variants, key=spec_sort_key)

    result = []
    for i, price in enumerate(sorted_prices):
        assigned = sorted_specs[i] if i < len(sorted_specs) else sorted_specs[-1]
        for product in products_by_price[price]:
            product.update(assigned)
            result.append(product)

    return result


# ==================== MAC SCRAPER ====================

class MacScraper(AppleStoreScraper):
    product_name = "Mac"
    output_file = "mac_products_merged.csv"
    extra_columns = ['Chip', 'CPU_Cores', 'GPU_Cores', 'Neural_Engine', 'Memory', 'Storage']

    # Last-resort fallback — only used if Apple's website is completely unreachable.
    DEFAULT_MODELS = ["mac-mini", "imac", "mac-studio", "macbook-air", "macbook-pro"]

    # Slugs that appear in /shop/buy-mac/ links but are not Mac computers
    NON_PRODUCT_SLUGS = {'compare', 'accessories', 'help', 'financing',
                         'studio-display', 'studio-display-xdr', 'pro-display-xdr'}

    def get_models(self):
        # Only discover from US to avoid duplicates
        url = "https://www.apple.com/shop/buy-mac"
        models = discover_models(
            "", url,
            link_pattern='/shop/buy-mac/',
            default_models=self.DEFAULT_MODELS,
        )
        # Filter out non-computer products (displays, accessories, etc.)
        filtered = [m for m in models if m not in self.NON_PRODUCT_SLUGS
                     and not any(x in m for x in ('display', 'accessories', 'compare', 'help'))]
        return filtered if filtered else self.DEFAULT_MODELS

    def build_product_url(self, model, region_code):
        region_prefix = f"/{region_code}" if region_code else ""
        return f"https://www.apple.com{region_prefix}/shop/buy-mac/{model}"

    def post_process_products(self, products, soup):
        """Enrich products with spec data extracted from the page."""
        spec_variants = extract_spec_variants_from_page(soup)
        debug_print(f"Extracted {len(spec_variants)} spec variants from HTML")

        if spec_variants:
            products = assign_specs_to_products(products, spec_variants)
        else:
            empty = {'Chip': '', 'CPU_Cores': '', 'GPU_Cores': '', 'Neural_Engine': '', 'Memory': '', 'Storage': ''}
            for p in products:
                for k, v in empty.items():
                    p.setdefault(k, v)

        # Normalize key names for merge (specs use lowercase keys from extraction)
        key_map = {
            'chip': 'Chip', 'cpu_cores': 'CPU_Cores', 'gpu_cores': 'GPU_Cores',
            'neural_engine': 'Neural_Engine', 'memory': 'Memory', 'storage': 'Storage',
        }
        for p in products:
            for old, new in key_map.items():
                if old in p:
                    p[new] = p.pop(old)
        return products


def get_available_models(region_code=""):
    """Backward-compatible function for tests."""
    url = "https://www.apple.com/shop/buy-mac"
    return discover_models(
        "", url,
        link_pattern='/shop/buy-mac/',
        default_models=MacScraper.DEFAULT_MODELS,
    )


def extract_product_details(url, region_code=""):
    """Backward-compatible function for tests."""
    from scraper_base import fetch_product_page
    return fetch_product_page(url, region_code)


def merge_product_data(product_data):
    """Backward-compatible function for tests."""
    from scraper_base import merge_product_data as _merge
    return _merge(product_data, extra_columns=MacScraper.extra_columns)


def main():
    scraper = MacScraper()
    scraper.run()


if __name__ == "__main__":
    main()
