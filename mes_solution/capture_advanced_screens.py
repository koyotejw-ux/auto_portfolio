import os
import time
import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from playwright.sync_api import sync_playwright

BUILD_251030 = r"D:\102_1.codebridgex\MES Solution Website Structure 251030\build"
BUILD_251229 = r"D:\102_1.codebridgex\MES Solution Website Structure 251229\build"

MOCKUP_DIR = r"d:\097.flutter_project\auto_portfolio\mes_solution\mockups"
os.makedirs(MOCKUP_DIR, exist_ok=True)

class Handler251030(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BUILD_251030, **kwargs)

class Handler251229(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BUILD_251229, **kwargs)

def start_server_251030():
    try:
        with TCPServer(("127.0.0.1", 4173), Handler251030) as httpd:
            print("Server 251030 running on port 4173...")
            httpd.serve_forever()
    except Exception as e:
        print("Server 4173 exception:", e)

def start_server_251229():
    try:
        with TCPServer(("127.0.0.1", 4174), Handler251229) as httpd:
            print("Server 251229 running on port 4174...")
            httpd.serve_forever()
    except Exception as e:
        print("Server 4174 exception:", e)

t1 = threading.Thread(target=start_server_251030, daemon=True)
t1.start()
t2 = threading.Thread(target=start_server_251229, daemon=True)
t2.start()
time.sleep(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # --- Part 1: Capture 251030 Desktop (Dark Mode & Light Mode) ---
    context_desktop = browser.new_context(viewport={"width": 1920, "height": 1080})
    page_desktop = context_desktop.new_page()
    page_desktop.goto("http://127.0.0.1:4173", wait_until="networkidle")
    time.sleep(1)
    
    # Enter Demo
    page_desktop.locator("text=대시보드로 이동").first.click()
    time.sleep(1.5)
    
    # Turn ON Dark Mode: evaluate document.documentElement.className = 'dark'
    page_desktop.evaluate("() => { document.documentElement.className = 'dark'; document.documentElement.classList.add('dark'); }")
    time.sleep(1)
    page_desktop.screenshot(path=os.path.join(MOCKUP_DIR, "screen_02_dashboard_dark.png"))
    print("Saved screen_02_dashboard_dark.png")

    # Dark Production
    page_desktop.locator("button:has-text('생산관리')").first.click()
    time.sleep(1)
    page_desktop.screenshot(path=os.path.join(MOCKUP_DIR, "screen_03_production_dark.png"))
    print("Saved screen_03_production_dark.png")

    # Dark Quality
    page_desktop.locator("button:has-text('품질관리')").first.click()
    time.sleep(1)
    page_desktop.screenshot(path=os.path.join(MOCKUP_DIR, "screen_04_quality_dark.png"))
    print("Saved screen_04_quality_dark.png")

    # Dark Inventory
    try:
        page_desktop.locator("button:has-text('자재관리')").first.click()
    except:
        page_desktop.locator("button:has-text('재고관리')").first.click()
    time.sleep(1)
    page_desktop.screenshot(path=os.path.join(MOCKUP_DIR, "screen_05_inventory_dark.png"))
    print("Saved screen_05_inventory_dark.png")

    # --- Part 2: Capture Mobile Viewport (390 x 844 iPhone style) ---
    context_mobile = browser.new_context(viewport={"width": 412, "height": 915}, is_mobile=True)
    page_mobile = context_mobile.new_page()
    page_mobile.goto("http://127.0.0.1:4173", wait_until="networkidle")
    time.sleep(1)
    page_mobile.locator("text=대시보드로 이동").first.click()
    time.sleep(1.5)
    page_mobile.screenshot(path=os.path.join(MOCKUP_DIR, "screen_mobile_dashboard.png"))
    print("Saved screen_mobile_dashboard.png")

    # --- Part 3: Capture Tablet Viewport (820 x 1180 iPad style) ---
    context_tablet = browser.new_context(viewport={"width": 820, "height": 1180})
    page_tablet = context_tablet.new_page()
    page_tablet.goto("http://127.0.0.1:4173", wait_until="networkidle")
    time.sleep(1)
    page_tablet.locator("text=대시보드로 이동").first.click()
    time.sleep(1.5)
    page_tablet.screenshot(path=os.path.join(MOCKUP_DIR, "screen_tablet_dashboard.png"))
    print("Saved screen_tablet_dashboard.png")

    # --- Part 4: Capture 251229 Wireframe Project ---
    print("Navigating to 251229 Wireframe Project on port 4174...")
    context_wf = browser.new_context(viewport={"width": 1920, "height": 1080})
    page_wf = context_wf.new_page()
    page_wf.goto("http://127.0.0.1:4174", wait_until="networkidle")
    time.sleep(1.5)
    page_wf.screenshot(path=os.path.join(MOCKUP_DIR, "wireframe_251229_main.png"))
    print("Saved wireframe_251229_main.png")

    # Try navigating inside 251229 if buttons exist
    buttons = page_wf.locator("button, a").all()
    print(f"251229 found {len(buttons)} interactive elements")
    # Take a detailed shot
    page_wf.screenshot(path=os.path.join(MOCKUP_DIR, "wireframe_251229_detail.png"))
    print("Saved wireframe_251229_detail.png")

    browser.close()
    print("ALL ADVANCED SCREENSHOTS CAPTURED!")

