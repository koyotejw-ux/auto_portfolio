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

# Editorial Korean Heritage & Cyber Han-Palette
# Crimson Imperial Red (#DC2626), Joseon Ink Navy (#0B0F19), Gold Amber (#F59E0B), Jade Mint (#10B981)
C_TITLE_WHITE = (248, 250, 252, 255)   # Slate-50 Pure White
C_RED_HERO    = (239, 68, 68, 255)     # Vibrant Imperial Crimson
C_RED_MUTED   = (252, 165, 165, 255)   # Red-300 Sub-accent
C_GOLD_ACC    = (245, 158, 11, 255)    # Joseon Royal Amber Gold
C_INDIGO_ACC  = (129, 140, 248, 255)   # Modern Indigo
C_TEXT_BODY   = (226, 232, 240, 255)   # Slate-200 Crisp Body Text
C_TEXT_MUTED  = (186, 198, 222, 255)   # Slate-300 Readable Secondary
C_GREEN_ACC   = (52, 211, 153, 255)    # Jade Mint Green
C_BORDER_RED  = (239, 68, 68, 90)      # Glass Card Outline Red Border
C_BG_CARD     = (15, 23, 42, 245)      # Glass Card Background (Slate 900)
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

def draw_pill_badge(draw, left_x, cy, text, font, theme='red', pad_x=14, height=28):
    w_text = draw.textlength(text, font=font)
    pill_w = int(w_text + pad_x * 2)
    top_y = int(cy - height / 2)
    bottom_y = int(cy + height / 2)
    
    if theme == 'red':
        bg_col = (239, 68, 68, 35)
        border_col = (239, 68, 68, 180)
        text_col = (252, 165, 165, 255)
    elif theme == 'gold':
        bg_col = (245, 158, 11, 35)
        border_col = (245, 158, 11, 180)
        text_col = (253, 230, 138, 255)
    elif theme == 'green':
        bg_col = (16, 185, 129, 35)
        border_col = (16, 185, 129, 180)
        text_col = (167, 243, 208, 255)
    else:
        bg_col = (99, 102, 241, 35)
        border_col = (99, 102, 241, 180)
        text_col = (199, 210, 254, 255)
        
    draw.rounded_rectangle([left_x, top_y, left_x + pill_w, bottom_y], radius=height//2, fill=bg_col, outline=border_col, width=1)
    draw.text((left_x + pad_x, top_y + (height - font.size) // 2 - 1), text, font=font, fill=text_col)
    return pill_w

def create_base_canvas(center_orbit=(1440, 520)):
    im = Image.new('RGBA', (W, H), (9, 12, 20, 255))
    draw = ImageDraw.Draw(im)
    
    # Atmospheric Background Ambient Mesh with Deep Imperial Red & Gold Auras
    aura1 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(aura1)
    d1.ellipse([center_orbit[0] - 460, center_orbit[1] - 460, center_orbit[0] + 460, center_orbit[1] + 460], fill=(185, 28, 28, 38))
    d1.ellipse([180, 220, 780, 820], fill=(180, 83, 9, 22))
    aura1 = aura1.filter(ImageFilter.GaussianBlur(110))
    im = Image.alpha_composite(im, aura1)
    
    draw = ImageDraw.Draw(im)
    
    # Precision Grid Network
    for x in range(100, W, 80):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 6), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 6), width=1)
        
    return im, draw

def draw_slide_header(draw, slide_idx, title, subtitle):
    # Top divider rule
    draw.line([(100, 52), (1820, 52)], fill=(239, 68, 68, 50), width=1)
    
    # Pill index
    idx_str = f"STEP {slide_idx:02d}"
    w_pill = draw_pill_badge(draw, left_x=100, cy=76, text=idx_str, font=get_font(12, 'bold'), theme='red', pad_x=14, height=28)
    
    # Category / Series Tag
    draw.text((100 + w_pill + 16, 68), "KOREAN HISTORY EDUTECH PLATFORM · UX/UI CASE STUDY", font=get_font(12.5, 'semibold'), fill=C_GOLD_ACC)
    
    # Page indicator
    page_txt = f"{slide_idx:02d} / 12"
    w_page = draw.textlength(page_txt, font=get_font(13, 'bold'))
    draw.text((1820 - w_page, 68), page_txt, font=get_font(13, 'bold'), fill=C_TEXT_MUTED)
    
    # Title & Subtitle
    draw.text((100, 116), title, font=get_font(34, 'black'), fill=C_TITLE_WHITE)
    draw.text((100, 162), subtitle, font=get_font(15, 'medium'), fill=C_TEXT_BODY)

def draw_slide_footer(draw, meta_tags=""):
    draw.line([(100, 1028), (1820, 1028)], fill=(255, 255, 255, 18), width=1)
    draw.text((100, 1042), "대한국사 (Korea History Quiz) · Product Design & Architecture by Jaewoong Jung", font=get_font(12, 'medium'), fill=C_TEXT_MUTED)
    if meta_tags:
        w_t = draw.textlength(meta_tags, font=get_font(12, 'semibold'))
        draw.text((1820 - w_t, 1042), meta_tags, font=get_font(12, 'semibold'), fill=C_GOLD_ACC)

def save_slide(im, slide_idx):
    fname = f"slide_{slide_idx:02d}.png"
    for d in OUT_DIRS:
        p = os.path.join(d, fname)
        im.save(p, 'PNG', optimize=True)
    print(f"Rendered: {fname}")

