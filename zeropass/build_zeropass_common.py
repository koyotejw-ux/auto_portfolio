import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
OUT_DIRS = [
    'd:/097.flutter_project/zeropass/portfolio/behance_slides',
    'd:/097.flutter_project/auto_portfolio/zeropass/behance_slides'
]
for d in OUT_DIRS:
    os.makedirs(d, exist_ok=True)

MOCKUP_DIR = 'd:/097.flutter_project/auto_portfolio/zeropass/assets/iphone_mockups'
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

# High-Contrast ZeroPass Design System Semantic Palette (Cyber Blue & Indigo Vault Theme)
C_TITLE_WHITE = (248, 250, 252, 255)   # Slate-50 Pure White
C_CYAN_HERO   = (0, 210, 255, 255)     # Electric Cyber Cyan Primary
C_CYAN_MUTED  = (103, 232, 249, 255)   # Cyan-300 Sub-accent
C_INDIGO_ACC  = (129, 140, 248, 255)   # Indigo-400
C_TEXT_BODY   = (226, 232, 240, 255)   # Slate-200 Crisp Body Text
C_TEXT_MUTED  = (186, 198, 222, 255)   # Slate-300 Readable Secondary
C_GREEN_ACC   = (52, 211, 153, 255)    # Emerald Jade Green
C_RED_ACC     = (255, 140, 140, 255)   # Coral Alert Red
C_BORDER_CYAN = (0, 210, 255, 80)      # Glass Card Outline Cyan Border
C_BG_CARD     = (15, 23, 42, 240)      # Glass Card Background (Slate 900)
C_BG_CONTAINER= (24, 32, 54, 255)      # Inner Container Background

def wrap_text_by_words(text, font, max_width, draw):
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

def draw_pill_badge(draw, cx=None, cy=0, text="", font=None, theme='cyan', has_dot=False, pad_x=12, height=28, left_x=None, solid=False):
    if font is None:
        font = get_font(10.5, 'bold')
        
    color_schemes = {
        'cyan':   {'bg': (10, 36, 48, 255),   'border': (0, 210, 255, 220),   'text': (0, 210, 255, 255)},
        'indigo': {'bg': (28, 28, 60, 255),   'border': (129, 140, 248, 220), 'text': (165, 180, 252, 255)},
        'green':  {'bg': (12, 42, 30, 255),   'border': (16, 185, 129, 220),  'text': (52, 211, 153, 255)},
        'red':    {'bg': (48, 16, 24, 255),   'border': (239, 68, 68, 220),   'text': (255, 140, 140, 255)},
        'slate':  {'bg': (20, 26, 42, 255),   'border': (100, 116, 139, 200), 'text': (203, 213, 225, 255)},
    }
    color_schemes_solid = {
        'cyan':   {'bg': (0, 210, 255, 255),   'border': (0, 210, 255, 255),   'text': (11, 15, 25, 255)},
        'indigo': {'bg': (129, 140, 248, 255), 'border': (129, 140, 248, 255), 'text': (11, 15, 25, 255)},
        'green':  {'bg': (52, 211, 153, 255),  'border': (16, 185, 129, 255),  'text': (11, 15, 25, 255)},
        'red':    {'bg': (248, 113, 113, 255), 'border': (239, 68, 68, 255),   'text': (11, 15, 25, 255)},
        'slate':  {'bg': (148, 163, 184, 255), 'border': (203, 213, 225, 255), 'text': (11, 15, 25, 255)},
    }
    scheme = color_schemes_solid.get(theme, color_schemes_solid['cyan']) if solid else color_schemes.get(theme, color_schemes['cyan'])
    
    tw = draw.textlength(text, font=font)
    bw = int(round(tw + pad_x * 2))
    bh = int(round(height))
    
    if left_x is not None:
        bx1 = int(round(left_x))
        bx2 = bx1 + bw
        cx = (bx1 + bx2) / 2.0
    else:
        bx1 = int(round(cx - bw / 2.0))
        bx2 = bx1 + bw
        
    by1 = int(round(cy - bh / 2.0))
    by2 = by1 + bh
    
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=bh // 2, fill=scheme['bg'], outline=scheme['border'], width=1)
    draw.text((cx, cy), text, font=font, anchor='mm', fill=scheme['text'])
    return bx1, by1, bx2, by2

