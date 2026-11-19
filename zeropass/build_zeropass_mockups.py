import os
from PIL import Image, ImageDraw, ImageFilter

MOCKUP_DIRS = [
    "d:/097.flutter_project/auto_portfolio/zeropass/assets/iphone_mockups"
]
for d in MOCKUP_DIRS:
    os.makedirs(d, exist_ok=True)

# Sources from actual simulator/device captures (904 x 2316)
SRC_SCREENS = {
    'mockup_01_pass.png': 'd:/097.flutter_project/zeropass/clean_ko_tab1.png',
    'mockup_02_ledger.png': 'd:/097.flutter_project/zeropass/clean_ko_tab2.png',
    'mockup_03_members.png': 'd:/097.flutter_project/zeropass/clean_ko_tab3.png',
    'mockup_04_pro.png': 'd:/097.flutter_project/zeropass/clean_ko_tab4.png',
    'mockup_05_vault.png': 'd:/097.flutter_project/zeropass/clean_ko_tab5.png',
    'mockup_06_en.png': 'd:/097.flutter_project/zeropass/clean_en_tab1.png',
}

def make_clean_iphone_mockup(screen_path, target_screen_w=720):
    screen = Image.open(screen_path).convert('RGBA')
    
    # 1. Clean bottom Android navigation gesture line/bar area if needed
    sample_y = screen.height - 80
    bg_sample = screen.getpixel((screen.width // 2, sample_y))
    if len(bg_sample) == 4 and bg_sample[3] == 0:
        bg_col = (11, 15, 25, 255)
    else:
        bg_col = (bg_sample[0], bg_sample[1], bg_sample[2], 255)
        
    s_draw = ImageDraw.Draw(screen)
    s_draw.rectangle([0, screen.height - 70, screen.width, screen.height], fill=bg_col)
    
    # Draw native iOS Home Indicator Bar
    bar_w_raw = 280
    bar_h_raw = 10
    bar_y_raw = screen.height - 35
    bar_col_raw = (0, 210, 255, 200) # Electric cyan bar
    s_draw.rounded_rectangle(
        [(screen.width - bar_w_raw) // 2, bar_y_raw, (screen.width + bar_w_raw) // 2, bar_y_raw + bar_h_raw],
        radius=5, fill=bar_col_raw
    )
    
    sw = target_screen_w
    target_sh = 1600 # 9:20 or ~19.5:9 standard phone ratio
    
    # Scale screen by width so no horizontal content is cropped
    scale = sw / screen.width
    new_w = sw
    new_h = int(round(screen.height * scale))
    screen_scaled = screen.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    if new_h <= target_sh:
        screen_resized = Image.new('RGBA', (sw, target_sh), bg_col)
        paste_y = (target_sh - new_h) // 2
        screen_resized.paste(screen_scaled, (0, paste_y))
    else:
        # Crop excess from bottom
        screen_resized = screen_scaled.crop((0, 0, sw, target_sh))
        
    sh = target_sh
    bezel = 18 # Ultra-slim bezel
    dev_w = sw + bezel * 2
    dev_h = sh + bezel * 2
    
    pad_side = 8
    canvas_w = dev_w + pad_side * 2
    canvas_h = dev_h
    
    device = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(device)
    
    ox = pad_side
    oy = 0
    
    # Hardware Buttons
    draw.rounded_rectangle([ox - 4, 220, ox, 270], radius=2, fill=(30, 41, 59, 255))
    draw.rounded_rectangle([ox - 4, 300, ox, 380], radius=2, fill=(30, 41, 59, 255))
    draw.rounded_rectangle([ox - 4, 400, ox, 480], radius=2, fill=(30, 41, 59, 255))
    draw.rounded_rectangle([ox + dev_w, 320, ox + dev_w + 4, 440], radius=2, fill=(30, 41, 59, 255))
    
    # Body Frame
    draw.rounded_rectangle([ox, oy, ox + dev_w, oy + dev_h], radius=54, fill=(15, 23, 42, 255), outline=(0, 210, 255, 140), width=2)
    draw.rounded_rectangle([ox + 2, oy + 2, ox + dev_w - 2, oy + dev_h - 2], radius=52, outline=(99, 102, 241, 70), width=1)
    draw.rounded_rectangle([ox + bezel - 2, oy + bezel - 2, ox + dev_w - bezel + 2, oy + dev_h - bezel + 2], radius=40, fill=(7, 10, 19, 255))
    
    # Mask
    mask = Image.new('L', (sw, sh), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, sw, sh], radius=38, fill=255)
    device.paste(screen_resized, (ox + bezel, oy + bezel), mask)
    
    # Dynamic Island
    di_w = int(round(sw * 0.28))
    di_h = 28
    di_x = ox + bezel + (sw - di_w) // 2
    di_y = oy + bezel + 10
    draw.rounded_rectangle([di_x, di_y, di_x + di_w, di_y + di_h], radius=14, fill=(0, 0, 0, 255))
    lens_x = di_x + di_w - 20
    lens_y = di_y + di_h // 2
    draw.ellipse([lens_x - 4, lens_y - 4, lens_x + 4, lens_y + 4], fill=(15, 23, 42, 255), outline=(30, 41, 59, 255), width=1)
    draw.ellipse([lens_x - 2, lens_y - 2, lens_x + 1, lens_y + 1], fill=(0, 210, 255, 180))
    
    return device

print("Generating ZeroPass device mockups from real captures...")
for out_name, src_path in SRC_SCREENS.items():
    dev = make_clean_iphone_mockup(src_path, target_screen_w=720)
    for out_d in MOCKUP_DIRS:
        save_p = os.path.join(out_d, out_name)
        dev.save(save_p, "PNG")
        print(f"Saved: {save_p}")
print("Mockup generation complete!")

