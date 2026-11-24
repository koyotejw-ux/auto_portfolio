import os
from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 675
img = Image.new('RGB', (W, H), (15, 23, 42)) # Elegant dark backdrop matching senior portfolio standard
draw = ImageDraw.Draw(img)

# Background tech grid & soft radial gradient glow
for gx in range(0, W, 30):
    draw.line([(gx, 0), (gx, H)], fill=(23, 33, 56), width=1)
for gy in range(0, H, 30):
    draw.line([(0, gy), (W, gy)], fill=(23, 33, 56), width=1)

# Subtle ambient light glow (Blue center glow)
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse([W//2 - 350, H//2 - 200, W//2 + 350, H//2 + 250], fill=(0, 81, 255, 45))
glow = glow.filter(ImageFilter.GaussianBlur(80))
img.paste(glow, (0, 0), glow)

# Paths
MOCKUP_DIR = r"d:\097.flutter_project\auto_portfolio\mes_solution\mockups"
desktop_path = os.path.join(MOCKUP_DIR, "screen_02_dashboard_dark.png")
if not os.path.exists(desktop_path):
    desktop_path = os.path.join(MOCKUP_DIR, "screen_02_dashboard.png")

phone_path = os.path.join(MOCKUP_DIR, "wireframe_phone_dashboard.png")
tablet_path = os.path.join(MOCKUP_DIR, "wireframe_tablet_dashboard.png")

# --- 1. Desktop Laptop / Monitor Mockup (Center-Back) ---
# Width: 780, Height: 488 (16:10 ratio)
desk_w = 780
desk_h = 488
desk_x = (W - desk_w) // 2 - 40
desk_y = 60

# Desktop Shadow
shadow = Image.new('RGBA', (desk_w + 60, desk_h + 60), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(shadow)
s_draw.rounded_rectangle([20, 20, desk_w + 40, desk_h + 40], radius=16, fill=(0, 0, 0, 180))
shadow = shadow.filter(ImageFilter.GaussianBlur(25))
img.paste(shadow, (desk_x - 30, desk_y - 30), shadow)

# Monitor Body
draw.rounded_rectangle([desk_x, desk_y, desk_x + desk_w, desk_y + desk_h], radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
# Monitor Title bar
draw.rounded_rectangle([desk_x, desk_y, desk_x + desk_w, desk_y + 28], radius=12, fill=(15, 23, 42))
draw.rectangle([desk_x, desk_y + 18, desk_x + desk_w, desk_y + 28], fill=(15, 23, 42))
# Dots
draw.ellipse([desk_x + 10, desk_y + 9, desk_x + 18, desk_y + 17], fill=(239, 68, 68))
draw.ellipse([desk_x + 23, desk_y + 9, desk_x + 31, desk_y + 17], fill=(245, 158, 11))
draw.ellipse([desk_x + 36, desk_y + 9, desk_x + 44, desk_y + 17], fill=(16, 185, 129))

# Desktop Screen Image
if os.path.exists(desktop_path):
    d_img = Image.open(desktop_path).convert('RGB')
    d_resized = d_img.resize((desk_w - 4, desk_h - 32), Image.Resampling.LANCZOS)
    img.paste(d_resized, (desk_x + 2, desk_y + 30))

# --- 2. Tablet Mockup (Left-Front, slightly overlapping) ---
# Tablet 10-inch landscape or portrait: let's do 360 x 240
tab_w = 340
tab_h = 226
tab_x = 70
tab_y = 380

# Tablet Shadow
tab_shadow = Image.new('RGBA', (tab_w + 40, tab_h + 40), (0, 0, 0, 0))
ts_draw = ImageDraw.Draw(tab_shadow)
ts_draw.rounded_rectangle([15, 15, tab_w + 25, tab_h + 25], radius=14, fill=(0, 0, 0, 200))
tab_shadow = tab_shadow.filter(ImageFilter.GaussianBlur(18))
img.paste(tab_shadow, (tab_x - 20, tab_y - 20), tab_shadow)

# Tablet Chassis
draw.rounded_rectangle([tab_x, tab_y, tab_x + tab_w, tab_y + tab_h], radius=12, fill=(15, 23, 42), outline=(100, 116, 139), width=2)
# Camera dot
draw.ellipse([tab_x + 8, tab_y + tab_h//2 - 3, tab_x + 14, tab_y + tab_h//2 + 3], fill=(71, 85, 105))

if os.path.exists(tablet_path):
    t_img = Image.open(tablet_path).convert('RGB')
    t_resized = t_img.resize((tab_w - 24, tab_h - 16), Image.Resampling.LANCZOS)
    img.paste(t_resized, (tab_x + 16, tab_y + 8))

# --- 3. Smartphone Phone Mockup (Right-Front, vertical standing) ---
phone_w = 175
phone_h = 360
phone_x = 940
phone_y = 260

# Phone Shadow
p_shadow = Image.new('RGBA', (phone_w + 40, phone_h + 40), (0, 0, 0, 0))
ps_draw = ImageDraw.Draw(p_shadow)
ps_draw.rounded_rectangle([15, 15, phone_w + 25, phone_h + 25], radius=24, fill=(0, 0, 0, 220))
p_shadow = p_shadow.filter(ImageFilter.GaussianBlur(20))
img.paste(p_shadow, (phone_x - 20, phone_y - 20), p_shadow)

# Phone Chassis (iPhone bezel)
draw.rounded_rectangle([phone_x, phone_y, phone_x + phone_w, phone_y + phone_h], radius=24, fill=(15, 23, 42), outline=(148, 163, 184), width=3)
# Dynamic Island
island_w = 46
island_h = 12
ix = phone_x + (phone_w - island_w) // 2
draw.rounded_rectangle([ix, phone_y + 8, ix + island_w, phone_y + 8 + island_h], radius=6, fill=(0, 0, 0))

if os.path.exists(phone_path):
    p_img = Image.open(phone_path).convert('RGB')
    p_resized = p_img.resize((phone_w - 12, phone_h - 28), Image.Resampling.LANCZOS)
    img.paste(p_resized, (phone_x + 6, phone_y + 22))

# Save output
out_hub_thumb = r"d:\097.flutter_project\auto_portfolio\assets\mes_solution_clean_devices.png"
img.save(out_hub_thumb, quality=95)
print("SAVED assets/mes_solution_clean_devices.png!")
