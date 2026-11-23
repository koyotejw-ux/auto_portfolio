import os
from PIL import Image, ImageDraw, ImageFilter

MOCKUP_DIR = "d:/097.flutter_project/auto_portfolio/korea_history_quiz/assets/iphone_mockups"
BRAIN_DIR = r"C:\Users\coyot\.gemini\antigravity\brain\1ef9de17-1396-4a70-8442-94124acd932e"
os.makedirs(MOCKUP_DIR, exist_ok=True)

# 5 Freshly Captured Real App Screenshots from simulator (904 x 2316 Light Mode)
RAW_SCREENS = {
    'mockup_01_home.png': os.path.join(BRAIN_DIR, 'real_test_03_home_allowed.png'),
    'mockup_02_exam.png': os.path.join(BRAIN_DIR, 'real_test_13_exam_center.png'),
    'mockup_03_quiz.png': os.path.join(BRAIN_DIR, 'real_test_32_opt3_center.png'),
    'mockup_04_study.png': os.path.join(BRAIN_DIR, 'real_test_18_study_tab.png'),
    'mockup_05_notes.png': os.path.join(BRAIN_DIR, 'device_incorrect_hub_sheet.png'),
}

def make_pristine_light_phone_mockup(screen_path, target_screen_w=720):
    screen = Image.open(screen_path).convert('RGBA')
    
    # 1. Clean bottom navigation bar area and draw crisp native home indicator
    sample_y = screen.height - 120
    bg_sample = screen.getpixel((screen.width // 2, sample_y))
    if len(bg_sample) == 4 and bg_sample[3] == 0:
        bg_col = (255, 255, 255, 255)
    else:
        bg_col = (bg_sample[0], bg_sample[1], bg_sample[2], 255)
        
    s_draw = ImageDraw.Draw(screen)
    # Clear bottom edge
    s_draw.rectangle([0, screen.height - 90, screen.width, screen.height], fill=bg_col)
    
    # Draw sleek dark slate home indicator
    bar_w_raw = 260
    bar_h_raw = 8
    bar_y_raw = screen.height - 36
    bar_col_raw = (30, 41, 59, 210) # Slate-800 Indicator
    s_draw.rounded_rectangle(
        [(screen.width - bar_w_raw) // 2, bar_y_raw, (screen.width + bar_w_raw) // 2, bar_y_raw + bar_h_raw],
        radius=4, fill=bar_col_raw
    )
    
    sw = target_screen_w
    target_sh = 1620 # 9:20 flagship phone ratio (720 x 1620)
    
    scale = sw / screen.width
    new_w = sw
    new_h = int(round(screen.height * scale))
    screen_scaled = screen.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    if new_h <= target_sh:
        screen_resized = Image.new('RGBA', (sw, target_sh), bg_col)
        paste_y = (target_sh - new_h) // 2
        screen_resized.paste(screen_scaled, (0, paste_y))
    else:
        screen_resized = screen_scaled.crop((0, 0, sw, target_sh))
        
    sh = target_sh
    bezel = 18 # Ultra-slim bezel
    dev_w = sw + bezel * 2
    dev_h = sh + bezel * 2
    
    pad_side = 8
    canvas_w = dev_w + pad_side * 2
    canvas_h = dev_h
    
    device = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(device)
    
    ox = pad_side
    oy = 0
    
    # Outer Frame: Midnight Titanium with subtle Cobalt Edge (#1D4ED8)
    d_draw.rounded_rectangle([ox, oy, ox + dev_w, oy + dev_h], radius=44, fill=(24, 28, 40, 255), outline=(29, 78, 216, 160), width=3)
    # Inner bezel
    d_draw.rounded_rectangle([ox + 4, oy + 4, ox + dev_w - 4, oy + dev_h - 4], radius=40, fill=(15, 20, 30, 255))
    
    # Screen Mask
    mask = Image.new('L', (sw, sh), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, sw, sh], radius=32, fill=255)
    
    screen_x = ox + bezel
    screen_y = oy + bezel
    device.paste(screen_resized, (screen_x, screen_y), mask)
    
    # Top Dynamic Island Pill
    pill_w = 160
    pill_h = 30
    pill_x0 = ox + (dev_w - pill_w) // 2
    pill_y0 = screen_y + 12
    d_draw.rounded_rectangle([pill_x0, pill_y0, pill_x0 + pill_w, pill_y0 + pill_h], radius=15, fill=(0, 0, 0, 255))
    
    # Camera Reflection
    lens_r = 4
    d_draw.ellipse([pill_x0 + pill_w - 24 - lens_r, pill_y0 + 15 - lens_r, pill_x0 + pill_w - 24 + lens_r, pill_y0 + 15 + lens_r], fill=(25, 45, 80, 255))
    
    return device

print("Generating Fresh Real App Screenshots Mockups...")
for name, raw_p in RAW_SCREENS.items():
    if os.path.exists(raw_p):
        out_img = make_pristine_light_phone_mockup(raw_p)
        out_p = os.path.join(MOCKUP_DIR, name)
        out_img.save(out_p, 'PNG')
        print(f"Saved Real Mockup: {out_p} ({out_img.size})")
    else:
        print(f"Missing Raw Screen: {raw_p}")

