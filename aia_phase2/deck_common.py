import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
BASE_DIR = r"d:\097.flutter_project\auto_portfolio\aia_phase2"
CORE_DIR = os.path.join(BASE_DIR, "core_screens")
QI_DIR = os.path.join(BASE_DIR, "qi_assets")
OUT_DIR = os.path.join(BASE_DIR, "behance_slides")
os.makedirs(OUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# Color Architecture (AIA Signature Red + Obsidian Navy System)
# -------------------------------------------------------------
AIA_RED = (211, 17, 69)            # #D31145 Primary AIA Red
AIA_RED_DARK = (158, 0, 43)        # #9E002B Deep Red
AIA_RED_LIGHT = (255, 238, 242)    # #FFE7ED Tint
AIA_RED_BORDER = (254, 205, 217)

BG_DARK = (15, 18, 26)             # #0F121A Obsidian Black/Navy
CARD_DARK = (24, 30, 42)           # Container Dark
BORDER_DARK = (51, 65, 85)
TEXT_DARK_MAIN = (255, 255, 255)
TEXT_DARK_SUB = (148, 163, 184)

BG_LIGHT = (248, 250, 252)         # #F8FAFC Ultra-Clean Slate
CARD_LIGHT = (255, 255, 255)
BORDER_LIGHT = (226, 232, 240)
BORDER_LIGHT_ACCENT = (203, 213, 225)
TEXT_LIGHT_MAIN = (15, 23, 42)
TEXT_LIGHT_SUB = (71, 85, 105)

FONT_DIR = "C:/Windows/Fonts"
WEIGHT_MAP = {
    'black': 'Pretendard-Black.ttf',
    'extrabold': 'Pretendard-ExtraBold.ttf',
    'bold': 'Pretendard-Bold.ttf',
    'semibold': 'Pretendard-SemiBold.ttf',
    'medium': 'Pretendard-Medium.ttf',
    'regular': 'Pretendard-Regular.ttf',
    'light': 'Pretendard-Light.ttf',
}

def get_font(size, weight='bold'):
    w_name = 'bold' if isinstance(weight, bool) and weight else ('regular' if isinstance(weight, bool) else str(weight).lower())
    font_file = WEIGHT_MAP.get(w_name, 'Pretendard-Regular.ttf')
    font_path = os.path.join(FONT_DIR, font_file)
    try:
        return ImageFont.truetype(font_path, int(round(size)))
    except:
        return ImageFont.load_default()

def get_num_font(size, weight='black'):
    return get_font(size, weight)

def wrap_text(text, font, max_width, draw):
    lines = []
    paragraphs = text.split('\n')
    for p in paragraphs:
        if not p:
            lines.append('')
            continue
        words = p.split(' ')
        current_line = ''
        for word in words:
            test_line = (current_line + ' ' + word).strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
    return lines

def draw_pill_badge(draw, cx=None, cy=0, text="", font=None, theme='red', dark_mode=False, pad_x=12, height=26, left_x=None, solid=False):
    if font is None:
        font = get_font(11, 'bold')
        
    color_schemes_dark = {
        'red':     {'bg': (70, 10, 25, 255),   'border': (211, 17, 69, 255),   'text': (255, 128, 160, 255)},
        'green':   {'bg': (6, 50, 36, 255),    'border': (16, 185, 129, 255),  'text': (52, 211, 153, 255)},
        'blue':    {'bg': (15, 35, 75, 255),   'border': (59, 130, 246, 255),  'text': (147, 197, 253, 255)},
        'amber':   {'bg': (55, 35, 10, 255),   'border': (245, 158, 11, 255),  'text': (252, 211, 77, 255)},
        'purple':  {'bg': (45, 15, 65, 255),   'border': (168, 85, 247, 255),  'text': (216, 180, 254, 255)},
        'gray':    {'bg': (30, 41, 59, 255),   'border': (71, 85, 105, 255),   'text': (203, 213, 225, 255)},
    }
    color_schemes_light = {
        'red':     {'bg': (255, 241, 244, 255), 'border': (254, 205, 217, 255), 'text': (211, 17, 69, 255)},
        'green':   {'bg': (236, 253, 245, 255), 'border': (167, 243, 208, 255), 'text': (5, 150, 105, 255)},
        'blue':    {'bg': (239, 246, 255, 255), 'border': (191, 219, 254, 255), 'text': (29, 78, 216, 255)},
        'amber':   {'bg': (254, 243, 199, 255), 'border': (253, 230, 138, 255), 'text': (180, 83, 9, 255)},
        'purple':  {'bg': (243, 232, 255, 255), 'border': (216, 180, 254, 255), 'text': (126, 34, 206, 255)},
        'gray':    {'bg': (241, 245, 249, 255), 'border': (203, 213, 225, 255), 'text': (71, 85, 105, 255)},
    }
    
    table = color_schemes_dark if dark_mode else color_schemes_light
    scheme = table.get(theme, table['red'])
    
    bg_col = scheme['bg']
    border_col = scheme['border']
    text_col = scheme['text']
    
    if solid:
        if theme == 'red':
            bg_col = (211, 17, 69, 255)
            border_col = (211, 17, 69, 255)
            text_col = (255, 255, 255, 255)
        elif theme == 'green':
            bg_col = (16, 185, 129, 255)
            border_col = (16, 185, 129, 255)
            text_col = (255, 255, 255, 255)
        elif theme == 'blue':
            bg_col = (0, 81, 255, 255)
            border_col = (0, 81, 255, 255)
            text_col = (255, 255, 255, 255)
            
    bbox = draw.textbbox((0, 0), text, font=font)
    t_w = bbox[2] - bbox[0]
    total_w = t_w + pad_x * 2
    
    if left_x is not None:
        x1 = left_x
    elif cx is not None:
        x1 = cx - total_w // 2
    else:
        x1 = 0
        
    y1 = cy - height // 2
    x2 = x1 + total_w
    y2 = cy + height // 2
    
    draw.rounded_rectangle([x1, y1, x2, y2], radius=height // 2, fill=bg_col, outline=border_col, width=1)
    draw.text((x1 + pad_x, cy), text, font=font, fill=text_col, anchor='lm')
    return total_w

def draw_arrow(draw, p1, p2, col=AIA_RED, width=2, arrow_size=6):
    x1, y1 = p1
    x2, y2 = p2
    draw.line([(x1, y1), (x2, y2)], fill=col, width=width)
    if x1 == x2:
        if y2 > y1:
            draw.polygon([(x2 - arrow_size, y2 - arrow_size * 1.5), (x2 + arrow_size, y2 - arrow_size * 1.5), (x2, y2)], fill=col)
        else:
            draw.polygon([(x2 - arrow_size, y2 + arrow_size * 1.5), (x2 + arrow_size, y2 + arrow_size * 1.5), (x2, y2)], fill=col)
    elif y1 == y2:
        if x2 > x1:
            draw.polygon([(x2 - arrow_size * 1.5, y2 - arrow_size), (x2 - arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)
        else:
            draw.polygon([(x2 + arrow_size * 1.5, y2 - arrow_size), (x2 + arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)

def draw_slide_header(draw, slide_num, category_kr, title_bold, title_accent, subtitle_kr, right_badge=None, dark_mode=False):
    line_col = (40, 50, 68) if dark_mode else (226, 232, 240)
    draw.line([(100, 48), (1820, 48)], fill=line_col, width=1)
    
    badge_text = f"{slide_num:02d} {category_kr}"
    draw_pill_badge(draw, left_x=100, cy=78, text=badge_text, font=get_font(10.5, 'bold'), theme='red', dark_mode=dark_mode, pad_x=12, height=26)
    
    if right_badge:
        txt, theme = right_badge
        draw_pill_badge(draw, cx=1700, cy=78, text=txt, font=get_font(10.5, 'bold'), theme=theme, solid=True, dark_mode=dark_mode, pad_x=14, height=28)
        
    font_title = get_font(33, 'bold')
    w_bold = draw.textlength(title_bold, font=font_title)
    text_main_col = TEXT_DARK_MAIN if dark_mode else TEXT_LIGHT_MAIN
    text_accent_col = (255, 90, 130) if dark_mode else AIA_RED
    draw.text((100, 118), title_bold, font=font_title, fill=text_main_col)
    draw.text((100 + w_bold, 118), title_accent, font=font_title, fill=text_accent_col)
    
    sub_col = TEXT_DARK_SUB if dark_mode else TEXT_LIGHT_SUB
    draw.text((100, 166), subtitle_kr, font=get_font(14.5, 'regular'), fill=sub_col)

def draw_slide_footer(draw, slide_num, total_slides=12, dark_mode=False):
    line_col = (40, 50, 68) if dark_mode else (226, 232, 240)
    draw.line([(100, 995), (1820, 995)], fill=line_col, width=1)
    
    brand_col = (255, 90, 130) if dark_mode else AIA_RED
    draw.text((100, 1018), "AIA LIFE · AIA+ PHASE 2", font=get_font(11.5, 'bold'), fill=brand_col)
    meta_col = (100, 116, 139) if dark_mode else (148, 163, 184)
    draw.text((285, 1018), "·   고령자 친화 배리어프리 금융 UX  ·  Qi 글로벌 디자인 시스템 v3.3", font=get_font(11, 'medium'), fill=meta_col)
    draw.text((960, 1018), "금융위원회 가이드라인 100% 준수  ·  10대 코어 비대면 금융 서비스 초간편화", font=get_font(10.5, 'medium'), fill=meta_col, anchor='mt')
    
    page_col = (148, 163, 184) if dark_mode else (100, 116, 139)
    page_str = f"PAGE {slide_num:02d} / {total_slides:02d}"
    draw.text((1820, 1018), page_str, font=get_num_font(11.5, 'black'), fill=page_col, anchor='rt')

def draw_phone_mockup(base_img, screen_path, cx, cy, phone_w=280, phone_h=580, bezel=10, radius=38, dark_body=True):
    """
    Ultra-refined luxury smartphone frame.
    Guarantees 100% full-screen visibility including bottom CTA buttons and navigation bars.
    """
    body_col = (18, 22, 30) if dark_body else (240, 243, 248)
    rim_col = (70, 80, 98) if dark_body else (203, 213, 225)
    inner_bezel_col = (10, 12, 16)
    
    x1 = cx - phone_w // 2
    y1 = cy - phone_h // 2
    x2 = cx + phone_w // 2
    y2 = cy + phone_h // 2
    
    # 1. Multi-tier drop shadow for luxury depth
    shadow = Image.new('RGBA', (phone_w + 80, phone_h + 80), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([35, 35, phone_w + 45, phone_h + 45], radius=radius + 4, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    base_img.paste(shadow, (x1 - 40, y1 - 25), shadow)
    
    draw = ImageDraw.Draw(base_img)
    # 2. Outer phone chassis
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=body_col, outline=rim_col, width=2)
    
    # 3. Inner screen viewport
    sx1 = x1 + bezel
    sy1 = y1 + bezel
    sx2 = x2 - bezel
    sy2 = y2 - bezel
    sw = sx2 - sx1
    sh = sy2 - sy1
    draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=radius - bezel // 2, fill=inner_bezel_col)
    
    # 4. Fit Screen with strict CTA button preservation
    if screen_path and os.path.exists(screen_path):
        screen = Image.open(screen_path).convert('RGBA')
        
        # Scale to match height perfectly so all bottom content & CTA buttons are strictly visible
        scale_h = sh / screen.height
        fit_w = int(round(screen.width * scale_h))
        fit_h = sh
        
        # If scaled width exceeds sw slightly, scale to fit sw instead
        if fit_w > sw:
            scale_w = sw / screen.width
            fit_w = sw
            fit_h = int(round(screen.height * scale_w))
            
        screen_resized = screen.resize((fit_w, fit_h), Image.Resampling.LANCZOS)
        
        # Background fill matching bottom or header
        sample_y = min(screen_resized.height - 10, screen_resized.height - 1)
        bg_sample = screen_resized.getpixel((fit_w // 2, sample_y))
        bg_color = (bg_sample[0], bg_sample[1], bg_sample[2], 255) if len(bg_sample) >= 3 else (255, 255, 255, 255)
        
        screen_canvas = Image.new('RGBA', (sw, sh), bg_color)
        paste_x = (sw - fit_w) // 2
        paste_y = (sh - fit_h) // 2 if fit_h < sh else 0
        screen_canvas.paste(screen_resized, (paste_x, paste_y))
        
        # Screen mask with smooth corners
        mask = Image.new('L', (sw, sh), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([0, 0, sw, sh], radius=radius - bezel // 2 - 2, fill=255)
        
        base_img.paste(screen_canvas, (sx1, sy1), mask)
        
    # 5. Top Dynamic Island
    pill_w = int(sw * 0.28)
    pill_h = 13
    pill_x1 = cx - pill_w // 2
    pill_y1 = sy1 + 6
    draw.rounded_rectangle([pill_x1, pill_y1, pill_x1 + pill_w, pill_y1 + pill_h], radius=6, fill=(0, 0, 0, 230))
    # Camera dot
    draw.ellipse([cx + pill_w // 4 - 3, pill_y1 + 3, cx + pill_w // 4 + 3, pill_y1 + 9], fill=(22, 34, 52))
    
    # 6. Bottom Home Indicator Bar
    bar_w = int(sw * 0.35)
    bar_h = 4
    bar_y = sy2 - 7
    draw.rounded_rectangle([cx - bar_w // 2, bar_y, cx + bar_w // 2, bar_y + bar_h], radius=2, fill=(255, 255, 255, 175))
