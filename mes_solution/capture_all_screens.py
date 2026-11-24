import os
import time
import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from playwright.sync_api import sync_playwright

BUILD_DIR = r"D:\102_1.codebridgex\MES Solution Website Structure 251030\build"
OUTPUT_DIR = r"d:\097.flutter_project\auto_portfolio\mes_solution\mockups"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BUILD_DIR, **kwargs)

def start_server():
    try:
        with TCPServer(("127.0.0.1", 4173), Handler) as httpd:
            print("Server running on port 4173...")
            httpd.serve_forever()
    except Exception as e:
        print("Server startup (or already running):", e)

t = threading.Thread(target=start_server, daemon=True)
t.start()
time.sleep(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    print("1. Capturing Landing Page...")
    page.goto("http://127.0.0.1:4173", wait_until="networkidle")
    time.sleep(1)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "screen_01_landing.png"))
    print("Saved screen_01_landing.png")

    # Click '대시보드로 이동' directly
    print("Navigating directly to Dashboard...")
    dash_btn = page.locator("text=대시보드로 이동").first
    if dash_btn.is_visible():
        dash_btn.click()
    else:
        page.locator("button:has-text('대시보드')").first.click()
    time.sleep(2)

    # 2. Executive / Main Dashboard
    page.screenshot(path=os.path.join(OUTPUT_DIR, "screen_02_dashboard.png"))
    print("Saved screen_02_dashboard.png")

    # Helper function to click sidebar items
    def click_sidebar(text_label):
        print(f"Trying to click sidebar: {text_label}")
        elem = page.locator(f"button:has-text('{text_label}')").first
        if elem.is_visible():
            elem.click()
            time.sleep(1.2)
            return True
        return False

    # 3. Production Management (생산관리)
    if click_sidebar("생산관리"):
        page.screenshot(path=os.path.join(OUTPUT_DIR, "screen_03_production.png"))
        print("Saved screen_03_production.png")

    # 4. Quality Management (품질관리)
    if click_sidebar("품질관리"):
        page.screenshot(path=os.path.join(OUTPUT_DIR, "screen_04_quality.png"))
        print("Saved screen_04_quality.png")

    # 5. Inventory / Material Management (자재관리 / 재고관리)
    if click_sidebar("자재관리") or click_sidebar("재고관리"):
        page.screenshot(path=os.path.join(OUTPUT_DIR, "screen_05_inventory.png"))
        print("Saved screen_05_inventory.png")

    # 6. Master Data / System Settings (기준정보 관리)
    if click_sidebar("기준정보 관리") or click_sidebar("기준정보"):
        page.screenshot(path=os.path.join(OUTPUT_DIR, "screen_06_master.png"))
        print("Saved screen_06_master.png")

    browser.close()
    print("All captures completed successfully!")
