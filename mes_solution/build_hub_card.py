import os
from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 675
img = Image.new('RGB', (W, H), (11, 15, 23)) # Senior deep navy theme matching Smart DCA / Korea History Quiz
draw = ImageDraw.Draw(img)

# Tech Grid Lines
for gx in range(0, W, 25):
    draw.line([(gx, 0), (gx, H)], fill=(20, 27, 45), width=1)
for gy in range(0, H, 25):
    draw.line([(0, gy), (W, gy)], fill=(20, 27, 45), width=1)

# Center ambient royal blue glow
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse([W//2 - 380, H//2 - 220, W//2 + 380, H//2 + 260], fill=(0, 81, 255, 55))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img.paste(glow, (0, 0), glow)

MOCKUP_DIR = r"d:\097.flutter_project\auto_portfolio\mes_solution\mockups"
desktop_path = os.path.join(MOCKUP_DIR, "render_desktop_dashboard.png")
tablet_path = os.path.join(MOCKUP_DIR, "render_tablet_dashboard.png")
mobile_path = os.path.join(MOCKUP_DIR, "render_mobile_dashboard.png")

# --- 1. Desktop Laptop Monitor (Center-Back) ---
# Size: 760 x 475 (16:10)
desk_w = 760
desk_h = 475
desk_x = (W - desk_w) // 2 - 20
desk_y = 55

# Desktop Shadow
shadow = Image.new('RGBA', (desk_w + 60, desk_h + 60), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(shadow)
s_draw.rounded_rectangle([20, 20, desk_w + 40, desk_h + 40], radius=16, fill=(0, 0, 0, 210))
shadow = shadow.filter(ImageFilter.GaussianBlur(28))
img.paste(shadow, (desk_x - 30, desk_y - 30), shadow)

# Desktop Bezel
draw.rounded_rectangle([desk_x, desk_y, desk_x + desk_w, desk_y + desk_h], radius=12, fill=(24, 32, 47), outline=(71, 85, 105), width=2)
# Desktop Title bar
draw.rounded_rectangle([desk_x, desk_y, desk_x + desk_w, desk_y + 26], radius=12, fill=(15, 23, 42))
draw.rectangle([desk_x, desk_y + 16, desk_x + desk_w, desk_y + 26], fill=(15, 23, 42))
draw.ellipse([desk_x + 12, desk_y + 8, desk_x + 20, desk_y + 16], fill=(239, 68, 68))
draw.ellipse([desk_x + 25, desk_y + 8, desk_x + 33, desk_y + 16], fill=(245, 158, 11))
draw.ellipse([desk_x + 38, desk_y + 8, desk_x + 46, desk_y + 16], fill=(16, 185, 129))

if os.path.exists(desktop_path):
    d_img = Image.open(desktop_path).convert('RGB')
    d_resized = d_img.resize((desk_w - 4, desk_h - 28), Image.Resampling.LANCZOS)
    img.paste(d_resized, (desk_x + 2, desk_y + 26))

# --- 2. Tablet 10-inch (Left-Front, Landscape) ---
# Size: 380 x 260
tab_w = 380
tab_h = 260
tab_x = 50
tab_y = 350

tab_shadow = Image.new('RGBA', (tab_w + 50, tab_h + 50), (0, 0, 0, 0))
ts_draw = ImageDraw.Draw(tab_shadow)
ts_draw.rounded_rectangle([20, 20, tab_w + 30, tab_h + 30], radius=16, fill=(0, 0, 0, 230))
tab_shadow = tab_shadow.filter(ImageFilter.GaussianBlur(22))
img.paste(tab_shadow, (tab_x - 25, tab_y - 25), tab_shadow)

draw.rounded_rectangle([tab_x, tab_y, tab_x + tab_w, tab_y + tab_h], radius=14, fill=(15, 23, 42), outline=(100, 116, 139), width=3)
draw.ellipse([tab_x + 8, tab_y + tab_h//2 - 3, tab_x + 14, tab_y + tab_h//2 + 3], fill=(71, 85, 105))

if os.path.exists(tablet_path):
    t_img = Image.open(tablet_path).convert('RGB')
    t_resized = t_img.resize((tab_w - 24, tab_h - 16), Image.Resampling.LANCZOS)
    img.paste(t_resized, (tab_x + 16, tab_y + 8))

# --- 3. Smartphone (Right-Front, Portrait) ---
# Size: 175 x 375
mob_w = 180
mob_h = 385
mob_x = 960
mob_y = 235

mob_shadow = Image.new('RGBA', (mob_w + 50, mob_h + 50), (0, 0, 0, 0))
ms_draw = ImageDraw.Draw(mob_shadow)
ms_draw.rounded_rectangle([20, 20, mob_w + 30, mob_h + 30], radius=28, fill=(0, 0, 0, 240))
mob_shadow = mob_shadow.filter(ImageFilter.GaussianBlur(24))
img.paste(mob_shadow, (mob_x - 25, mob_y - 25), mob_shadow)

draw.rounded_rectangle([mob_x, mob_y, mob_x + mob_w, mob_y + mob_h], radius=26, fill=(15, 23, 42), outline=(148, 163, 184), width=3)
# Dynamic Island
island_w = 52
island_h = 12
ix = mob_x + (mob_w - island_w) // 2
draw.rounded_rectangle([ix, mob_y + 8, ix + island_w, mob_y + 8 + island_h], radius=6, fill=(0, 0, 0))

if os.path.exists(mobile_path):
    m_img = Image.open(mobile_path).convert('RGB')
    m_resized = m_img.resize((mob_w - 12, mob_h - 30), Image.Resampling.LANCZOS)
    img.paste(m_resized, (mob_x + 6, mob_y + 24))

# Save output
out_hub_thumb = r"d:\097.flutter_project\auto_portfolio\assets\mes_solution_clean_devices.png"
img.save(out_hub_thumb, quality=95)
print("SAVED pristine assets/mes_solution_clean_devices.png with live rendered screens!")
