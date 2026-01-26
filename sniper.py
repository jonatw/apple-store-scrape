import asyncio
from playwright.async_api import async_playwright
import json
import re

async def fetch_price(page, region, url, steps):
    print(f"[{region}] Navigating to {url}...")
    await page.goto(url)
    
    # Wait for initial load
    await page.wait_for_selector('h1', timeout=30000)

    # DEBUG: Take screenshot
    await page.screenshot(path=f"debug_{region}.png")
    
    # DEBUG: Inspect inputs
    inputs = await page.locator('input[type="radio"]').all()
    print(f"[{region}] Found {len(inputs)} radio inputs:")
    for i in inputs:
        val = await i.get_attribute("value")
        print(f"  - {val}")

    for step_name, selector in steps.items():
        print(f"[{region}] Action: {step_name}")
        try:
            # Check if selector is a text locator or css
            if selector.startswith("text="):
                await page.click(selector)
            else:
                # Use locator with strict mode disabled to allow fuzzy matching if needed, 
                # or better specific selectors. For now simple click.
                # Apple often uses radio buttons hidden behind labels.
                # We try to click the label containing specific text or ID.
                await page.click(selector)
            
            # Small pause for reactivity
            await page.wait_for_timeout(500)
            
        except Exception as e:
            print(f"[{region}] ❌ Failed at step '{step_name}': {e}")
            # Optional screenshot for debug
            # await page.screenshot(path=f"debug_{region}_{step_name}.png")
            return None

    # Wait for price to update
    await page.wait_for_timeout(2000)

    # Extract Price
    # Apple usually puts the final price in specific localized class or sticky footer
    # Generic strategy: look for the price element
    try:
        # This selector is tricky and changes.
        # Often it is in data-autom="full-price" or similar
        price_el = await page.wait_for_selector('[data-autom="full-price"]', timeout=5000)
        price_text = await price_el.inner_text()
        print(f"[{region}] ✅ Found Price: {price_text}")
        return price_text
    except:
        print(f"[{region}] ⚠️ Price selector failed, dumping all text with currency symbol...")
        content = await page.content()
        # Fallback regex search
        return "Not Found"

async def run():
    async with async_playwright() as p:
        # Launch Firefox
        browser = await p.firefox.launch(
            headless=True,
            args=[]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/Los_Angeles'
        )
        
        page = await context.new_page()
        
        # Inject stealth JS
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        # --- US CONFIG (Anchorage 99501 is tax logic, but base price is same) ---
        us_steps = {
            "Select Model (Pro)": 'input[value="iphone-16-pro"] + label', # Select Pro (not Max)
            "Select Color (Desert)": 'input[value="deserttitanium"] + label',
            "Select Storage (256GB)": 'input[value="256gb"] + label',
            "No Trade-in": 'input[value="no_tradein"] + label',
            "Payment (Buy)": 'input[value="full_price"] + label', # "Buy" option
            "Carrier (Unlocked)": 'input[value="unlocked"] + label' # Connect to any carrier later
        }
        
        us_price = await fetch_price(
            page, 
            "US", 
            "https://www.apple.com/shop/buy-iphone/iphone-16-pro",
            us_steps
        )

        # --- TW CONFIG ---
        tw_steps = {
             "Select Model (Pro)": 'input[value="iphone-16-pro"] + label',
             "Select Color (Desert)": 'input[value="deserttitanium"] + label',
             "Select Storage (256GB)": 'input[value="256gb"] + label',
             "No Trade-in": 'input[value="no_tradein"] + label'
             # TW has no carrier selection step usually
        }

        tw_price = await fetch_price(
            page,
            "TW",
            "https://www.apple.com/tw/shop/buy-iphone/iphone-16-pro",
            tw_steps
        )

        print("\n--- REPORT ---")
        print(f"US Price (Unlocked): {us_price}")
        print(f"TW Price: {tw_price}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
