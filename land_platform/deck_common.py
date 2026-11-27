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
BRAND_GREEN = (0, 198, 95)        # Primary-500 #00C65F
BRAND_DARK = (4, 120, 87)          # Dark Green
BRAND_LIGHT = (83, 232, 130)       # Primary-2 #53E882
BRAND_TEAL = (0, 157, 220)         # Secondary #009DDC
AIA_RED = BRAND_GREEN              # Primary Accent

BG_LIGHT = (255, 255, 255)
BG_DARK = (15, 23, 42)
CARD_LIGHT = (255, 255, 255)
CARD_DARK = (30, 41, 59)
BORDER_LIGHT = (226, 232, 240)
BORDER_DARK = (51, 65, 85)

TEXT_LIGHT_MAIN = (15, 23, 42)     # #0F172A
TEXT_LIGHT_SUB = (100, 116, 139)   # #64748B
TEXT_DARK_MAIN = (248, 250, 252)
TEXT_DARK_SUB = (148, 163, 184)

def get_font(size, weight='bold'):
    candidates = {
        'black': ["Pretendard-Black.otf", "Pretendard-Black.ttf", "malgunbd.ttf", "arialbd.ttf"],
        'bold': ["Pretendard-Bold.otf", "Pretendard-Bold.ttf", "malgunbd.ttf", "arialbd.ttf"],
        'medium': ["Pretendard-Medium.otf", "Pretendard-Medium.ttf", "malgun.ttf", "arial.ttf"],
        'regular': ["Pretendard-Regular.otf", "Pretendard-Regular.ttf", "malgun.ttf", "arial.ttf"],
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

def get_num_font(size, weight='black'):
    return get_font(size, weight=weight)

def wrap_text(text, font, max_width, draw):
    lines = []
    paragraphs = text.split('\n')
    for para in paragraphs:
        if not para.strip():
            lines.append("")
            continue
        words = para.split(' ')
        cur_line = ""
        for word in words:
            test_line = f"{cur_line} {word}".strip()
            if draw.textlength(test_line, font=font) <= max_width:
                cur_line = test_line
            else:
                if cur_line:
                    lines.append(cur_line)
                cur_line = word
        if cur_line:
            lines.append(cur_line)
    return lines

def draw_pill_badge(draw, cx=None, cy=0, text="", font=None, theme='green', dark_mode=False, pad_x=12, height=26, left_x=None, solid=False):
    themes = {
        'green': {
            'bg': (0, 198, 95) if solid else ((0, 198, 95, 25) if dark_mode else (238, 253, 244)),
            'border': (0, 198, 95) if solid else (0, 198, 95),
            'text': (255, 255, 255) if solid else (0, 198, 95)
        },
        'red': {
            'bg': (211, 17, 69) if solid else (255, 241, 242),
            'border': (211, 17, 69),
            'text': (255, 255, 255) if solid else (211, 17, 69)
        },
        'blue': {
            'bg': (37, 99, 235) if solid else (239, 246, 255),
            'border': (37, 99, 235),
            'text': (255, 255, 255) if solid else (37, 99, 235)
        },
        'gray': {
            'bg': (241, 245, 249),
            'border': (203, 213, 225),
            'text': (100, 116, 139)
        }
    }
    th = themes.get(theme, themes['green'])
    tw = draw.textlength(text, font=font)
    bw = tw + pad_x * 2
    if left_x is not None:
        x1 = left_x
        x2 = x1 + bw
    else:
        x1 = cx - bw // 2
        x2 = cx + bw // 2
    y1 = cy - height // 2
    y2 = cy + height // 2
    draw.rounded_rectangle([x1, y1, x2, y2], radius=height // 2, fill=th['bg'], outline=th['border'], width=1)
    draw.text(((x1 + x2) // 2, cy), text, font=font, fill=th['text'], anchor='mm')
    return bw

def draw_arrow(draw, p1, p2, col=BRAND_GREEN, width=2, arrow_size=6):
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
    draw_pill_badge(draw, left_x=100, cy=78, text=badge_text, font=get_font(10.5, 'bold'), theme='green', dark_mode=dark_mode, pad_x=12, height=26)
    
    if right_badge:
        txt, theme = right_badge
        draw_pill_badge(draw, cx=1700, cy=78, text=txt, font=get_font(10.5, 'bold'), theme=theme, solid=True, dark_mode=dark_mode, pad_x=14, height=28)
        
    font_title = get_font(33, 'bold')
    w_bold = draw.textlength(title_bold, font=font_title)
    text_main_col = TEXT_DARK_MAIN if dark_mode else TEXT_LIGHT_MAIN
    text_accent_col = BRAND_LIGHT if dark_mode else BRAND_GREEN
    draw.text((100, 118), title_bold, font=font_title, fill=text_main_col)
    draw.text((100 + w_bold, 118), title_accent, font=font_title, fill=text_accent_col)
    
    sub_col = TEXT_DARK_SUB if dark_mode else TEXT_LIGHT_SUB
    draw.text((100, 166), subtitle_kr, font=get_font(14.5, 'regular'), fill=sub_col)

def draw_slide_footer(draw, slide_num, total_slides=12, dark_mode=False):
    line_col = (40, 50, 68) if dark_mode else (226, 232, 240)
    draw.line([(100, 995), (1820, 995)], fill=line_col, width=1)
    
    brand_col = BRAND_LIGHT if dark_mode else BRAND_GREEN
    draw.text((100, 1018), "FARMINGSYS · B2B PROPTECH", font=get_font(11.5, 'bold'), fill=brand_col)
    meta_col = (100, 116, 139) if dark_mode else (148, 163, 184)
    draw.text((310, 1018), "·   공간 GIS 빅데이터 & 토지개발 사업 타당성 분석 플랫폼", font=get_font(11, 'medium'), fill=meta_col)
    draw.text((960, 1018), "12대 공공 데이터 실시간 파싱  ·  스마트 시설배치 & 정량 경제성 분석 시뮬레이션", font=get_font(10.5, 'medium'), fill=meta_col, anchor='mt')
    
    page_col = (148, 163, 184) if dark_mode else (100, 116, 139)
    page_str = f"PAGE {slide_num:02d} / {total_slides:02d}"
    draw.text((1820, 1018), page_str, font=get_num_font(11.5, 'black'), fill=page_col, anchor='rt')

def draw_browser_mockup(base_img, screen_path, x, y, w, h, title="FARMINGSYS ENTERPRISE · GIS CLOUD", url="https://farmingsys.io/workspace/land-analysis"):
    draw = ImageDraw.Draw(base_img)
    # Browser window container shadow/outline
    header_h = 36
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    
    # Window traffic light buttons
    btn_y = y + header_h // 2
    draw.ellipse([x + 16, btn_y - 5, x + 26, btn_y + 5], fill=(239, 68, 68))
    draw.ellipse([x + 32, btn_y - 5, x + 42, btn_y + 5], fill=(245, 158, 11))
    draw.ellipse([x + 48, btn_y - 5, x + 58, btn_y + 5], fill=(16, 185, 129))
    
    # URL address bar
    url_box_w = min(420, w - 240)
    url_x = x + 75
    draw.rounded_rectangle([url_x, y + 7, url_x + url_box_w, y + header_h - 7], radius=6, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    draw.text((url_x + 10, btn_y), "🔒 " + url, font=get_font(10, 'medium'), fill=(148, 163, 184), anchor='lm')
    
    # Title in center
    draw.text((x + w - 20, btn_y), title, font=get_font(10.5, 'bold'), fill=(100, 116, 139), anchor='rm')
    
    # Inner viewport screen
    if os.path.exists(screen_path):
        s_img = Image.open(screen_path).convert('RGBA')
        vp_w = w - 4
        vp_h = h - header_h - 2
        scale = min(vp_w / s_img.width, vp_h / s_img.height)
        nw = int(s_img.width * scale)
        nh = int(s_img.height * scale)
        s_res = s_img.resize((nw, nh), Image.Resampling.LANCZOS)
        
        # Center in viewport
        px = x + 2 + (vp_w - nw) // 2
        py = y + header_h + (vp_h - nh) // 2
        base_img.paste(s_res, (px, py), s_res)
    else:
        draw.text((x + w//2, y + h//2), "Mockup Screen Asset", font=get_font(14, 'bold'), fill=(148, 163, 184), anchor='mm')

