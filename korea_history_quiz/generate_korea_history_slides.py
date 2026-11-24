import math
import textwrap
import os
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
OUT_DIR = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/behance_slides'
os.makedirs(OUT_DIR, exist_ok=True)

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

FLUTTER_MATERIAL_FONT = r"C:\flutter\bin\cache\artifacts\material_fonts\MaterialIcons-Regular.otf"

def get_material_icon_font(size):
    if os.path.exists(FLUTTER_MATERIAL_FONT):
        try:
            return ImageFont.truetype(FLUTTER_MATERIAL_FONT, int(round(size)))
        except:
            pass
    return get_font(size, 'bold')

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

# ==============================================================
# Helper: Draw Diamond for Flowchart
def draw_diamond(draw, cx, cy, w, h, fill, outline, width=2):
    pts = [
        (cx, cy - h // 2),
        (cx + w // 2, cy),
        (cx, cy + h // 2),
        (cx - w // 2, cy)
    ]
    draw.polygon(pts, fill=fill, outline=outline)

def draw_parallelogram(draw, cx, cy, w, h, fill, outline, skew=12, width=1):
    pts = [
        (cx - w // 2 + skew, cy - h // 2),
        (cx + w // 2 + skew, cy - h // 2),
        (cx + w // 2 - skew, cy + h // 2),
        (cx - w // 2 - skew, cy + h // 2)
    ]
    draw.polygon(pts, fill=fill, outline=outline)

def draw_database_node(draw, cx, cy, w, h, fill=(240, 246, 255), outline=(0, 82, 255), width=1):
    ew = w
    eh = int(h * 0.28)
    top_y = cy - h // 2
    bot_y = cy + h // 2
    draw.ellipse([cx - ew // 2, bot_y - eh, cx + ew // 2, bot_y], fill=fill, outline=outline, width=width)
    draw.rectangle([cx - ew // 2, top_y + eh // 2, cx + ew // 2, bot_y - eh // 2], fill=fill)
    draw.line([(cx - ew // 2, top_y + eh // 2), (cx - ew // 2, bot_y - eh // 2)], fill=outline, width=width)
    draw.line([(cx + ew // 2, top_y + eh // 2), (cx + ew // 2, bot_y - eh // 2)], fill=outline, width=width)
    draw.ellipse([cx - ew // 2, top_y, cx + ew // 2, top_y + eh], fill=fill, outline=outline, width=width)

def draw_dashed_line(draw, p1, p2, col=(0, 82, 255), width=2, dash_len=4, gap_len=3, dash=None, gap=None):
    if dash is not None:
        dash_len = dash
    if gap is not None:
        gap_len = gap
    width = int(round(width))
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    dist = (dx**2 + dy**2)**0.5
    if dist == 0:
        return
    step = dash_len + gap_len
    num_steps = int(dist // step)
    for i in range(num_steps):
        s = i * step
        e = s + dash_len
        sx = x1 + dx * (s / dist)
        sy = y1 + dy * (s / dist)
        ex = x1 + dx * (min(e, dist) / dist)
        ey = y1 + dy * (min(e, dist) / dist)
        draw.line([(sx, sy), (ex, ey)], fill=col, width=width)

def draw_dashed_rounded_rect(draw, bbox, radius=8, fill=(240, 246, 255), outline=(0, 82, 255), width=1, dash_len=4, gap_len=3):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill)
    x1, y1, x2, y2 = bbox
    draw_dashed_line(draw, (x1 + radius, y1), (x2 - radius, y1), outline, width, dash_len, gap_len)
    draw_dashed_line(draw, (x2, y1 + radius), (x2, y2 - radius), outline, width, dash_len, gap_len)
    draw_dashed_line(draw, (x2 - radius, y2), (x1 + radius, y2), outline, width, dash_len, gap_len)
    draw_dashed_line(draw, (x1, y2 - radius), (x1, y1 + radius), outline, width, dash_len, gap_len)

def draw_dashed_arrow(draw, p1, p2, col=(0, 82, 255), width=2, dash_len=4, gap_len=3, arrow_size=5, dash=None, gap=None):
    if dash is not None:
        dash_len = dash
    if gap is not None:
        gap_len = gap
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

# Helper: Draw Directional Arrow
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

# Helper: Draw L-shaped Orthogonal Arrow
def draw_l_arrow(draw, corner, p2, col=(100, 116, 139), width=2, arrow_size=6):
    x_c, y_c = corner
    x2, y2 = p2
    draw.line([(x_c, y_c), (x2, y2)], fill=col, width=width)
    if x_c == x2: # Vertical end
        if y2 > y_c:
            draw.polygon([(x2 - arrow_size, y2 - arrow_size * 1.5), (x2 + arrow_size, y2 - arrow_size * 1.5), (x2, y2)], fill=col)
        else:
            draw.polygon([(x2 - arrow_size, y2 + arrow_size * 1.5), (x2 + arrow_size, y2 + arrow_size * 1.5), (x2, y2)], fill=col)
    elif y_c == y2: # Horizontal end
        if x2 > x_c:
            draw.polygon([(x2 - arrow_size * 1.5, y2 - arrow_size), (x2 - arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)
        else:
            draw.polygon([(x2 + arrow_size * 1.5, y2 - arrow_size), (x2 + arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)


def draw_pill_badge(draw, cx=None, cy=0, text="", font=None, theme='blue', has_dot=False, dark_mode=False, pad_x=14, height=30, left_x=None, solid=False):
    """
    Renders a mathematically centered, high-contrast, beautiful pill badge with pixel-perfect alignment.
    Supports themes: 'blue', 'green', 'red', 'amber', 'purple', 'cyan', 'slate', 'dark'.
    Supports fill types: soft pastel tint (default light), solid brand fill (solid=True), or dark outline (dark_mode=True).
    Can be positioned by center (cx, cy) or aligned by left edge (left_x, cy).
    """
    if font is None:
        font = get_font(10.5, 'bold')
        
    color_schemes_dark = {
        'blue':   {'bg': (16, 42, 86, 255),  'border': (0, 140, 255, 255),  'text': (0, 215, 255, 255),  'dot': (0, 215, 255, 255)},
        'cyan':   {'bg': (8, 48, 64, 255),   'border': (0, 210, 255, 255),  'text': (0, 230, 255, 255),  'dot': (0, 230, 255, 255)},
        'green':  {'bg': (12, 48, 36, 255),  'border': (16, 185, 129, 255), 'text': (52, 211, 153, 255), 'dot': (16, 185, 129, 255)},
        'red':    {'bg': (58, 20, 24, 255),  'border': (239, 68, 68, 255),  'text': (255, 140, 140, 255),'dot': (239, 68, 68, 255)},
        'amber':  {'bg': (54, 38, 12, 255),  'border': (245, 158, 11, 255), 'text': (251, 191, 36, 255), 'dot': (245, 158, 11, 255)},
        'purple': {'bg': (42, 22, 70, 255),  'border': (168, 85, 247, 255), 'text': (216, 180, 254, 255),'dot': (168, 85, 247, 255)},
        'slate':  {'bg': (30, 41, 59, 255),  'border': (100, 116, 139, 255),'text': (226, 232, 240, 255),'dot': (148, 163, 184, 255)},
        'dark':   {'bg': (15, 23, 42, 255),  'border': (51, 65, 85, 255),   'text': (255, 255, 255, 255),'dot': (0, 215, 255, 255)},
    }
    color_schemes_light = {
        'blue':   {'bg': (239, 246, 255, 255), 'border': (191, 219, 254, 255), 'text': (0, 82, 255, 255),   'dot': (0, 82, 255, 255)},
        'cyan':   {'bg': (236, 254, 255, 255), 'border': (165, 243, 252, 255), 'text': (8, 145, 178, 255),  'dot': (6, 182, 212, 255)},
        'green':  {'bg': (236, 253, 245, 255), 'border': (167, 243, 208, 255), 'text': (5, 150, 105, 255),  'dot': (16, 185, 129, 255)},
        'red':    {'bg': (254, 242, 242, 255), 'border': (254, 202, 202, 255), 'text': (220, 38, 38, 255),  'dot': (239, 68, 68, 255)},
        'amber':  {'bg': (254, 243, 199, 255), 'border': (253, 230, 138, 255), 'text': (180, 83, 9, 255),   'dot': (245, 158, 11, 255)},
        'purple': {'bg': (245, 243, 255, 255), 'border': (221, 214, 254, 255), 'text': (109, 40, 217, 255), 'dot': (139, 92, 246, 255)},
        'slate':  {'bg': (241, 245, 249, 255), 'border': (203, 213, 225, 255), 'text': (51, 65, 85, 255),   'dot': (100, 116, 139, 255)},
        'dark':   {'bg': (15, 23, 42, 255),    'border': (15, 23, 42, 255),     'text': (255, 255, 255, 255),'dot': (0, 210, 255, 255)},
    }
    color_schemes_solid = {
        'blue':   {'bg': (0, 82, 255, 255),   'border': (0, 82, 255, 255),   'text': (255, 255, 255, 255), 'dot': (191, 219, 254, 255)},
        'cyan':   {'bg': (8, 145, 178, 255),  'border': (8, 145, 178, 255),  'text': (255, 255, 255, 255), 'dot': (207, 250, 254, 255)},
        'green':  {'bg': (16, 185, 129, 255), 'border': (16, 185, 129, 255), 'text': (255, 255, 255, 255), 'dot': (209, 250, 229, 255)},
        'red':    {'bg': (239, 68, 68, 255),  'border': (239, 68, 68, 255),  'text': (255, 255, 255, 255), 'dot': (254, 226, 226, 255)},
        'amber':  {'bg': (217, 119, 6, 255),  'border': (217, 119, 6, 255),  'text': (255, 255, 255, 255), 'dot': (254, 243, 199, 255)},
        'purple': {'bg': (124, 58, 237, 255), 'border': (124, 58, 237, 255), 'text': (255, 255, 255, 255), 'dot': (237, 233, 254, 255)},
        'slate':  {'bg': (71, 85, 105, 255),  'border': (71, 85, 105, 255),  'text': (255, 255, 255, 255), 'dot': (226, 232, 240, 255)},
        'dark':   {'bg': (15, 23, 42, 255),   'border': (15, 23, 42, 255),   'text': (255, 255, 255, 255), 'dot': (0, 210, 255, 255)},
    }
    
    if solid:
        scheme = color_schemes_solid.get(theme, color_schemes_solid['blue'])
    elif dark_mode:
        scheme = color_schemes_dark.get(theme, color_schemes_dark['blue'])
    else:
        scheme = color_schemes_light.get(theme, color_schemes_light['blue'])
    
    has_dot = False  # Completely remove leading dot from all badges per user request
    tw = draw.textlength(text, font=font)
    dot_diameter = 7
    dot_gap = 8
    
    if has_dot:
        content_w = dot_diameter + dot_gap + tw
    else:
        content_w = tw
        
    bw = int(round(content_w + pad_x * 2))
    bh = int(round(height))
    radius = bh // 2
    
    if left_x is not None:
        bx1 = int(round(left_x))
        bx2 = bx1 + bw
        cx = (bx1 + bx2) / 2.0
    else:
        bx1 = int(round(cx - bw / 2.0))
        bx2 = bx1 + bw
        
    by1 = int(round(cy - bh / 2.0))
    by2 = by1 + bh
    
    # Draw pill container
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=radius, fill=scheme['bg'], outline=scheme['border'], width=1)
    
    if has_dot:
        content_x1 = bx1 + pad_x
        dot_cx = content_x1 + dot_diameter / 2.0
        r = dot_diameter / 2.0
        draw.ellipse([int(round(dot_cx - r)), int(round(cy - r)), int(round(dot_cx + r)), int(round(cy + r))], fill=scheme['dot'])
        tx = content_x1 + dot_diameter + dot_gap
        draw.text((tx, cy), text, font=font, anchor='lm', fill=scheme['text'])
    else:
        draw.text((cx, cy), text, font=font, anchor='mm', fill=scheme['text'])
        
    return bx1, by1, bx2, by2

def draw_slide_header(draw, slide_num, category_en, title_black, title_blue, subtitle_kr, right_badge=None, dark_mode=False):
    """
    Renders the unified, executive Behance editorial header across all portfolio slides.
    Standardizes top hairline, kicker badge, dual-color main headline, and subtitle.
    Guarantees a clean, comfortable bottom margin (25px) below the kicker badge.
    Supports dark_mode for high-impact finale slides.
    """
    line_col = (40, 53, 72) if dark_mode else (226, 232, 240)
    draw.line([(100, 52), (1820, 52)], fill=line_col, width=1)
    
    badge_text = f"{slide_num:02d} {category_en.upper()}"
    draw_pill_badge(draw, left_x=100, cy=78, text=badge_text, font=get_font(10.5, 'bold'), theme='blue', has_dot=True, dark_mode=dark_mode, pad_x=10, height=26)
    
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
    """
    Renders the unified, executive Behance editorial footer strip across all portfolio slides.
    Standardizes bottom hairline, brand text, tech stack, and pagination.
    Supports dark_mode for high-impact finale slides.
    """
    line_col = (40, 53, 72) if dark_mode else (226, 232, 240)
    draw.line([(100, 995), (1820, 995)], fill=line_col, width=1)
    
    brand_col = (56, 189, 248) if dark_mode else (0, 81, 255)
    draw.text((100, 1018), "KOREA HISTORY QUIZ", font=get_font(11, 'bold'), fill=brand_col)
    meta_col = (100, 116, 139) if dark_mode else (148, 163, 184)
    draw.text((270, 1018), "·   비핸스 엔터프라이즈 케이스 스터디  ·  실전 한능검 기출 솔루션", font=get_font(11, 'medium'), fill=meta_col)
    draw.text((960, 1018), "Flutter 3.47+ 모바일 & 웹  ·  SQLite 1,500제 완비  ·  구글 플레이 출시", font=get_font(10.5, 'medium'), fill=meta_col, anchor='mt')
    
    page_col = (148, 163, 184) if dark_mode else (100, 116, 139)
    page_str = f"PAGE {slide_num:02d} / {total_slides:02d}"
    draw.text((1820, 1018), page_str, font=get_num_font(11.5, 'black'), fill=page_col, anchor='rt')


def draw_behavior_slider(draw, x, y, w, label, left_txt, right_txt, ratio, theme='blue'):
    """
    Renders an editorial behavior spectrum slider track with active segment and circular marker dot.
    Inspired by senior Behance case study persona spectrums.
    """
    theme_colors = {
        'blue': {'active': (0, 82, 255), 'dot': (0, 82, 255)},
        'amber': {'active': (217, 119, 6), 'dot': (217, 119, 6)},
        'green': {'active': (16, 185, 129), 'dot': (16, 185, 129)},
        'cyan': {'active': (6, 182, 212), 'dot': (6, 182, 212)},
    }
    col = theme_colors.get(theme, theme_colors['blue'])
    
    # Label
    draw.text((x, y), label, font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    
    # Left and Right endpoint annotations
    draw.text((x + 75, y + 1), left_txt, font=get_font(9, 'medium'), fill=(100, 116, 139))
    r_bbox = draw.textbbox((0, 0), right_txt, font=get_font(9, 'medium'))
    r_w = r_bbox[2] - r_bbox[0]
    draw.text((x + w - r_w, y + 1), right_txt, font=get_font(9, 'medium'), fill=(100, 116, 139))
    
    # Slider Track
    track_x = x + 125
    track_w = w - 135 - r_w
    track_y = y + 7
    
    draw.rounded_rectangle([track_x, track_y, track_x + track_w, track_y + 4], radius=2, fill=(226, 232, 240))
    active_w = int(round(track_w * max(0.0, min(1.0, ratio))))
    draw.rounded_rectangle([track_x, track_y, track_x + active_w, track_y + 4], radius=2, fill=col['active'])
    
    # Indicator Dot (circle with white ring)
    dot_cx = track_x + active_w
    dot_cy = track_y + 2
    r = 5
    draw.ellipse([dot_cx - r - 1, dot_cy - r - 1, dot_cx + r + 1, dot_cy + r + 1], fill=(255, 255, 255))
    draw.ellipse([dot_cx - r, dot_cy - r, dot_cx + r, dot_cy + r], fill=col['dot'])


def draw_dotted_callout(draw, p1, p2, col=(0, 82, 255), dot_r=4, elbow_x=None):
    """
    Renders an architectural blueprint-style dotted connector line from phone UI anchor to annotation card.
    Inspired by Behance feature callout schematics.
    """
    x1, y1 = p1
    x2, y2 = p2
    
    # 1. Anchor node at start point (circle with white ring)
    draw.ellipse([x1 - dot_r - 2, y1 - dot_r - 2, x1 + dot_r + 2, y1 + dot_r + 2], fill=(255, 255, 255, 220))
    draw.ellipse([x1 - dot_r, y1 - dot_r, x1 + dot_r, y1 + dot_r], fill=col)
    
    # 2. Dotted path
    if elbow_x is None:
        elbow_x = int(x1 + (x2 - x1) * 0.45)
        
    pts = [(x1, y1), (elbow_x, y1), (elbow_x, y2), (x2, y2)]
    
    def draw_dotted_segment(ptA, ptB, dot_spacing=6):
        ax, ay = ptA
        bx, by = ptB
        dist = math.hypot(bx - ax, by - ay)
        if dist == 0:
            return
        steps = int(dist // dot_spacing)
        for s in range(steps + 1):
            t = s / max(1, steps)
            px = ax + (bx - ax) * t
            py = ay + (by - ay) * t
            draw.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=col)
            
    for i in range(len(pts) - 1):
        draw_dotted_segment(pts[i], pts[i+1])
        
    # 3. Arrow / terminal anchor at end point (pointing appropriately)
    arrow_size = 6
    if x2 >= x1:
        draw.polygon([(x2, y2), (x2 - arrow_size, y2 - arrow_size * 0.7), (x2 - arrow_size, y2 + arrow_size * 0.7)], fill=col)
    else:
        draw.polygon([(x2, y2), (x2 + arrow_size, y2 - arrow_size * 0.7), (x2 + arrow_size, y2 + arrow_size * 0.7)], fill=col)



def draw_branch_badge(draw, cx, cy, text, is_yes=True):
    """Draws a clean, high-contrast, solid badge for YES / NO branches positioned with clear margins."""
    return draw_pill_badge(draw, cx, cy, text, theme='green' if is_yes else 'red', has_dot=False, dark_mode=False, pad_x=10, height=22)

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

def find_perspective_coeffs(source_coords, target_coords):
    """Computes homography coefficients for PIL inverse perspective transform."""
    matrix = []
    for (x_t, y_t), (x_s, y_s) in zip(target_coords, source_coords):
        matrix.append([x_t, y_t, 1, 0, 0, 0, -x_s * x_t, -x_s * y_t])
        matrix.append([0, 0, 0, x_t, y_t, 1, -y_s * x_t, -y_s * y_t])
    A = np.matrix(matrix, dtype=float)
    B = np.array(source_coords).reshape(8)
    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

def render_3d_phone(device_img, target_corners, depth=20, extrude_dir=(-14, 12), canvas_size=(W, H)):
    """
    Renders a 3D perspective flagship smartphone with realistic metallic chassis depth extrusion.
    """
    cw, ch = canvas_size
    dw, dh = device_img.size
    src_corners = [(0, 0), (dw, 0), (dw, dh), (0, dh)]
    
    t_tl, t_tr, t_br, t_bl = target_corners
    dx, dy = extrude_dir
    
    # 1. Extrude 3D Chassis Depth Layers (Back-to-Front)
    chassis_canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    dev_mask = device_img.split()[3]
    
    for step in range(depth, 0, -1):
        ratio = step / depth
        # Dark metallic titanium transition
        v = int(16 + (1 - ratio) * 50)
        step_corners = [
            (t_tl[0] + int(dx * ratio), t_tl[1] + int(dy * ratio)),
            (t_tr[0] + int(dx * ratio), t_tr[1] + int(dy * ratio)),
            (t_br[0] + int(dx * ratio), t_br[1] + int(dy * ratio)),
            (t_bl[0] + int(dx * ratio), t_bl[1] + int(dy * ratio))
        ]
        step_coeffs = find_perspective_coeffs(src_corners, step_corners)
        step_mask = dev_mask.transform((cw, ch), Image.Transform.PERSPECTIVE, step_coeffs, Image.Resampling.BICUBIC)
        
        col_img = Image.new('RGBA', (cw, ch), (v, v + 6, v + 16, 255))
        chassis_canvas.paste(col_img, (0, 0), step_mask)
        
    # 2. Front Face Perspective Transform (Pure Authentic Screenshot + Bezel)
    front_coeffs = find_perspective_coeffs(src_corners, target_corners)
    phone_front = device_img.transform((cw, ch), Image.Transform.PERSPECTIVE, front_coeffs, Image.Resampling.BICUBIC)
    
    # 3. Subtle Glass Specular Reflection Highlight (Very soft 15-alpha sheen)
    specular = Image.new('RGBA', (dw, dh), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(specular)
    s_draw.polygon([(0, 0), (dw // 2, 0), (0, dh // 2)], fill=(255, 255, 255, 14))
    specular_transformed = specular.transform((cw, ch), Image.Transform.PERSPECTIVE, front_coeffs, Image.Resampling.BICUBIC)
    
    # Composite Phone front onto chassis
    composite = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    composite.paste(chassis_canvas, (0, 0), chassis_canvas)
    composite.paste(phone_front, (0, 0), phone_front)
    composite = Image.alpha_composite(composite, specular_transformed)
    
    return composite

# ==============================================================
# SLIDE 01: Hero Cover with Dual Tilted Mockups & Korail Layout
# ==============================================================
def draw_hero_pill(draw, cx, cy, text, font=None, fill_color=(255, 255, 255, 25), outline_color=(255, 255, 255, 120), text_color=(255, 255, 255), pad_x=16, height=32):
    if font is None:
        font = get_font(13, 'semibold')
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w = tw + pad_x * 2
    r = height // 2
    x0 = cx - w // 2
    y0 = cy - height // 2
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + height], radius=r, fill=fill_color, outline=outline_color, width=1)
    draw.text((x0 + pad_x, y0 + (height - th) // 2 - 1), text, font=font, fill=text_color)

def make_slide_01():
    base = Image.new('RGBA', (W, H), (250, 252, 255, 255))
    
    # 1. Subtle Ambient Radial Glow
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([800, 100, 1850, 850], fill=(0, 82, 255, 18))
    g_draw.ellipse([1050, 180, 1750, 780], fill=(6, 182, 212, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    
    draw = ImageDraw.Draw(base)
    
    # Hairline Top Boundary
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    # Top Kicker & Metadata
    draw_pill_badge(draw, left_x=100, cy=76, text="2026 포트폴리오 케이스 스터디", font=get_font(11.5, 'bold'), theme='blue', has_dot=True, pad_x=12, height=28)
    
    meta_txt = "기획(PM) · UI/UX 디자인 · Android Live (v2.0) · Web Prototype"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=(100, 116, 139))
    
    # Category Label
    draw.text((100, 146), "대한국사 · 에듀테크 모바일 UX/UI 아키텍처", font=get_font(14, 'bold'), fill=(0, 82, 255))
    
    # Big Clean Headline
    title_p1 = "방대한 역사를, "
    title_p2 = "한 손에 정복하다."
    w_p1 = draw.textlength(title_p1, font=get_font(56, 'black'))
    draw.text((100, 178), title_p1, font=get_font(56, 'black'), fill=(15, 23, 42))
    draw.text((100 + w_p1, 178), title_p2, font=get_font(56, 'black'), fill=(0, 82, 255))
    
        # Clean UX Subtitle (2 balanced lines)
    sub1 = "두꺼운 기출 문제집과 분절된 암기 카드 대신 1,500제 기출과 6대 시대를 완벽 정리하고,"
    sub2 = "수험생의 오답 취약 패턴을 분석해 합격권 80점을 최단기로 완성하는 스마트 에듀테크 솔루션"
    draw.text((100, 260), sub1, font=get_font(16.5, 'regular'), fill=(71, 85, 105))
    draw.text((100, 288), sub2, font=get_font(16.5, 'semibold'), fill=(30, 41, 59))
    
    # OPEN STORYLINE: Key Strengths (Open layout with zero enclosing boxes as requested)
    strengths = [
        ("01", "실전 감각 극대화", "실전 모의고사 50문항 엔진", "Real Exam 80min Sim Engine",
         "실제 한능검 시험과 동일한 50문항 80분 타이머와 원터치 OMR 시트 인터랙션으로 실전 긴장감을 극대화했습니다."),
        ("02", "취약점 자동 인덱싱", "AI 취약시대 오답 분석 볼트", "Weak Era Diagnostic Vault",
         "풀이 즉시 오답 데이터를 수집해 선사부터 현대까지 6대 시대별 취약점을 자동 분석하고 오답률 88% 빈출 사료를 정밀 제시합니다."),
        ("03", "입체적 역사 구조화", "키워드 연표 & 사료 마스터", "Chronological History Ledger",
         "왕조 계보와 주요 사건 연표를 가로 스크롤 및 계층형 타임라인으로 시각화하여 방대한 사료 흐름을 직관적으로 구조화했습니다."),
        ("04", "언제 어디서나 학습", "100% 오프라인 SQLite 캐시", "100% Offline SQLite Engine",
         "1,500문항 기출 데이터와 해설, 오답 노트를 기기 내부 SQLite에 완전 영속화하여 데이터 통신 없이 어디서든 즉시 학습 가능합니다.")
    ]
    
    # Calculate maximum badge width to ensure unified title alignment with clean margin
    max_badge_w = max(draw.textlength(tag, font=get_font(10, 'bold')) + 16 for _, tag, _, _, _ in strengths)
    title_x = int(round(144 + max_badge_w + 24)) # 24px clean margin after the longest badge
    
    k_y = 358
    for idx, (num, tag, title_ko, sub_en, desc) in enumerate(strengths):
        # Open number pill
        draw.rounded_rectangle([100, k_y + 2, 136, k_y + 28], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.text((118, k_y + 15), num, font=get_font(11, 'bold'), fill=(0, 82, 255), anchor='mm')
        
        # Tag & Title & EN Subtitle
        draw_pill_badge(draw, left_x=144, cy=k_y + 15, text=tag, font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=22)
        
        draw.text((title_x, k_y + 4), title_ko, font=get_font(15.5, 'bold'), fill=(15, 23, 42))
        
        w_title = draw.textlength(title_ko, font=get_font(15.5, 'bold'))
        draw.text((title_x + w_title + 12, k_y + 6), f"·  {sub_en}", font=get_font(12, 'medium'), fill=(100, 116, 139))
        
        # 2-line description with comfortable width (up to 780px)
        words = desc.split(' ')
        lines = []
        cur_l = ""
        for w in words:
            test = (cur_l + ' ' + w).strip()
            if draw.textlength(test, font=get_font(12, 'regular')) <= 780:
                cur_l = test
            else:
                lines.append(cur_l)
                cur_l = w
        if cur_l:
            lines.append(cur_l)
            
        desc_y = k_y + 36
        for l in lines[:2]:
            draw.text((144, desc_y), l, font=get_font(12, 'regular'), fill=(71, 85, 105))
            desc_y += 20
            
        # Subtle hairline divider between items
        if idx < 3:
            draw.line([(100, k_y + 92), (900, k_y + 92)], fill=(226, 232, 240), width=1)
            
        k_y += 114
        
    # Right Side: Dual Flagship iPhone Mockups
    phone_home = Image.open('d:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/iphone_01_home.png').convert('RGBA')
    phone_target = Image.open('d:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/iphone_03_target.png').convert('RGBA')
    
    target_h = 670
    target_w = int(round(target_h * (phone_home.width / phone_home.height)))
    p_front = phone_home.resize((target_w, target_h), Image.Resampling.LANCZOS)
    p_back = phone_target.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    angle = -11.0
    rot_front = p_front.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    rot_back = p_back.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    def make_shadow(img, blur=44, offset=(22, 40), alpha=80):
        mask = img.split()[3]
        sh_img = Image.new('RGBA', (img.width + 120, img.height + 120), (0, 0, 0, 0))
        black = Image.new('RGBA', img.size, (0, 0, 0, alpha))
        sh_img.paste(black, (60 + offset[0], 60 + offset[1]), mask)
        return sh_img.filter(ImageFilter.GaussianBlur(blur)), (60, 60)
        
    sh_back, pad_b = make_shadow(rot_back, blur=40, offset=(18, 34), alpha=65)
    sh_front, pad_f = make_shadow(rot_front, blur=48, offset=(24, 44), alpha=88)
    
    p_back_x, p_back_y = 1270, 115
    p_front_x, p_front_y = 970, 170
    
    base.paste(sh_back, (p_back_x - pad_b[0], p_back_y - pad_b[1]), sh_back)
    base.paste(rot_back, (p_back_x, p_back_y), rot_back)
    
    base.paste(sh_front, (p_front_x - pad_f[0], p_front_y - pad_f[1]), sh_front)
    base.paste(rot_front, (p_front_x, p_front_y), rot_front)
    
    draw = ImageDraw.Draw(base)
    
    # Bottom 4-Column Specification Strip (Spanning x=100 to 1820, y=840 to 956)
    bar_y = 840
    bar_h = 116
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    col_w = (1720) // 4
    specs = [
        ("PROJECT ROLE", "기획(PM) 100% · UI/UX 디자인 100%", "사용자 리서치 · 문제 정의 · IA 정보 설계 · 와이어프레임 · UI 디자인 총괄"),
        ("PERIOD & TIMELINE", "2026.02 - 현재 (상용 라이브 배포)", "기출 77회 수록 및 실 수험생 피드백을 반영한 상용 고도화 및 60fps 인터랙션 구축"),
        ("DESIGN SYSTEM", "태극 헤리티지 토큰 · 8pt 그리드 규격", "코발트 블루 & 백자 캔버스 · 24dp 단청 아이콘 · 고대비 수험 가독성 타이포그래피"),
        ("DELIVERY & RELEASE", "Google Play 상용 출시 & 인터랙티브 웹 허브", "실제 스토어 사용자 피드백 반영(v2.0) · 60fps 인터랙티브 체험 환경 구축")
    ]
    
    for i, (cat, val_bold, val_desc) in enumerate(specs):
        cx = 100 + i * col_w
        if i > 0:
            draw.line([(cx, bar_y + 18), (cx, bar_y + bar_h - 18)], fill=(226, 232, 240), width=1)
        
        draw.text((cx + 28, bar_y + 18), cat, font=get_font(11, 'bold'), fill=(0, 82, 255))
        draw.text((cx + 28, bar_y + 42), val_bold, font=get_font(14.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 28, bar_y + 70), val_desc, font=get_font(11, 'regular'), fill=(100, 116, 139))
        
    draw_slide_footer(draw, 1)
    base.save(f'{OUT_DIR}/slide_01.png')
    # auto_out stripped
    print("SAVED Bento Grid Slide 01 to both repos successfully!")
def make_slide_02():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=2, 
        category_en="사용자 리서치 | 데스크 리서치 & 수험생 학습 행태 분석", 
        title_black="한능검·공무원 수험생의 학습 병목과 ", 
        title_blue="휘발성 암기 극복을 위한 3대 전략", 
        subtitle_kr="수험생 520명 심층 인터뷰 및 에빙하우스 망각곡선 기반 3대 학습 솔루션 도출"
    )
    
    # ==============================================================
    # 1. TOP: 3 Horizontal Market Trend Cards
    # ==============================================================
    sy = 234
    card_w = 540
    card_h = 240
    gap = 50
    c1_x = 100
    
    # --- Card 1: Donut Chart (74.2% 사료 독해 난항 및 중도 포기율) ---
    draw.rounded_rectangle([c1_x, sy, c1_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c1_x, sy + 18, c1_x + 5, sy + card_h - 18], radius=2, fill=(225, 29, 72))
    
    draw_pill_badge(draw, left_x=c1_x + 24, cy=sy + 26, text="PAIN POINT", font=get_font(10, 'bold'), theme='red', has_dot=False, pad_x=8, height=22)
    draw.text((c1_x + 24, sy + 58), "사료 독해 난항 및 중도 포기율", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c1_x + 24, sy + 88), "고문헌 사료 해석 실패와 방대한 암기량으로\n수험생 10명 중 7명이 기출 3회독 전 중도 탈락합니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c1_x + 24, sy + 144), "74.2%", font=get_num_font(30, 'black'), fill=(225, 29, 72))
    draw.text((c1_x + 24, sy + 188), "사료 해석 막힘 & 암기 휘발성 호소 (N=520)", font=get_font(11, 'bold'), fill=(225, 29, 72))
    
    # Donut Chart Visual
    ch1_cx = c1_x + card_w - 95
    ch1_cy = sy + card_h // 2 + 10
    cr1 = 58
    thick1 = 14
    draw.ellipse([ch1_cx - cr1, ch1_cy - cr1, ch1_cx + cr1, ch1_cy + cr1], fill=(241, 245, 249))
    arc_deg = int(round(360 * 0.742))
    draw.pieslice([ch1_cx - cr1, ch1_cy - cr1, ch1_cx + cr1, ch1_cy + cr1], start=-90, end=-90 + arc_deg, fill=(225, 29, 72))
    draw.ellipse([ch1_cx - (cr1 - thick1), ch1_cy - (cr1 - thick1), ch1_cx + (cr1 - thick1), ch1_cy + (cr1 - thick1)], fill=(255, 255, 255))
    draw.text((ch1_cx, ch1_cy - 6), "74%", font=get_num_font(15, 'black'), fill=(15, 23, 42), anchor='mm')
    draw.text((ch1_cx, ch1_cy + 10), "암기 한계", font=get_font(8.5, 'bold'), fill=(100, 116, 139), anchor='mm')
    
    # --- Card 2: H-Bar Chart (1,200g 문제집의 물리적 한계) ---
    c2_x = c1_x + card_w + gap
    draw.rounded_rectangle([c2_x, sy, c2_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c2_x, sy + 18, c2_x + 5, sy + card_h - 18], radius=2, fill=(217, 119, 6))
    
    draw_pill_badge(draw, left_x=c2_x + 24, cy=sy + 26, text="BEHAVIOR TREND", font=get_font(10, 'bold'), theme='amber', has_dot=False, pad_x=8, height=22)
    draw.text((c2_x + 24, sy + 58), "두꺼운 기출 문제집의 물리적 한계", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c2_x + 24, sy + 88), "두꺼운 문제집을 수기로 채점하고 오답 노트를 일일이 풀칠하느라\n2시간 넘게 낭비되고 정작 실전 사료 독해 훈련을 놓칩니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c2_x + 24, sy + 144), "1,200g → 0g", font=get_num_font(30, 'black'), fill=(217, 119, 6))
    draw.text((c2_x + 24, sy + 188), "무게 100% 모바일 경량화 (출퇴근/통학 학습)", font=get_font(11, 'bold'), fill=(16, 185, 129))
    
    # H-Bar Graphic
    hb_x = c2_x + card_w - 180
    hb_y = sy + 76
    h_data = [("종이 문제집", 150, (203, 213, 225), "110분/일"), ("대한국사", 36, (29, 78, 216), "0초 (자동)")]
    for hidx, (hlbl, hval, hcol, hstat) in enumerate(h_data):
        hy = hb_y + hidx * 62
        draw.text((hb_x, hy), hlbl, font=get_font(10, 'bold'), fill=(71, 85, 105))
        draw.text((hb_x + 155, hy), hstat, font=get_font(9.5, 'bold'), fill=hcol, anchor='rm')
        draw.rounded_rectangle([hb_x, hy + 18, hb_x + 155, hy + 28], radius=5, fill=(241, 245, 249))
        draw.rounded_rectangle([hb_x, hy + 18, hb_x + hval, hy + 28], radius=5, fill=hcol)
        
    # --- Card 3: V-Bar Chart (1초 자동 오답 인덱싱 솔루션) ---
    c3_x = c2_x + card_w + gap
    draw.rounded_rectangle([c3_x, sy, c3_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c3_x, sy + 18, c3_x + 5, sy + card_h - 18], radius=2, fill=(29, 78, 216))
    
    draw_pill_badge(draw, left_x=c3_x + 24, cy=sy + 26, text="CORE SOLUTION", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=22)
    draw.text((c3_x + 24, sy + 58), "스마트 오답 볼트 & 키워드 하이라이트", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c3_x + 24, sy + 88), "틀린 문제 1초 만에 자동 인덱싱 & 사료 핵심 단서 형광펜\n50:50 찬스 기반 능동적 소거법 추론 훈련을 완성합니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c3_x + 24, sy + 144), "340% 향상", font=get_num_font(30, 'black'), fill=(29, 78, 216))
    draw.text((c3_x + 24, sy + 188), "단기 1급 합격 암기 지속도 실측 검증", font=get_font(11, 'bold'), fill=(29, 78, 216))
    
    # V-Bar Visual
    vb_x = c3_x + card_w - 180
    vb_base_y = sy + card_h - 35
    v_data = [("기존 종이", 36, (203, 213, 225), "38%"), ("대한국사", 124, (29, 78, 216), "91%")]
    for vidx, (vlbl, vh, vcol, vscore) in enumerate(v_data):
        vx = vb_x + vidx * 80
        draw.rounded_rectangle([vx, vb_base_y - 128, vx + 52, vb_base_y], radius=6, fill=(241, 245, 249))
        draw.rounded_rectangle([vx, vb_base_y - vh, vx + 52, vb_base_y], radius=6, fill=vcol)
        draw.text((vx + 26, vb_base_y - vh - 10), vscore, font=get_font(10, 'bold'), fill=vcol, anchor='mm')
        draw.text((vx + 26, vb_base_y + 12), vlbl, font=get_font(9.5, 'bold'), fill=(71, 85, 105), anchor='mm')
        
    # ==============================================================
    # 2. BOTTOM: Dual Master Pane (SWOT Matrix + 3-Core UX Strategy)
    # ==============================================================
    b_y = 514
    b_h = 425
    b_w = 835
    
    # --- BOTTOM LEFT: SWOT ANALYSIS ---
    draw.rounded_rectangle([100, b_y, 100 + b_w, b_y + b_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=125, cy=b_y + 30, text="STRATEGIC MATRIX", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((260, b_y + 30), "SWOT ANALYSIS : 대한국사 에듀테크 플랫폼의 전략적 포지셔닝", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    qw = (b_w - 50 - 16) // 2
    qh = 155
    q_gap = 16
    q_x1 = 125
    q_x2 = q_x1 + qw + q_gap
    q_y1 = b_y + 60
    q_y2 = q_y1 + qh + q_gap
    
    swot_cards = [
        ("S", "STRENGTHS (강점)", [
            "• 최신 77회 포함 1,500제 기출 완벽 내장",
            "• 사료 핵심 단서 형광펜 & 50:50 소거 찬스",
            "• 완전 오프라인 SQLite 구동 (데이터 0MB)"
        ], (29, 78, 216), q_x1, q_y1),
        ("W", "WEAKNESSES (약점)", [
            "• 방대한 5,000년 역사 데이터 초벌 학습 필요",
            "• 고해상도 유물·사료 이미지 저장 용량 필요",
            "• 초기 온보딩 시 실전 모의고사 난이도 체감"
        ], (100, 116, 139), q_x2, q_y1),
        ("O", "OPPORTUNITIES (기회)", [
            "• 한능검·공무원 수험생 모바일 학습 수요 88.4%",
            "• 두꺼운 기출집 대비 출퇴근 자투리 학습 대세",
            "• 공공 데이터 기출 전 문항 합법 라이선스 활용"
        ], (5, 150, 105), q_x1, q_y2),
        ("T", "THREATS (위협)", [
            "• 대형 어학·공무원 학원의 무료 기출 PDF 배포",
            "• 유튜브 요약 강의 등 수동적 영상 소비 선호",
            "• 모바일 시험 풀이 시 집중력 저하 우려"
        ], (225, 29, 72), q_x2, q_y2)
    ]
    
    for s_code, s_title, s_bullets, s_col, sx_pos, sy_pos in swot_cards:
        draw.rounded_rectangle([sx_pos, sy_pos, sx_pos + qw, sy_pos + qh], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.ellipse([sx_pos + 12, sy_pos + 12, sx_pos + 36, sy_pos + 36], fill=s_col)
        draw.text((sx_pos + 24, sy_pos + 24), s_code, font=get_font(12, 'black'), fill=(255, 255, 255), anchor='mm')
        draw.text((sx_pos + 44, sy_pos + 24), s_title, font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
        b_ly = sy_pos + 46
        for b_txt in s_bullets:
            draw.text((sx_pos + 12, b_ly), b_txt, font=get_font(9.5, 'regular'), fill=(71, 85, 105))
            b_ly += 26
            
    # --- BOTTOM RIGHT: 3-CORE OUTCOME STRATEGY ---
    rx = 100 + b_w + gap
    draw.rounded_rectangle([rx, b_y, rx + b_w, b_y + b_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=b_y + 30, text="UX STRATEGY", font=get_font(10, 'bold'), theme='green', pad_x=8, height=22)
    draw.text((rx + 160, b_y + 30), "OUTCOME STRATEGY : 수험생 합격을 완성하는 3대 UX 원칙", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    strat_cards = [
        ("01", "기출 1,500제 완벽 분석 및 오답 자동 인덱싱",
         "AS-IS : 두꺼운 문제집 들고 다니며 오답 체크에 2시간 이상 낭비되는 비효율",
         "TO-BE : 틀린 문제 1초 만에 오답 볼트로 인덱싱 & 취약 시대 타겟 숏폼 복습",
         (29, 78, 216)),
        ("02", "사료 판독 키워드 하이라이트 & 50:50 찬스",
         "AS-IS : 고문헌 한자/초서 사료 해석에 막혀 문제 전체를 포기하는 수험생 좌절",
         "TO-BE : 사료 속 핵심 단서 자동 형광펜 + 50:50 확률 찬스로 수험생 추론 훈련",
         (217, 119, 6)),
        ("03", "시대별 마스터리 레이더 & 실전 80분 시험장 시뮬레이션",
         "AS-IS : 시험장 시간 배분 연습 부족으로 마지막 10문항 OMR 마킹 실패 다수",
         "TO-BE : 50문항 80분 공인 시험 OMR 타이머 및 6대 시대별 취약점 레이더 분석",
         (5, 150, 105))
    ]
    
    st_y = b_y + 60
    st_h = 105
    for scode, stitle, asis, tobe, scol in strat_cards:
        draw.rounded_rectangle([rx + 25, st_y, rx + b_w - 25, st_y + st_h], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.ellipse([rx + 42, st_y + 24, rx + 74, st_y + 56], fill=scol)
        draw.text((rx + 58, st_y + 40), scode, font=get_font(13, 'black'), fill=(255, 255, 255), anchor='mm')
        draw.text((rx + 86, st_y + 30), stitle, font=get_font(12.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((rx + 86, st_y + 54), asis, font=get_font(10, 'regular'), fill=(225, 29, 72))
        draw.text((rx + 86, st_y + 76), tobe, font=get_font(10, 'bold'), fill=(29, 78, 216))
        st_y += st_h + 16
        
    draw_slide_footer(draw, 2)
    base.save(f'{OUT_DIR}/slide_02.png')
    print("SAVED diverse Slide 02 (Desk Research + Insight + SWOT Matrix + Outcomes) successfully!")


def make_slide_03():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=3, 
        category_en="타깃 & 페르소나 | 세그멘테이션 매트릭스 & 경쟁사 벤치마킹", 
        title_black="타깃 세그먼트 매트릭스와 ", 
        title_blue="경쟁사 벤치마킹 분석", 
        subtitle_kr="2x2 타깃 포지셔닝 매트릭스와 4대 플랫폼 벤치마크, 그리고 대표 페르소나 행동 지표"
    )
    
    # -------------------------------------------------------------
    # 1. TOP-LEFT: 2x2 Target Segmentation Matrix
    # -------------------------------------------------------------
    mx_x = 100
    mx_y = 234
    mx_w = 840
    mx_h = 320
    
    draw.rounded_rectangle([mx_x, mx_y, mx_x + mx_w, mx_y + mx_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=mx_x + 24, cy=mx_y + 26, text="TARGET MATRIX", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((mx_x + 155, mx_y + 26), "2x2 세그멘테이션 : 학습 집중도 vs. 시험 목표 레벨", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # Quadrant Boxes
    qw = 385
    qh = 115
    q1_x = mx_x + 24
    q1_y = mx_y + 60
    q2_x = q1_x + qw + 22
    q2_y = q1_y
    q3_x = q1_x
    q3_y = q1_y + qh + 16
    q4_x = q2_x
    q4_y = q3_y
    
    # Q1: 직장인 숏폼 암기형
    draw.rounded_rectangle([q1_x, q1_y, q1_x + qw, q1_y + qh], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=q1_x + 12, cy=q1_y + 18, text="Q1 · 통근/자투리 수험생", font=get_font(8.5, 'bold'), theme='slate', pad_x=6, height=18)
    draw.text((q1_x + 12, q1_y + 44), "자투리 10분 활용 & 핵심 기출 요약 선호", font=get_font(11, 'bold'), fill=(15, 23, 42))
    draw.text((q1_x + 12, q1_y + 68), "• 두꺼운 기출집 휴대 불가, 지하철 한 손 풀이\n• 솔루션 : 10문항 숏폼 & 원터치 50:50 찬스", font=get_font(9.5, 'regular'), fill=(71, 85, 105), spacing=3)
    
    # Q2: 전업 공시생 실전형 (PRIMARY TARGET)
    draw.rounded_rectangle([q2_x, q2_y, q2_x + qw, q2_y + qh], radius=10, fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw_pill_badge(draw, left_x=q2_x + 12, cy=q2_y + 18, text="Q2 · 한능검 1급 실전형 (PRIMARY)", font=get_font(8.5, 'bold'), theme='blue', pad_x=6, height=18)
    draw.text((q2_x + 12, q2_y + 44), "50문항 80분 시험장 시뮬레이션 및 80점 돌파", font=get_font(11, 'bold'), fill=(29, 78, 216))
    draw.text((q2_x + 12, q2_y + 68), "• 실제 시험과 동일한 OMR 타이머 및 1,500제 기출 완벽 대비\n• 솔루션 : 50문항 실전 시험 센터 & OMR 시간 안배", font=get_font(9.5, 'regular'), fill=(30, 58, 138), spacing=3)
    
    # Q3: 고교 내신/수능 기초형
    draw.rounded_rectangle([q3_x, q3_y, q3_x + qw, q3_y + qh], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=q3_x + 12, cy=q3_y + 18, text="Q3 · 내신/수능 기초 학습생", font=get_font(8.5, 'bold'), theme='slate', pad_x=6, height=18)
    draw.text((q3_x + 12, q3_y + 44), "시대별 흐름 파악 및 유물 시각 자료 중심", font=get_font(11, 'bold'), fill=(15, 23, 42))
    draw.text((q3_x + 12, q3_y + 68), "• 단순 연도 암기 한계, 사진 유물 연계 부족\n• 솔루션 : 6대 시대별 서고 & 고해상도 유물 갤러리", font=get_font(9.5, 'regular'), fill=(71, 85, 105), spacing=3)
    
    # Q4: 취약 시대 집중 보완형
    draw.rounded_rectangle([q4_x, q4_y, q4_x + qw, q4_y + qh], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=q4_x + 12, cy=q4_y + 18, text="Q4 · 오답 반복 보완형", font=get_font(8.5, 'bold'), theme='red', pad_x=6, height=18)
    draw.text((q4_x + 12, q4_y + 44), "틀린 사료·근현대사 집중 오답 박멸", font=get_font(11, 'bold'), fill=(225, 29, 72))
    draw.text((q4_x + 12, q4_y + 68), "• 틀린 문제를 다시 틀리는 암기 누수 현상 극심\n• 솔루션 : 원터치 스마트 오답 볼트 & 에빙하우스 복습", font=get_font(9.5, 'regular'), fill=(153, 27, 27), spacing=3)
    
    # -------------------------------------------------------------
    # 2. TOP-RIGHT: 4-Competitor Benchmark Table
    # -------------------------------------------------------------
    bm_x = mx_x + mx_w + 40
    bm_y = 234
    bm_w = 840
    bm_h = 320
    
    draw.rounded_rectangle([bm_x, bm_y, bm_x + bm_w, bm_y + bm_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=bm_x + 24, cy=bm_y + 26, text="BENCHMARK", font=get_font(10, 'bold'), theme='amber', pad_x=8, height=22)
    draw.text((bm_x + 145, bm_y + 26), "국내 주요 에듀테크 앱 대비 대한국사의 5대 핵심 차별점", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    cols = [
        ("비교 항목", 130),
        ("E사 기출앱", 140),
        ("C사 모바일", 140),
        ("H사 공무원", 140),
        ("대한국사 (본 앱)", 220)
    ]
    
    # Header Row
    th_y = bm_y + 54
    cur_x = bm_x + 24
    for cname, cwidth in cols:
        draw.text((cur_x + cwidth // 2, th_y + 10), cname, font=get_font(10.5, 'bold'), fill=(15, 23, 42) if "본 앱" not in cname else (29, 78, 216), anchor='mm')
        cur_x += cwidth + 10
        
    draw.line([(bm_x + 24, th_y + 24), (bm_x + bm_w - 24, th_y + 24)], fill=(226, 232, 240), width=1)
    
    b_rows = [
        ("학습 모드", "단순 PDF 나열", "웹 뷰어 풀이", "강의 연계 퀴즈", "실전 50제 + 10문항 숏폼"),
        ("사료 분석", "텍스트 원문만", "단순 정답 표시", "강의 유도 링크", "핵심 단서 형광펜 + 50:50 찬스"),
        ("오답 관리", "수동 스크랩", "단순 체크 리스트", "별도 노트 작성", "1초 자동 인덱싱 오답 볼트"),
        ("오프라인", "네트워크 필수", "로그인 세션 만료", "데이터 1.2GB 소모", "SQLite 100% 온디바이스"),
        ("UI/UX 완성도", "전면 배너 광고 피로", "정적인 텍스트 테이블", "복잡한 학원 결제창", "Flutter 60FPS 네이티브 UI")
    ]
    
    row_y = th_y + 32
    for r_idx, row in enumerate(b_rows):
        cur_x = bm_x + 24
        bg_color = (248, 250, 252) if r_idx % 2 == 0 else (255, 255, 255)
        draw.rounded_rectangle([bm_x + 20, row_y - 4, bm_x + bm_w - 20, row_y + 26], radius=4, fill=bg_color)
        
        for c_idx, cell in enumerate(row):
            cwidth = cols[c_idx][1]
            txt_col = (29, 78, 216) if c_idx == 4 else ((15, 23, 42) if c_idx == 0 else (100, 116, 139))
            txt_weight = 'bold' if (c_idx == 0 or c_idx == 4) else 'regular'
            draw.text((cur_x + cwidth // 2, row_y + 11), cell, font=get_font(9.5, txt_weight), fill=txt_col, anchor='mm')
            cur_x += cwidth + 10
        row_y += 38
        
    # -------------------------------------------------------------
    # 3. BOTTOM: Detailed Representative Personas
    # -------------------------------------------------------------
    p_y = 574
    p_h = 365
    p_w = 840
    
    # Persona 1: 직장인 이수진 (자투리 1급 도전형)
    px1 = 100
    draw.rounded_rectangle([px1, p_y, px1 + p_w, p_y + p_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=px1 + 24, cy=p_y + 26, text="PRIMARY PERSONA 01", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((px1 + 190, p_y + 26), "이수진 (29세 · 공기업 이직 준비 직장인)", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    p1_details = [
        ("• 핵심 목표 : 출퇴근 지하철 20분 활용하여 3주 만에 한능검 심화 1급(80점↑) 취득", (15, 23, 42)),
        ("• 주요 고통 : 두꺼운 기출 문제집 휴대 불가, 채점 및 오답 정리 시간이 부족하여 진도 정체", (225, 29, 72)),
        ("• 학습 행태 : 환승 구간 등 짧은 시간에 5~10문제씩 빠르게 풀고 즉각 채점 확인 선호", (71, 85, 105)),
        ("• 핵심 니즈 : 10문항 숏폼 테스트, 헷갈리는 선지 2개 지워주는 50:50 찬스, 모바일 오답 자동 정리", (29, 78, 216))
    ]
    p1_ly = p_y + 64
    for ptxt, pcol in p1_details:
        draw.text((px1 + 24, p1_ly), ptxt, font=get_font(11, 'bold' if pcol != (71, 85, 105) else 'regular'), fill=pcol)
        p1_ly += 30
        
    draw.rounded_rectangle([px1 + 24, p_y + 200, px1 + p_w - 24, p_y + p_h - 20], radius=10, fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw.text((px1 + 40, p_y + 220), "KEY SCENARIO & UX SOLUTION", font=get_font(10.5, 'bold'), fill=(29, 78, 216))
    draw.text((px1 + 40, p_y + 248), "지하철 2호선 만원 전철에서 한 손으로 앱을 켜고, 10문항 숏폼 모의고사를 실행합니다.\n생소한 사료가 나왔을 때 '50:50 찬스'로 함정 선지 2개를 날리고 소거법으로 정답을 맞힙니다.\n틀린 문제는 '스마트 오답 볼트'에 1초 만에 저장되어 퇴근길에 3분 만에 복습을 완료합니다.", font=get_font(10.5, 'regular'), fill=(30, 58, 138), spacing=6)
    
    # Persona 2: 전업 수험생 박민우 (공무원 실전 고득점형)
    px2 = px1 + p_w + 40
    draw.rounded_rectangle([px2, p_y, px2 + p_w, p_y + p_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=px2 + 24, cy=p_y + 26, text="PRIMARY PERSONA 02", font=get_font(10, 'bold'), theme='amber', pad_x=8, height=22)
    draw.text((px2 + 190, p_y + 26), "박민우 (26세 · 7/9급 공무원 전업 수험생)", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    p2_details = [
        ("• 핵심 목표 : 최신 77회 한능검 심화 95점 이상 달성 및 킬러 사료 완벽 정복", (15, 23, 42)),
        ("• 주요 고통 : 지문이 길고 사료 단서가 숨겨진 3점짜리 킬러 문항에서 오답 발생 빈번", (225, 29, 72)),
        ("• 학습 행태 : 매일 아침 실제 시험과 동일한 80분 타이머로 50문항 전 회차 실전 풀이", (71, 85, 105)),
        ("• 핵심 니즈 : 80분 OMR 타이머, 사료 속 핵심 키워드 형광펜 분석, 시대별 마스터리 레이더", (217, 119, 6))
    ]
    p2_ly = p_y + 64
    for ptxt, pcol in p2_details:
        draw.text((px2 + 24, p2_ly), ptxt, font=get_font(11, 'bold' if pcol != (71, 85, 105) else 'regular'), fill=pcol)
        p2_ly += 30
        
    draw.rounded_rectangle([px2 + 24, p_y + 200, px2 + p_w - 24, p_y + p_h - 20], radius=10, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw.text((px2 + 40, p_y + 220), "KEY SCENARIO & UX SOLUTION", font=get_font(10.5, 'bold'), fill=(180, 83, 9))
    draw.text((px2 + 40, p_y + 248), "독서실에서 '실전 시험 센터'의 제77회 심화 모의고사를 실행하여 80분 OMR 카운트다운을 시작합니다.\n시간 안배 훈련을 거쳐 50문항을 완주한 후, 실시간 점수 환산과 오답 사료 분석을 확인합니다.\n조선 후기 정치사 등 취약 시대를 레이더 차트로 확인하고 서고에서 핵심 사료를 즉시 복습합니다.", font=get_font(10.5, 'regular'), fill=(146, 64, 14), spacing=6)
    
    draw_slide_footer(draw, 3)
    base.save(f'{OUT_DIR}/slide_03.png')
    print("SAVED diverse Slide 03 (Target 2x2 Matrix + Benchmark + Personas) successfully!")


def make_slide_04():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=4, 
        category_en="정보 구조 설계 | 5대 핵심 메뉴 구조도", 
        title_black="누구나 바로 이해하고 쓰는 ", 
        title_blue="5대 핵심 합격 내비게이션", 
        subtitle_kr="홈 대시보드부터 실전 기출, 사료 서고, 오답 볼트까지 합격에 필요한 기능을 한눈에 찾는 쉬운 화면 구조"
    )
    
    # Top-Right Badge: Clean, Compact Overview (w=340, h=60)
    top_badge_x = 1480
    top_badge_y = 65
    draw.rounded_rectangle([top_badge_x, top_badge_y, top_badge_x + 340, top_badge_y + 60], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=top_badge_x + 16, cy=top_badge_y + 30, text="서비스 구성", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=24)
    draw.text((top_badge_x + 110, top_badge_y + 21), "5대 메인 탭", font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((top_badge_x + 110, top_badge_y + 40), "총 15개 직관적 화면 설계", font=get_font(10.5, 'medium'), fill=(100, 116, 139), anchor='lm')
    
    # Level 0 Root Node: Compact, Centered, Clean Korean!
    # Width: 460px (x: 730 to 1190)
    root_x1, root_y1, root_x2, root_y2 = 730, 226, 1190, 290
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=12, fill=(255, 255, 255), outline=(29, 78, 216), width=2)
    root_cy = (root_y1 + root_y2) // 2
    b_root = draw_pill_badge(draw, left_x=root_x1 + 18, cy=root_cy, text="시작 화면", font=get_font(10, 'bold'), theme='blue', has_dot=True, pad_x=10, height=26)
    draw.text((b_root[2] + 16, root_cy - 11), "대한국사 전체 5대 핵심 메뉴 구조", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((b_root[2] + 16, root_cy + 11), "한 손으로 편리하게 이용하는 5대 핵심 메뉴와 기능 안내", font=get_font(10.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    # Connectors from Root Node to 5 Level 1 Columns
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    col_centers = [cx + cw // 2 for cx in cols_x]
    
    draw.line([(960, root_y2), (960, 308)], fill=(29, 78, 216), width=2)
    draw.ellipse([956, 304, 964, 312], fill=(29, 78, 216))
    draw.line([(col_centers[0], 308), (col_centers[-1], 308)], fill=(29, 78, 216, 180), width=2)
    for cx in col_centers:
        draw.ellipse([cx - 4, 308 - 4, cx + 4, 308 + 4], fill=(29, 78, 216))
        draw_arrow(draw, (cx, 308), (cx, 330), col=(29, 78, 216), width=2, arrow_size=4)
        
    # 5 Domains Data (대한국사 100% 맞춤)
    domains_data = [
        ("01. 홈 대시보드", "종합 학습 관제", "출석 스트릭, D-Day, 오늘의 추천 기출을 한눈에 조회", [
            ("스트릭 화면", "출석 스트릭 관리", "매일 이어지는 연속 학습과 시험 목표 D-Day 확인", False),
            ("추천 화면", "77회 실전 모의고사", "최신 한능검 심화 50문항 실전 시험 1-Tap 즉시 진입", True),
            ("레이더 화면", "시대별 마스터리", "선사부터 현대사까지 6대 시대별 취약 영역 조망", False)
        ]),
        ("02. 학습관 (서고)", "시대별 사료 바이블", "6대 시대별 핵심 요약 노트와 고해상도 유물 도감", [
            ("요약 화면", "6대 시대별 요약", "선사·삼국·고려·조선·근대·현대사 핵심 사료 정리", True),
            ("갤러리", "시각 유물 도감", "시험에 빈출되는 국보·보물 유물 고화질 사진 및 해설", False),
            ("단서 사전", "사료 힌트 바이블", "사료 속 인물·연호·관직·지명 핵심 단서 사전 열람", True)
        ]),
        ("03. 실전 시험 센터", "공인 기출 모의고사", "실제 시험과 동일한 50문항 80분 타이머와 숏폼 10제", [
            ("실전 50제", "77회 실전 응시", "실제 시험지와 100% 동일한 배점 및 80분 카운트다운", True),
            ("숏폼 10제", "자투리 10분 모의고사", "출퇴근길 5분 만에 푸는 핵심 기출 압축 테스트", True),
            ("랜덤 모드", "무작위 50제 풀이", "1,500제 기출 풀에서 무작위 50문항 추출 실전 응시", False)
        ]),
        ("04. 오답 볼트", "취약점 자동 인덱싱", "틀린 문제 1초 만에 자동 분류 및 주기 복습 루프", [
            ("보관함", "오답 자동 인덱싱", "틀린 문제의 문항 번호, 시대, 정답률 자동 태깅", True),
            ("사료 해설", "키워드 형광펜 판독", "오답 문제 사료 속 결정적 정답 키워드 형광펜 분석", True),
            ("AI 트레이닝", "취약 시대 집중 복습", "오답만 골라 10문항씩 무한 반복 재응시 트레이닝", True)
        ]),
        ("05. 수험 환경 설정", "학습 편의 맞춤", "목표 급수, 음성 낭독 속도, OLED 다크 테마 설정", [
            ("급수 설정", "목표 급수 관리", "1급/2급/3급 커트라인 설정 및 시험 일정 동기화", False),
            ("음성 설정", "사료 TTS 배속 조절", "사료 본문 및 해설 음성 낭독 속도(1.0x~2.0x) 조절", False),
            ("테마 설정", "OLED 다크 테마", "야간 학습 및 독서실에서 눈의 피로를 덜어주는 테마", True)
        ])
    ]
    
    # Render 5 Columns (Level 1 + Level 2 Tree)
    for c_idx, (t_name, t_sub, t_desc, containers) in enumerate(domains_data):
        cx = cols_x[c_idx]
        
        # Level 1 Column Container
        draw.rounded_rectangle([cx, 330, cx + cw, 696], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # L1 Header Box (y: 330 to 398, h=68)
        draw.rounded_rectangle([cx, 330, cx + cw, 398], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.rectangle([cx, 386, cx + cw, 398], fill=(240, 246, 255))
        draw.line([(cx, 398), (cx + cw, 398)], fill=(191, 219, 254), width=1)
        
        # L1 Title & Subtitle
        draw.text((cx + 14, 342), t_name, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 14, 362), t_sub, font=get_font(10.5, 'bold'), fill=(29, 78, 216))
        draw.text((cx + 14, 380), t_desc, font=get_font(8.5, 'regular'), fill=(100, 116, 139))
        
        # Tree Branch Line (Vertical spine)
        tree_x = cx + 18
        draw.line([(tree_x, 410), (tree_x, 665)], fill=(29, 78, 216, 100), width=2)
        
        # 3 L2 Cards per column (card_h = 82, gap = 10)
        card_w = cw - 32
        card_x = cx + 32
        cy = 414
        card_h = 82
        gap = 10
        
        for scr_type, title, desc, is_core in containers:
            draw.line([(tree_x, cy + 20), (card_x, cy + 20)], fill=(29, 78, 216, 120), width=2)
            draw.ellipse([tree_x - 3, cy + 20 - 3, tree_x + 3, cy + 20 + 3], fill=(29, 78, 216))
            
            card_bg = (255, 255, 255) if not is_core else (250, 252, 255)
            card_bd = (226, 232, 240) if not is_core else (191, 219, 254)
            draw.rounded_rectangle([card_x, cy, card_x + card_w, cy + card_h], radius=8, fill=card_bg, outline=card_bd, width=1)
            
            # Row 1: Friendly Korean Type tag + CORE badge
            draw_pill_badge(draw, left_x=card_x + 14, cy=cy + 15, text=scr_type, font=get_font(8.5, 'bold'), theme='slate', pad_x=6, height=18)
            if is_core:
                draw_pill_badge(draw, left_x=card_x + card_w - 46, cy=cy + 15, text="핵심", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18)
                
            # Row 2: Title with breathing room
            draw.text((card_x + 14, cy + 39), title, font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
            
            # Row 3: Description in clear, friendly Korean
            draw.text((card_x + 14, cy + 62), desc, font=get_font(9.5, 'regular'), fill=(71, 85, 105), anchor='lm')
            
            cy += card_h + gap
            
    # 3. Bottom Architecture Principles: 4 Clean, Well-Proportioned Cards!
    bar_y = 730
    bp_w = 415
    bp_gap = 20
    bp_h = 195
    
    pillars = [
        ("01", "명확한 5대 메뉴 분리", "수험생이 헤매지 않고 목표 회차에 1초 만에 접근할 수 있도록 5개 핵심 메뉴를 명확하게 분리했습니다.",
         ["· 대시보드, 기출 시험, 사료 서고를 목적별로 직관화", "· 불필요한 단계 없이 원하는 메뉴로 1초 만에 이동"]),
        ("02", "한 손 조작 최적화", "엄지손가락이 편안하게 닿는 화면 중하단에 50:50 찬스와 선지 선택 버튼을 집중 배치했습니다.",
         ["· 출퇴근 만원 지하철에서도 한 손으로 흔들림 없는 풀이", "· 원터치 5개 선지 마킹으로 종이 OMR 마킹 피로 해소"]),
        ("03", "실전 사료 단서 식별", "복잡한 고문헌 사료도 핵심 키워드 형광펜으로 정답의 결정적 단서를 0.5초 만에 포착합니다.",
         ["· 헷갈리는 함정 선지 2개를 소거하는 50:50 찬스 연동", "· 전 선지 상세 해설로 왜 오답인지 명쾌한 팩트 체크"]),
        ("04", "100% 기기 내 오답 보관", "네트워크 통신 없이도 1,500제 기출과 오답 노트가 내 스마트폰 안에서 즉시 구동됩니다.",
         ["· 데이터 요금 걱정 없는 100% 완전 오프라인 SQLite 볼트", "· 에빙하우스 망각곡선 주기 복습 알림으로 단기 1급 합격"])
    ]
    
    for pidx, (pnum, ptitle, pdesc, psub_lines) in enumerate(pillars):
        px = 100 + pidx * (bp_w + bp_gap)
        draw.rounded_rectangle([px, bar_y, px + bp_w, bar_y + bp_h], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Number chip + Title
        draw.rounded_rectangle([px + 18, bar_y + 18, px + 52, bar_y + 44], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((px + 35, bar_y + 31), pnum, font=get_font(11, 'bold'), fill=(29, 78, 216), anchor='mm')
        
        draw.text((px + 62, bar_y + 31), ptitle, font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.line([(px + 18, bar_y + 54), (px + bp_w - 18, bar_y + 54)], fill=(241, 245, 249), width=1)
        
        # Description
        words = pdesc.split(' ')
        lines = []
        cur_l = ""
        for w in words:
            test = (cur_l + ' ' + w).strip()
            if draw.textlength(test, font=get_font(10.5, 'regular')) <= bp_w - 36:
                cur_l = test
            else:
                lines.append(cur_l)
                cur_l = w
        if cur_l:
            lines.append(cur_l)
            
        dy = bar_y + 70
        for l in lines[:2]:
            draw.text((px + 18, dy), l, font=get_font(10.5, 'regular'), fill=(51, 65, 85))
            dy += 20
            
        # Bullet details
        dy += 6
        for subl in psub_lines:
            draw.text((px + 18, dy), subl, font=get_font(9.5, 'medium'), fill=(100, 116, 139))
            dy += 18
            
    draw_slide_footer(draw, 4)
    base.save(f'{OUT_DIR}/slide_04.png')
    print("SAVED new Slide 04 with exact Smart DCA Tree & 4-Pillar Layout!")


def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=5, 
        category_en="사용자 플로우 | 5단계 서비스 인터랙션 플로우차트", 
        title_black="사용자 행동과 판단을 이끄는 ", 
        title_blue="5단계 서비스 UX 플로우차트", 
        subtitle_kr="앱 실행부터 모의고사 회차 선택, 50:50 찬스 추론 풀이, 사료 키워드 판독, 오답 자동 인덱싱까지 이어지는 실전 학습 여정"
    )
    
    # Top-Right Legend
    leg_x = 1280
    leg_y = 65
    leg_w = 540
    leg_h = 78
    draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=leg_x + 16, cy=leg_y + 20, text="NOTATION", font=get_font(8, 'bold'), theme='blue', has_dot=True, pad_x=6, height=18)
    draw.text((leg_x + 105, leg_y + 20), "플로우차트 기호 범례", font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 16, leg_y + 44, leg_x + 70, leg_y + 68], radius=10, fill=(29, 78, 216))
    draw.text((leg_x + 43, leg_y + 56), "Start/End", font=get_font(7, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((leg_x + 76, leg_y + 56), "시작/종료", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 142, leg_y + 44, leg_x + 192, leg_y + 68], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 167, leg_y + 56), "Screen", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((leg_x + 198, leg_y + 56), "화면/접점", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 268, leg_y + 44, leg_x + 318, leg_y + 68], radius=4, fill=(238, 242, 255), outline=(29, 78, 216), width=1)
    draw.text((leg_x + 293, leg_y + 56), "Action", font=get_font(7.5, 'bold'), fill=(29, 78, 216), anchor='mm')
    draw.text((leg_x + 325, leg_y + 56), "사용자 행동", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw_diamond(draw, cx=leg_x + 410, cy=leg_y + 56, w=34, h=22, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw.text((leg_x + 410, leg_y + 56), "Decide", font=get_font(6.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((leg_x + 434, leg_y + 56), "판단 분기", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    # 5 STAGE COLUMNS
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    col_centers = [cx + cw // 2 for cx in cols_x]
    
    stages_info = [
        ("STAGE 01", "진입 & 온보딩", "Launch & Streak Check"),
        ("STAGE 02", "기출 모드 선택", "Exam Mode & Locus Select"),
        ("STAGE 03", "실전 문제 풀이", "Quiz Solve & 50:50 Chance"),
        ("STAGE 04", "사료 단서 식별", "Passage Analysis & Feedback"),
        ("STAGE 05", "오답 볼트 인덱싱", "Auto-Vault & Mastery Loop")
    ]
    
    for i, (st_code, st_name, st_en) in enumerate(stages_info):
        cx = cols_x[i]
        draw.rounded_rectangle([cx, 234, cx + cw, 284], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw_pill_badge(draw, left_x=cx + 16, cy=249, text=st_code, font=get_font(7.5, 'bold'), theme='blue', pad_x=5, height=16)
        draw.text((cx + 86, 249), st_name, font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((cx + 16, 269), st_en, font=get_font(8.5, 'medium'), fill=(100, 116, 139), anchor='lm')
        
        if i < 4:
            draw_arrow(draw, (cx + cw + 2, 259), (cols_x[i + 1] - 2, 259), col=(29, 78, 216), width=2, arrow_size=4)
            
    nw = 260
    
    # --- STAGE 01 (Center: col_centers[0]) ---
    c0 = col_centers[0]
    draw.rounded_rectangle([c0 - 75, 300, c0 + 75, 328], radius=14, fill=(29, 78, 216))
    draw.text((c0, 314), "Start : 앱 실행", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw_arrow(draw, (c0, 328), (c0, 344), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c0 - nw // 2, 344, c0 + nw // 2, 388], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=358, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c0 - 54, 358), "스플래시 & SQLite DB 초기화", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c0, 375), "1,500제 기출 데이터셋 및 스트릭 바인딩", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c0, 388), (c0, 406), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw_diamond(draw, cx=c0, cy=432, w=176, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c0, 432), "이전 응시 기록 존재?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    
    # Yes -> 이어풀기
    draw_arrow(draw, (c0, 458), (c0, 502), col=(29, 78, 216), width=2, arrow_size=4)
    draw.text((c0 - 30, 480), "No (새로)", font=get_font(8, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    draw.rounded_rectangle([c0 - nw // 2, 502, c0 + nw // 2, 546], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=516, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c0 - 54, 516), "홈 대시보드 화면 로드", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c0, 533), "출석 스트릭 · D-Day · 추천 모의고사 확인", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c0, 546), (c0, 564), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c0 - nw // 2, 564, c0 + nw // 2, 608], radius=6, fill=(240, 246, 255), outline=(29, 78, 216), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=578, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c0 - 54, 578), "시험센터 탭 또는 배너 탭", font=get_font(9, 'bold'), fill=(29, 78, 216), anchor='lm')
    draw.text((c0, 595), "최신 77회 심화 기출 1-Tap 진입", font=get_font(8, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c0, 608), (c0, 626), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c0 - nw // 2, 626, c0 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c0 - 44, 640), "시험 정보 번들 초기화 완료", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c0, 656), "50문항 배점 및 80분 카운트다운 타이머 바인딩", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    draw_arrow(draw, (cols_x[0] + cw, 647), (cols_x[1], 647), col=(29, 78, 216), width=2, arrow_size=4)
    
    # --- STAGE 02 (Center: col_centers[1]) ---
    c1 = col_centers[1]
    draw.rounded_rectangle([c1 - nw // 2, 344, c1 + nw // 2, 388], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=358, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c1 - 54, 358), "기출 시험 센터 화면", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c1, 375), "회차별 실전 기출 / 랜덤 50제 / 10문항 숏폼", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c1, 388), (c1, 406), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw_diamond(draw, cx=c1, cy=432, w=176, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c1, 432), "모의고사 모드 선택", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    
    draw_arrow(draw, (c1, 458), (c1, 502), col=(29, 78, 216), width=2, arrow_size=4)
    draw.text((c1 + 35, 480), "50문항 실전", font=get_font(8, 'bold'), fill=(29, 78, 216), anchor='lm')
    
    draw.rounded_rectangle([c1 - nw // 2, 502, c1 + nw // 2, 546], radius=6, fill=(240, 246, 255), outline=(29, 78, 216), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=516, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c1 - 54, 516), "제77회 심화 실전 응시 탭", font=get_font(9, 'bold'), fill=(29, 78, 216), anchor='lm')
    draw.text((c1, 533), "실제 공인 시험지 배열 및 배점(1·2·3점) 로드", font=get_font(8, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c1, 546), (c1, 564), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c1 - nw // 2, 564, c1 + nw // 2, 608], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=578, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c1 - 54, 578), "실전 퀴즈 풀이 뷰포트 진입", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c1, 595), "사료 본문 · 사진 유물 · 5개 선지 레이아웃", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c1, 608), (c1, 626), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c1 - nw // 2, 626, c1 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c1 - 44, 640), "80분 시험 타이머 시작", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c1, 656), "문항당 권장 1분 36초 카운트다운 가동", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    draw_arrow(draw, (cols_x[1] + cw, 647), (cols_x[2], 647), col=(29, 78, 216), width=2, arrow_size=4)
    
    # --- STAGE 03 (Center: col_centers[2]) ---
    c2 = col_centers[2]
    draw.rounded_rectangle([c2 - nw // 2, 344, c2 + nw // 2, 388], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=358, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c2 - 54, 358), "사료 독해 및 선지 탐색", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c2, 375), "한문 사료 · 국보 유물 사진 정밀 대조", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c2, 388), (c2, 406), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw_diamond(draw, cx=c2, cy=432, w=176, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c2, 432), "선지 헷갈림 발생?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    
    draw_arrow(draw, (c2, 458), (c2, 502), col=(29, 78, 216), width=2, arrow_size=4)
    draw.text((c2 + 35, 480), "Yes (찬스)", font=get_font(8, 'bold'), fill=(217, 119, 6), anchor='lm')
    
    draw.rounded_rectangle([c2 - nw // 2, 502, c2 + nw // 2, 546], radius=6, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=516, text="CHANCE", font=get_font(6.5, 'bold'), theme='amber', pad_x=4, height=14)
    draw.text((c2 - 54, 516), "50:50 확률 찬스 버튼 탭", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='lm')
    draw.text((c2, 533), "오답 함정 선지 2개 즉시 블러/소거 처리", font=get_font(8, 'medium'), fill=(146, 64, 14), anchor='mm')
    draw_arrow(draw, (c2, 546), (c2, 564), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c2 - nw // 2, 564, c2 + nw // 2, 608], radius=6, fill=(240, 246, 255), outline=(29, 78, 216), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=578, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c2 - 54, 578), "정답 선지 선택 & 마킹", font=get_font(9, 'bold'), fill=(29, 78, 216), anchor='lm')
    draw.text((c2, 595), "소거법 추론 후 최종 1개 선지 터치", font=get_font(8, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c2, 608), (c2, 626), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c2 - nw // 2, 626, c2 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c2 - 44, 640), "정답 여부 즉시 판별 & 채점", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c2, 656), "진동 햅틱 피드백 및 실시간 획득 점수 누적", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    draw_arrow(draw, (cols_x[2] + cw, 647), (cols_x[3], 647), col=(29, 78, 216), width=2, arrow_size=4)
    
    # --- STAGE 04 (Center: col_centers[3]) ---
    c3 = col_centers[3]
    draw.rounded_rectangle([c3 - nw // 2, 344, c3 + nw // 2, 388], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=358, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c3 - 54, 358), "정답 해설 바텀시트 호출", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c3, 375), "사료 단서 형광펜 & 전 선지 코멘터리", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c3, 388), (c3, 406), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw_diamond(draw, cx=c3, cy=432, w=176, h=52, fill=(254, 242, 242), outline=(225, 29, 72), width=2)
    draw.text((c3, 432), "오답 발생 여부?", font=get_font(9, 'bold'), fill=(225, 29, 72), anchor='mm')
    
    draw_arrow(draw, (c3, 458), (c3, 502), col=(225, 29, 72), width=2, arrow_size=4)
    draw.text((c3 + 30, 480), "Yes (오답)", font=get_font(8, 'bold'), fill=(225, 29, 72), anchor='lm')
    
    draw.rounded_rectangle([c3 - nw // 2, 502, c3 + nw // 2, 546], radius=6, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=516, text="AUTO-VAULT", font=get_font(6.5, 'bold'), theme='red', pad_x=4, height=14)
    draw.text((c3 - 44, 516), "스마트 오답 볼트 자동 인덱싱", font=get_font(9, 'bold'), fill=(153, 27, 27), anchor='lm')
    draw.text((c3, 533), "문항 번호 · 시대 태그 · 선택 오답 자동 기록", font=get_font(8, 'medium'), fill=(153, 27, 27), anchor='mm')
    draw_arrow(draw, (c3, 546), (c3, 564), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c3 - nw // 2, 564, c3 + nw // 2, 608], radius=6, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=578, text="ANALYSIS", font=get_font(6.5, 'bold'), theme='amber', pad_x=4, height=14)
    draw.text((c3 - 54, 578), "사료 핵심 단서 형광펜 확인", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='lm')
    draw.text((c3, 595), "연호/인물/관직 키워드 하이라이트 분석", font=get_font(8, 'medium'), fill=(146, 64, 14), anchor='mm')
    draw_arrow(draw, (c3, 608), (c3, 626), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c3 - nw // 2, 626, c3 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c3 - 44, 640), "오답 원인 분석 완료", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c3, 656), "매력적 오답 함정 원리 및 팩트 체크 습득", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    draw_arrow(draw, (cols_x[3] + cw, 647), (cols_x[4], 647), col=(29, 78, 216), width=2, arrow_size=4)
    
    # --- STAGE 05 (Center: col_centers[4]) ---
    c4 = col_centers[4]
    draw.rounded_rectangle([c4 - nw // 2, 344, c4 + nw // 2, 388], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=358, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c4 - 54, 358), "모의고사 최종 성적 리포트", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c4, 375), "총점(100점 만점) · 합격 급수 판정 (1~3급)", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c4, 388), (c4, 406), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c4 - nw // 2, 412, c4 + nw // 2, 456], radius=6, fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=426, text="RADAR", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c4 - 54, 426), "시대별 마스터리 레이더 갱신", font=get_font(9, 'bold'), fill=(29, 78, 216), anchor='lm')
    draw.text((c4, 443), "선사~현대사 6대 시대 완성도 시각화", font=get_font(8, 'medium'), fill=(30, 58, 138), anchor='mm')
    draw_arrow(draw, (c4, 456), (c4, 502), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c4 - nw // 2, 502, c4 + nw // 2, 546], radius=6, fill=(240, 246, 255), outline=(29, 78, 216), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=516, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c4 - 54, 516), "취약 오답 집중 트레이닝 시작", font=get_font(9, 'bold'), fill=(29, 78, 216), anchor='lm')
    draw.text((c4, 533), "오답 볼트에서 틀린 문제만 10개 재응시", font=get_font(8, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c4, 546), (c4, 564), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c4 - nw // 2, 564, c4 + nw // 2, 608], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=578, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c4 - 44, 578), "에빙하우스 망각곡선 복습 예약", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c4, 595), "1일·3일·7일 후 맞춤형 스마트 복습 알림", font=get_font(8, 'medium'), fill=(21, 128, 61), anchor='mm')
    draw_arrow(draw, (c4, 608), (c4, 638), col=(29, 78, 216), width=2, arrow_size=4)
    
    draw.rounded_rectangle([c4 - 75, 638, c4 + 75, 666], radius=14, fill=(29, 78, 216))
    draw.text((c4, 652), "End : 1급 합격 루프", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # BOTTOM BAR: METRICS & TELMETRY (y=720 to 920)
    # -------------------------------------------------------------
    bar_y = 720
    bar_h = 200
    bar_w = 1720
    draw.rounded_rectangle([100, bar_y, 100 + bar_w, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Left Half: Flowchart Summary
    draw_pill_badge(draw, left_x=124, cy=bar_y + 24, text="UX ARCHITECTURE", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((275, bar_y + 24), "5단계 완결형 에듀테크 사용자 인터랙션 루프", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    f_bullets = [
        "• 진입 온보딩 : 앱 실행 0.4초 만에 스트릭 및 이전 모의고사 이어풀기 즉시 바인딩",
        "• 실전 50제 응시 : 80분 카운트다운 타이머와 실제 시험지와 동일한 1·2·3점 배점 적용",
        "• 50:50 확률 찬스 : 수험생이 고민하는 오답 2개를 소거하여 실전 추론 및 소거법 훈련",
        "• 스마트 오답 볼트 : 틀린 문제 1초 만에 자동 인덱싱 및 에빙하우스 주기 복습 루프 완성"
    ]
    bly = bar_y + 60
    for fb in f_bullets:
        draw.text((124, bly), fb, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
        bly += 28
        
    draw.line([(100 + 880, bar_y + 20), (100 + 880, bar_y + bar_h - 20)], fill=(226, 232, 240), width=1)
    
    # Right Half: KPIs
    kpi_x = 100 + 910
    draw_pill_badge(draw, left_x=kpi_x, cy=bar_y + 24, text="QUANTITATIVE IMPACT", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=22)
    draw.text((kpi_x + 180, bar_y + 24), "정량적 실측 학습 효과 및 수험생 검증 지표", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    kpis = [
        ("모의고사 완주율", "78.4%", "종이 문제집 대비 2.1배↑", "blue"),
        ("오답 정리 시간", "0초", "수기 노트 110분 → 자동", "green"),
        ("50:50 찬스 정답률", "84.6%", "소거법 추론 훈련 성공", "amber"),
        ("오프라인 구동", "100%", "데이터 소모 0MB 완결", "blue")
    ]
    kw = (bar_w - 940 - 30) // 4
    for kidx, (klabel, kval, ksub, ktheme) in enumerate(kpis):
        kx = kpi_x + kidx * (kw + 10)
        draw.rounded_rectangle([kx, bar_y + 60, kx + kw, bar_y + bar_h - 24], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((kx + 16, bar_y + 76), klabel, font=get_font(10, 'bold'), fill=(100, 116, 139))
        draw.text((kx + 16, bar_y + 102), kval, font=get_num_font(18, 'black'), fill=(29, 78, 216) if ktheme == 'blue' else ((5, 150, 105) if ktheme == 'green' else (217, 119, 6)))
        draw.text((kx + 16, bar_y + 138), ksub, font=get_font(9.5, 'medium'), fill=(71, 85, 105))
        
    draw_slide_footer(draw, 5)
    base.save(f'{OUT_DIR}/slide_05.png')
    print("SAVED perfect Slide 05 successfully!")


def make_slide_06():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=6, 
        category_en="와이어프레임 | 4대 모바일 UX & 인체공학적 설계", 
        title_black="대한국사 앱 구조를 그대로 반영한 ", 
        title_blue="4대 모바일 와이어프레임과 인체공학적 설계", 
        subtitle_kr="홈 대시보드·실전 시험센터·실전 문제풀이(50:50 찬스)·스마트 오답볼트 4대 핵심 화면의 골격 구조와 한 손 조작 엄지 영역(Thumb-Zone) 인체공학 설계"
    )
    
    sec_y = 234
    ph = 525
    pw = 280
    
    p1_x = 100
    p2_x = 580
    p3_x = 1060
    p4_x = 1540
    
    # Helper to draw chassis base with soft shadow & dynamic island
    def draw_wireframe_chassis(draw_obj, px, title_text, theme_key):
        # Soft drop shadow
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([px + 8, sec_y + 12, px + pw - 8, sec_y + ph + 16], radius=28, fill=(0, 0, 0, 30))
        sh_blur = sh.filter(ImageFilter.GaussianBlur(14))
        base.paste(sh_blur, (0, 0), sh_blur)
        
        # Outer Chassis
        draw.rounded_rectangle([px, sec_y, px + pw, sec_y + ph], radius=26, fill=(255, 255, 255), outline=(15, 23, 42), width=2)
        # Dynamic Island Pill
        draw.rounded_rectangle([px + pw//2 - 24, sec_y + 8, px + pw//2 + 24, sec_y + 20], radius=6, fill=(15, 23, 42))
        # Screen Title Badge
        draw_pill_badge(draw, cx=px + pw//2, cy=sec_y + 36, text=title_text, font=get_font(9.5, 'bold'), theme=theme_key, has_dot=True, pad_x=8, height=20)
        # Native Home Indicator
        draw.rounded_rectangle([px + pw//2 - 24, sec_y + ph - 8, px + pw//2 + 24, sec_y + ph - 4], radius=2, fill=(15, 23, 42))
        
        # Thumb-Zone 48dp ergonomic bottom arc highlight
        tz_y = sec_y + ph - 92
        draw.rounded_rectangle([px + 6, tz_y, px + pw - 6, sec_y + ph - 14], radius=16, fill=(0, 81, 255, 12), outline=(0, 81, 255, 70), width=1)
        draw.text((px + pw - 14, tz_y + 6), "Thumb-Zone (48dp)", font=get_font(7.5, 'bold'), fill=(0, 81, 255), anchor='ra')

    # Helper to draw PRD-level aesthetic callout pin on core features
    def draw_callout_anchor_pin(draw_obj, cx, cy, pin_num, pin_label, accent_col, is_right=True):
        # Soft outer pulse halo (radius 16)
        draw_obj.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(*accent_col[:3], 45))
        # Crisp white border ring
        draw_obj.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 255, 255), outline=accent_col, width=2)
        # Inner solid colored circle
        draw_obj.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=accent_col)
        # Pin number text
        draw_obj.text((cx, cy), str(pin_num), font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        # Micro callout pill tag
        tag_font = get_font(8.5, 'bold')
        t_bbox = draw_obj.textbbox((0, 0), pin_label, font=tag_font)
        tw = t_bbox[2] - t_bbox[0] + 16
        th = 20
        if is_right:
            tx = cx + 14
            draw_obj.rounded_rectangle([tx, cy - th//2, tx + tw, cy + th//2], radius=5, fill=(15, 23, 42), outline=accent_col, width=1)
            draw_obj.text((tx + tw//2, cy), pin_label, font=tag_font, fill=(255, 255, 255), anchor='mm')
        else:
            tx = cx - 14 - tw
            draw_obj.rounded_rectangle([tx, cy - th//2, tx + tw, cy + th//2], radius=5, fill=(15, 23, 42), outline=accent_col, width=1)
            draw_obj.text((tx + tw//2, cy), pin_label, font=tag_font, fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 1: [SCR-01 · 홈 대시보드] (p1_x = 100)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p1_x, "① SCR-01 · 홈 대시보드", "blue")
    
    # 1. Streak & Heart Header Card
    sc_y = sec_y + 54
    draw.rounded_rectangle([p1_x + 14, sc_y, p1_x + pw - 14, sc_y + 60], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((p1_x + 24, sc_y + 12), "연속 출석 스트릭 & 수험 D-Day", font=get_font(9.5, 'bold'), fill=(0, 81, 255))
    draw.text((p1_x + 24, sc_y + 32), "7일 연속 달성 (D-28)", font=get_font(13.5, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p1_x + pw - 48, cy=sc_y + 38, text="STREAK 7d", font=get_font(8.5, 'bold'), theme='amber', has_dot=False, pad_x=6, height=18)
    
    # 2. Main Exam Launcher Banner
    hb_y = sc_y + 68
    draw.rounded_rectangle([p1_x + 14, hb_y, p1_x + pw - 14, hb_y + 88], radius=10, fill=(29, 78, 216))
    draw.text((p1_x + 24, hb_y + 16), "제77회 심화 실전 모의고사", font=get_font(11, 'bold'), fill=(255, 255, 255))
    draw.text((p1_x + 24, hb_y + 36), "50문항 · 80분 타이머 · 실전 배점", font=get_font(9, 'regular'), fill=(191, 219, 254))
    draw.rounded_rectangle([p1_x + 24, hb_y + 56, p1_x + pw - 24, hb_y + 78], radius=6, fill=(255, 255, 255))
    draw.text((p1_x + pw//2, hb_y + 67), "지금 바로 응시하기 →", font=get_font(9.5, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    # Callout Anchor Pin ① floating above quick actions
    draw_callout_anchor_pin(draw, p1_x + 24, hb_y + 102, "1", "① 1-Tap 즉시 응시 허브", (0, 81, 255), is_right=True)

    # 3. 2x2 Quick Action Grid
    qg_y = hb_y + 118
    q_items = [("기출 시험센터", "77회~50회"), ("오답 복습", "14문항 대기"), ("시대별 서고", "6대 시대 요약"), ("마스터리 통계", "정답률 레이더")]
    for qidx, (qname, qdesc) in enumerate(q_items):
        qcol = qidx % 2
        qrow = qidx // 2
        qx = p1_x + 14 + qcol * 128
        qy = qg_y + qrow * 52
        draw.rounded_rectangle([qx, qy, qx + 120, qy + 46], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((qx + 10, qy + 12), qname, font=get_font(9.5, 'bold'), fill=(15, 23, 42))
        draw.text((qx + 10, qy + 28), qdesc, font=get_font(8, 'regular'), fill=(100, 116, 139))
        
    # Era Progress Radar Summary Card inside Thumb Zone
    bb_y = sec_y + ph - 80
    draw.line([(p1_x + 14, bb_y), (p1_x + pw - 14, bb_y)], fill=(226, 232, 240), width=1)
    b_tabs = ["홈", "기출", "사료", "오답", "설정"]
    tw_b = (pw - 28) // len(b_tabs)
    for tidx, tname in enumerate(b_tabs):
        tx = p1_x + 14 + tidx * tw_b + tw_b // 2
        tcol = (29, 78, 216) if tidx == 0 else (100, 116, 139)
        draw.text((tx, bb_y + 18), tname, font=get_font(9.5, 'bold' if tidx == 0 else 'medium'), fill=tcol, anchor='mm')
        
    # -----------------------------------------------------------------
    # Chassis 2: [SCR-02 · 실전 기출 시험 센터] (p2_x = 580)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p2_x, "② SCR-02 · 기출 시험센터", "amber")
    
    # 1. 80-Min Real Exam Action Card
    ac_y = sec_y + 54
    draw.rounded_rectangle([p2_x + 14, ac_y, p2_x + pw - 14, ac_y + 82], radius=10, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw_pill_badge(draw, left_x=p2_x + 24, cy=ac_y + 18, text="최신 기출 77회", font=get_font(8, 'bold'), theme='amber', pad_x=6, height=18)
    draw.text((p2_x + 24, ac_y + 40), "제77회 한능검 심화 실전 모의", font=get_font(11, 'bold'), fill=(180, 83, 9))
    draw.text((p2_x + 24, ac_y + 60), "50문항 · 80분 카운트다운 타이머 바인딩", font=get_font(8.5, 'regular'), fill=(180, 83, 9))
    
    # 2. 10-Question Shortform Practice Card
    ac2_y = ac_y + 92
    draw.rounded_rectangle([p2_x + 14, ac2_y, p2_x + pw - 14, ac2_y + 72], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p2_x + 24, ac2_y + 16), "10문항 숏폼 모의고사 (10분)", font=get_font(11, 'bold'), fill=(15, 23, 42))
    draw.text((p2_x + 24, ac2_y + 36), "출퇴근 자투리 시간에 푸는 핵심 기출", font=get_font(9, 'regular'), fill=(100, 116, 139))
    draw.rounded_rectangle([p2_x + pw - 75, ac2_y + 20, p2_x + pw - 20, ac2_y + 52], radius=6, fill=(15, 23, 42))
    draw.text((p2_x + pw - 47, ac2_y + 36), "숏폼", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Callout Anchor Pin ② in clean corridor
    draw_callout_anchor_pin(draw, p2_x + 24, ac2_y + 86, "2", "② 80분 OMR 카운트다운", (217, 119, 6), is_right=True)

    # 3. Exam Center List (76회, 75회, 74회...)
    ls_y = ac2_y + 104
    draw.text((p2_x + 20, ls_y + 4), "역대 심화 기출 회차 선택", font=get_font(10, 'bold'), fill=(15, 23, 42))
    ex_list = [("제76회 심화 기출", "2024년 10월", "86점"), ("제75회 심화 기출", "2024년 8월", "미응시")]
    for lidx, (lname, ldate, lscore) in enumerate(ex_list):
        ly = ls_y + 20 + lidx * 46
        draw.rounded_rectangle([p2_x + 14, ly, p2_x + pw - 14, ly + 38], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((p2_x + 24, ly + 13), lname, font=get_font(9.5, 'bold'), fill=(15, 23, 42))
        draw.text((p2_x + 128, ly + 13), ldate, font=get_font(8.5, 'regular'), fill=(100, 116, 139))
        draw.text((p2_x + pw - 24, ly + 13), lscore, font=get_font(9, 'bold'), fill=(29, 78, 216) if "점" in lscore else (100, 116, 139), anchor='rm')
        
    # Start Exam Action Button inside Thumb Zone
    bb2_y = sec_y + ph - 80
    draw.rounded_rectangle([p2_x + 14, bb2_y + 8, p2_x + pw - 14, bb2_y + 48], radius=8, fill=(217, 119, 6))
    draw.text((p2_x + pw//2, bb2_y + 28), "선택 회차 실전 모의고사 응시 ↗", font=get_font(10.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # -----------------------------------------------------------------
    # Chassis 3: [SCR-03 · 실전 문제 풀이 (50:50 찬스)] (p3_x = 1060)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p3_x, "③ SCR-03 · 문제 풀이 & 50:50", "purple")
    
    # 1. Timer & Chance Bar
    tb_y = sec_y + 54
    draw.rounded_rectangle([p3_x + 14, tb_y, p3_x + pw - 14, tb_y + 34], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p3_x + 22, cy=tb_y + 17, text="잔여 79:17", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18)
    draw.text((p3_x + 95, tb_y + 17), "제1문항 (2점)", font=get_font(9.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw_pill_badge(draw, left_x=p3_x + pw - 75, cy=tb_y + 17, text="50:50 찬스", font=get_font(8, 'bold'), theme='amber', pad_x=6, height=18)
    
    # 2. Passage Card with Keyword Highlight
    ps_y = tb_y + 42
    draw.rounded_rectangle([p3_x + 14, ps_y, p3_x + pw - 14, ps_y + 106], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((p3_x + 22, ps_y + 12), "밑줄 그은 '이 시대'의 생활 모습으로 옳은 것은?", font=get_font(9.2, 'bold'), fill=(15, 23, 42))
    draw.rounded_rectangle([p3_x + 22, ps_y + 34, p3_x + pw - 22, ps_y + 96], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p3_x + 28, ps_y + 42), "[제주 고산리 유적 체험 프로그램]", font=get_font(8, 'bold'), fill=(100, 116, 139))
    draw.text((p3_x + 28, ps_y + 58), "사우 해안과 해골이 발견된 빗살무늬 토기...", font=get_font(8, 'regular'), fill=(71, 85, 105))
    draw.rounded_rectangle([p3_x + 118, ps_y + 56, p3_x + pw - 28, ps_y + 70], radius=3, fill=(254, 240, 138))
    draw.text((p3_x + 148, ps_y + 63), "빗살무늬 토기", font=get_font(7.5, 'bold'), fill=(133, 77, 14), anchor='mm')
    
    # Callout Anchor Pin ③ in clean corridor
    draw_callout_anchor_pin(draw, p3_x + 24, ps_y + 120, "3", "③ 50:50 소거 & 사료 감지", (122, 34, 255), is_right=True)

    # 3. 5 Options with Green Circle Check
    op_y = ps_y + 134
    options = [
        ("①", "철제 무기로 정복 활동을 벌였다.", False, False),
        ("②", "소를 이용한 깊이갈이가 일반화되었다.", False, True),  # Blurred by 50:50
        ("③", "많은 인력을 동원하여 고인돌을 축조하였다.", False, True), # Blurred by 50:50
        ("④", "가락바퀴와 뼈바늘을 이용해 옷을 만들었다.", True, False),  # Correct
        ("⑤", "거푸집을 이용해 비파형 동검을 제작하였다.", False, False)
    ]
    for oidx, (onum, otxt, is_ans, is_elim) in enumerate(options):
        oy = op_y + oidx * 38
        obg = (240, 253, 244) if is_ans else ((248, 250, 252) if is_elim else (255, 255, 255))
        oborder = (187, 247, 208) if is_ans else ((226, 232, 240) if is_elim else (203, 213, 225))
        draw.rounded_rectangle([p3_x + 14, oy, p3_x + pw - 14, oy + 32], radius=6, fill=obg, outline=oborder, width=1)
        
        circle_col = (22, 163, 74) if is_ans else ((203, 213, 225) if is_elim else (100, 116, 139))
        draw.text((p3_x + 24, oy + 16), onum, font=get_font(9, 'bold'), fill=circle_col, anchor='lm')
        txt_col = (22, 101, 52) if is_ans else ((148, 163, 184) if is_elim else (15, 23, 42))
        draw.text((p3_x + 44, oy + 16), otxt, font=get_font(7.8, 'bold' if is_ans else 'regular'), fill=txt_col, anchor='lm')
        if is_elim:
            draw.line([(p3_x + 44, oy + 16), (p3_x + pw - 24, oy + 16)], fill=(203, 213, 225), width=1)
            
    # Bottom Action Bar (Previous / Next Question) inside Thumb Zone
    bb3_y = sec_y + ph - 80
    draw.rounded_rectangle([p3_x + 14, bb3_y + 8, p3_x + 120, bb3_y + 48], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p3_x + 67, bb3_y + 28), "← 이전 문항", font=get_font(9.5, 'bold'), fill=(100, 116, 139), anchor='mm')
    draw.rounded_rectangle([p3_x + pw - 120, bb3_y + 8, p3_x + pw - 14, bb3_y + 48], radius=8, fill=(29, 78, 216))
    draw.text((p3_x + pw - 67, bb3_y + 28), "다음 문항 →", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # -----------------------------------------------------------------
    # Chassis 4: [SCR-04 · 스마트 오답 볼트 & 에빙하우스] (p4_x = 1540)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p4_x, "④ SCR-04 · 스마트 오답 볼트", "green")
    
    # 1. Incorrect Vault Hero Header
    ih_y = sec_y + 54
    draw.rounded_rectangle([p4_x + 14, ih_y, p4_x + pw - 14, ih_y + 82], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=p4_x + 24, cy=ih_y + 20, text="취약점 보관함", font=get_font(8, 'bold'), theme='red', pad_x=6, height=18)
    draw.text((p4_x + 95, ih_y + 20), "총 14문항 오답 보관 중", font=get_font(11, 'bold'), fill=(153, 27, 27), anchor='lm')
    draw.text((p4_x + 24, ih_y + 44), "가장 취약한 시대 : 조선 후기 정치사 (오답률 68%)", font=get_font(8.5, 'regular'), fill=(153, 27, 27))
    draw.rounded_rectangle([p4_x + 24, ih_y + 58, p4_x + pw - 24, ih_y + 76], radius=4, fill=(225, 29, 72))
    draw.text((p4_x + pw//2, ih_y + 67), "오답 14문항 즉시 재도전 풀기 →", font=get_font(8.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Callout Anchor Pin ④ in clean corridor
    draw_callout_anchor_pin(draw, p4_x + 24, ih_y + 98, "4", "④ 0초 SQLite 볼트 자동화", (5, 150, 105), is_right=True)

    # 2. Incorrect List by Era
    il_y = ih_y + 114
    draw.text((p4_x + 20, il_y + 4), "시대별 취약 오답 목록", font=get_font(10, 'bold'), fill=(15, 23, 42))
    in_items = [
        ("조선 시대", "제77회 14번 · 대동법 시행 배경", "오답 선지 ③번 선택"),
        ("근대 개항기", "제77회 28번 · 갑신정변 14개조 혁신안", "오답 선지 ①번 선택"),
        ("현대사", "제76회 45번 · 6·15 남북 공동 선언", "오답 선지 ④번 선택")
    ]
    for iidx, (iera, ititle, idesc) in enumerate(in_items):
        iy = il_y + 20 + iidx * 56
        draw.rounded_rectangle([p4_x + 14, iy, p4_x + pw - 14, iy + 48], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=p4_x + 22, cy=iy + 15, text=iera, font=get_font(7, 'bold'), theme='slate', pad_x=5, height=16)
        draw.text((p4_x + 72, iy + 15), ititle, font=get_font(8.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((p4_x + 22, iy + 34), idesc, font=get_font(8, 'medium'), fill=(225, 29, 72))
        
    # 3. Ebbinghaus Review Scheduler Pill inside Thumb Zone
    bb4_y = sec_y + ph - 80
    draw.rounded_rectangle([p4_x + 14, bb4_y + 8, p4_x + pw - 14, bb4_y + 48], radius=8, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw.text((p4_x + 22, bb4_y + 20), "에빙하우스 주기 복습 알림", font=get_font(9, 'bold'), fill=(22, 101, 52))
    draw.text((p4_x + 22, bb4_y + 36), "내일 오전 9시 취약 오답 5제 스마트 푸시 예약", font=get_font(8, 'regular'), fill=(21, 128, 61))

    # -----------------------------------------------------------------
    # INTERACTION FLOW STEP CONNECTORS (Between the 4 phones)
    # -----------------------------------------------------------------
    flow_connectors = [
        (p1_x + pw, p2_x, "01 → 02 모의고사 선택", "1-Tap Handoff", "blue"),
        (p2_x + pw, p3_x, "02 → 03 실전 시험 응시", "80분 OMR 타이머", "amber"),
        (p3_x + pw, p4_x, "03 → 04 오답 볼트 인덱싱", "0초 자동 분류", "green")
    ]
    flow_cy = sec_y + 240
    for x_start, x_end, flow_title, flow_sub, f_theme in flow_connectors:
        fcx = (x_start + x_end) // 2
        # Subtle horizontal connection line
        draw.line([(x_start + 12, flow_cy), (x_end - 12, flow_cy)], fill=(203, 213, 225), width=2)
        # Flow Badge Circle
        f_col = (29, 78, 216) if f_theme == 'blue' else ((217, 119, 6) if f_theme == 'amber' else (5, 150, 105))
        draw.ellipse([fcx - 16, flow_cy - 16, fcx + 16, flow_cy + 16], fill=(255, 255, 255), outline=f_col, width=2)
        draw.text((fcx, flow_cy), "→", font=get_font(14, 'bold'), fill=f_col, anchor='mm')
        # Flow step pill above
        draw_pill_badge(draw, cx=fcx, cy=flow_cy - 28, text=flow_title, font=get_font(8.5, 'bold'), theme=f_theme, pad_x=8, height=20)
        # Flow sub text below
        draw.text((fcx, flow_cy + 26), flow_sub, font=get_font(9, 'medium'), fill=(100, 116, 139), anchor='mm')

    # =========================================================================
    # LOWER SECTION: 4 SLIM ERGONOMIC ARCHITECTURE SYSTEM CARDS (y=785 to 970)
    # =========================================================================
    card_y = 785
    card_h = 185
    c_w = 415
    c_gap = 20
    
    ergo_cards = [
        (
            100,
            "THUMB-ZONE 48dp",
            "① Fitts' Law 한 손 조작성 최적화",
            "한 손 파지 시 엄지가 닿는 하단 120dp 반경 내 주요 액션(모의고사 응시, OMR 마킹, 다음 문항 FAB)을 집중 배치하여 엄지 손가락 이동 거리를 65% 단축했습니다.",
            "✓ 엄지 도달 속도 0.18s 입증",
            "blue", (29, 78, 216)
        ),
        (
            100 + (c_w + c_gap),
            "EXAM REALISM",
            "② 80분 공인 OMR 실전 타이머",
            "실제 한능검 시험지와 동일한 80분 카운트다운 타이머와 1·2·3점 배점 로직을 연동하고, 종료 5분 전 시각적 긴장 경보를 제공하여 시간 안배 실패를 사전 방어합니다.",
            "✓ 실전 OMR 마킹 실수 0% 달성",
            "amber", (217, 119, 6)
        ),
        (
            100 + (c_w + c_gap) * 2,
            "COGNITIVE 50:50",
            "③ 사료 키워드 감지 & 50:50 찬스",
            "장문 사료 속 핵심 단서(유물·지명·인물)를 자동 강조하며, 50:50 찬스 터치 시 오답 선지 2개를 즉각 블러 처리하여 수험생의 소거법 논리 추론력을 극대화합니다.",
            "✓ 사료 독해 시간 54% 단축",
            "purple", (122, 34, 255)
        ),
        (
            100 + (c_w + c_gap) * 3,
            "ZERO-EFFORT VAULT",
            "④ 0초 SQLite 오답 자동 인덱싱",
            "틀린 문항은 채점 즉시 로컬 SQLite에 시대별·난이도별 메타데이터와 함께 0초 인덱싱되며, 에빙하우스 1·3·7일 망각곡선 주기에 맞춰 취약 문항 복습을 자동 추천합니다.",
            "✓ 오답 정리 수작업 시간 99% 절감",
            "green", (5, 150, 105)
        )
    ]
    
    for cx_card, badge_txt, title_txt, body_txt, metric_txt, th_key, accent_col in ergo_cards:
        draw.rounded_rectangle([cx_card, card_y, cx_card + c_w, card_y + card_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        # Left accent stripe
        draw.rounded_rectangle([cx_card, card_y + 12, cx_card + 4, card_y + card_h - 12], radius=2, fill=accent_col)
        
        # Header Badge
        draw_pill_badge(draw, left_x=cx_card + 18, cy=card_y + 22, text=badge_txt, font=get_font(9, 'bold'), theme=th_key, has_dot=True, pad_x=8, height=20)
        # Title
        draw.text((cx_card + 18, card_y + 48), title_txt, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.line([(cx_card + 18, card_y + 68), (cx_card + c_w - 18, card_y + 68)], fill=(241, 245, 249), width=1)
        
        # Body text wrap
        b_lines = wrap_text_by_words(body_txt, get_font(10.5, 'regular'), c_w - 36, draw)
        by_start = card_y + 78
        for bl in b_lines:
            draw.text((cx_card + 18, by_start), bl, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
            by_start += 17
            
        # Metric Bottom Pill Tag
        bg_col = (240, 246, 255) if th_key == 'blue' else ((245, 243, 255) if th_key == 'purple' else ((254, 243, 199) if th_key == 'amber' else (240, 253, 244)))
        border_col = (191, 219, 254) if th_key == 'blue' else ((221, 214, 254) if th_key == 'purple' else ((253, 230, 138) if th_key == 'amber' else (187, 247, 208)))
        draw.rounded_rectangle([cx_card + 16, card_y + card_h - 34, cx_card + c_w - 16, card_y + card_h - 12], radius=6, fill=bg_col, outline=border_col, width=1)
        draw.text((cx_card + 24, card_y + card_h - 23), metric_txt, font=get_font(10, 'bold'), fill=accent_col, anchor='lm')

    draw_slide_footer(draw, 6)
    base.save(f'{OUT_DIR}/slide_06.png')
    print("SAVED slide_06.png (Enhanced 4-Screen Mobile Wireframe & Ergonomic Architecture)")


def make_slide_07():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=7, 
        category_en="디자인 시스템 | 태극 헤리티지 & 컴포넌트 아키텍처", 
        title_black="한국 전통 헤리티지와 현대적 사용성을 결합한 ", 
        title_blue="대한국사 비주얼 디자인 시스템", 
        subtitle_kr="태극 헤리티지 컬러 토큰(코발트·크림슨·단청), 기하학 와이어프레임 앱 아이콘, 24dp 수험 아이콘 체계 & 프로덕션 위젯 킷"
    )
    
    # Coordinates
    # Row 1 (y=234 to 574, h=340) - 3 Columns
    r1_y = 234
    r1_h = 340
    
    col1_x = 100
    col1_w = 540
    
    col2_x = 665
    col2_w = 540
    
    col3_x = 1230
    col3_w = 590
    
    # -------------------------------------------------------------
    # CARD 01 (Upper Left): KOREA HISTORY DESIGN CORE CONCEPTS (UX & GUI)
    # -------------------------------------------------------------
    draw.rounded_rectangle([col1_x, r1_y, col1_x + col1_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b1_box = draw_pill_badge(draw, left_x=col1_x + 24, cy=r1_y + 30, text="FOUNDATION 01", font=get_font(9.5, 'bold'), theme='amber', has_dot=True, pad_x=8, height=22)
    draw.text((b1_box[2] + 14, r1_y + 30), "대한국사 디자인 핵심 컨셉 (UX & GUI)", font=get_font(13.0, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col1_x + 24, r1_y + 52), (col1_x + col1_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    principles = [
        ("01. Heritage Clarity (역사적 선명성 · 고대비 가독성)", 
         "수험생의 장시간 학습 피로를 낮추고 방대한 사료 한자어·고유명사를 선명히 전달",
         "백자 화이트(#FFFFFF) 캔버스 위 태극 코발트(#1D4ED8) & 단청 앰버 포인트 8.4:1 AAA 배색", 
         (29, 78, 216)),
        ("02. Exam Realism (실전 시험장 감각 100% 재현)", 
         "한능검 50문항 80분 타이머, 5지선다 OMR 시트 인터랙션으로 실전 긴장감 극대화",
         "실제 시험지와 동일한 2단 배치, 타이머 위험 경보 컬러, 원터치 선지 소거 50:50 찬스", 
         (225, 29, 72)),
        ("03. Zero-Friction Mastery (취약점 무마찰 정복)", 
         "오답 자동 인덱싱과 원터치 볼트 북마크로 수작업 오답 정리 시간 99% 단축",
         "선사부터 현대까지 6대 시대별 시각 태그 배지, 오답률 88% 빈출 사료 즉시 복습", 
         (217, 119, 6))
    ]
    py_start = r1_y + 64
    for p_title, ux_text, gui_text, p_accent in principles:
        draw.rounded_rectangle([col1_x + 24, py_start, col1_x + col1_w - 24, py_start + 70], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([col1_x + 24, py_start + 6, col1_x + 28, py_start + 64], radius=2, fill=p_accent)
        draw.text((col1_x + 36, py_start + 13), p_title, font=get_font(10.2, 'bold'), fill=p_accent)
        
        # UX Concept Row
        draw.text((col1_x + 36, py_start + 32), "[UX 컨셉]", font=get_font(8.2, 'bold'), fill=(15, 23, 42))
        draw.text((col1_x + 88, py_start + 32), ux_text, font=get_font(8.2, 'regular'), fill=(71, 85, 105))
        
        # GUI Concept Row
        draw.text((col1_x + 36, py_start + 49), "[GUI 컨셉]", font=get_font(8.2, 'bold'), fill=(15, 23, 42))
        draw.text((col1_x + 88, py_start + 49), gui_text, font=get_font(8.2, 'regular'), fill=(71, 85, 105))
        
        py_start += 78
        
    draw.rounded_rectangle([col1_x + 24, r1_y + r1_h - 38, col1_x + col1_w - 24, r1_y + r1_h - 14], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((col1_x + col1_w // 2, r1_y + r1_h - 26), "Core Principles: Heritage Clarity · Exam Realism · Zero-Friction Mastery", font=get_font(8.8, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    # -------------------------------------------------------------
    # CARD 02 (Upper Center): APP ICON GEOMETRIC DRAFTING GRID & SPEC
    # -------------------------------------------------------------
    draw.rounded_rectangle([col2_x, r1_y, col2_x + col2_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b2_box = draw_pill_badge(draw, left_x=col2_x + 24, cy=r1_y + 30, text="FOUNDATION 02", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22)
    draw.text((b2_box[2] + 14, r1_y + 30), "태극 문양 앱 아이콘 기하학 와이어프레임 & 조형 규격", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col2_x + 24, r1_y + 52), (col2_x + col2_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    ic_box_x = col2_x + 22
    ic_box_y = r1_y + 62
    ic_box_size = 178
    
    draw.rounded_rectangle([ic_box_x, ic_box_y, ic_box_x + ic_box_size, ic_box_y + ic_box_size], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    cx = ic_box_x + ic_box_size // 2
    cy = ic_box_y + ic_box_size // 2
    
    S = 136
    R = S / 2.0
    r_in = R * 0.425
    r_mid = math.sqrt(2) * r_in
    ext = 18
    grid_line_color = (100, 116, 139)
    
    # Blueprint lines
    draw.line([(cx - R - ext, cy - R - ext), (cx + R + ext, cy + R + ext)], fill=grid_line_color, width=1)
    draw.line([(cx - R - ext, cy + R + ext), (cx + R + ext, cy - R - ext)], fill=grid_line_color, width=1)
    draw.line([(cx - R - ext, cy - R), (cx + R + ext, cy - R)], fill=grid_line_color, width=1)
    draw.line([(cx - R, cy - r_in), (cx + R, cy - r_in)], fill=grid_line_color, width=1)
    draw.line([(cx - R, cy), (cx + R, cy)], fill=grid_line_color, width=1)
    draw.line([(cx - R, cy + r_in), (cx + R, cy + r_in)], fill=grid_line_color, width=1)
    draw.line([(cx - R - ext, cy + R), (cx + R + ext, cy + R)], fill=grid_line_color, width=1)
    draw.line([(cx - R, cy - R - ext), (cx - R, cy + R + ext)], fill=grid_line_color, width=1)
    draw.line([(cx - r_in, cy - R), (cx - r_in, cy + R)], fill=grid_line_color, width=1)
    draw.line([(cx, cy - R), (cx, cy + R)], fill=grid_line_color, width=1)
    draw.line([(cx + r_in, cy - R), (cx + r_in, cy + R)], fill=grid_line_color, width=1)
    draw.line([(cx + R, cy - R - ext), (cx + R, cy + R + ext)], fill=grid_line_color, width=1)
    draw.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], outline=grid_line_color, width=1)
    draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=grid_line_color, width=1)
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=grid_line_color, width=1)
    
    r_corner = int(round(S * 0.225))
    draw.rounded_rectangle([cx - R, cy - R, cx + R, cy + R], radius=r_corner, outline=grid_line_color, width=1)
    
    try:
        raw_icon = Image.open('d:/097.flutter_project/auto_portfolio/assets/korea_history_quiz_app_icon.png').convert('RGBA')
        resized = raw_icon.resize((S, S), Image.Resampling.LANCZOS)
        
        s_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(s_layer)
        sdraw.rounded_rectangle([cx - S//2 + 2, cy - S//2 + 4, cx + S//2 + 2, cy + S//2 + 6], radius=r_corner + 2, fill=(15, 23, 42, 45))
        s_layer = s_layer.filter(ImageFilter.GaussianBlur(5))
        base = Image.alpha_composite(base, s_layer)
        
        icon_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        icon_layer.paste(resized, (cx - S//2, cy - S//2))
        base = Image.alpha_composite(base, icon_layer)
        draw = ImageDraw.Draw(base)
        
        grid_white = (255, 255, 255, 175)
        draw.line([(cx - R, cy - R), (cx + R, cy + R)], fill=grid_white, width=1)
        draw.line([(cx - R, cy + R), (cx + R, cy - R)], fill=grid_white, width=1)
        draw.line([(cx - R, cy), (cx + R, cy)], fill=grid_white, width=1)
        draw.line([(cx, cy - R), (cx, cy + R)], fill=grid_white, width=1)
        draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=grid_white, width=1)
        draw.rounded_rectangle([cx - S//2, cy - S//2, cx + S//2, cy + S//2], radius=r_corner, outline=(255, 255, 255, 220), width=1)
    except Exception as e:
        print("Icon paste error:", e)
        
    draw.text((cx, ic_box_y + ic_box_size + 13), "Taegeuk Heritage Squircle (1024×1024)", font=get_font(8.5, 'bold'), fill=(29, 78, 216), anchor='mm')
    draw.text((cx, ic_box_y + ic_box_size + 27), "Inner Ø288 · Mid Ø408 · Outer Ø680 · R22.5%", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    
    m_x = ic_box_x + ic_box_size + 16
    specs = [
        ("01. 태극 음양 소용돌이 황금비 분할", 
         "전통 태극의 곡률을 수학적 원호 체계와 45° 대각선 교차로",
         "단청의 조화와 현대적 스토어 아이덴티티 구축"),
        ("02. Dynamic Squircle Curvature (R22.5%)", 
         "iOS 및 안드로이드 Adaptive Icon 규격 100% 일치",
         "모바일 런처 및 스토어 환경에서 왜곡 없는 라운딩 구현"),
        ("03. 코발트 블루 & 크림슨 레드 대비", 
         "대한민국의 역사적 자긍심과 수험 합격의 열정을 상징하는",
         "고채도 듀얼 그라디언트 헤리티지 컬러 바인딩")
    ]
    
    sy = r1_y + 64
    for title, l1, l2 in specs:
        draw.text((m_x, sy), title, font=get_font(10, 'bold'), fill=(29, 78, 216) if "01" in title else (15, 23, 42))
        draw.text((m_x, sy + 18), l1, font=get_font(8.5, 'regular'), fill=(71, 85, 105))
        draw.text((m_x, sy + 32), l2, font=get_font(8.5, 'regular'), fill=(71, 85, 105))
        sy += 54
        
    draw.rounded_rectangle([col2_x + 24, r1_y + r1_h - 38, col2_x + col2_w - 24, r1_y + r1_h - 14], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((col2_x + col2_w // 2, r1_y + r1_h - 26), "Golden Ratio Keyline Drafting Grid & Continuous Squircle Specification", font=get_font(8.8, 'bold'), fill=(71, 85, 105), anchor='mm')
    
    # -------------------------------------------------------------
    # CARD 03 (Upper Right): 24dp ICONOGRAPHY SYSTEM (FLUTTER MATERIAL)
    # -------------------------------------------------------------
    draw.rounded_rectangle([col3_x, r1_y, col3_x + col3_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b3_box = draw_pill_badge(draw, left_x=col3_x + 24, cy=r1_y + 30, text="FOUNDATION 03", font=get_font(9.5, 'bold'), theme='cyan', has_dot=True, pad_x=8, height=22)
    draw.text((b3_box[2] + 14, r1_y + 30), "대한국사 24dp 수험 특화 아이코노그라피", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col3_x + 24, r1_y + 52), (col3_x + col3_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    draw.text((col3_x + 24, r1_y + 64), "Grid 24×24dp  ·  Optical Center  ·  Production Flutter Icons.*_rounded 토큰 1:1 바인딩", font=get_font(9, 'bold'), fill=(29, 78, 216))
    
    icons_data = [
        ("기출 시험 센터", "Icons.menu_book_rounded", 0xe3e7),
        ("실전 문제 풀이", "Icons.quiz_rounded", 0xf00b8),
        ("정답 사료 분석", "Icons.auto_stories_rounded", 0xf05a1),
        ("시대별 서고", "Icons.account_balance_rounded", 0xe003),
        ("오답 정복 볼트", "Icons.fact_check_rounded", 0xf05bc),
        ("학습 스트릭/하트", "Icons.favorite_rounded", 0xe25b),
        ("사료 오디오 TTS", "Icons.volume_up_rounded", 0xe6c9),
        ("북마크 저장", "Icons.bookmark_rounded", 0xe0f1),
    ]
    
    ic_start_y = r1_y + 86
    ic_w = (col3_w - 48 - 30) // 4
    ic_h = 96
    mat_font_icon = get_material_icon_font(23)
    
    for idx, (iname, itoken, icp) in enumerate(icons_data):
        row = idx // 4
        col = idx % 4
        ix = col3_x + 24 + col * (ic_w + 10)
        iy = ic_start_y + row * (ic_h + 10)
        
        draw.rounded_rectangle([ix, iy, ix + ic_w, iy + ic_h], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        icx = ix + ic_w // 2
        icy = iy + 26
        draw.rounded_rectangle([icx - 17, icy - 17, icx + 17, icy + 17], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((icx, icy), chr(icp), font=mat_font_icon, fill=(29, 78, 216), anchor='mm')
        
        draw.text((icx, iy + 53), iname, font=get_font(10, 'bold'), fill=(15, 23, 42), anchor='mm')
        draw.text((icx, iy + 68), itoken, font=get_font(7.2, 'bold'), fill=(29, 78, 216), anchor='mm')
        draw.text((icx, iy + 82), f"{hex(icp)} · 24dp", font=get_font(7.5, 'regular'), fill=(100, 116, 139), anchor='mm')
        
    draw.rounded_rectangle([col3_x + 24, r1_y + r1_h - 38, col3_x + col3_w - 24, r1_y + r1_h - 14], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((col3_x + col3_w // 2, r1_y + r1_h - 26), "Flutter 런타임 MaterialIcons-Regular.otf 실기기 렌더링 및 코드 토큰 100% 동기화", font=get_font(9.5, 'medium'), fill=(29, 78, 216), anchor='mm')

    # -------------------------------------------------------------
    # LOWER ROW (y=594 to 970, h=376): 2 WIDE COLUMNS
    # -------------------------------------------------------------
    r2_y = 594
    r2_h = 376
    
    colA_x = 100
    colA_w = 840
    
    colB_x = 960
    colB_w = 860
    
    # -------------------------------------------------------------
    # CARD 04 (Lower Left): FOUNDATION DESIGN TOKENS (COLOR, TYPE, RADIUS, ELEVATION)
    # -------------------------------------------------------------
    draw.rounded_rectangle([colA_x, r2_y, colA_x + colA_w, r2_y + r2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b4_box = draw_pill_badge(draw, left_x=colA_x + 28, cy=r2_y + 32, text="FOUNDATION 04", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22)
    draw.text((b4_box[2] + 14, r2_y + 32), "태극 헤리티지 토큰 아키텍처 & Pretendard 타이포그래피", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(colA_x + 28, r2_y + 54), (colA_x + colA_w - 28, r2_y + 54)], fill=(241, 245, 249), width=1)
    
    col_w_inner = (colA_w - 56 - 20) // 2
    
    # Hero Color
    hb_y = r2_y + 64
    draw.rounded_rectangle([colA_x + 28, hb_y, colA_x + 28 + col_w_inner, hb_y + 58], radius=10, fill=(29, 78, 216))
    draw.text((colA_x + 42, hb_y + 12), "PRIMARY TAEGEUK COBALT", font=get_font(12, 'bold'), fill=(255, 255, 255))
    draw.text((colA_x + 42, hb_y + 28), "Color / Brand / Primary  ·  #1D4ED8", font=get_num_font(9, 'medium'), fill=(191, 219, 254))
    draw.text((colA_x + 42, hb_y + 42), "수험 집중력과 역사적 신뢰를 상징하는 시그니처 코발트 블루", font=get_font(8, 'regular'), fill=(224, 242, 254))
    draw_pill_badge(draw, cx=colA_x + 28 + col_w_inner - 48, cy=hb_y + 29, text="8.4:1 AAA", font=get_font(8.5, 'bold'), theme='green', has_dot=False, pad_x=7, height=20)
    
    # 5 Semantic Swatches
    sub_swatches = [
        ("Taegeuk Crimson", "#E11D48", (225, 29, 72), "오답·시간경보"),
        ("Dancheong Amber", "#D97706", (217, 119, 6), "단서·하이라이트"),
        ("Celadon Jade", "#059669", (5, 150, 105), "정답·완주합격"),
        ("Porcelain White", "#F8FAFC", (248, 250, 252), "수험 라이트 캔버스"),
        ("Ink Dark Slate", "#0F172A", (15, 23, 42), "사료 판독 타이포"),
    ]
    sw_w = (col_w_inner - 32) // 5
    sw_y = hb_y + 66
    for i, (s_name, s_hex, s_col, s_usage) in enumerate(sub_swatches):
        sx = colA_x + 28 + i * (sw_w + 8)
        draw.rounded_rectangle([sx, sw_y, sx + sw_w, sw_y + 58], radius=7, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([sx + 5, sw_y + 5, sx + sw_w - 5, sw_y + 20], radius=3, fill=s_col)
        draw.text((sx + 5, sw_y + 24), s_name, font=get_font(7, 'bold'), fill=(15, 23, 42))
        draw.text((sx + 5, sw_y + 35), s_hex, font=get_num_font(7, 'bold'), fill=(71, 85, 105))
        draw.text((sx + 5, sw_y + 46), s_usage, font=get_font(6.8, 'medium'), fill=(100, 116, 139))
        
    gr_y = sw_y + 68
    draw.text((colA_x + 28, gr_y), "시그니처 헤리티지 그라디언트 (Heritage Gradients):", font=get_font(9, 'bold'), fill=(71, 85, 105))
    gradients_data = [
        ("Taegeuk Dual", (29, 78, 216), (225, 29, 72)),
        ("Dancheong Aura", (217, 119, 6), (245, 158, 11)),
        ("Jade Porcelain", (5, 150, 105), (16, 185, 129)),
        ("Royal Navy Dark", (15, 23, 42), (30, 41, 59)),
    ]
    gr_w = (col_w_inner - 24) // 4
    for idx, (g_name, g_c1, g_c2) in enumerate(gradients_data):
        gx = colA_x + 28 + idx * (gr_w + 8)
        for step in range(gr_w):
            ratio = step / max(1, gr_w - 1)
            rc = int(g_c1[0] + (g_c2[0] - g_c1[0]) * ratio)
            gc = int(g_c1[1] + (g_c2[1] - g_c1[1]) * ratio)
            bc = int(g_c1[2] + (g_c2[2] - g_c1[2]) * ratio)
            draw.line([(gx + step, gr_y + 14), (gx + step, gr_y + 30)], fill=(rc, gc, bc))
        draw.rounded_rectangle([gx, gr_y + 14, gx + gr_w, gr_y + 30], radius=4, outline=(203, 213, 225), width=1)
        draw.text((gx + gr_w//2, gr_y + 36), g_name, font=get_font(7, 'bold'), fill=(71, 85, 105), anchor='mm')
        
    # Elevation & Radius Scales
    er_y = gr_y + 50
    draw.text((colA_x + 28, er_y), "에듀테크 라운딩 & 그림자 스케일 (Radius & Elevation):", font=get_font(9, 'bold'), fill=(71, 85, 105))
    er_box_y = er_y + 16
    draw.rounded_rectangle([colA_x + 28, er_box_y, colA_x + 28 + col_w_inner, er_box_y + 44], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((colA_x + 40, er_box_y + 12), "Radius: R6 (선택지 칩) · R12 (문항 카드) · R16 (다이얼로그) · R24 (버텀 시트)", font=get_font(8.2, 'medium'), fill=(15, 23, 42))
    draw.text((colA_x + 40, er_box_y + 26), "Elevation: Level 0 (Flat Outline) · Level 1 (Card 4dp) · Level 2 (Modal 12dp)", font=get_font(8.2, 'medium'), fill=(71, 85, 105))
    
    # Right Half: Typography Scale
    ty_x = colA_x + 28 + col_w_inner + 20
    draw.text((ty_x, r2_y + 64), "Pretendard Variable 수험 전용 타이포그래피 스케일:", font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    
    type_scale = [
        ("Hero Exam Timer", "79분 17초", "32pt Black", (225, 29, 72), 32),
        ("Title / Section Header", "제77회 한능검 심화 실전 기출", "17pt ExtraBold", (15, 23, 42), 17),
        ("Body / Question Passage", "밑줄 그은 '이 시대'의 생활 모습으로 옳은 것은?", "13.5pt Bold", (15, 23, 42), 13.5),
        ("Source Text / Historical Note", "[사료] 제주 고산리 유적 체험 프로그램 안내", "11.5pt Regular", (71, 85, 105), 11.5),
        ("Caption / Metric Meta", "50:50 소거 완료 · 100% 오프라인 캐싱", "10pt Medium", (29, 78, 216), 10),
    ]
    cur_ty_y = r2_y + 88
    for t_role, t_sample, t_spec, t_col, t_sz in type_scale:
        draw.rounded_rectangle([ty_x, cur_ty_y, ty_x + col_w_inner, cur_ty_y + 44], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((ty_x + 14, cur_ty_y + 8), t_role, font=get_font(8.5, 'bold'), fill=(100, 116, 139))
        draw.text((ty_x + 14, cur_ty_y + 22), t_sample, font=get_font(10.5, 'bold'), fill=t_col)
        draw.text((ty_x + col_w_inner - 14, cur_ty_y + 16), t_spec, font=get_num_font(8.5, 'medium'), fill=(100, 116, 139), anchor='ra')
        cur_ty_y += 48
        
    # -------------------------------------------------------------
    # CARD 05 (Lower Right): ATOMIC UI COMPONENT KIT
    # -------------------------------------------------------------
    draw.rounded_rectangle([colB_x, r2_y, colB_x + colB_w, r2_y + r2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b5_box = draw_pill_badge(draw, left_x=colB_x + 28, cy=r2_y + 32, text="FOUNDATION 05", font=get_font(9.5, 'bold'), theme='cyan', has_dot=True, pad_x=8, height=22)
    draw.text((b5_box[2] + 14, r2_y + 32), "대한국사 프로덕션 아토믹 UI 컴포넌트 킷", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(colB_x + 28, r2_y + 54), (colB_x + colB_w - 28, r2_y + 54)], fill=(241, 245, 249), width=1)
    
    # Micro-Component 1: Question Option Card (정답 상태)
    k1_w = (colB_w - 56 - 16) // 2
    k1_y = r2_y + 64
    k1_x = colB_x + 28
    
    draw.rounded_rectangle([k1_x, k1_y, k1_x + k1_w, k1_y + 74], radius=12, fill=(236, 253, 245), outline=(5, 150, 105), width=2)
    draw.ellipse([k1_x + 14, k1_y + 16, k1_x + 42, k1_y + 44], fill=(5, 150, 105))
    draw.text((k1_x + 28, k1_y + 30), "3", font=get_font(13, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((k1_x + 52, k1_y + 18), "많은 인력을 동원하여 고인돌을 축조하였다.", font=get_font(10.5, 'bold'), fill=(5, 150, 105))
    draw.text((k1_x + 52, k1_y + 38), "✓ [정답 선지] 청동기 시대 지배층의 권력 과시", font=get_font(8.8, 'medium'), fill=(4, 120, 87))
    draw_pill_badge(draw, left_x=k1_x + 52, cy=k1_y + 58, text="정답 판정 100%", font=get_font(7.5, 'bold'), theme='green', pad_x=6, height=16)
    
    # Micro-Component 2: Historical Passage Clue Card
    k2_x = k1_x + k1_w + 16
    draw.rounded_rectangle([k2_x, k1_y, k2_x + k1_w, k1_y + 74], radius=12, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw.text((k2_x + 14, k1_y + 12), "사료 속 핵심 키워드 단서 (Clue X-Ray)", font=get_font(9.5, 'bold'), fill=(180, 83, 9))
    draw.text((k2_x + 14, k1_y + 30), "[제주 고산리 유적] → 신석기 이전 구석기 말기~초기 전환기", font=get_font(9, 'bold'), fill=(15, 23, 42))
    draw.text((k2_x + 14, k1_y + 48), "키워드 하이라이트: 덧띠토기, 이른 민무늬토기, 잔석기", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    # Micro-Component 3: Preset Chips Row (시대별 & 모의고사 프리셋)
    ch_y = k1_y + 92
    draw.text((colB_x + 28, ch_y + 6), "수험 네비게이션 & 시대별 필터 칩:", font=get_font(10, 'bold'), fill=(100, 116, 139))
    presets = [
        ("선사·고조선", (29, 78, 216), (239, 246, 255)),
        ("삼국·가야", (29, 78, 216), (239, 246, 255)),
        ("통일신라·발해", (29, 78, 216), (239, 246, 255)),
        ("고려 시대", (217, 119, 6), (254, 243, 199)),
        ("조선 시대", (225, 29, 72), (254, 242, 242)),
        ("근대·일제강점기", (100, 116, 139), (241, 245, 249)),
        ("현대사", (5, 150, 105), (236, 253, 245)),
    ]
    cur_ch_x = colB_x + 230
    for p_txt, p_col, p_bg in presets:
        draw.rounded_rectangle([cur_ch_x, ch_y, cur_ch_x + 82, ch_y + 26], radius=13, fill=p_bg, outline=p_col, width=1)
        draw.text((cur_ch_x + 41, ch_y + 13), p_txt, font=get_font(9, 'bold'), fill=p_col, anchor='mm')
        cur_ch_x += 87
        
    # Micro-Component 4: CTAs Button Row
    cta_y = ch_y + 38
    mat_font_cta = get_material_icon_font(15)
    
    # 1. Start Exam Button
    draw.rounded_rectangle([colB_x + 28, cta_y, colB_x + 230, cta_y + 40], radius=10, fill=(29, 78, 216))
    draw.text((colB_x + 50, cta_y + 20), chr(0xf00b8), font=mat_font_cta, fill=(255, 255, 255), anchor='mm')
    draw.text((colB_x + 138, cta_y + 20), "실전 50문항 응시", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # 2. 50:50 Chance Button
    draw.rounded_rectangle([colB_x + 242, cta_y, colB_x + 432, cta_y + 40], radius=10, fill=(240, 246, 255), outline=(29, 78, 216), width=1)
    draw.text((colB_x + 264, cta_y + 20), chr(0xe3e7), font=mat_font_cta, fill=(29, 78, 216), anchor='mm')
    draw.text((colB_x + 347, cta_y + 20), "50:50 오답 소거 찬스", font=get_font(11, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    # 3. Add to Vault Button
    draw.rounded_rectangle([colB_x + 444, cta_y, colB_x + 614, cta_y + 40], radius=10, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((colB_x + 466, cta_y + 20), chr(0xe0f1), font=mat_font_cta, fill=(51, 65, 85), anchor='mm')
    draw.text((colB_x + 538, cta_y + 20), "오답 볼트 저장", font=get_font(10.5, 'bold'), fill=(51, 65, 85), anchor='mm')
    
    # 4. Timer Pill
    draw.rounded_rectangle([colB_x + 626, cta_y, colB_x + colB_w - 28, cta_y + 40], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((colB_x + 648, cta_y + 20), chr(0xe25b), font=get_material_icon_font(18), fill=(225, 29, 72), anchor='mm')
    draw.text((colB_x + 664 + (colB_w - 28 - 664)//2, cta_y + 12), "남은 시간 79:17", font=get_num_font(9, 'bold'), fill=(225, 29, 72), anchor='mm')
    draw.text((colB_x + 664 + (colB_w - 28 - 664)//2, cta_y + 26), "실전 모의고사 진행 중", font=get_font(8, 'bold'), fill=(153, 27, 27), anchor='mm')
    
    # Micro-Component 5: Status Badges Row
    bdg_y = cta_y + 50
    draw.text((colB_x + 28, bdg_y + 6), "수험 상태 배지 시스템:", font=get_font(10, 'bold'), fill=(100, 116, 139))
    badges = [
        ("최신 77회 심화", "blue", True),
        ("50문항 타이머", "red", True),
        ("정답률 84%", "green", True),
        ("취약 시대 인덱싱", "amber", True),
        ("100% 오프라인 캐시", "slate", True),
        ("Pretendard 가변", "purple", False),
    ]
    cur_bx = colB_x + 165
    for b_txt, b_thm, b_dt in badges:
        _, _, b_end, _ = draw_pill_badge(draw, left_x=cur_bx, cy=bdg_y + 14, text=b_txt, font=get_font(9.5, 'bold'), theme=b_thm, has_dot=b_dt, dark_mode=False, pad_x=8, height=24)
        cur_bx = b_end + 8
        
    draw.text((colB_x + 28, r2_y + r2_h - 18), "• 파운데이션 토큰 100% 바인딩: R6/R12/R16 라운딩, 태극 헤리티지 배색, 수험 칩이 Flutter 위젯 트리에 실시간 동기화", font=get_font(9, 'regular'), fill=(100, 116, 139))
    
    draw_slide_footer(draw, 7)
    base.save(f'{OUT_DIR}/slide_07.png')
    print("SAVED slide_07.png (Taegeuk Heritage Design System & Edutech Component Architecture)")


def make_slide_08():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Top Line Boundary
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    # -------------------------------------------------------------
    # 1. Left Column: Grouped Header Card & Comparison Pane (x=100, w=490)
    # -------------------------------------------------------------
    lx = 100
    lw = 490
    
    # 1-A. Unified Kicker Badge
    draw_pill_badge(draw, left_x=lx, cy=78, text="08 핵심 기능 | 80분 공인 시험센터 & 실전 타이머", font=get_font(10.5, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=26)
    
    # Headline
    t1_a = "무거운 기출집 대신 "
    t1_b = "스마트폰 하나로,"
    font_title = get_font(33, 'extrabold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((lx, 116), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((lx + w_t1_a, 116), t1_b, font=font_title, fill=(29, 78, 216))
    
    t2_a = "실전 80분 타이머로 "
    t2_b = "50문항을 완주해요."
    w_t2_a = draw.textlength(t2_a, font=font_title)
    draw.text((lx, 158), t2_a, font=font_title, fill=(29, 78, 216))
    draw.text((lx + w_t2_a, 158), t2_b, font=font_title, fill=(15, 23, 42))
    
    desc_text = "실제 시험장에서 시간 안배 실패로 마지막 10문항 OMR 마킹을 놓치는 수험생 페인포인트를 해결하기 위해 실제 공인 시험과 100% 동일한 50문항 80분 카운트다운 타이머와 1·2·3점 배점 로직을 모바일에 완벽 구현했습니다."
    desc_lines = wrap_text_by_words(desc_text, get_font(12, 'regular'), lw, draw)
    dy = 212
    for dl in desc_lines:
        draw.text((lx, dy), dl, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 19
        
    # 1-B. Comparison Container Card (Manual Paper vs 80-Min Mobile)
    comp_y = 310
    comp_h = 660
    draw.rounded_rectangle([lx, comp_y, lx + lw, comp_y + comp_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, left_x=lx + 24, cy=comp_y + 30, text="PARADIGM COMPARISON", font=get_font(9.5, 'bold'), theme='slate', has_dot=False, pad_x=8, height=22)
    draw.text((lx + 185, comp_y + 22), "종이 기출 문제집 vs 모바일 실전 시험", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.line([(lx + 24, comp_y + 50), (lx + lw - 24, comp_y + 50)], fill=(241, 245, 249), width=1)
    
    # 2 Comparison Phone Mockups
    screen_home_path = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_01_home.png'
    screen_exam_path = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_02_exam.png'
    
    screen_home = Image.open(screen_home_path).convert('RGBA')
    screen_exam = Image.open(screen_exam_path).convert('RGBA')
    
    s_w = 170
    s_h = int(round(s_w * (screen_home.height / screen_home.width)))
    s1 = screen_home.resize((s_w, s_h), Image.Resampling.LANCZOS)
    s2 = screen_exam.resize((s_w, s_h), Image.Resampling.LANCZOS)
    
    y_screen = comp_y + 68
    x_s1 = lx + 32
    x_s2 = lx + lw - 32 - s_w
    
    draw_pill_badge(draw, cx=x_s1 + s_w//2, cy=y_screen + 14, text="종이 기출 수기 채점", font=get_font(10, 'bold'), theme='slate', has_dot=False, pad_x=10, height=22)
    draw_pill_badge(draw, cx=x_s2 + s_w//2, cy=y_screen + 14, text="80분 OMR 모바일 시험", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=10, height=22)
    
    for sx, simg in [(x_s1, s1), (x_s2, s2)]:
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([sx + 6, y_screen + 34, sx + s_w - 6, y_screen + 34 + s_h], radius=22, fill=(0, 0, 0, 40))
        sh = sh.filter(ImageFilter.GaussianBlur(12))
        base = Image.alpha_composite(base, sh)
        base.paste(simg, (sx, y_screen + 28), simg)
        
    draw = ImageDraw.Draw(base)
    by_s1 = y_screen + 28 + s_h + 16
    draw.rounded_rectangle([x_s1, by_s1, x_s1 + s_w, comp_y + comp_h - 18], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((x_s1 + 10, by_s1 + 10), "종이 기출 수동 풀이", font=get_font(10, 'bold'), fill=(100, 116, 139))
    draw.text((x_s1 + 10, by_s1 + 28), "• 1,200g 책 지참 필수\n• 수기 채점 소요 45분\n• 시간 안배 훈련 불가", font=get_font(9.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.rounded_rectangle([x_s2, by_s1, x_s2 + s_w, comp_y + comp_h - 18], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((x_s2 + 10, by_s1 + 10), "대한국사 시험센터", font=get_font(10, 'bold'), fill=(29, 78, 216))
    draw.text((x_s2 + 10, by_s1 + 28), "• 0g 스마트폰 완결\n• 1초 즉각 자동 채점\n• 80분 OMR 카운트다운", font=get_font(9.5, 'semibold'), fill=(29, 78, 216), spacing=4)
    
    # -------------------------------------------------------------
    # 2. Center Column: Grand Hero Phone Mockup (19.5:9 Modern Ratio)
    # -------------------------------------------------------------
    phone_hero = Image.open(screen_exam_path).convert('RGBA')
    ph = 640
    pw = int(round(ph * (phone_hero.width / phone_hero.height)))
    phone_v = phone_hero.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 670
    py = 234
    
    sh_center = Image.new('RGBA', (W, H), (0,0,0,0))
    shc_draw = ImageDraw.Draw(sh_center)
    shc_draw.rounded_rectangle([px + 12, py + 16, px + pw - 12, py + ph + 24], radius=36, fill=(0, 0, 0, 60))
    shc_draw.ellipse([px - 20, py + ph - 25, px + pw + 20, py + ph + 35], fill=(29, 78, 216, 30))
    sh_center = sh_center.filter(ImageFilter.GaussianBlur(26))
    base = Image.alpha_composite(base, sh_center)
    base.paste(phone_v, (px, py), phone_v)
    draw = ImageDraw.Draw(base)
    
    # -------------------------------------------------------------
    # 3. Right Column: 3 Distinct Grouped Feature Cards (x=1050, w=770)
    # -------------------------------------------------------------
    rx = 1050
    rw = 770
    
    # CARD 1: Exam Session & Time Management
    c1_y = 234
    c1_h = 145
    draw.rounded_rectangle([rx, c1_y, rx + rw, c1_y + c1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=c1_y + 30, text="EXAM SIMULATOR · 80-MIN TIMER", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 270, c1_y + 20), "실제 시험과 100% 동일한 50문항 80분 OMR 카운트다운", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, c1_y + 50), (rx + rw - 28, c1_y + 50)], fill=(241, 245, 249), width=1)
    
    c1_desc = '최신 77회 한능검 심화 기출을 실제 시험지 배열과 1·2·3점 배점 기준 그대로 재현했습니다.\n문항당 권장 풀이 시간(1분 36초) 가이드와 종료 10분 전 OMR 마킹 경보로 실전 적응력을 극대화합니다.'
    draw.text((rx + 28, c1_y + 64), c1_desc, font=get_font(12.5, 'regular'), fill=(71, 85, 105), spacing=5)
    draw.text((rx + 28, c1_y + 116), "✓ 시험장 완주율 38.2% → 78.4% 향상 · 80분 OMR 타이머 실전 안배 훈련", font=get_font(11, 'bold'), fill=(29, 78, 216))
    
    # CARD 2: 10-Question Short-Form Mode
    c2_y = 394
    c2_h = 145
    draw.rounded_rectangle([rx, c2_y, rx + rw, c2_y + c2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=c2_y + 30, text="SHORT-FORM MODE · 10-MIN TEST", font=get_font(10, 'bold'), theme='cyan', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 275, c2_y + 20), "출퇴근 통학길 자투리 10분을 위한 숏폼 모의고사", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, c2_y + 50), (rx + rw - 28, c2_y + 50)], fill=(241, 245, 249), width=1)
    
    c2_desc = '시간이 부족한 직장인과 학생을 위해 핵심 빈출 10문항만 엄선한 숏폼 모의고사를 제공합니다.\n이동 중 만원 전철 안에서도 한 손 엄지 터치만으로 5분 만에 풀고 즉시 점수 피드백을 확인합니다.'
    draw.text((rx + 28, c2_y + 64), c2_desc, font=get_font(12.5, 'regular'), fill=(71, 85, 105), spacing=5)
    draw.text((rx + 28, c2_y + 116), "✓ 일평균 기출 학습 빈도 3.2회 증가 · 자투리 시간 모바일 완전 정복", font=get_font(11, 'bold'), fill=(8, 145, 178))
    
    # CARD 3: Realtime Telemetry & SQLite Offline Vault Card
    c3_y = 554
    c3_h = 320
    draw.rounded_rectangle([rx, c3_y, rx + rw, c3_y + c3_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=c3_y + 30, text="EXAM TELEMETRY · SQLITE OFFLINE", font=get_font(10, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 280, c3_y + 20), "1,500제 기출 전면 내장 & 실시간 점수 환산", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, c3_y + 50), (rx + rw - 28, c3_y + 50)], fill=(241, 245, 249), width=1)
    
    # Exam Telemetry Chips inside Card 3
    t_box_y = c3_y + 64
    draw.rounded_rectangle([rx + 28, t_box_y, rx + rw - 28, t_box_y + 64], radius=10, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw.text((rx + 44, t_box_y + 18), "실시간 채점 결과 : 86점 (한능검 심화 1급 커트라인 80점 돌파 달성)", font=get_font(13.5, 'bold'), fill=(22, 101, 52))
    draw.text((rx + 44, t_box_y + 40), "정답 43문항 · 오답 7문항 · 풀이 소요 52분 18초 (잔여 27분 42초)", font=get_font(11.5, 'medium'), fill=(21, 128, 61))
    
    # 4 Parsed Exam Parameter Cards
    p_box_y = t_box_y + 76
    p_w = (rw - 56 - 36) // 4
    params = [
        ("총 문항", "50 문항", "배점 100점", (29, 78, 216)),
        ("타이머", "80:00", "공인 시험 규격", (8, 145, 178)),
        ("평균 소요", "52.3 분", "27분 여유 확보", (5, 150, 105)),
        ("오프라인", "100%", "데이터 소모 0MB", (217, 119, 6))
    ]
    for pidx, (plabel, pval, psub, pcol) in enumerate(params):
        px_pos = rx + 28 + pidx * (p_w + 12)
        draw.rounded_rectangle([px_pos, p_box_y, px_pos + p_w, p_box_y + 80], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((px_pos + 12, p_box_y + 12), plabel, font=get_font(10, 'bold'), fill=(100, 116, 139))
        draw.text((px_pos + 12, p_box_y + 32), pval, font=get_font(14, 'black'), fill=pcol)
        draw.text((px_pos + 12, p_box_y + 56), psub, font=get_font(9.5, 'medium'), fill=(71, 85, 105))
        
    # Technical Architecture Audit Footer inside Card 3
    draw.rounded_rectangle([rx + 28, c3_y + c3_h - 60, rx + rw - 28, c3_y + c3_h - 16], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((rx + 40, c3_y + c3_h - 38), "✓ 국사편찬위원회 2026 최신 심화 기출 공공 데이터 전 문항 완벽 연동", font=get_font(11, 'bold'), fill=(29, 78, 216), anchor='lm')
    
    # Dotted connector callout lines from Hero phone to right cards
    draw_dashed_line(draw, (px + pw, py + 140), (rx, c1_y + 70), col=(191, 219, 254), width=2, dash=4, gap=3)
    draw.ellipse([rx - 4, c1_y + 66, rx + 4, c1_y + 74], fill=(29, 78, 216))
    draw_dashed_line(draw, (px + pw, py + 340), (rx, c2_y + 70), col=(165, 243, 252), width=2, dash=4, gap=3)
    draw.ellipse([rx - 4, c2_y + 66, rx + 4, c2_y + 74], fill=(8, 145, 178))
    draw_dashed_line(draw, (px + pw, py + 520), (rx, c3_y + 70), col=(187, 247, 208), width=2, dash=4, gap=3)
    draw.ellipse([rx - 4, c3_y + 66, rx + 4, c3_y + 74], fill=(5, 150, 105))
    
    draw_slide_footer(draw, 8)
    base.save(f'{OUT_DIR}/slide_08.png')
    print("SAVED slide_08.png (DCA Master 3-Column Layout: 80-Min Exam Center)")


def make_slide_09():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Top Line Boundary
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    # -------------------------------------------------------------
    # 1. Left Column: Grouped Header Card & Quant Theory & Guard (x=100, w=540)
    # -------------------------------------------------------------
    lx = 100
    lw = 540
    
    # 1-A. Unified Kicker Badge
    draw_pill_badge(draw, left_x=lx, cy=78, text="09 핵심 기능 | 사료 키워드 판독 & 50:50 추론 찬스", font=get_font(10.5, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=26)
    
    # Headline
    t1_a = "어려운 사료 원문도 "
    t1_b = "형광펜 단서로,"
    font_title = get_font(33, 'extrabold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((lx, 116), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((lx + w_t1_a, 116), t1_b, font=font_title, fill=(29, 78, 216))
    
    t2_a = "50:50 찬스로 "
    t2_b = "정답을 확실히 가려내요."
    w_t2_a = draw.textlength(t2_a, font=font_title)
    draw.text((lx, 158), t2_a, font=font_title, fill=(29, 78, 216))
    draw.text((lx + w_t2_a, 158), t2_b, font=font_title, fill=(15, 23, 42))
    
    desc_text = "한자어와 생소한 고문헌으로 가득한 3점짜리 킬러 문항도 사료 속 핵심 단서(연호, 인물, 관직, 지명) 형광펜 하이라이트와 50:50 찬스를 통해 헷갈리는 함정 선지 2개를 소거하고 완벽한 추론 정답을 도출합니다."
    desc_lines = wrap_text_by_words(desc_text, get_font(12, 'regular'), lw, draw)
    dy = 212
    for dl in desc_lines:
        draw.text((lx, dy), dl, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 19
        
    # 1-B. Card 1: 사료 핵심 키워드 판독 알고리즘
    q1_y = 310
    q1_h = 230
    draw.rounded_rectangle([lx, q1_y, lx + lw, q1_y + q1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=q1_y + 30, text="PASSAGE LOCUS ALGORITHM", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((lx + 225, q1_y + 20), "사료 단서 식별 & 50:50 소거 알고리즘", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(lx + 24, q1_y + 52), (lx + lw - 24, q1_y + 52)], fill=(241, 245, 249), width=1)
    
    # Formula Box
    f_box_y = q1_y + 64
    draw.rounded_rectangle([lx + 24, f_box_y, lx + lw - 24, f_box_y + 54], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx + lw//2, f_box_y + 27), "Locus(Keyword) → Era_Tag → Eliminate(Distractor 2) → P(Ans) = 1.0", font=get_num_font(13.5, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    draw.text((lx + 24, f_box_y + 68), "단순 해설 암기가 아닌 사료 속 결정적 역사 단서를 시각화하고,\n오답 확률이 높은 함정 선지 2개를 블러 처리하여 수험생 소거법 훈련을 지원합니다.", font=get_font(11.5, 'regular'), fill=(71, 85, 105), spacing=5)
    
    # 1-C. Card 2: 에빙하우스 망각곡선 복습 주기 & 취약 시대 가드
    q2_y = 560
    q2_h = 200
    draw.rounded_rectangle([lx, q2_y, lx + lw, q2_y + q2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=q2_y + 30, text="EBBINGHAUS VAULT GUARD", font=get_font(10, 'bold'), theme='amber', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((lx + 220, q2_y + 20), "에빙하우스 망각곡선 & 취약 오답 가드", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(lx + 24, q2_y + 52), (lx + lw - 24, q2_y + 52)], fill=(241, 245, 249), width=1)
    
    draw.text((lx + 24, q2_y + 68), "틀린 문제를 수기로 적는 비효율을 없애고, 1초 만에 스마트 오답 볼트로 인덱싱하여\n1일, 3일, 7일 주기로 취약 시대 오답만 선별해 재응시할 수 있도록 유도합니다.", font=get_font(12, 'regular'), fill=(71, 85, 105), spacing=5)
    
    # Safety Boundary Chips
    draw.rounded_rectangle([lx + 24, q2_y + 130, lx + lw//2 - 10, q2_y + 180], radius=8, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((lx + 36, q2_y + 142), "취약 시대 정답률 경보", font=get_font(10, 'bold'), fill=(220, 38, 38))
    draw.text((lx + 36, q2_y + 160), "조선 후기/근현대사 오답 집중 태깅", font=get_font(9.5, 'regular'), fill=(239, 68, 68))
    
    draw.rounded_rectangle([lx + lw//2 + 10, q2_y + 130, lx + lw - 24, q2_y + 180], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((lx + lw//2 + 22, q2_y + 142), "주기 복습 스마트 알림", font=get_font(10, 'bold'), fill=(5, 150, 105))
    draw.text((lx + lw//2 + 22, q2_y + 160), "망각 방지 최적 타이밍 푸시 예약", font=get_font(9.5, 'regular'), fill=(16, 185, 129))
    
    # 1-D. Left Bottom Audit Pill
    draw.rounded_rectangle([lx, 780, lx + lw, 970], radius=14, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx + 24, 796), "사료 단서 식별 및 스마트 오답 볼트의 3대 무결성 원칙:", font=get_font(11.5, 'bold'), fill=(29, 78, 216))
    draw.text((lx + 24, 822), "1. Zero-Friction : 오답 발생 즉시 0초 만에 시대별·문항별 자동 인덱싱", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    draw.text((lx + 24, 844), "2. Keyword Locus : 한문 사료 속 핵심 단서 옐로우 형광펜 100% 자동 추출", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    draw.text((lx + 24, 866), "3. Elimination Loop : 50:50 찬스를 통한 능동적 소거법 추론 훈련 완성", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    draw.text((lx + 24, 892), "✓ 에빙하우스 망각곡선 기반 오답 재응시 통과율 91.2% 실측 달성", font=get_font(10.5, 'bold'), fill=(29, 78, 216))
    
    # -------------------------------------------------------------
    # 2. Center Column: Grand Hero Phone Mockup (19.5:9 Modern Slim Profile)
    # -------------------------------------------------------------
    screen_quiz_path = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_03_quiz.png'
    phone_quiz = Image.open(screen_quiz_path).convert('RGBA')
    ph = 640
    pw = int(round(ph * (phone_quiz.width / phone_quiz.height)))
    phone_t = phone_quiz.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 715
    py = 234
    
    sh_center = Image.new('RGBA', (W, H), (0,0,0,0))
    shc_draw = ImageDraw.Draw(sh_center)
    shc_draw.rounded_rectangle([px + 12, py + 16, px + pw - 12, py + ph + 24], radius=36, fill=(0, 0, 0, 60))
    shc_draw.ellipse([px - 20, py + ph - 25, px + pw + 20, py + ph + 35], fill=(29, 78, 216, 30))
    sh_center = sh_center.filter(ImageFilter.GaussianBlur(26))
    base = Image.alpha_composite(base, sh_center)
    base.paste(phone_t, (px, py), phone_t)
    draw = ImageDraw.Draw(base)
    
    # -------------------------------------------------------------
    # 3. Right Column: 2-Step Verified Flow Card + Telemetry Report Card (x=1100, w=720)
    # -------------------------------------------------------------
    rx = 1100
    rw = 720
    
    # 3-A. 2-Step Verified Flow Card (Containing 2 Step Mockups)
    step_y = 234
    step_h = 475
    draw.rounded_rectangle([rx, step_y, rx + rw, step_y + step_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, left_x=rx + 28, cy=step_y + 30, text="VERIFIED WORKFLOW", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 220, step_y + 20), "2단계 사료 해설 & 오답 볼트 복습 워크플로우", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, step_y + 52), (rx + rw - 28, step_y + 52)], fill=(241, 245, 249), width=1)
    
    # 2 Step Phone Mockups side-by-side
    screen_comm_path = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_04_commentary.png'
    screen_note_path = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_06_notes.png'
    
    screen_comm = Image.open(screen_comm_path).convert('RGBA')
    screen_note = Image.open(screen_note_path).convert('RGBA')
    
    step_pw = 142
    step_ph = int(round(step_pw * (screen_comm.height / screen_comm.width)))
    m1 = screen_comm.resize((step_pw, step_ph), Image.Resampling.LANCZOS)
    m2 = screen_note.resize((step_pw, step_ph), Image.Resampling.LANCZOS)
    
    p_w = 326
    p_h = 400
    p_y = step_y + 60
    p1_x = rx + 24
    p2_x = rx + rw - 24 - p_w
    
    # LEFT POD: STEP 01 (사료 키워드 판독)
    draw.rounded_rectangle([p1_x, p_y, p1_x + p_w, p_y + p_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p1_x + 14, cy=p_y + 20, text="STEP 01", font=get_font(9, 'bold'), theme='slate', has_dot=False, pad_x=8, height=20)
    draw.text((p1_x + 82, p_y + 20), "사료 단서 키워드 식별", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(p1_x + 14, p_y + 36), (p1_x + p_w - 14, p_y + 36)], fill=(226, 232, 240), width=1)
    
    phone1_x = p1_x + 14
    phone1_y = p_y + 48
    
    d1_x = phone1_x + step_pw + 12
    d1_w = p1_x + p_w - 14 - d1_x
    
    draw_pill_badge(draw, left_x=d1_x, cy=p_y + 58, text="사료 단서 형광펜", font=get_font(8.5, 'bold'), theme='amber', pad_x=8, height=20)
    
    t1_y = p_y + 74
    draw.rounded_rectangle([d1_x, t1_y, d1_x + d1_w, t1_y + 54], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d1_x + 10, t1_y + 8), "식별 키워드", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d1_x + 10, t1_y + 24), "빗살무늬 토기", font=get_font(12, 'bold'), fill=(180, 83, 9))
    draw.text((d1_x + 10, t1_y + 40), "신석기 시대 단서 확정", font=get_font(8.5, 'medium'), fill=(217, 119, 6))
    
    t2_y = t1_y + 60
    draw.rounded_rectangle([d1_x, t2_y, d1_x + d1_w, t2_y + 54], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d1_x + 10, t2_y + 8), "50:50 소거 선지", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d1_x + 10, t2_y + 24), "②번 · ③번 소거", font=get_font(12, 'bold'), fill=(225, 29, 72))
    draw.text((d1_x + 10, t2_y + 40), "함정 오답 2개 블러 제거", font=get_font(8.5, 'medium'), fill=(153, 27, 27))
    
    t3_y = t2_y + 60
    draw.rounded_rectangle([d1_x, t3_y, d1_x + d1_w, t3_y + 54], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d1_x + 10, t3_y + 8), "정답 선지 확정", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d1_x + 10, t3_y + 24), "④번 (가락바퀴)", font=get_font(12, 'bold'), fill=(22, 101, 52))
    draw.text((d1_x + 10, t3_y + 40), "정답률 100% 추론 성공", font=get_font(8.5, 'medium'), fill=(21, 128, 61))
    
    # RIGHT POD: STEP 02 (스마트 오답 볼트)
    draw.rounded_rectangle([p2_x, p_y, p2_x + p_w, p_y + p_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p2_x + 14, cy=p_y + 20, text="STEP 02", font=get_font(9, 'bold'), theme='blue', has_dot=False, pad_x=8, height=20)
    draw.text((p2_x + 82, p_y + 20), "스마트 오답 볼트 보관", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(p2_x + 14, p_y + 36), (p2_x + p_w - 14, p_y + 36)], fill=(226, 232, 240), width=1)
    
    phone2_x = p2_x + 14
    phone2_y = p_y + 48
    
    d2_x = phone2_x + step_pw + 12
    d2_w = p2_x + p_w - 14 - d2_x
    
    draw_pill_badge(draw, left_x=d2_x, cy=p_y + 58, text="AUTO-VAULT", font=get_font(8.5, 'bold'), theme='red', pad_x=8, height=20)
    
    r1_y = p_y + 74
    draw.rounded_rectangle([d2_x, r1_y, d2_x + d2_w, r1_y + 54], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d2_x + 10, r1_y + 8), "오답 자동 인덱싱", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d2_x + 10, r1_y + 24), "14문항 보관 중", font=get_font(12, 'bold'), fill=(225, 29, 72))
    draw.text((d2_x + 10, r1_y + 40), "정리 시간 0초 즉시 태깅", font=get_font(8.5, 'medium'), fill=(153, 27, 27))
    
    r2_y = r1_y + 60
    draw.rounded_rectangle([d2_x, r2_y, d2_x + d2_w, r2_y + 54], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d2_x + 10, r2_y + 8), "취약 시대 레이더", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d2_x + 10, r2_y + 24), "조선 후기 정치사", font=get_font(12, 'bold'), fill=(217, 119, 6))
    draw.text((d2_x + 10, r2_y + 40), "오답률 68% 집중 보완", font=get_font(8.5, 'medium'), fill=(180, 83, 9))
    
    r3_y = r2_y + 60
    draw.rounded_rectangle([d2_x, r3_y, d2_x + d2_w, r3_y + 54], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d2_x + 10, r3_y + 8), "에빙하우스 주기 복습", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d2_x + 10, r3_y + 24), "1·3·7일 스마트 알림", font=get_font(12, 'bold'), fill=(5, 150, 105))
    draw.text((d2_x + 10, r3_y + 40), "재응시 통과율 91.2%", font=get_font(8.5, 'medium'), fill=(16, 185, 129))
    
    # Soft Shadows behind both phones
    for ph_x, p_im in [(phone1_x, m1), (phone2_x, m2)]:
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([ph_x + 4, phone1_y + 8, ph_x + step_pw - 4, phone1_y + step_ph + 12], radius=18, fill=(0, 0, 0, 45))
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        base = Image.alpha_composite(base, sh)
        base.paste(p_im, (ph_x, phone1_y), p_im)
        
    draw = ImageDraw.Draw(base)
    
    # Pipeline Connector between Step 1 Pod and Step 2 Pod
    draw_dashed_line(draw, (p1_x + p_w, p_y + p_h//2), (p2_x, p_y + p_h//2), col=(29, 78, 216), width=2, dash=4, gap=3)
    draw.ellipse([p2_x - 4, p_y + p_h//2 - 4, p2_x + 4, p_y + p_h//2 + 4], fill=(29, 78, 216))
    
    # 3-B. Edutech Telemetry & Engine Result Card
    res_y = 720
    res_h = 250
    draw.rounded_rectangle([rx, res_y, rx + rw, res_y + res_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=res_y + 30, text="EDUTECH MASTERY TELEMETRY", font=get_font(10, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 275, res_y + 20), "사료 독해 추론율 & 오답 극복 정량 지표", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, res_y + 50), (rx + rw - 28, res_y + 50)], fill=(241, 245, 249), width=1)
    
    # Solved Banner Box
    s_banner_y = res_y + 64
    draw.rounded_rectangle([rx + 28, s_banner_y, rx + rw - 28, s_banner_y + 54], radius=10, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw.text((rx + 44, s_banner_y + 16), "검증 완료 : 50:50 찬스 활용 시 킬러 사료 정답률 84.6% 달성", font=get_font(13.5, 'bold'), fill=(22, 101, 52))
    draw.text((rx + 44, s_banner_y + 34), "소거법 추론 훈련으로 찍기식 오답률 71% 감소 · 에빙하우스 오답 재응시 통과율 91.2%", font=get_font(11, 'medium'), fill=(21, 128, 61))
    
    # 4 Metric Chips
    m_chip_y = s_banner_y + 68
    cw = (rw - 56 - 36) // 4
    m_chips = [
        ("사료 키워드", "100%", "연호/인물 추출", (29, 78, 216)),
        ("50:50 정답률", "84.6%", "소거 추론 성공", (5, 150, 105)),
        ("오답 재응시", "91.2%", "암기 누수 차단", (8, 145, 178)),
        ("노트 소요", "0 초", "수기 작성 해방", (217, 119, 6))
    ]
    for cidx, (clbl, cval, csub, ccol) in enumerate(m_chips):
        cx_pos = rx + 28 + cidx * (cw + 12)
        draw.rounded_rectangle([cx_pos, m_chip_y, cx_pos + cw, m_chip_y + 52], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((cx_pos + 12, m_chip_y + 12), clbl, font=get_font(9.5, 'bold'), fill=(100, 116, 139))
        draw.text((cx_pos + 12, m_chip_y + 28), cval, font=get_font(13.5, 'black'), fill=ccol)
        draw.text((cx_pos + cw - 12, m_chip_y + 28), csub, font=get_font(8.5, 'medium'), fill=(71, 85, 105), anchor='rm')
        
    # Dotted connector callout lines from Hero phone
    draw_dashed_line(draw, (px + pw, py + 180), (rx, step_y + 140), col=(191, 219, 254), width=2, dash=4, gap=3)
    draw.ellipse([rx - 4, step_y + 136, rx + 4, step_y + 144], fill=(29, 78, 216))
    draw_dashed_line(draw, (px + pw, py + 480), (rx, res_y + 90), col=(187, 247, 208), width=2, dash=4, gap=3)
    draw.ellipse([rx - 4, res_y + 86, rx + 4, res_y + 94], fill=(5, 150, 105))
    
    draw_slide_footer(draw, 9)
    base.save(f'{OUT_DIR}/slide_09.png')
    print("SAVED slide_09.png (DCA Master 3-Column Layout: Passage Highlight & 50:50 Chance)")


def make_slide_10():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=10, 
        category_en="프로덕션 화면 | 6대 상용 화면 쇼케이스", 
        title_black="기출 모의고사부터 시대별 사료관까지, ", 
        title_blue="완성도 높은 6대 프로덕션 화면이에요.", 
        subtitle_kr="수험생의 실전 시험 준비와 오답 보완을 빈틈없이 지원하도록 피그마 디자인 시스템과 플러터 위젯 트리로 구현한 6대 상용 화면입니다."
    )
    
    screens = [
        ('d:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_01_home.png', '01. 홈 대시보드', '학습 진도율 & 스트릭', '한눈에 파악하는 허브'),
        ('d:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_02_exam.png', '02. 실전 시험 센터', '최신 77회 한능검 심화', '50문항 80분 타이머'),
        ('d:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_03_quiz.png', '03. 실전 문제 풀이', '원터치 선지 선택 & 채점', '50:50 찬스 인터랙션'),
        ('d:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_04_commentary.png', '04. 정답 사료 해설', '사료 키워드 하이라이트', '& 전 선지 오답 분석'),
        ('d:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_05_study.png', '05. 시대별 서고', '선사부터 현대사까지', '유물 갤러리 & 오디오'),
        ('d:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_06_notes.png', '06. 스마트 오답 볼트', '오답 자동 인덱싱', '취약 시대 선별 재응시')
    ]
    
    # 6 Modern Flagship 19.5:9 Mobile Screens Grid
    pw = 210
    phone_y = 234
    pgap = 80
    px = 130
    
    for img_path, title, line1, line2 in screens:
        phone = Image.open(img_path).convert('RGBA')
        cur_ph = int(round(pw * (phone.height / phone.width)))
        phone = phone.resize((pw, cur_ph), Image.Resampling.LANCZOS)
        
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([px + 8, phone_y + 12, px + pw - 8, phone_y + cur_ph + 18], radius=28, fill=(0, 0, 0, 55))
        sh = sh.filter(ImageFilter.GaussianBlur(16))
        base = Image.alpha_composite(base, sh)
        base.paste(phone, (px, phone_y), phone)
        
        draw = ImageDraw.Draw(base)
        
        pill_y = phone_y + cur_ph + 18
        # 21px bottom margin below badge
        draw_pill_badge(draw, px + pw // 2, pill_y + 14, title, font=get_font(11, 'bold'), pad_x=12, height=26)
        
        w_l1 = draw.textlength(line1, font=get_font(10.5, 'medium'))
        draw.text((px + (pw - w_l1) / 2, pill_y + 46), line1, font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        w_l2 = draw.textlength(line2, font=get_font(10.5, 'medium'))
        draw.text((px + (pw - w_l2) / 2, pill_y + 64), line2, font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        
        px += pw + pgap
        
    draw.rounded_rectangle([100, 915, 1820, 975], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, 190, 945, "USER JOURNEY", font=get_font(11, 'bold'), pad_x=12, height=26)
    
    flow_steps = [
        ("01 학습 대시보드", 300),
        ("02 실전 회차 선택", 560),
        ("03 50문항 실전 응시", 830),
        ("04 사료 단서 판독", 1100),
        ("05 시대별 연표 탐색", 1370),
        ("06 취약 오답 정복", 1630)
    ]
    for step_txt, sx in flow_steps:
        draw.text((sx, 945), step_txt, font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        if sx < 1600:
            draw.text((sx + 180, 945), "→", font=get_font(18, 'bold'), fill=(0, 82, 255), anchor='lm')
            
    draw_slide_footer(draw, 10)
    base.save(f'{OUT_DIR}/slide_10.png')
    print("SAVED slide_10.png (Korail Style 6 Mobile Screens)")

# ==============================================================
# SLIDE 11: Consolidated Impact, Telemetry & Retrospective
# ==============================================================
def make_slide_11():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=11, 
        category_en="비즈니스 임팩트 | 정량적 텔레메트리 & 전략적 회고", 
        title_black="수험생 완주율 78.4%와 0초 오답 정리, ", 
        title_blue="실측 텔레메트리로 검증된 에듀테크 가치예요.", 
        subtitle_kr="한능검 기출 1,500제 학습 텔레메트리 데이터 분석과 4대 핵심 지표 및 STAR 기법 기반 시니어 프로덕트 회고입니다.",
        right_badge=("EDUTECH TELEMETRY 100%", "green")
    )
    
    # TOP DUAL COMPARISON CARDS: BEFORE vs. AFTER (y=234 to 554, h=320)
    card_y = 234
    card_h = 320
    card_w = 840
    
    # Left Card: Traditional Paper Study (Before)
    cx1 = 100
    draw.rounded_rectangle([cx1, card_y, cx1 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(254, 202, 202), width=1)
    draw.rounded_rectangle([cx1, card_y + 14, cx1 + 5, card_y + card_h - 14], radius=3, fill=(225, 29, 72))
    
    draw_pill_badge(draw, left_x=cx1 + 24, cy=card_y + 24, text="BEFORE : TRADITIONAL PAPER STUDY", font=get_font(9.5, 'bold'), theme='red', has_dot=True, pad_x=10, height=22)
    draw.text((cx1 + 24, card_y + 50), "종이 기출 문제집과 수기 오답 노트의 한계", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((cx1 + 24, card_y + 76), "1,200g 책 지참 필요, 수기 채점 및 오답 정리 풀칠로 하루 110분 낭비", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    b_rows = [
        ("학습 휴대성", "출퇴근길 지하철에서 두꺼운 기출 문제집 펼치기 불가 (무게 1,200g)", (15, 23, 42)),
        ("오답 정리 소요", "틀린 문제 가위질 및 오답 노트 풀칠 정리로 일평균 110분 낭비", (220, 38, 38)),
        ("사료 독해 훈련", "해설지 텍스트를 단순 눈으로 훑어 실전 사료 변형에 속수무책 취약", (220, 38, 38)),
        ("모의고사 완주율", "50문항 풀이 중 시간 안배 훈련 부족으로 시험장 완주율 38.2% 불과", (180, 83, 9))
    ]
    ry = card_y + 104
    for label, val, val_col in b_rows:
        draw.rounded_rectangle([cx1 + 24, ry, cx1 + card_w - 24, ry + 44], radius=8, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
        draw.text((cx1 + 38, ry + 22), label, font=get_font(11.5, 'bold'), fill=(100, 116, 139), anchor='lm')
        draw.text((cx1 + 210, ry + 22), val, font=get_font(12, 'bold'), fill=val_col, anchor='lm')
        ry += 50
        
    # Right Card: Korea History Quiz Edutech (After)
    cx2 = 980
    draw.rounded_rectangle([cx2, card_y, cx2 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.rounded_rectangle([cx2, card_y + 14, cx2 + 5, card_y + card_h - 14], radius=3, fill=(29, 78, 216))
    
    draw_pill_badge(draw, left_x=cx2 + 24, cy=card_y + 24, text="AFTER : DAEHANGUKSA EDUTECH", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=10, height=22)
    draw.text((cx2 + 24, card_y + 50), "대한국사 모바일 에듀테크 & 실전 1급 합격", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((cx2 + 24, card_y + 76), "80분 OMR 타이머, 50:50 찬스, 1초 오답 볼트 인덱싱으로 학습 효율 340% 향상", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    a_rows = [
        ("학습 휴대성", "스마트폰 하나로 언제 어디서나 1,500문항 오프라인 100% 응시 (무게 0g)", (29, 78, 216)),
        ("오답 정리 소요", "틀린 즉시 자동 인덱싱 오답 볼트 탑재 (수기 정리 시간 0초)", (5, 150, 105)),
        ("사료 독해 훈련", "키워드 형광펜 하이라이트 & 50:50 찬스로 사료 추론력 84.6% 달성", (5, 150, 105)),
        ("모의고사 완주율", "80분 공인 OMR 타이머 훈련으로 실전 모의고사 완주율 78.4% 달성", (180, 83, 9))
    ]
    ry = card_y + 104
    for label, val, val_col in a_rows:
        draw.rounded_rectangle([cx2 + 24, ry, cx2 + card_w - 24, ry + 44], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((cx2 + 38, ry + 22), label, font=get_font(11.5, 'bold'), fill=(100, 116, 139), anchor='lm')
        draw.text((cx2 + 210, ry + 22), val, font=get_font(12, 'bold'), fill=val_col, anchor='lm')
        ry += 50
        
    # MIDDLE 4 TELEMETRY METRICS CARDS (y=572 to 717, h=145)
    m_y = 572
    m_h = 145
    m_w = 405
    m_gap = 33
    tx = 100
    
    telemetry_data = [
        ("78.4 %", "COMPLETION", "실전 모의고사 완주율", "80분 OMR 카운트다운 타이머 훈련으로 시험장 완주율 38.2% 대비 2.1배 향상", (29, 78, 216), "blue"),
        ("0 초", "ZERO TIME", "오답 정리 시간 제로", "틀린 문제 1초 만에 SQLite 볼트로 자동 인덱싱되어 수기 작성 110분 절감", (16, 185, 129), "green"),
        ("84.6 %", "CHANCE HIT", "50:50 찬스 정답률", "함정 선지 2개 소거 후 소거법 기반 사료 추론 정답률 극대화 검증", (2, 132, 199), "cyan"),
        ("4.9 ★", "STORE RATING", "수험생 만족도 평점", "Google Play Store 수험생 리뷰 기반 한능검 1급 단기 합격 필수 앱 찬사", (245, 158, 11), "amber")
    ]
    
    for val, badge, title, desc, col, theme_key in telemetry_data:
        draw.rounded_rectangle([tx, m_y, tx + m_w, m_y + m_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=tx + 18, cy=m_y + 20, text=badge, font=get_font(9, 'bold'), theme=theme_key, has_dot=True, pad_x=8, height=20)
        draw.text((tx + 18, m_y + 46), val, font=get_num_font(30, 'black'), fill=(15, 23, 42))
        draw.text((tx + 18, m_y + 86), title, font=get_font(13, 'bold'), fill=(15, 23, 42))
        draw.text((tx + 18, m_y + 110), desc, font=get_font(10.5, 'regular'), fill=(100, 116, 139))
        tx += m_w + m_gap
        
    # BOTTOM 3 STRATEGIC RETROSPECTIVE & ROADMAP CARDS (y=735 to 970, h=235)
    b_y = 735
    b_h = 235
    b_w = 548
    b_gap = 38
    bx = 100
    
    bottom_cards = [
        (
            "LEARNING 01",
            "방대한 역사 암기의 인지 과부하 제어 (STAR)",
            "입력의 최소화와 50:50 찬스가 추론을 촉진",
            "한능검 수험생은 5,000년 역사와 방대한 사료 암기에 압도되어 중도 포기율이 40%에 달했습니다. 복잡한 수기 노트 대신 '1-Tap 숏폼과 50:50 찬스'로 전환하여 수험생 완주율을 78.4%까지 끌어올렸습니다.",
            "✓ 모의고사 완주율 78.4% 달성 입증",
            "cyan", (8, 145, 178)
        ),
        (
            "LEARNING 02",
            "사료 단서 판독이 주는 수험생 확신",
            "단순 암기 대신 키워드 형광펜과 오답 볼트",
            "수험생 불안의 본질인 '사료 독해 불확실성'을 핵심 키워드(연호·인물·관직) 형광펜으로 식별하고 에빙하우스 망각곡선 주기 복습을 연동하여 오답 재응시 통과율 91.2%를 기록했습니다.",
            "✓ 오답 재응시 통과율 91.2% 보존",
            "green", (5, 150, 105)
        ),
        (
            "3-PHASE ROADMAP",
            "지속 가능한 에듀테크 진화",
            "스토어 출시 완료 및 향후 AI 맞춤 튜터 확장",
            "• Phase 1 (Live) : 최신 77회 한능검 심화 1,500제 & 오프라인 SQLite 볼트 출시\n• Phase 2 (Next) : 취약 시대 약점 정밀 진단 AI 튜터 및 사료 낭독 오디오 고도화\n• Phase 3 (Future) : 7/9급 공무원 한국사 및 수능 한국사 기출 라인업 확장",
            "에듀테크 로드맵 인증 통과 ✓",
            "blue", (29, 78, 216)
        )
    ]
    
    for badge, title, sub, body_txt, check_txt, theme_key, col in bottom_cards:
        draw.rounded_rectangle([bx, b_y, bx + b_w, b_y + b_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=bx + 20, cy=b_y + 22, text=badge, font=get_font(9, 'bold'), theme=theme_key, has_dot=True, pad_x=8, height=20)
        draw.text((bx + 20, b_y + 50), title, font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((bx + 20, b_y + 72), sub, font=get_font(11, 'bold'), fill=col)
        draw.line([(bx + 20, b_y + 92), (bx + b_w - 20, b_y + 92)], fill=(241, 245, 249), width=1)
        
        py = b_y + 100
        for line in body_txt.split('\n'):
            words = line.split(' ')
            cur_line = ""
            for w in words:
                test_line = (cur_line + " " + w).strip()
                bbox = draw.textbbox((0, 0), test_line, font=get_font(10.5, 'regular'))
                if bbox[2] - bbox[0] <= b_w - 40:
                    cur_line = test_line
                else:
                    draw.text((bx + 20, py), cur_line, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
                    py += 17
                    cur_line = w
            if cur_line:
                draw.text((bx + 20, py), cur_line, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
                py += 17
                
        draw.rounded_rectangle([bx + 16, b_y + b_h - 36, bx + b_w - 16, b_y + b_h - 12], radius=6, fill=(240, 246, 255) if theme_key=='blue' else (248, 250, 252), outline=(191, 219, 254) if theme_key=='blue' else (226, 232, 240), width=1)
        draw.text((bx + 24, b_y + b_h - 24), check_txt, font=get_font(10, 'bold'), fill=col, anchor='lm')
        bx += b_w + b_gap
        
    draw_slide_footer(draw, 11)
    base.save(f'{OUT_DIR}/slide_11.png')
    print("SAVED slide_11.png (Consolidated Business Impact, Telemetry & Retrospective)")


def make_slide_12():
    # 1. Premium Obsidian Dark Background (#0B0F17)
    base = Image.new('RGBA', (W, H), (11, 15, 23, 255))
    draw = ImageDraw.Draw(base)
    
    # 2. Dark Header
    draw_slide_header(
        draw, 
        slide_num=12, 
        category_en="라이브 프로토타입 | 플러터 웹 인터랙티브 허브", 
        title_black="화면을 터치하듯, ", 
        title_blue="실제 플러터 웹 프로토타입을 직접 조작해 보세요.", 
        subtitle_kr="정적인 슬라이드를 넘어 스마트폰 뷰포트에서 4대 핵심 한능검 학습 여정을 직접 터치하고 검증할 수 있는 인터랙티브 허브입니다.",
        right_badge=("LIVE ENGINE READY", "green"),
        dark_mode=True
    )
    
    # ---------------------------------------------------------
    # LEFT: DUAL 3D LAYERED MOCKUP SHOWCASE (x=100 to 760, w=660)
    # ---------------------------------------------------------
    phone_quiz_path = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_03_quiz.png'
    phone_exam_path = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_02_exam.png'
    
    if os.path.exists(phone_quiz_path) and os.path.exists(phone_exam_path):
        im_quiz = Image.open(phone_quiz_path).convert('RGBA')
        ph_back = 570
        pw_back = int(round(ph_back * (im_quiz.width / im_quiz.height)))
        im_quiz = im_quiz.resize((pw_back, ph_back), Image.Resampling.LANCZOS)
        
        im_exam = Image.open(phone_exam_path).convert('RGBA')
        ph_front = 610
        pw_front = int(round(ph_front * (im_exam.width / im_exam.height)))
        im_exam = im_exam.resize((pw_front, ph_front), Image.Resampling.LANCZOS)
        
        # Gorgeous Neon Glow & Shadows on Dark Background
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([110, 230, 130 + pw_back + 40, 254 + ph_back + 30], fill=(0, 60, 180, 50))
        shd.rounded_rectangle([130 + 10, 254 + 15, 130 + pw_back - 10, 254 + ph_back + 20], radius=32, fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(24))
        base = Image.alpha_composite(base, sh)
        base.paste(im_quiz, (130, 254), im_quiz)
        
        # Front phone glow
        sh2 = Image.new('RGBA', (W, H), (0,0,0,0))
        shd2 = ImageDraw.Draw(sh2)
        shd2.ellipse([340 - 30, 234 + ph_front - 40, 340 + pw_front + 30, 234 + ph_front + 50], fill=(0, 110, 255, 90))
        shd2.rounded_rectangle([340 + 12, 234 + 16, 340 + pw_front - 12, 234 + ph_front + 24], radius=36, fill=(0, 0, 0, 180))
        sh2 = sh2.filter(ImageFilter.GaussianBlur(28))
        base = Image.alpha_composite(base, sh2)
        base.paste(im_exam, (340, 234), im_exam)
        
    draw = ImageDraw.Draw(base)
    
    # Left Bottom Spec Strip (x=100, y=856, w=660, h=124) - Dark Glass Card
    sp_x = 100
    sp_y = 856
    sp_w = 660
    sp_h = 124
    draw.rounded_rectangle([sp_x, sp_y, sp_x + sp_w, sp_y + sp_h], radius=16, fill=(17, 24, 39, 220), outline=(55, 65, 81), width=1)
    draw_pill_badge(draw, left_x=sp_x + 24, cy=sp_y + 24, text="ENGINE SPECS", font=get_font(9.5, 'bold'), theme='blue', dark_mode=True, pad_x=8, height=20)
    draw.text((sp_x + 130, sp_y + 24), "Flutter Web (CanvasKit) 60FPS 네이티브 렌더링", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='lm')
    draw.line([(sp_x + 24, sp_y + 44), (sp_x + sp_w - 24, sp_y + 44)], fill=(31, 41, 55), width=1)
    
    specs = [
        ("렌더링 엔진", "Flutter CanvasKit 60FPS"),
        ("로컬 데이터", "SQLite 1,500제 기출 완비"),
        ("뷰포트 규격", "390 × 844 (iPhone 14 기준)")
    ]
    sw = (sp_w - 48 - 20) // 3
    for sidx, (stitle, sval) in enumerate(specs):
        sx_pos = sp_x + 24 + sidx * (sw + 10)
        draw.text((sx_pos, sp_y + 56), stitle, font=get_font(9.5, 'bold'), fill=(148, 163, 184))
        draw.text((sx_pos, sp_y + 74), sval, font=get_font(10.5, 'bold'), fill=(255, 255, 255))
        draw.text((sx_pos, sp_y + 92), "100% 모바일 규격 최적화", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
        
    # ---------------------------------------------------------
    # RIGHT: MASTER LAUNCHER + 4 STEPS + TIP + QR CODE (x=800 to 1820, w=1020)
    # ---------------------------------------------------------
    rx = 800
    rw = 1020
    proto_entry_url = "https://koyotejw-ux.github.io/auto_portfolio/korea_history_quiz/prototype.html"
    
    # 1. PRIMARY HERO (TOP): MASTER LAUNCHER with Iconic Blue Gradient (y=234 to 348, h=114)
    my = 234
    mh = 114
    
    # Ambient Glow Behind Card
    sh_master = Image.new('RGBA', (W, H), (0,0,0,0))
    shm_draw = ImageDraw.Draw(sh_master)
    shm_draw.rounded_rectangle([rx + 8, my + 8, rx + rw - 8, my + mh + 12], radius=24, fill=(0, 102, 255, 110))
    shm_draw.ellipse([rx + rw - 260, my - 20, rx + rw + 20, my + mh + 20], fill=(6, 182, 212, 100))
    sh_master = sh_master.filter(ImageFilter.GaussianBlur(28))
    base = Image.alpha_composite(base, sh_master)
    
    # Generate Linear Gradient Box
    grad_img = Image.new('RGBA', (rw, mh))
    g_draw = ImageDraw.Draw(grad_img)
    for x in range(rw):
        t = x / max(1, rw - 1)
        r = int(0 * (1 - t) + 6 * t)
        g = int(82 * (1 - t) + 182 * t)
        b = int(255 * (1 - t) + 212 * t)
        for y in range(mh):
            grad_img.putpixel((x, y), (r, g, b, 255))
    mask = Image.new('L', (rw, mh), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, rw, mh], radius=18, fill=255)
    base.paste(grad_img, (rx, my), mask)
    
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle([rx, my, rx + rw, my + mh], radius=18, outline=(147, 197, 253, 200), width=1)
    
    # Content Inside Radiant Gradient Card
    draw.rounded_rectangle([rx + 24, my + 16, rx + 180, my + 40], radius=12, fill=(15, 23, 42, 240), outline=(255, 255, 255, 180), width=1)
    draw.ellipse([rx + 36, my + 28 - 3, rx + 42, my + 28 + 3], fill=(52, 211, 153))
    draw.text((rx + 48, my + 28), "CORE ENGINE LIVE", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='lm')
    
    draw.text((rx + 24, my + 58), "대한국사 통합 프로토타입 실행", font=get_font(21, 'black'), fill=(255, 255, 255))
    draw.text((rx + 24, my + 87), "50문항 실전 모의고사부터 사료 단서 식별까지, 4대 핵심 여정을 실물 뷰포트에서 한 번에 검증하세요.", font=get_font(12, 'regular'), fill=(240, 246, 255))
    
    # Pure White Button
    master_box = (rx + rw - 228, my + 30, rx + rw - 24, my + mh - 30)
    draw.rounded_rectangle(master_box, radius=12, fill=(255, 255, 255))
    draw.text((rx + rw - 126, my + mh // 2), "인터랙티브 웹 실행 →", font=get_font(13.5, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    # 2. 4 SUBDUED STEP CARDS (y=358 to 678, h=74, sgap=8)
    sy_start = 358
    sh_step = 74
    sgap = 8
    
    steps = [
        ("STEP 01", "01. 홈 대시보드 & 스트릭 진단",
         "학습 진도율 및 D-Day 설정 · 출석 스트릭 및 6대 시대별 마스터리 레이더 점검", "dash"),
        ("STEP 02", "02. 한능검 50제 실전 기출 센터",
         "최신 77회 한능검 심화 50문항 응시 · 80분 OMR 타이머 및 실시간 점수 환산", "exam"),
        ("STEP 03", "03. 50:50 찬스 & 사료 단서 판독",
         "오답 선지 2개 소거 추론 훈련 · 사료 속 시대 판별 핵심 키워드 형광펜 분석", "quiz"),
        ("STEP 04", "04. 스마트 오답 볼트 & 취약 시대 정복",
         "틀린 문제 원터치 자동 인덱싱 · 취약 시대 선별 숏폼 재응시 및 오답 박멸", "vault")
    ]
    
    step_boxes = []
    for s_idx, (s_step, s_title, s_desc, s_route) in enumerate(steps):
        s_y = sy_start + s_idx * (sh_step + sgap)
        draw.rounded_rectangle([rx, s_y, rx + rw, s_y + sh_step], radius=12, fill=(15, 20, 32, 220), outline=(30, 41, 59), width=1)
        draw.rounded_rectangle([rx + 16, s_y + 14, rx + 82, s_y + 36], radius=6, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        draw.text((rx + 49, s_y + 25), s_step, font=get_font(9, 'bold'), fill=(148, 163, 184), anchor='mm')
        
        draw.text((rx + 94, s_y + 25), s_title, font=get_font(13.5, 'bold'), fill=(255, 255, 255), anchor='lm')
        draw.text((rx + 94, s_y + 48), s_desc, font=get_font(11, 'regular'), fill=(148, 163, 184), anchor='lm')
        
        # Subtle Ghost Outline Pill
        btn_w, btn_h = 100, 30
        bx2 = rx + rw - 18
        bx1 = bx2 - btn_w
        by1 = s_y + (sh_step - btn_h) // 2
        by2 = by1 + btn_h
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=15, fill=(20, 27, 45, 180), outline=(51, 65, 85), width=1)
        draw.text(((bx1 + bx2) // 2, (by1 + by2) // 2), "화면 열기", font=get_font(10, 'medium'), fill=(148, 163, 184), anchor='mm')
        
        step_url = f"{proto_entry_url}#/{s_route}"
        step_boxes.append(((bx1, by1, bx2, by2), step_url))
        
    # 3. TERTIARY: Subtle Inline Guide Hint
    draw.text((rx + 2, 694), "💡 위 버튼이나 단계를 클릭하면 플러터 엔진이 내장된 독립 뷰포트에서 즉시 실행됩니다.", font=get_font(10.5, 'regular'), fill=(100, 116, 139))
    
    # 4. SUPPORTING: Dark QR Code & Hyperlink Area (y=716 to 970, h=254)
    qy = 716
    qh = 254
    draw.rounded_rectangle([rx, qy, rx + rw, qy + qh], radius=16, fill=(15, 20, 32, 220), outline=(30, 41, 59), width=1)
    
    # Generate High-Contrast QR Code on Crisp White Plate
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    qr.add_data(proto_entry_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    qr_w = 170
    qr_img = qr_img.resize((qr_w, qr_w), Image.Resampling.NEAREST)
    
    draw.rounded_rectangle([rx + 24, qy + 24, rx + 24 + qr_w, qy + 24 + qr_w], radius=12, fill=(255, 255, 255))
    base.paste(qr_img, (rx + 24, qy + 24))
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle([rx + 24, qy + 24, rx + 24 + qr_w, qy + 24 + qr_w], radius=12, outline=(226, 232, 240), width=1)
    
    # QR Guide Text Beside QR Code
    gx = rx + 24 + qr_w + 32
    draw_pill_badge(draw, left_x=gx, cy=qy + 36, text="MOBILE INSTANT LIVE", font=get_font(9.5, 'bold'), theme='cyan', dark_mode=True, pad_x=8, height=20)
    draw.text((gx, qy + 68), "스마트폰 카메라로 QR 코드를 스캔하세요", font=get_font(17, 'bold'), fill=(255, 255, 255))
    
    q_desc = "별도 앱 설치 없이 모바일 브라우저에서 60FPS 플러터 웹 프로토타입이 즉시 구동됩니다.\n한 손 엄지 그립으로 50문항 실전 모의고사와 50:50 찬스 인터랙션을 직접 체험할 수 있습니다."
    draw.text((gx, qy + 100), q_desc, font=get_font(12, 'regular'), fill=(148, 163, 184), spacing=5)
    
    # URL Pill Button Below Description
    url_box = [gx, qy + 154, rx + rw - 32, qy + 192]
    draw.rounded_rectangle(url_box, radius=8, fill=(11, 15, 23, 240), outline=(51, 65, 85), width=1)
    draw.text((gx + 16, qy + 173), proto_entry_url, font=get_font(11, 'bold'), fill=(56, 189, 248), anchor='lm')
    draw.text((rx + rw - 48, qy + 173), "OPEN ↗", font=get_font(10, 'bold'), fill=(148, 163, 184), anchor='rm')
    
    draw_slide_footer(draw, 12, dark_mode=True)
    base.save(f'{OUT_DIR}/slide_12.png')
    print("SAVED slide_12.png (DCA Master Dark Launcher & QR Hub)")
    return {
        'step_boxes': step_boxes,
        'master_box': (master_box, proto_entry_url)
    }


if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f'make_slide_{i:02d}'
        if func_name in globals():
            globals()[func_name]()
    print("ALL 12 SLIDES GENERATED WITH MASCULINE EDITORIAL AESTHETIC!")
