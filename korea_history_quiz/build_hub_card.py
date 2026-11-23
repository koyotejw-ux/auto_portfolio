import os
import math
from PIL import Image, ImageDraw, ImageFilter

MOCKUP_DIR = "d:/097.flutter_project/auto_portfolio/korea_history_quiz/assets/iphone_mockups"
OUT_PATH = "d:/097.flutter_project/auto_portfolio/assets/korea_history_quiz_clean_devices.png"

# Canvas 1200 x 675 (16:9 standard for hub portfolio cards)
W, H = 1200, 675
canvas = Image.new('RGB', (W, H), (11, 15, 25))
draw = ImageDraw.Draw(canvas)

# 1. Ambient Background Glows (Imperial Crimson #DC2626 & Amber Gold #F59E0B)
aura = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ad = ImageDraw.Draw(aura)
ad.ellipse([W//2 - 380, H//2 - 280, W//2 + 380, H//2 + 280], fill=(220, 38, 38, 55))
ad.ellipse([150, 100, 650, 600], fill=(245, 158, 11, 30))
ad.ellipse([W - 600, 80, W - 100, 580], fill=(185, 28, 28, 40))
aura = aura.filter(ImageFilter.GaussianBlur(90))
canvas.paste(aura, (0, 0), aura)

# 2. Subtle Precision Grid Network
grid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
for x in range(0, W, 40):
    gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 7), width=1)
for y in range(0, H, 40):
    gd.line([(0, y), (W, y)], fill=(255, 255, 255, 7), width=1)
canvas.paste(grid, (0, 0), grid)

# 3. Load Phone Mockups
# We will place 3 phones: Left (Exam Center), Right (Study Hall), Center (Home Dashboard)
p_home = Image.open(os.path.join(MOCKUP_DIR, 'mockup_01_home.png')).convert('RGBA')
p_exam = Image.open(os.path.join(MOCKUP_DIR, 'mockup_02_exam.png')).convert('RGBA')
p_study = Image.open(os.path.join(MOCKUP_DIR, 'mockup_04_study.png')).convert('RGBA')

# Target height for center phone: 560px
h_center = 570
scale_c = h_center / p_home.height
w_center = int(p_home.width * scale_c)
p_center_scaled = p_home.resize((w_center, h_center), Image.Resampling.LANCZOS)

# Side phones slightly smaller (e.g. 500px height) and angled / offset
h_side = 505
scale_s = h_side / p_exam.height
w_side = int(p_exam.width * scale_s)
p_left_scaled = p_exam.resize((w_side, h_side), Image.Resampling.LANCZOS)
p_right_scaled = p_study.resize((w_side, h_side), Image.Resampling.LANCZOS)

def make_device_shadow(im, radius=32, alpha=180):
    sh = Image.new('RGBA', (im.width + 64, im.height + 64), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([32, 32, 32 + im.width, 32 + im.height], radius=44, fill=(0, 0, 0, alpha))
    return sh.filter(ImageFilter.GaussianBlur(radius))

# Layout positions
cx_center = (W - w_center) // 2
cy_center = 60 # Centers vertically within 675

cx_left = cx_center - int(w_side * 0.72)
cy_left = 95

cx_right = cx_center + int(w_center * 0.78)
cy_right = 95

# Paste Left Device
sh_left = make_device_shadow(p_left_scaled, radius=30, alpha=160)
canvas.paste(sh_left, (cx_left - 32, cy_left - 24), sh_left)
canvas.paste(p_left_scaled, (cx_left, cy_left), p_left_scaled)

# Paste Right Device
sh_right = make_device_shadow(p_right_scaled, radius=30, alpha=160)
canvas.paste(sh_right, (cx_right - 32, cy_right - 24), sh_right)
canvas.paste(p_right_scaled, (cx_right, cy_right), p_right_scaled)

# Paste Center Device (Foreground Hero)
sh_center = make_device_shadow(p_center_scaled, radius=38, alpha=210)
canvas.paste(sh_center, (cx_center - 32, cy_center - 24), sh_center)
canvas.paste(p_center_scaled, (cx_center, cy_center), p_center_scaled)

# Subtle Vignette / Edge Shadow on bottom
vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
vd.rectangle([0, H - 90, W, H], fill=(11, 15, 25, 120))
vignette = vignette.filter(ImageFilter.GaussianBlur(30))
canvas.paste(vignette, (0, 0), vignette)

canvas.save(OUT_PATH, 'PNG', quality=95)
print(f"Generated High-End Hub Clean Devices Card: {OUT_PATH} ({canvas.size})")
