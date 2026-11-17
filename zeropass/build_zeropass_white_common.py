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

# High-Contrast Light Editorial Palette (Exact 1:1 Matching Smart DCA)
C_TITLE_BLACK = (15, 23, 42, 255)     # Slate-900 Pure Deep Black
C_BLUE_HERO   = (0, 81, 255, 255)     # Electric Brand Blue (Same as Smart DCA)
C_CYAN_ACCENT = (8, 145, 178, 255)    # Cyan-600
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

def draw_pill_badge(draw, left_x=None, cx=None, cy=None, text="", font=None, theme='blue', has_dot=False, dark_mode=False, solid=False, pad_x=10, height=24, radius=None):
    if font is None:
        font = get_font(11, 'bold')
    if radius is None:
        radius = height // 2
        
    COLOR_THEMES_LIGHT = {
        'blue':   {'bg': (239, 246, 255), 'border': (191, 219, 254), 'text': (0, 81, 255),   'dot': (0, 81, 255)},
        'cyan':   {'bg': (236, 254, 255), 'border': (165, 243, 252), 'text': (8, 145, 178),  'dot': (8, 145, 178)},
        'green':  {'bg': (236, 253, 245), 'border': (167, 243, 208), 'text': (16, 185, 129), 'dot': (16, 185, 129)},
        'amber':  {'bg': (254, 243, 199), 'border': (253, 230, 138), 'text': (217, 119, 6),  'dot': (217, 119, 6)},
        'red':    {'bg': (254, 242, 242), 'border': (254, 202, 202), 'text': (220, 38, 38),  'dot': (220, 38, 38)},
        'slate':  {'bg': (241, 245, 249), 'border': (203, 213, 225), 'text': (71, 85, 105),  'dot': (71, 85, 105)},
    }
    
    COLOR_THEMES_DARK = {
        'blue':   {'bg': (18, 38, 77),    'border': (30, 58, 110),   'text': (56, 189, 248),  'dot': (56, 189, 248)},
        'cyan':   {'bg': (12, 44, 58),    'border': (18, 68, 88),    'text': (34, 211, 238),  'dot': (34, 211, 238)},
        'green':  {'bg': (10, 46, 32),    'border': (16, 75, 48),    'text': (52, 211, 153),  'dot': (52, 211, 153)},
        'amber':  {'bg': (45, 34, 12),    'border': (72, 54, 18),    'text': (251, 191, 36),  'dot': (251, 191, 36)},
        'red':    {'bg': (48, 18, 18),    'border': (78, 28, 28),    'text': (248, 113, 113), 'dot': (248, 113, 113)},
        'slate':  {'bg': (26, 34, 48),    'border': (38, 50, 70),    'text': (148, 163, 184), 'dot': (148, 163, 184)},
    }
    
    themes = COLOR_THEMES_DARK if dark_mode else COLOR_THEMES_LIGHT
    scheme = themes.get(theme, themes['blue'])
    
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    dot_w = 12 if has_dot else 0
    bw = tw + pad_x * 2 + dot_w
    bh = height
    
    if cx is not None:
        bx1 = cx - bw // 2
    else:
        bx1 = left_x
    bx2 = bx1 + bw
    by1 = cy - bh // 2
    by2 = by1 + bh
    
    bg_col = scheme['text'] if solid else scheme['bg']
    border_col = scheme['text'] if solid else scheme['border']
    text_col = (255, 255, 255) if solid else scheme['text']
    
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=radius, fill=bg_col, outline=border_col, width=1)
    
    tx = bx1 + pad_x + dot_w
    if cx is not None:
        draw.text((cx + dot_w // 2, cy), text, font=font, anchor='mm', fill=text_col)
    else:
        target_top = by1 + (bh - th) / 2.0
        draw.text((tx - bbox[0], target_top - bbox[1]), text, font=font, fill=text_col)
        
    if has_dot:
        dot_x = bx1 + pad_x + 4
        dot_y = cy
        draw.ellipse([dot_x - 3, dot_y - 3, dot_x + 3, dot_y + 3], fill=scheme['dot'])
        
    return bx1, by1, bx2, by2

def draw_slide_header(draw, slide_num, category_en, title_black, title_blue, subtitle_kr, right_badge=None, dark_mode=False):
    line_col = (40, 53, 72) if dark_mode else (226, 232, 240)
    draw.line([(100, 52), (1820, 52)], fill=line_col, width=1)
    
    badge_text = f"{slide_num:02d} {category_en.upper()}"
    draw_pill_badge(draw, left_x=100, cy=78, text=badge_text, font=get_font(10.5, 'bold'), theme='blue', has_dot=False, dark_mode=dark_mode, pad_x=10, height=26)
    
    if right_badge:
        txt, theme = right_badge
        draw_pill_badge(draw, cx=1700, cy=78, text=txt, font=get_font(10.5, 'bold'), theme=theme, solid=True, dark_mode=dark_mode, pad_x=14, height=28)
        
    font_title = get_font(35, 'bold')
    w_black = draw.textlength(title_black, font=font_title)
    text_main_col = (255, 255, 255) if dark_mode else (15, 23, 42)
    text_blue_col = (56, 189, 248) if dark_mode else (0, 81, 255)
    draw.text((100, 116), title_black, font=font_title, fill=text_main_col)
    draw.text((100 + w_black, 116), title_blue, font=font_title, fill=text_blue_col)
    
    sub_col = (148, 163, 184) if dark_mode else (71, 85, 105)
    draw.text((100, 164), subtitle_kr, font=get_font(14.5, 'regular'), fill=sub_col)

def draw_slide_footer(draw, slide_num, total_slides=12, dark_mode=False):
    line_col = (40, 53, 72) if dark_mode else (226, 232, 240)
    draw.line([(100, 995), (1820, 995)], fill=line_col, width=1)
    
    brand_col = (56, 189, 248) if dark_mode else (0, 81, 255)
    draw.text((100, 1018), "CHECK & PAY (ZEROPASS)", font=get_font(11, 'bold'), fill=brand_col)
    meta_col = (100, 116, 139) if dark_mode else (148, 163, 184)
    draw.text((270, 1018), "·   Behance Enterprise Case Study  ·  Smart Attendance & Ledger Vault", font=get_font(11, 'medium'), fill=meta_col)
    draw.text((960, 1018), "Flutter Mobile & Tablet  ·  100% On-Device SQLite  ·  Google Play Live", font=get_font(10.5, 'medium'), fill=meta_col, anchor='mt')
    
    page_col = (148, 163, 184) if dark_mode else (100, 116, 139)
    page_str = f"PAGE {slide_num:02d} / {total_slides:02d}"
    draw.text((1820, 1018), page_str, font=get_num_font(11.5, 'black'), fill=page_col, anchor='rt')

def draw_donut_chart_on_base(base, cx, cy, r_outer, r_inner, percentage, col_fill=(220, 38, 38), col_track=(241, 245, 249)):
    """Renders a super-sampled anti-aliased radial donut chart onto the base image."""
    scale = 4
    size_ss = int((r_outer * 2 + 16) * scale)
    chart_ss = Image.new('RGBA', (size_ss, size_ss), (0, 0, 0, 0))
    d_ss = ImageDraw.Draw(chart_ss)
    
    center_ss = size_ss // 2
    ro_ss = r_outer * scale
    ri_ss = r_inner * scale
    
    box_outer = [center_ss - ro_ss, center_ss - ro_ss, center_ss + ro_ss, center_ss + ro_ss]
    d_ss.ellipse(box_outer, fill=col_track)
    
    start_angle = -90
    sweep_angle = (percentage / 100.0) * 360.0
    end_angle = start_angle + sweep_angle
    d_ss.pieslice(box_outer, start=start_angle, end=end_angle, fill=col_fill)
    
    box_inner = [center_ss - ri_ss, center_ss - ri_ss, center_ss + ri_ss, center_ss + ri_ss]
    d_ss.ellipse(box_inner, fill=(0, 0, 0, 0))
    
    chart = chart_ss.resize((int(r_outer * 2 + 16), int(r_outer * 2 + 16)), Image.Resampling.LANCZOS)
    paste_x = int(round(cx - (r_outer * 2 + 16) / 2))
    paste_y = int(round(cy - (r_outer * 2 + 16) / 2))
    base.paste(chart, (paste_x, paste_y), chart)

def draw_diamond(draw, cx, cy, w, h, fill, outline, width=2):
    pts = [
        (cx, cy - h // 2),
        (cx + w // 2, cy),
        (cx, cy + h // 2),
        (cx - w // 2, cy)
    ]
    draw.polygon(pts, fill=fill, outline=outline)

def draw_arrow(draw, p1, p2, col=(100, 116, 139), width=2, arrow_size=6):
    x1, y1 = p1
    x2, y2 = p2
    draw.line([(x1, y1), (x2, y2)], fill=col, width=width)
    if x1 == x2: # Vertical
        if y2 > y1: # Down
            draw.polygon([(x2 - arrow_size, y2 - arrow_size * 1.5), (x2 + arrow_size, y2 - arrow_size * 1.5), (x2, y2)], fill=col)
        else: # Up
            draw.polygon([(x2 - arrow_size, y2 + arrow_size * 1.5), (x2 + arrow_size, y2 + arrow_size * 1.5), (x2, y2)], fill=col)
    elif y1 == y2: # Horizontal
        if x2 > x1: # Right
            draw.polygon([(x2 - arrow_size * 1.5, y2 - arrow_size), (x2 - arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)
        else: # Left
            draw.polygon([(x2 + arrow_size * 1.5, y2 - arrow_size), (x2 + arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)

def draw_dashed_line(draw, p1, p2, col=(0, 82, 255), width=2, dash_len=4, gap_len=3):
    width = int(round(width))
    x1, y1 = p1
    x2, y2 = p2
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist == 0:
        return
    step = dash_len + gap_len
    num_steps = int(dist // step)
    for i in range(num_steps):
        s = i * step
        e = s + dash_len
        sx = x1 + (x2 - x1) * (s / dist)
        sy = y1 + (y2 - y1) * (s / dist)
        ex = x1 + (x2 - x1) * (min(e, dist) / dist)
        ey = y1 + (y2 - y1) * (min(e, dist) / dist)
        draw.line([(sx, sy), (ex, ey)], fill=col, width=width)

def draw_dashed_arrow(draw, p1, p2, col=(0, 82, 255), width=2, dash_len=4, gap_len=3, arrow_size=5):
    draw_dashed_line(draw, p1, p2, col, width, dash_len, gap_len)
    x1, y1 = p1
    x2, y2 = p2
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

def draw_behavior_slider(draw, x, y, w, label, left_txt, right_txt, ratio, theme='blue'):
    """
    Renders an editorial behavior spectrum slider track with active segment and circular marker dot.
    """
    theme_colors = {
        'blue': {'active': (0, 82, 255), 'dot': (0, 82, 255)},
        'amber': {'active': (217, 119, 6), 'dot': (217, 119, 6)},
        'green': {'active': (16, 185, 129), 'dot': (16, 185, 129)},
        'cyan': {'active': (6, 182, 212), 'dot': (6, 182, 212)},
        'purple': {'active': (124, 58, 237), 'dot': (124, 58, 237)},
    }
    col = theme_colors.get(theme, theme_colors['blue'])
    
    draw.text((x, y), label, font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    draw.text((x + 75, y + 1), left_txt, font=get_font(9, 'medium'), fill=(100, 116, 139))
    r_bbox = draw.textbbox((0, 0), right_txt, font=get_font(9, 'medium'))
    r_w = r_bbox[2] - r_bbox[0]
    draw.text((x + w - r_w, y + 1), right_txt, font=get_font(9, 'medium'), fill=(100, 116, 139))
    
    track_x = x + 125
    track_w = w - 135 - r_w
    track_y = y + 7
    
    draw.rounded_rectangle([track_x, track_y, track_x + track_w, track_y + 4], radius=2, fill=(226, 232, 240))
    active_w = int(round(track_w * max(0.0, min(1.0, ratio))))
    draw.rounded_rectangle([track_x, track_y, track_x + active_w, track_y + 4], radius=2, fill=col['active'])
    
    dot_cx = track_x + active_w
    dot_cy = track_y + 2
    r = 5
    draw.ellipse([dot_cx - r - 1, dot_cy - r - 1, dot_cx + r + 1, dot_cy + r + 1], fill=(255, 255, 255))
    draw.ellipse([dot_cx - r, dot_cy - r, dot_cx + r, dot_cy + r], fill=col['dot'])

def save_slide(img, num):
    for d in OUT_DIRS:
        img.save(f"{d}/slide_{num:02d}.png", quality=100)
    print(f"Slide {num:02d} saved to all target directories.")
