import os
import re
import json
from playwright.sync_api import sync_playwright

icons = [
    ('LayoutDashboard', 'layout-dashboard', '경영종합대시보드', 'lucide:layout-dashboard'),
    ('Factory', 'factory', '생산 공정 관리', 'lucide:factory'),
    ('ClipboardCheck', 'clipboard-check', '품질 보증·SPC', 'lucide:clipboard-check'),
    ('Package', 'package', '실시간 재고·BOM', 'lucide:package'),
    ('TrendingUp', 'trending-up', '영업·수주 분석', 'lucide:trending-up'),
    ('Shield', 'shield', '권한·보안 정책', 'lucide:shield'),
    ('Settings', 'settings', '시스템 환경 설정', 'lucide:settings'),
    ('Users', 'users', '작업자·인사 관리', 'lucide:users'),
]

base_dir = r"D:\102_1.codebridgex\MES Solution Website Structure 251030\node_modules\lucide-react\dist\esm\icons"
svg_items = []

for title, filename, label, token in icons:
    fp = os.path.join(base_dir, f"{filename}.js")
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
            m = re.search(r"const __iconNode = (\[.*?\]);", content, re.DOTALL)
            if m:
                node_str = m.group(1)
                clean_json = re.sub(r"(\w+):", r'"\1":', node_str)
                clean_json = re.sub(r",\s*([\]}])", r"\1", clean_json)
                nodes = json.loads(clean_json)
                
                inner_svg = ""
                for tag, attrs in nodes:
                    attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items() if k != "key")
                    inner_svg += f"<{tag} {attr_str} />"
                    
                svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" id="{filename}">{inner_svg}</svg>'''
                svg_items.append((filename, svg))

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; padding: 20px; background: transparent; display: flex; flex-wrap: wrap; gap: 20px; }
.icon-box { width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; }
</style>
</head>
<body>
"""
for fn, s in svg_items:
    html += f'<div class="icon-box" id="box-{fn}">{s}</div>\n'
html += "</body></html>"

out_dir = r"d:\097.flutter_project\auto_portfolio\assets\lucide_icons"
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1000, "height": 400})
    page.set_content(html)
    for fn, _ in svg_items:
        loc = page.locator(f"#box-{fn}")
        loc.screenshot(path=os.path.join(out_dir, f"{fn}.png"), omit_background=True)
    browser.close()

print(f"Successfully generated {len(svg_items)} real Lucide icon PNGs in {out_dir}!")
