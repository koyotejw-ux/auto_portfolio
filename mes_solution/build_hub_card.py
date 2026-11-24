import os
from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 675
img = Image.new('RGB', (W, H), (11, 15, 23)) # Deep elegant dark slate
draw = ImageDraw.Draw(img)

# Background subtle precision grid
for gx in range(0, W, 25):
    draw.line([(gx, 0), (gx, H)], fill=(20, 27, 45), width=1)
for gy in range(0, H, 25):
    draw.line([(0, gy), (W, gy)], fill=(20, 27, 45), width=1)

# Center ambient royal blue glow
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse([W//2 - 380, H//2 - 220, W//2 + 380, H//2 + 260], fill=(0, 81, 255, 50))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img.paste(glow, (0, 0), glow)

MOCKUP_DIR = r"d:\097.flutter_project\auto_portfolio\mes_solution\mockups"
desktop_path = os.path.join(MOCKUP_DIR, "render_desktop_dashboard.png")
tablet_path = os.path.join(MOCKUP_DIR, "render_tablet_dashboard.png")
mobile_path = os.path.join(MOCKUP_DIR, "render_mobile_dashboard.png")

# ==========================================
# 1. Desktop 16:9 Screen (1920x1080)
# Screen width: 720, height: 405 (Exact 16:9 = 1.7778)
# Chassis width: 732, height: 440
# ==========================================
desk_screen_w = 720
desk_screen_h = 405
desk_x = 210
desk_y = 65
title_bar_h = 28

desk_box_w = desk_screen_w + 12
desk_box_h = desk_screen_h + title_bar_h + 8

# Desktop Shadow
d_shadow = Image.new('RGBA', (desk_box_w + 50, desk_box_h + 50), (0, 0, 0, 0))
ds_draw = ImageDraw.Draw(d_shadow)
ds_draw.rounded_rectangle([20, 20, desk_box_w + 30, desk_box_h + 30], radius=16, fill=(0, 0, 0, 220))
d_shadow = d_shadow.filter(ImageFilter.GaussianBlur(25))
img.paste(d_shadow, (desk_x - 25, desk_y - 25), d_shadow)

# Chassis
draw.rounded_rectangle([desk_x, desk_y, desk_x + desk_box_w, desk_y + desk_box_h], radius=12, fill=(24, 32, 47), outline=(71, 85, 105), width=2)
# Title bar
draw.rounded_rectangle([desk_x, desk_y, desk_x + desk_box_w, desk_y + title_bar_h], radius=12, fill=(15, 23, 42))
draw.rectangle([desk_x, desk_y + 16, desk_x + desk_box_w, desk_y + title_bar_h], fill=(15, 23, 42))
draw.ellipse([desk_x + 12, desk_y + 10, desk_x + 18, desk_y + 16], fill=(239, 68, 68))
draw.ellipse([desk_x + 24, desk_y + 10, desk_x + 30, desk_y + 16], fill=(245, 158, 11))
draw.ellipse([desk_x + 36, desk_y + 10, desk_x + 42, desk_y + 16], fill=(16, 185, 129))

if os.path.exists(desktop_path):
    d_img = Image.open(desktop_path).convert('RGB')
    d_resized = d_img.resize((desk_screen_w, desk_screen_h), Image.Resampling.LANCZOS)
    img.paste(d_resized, (desk_x + 6, desk_y + title_bar_h + 2))

# ==========================================
# 2. Tablet 4:3 Screen (1024x768)
# Screen width: 340, height: 255 (Exact 4:3 = 1.3333)
# Chassis width: 364, height: 279
# ==========================================
tab_screen_w = 340
tab_screen_h = 255
tab_box_w = tab_screen_w + 24
tab_box_h = tab_screen_h + 24
tab_x = 70
tab_y = 340

t_shadow = Image.new('RGBA', (tab_box_w + 50, tab_box_h + 50), (0, 0, 0, 0))
ts_draw = ImageDraw.Draw(t_shadow)
ts_draw.rounded_rectangle([20, 20, tab_box_w + 30, tab_box_h + 30], radius=18, fill=(0, 0, 0, 230))
t_shadow = t_shadow.filter(ImageFilter.GaussianBlur(22))
img.paste(t_shadow, (tab_x - 25, tab_y - 25), t_shadow)

draw.rounded_rectangle([tab_x, tab_y, tab_x + tab_box_w, tab_y + tab_box_h], radius=16, fill=(15, 23, 42), outline=(100, 116, 139), width=2)
# Front camera dot
draw.ellipse([tab_x + 6, tab_y + tab_box_h // 2 - 3, tab_x + 12, tab_y + tab_box_h // 2 + 3], fill=(71, 85, 105))

if os.path.exists(tablet_path):
    t_img = Image.open(tablet_path).convert('RGB')
    t_resized = t_img.resize((tab_screen_w, tab_screen_h), Image.Resampling.LANCZOS)
    img.paste(t_resized, (tab_x + 16, tab_y + 12))

# ==========================================
# 3. Mobile Smartphone (390x844)
# Screen width: 175, height: 379 (Exact ratio 390/844 = 0.462)
# Chassis width: 191, height: 403
# ==========================================
mob_screen_w = 175
mob_screen_h = int(round(mob_screen_w / (390 / 844))) # 379px!
mob_box_w = mob_screen_w + 16
mob_box_h = mob_screen_h + 24
mob_x = 945
mob_y = 220

m_shadow = Image.new('RGBA', (mob_box_w + 50, mob_box_h + 50), (0, 0, 0, 0))
ms_draw = ImageDraw.Draw(m_shadow)
ms_draw.rounded_rectangle([20, 20, mob_box_w + 30, mob_box_h + 30], radius=30, fill=(0, 0, 0, 240))
m_shadow = m_shadow.filter(ImageFilter.GaussianBlur(24))
img.paste(m_shadow, (mob_x - 25, mob_y - 25), m_shadow)

draw.rounded_rectangle([mob_x, mob_y, mob_x + mob_box_w, mob_y + mob_box_h], radius=28, fill=(15, 23, 42), outline=(148, 163, 184), width=3)
# Dynamic Island
island_w = 48
island_h = 10
ix = mob_x + (mob_box_w - island_w) // 2
draw.rounded_rectangle([ix, mob_y + 6, ix + island_w, mob_y + 6 + island_h], radius=5, fill=(0, 0, 0))

if os.path.exists(mobile_path):
    m_img = Image.open(mobile_path).convert('RGB')
    m_resized = m_img.resize((mob_screen_w, mob_screen_h), Image.Resampling.LANCZOS)
    img.paste(m_resized, (mob_x + 8, mob_y + 18))

# Save output
out_hub_thumb = r"d:\097.flutter_project\auto_portfolio\assets\mes_solution_clean_devices.png"
img.save(out_hub_thumb, quality=95)
print("SAVED pixel-perfect 16:9, 4:3, 19.5:9 proportioned assets/mes_solution_clean_devices.png!")
