import os
from PIL import Image, ImageDraw, ImageFilter

MOCKUP_DIR = "d:/097.flutter_project/auto_portfolio/korea_history_quiz/assets/iphone_mockups"
os.makedirs(MOCKUP_DIR, exist_ok=True)

SRC_SCREENS = {
    'mockup_01_home.png': 'd:/097.flutter_project/korea_history_quiz/store/screenshots/phone/screen_1_home_dashboard.png',
    'mockup_02_exam.png': 'd:/097.flutter_project/korea_history_quiz/store/screenshots/phone/screen_2_exam_center.png',
    'mockup_03_quiz.png': 'd:/097.flutter_project/korea_history_quiz/store/screenshots/phone/screen_3_quiz_commentary.png',
    'mockup_04_study.png': 'd:/097.flutter_project/korea_history_quiz/store/screenshots/phone/screen_4_study_hall.png',
    'mockup_05_notes.png': 'd:/097.flutter_project/korea_history_quiz/store/screenshots/phone/screen_5_incorrect_notes.png',
}

def make_clean_phone_mockup(screen_path, target_screen_w=720):
    screen = Image.open(screen_path).convert('RGBA')
    
    # 1. Clean bottom Android navigation gesture line/bar area if needed
    sample_y = screen.height - 80
    bg_sample = screen.getpixel((screen.width // 2, sample_y))
    if len(bg_sample) == 4 and bg_sample[3] == 0:
        bg_col = (15, 23, 42, 255)
    else:
        bg_col = (bg_sample[0], bg_sample[1], bg_sample[2], 255)
        
    s_draw = ImageDraw.Draw(screen)
    # Draw bottom bar
    bar_w_raw = 280
    bar_h_raw = 8
    bar_y_raw = screen.height - 30
    bar_col_raw = (220, 38, 38, 200) # Deep Crimson Accent
    s_draw.rounded_rectangle(
        [(screen.width - bar_w_raw) // 2, bar_y_raw, (screen.width + bar_w_raw) // 2, bar_y_raw + bar_h_raw],
        radius=4, fill=bar_col_raw
    )
    
    sw = target_screen_w
    target_sh = 1600 # 9:20 ratio
    
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
    bezel = 18
    dev_w = sw + bezel * 2
    dev_h = sh + bezel * 2
    
    pad_side = 8
    canvas_w = dev_w + pad_side * 2
    canvas_h = dev_h
    
    device = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(device)
    
    dev_x0 = pad_side
    dev_y0 = 0
    dev_x1 = dev_x0 + dev_w
    dev_y1 = dev_y0 + dev_h
    
    # Outer frame: Titanium Dark Metal with Subtle Crimson Hue
    d_draw.rounded_rectangle([dev_x0, dev_y0, dev_x1, dev_y1], radius=44, fill=(18, 20, 29, 255), outline=(220, 38, 38, 140), width=3)
    # Inner border
    d_draw.rounded_rectangle([dev_x0 + 4, dev_y0 + 4, dev_x1 - 4, dev_y1 - 4], radius=40, fill=(10, 12, 18, 255))
    
    # Screen Mask
    mask = Image.new('L', (sw, sh), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, sw, sh], radius=32, fill=255)
    
    screen_x = dev_x0 + bezel
    screen_y = dev_y0 + bezel
    device.paste(screen_resized, (screen_x, screen_y), mask)
    
    # Top Dynamic Island Pill
    pill_w = 170
    pill_h = 32
    pill_x0 = dev_x0 + (dev_w - pill_w) // 2
    pill_y0 = screen_y + 12
    d_draw.rounded_rectangle([pill_x0, pill_y0, pill_x0 + pill_w, pill_y0 + pill_h], radius=16, fill=(0, 0, 0, 255))
    
    # Lens reflection
    lens_r = 5
    d_draw.ellipse([pill_x0 + pill_w - 24 - lens_r, pill_y0 + 16 - lens_r, pill_x0 + pill_w - 24 + lens_r, pill_y0 + 16 + lens_r], fill=(20, 35, 60, 255))
    
    return device

print("Generating Clean Phone Mockups...")
for name, path in SRC_SCREENS.items():
    if os.path.exists(path):
        out_img = make_clean_phone_mockup(path)
        out_path = os.path.join(MOCKUP_DIR, name)
        out_img.save(out_path, 'PNG')
        print(f"Saved: {out_path} ({out_img.size})")

# Also generate combined devices image for hub thumbnail
def generate_hub_clean_devices():
    hub_asset_path = 'd:/097.flutter_project/auto_portfolio/assets/korea_history_quiz_clean_devices.png'
    phone1 = Image.open(os.path.join(MOCKUP_DIR, 'mockup_01_home.png')).convert('RGBA')
    phone2 = Image.open(os.path.join(MOCKUP_DIR, 'mockup_02_exam.png')).convert('RGBA')
    phone3 = Image.open(os.path.join(MOCKUP_DIR, 'mockup_03_quiz.png')).convert('RGBA')
    
    cw, ch = 1200, 800
    comp = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    
    # Scale phones to fit canvas
    s_h = 680
    sc = s_h / phone1.height
    s_w = int(phone1.width * sc)
    
    p1 = phone1.resize((s_w, s_h), Image.Resampling.LANCZOS)
    p2 = phone2.resize((s_w, s_h), Image.Resampling.LANCZOS)
    p3 = phone3.resize((s_w, s_h), Image.Resampling.LANCZOS)
    
    # Add subtle shadows
    def paste_with_shadow(canvas, img, pos):
        sh = Image.new('RGBA', (img.width + 40, img.height + 40), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(sh)
        sh_draw.rounded_rectangle([20, 20, 20 + img.width, 20 + img.height], radius=36, fill=(0, 0, 0, 120))
        sh_blur = sh.filter(ImageFilter.GaussianBlur(18))
        canvas.paste(sh_blur, (pos[0] - 20, pos[1] - 10), sh_blur)
        canvas.paste(img, pos, img)
        
    paste_with_shadow(comp, p2, (80, 70))
    paste_with_shadow(comp, p3, (cw - s_w - 80, 70))
    paste_with_shadow(comp, p1, ((cw - s_w) // 2, 40)) # Center front
    
    comp.save(hub_asset_path, 'PNG')
    print(f"Saved Hub Clean Devices Thumbnail: {hub_asset_path} ({comp.size})")

generate_hub_clean_devices()

