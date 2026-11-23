import os
from PIL import Image, ImageDraw, ImageFilter

MOCKUP_DIR = "d:/097.flutter_project/auto_portfolio/korea_history_quiz/assets/iphone_mockups"
OUT_PATH = "d:/097.flutter_project/auto_portfolio/assets/korea_history_quiz_clean_devices.png"

# Canvas 1200 x 675 (Exact hub card aspect ratio and dark luxury container matching smart_dca)
W, H = 1200, 675
canvas = Image.new('RGB', (W, H), (11, 15, 25))

# 1. Subtle Radial Ambient Lighting behind devices (Navy & Cobalt Aura matching Korean Heritage)
aura = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ad = ImageDraw.Draw(aura)
ad.ellipse([W//2 - 320, H//2 - 250, W//2 + 320, H//2 + 250], fill=(29, 78, 216, 45)) # Cobalt Navy
ad.ellipse([W//2 - 200, H//2 - 180, W//2 + 200, H//2 + 180], fill=(225, 29, 72, 35)) # Taegeuk Crimson glow
aura = aura.filter(ImageFilter.GaussianBlur(95))
canvas.paste(aura, (0, 0), aura)

# 2. Devices Setup
# Phone 1: Left slightly behind (Exam Center)
# Phone 2: Right slightly behind (Study Hall / Quiz)
# Phone 3: Center foreground hero (Home Dashboard)
p_home = Image.open(os.path.join(MOCKUP_DIR, 'mockup_01_home.png')).convert('RGBA')
p_exam = Image.open(os.path.join(MOCKUP_DIR, 'mockup_02_exam.png')).convert('RGBA')
p_quiz = Image.open(os.path.join(MOCKUP_DIR, 'mockup_03_quiz.png')).convert('RGBA')

# In smart_dca, the bounding box spans x=250 to 950 (width 700px), y=20 to 670 (height 650px)
# Center device height ~ 630px
h_center = 635
sc_center = h_center / p_home.height
w_center = int(p_home.width * sc_center)
p_center_scaled = p_home.resize((w_center, h_center), Image.Resampling.LANCZOS)

# Side devices height ~ 560px
h_side = 565
sc_side = h_side / p_exam.height
w_side = int(p_exam.width * sc_side)
p_left_scaled = p_exam.resize((w_side, h_side), Image.Resampling.LANCZOS)
p_right_scaled = p_quiz.resize((w_side, h_side), Image.Resampling.LANCZOS)

def make_device_shadow(im, radius=36, alpha=190):
    sh = Image.new('RGBA', (im.width + 72, im.height + 72), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([36, 36, 36 + im.width, 36 + im.height], radius=44, fill=(0, 0, 0, alpha))
    return sh.filter(ImageFilter.GaussianBlur(radius))

cx_center = (W - w_center) // 2
cy_center = (H - h_center) // 2 + 10 # ~30px from top

# Exact offsets matching Smart DCA 3-phone cluster
offset_x = int(w_center * 0.72) # ~215px
cx_left = cx_center - offset_x
cy_left = cy_center + 45

cx_right = cx_center + offset_x
cy_right = cy_center + 45

# 1. Left Device
sh_left = make_device_shadow(p_left_scaled, radius=32, alpha=160)
canvas.paste(sh_left, (cx_left - 36, cy_left - 24), sh_left)
canvas.paste(p_left_scaled, (cx_left, cy_left), p_left_scaled)

# 2. Right Device
sh_right = make_device_shadow(p_right_scaled, radius=32, alpha=160)
canvas.paste(sh_right, (cx_right - 36, cy_right - 24), sh_right)
canvas.paste(p_right_scaled, (cx_right, cy_right), p_right_scaled)

# 3. Center Device (Hero)
sh_center = make_device_shadow(p_center_scaled, radius=42, alpha=220)
canvas.paste(sh_center, (cx_center - 36, cy_center - 24), sh_center)
canvas.paste(p_center_scaled, (cx_center, cy_center), p_center_scaled)

canvas.save(OUT_PATH, 'PNG', quality=95)
print(f"Generated Consistent Hub Clean Devices Card: {OUT_PATH} ({canvas.size})")
