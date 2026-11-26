import os
import time
import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from playwright.sync_api import sync_playwright

BUILD_DIR = r"D:\102_1.codebridgex\MES Solution Website Structure 251030\build"
OUTPUT_DIR = r"d:\097.flutter_project\auto_portfolio\mes_solution\mockups"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BUILD_DIR, **kwargs)

def start_server():
    try:
        with TCPServer(('127.0.0.1', 4175), Handler) as httpd:
            print("Server running on 4175...")
            httpd.serve_forever()
    except Exception as e:
        print("Server info:", e)

t = threading.Thread(target=start_server, daemon=True)
t.start()
time.sleep(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # 1024x768 태블릿 해상도
    context = browser.new_context(viewport={"width": 1024, "height": 768})
    page = context.new_page()

    page.goto("http://127.0.0.1:4175", wait_until="networkidle")
    time.sleep(1)

    dash_btn = page.locator("text=대시보드로 이동").first
    if dash_btn.is_visible():
        dash_btn.click()
    else:
        for b in page.locator("button").all():
            if "데모" in b.inner_text() or "체험" in b.inner_text():
                b.click()
                break
    time.sleep(2)

    # 1. 태블릿 다크모드 캡처
    page.evaluate("() => { document.documentElement.classList.add('dark'); document.body.classList.add('dark'); }")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "render_tablet_dashboard_dark.png"))
    print("Saved render_tablet_dashboard_dark.png")

    # 2. 태블릿 라이트모드 캡처
    page.evaluate("() => { document.documentElement.classList.remove('dark'); document.body.classList.remove('dark'); }")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "render_tablet_dashboard.png"))
    print("Saved render_tablet_dashboard.png")

    browser.close()
    print("Done!")

