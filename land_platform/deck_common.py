import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
BASE_DIR = r"d:\097.flutter_project\auto_portfolio\land_platform"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FIG_DIR = os.path.join(BASE_DIR, "fig_extracted")
OUT_DIR = os.path.join(BASE_DIR, "behance_slides")
os.makedirs(OUT_DIR, exist_ok=True)

# Colors
BRAND_GREEN = (5, 150, 105)       # Emerald Green #059669
BRAND_DARK = (4, 120, 87)          # Dark Green #047857
BRAND_LIGHT = (16, 185, 129)       # Mint Light #10B981
BRAND_BG_DARK = (10, 25, 20)       # Dark Navy Green #0A1914

BG_DARK = (15, 23, 42)             # Slate 900
BG_LIGHT = (248, 250, 252)         # Slate 50
CARD_DARK = (30, 41, 59)           # Slate 800
CARD_LIGHT = (255, 255, 255)
BORDER_DARK = (51, 65, 85)         # Slate 700
BORDER_LIGHT = (226, 232, 240)     # Slate 200

TEXT_DARK_MAIN = (248, 250, 252)
TEXT_DARK_SUB = (148, 163, 184)
TEXT_LIGHT_MAIN = (15, 23, 42)
TEXT_LIGHT_SUB = (100, 116, 139)

def get_font(size, weight='regular'):
    candidates = {
        'bold': ["Pretendard-Bold.otf", "Pretendard-Bold.ttf", "malgunbd.ttf", "arialbd.ttf"],
        'medium': ["Pretendard-Medium.otf", "Pretendard-Medium.ttf", "malgun.ttf", "arial.ttf"],
        'regular': ["Pretendard-Regular.otf", "Pretendard-Regular.ttf", "malgun.ttf", "arial.ttf"],
        'black': ["Pretendard-Black.otf", "Pretendard-ExtraBold.ttf", "malgunbd.ttf", "arialbd.ttf"],
    }
    font_paths = [
        r"C:\Windows\Fonts",
        r"C:\Users\coyot\AppData\Local\Microsoft\Windows\Fonts",
        os.path.join(r"d:\097.flutter_project\auto_portfolio", "assets", "fonts"),
    ]
    for fn in candidates.get(weight, candidates['regular']):
        for d in font_paths:
            fp = os.path.join(d, fn)
            if os.path.exists(fp):
                try:
                    return ImageFont.truetype(fp, int(size * 1.33))
                except Exception:
                    pass
    return ImageFont.load_default()

def draw_pill_badge(draw, left_x, cy, text, font, theme='green', pad_x=12, height=26):
    themes = {
        'green': {'bg': (5, 150, 105, 30), 'border': (5, 150, 105, 180), 'text': (5, 150, 105)},
        'dark_green': {'bg': (5, 150, 105, 50), 'border': (16, 185, 129, 200), 'text': (52, 211, 153)},
        'blue': {'bg': (37, 99, 235, 30), 'border': (37, 99, 235, 180), 'text': (37, 99, 235)},
        'gray': {'bg': (241, 245, 249), 'border': (203, 213, 225), 'text': (100, 116, 139)},
    }
    th = themes.get(theme, themes['green'])
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    bw = tw + pad_x * 2
    y1 = cy - height // 2
    y2 = cy + height // 2
    draw.rounded_rectangle([left_x, y1, left_x + bw, y2], radius=height//2, fill=th['bg'], outline=th['border'], width=1)
    draw.text((left_x + pad_x, cy), text, font=font, fill=th['text'], anchor='lm')
    return bw

def draw_slide_header(draw, slide_num, cat_title, eng_sub, kor_title, desc_text, dark_mode=False, right_badge=None):
    txt_main = TEXT_DARK_MAIN if dark_mode else TEXT_LIGHT_MAIN
    txt_sub = TEXT_DARK_SUB if dark_mode else TEXT_LIGHT_SUB
    
    # Top badge
    draw_pill_badge(draw, 80, 72, f"CASE STUDY · SLIDE {slide_num:02d}", get_font(11, 'bold'), theme='dark_green' if dark_mode else 'green')
    
    # Category tag
    draw.text((250, 72), f"LAND DEV PLATFORM  |  {cat_title}", font=get_font(12, 'bold'), fill=BRAND_LIGHT if dark_mode else BRAND_GREEN, anchor='lm')
    
    # Right Badge
    if right_badge:
        rb_text, rb_theme = right_badge
        draw_pill_badge(draw, W - 320, 72, rb_text, get_font(11, 'bold'), theme=rb_theme, pad_x=16)
        
    # Title
    draw.text((80, 125), kor_title, font=get_font(28, 'bold'), fill=txt_main)
    # Description
    draw.text((80, 172), desc_text, font=get_font(14, 'regular'), fill=txt_sub)
    
    # Divider
    border_col = BORDER_DARK if dark_mode else BORDER_LIGHT
    draw.line([(80, 210), (W - 80, 210)], fill=border_col, width=1)

def draw_slide_footer(draw, cur_page, total_pages=12, dark_mode=False):
    border_col = BORDER_DARK if dark_mode else BORDER_LIGHT
    txt_sub = TEXT_DARK_SUB if dark_mode else TEXT_LIGHT_SUB
    draw.line([(80, H - 65), (W - 80, H - 65)], fill=border_col, width=1)
    
    # Brand tag
    draw.text((80, H - 42), "FARMINGSYS · 토지개발사업 분석 플랫폼 B2B 클라우드 SaaS", font=get_font(11, 'bold'), fill=BRAND_LIGHT if dark_mode else BRAND_GREEN, anchor='lm')
    draw.text((W // 2, H - 42), "GIS 기반 공간 빅데이터 및 인허가·타당성 자동 분석 엔진", font=get_font(11, 'regular'), fill=txt_sub, anchor='mm')
    draw.text((W - 80, H - 42), f"{cur_page:02d} / {total_pages:02d}", font=get_font(12, 'bold'), fill=txt_sub, anchor='rm')