def create_base_canvas(center_orbit=(1480, 520)):
    base = Image.new('RGBA', (W, H), (11, 15, 25, 255)) # Dark Navy
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([center_orbit[0] - 420, center_orbit[1] - 420, center_orbit[0] + 380, center_orbit[1] + 380], fill=(0, 210, 255, 28))
    gw.ellipse([center_orbit[0] - 250, center_orbit[1] - 250, center_orbit[0] + 320, center_orbit[1] + 420], fill=(99, 102, 241, 32))
    gw.ellipse([100, 600, 750, 1050], fill=(0, 210, 255, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    
    draw = ImageDraw.Draw(base)
    for r in [280, 420, 560]:
        draw.ellipse([center_orbit[0] - r, center_orbit[1] - r, center_orbit[0] + r, center_orbit[1] + r], outline=(0, 210, 255, 15), width=1)
        
    draw.line([(100, 52), (1820, 52)], fill=(0, 210, 255, 40), width=1)
    draw.line([(100, 995), (1820, 995)], fill=(0, 210, 255, 40), width=1)
    return base, draw

def draw_slide_header(draw, slide_num, category_en, title_white, title_cyan, subtitle_kr, right_badge=None):
    draw.line([(100, 52), (1820, 52)], fill=(0, 210, 255, 40), width=1)
    badge_text = f"{slide_num:02d} {category_en.upper()}"
    draw_pill_badge(draw, left_x=100, cy=78, text=badge_text, font=get_font(10.5, 'bold'), theme='cyan', pad_x=10, height=26)
    
    if right_badge:
        txt, theme = right_badge
        draw_pill_badge(draw, cx=1700, cy=78, text=txt, font=get_font(11, 'extrabold'), theme=theme, solid=True, pad_x=14, height=28)
        
    font_title = get_font(34, 'bold')
    w_white = draw.textlength(title_white, font=font_title)
    draw.text((100, 116), title_white, font=font_title, fill=C_TITLE_WHITE)
    draw.text((100 + w_white, 116), title_cyan, font=font_title, fill=C_CYAN_HERO)
    draw.text((100, 164), subtitle_kr, font=get_font(14.5, 'medium'), fill=C_TEXT_BODY)

def draw_slide_footer(draw, slide_num, total_slides=12):
    draw.line([(100, 995), (1820, 995)], fill=(0, 210, 255, 60), width=1)
    draw.text((100, 1018), "ZEROPASS (체크앤페이)", font=get_font(11, 'bold'), fill=C_CYAN_HERO)
    draw.text((260, 1018), "·   Enterprise Case Study  ·  1초 원터치 출결 & 수납 관리 통합 솔루션", font=get_font(11, 'medium'), fill=C_TEXT_BODY)
    draw.text((960, 1018), "Smart SQLite Vault  ·  Zero-Latency Kiosk Engine  ·  Google Play 비공개 테스트", font=get_font(10.5, 'medium'), fill=C_TEXT_MUTED, anchor='mt')
    page_str = f"PAGE {slide_num:02d} / {total_slides:02d}"
    draw.text((1820, 1018), page_str, font=get_num_font(11.5, 'black'), fill=C_TEXT_BODY, anchor='rt')

def save_slide(img, num):
    if img.mode == 'RGBA':
        bg = Image.new('RGBA', img.size, (11, 15, 25, 255))
        final_img = Image.alpha_composite(bg, img).convert('RGB')
    else:
        final_img = img.convert('RGB')
        
    for d in OUT_DIRS:
        final_img.save(f"{d}/slide_{num:02d}.png", quality=100)
    print(f"Slide {num:02d} saved to all target directories.")

