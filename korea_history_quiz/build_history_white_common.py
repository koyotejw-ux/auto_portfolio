import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
OUT_DIRS = [
    'd:/097.flutter_project/auto_portfolio/korea_history_quiz/behance_slides',
]
for d in OUT_DIRS:
    os.makedirs(d, exist_ok=True)

MOCKUP_DIR = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/assets/iphone_mockups'
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

# High-Contrast Light Editorial Palette (Korean Heritage Light Mode)
# Pure White (#FFFFFF), Slate-50 (#F8FAFC), Brand Navy (#0F265C), Taegeuk Cobalt (#1D4ED8), Taegeuk Crimson (#E11D48), Amber Gold (#D97706), Celadon Jade (#059669)
C_TITLE_BLACK = (15, 23, 42, 255)     # Slate-900 Pure Deep Black
C_NAVY_HERO   = (15, 38, 92, 255)     # Brand Navy #0F265C
C_COBALT_HERO = (29, 78, 216, 255)    # Taegeuk Cobalt #1D4ED8
C_CRIMSON_HERO= (225, 29, 72, 255)    # Taegeuk Crimson #E11D48
C_AMBER_HERO  = (217, 119, 6, 255)     # Dancheong Amber #D97706
C_JADE_HERO   = (5, 150, 105, 255)    # Celadon Jade #059669
C_TEXT_BODY   = (51, 65, 85, 255)     # Slate-700 Crisp Readable Body Text
C_TEXT_MUTED  = (100, 116, 139, 255)  # Slate-500 Secondary Metadata
C_BORDER_LINE = (226, 232, 240, 255)  # Slate-200 Clean Border Line
C_BG_CARD     = (255, 255, 255, 255)  # Pure White Card
C_BG_CONTAINER= (248, 250, 252, 255)  # Slate-50 Clean Container Background

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

def draw_pill_badge(draw, left_x=None, cx=None, cy=None, text="", font=None, theme='cobalt', pad_x=12, height=28, radius=None):
    if font is None:
        font = get_font(11.5, 'bold')
    if radius is None:
        radius = height // 2
        
    COLOR_THEMES = {
        'cobalt':  {'bg': (239, 246, 255), 'border': (191, 219, 254), 'text': (29, 78, 216)},
        'crimson': {'bg': (255, 241, 242), 'border': (254, 205, 211), 'text': (225, 29, 72)},
        'amber':   {'bg': (254, 243, 199), 'border': (253, 230, 138), 'text': (217, 119, 6)},
        'jade':    {'bg': (236, 253, 245), 'border': (167, 243, 208), 'text': (5, 150, 105)},
        'slate':   {'bg': (241, 245, 249), 'border': (203, 213, 225), 'text': (71, 85, 105)},
    }
    th = COLOR_THEMES.get(theme, COLOR_THEMES['cobalt'])
    w_text = draw.textlength(text, font=font)
    pill_w = int(w_text + pad_x * 2)
    
    if left_x is None and cx is not None:
        left_x = int(cx - pill_w / 2)
    top_y = int(cy - height / 2)
    bottom_y = int(cy + height / 2)
    
    draw.rounded_rectangle([left_x, top_y, left_x + pill_w, bottom_y], radius=radius, fill=th['bg'], outline=th['border'], width=1)
    draw.text((left_x + pad_x, top_y + (height - font.size) // 2 - 1), text, font=font, fill=th['text'])
    return pill_w

def create_base_canvas(center_orbit=(1440, 520)):
    # Pristine Light Editorial Canvas: Slate-50 Clean Canvas (#F8FAFC)
    im = Image.new('RGB', (W, H), (248, 250, 252))
    
    # Atmospheric Background Ambient Mesh with Soft Cobalt and Crimson Tints
    aura1 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(aura1)
    d1.ellipse([center_orbit[0] - 400, center_orbit[1] - 380, center_orbit[0] + 400, center_orbit[1] + 380], fill=(219, 234, 254, 180)) # Soft Cobalt Blue Tint
    d1.ellipse([200, 150, 750, 700], fill=(255, 228, 230, 130)) # Soft Crimson Tint
    aura1 = aura1.filter(ImageFilter.GaussianBlur(120))
    
    im_rgba = im.convert('RGBA')
    im_composite = Image.alpha_composite(im_rgba, aura1)
    im = im_composite.convert('RGB')
    
    draw = ImageDraw.Draw(im)
    
    # Subtle Crisp Grid Network (Slate-200, 0.05 opacity)
    for x in range(100, W, 80):
        draw.line([(x, 0), (x, H)], fill=(226, 232, 240), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(226, 232, 240), width=1)
        
    return im, draw

def draw_slide_header(draw, slide_idx, title, subtitle):
    # Top divider rule
    draw.line([(100, 52), (1820, 52)], fill=C_BORDER_LINE, width=1)
    
    # Pill index
    idx_str = f"STEP {slide_idx:02d}"
    w_pill = draw_pill_badge(draw, left_x=100, cy=76, text=idx_str, font=get_font(12, 'bold'), theme='cobalt', pad_x=14, height=28)
    
    # Category / Series Tag
    draw.text((100 + w_pill + 16, 68), "KOREAN HERITAGE EDUTECH PLATFORM · UX/UI CASE STUDY", font=get_font(12.5, 'semibold'), fill=C_AMBER_HERO)
    
    # Page indicator
    page_txt = f"{slide_idx:02d} / 12"
    w_page = draw.textlength(page_txt, font=get_font(13, 'bold'))
    draw.text((1820 - w_page, 68), page_txt, font=get_font(13, 'bold'), fill=C_TEXT_MUTED)
    
    # Title & Subtitle
    draw.text((100, 114), title, font=get_font(34, 'black'), fill=C_TITLE_BLACK)
    draw.text((100, 160), subtitle, font=get_font(15, 'medium'), fill=C_TEXT_BODY)

def draw_slide_footer(draw, meta_tags=""):
    draw.line([(100, 1028), (1820, 1028)], fill=C_BORDER_LINE, width=1)
    draw.text((100, 1042), "대한한국사 (Korea History Quiz) · Product Design & Architecture by Jaewoong Jung", font=get_font(12, 'medium'), fill=C_TEXT_MUTED)
    if meta_tags:
        w_t = draw.textlength(meta_tags, font=get_font(12, 'semibold'))
        draw.text((1820 - w_t, 1042), meta_tags, font=get_font(12, 'semibold'), fill=C_COBALT_HERO)

def save_slide(im, slide_idx):
    fname = f"slide_{slide_idx:02d}.png"
    for d in OUT_DIRS:
        p = os.path.join(d, fname)
        im.save(p, 'PNG', optimize=True)
    print(f"Rendered Light Slide: {fname}")

