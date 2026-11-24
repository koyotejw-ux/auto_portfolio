import time
import os
from playwright.sync_api import sync_playwright

output_dir = r"d:\097.flutter_project\auto_portfolio\mes_solution\mockups"
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    print("1. Navigating to landing page...")
    page.goto("http://127.0.0.1:4173", wait_until="networkidle")
    time.sleep(1)
    page.screenshot(path=os.path.join(output_dir, "screen_01_landing.png"))
    print("Saved screen_01_landing.png")

    # Enter Demo mode
    demo_btn = page.locator("text=데모 체험하기").first
    if demo_btn.is_visible():
        demo_btn.click()
        time.sleep(1.5)
    else:
        # Fallback to any button with 데모
        for b in page.locator("button").all():
            if "데모" in b.inner_text():
                b.click()
                time.sleep(1.5)
                break

    # 2. Executive / Main Dashboard
    page.screenshot(path=os.path.join(output_dir, "screen_02_dashboard.png"))
    print("Saved screen_02_dashboard.png")

    # 3. Production Management (생산관리)
    try:
        page.locator("text=생산관리").first.click()
        time.sleep(1.2)
        page.screenshot(path=os.path.join(output_dir, "screen_03_production.png"))
        print("Saved screen_03_production.png")
    except Exception as e:
        print("Failed to capture production:", e)

    # 4. Quality Management (품질관리)
    try:
        page.locator("text=품질관리").first.click()
        time.sleep(1.2)
        page.screenshot(path=os.path.join(output_dir, "screen_04_quality.png"))
        print("Saved screen_04_quality.png")
    except Exception as e:
        print("Failed to capture quality:", e)

    # 5. Inventory / Material Management (자재관리 or 재고관리)
    try:
        if page.locator("text=자재관리").count() > 0:
            page.locator("text=자재관리").first.click()
        else:
            page.locator("text=재고관리").first.click()
        time.sleep(1.2)
        page.screenshot(path=os.path.join(output_dir, "screen_05_inventory.png"))
        print("Saved screen_05_inventory.png")
    except Exception as e:
        print("Failed to capture inventory:", e)

    # 6. Master Data Management (기준정보 관리)
    try:
        page.locator("text=기준정보 관리").first.click()
        time.sleep(1.2)
        page.screenshot(path=os.path.join(output_dir, "screen_06_master.png"))
        print("Saved screen_06_master.png")
    except Exception as e:
        print("Failed to capture master data:", e)

    browser.close()
    print("Capture process completed!")

