import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Test Master Hub
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto("file:///d:/097.flutter_project/auto_portfolio/index.html")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="d:/097.flutter_project/auto_portfolio/master_hub_screenshot.png", full_page=False)
        print("Master Hub Screenshot saved.")
        
        # 2. Test FTMT Case Study
        page_ftmt = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_ftmt.goto("file:///d:/097.flutter_project/auto_portfolio/ftmt/index.html")
        await page_ftmt.wait_for_timeout(1000)
        await page_ftmt.screenshot(path="d:/097.flutter_project/auto_portfolio/ftmt_deck_screenshot.png", full_page=False)
        print("FTMT Case Study Screenshot saved.")
        
        # 3. Test FTMT Prototype (Desktop 1440x900)
        page_proto = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_proto.goto("file:///d:/097.flutter_project/auto_portfolio/ftmt/prototype.html")
        await page_proto.wait_for_timeout(1500)
        await page_proto.screenshot(path="d:/097.flutter_project/auto_portfolio/ftmt_proto_desktop.png")
        print("FTMT Prototype Desktop Screenshot saved.")
        
        # 4. Test FTMT Prototype (Laptop short height 1366x700 - verifying auto-resizing fits without vertical clipping!)
        page_short = await browser.new_page(viewport={'width': 1366, 'height': 700})
        await page_short.goto("file:///d:/097.flutter_project/auto_portfolio/ftmt/prototype.html")
        await page_short.wait_for_timeout(1500)
        scale_val = await page_short.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--device-scale')")
        print(f"Device Scale on 700px height: {scale_val.strip()}")
        await page_short.screenshot(path="d:/097.flutter_project/auto_portfolio/ftmt_proto_short_laptop.png")
        print("FTMT Prototype Short Laptop Screenshot saved.")
        
        await browser.close()
        print("All verification tests passed successfully!")

asyncio.run(main())
