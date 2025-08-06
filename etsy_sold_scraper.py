from playwright.sync_api import sync_playwright
import os, time

SHOP_NAME = os.getenv("SHOP_NAME", "TheStyledSquare")
WAIT_BETWEEN_PAGES = int(os.getenv("WAIT_SECONDS", 5))

output_folder = f"{SHOP_NAME}_sold"
os.makedirs(output_folder, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page_num = 1
    while True:
        url = f"https://www.etsy.com/shop/{SHOP_NAME}/sold?page={page_num}"
        print(f"Opening: {url}")
        page.goto(url, timeout=30000)
        time.sleep(WAIT_BETWEEN_PAGES)

        content = page.content()
        if "We couldn’t find any results" in content or "/search?q=" in page.url:
            print("✅ No more sold pages.")
            break

        screenshot_path = os.path.join(output_folder, f"sold_page_{page_num}.png")
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Saved → {screenshot_path}")
        page_num += 1

    browser.close()
