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
    draw.text((270, 1018), "·   Behance Enterprise Case Study  ·  Quant Inversion Engine", font=get_font(11, 'medium'), fill=meta_col)
    draw.text((960, 1018), "Flutter 3.38+ Mobile & Web  ·  Closed-Form Math  ·  Google Play Live", font=get_font(10.5, 'medium'), fill=meta_col, anchor='mt')
    
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
    draw_pill_badge(draw, left_x=100, cy=76, text="2026 CASE STUDY", font=get_font(11.5, 'bold'), theme='blue', has_dot=True, pad_x=12, height=28)
    
    meta_txt = "기획(PM) · UI/UX 디자인 · Android Live (v2.0) · Web Prototype"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=(100, 116, 139))
    
    # Category Label
    draw.text((100, 146), "KOREA HISTORY QUIZ · EDUTECH UX/UI", font=get_font(14, 'bold'), fill=(0, 82, 255))
    
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
        category_en="USER RESEARCH | DESK RESEARCH & 수험생 학습 행태 분석", 
        title_black="한능검·공무원 수험생의 학습 병목과 ", 
        title_blue="휘발성 암기 극복을 위한 3대 전략", 
        subtitle_kr="수험생 520명 심층 인터뷰 및 에빙하우스 망각곡선 기반 3대 학습 솔루션 도출"
    )
    
    # ==============================================================
    # 1. TOP: 3 Horizontal Market Trend Cards (Donut, H-Bar, V-Bar)
    # ==============================================================
    card_w = 546
    card_h = 224
    gap = 40
    sy = 234
    
    # --------------------------------------------------------------
    # CARD 1: MARKET TREND (Large Donut Chart - 84.2%)
    # --------------------------------------------------------------
    c1_x = 100
    draw.rounded_rectangle([c1_x, sy, c1_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c1_x, sy + 18, c1_x + 5, sy + card_h - 18], radius=2, fill=(220, 38, 38))
    
    # Left Typography Stack (21px bottom margin below badge)
    draw_pill_badge(draw, left_x=c1_x + 24, cy=sy + 26, text="MARKET TREND", font=get_font(10, 'bold'), theme='red', has_dot=False, pad_x=8, height=22)
    draw.text((c1_x + 24, sy + 58), "에빙하우스 망각곡선과 휘발성 암기", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c1_x + 24, sy + 88), "개인 투자자 10명 중 8명 이상이 출구 전략 없이\n감에 의존해 추가 매수를 감행하다 손실을 키웁니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c1_x + 24, sy + 144), "84.2%", font=get_num_font(38, 'black'), fill=(220, 38, 38))
    draw.text((c1_x + 24, sy + 188), "망각 호소율 (수험생 520명 설문)", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    # Right: Large Anti-Aliased Donut Chart (Radius 56 / 38)
    cx_donut = c1_x + card_w - 95
    cy_donut = sy + 116
    draw_donut_chart_on_base(base, cx_donut, cy_donut, r_outer=56, r_inner=38, percentage=82.6, col_fill=(220, 38, 38), col_track=(254, 226, 226))
    draw = ImageDraw.Draw(base)
    
    # Top Tag above Donut
    draw_pill_badge(draw, cx=cx_donut, cy=sy + 32, text="N=428 실태조사", font=get_font(9, 'bold'), theme='red', has_dot=False, pad_x=8, height=20)
    
    # Center text inside Donut hole (Mathematically centered)
    d_num = "83%"
    b_dnum = draw.textbbox((0, 0), d_num, font=get_num_font(18, 'black'))
    w_dnum = b_dnum[2] - b_dnum[0]
    h_dnum = b_dnum[3] - b_dnum[1]
    d_sub = "응답률"
    b_dsub = draw.textbbox((0, 0), d_sub, font=get_font(9.5, 'bold'))
    w_dsub = b_dsub[2] - b_dsub[0]
    h_dsub = b_dsub[3] - b_dsub[1]
    
    d_tot_h = h_dnum + 4 + h_dsub
    d_top = cy_donut - d_tot_h / 2.0
    draw.text((cx_donut - (b_dnum[0] + b_dnum[2]) / 2.0, d_top - b_dnum[1]), d_num, font=get_num_font(18, 'black'), fill=(220, 38, 38))
    draw.text((cx_donut - (b_dsub[0] + b_dsub[2]) / 2.0, d_top + h_dnum + 4 - b_dsub[1]), d_sub, font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    
    # --------------------------------------------------------------
    # CARD 2: BEHAVIOR TREND (Large Horizontal Bar Chart)
    # --------------------------------------------------------------
    c2_x = c1_x + card_w + gap
    draw.rounded_rectangle([c2_x, sy, c2_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c2_x, sy + 18, c2_x + 5, sy + card_h - 18], radius=2, fill=(217, 119, 6))
    
    # Left Typography Stack (21px bottom margin below badge)
    draw_pill_badge(draw, left_x=c2_x + 24, cy=sy + 26, text="BEHAVIOR TREND", font=get_font(10, 'bold'), theme='amber', has_dot=False, pad_x=8, height=22)
    draw.text((c2_x + 24, sy + 58), "두꺼운 기출 문제집의 물리적 한계", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c2_x + 24, sy + 88), "두꺼운 문제집을 수기로 채점하고 오답 노트를 일일이 풀칠하느라\n2시간 넘게 낭비되고 정작 실전 사료 독해 훈련을 놓칩니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c2_x + 24, sy + 144), "1,200g → 0g", font=get_num_font(30, 'black'), fill=(217, 119, 6))
    draw.text((c2_x + 24, sy + 188), "무게 100% 모바일 경량화 (출퇴근/통학 학습)", font=get_font(11, 'bold'), fill=(16, 185, 129))
    
    # Right: Large Horizontal Bar Chart
    bx = c2_x + card_w - 170
    b_w = 145
    draw_pill_badge(draw, cx=bx + b_w // 2, cy=sy + 32, text="소요 시간 비교", font=get_font(9, 'bold'), theme='amber', has_dot=False, pad_x=8, height=20)
    
    # Bar 1: 기존 수동 키패드 (240초)
    draw.text((bx, sy + 57), "기존 수동 키패드", font=get_font(10, 'bold'), fill=(148, 163, 184))
    w_240s = draw.textlength("240s", font=get_num_font(11.5, 'bold'))
    draw.text((bx + b_w - w_240s, sy + 57), "240s", font=get_num_font(11.5, 'bold'), fill=(220, 38, 38))
    draw.rounded_rectangle([bx, sy + 75, bx + b_w, sy + 75 + 16], radius=8, fill=(254, 226, 226))
    draw.rounded_rectangle([bx, sy + 75, bx + b_w, sy + 75 + 16], radius=8, fill=(248, 113, 113))
    
    # Bar 2: 스마트 음성 도크 (4.2초)
    draw.text((bx, sy + 101), "스마트 음성 도크", font=get_font(10, 'bold'), fill=(0, 82, 255))
    w_4s = draw.textlength("4.2s", font=get_num_font(11.5, 'bold'))
    draw.text((bx + b_w - w_4s, sy + 101), "4.2s", font=get_num_font(11.5, 'bold'), fill=(16, 185, 129))
    draw.rounded_rectangle([bx, sy + 119, bx + b_w, sy + 119 + 16], radius=8, fill=(241, 245, 249))
    draw.rounded_rectangle([bx, sy + 119, bx + 18, sy + 119 + 16], radius=8, fill=(16, 185, 129))
    
    # Speed Reduction Callout Badge (No missing glyphs)
    draw_pill_badge(draw, cx=bx + b_w // 2, cy=sy + 166, text="57배 고속 · 98% 단축", font=get_font(9.5, 'bold'), theme='green', has_dot=False, pad_x=10, height=24, solid=True)
    
    # --------------------------------------------------------------
    # CARD 3: INDUSTRY GAP (Large Vertical Bar / Column Chart)
    # --------------------------------------------------------------
    c3_x = c2_x + card_w + gap
    draw.rounded_rectangle([c3_x, sy, c3_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c3_x, sy + 18, c3_x + 5, sy + card_h - 18], radius=2, fill=(0, 82, 255))
    
    # Left Typography Stack (21px bottom margin below badge)
    draw_pill_badge(draw, left_x=c3_x + 24, cy=sy + 26, text="INDUSTRY GAP", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=22)
    draw.text((c3_x + 24, sy + 58), "증권사 MTS의 역산 기능 부재", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c3_x + 24, sy + 88), "국내 모든 MTS는 사후 가중평균만 보여줄 뿐,\n'탈출하려면 정확히 몇 주를 사야 하는가'에 답하지 못함.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c3_x + 24, sy + 144), "0 / 14개", font=get_num_font(38, 'black'), fill=(0, 82, 255))
    draw.text((c3_x + 24, sy + 188), "국내 14대 증권사 전수조사 (역산 0%)", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    # Right: Large Vertical Bar / Column Chart
    draw_pill_badge(draw, cx=c3_x + card_w - 90, cy=sy + 32, text="역산 지원율", font=get_font(9, 'bold'), theme='blue', has_dot=False, pad_x=8, height=20)
    
    base_v_y = sy + 160
    col_h = 74
    draw.line([(c3_x + card_w - 165, base_v_y), (c3_x + card_w - 20, base_v_y)], fill=(226, 232, 240), width=1)
    draw_dashed_line(draw, (c3_x + card_w - 160, base_v_y - col_h // 2), (c3_x + card_w - 25, base_v_y - col_h // 2), col=(241, 245, 249), width=1, dash_len=3, gap_len=3)
    
    # Column 1: 14대 증권사 MTS (0%) - Empty container track with red bottom indicator
    col1_x = c3_x + card_w - 124
    draw.rounded_rectangle([col1_x - 22, base_v_y - col_h, col1_x + 22, base_v_y], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([col1_x - 22, base_v_y - 8, col1_x + 22, base_v_y], radius=3, fill=(254, 202, 202), outline=(239, 68, 68), width=1)
    w_0pct = draw.textlength("0%", font=get_num_font(13.5, 'bold'))
    draw.text((col1_x - w_0pct / 2.0, base_v_y - col_h - 20), "0%", font=get_num_font(13.5, 'bold'), fill=(220, 38, 38))
    w_mts = draw.textlength("14대 MTS", font=get_font(10.5, 'bold'))
    draw.text((col1_x - w_mts / 2.0, base_v_y + 8), "14대 MTS", font=get_font(10.5, 'bold'), fill=(148, 163, 184))
    
    # Column 2: 대한국사 (100%) - Full solid container column
    col2_x = c3_x + card_w - 56
    draw.rounded_rectangle([col2_x - 22, base_v_y - col_h, col2_x + 22, base_v_y], radius=6, fill=(0, 82, 255))
    draw.rounded_rectangle([col2_x - 20, base_v_y - col_h + 2, col2_x + 20, base_v_y - col_h + 8], radius=3, fill=(96, 165, 250))
    w_100pct = draw.textlength("100%", font=get_num_font(13.5, 'black'))
    draw.text((col2_x - w_100pct / 2.0, base_v_y - col_h - 20), "100%", font=get_num_font(13.5, 'black'), fill=(0, 82, 255))
    w_dca = draw.textlength("대한국사", font=get_font(10.5, 'bold'))
    draw.text((col2_x - w_dca / 2.0, base_v_y + 8), "대한국사", font=get_font(10.5, 'bold'), fill=(0, 82, 255))
        
    # ==============================================================
    # 2. MIDDLE: INSIGHT CONNECTING BANNER WITH DOWN ARROW (Image 1 Style)
    # ==============================================================
    ins_y = 465
    draw.rounded_rectangle([100, ins_y, 1820, ins_y + 54], radius=12, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=120, cy=ins_y + 27, text="CORE INSIGHT", font=get_font(11, 'bold'), theme='blue', has_dot=True, pad_x=12, height=30)
    
    ins_text = "단순 수치 계산기가 아닌, '확실한 탈출 목표량 역산'과 '0.2초 음성 도크'를 결합한 전략적 퀀트 솔루션이 필요하다."
    draw.text((280, ins_y + 17), ins_text, font=get_font(14.5, 'bold'), fill=(0, 82, 255))
    
    # Down Arrow Indicator
    draw.polygon([(960, ins_y + 54), (952, ins_y + 64), (968, ins_y + 64)], fill=(0, 82, 255))
    
    # ==============================================================
    # 3. BOTTOM: 2x2 SWOT MATRIX (Left) + 3 STRATEGIC OUTCOMES (Right)
    # ==============================================================
    b_y = 550
    
    # Left: 2x2 SWOT Matrix (Reference Image 1 Style)
    swot_w = 830
    swot_h = 415
    draw.rounded_rectangle([100, b_y, 100 + swot_w, b_y + swot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((125, b_y + 20), "SWOT ANALYSIS : 대한국사 에듀테크 플랫폼의 전략적 포지셔닝", font=get_font(15, 'bold'), fill=(15, 23, 42))
    draw.line([(125, b_y + 48), (100 + swot_w - 25, b_y + 48)], fill=(241, 245, 249), width=1)
    
    qw = (swot_w - 60) // 2
    qh = 158
    
    # S (Strength)
    s_x = 125
    s_y = b_y + 65
    draw.rounded_rectangle([s_x, s_y, s_x + qw, s_y + qh], radius=10, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw_pill_badge(draw, left_x=s_x + 14, cy=s_y + 22, text="Strength (강점)", font=get_font(10, 'bold'), theme='green', has_dot=False, pad_x=10, height=24, solid=True)
    s_points = [
        "• 0.2초 음성 도크로 타이핑 제로화",
        "• 닫힌 형식 퀀트 방정식 즉시 역산",
        "• 100% 온디바이스 개인정보 보호"
    ]
    dy = s_y + 56
    for p in s_points:
        draw.text((s_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(6, 95, 70))
        dy += 24
        
    # W (Weakness)
    w_x = s_x + qw + 10
    w_y = s_y
    draw.rounded_rectangle([w_x, w_y, w_x + qw, w_y + qh], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=w_x + 14, cy=w_y + 22, text="Weakness (약점)", font=get_font(10, 'bold'), theme='red', has_dot=False, pad_x=10, height=24, solid=True)
    w_points = [
        "• 초기 개인 개발자 브랜드 인지도",
        "• 증권사 계좌 API 실시간 직접 연동 부재",
        "• 방대한 5,000년 역사 데이터 초벌 학습 필요"
    ]
    dy = w_y + 56
    for p in w_points:
        draw.text((w_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(153, 27, 27))
        dy += 24
        
    # O (Opportunity)
    o_x = s_x
    o_y = s_y + qh + 10
    draw.rounded_rectangle([o_x, o_y, o_x + qw, o_y + qh], radius=10, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=o_x + 14, cy=o_y + 22, text="Opportunity (기회)", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=10, height=24, solid=True)
    o_points = [
        "• 한능검·공무원 수험생 모바일 학습 수요 88.4%",
        "• 복잡한 수식 없는 직관적 모바일 도구 요구",
        "• 1인 가구 및 주린이 투자자의 리스크 관리 니즈"
    ]
    dy = o_y + 56
    for p in o_points:
        draw.text((o_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(30, 64, 175))
        dy += 24
        
    # T (Threat)
    t_x = w_x
    t_y = o_y
    draw.rounded_rectangle([t_x, t_y, t_x + qw, t_y + qh], radius=10, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw_pill_badge(draw, left_x=t_x + 14, cy=t_y + 22, text="Threat (위협)", font=get_font(10, 'bold'), theme='amber', has_dot=False, pad_x=10, height=24, solid=True)
    t_points = [
        "• 대형 증권사의 유사 퀀트 기능 복제",
        "• 급격한 하락장 장기화로 투자 심리 위축",
        "• 타사 금융 앱의 무료 광고 공세"
    ]
    dy = t_y + 56
    for p in t_points:
        draw.text((t_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(146, 64, 14))
        dy += 24
        
    # Right: 3 Strategic Outcome Cards (Reference Image 1 Style)
    strat_x = 100 + swot_w + 30
    strat_w = 860
    strat_h = 415
    draw.rounded_rectangle([strat_x, b_y, strat_x + strat_w, b_y + strat_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((strat_x + 25, b_y + 20), "STRATEGIC OUTCOMES : 도출된 3대 제품 혁신 전략", font=get_font(15, 'bold'), fill=(15, 23, 42))
    draw.line([(strat_x + 25, b_y + 48), (strat_x + strat_w - 25, b_y + 48)], fill=(241, 245, 249), width=1)
    
    outcomes = [
        ("01", "기출 1,500제 완벽 분석 및 오답 자동 인덱싱",
         "AS-IS : 두꺼운 문제집 들고 다니며 오답 체크에 2시간 이상 낭비되는 비효율",
         "TO-BE : 틀린 문제 1초 만에 오답 볼트로 인덱싱 & 취약 시대 타겟 숏폼 복습",
         "blue"),
        ("02", "사료 판독 키워드 하이라이트 & 50:50 찬스",
         "AS-IS : 급락 순간 키보드로 가격을 치다 지지선을 놓치고 -6.4% 추가 손실",
         "TO-BE : 0.2초 음성 도크 & ±5% 원터치 프리셋 칩으로 4.2초 만에 파라미터 세팅",
         "cyan"),
        ("03", "시대별 마스터리 레이더 & 실전 80분 시험장 시뮬레이션",
         "AS-IS : 원금 회복을 위해 몇 주를 사야 하는지 계산할 수 없어 맹목적 매수",
         "TO-BE : 폐쇄형(Closed-Form) 퀀트 역산 엔진으로 목표 탈출가 도달 수량 0ms 즉각 산출",
         "green")
    ]
    
    sy_out = b_y + 65
    for num, o_title, o_asis, o_tobe, o_theme in outcomes:
        draw.rounded_rectangle([strat_x + 25, sy_out, strat_x + strat_w - 25, sy_out + 102], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        # Number Badge & Aligned Title
        draw.rounded_rectangle([strat_x + 40, sy_out + 14, strat_x + 68, sy_out + 38], radius=6, fill=(15, 23, 42))
        draw.text((strat_x + 54, sy_out + 26), num, font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((strat_x + 78, sy_out + 26), o_title, font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
        
        # As-is line
        draw.text((strat_x + 40, sy_out + 46), o_asis, font=get_font(11.5, 'regular'), fill=(220, 38, 38))
        # To-be line
        draw.text((strat_x + 40, sy_out + 70), o_tobe, font=get_font(11.5, 'bold'), fill=(0, 82, 255))
        
        sy_out += 114
        
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
        category_en="TARGET & PERSONA | SEGMENTATION MATRIX & BENCHMARK", 
        title_black="타깃 세그먼트 매트릭스와 ", 
        title_blue="경쟁사 벤치마킹 분석", 
        subtitle_kr="2x2 타깃 포지셔닝 매트릭스와 4대 플랫폼 벤치마크, 그리고 대표 페르소나 행동 지표"
    )
    
    # ==============================================================
    # 1. TOP-LEFT: 2x2 Target Segmentation Matrix (Reference Image 2 Style)
    # ==============================================================
    t_x = 100
    t_y = 234
    t_w = 780
    t_h = 378
    draw.rounded_rectangle([t_x, t_y, t_x + t_w, t_y + t_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((t_x + 24, t_y + 18), "TARGET SEGMENTATION MATRIX (타깃 세그먼트 분석)", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((t_x + 24, t_y + 38), "매매 빈도와 퀀트 도구 수용도에 따른 4대 투자자 유형 분류", font=get_font(11.5, 'medium'), fill=(100, 116, 139))
    
    # 2x2 Quadrant Grid - Centered Horizontally & Vertically within card
    grid_w = 540
    grid_h = 260
    grid_x = t_x + (t_w - grid_w) // 2 # 220
    grid_y = t_y + 76 # 310
    qw = (grid_w - 16) // 2 # 262
    qh = (grid_h - 16) // 2 # 122
    
    # Axis lines & labels
    axis_x = grid_x + qw + 8 # 490
    axis_y = grid_y + qh + 8 # 430
    draw.line([(axis_x, grid_y), (axis_x, grid_y + grid_h)], fill=(203, 213, 225), width=2)
    draw.line([(grid_x, axis_y), (grid_x + grid_w, axis_y)], fill=(203, 213, 225), width=2)
    
    # Axis Direction Labels with anchor alignment (Protected well inside card boundaries)
    draw.text((axis_x, grid_y - 12), "▲ 실시간 모멘텀 (초단위)", font=get_font(10, 'bold'), fill=(0, 82, 255), anchor='ms')
    draw.text((axis_x, grid_y + grid_h + 16), "▼ 적립식 장기 (월단위)", font=get_font(10, 'bold'), fill=(100, 116, 139), anchor='ma')
    draw.text((grid_x - 12, axis_y), "◀ 직관/감", font=get_font(10, 'bold'), fill=(100, 116, 139), anchor='rm')
    draw.text((grid_x + grid_w + 12, axis_y), "데이터/역산 ▶", font=get_font(10, 'bold'), fill=(0, 82, 255), anchor='lm')
    
    # Quadrant 1: Top-Right (Active Momentum Quant) - CORE TARGET
    q1_x = grid_x + qw + 16
    q1_y = grid_y
    draw.rounded_rectangle([q1_x, q1_y, q1_x + qw, q1_y + qh], radius=8, fill=(239, 246, 255), outline=(147, 197, 253), width=1)
    draw_pill_badge(draw, left_x=q1_x + 12, cy=q1_y + 22, text="CORE TARGET", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22, solid=True)
    draw.text((q1_x + 12, q1_y + 44), "실시간 모멘텀 퀀트", font=get_font(13, 'bold'), fill=(0, 82, 255))
    draw.text((q1_x + 12, q1_y + 68), "• 두꺼운 기출집 휴대 피로 극심\n• 10문항 숏폼 & 즉시 채점 최우선 수용", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    # Quadrant 2: Bottom-Right (Systematic Exam Taker) - PRIMARY TARGET
    q2_x = q1_x
    q2_y = grid_y + qh + 16
    draw.rounded_rectangle([q2_x, q2_y, q2_x + qw, q2_y + qh], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw_pill_badge(draw, left_x=q2_x + 12, cy=q2_y + 22, text="PRIMARY TARGET", font=get_font(9.5, 'bold'), theme='green', has_dot=True, pad_x=8, height=22, solid=True)
    draw.text((q2_x + 12, q2_y + 44), "안정 적립식 플래너", font=get_font(13, 'bold'), fill=(5, 150, 105))
    draw.text((q2_x + 12, q2_y + 68), "• 계획적 실전 시험 및 시간 안배 중시\n• 80분 OMR 타이머 및 실전 회차 풀이", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    # Quadrant 3: Top-Left (Impulsive Scalper) - SECONDARY TARGET
    q3_x = grid_x
    q3_y = grid_y
    draw.rounded_rectangle([q3_x, q3_y, q3_x + qw, q3_y + qh], radius=8, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw_pill_badge(draw, left_x=q3_x + 12, cy=q3_y + 22, text="SECONDARY TARGET", font=get_font(9.5, 'bold'), theme='amber', has_dot=True, pad_x=8, height=22, solid=True)
    draw.text((q3_x + 12, q3_y + 44), "충동적 모멘텀 스캘퍼", font=get_font(13, 'bold'), fill=(180, 83, 9))
    draw.text((q3_x + 12, q3_y + 68), "• 사료 독해 난항으로 오답 반복\n• 솔루션 : 핵심 단서 하이라이트 & 50:50 찬스", font=get_font(11, 'regular'), fill=(120, 53, 15), spacing=3)
    
    # Quadrant 4: Bottom-Left (Blind Averager) - POTENTIAL TARGET
    q4_x = grid_x
    q4_y = grid_y + qh + 16
    draw.rounded_rectangle([q4_x, q4_y, q4_x + qw, q4_y + qh], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=q4_x + 12, cy=q4_y + 22, text="POTENTIAL TARGET", font=get_font(9.5, 'bold'), theme='slate', has_dot=True, pad_x=8, height=22, solid=True)
    draw.text((q4_x + 12, q4_y + 44), "비이성적 맹목 매수자", font=get_font(13, 'bold'), fill=(71, 85, 105))
    draw.text((q4_x + 12, q4_y + 68), "• 특정 시대(근현대사 등) 취약 누적\n• 솔루션 : 시대별 레이더 & 오답 볼트", font=get_font(11, 'regular'), fill=(71, 85, 105), spacing=3)

    # ==============================================================
    # 2. TOP-RIGHT: Competitive Benchmark Table (Reference Image 2 Style)
    # ==============================================================
    c_x = 910
    c_y = 234
    c_w = 810
    c_h = 378
    draw.rounded_rectangle([c_x, c_y, c_x + c_w, c_y + c_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((c_x + 24, c_y + 18), "COMPETITIVE BENCHMARK (경쟁사 비교 분석)", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((c_x + 24, c_y + 38), "국내 주요 에듀테크 앱 대비 대한국사의 5대 핵심 차별점", font=get_font(11.5, 'medium'), fill=(100, 116, 139))
    
    # Table layout dimensions
    tbl_x = c_x + 20
    tbl_w = c_w - 40
    th_y = c_y + 64
    th_h = 36
    th_cy = th_y + th_h // 2
    
    x1 = tbl_x + 16
    x2 = tbl_x + 155
    x3 = tbl_x + 335
    col4_x = tbl_x + 520
    col4_w = tbl_w - 520
    
    # Table Header Row background
    draw.rounded_rectangle([tbl_x, th_y, tbl_x + tbl_w, th_y + th_h], radius=8, fill=(241, 245, 249))
    
    # DAEHANGUKSA Column 4 Highlight Card (Runs behind header & all data rows)
    draw.rounded_rectangle([col4_x, th_y - 2, col4_x + col4_w, th_y + th_h + 5 * 46 + 4], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    
    # Header Labels
    draw.text((x1, th_cy), "비교 차원 (Dimensions)", font=get_font(11.5, 'bold'), fill=(71, 85, 105), anchor='lm')
    draw.text((x2, th_cy), "증권사 MTS", font=get_font(11.5, 'bold'), fill=(71, 85, 105), anchor='lm')
    draw.text((x3, th_cy), "일반 계산기 웹/앱", font=get_font(11.5, 'bold'), fill=(71, 85, 105), anchor='lm')
    draw_pill_badge(draw, cx=col4_x + col4_w // 2, cy=th_cy, text="대한국사 (본 앱)", font=get_font(11, 'bold'), theme='blue', solid=True, has_dot=True, height=26, pad_x=12)
    
    rows = [
        ("학습 모드", "단순 PDF 문제 나열", "광고 팝업 지연 풀이", "실전 모의고사 + 10문항 숏폼"),
        ("연산 엔진", "사후 단순 가중평균", "1회성 수동 단일 수식", "닫힌 형식(Closed-Form) 역산"),
        ("의사결정", "단순 평가액 나열", "결과 저장 미지원", "A vs B 시뮬레이션 매트릭스"),
        ("오답 관리", "수동 스크랩 캡처", "별도 노트 작성 필요", "원터치 자동 인덱싱 오답 볼트"),
        ("프라이버시", "서버 공인인증 필수", "임시 세션 리셋", "100% 온디바이스 로컬 암호화")
    ]
    
    row_h = 46
    r_y = th_y + th_h + 6
    for dim, r_mts, r_app, r_smart in rows:
        row_cy = r_y + row_h // 2
        # Clean horizontal divider line across entire table
        draw.line([(tbl_x + 10, r_y), (tbl_x + tbl_w - 10, r_y)], fill=(235, 240, 245), width=1)
        
        draw.text((x1, row_cy), dim, font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((x2, row_cy), r_mts, font=get_font(11.5, 'regular'), fill=(100, 116, 139), anchor='lm')
        draw.text((x3, row_cy), r_app, font=get_font(11.5, 'regular'), fill=(100, 116, 139), anchor='lm')
        
        # Col 4: dot + bold blue text
        dot_r = 3.5
        draw.ellipse([int(round(col4_x + 16 - dot_r)), int(round(row_cy - dot_r)), int(round(col4_x + 16 + dot_r)), int(round(row_cy + dot_r))], fill=(0, 82, 255))
        draw.text((col4_x + 28, row_cy), r_smart, font=get_font(11.5, 'bold'), fill=(0, 82, 255), anchor='lm')
        r_y += row_h
        
    # ==============================================================
    # 3. BOTTOM: 2 PERSONA CARDS WITH BEHAVIOR SLIDERS (Image 3 Style)
    # ==============================================================
    p_y = 632
    pw = 800
    ph = 338
    
    # Persona A (김투자)
    draw.rounded_rectangle([100, p_y, 100 + pw, p_y + ph], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=128, cy=p_y + 26, text="ARCHETYPE A", font=get_font(10, 'bold'), theme='blue', has_dot=True, pad_x=10, height=24)
    draw.text((260, p_y + 26), "김투자 (34세, 적립식 직장인 투자자)", font=get_font(16.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # 22px bottom margin below badge
    draw.text((128, p_y + 60), '"월급날마다 분할 매수하지만, 내 자금이 언제 바닥날지 늘 불안합니다."', font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    
    desc_a = [
        "• 투자 성향 : 계획적 분할 매수를 원하나 모바일에서 계산 수식 관리가 어려움",
        "• 주요 고통 : 추가 매수로 인해 특정 종목 비중이 커져 포트폴리오 균형 붕괴",
        "• 핵심 목표 : 출퇴근 자투리 시간 10분 활용 한능검 1급 80점 이상 단기 취득"
    ]
    dy = p_y + 84
    for d in desc_a:
        draw.text((128, dy), d, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 22
        
    draw.line([(128, p_y + 160), (100 + pw - 28, p_y + 160)], fill=(241, 245, 249), width=1)
    draw.text((128, p_y + 172), "BEHAVIOR SPECTRUM (투자 행동 성향 지표)", font=get_font(10.5, 'bold'), fill=(100, 116, 139))
    
    draw_behavior_slider(draw, 128, p_y + 204, 350, "매매 주기", "안정 적립", "공격 단타", 0.20, theme='blue')
    draw_behavior_slider(draw, 500, p_y + 204, 350, "자금 운용", "계획 분할", "몰빵 집중", 0.25, theme='blue')
    draw_behavior_slider(draw, 128, p_y + 250, 350, "계산 도구", "수동 암산", "퀀트 역산", 0.35, theme='blue')
    draw_behavior_slider(draw, 500, p_y + 250, 350, "모바일 긴급", "여유 조망", "초단위 긴급", 0.60, theme='blue')
    
    # Persona B (박스캘퍼)
    pb_x = 100 + pw + 20
    draw.rounded_rectangle([pb_x, p_y, pb_x + pw, p_y + ph], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=pb_x + 28, cy=p_y + 26, text="ARCHETYPE B", font=get_font(10, 'bold'), theme='amber', has_dot=True, pad_x=10, height=24)
    draw.text((pb_x + 160, p_y + 26), "박스캘퍼 (28세, 실시간 모멘텀 트레이더)", font=get_font(16.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # 22px bottom margin below badge
    draw.text((pb_x + 28, p_y + 60), '"초 단위로 쏟아지는 급락장에서 가격을 치고 있을 여유가 없습니다."', font=get_font(13.5, 'bold'), fill=(217, 119, 6))
    
    desc_b = [
        "• 학습 성향 : 실전 기출 반복 풀이, 사료 키워드 중심의 직관적 암기 선호",
        "• 주요 고통 : 두꺼운 문제집과 사료집 분권으로 이동 중 학습 불가 및 오답 정리 피로",
        "• 핵심 목표 : 말 한마디로 끝나는 0.2초 음성 입력과 목표 탈출 수량 즉시 확인"
    ]
    dy = p_y + 84
    for d in desc_b:
        draw.text((pb_x + 28, dy), d, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 22
        
    draw.line([(pb_x + 28, p_y + 160), (pb_x + pw - 28, p_y + 160)], fill=(241, 245, 249), width=1)
    draw.text((pb_x + 28, p_y + 172), "BEHAVIOR SPECTRUM (투자 행동 성향 지표)", font=get_font(10.5, 'bold'), fill=(100, 116, 139))
    
    draw_behavior_slider(draw, pb_x + 28, p_y + 204, 350, "매매 주기", "안정 적립", "공격 단타", 0.95, theme='amber')
    draw_behavior_slider(draw, pb_x + 400, p_y + 204, 350, "자금 운용", "계획 분할", "몰빵 집중", 0.85, theme='amber')
    draw_behavior_slider(draw, pb_x + 28, p_y + 250, 350, "계산 도구", "수동 암산", "퀀트 역산", 0.85, theme='amber')
    draw_behavior_slider(draw, pb_x + 400, p_y + 250, 350, "모바일 긴급", "여유 조망", "초단위 긴급", 1.00, theme='amber')
    
    draw_slide_footer(draw, 3)
    base.save(f'{OUT_DIR}/slide_03.png')
    print("SAVED diverse Slide 03 (Target 2x2 Matrix + Benchmark + Personas) successfully!")

def make_slide_04():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header - Simplified title
    draw_slide_header(
        draw, 
        slide_num=4, 
        category_en="INFORMATION ARCHITECTURE · 5대 핵심 메뉴 구조", 
        title_black="수험생이 한눈에 파악하는 ", 
        title_blue="5대 합격 학습 내비게이션", 
        subtitle_kr="실전 모의고사부터 시대별 핵심 요약, AI 오답 노트까지 학습 흐름이 끊기지 않는 최적의 정보 구조"
    )
    
    # Top-Right Badge: Clean, Compact Overview (w=340, h=60, nicely proportioned)
    top_badge_x = 1480
    top_badge_y = 65
    draw.rounded_rectangle([top_badge_x, top_badge_y, top_badge_x + 340, top_badge_y + 60], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=top_badge_x + 16, cy=top_badge_y + 30, text="서비스 구성", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=24)
    draw.text((top_badge_x + 110, top_badge_y + 20), "5대 메인 탭", font=get_font(12, 'bold'), fill=(15, 23, 42))
    draw.text((top_badge_x + 110, top_badge_y + 39), "총 15개 직관적 화면 설계", font=get_font(10.5, 'medium'), fill=(100, 116, 139))
    
    # Level 0 Root Node: Compact, Centered, Clean Korean!
    # Width: 460px (x: 730 to 1190) - NOT overly wide!
    root_x1, root_y1, root_x2, root_y2 = 730, 226, 1190, 286
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=12, fill=(255, 255, 255), outline=(0, 82, 255), width=2)
    b_root = draw_pill_badge(draw, left_x=root_x1 + 18, cy=root_y1 + 30, text="시작 화면", font=get_font(10, 'bold'), theme='blue', has_dot=True, pad_x=10, height=26)
    draw.text((b_root[2] + 16, root_y1 + 19), "대한국사 전체 5대 핵심 메뉴 구조", font=get_font(14.5, 'bold'), fill=(15, 23, 42))
    draw.text((b_root[2] + 16, root_y1 + 41), "한 손으로 편리하게 이용하는 5대 핵심 메뉴와 기능 안내", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # Connectors from Root Node to 5 Level 1 Columns
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    col_centers = [cx + cw // 2 for cx in cols_x]
    
    draw.line([(960, root_y2), (960, 308)], fill=(0, 82, 255), width=2)
    draw.ellipse([956, 304, 964, 312], fill=(0, 82, 255))
    draw.line([(col_centers[0], 308), (col_centers[-1], 308)], fill=(0, 82, 255, 180), width=2)
    for cx in col_centers:
        draw.ellipse([cx - 4, 308 - 4, cx + 4, 308 + 4], fill=(0, 82, 255))
        draw_arrow(draw, (cx, 308), (cx, 330), col=(0, 82, 255), width=2, arrow_size=4)
        
    # 5 Domains Data (Clean Korean, easily understandable terms, zero developer jargon!)
    domains_data = [
        ("01. 홈 대시보드", "학습 현황 종합 관제", "출석 스트릭, 오늘의 추천 기출, 시대별 진도율을 한눈에 조회", [
            ("기본 화면", "자산 현황 요약", "내 투자금과 총 수익률, 현재 환율을 한눈에 확인", False),
            ("스트릭 현황", "연속 학습 달성", "매일 이어지는 학습 습관과 잔여 목표 일수 확인", False),
            ("입력 창", "음성 간편 입력", "숫자를 직접 치지 않고 말 한마디로 단가와 수량 입력", True)
        ]),
        ("02. 실전 기출 센터", "회차별 모의고사", "최신 77회 한능검 심화 50문항 실전 응시 및 80분 타이머", [
            ("실전 50제", "공인 시험 모의고사", "실제 시험지와 동일한 배점 및 80분 OMR 마킹 시뮬레이션", False),
            ("숏폼 10제", "자투리 10문항", "출퇴근길 5분 만에 푸는 핵심 기출 압축 테스트", False),
            ("비교 화면", "매수 방식 비교", "한 번에 몰아서 살 때와 나눠서 살 때의 결과 비교", True)
        ]),
        ("03. 시대별 서고", "선사부터 현대사까지", "6대 시대별 요약 카드, 유물 고해상도 갤러리 및 오디오", [
            ("시대별 요약", "핵심 사료 정리", "선사·삼국·고려·조선·근대·현대사 마스터 노트", True),
            ("안내 팝업", "현실적인 목표 안내", "도달하기 어려운 무리한 목표일 때 실현 가능한 수치 안내", True),
            ("유물 갤러리", "시각 자료 도감", "시험에 빈출되는 국보·보물 유물 고화질 사진 및 해설", True)
        ]),
        ("04. 위험 진단", "안전한 계좌 관리", "무리한 추가 매수를 막고 현금 비중을 안전하게 유지", [
            ("진단 화면", "종목 비중 점검", "특정 종목에 투자금이 너무 쏠리지 않도록 비중 점검", True),
            ("알림 창", "안전 잔고 알림", "무리한 매수로 현금이 바닥나지 않도록 안전 가이드 제공", True),
            ("예측 화면", "시장 변동 점검", "주가가 더 떨어졌을 때 내 계좌에 미치는 영향 미리 확인", True)
        ]),
        ("05. 맞춤 설정", "편리한 환경 설정", "통화 변경, 다국어 지원, 안전한 내 기기 데이터 보관", [
            ("설정 화면", "통화 및 환율 선택", "원화(KRW), 달러(USD) 등 원하는 화폐 단위로 자유롭게 변환", False),
            ("안내 화면", "광고 없는 안심 모드", "방해 요소 없이 깔끔하고 쾌적하게 계산기 이용", True),
            ("보안 화면", "안전한 기기 내 보관", "모든 자산 정보는 외부 전송 없이 내 폰에만 안전하게 보관", True)
        ])
    ]
    
    # Render 5 Columns
    for i, (dom_code, dom_name, dom_desc, containers) in enumerate(domains_data):
        cx = cols_x[i]
        
        # Level 1 Domain Header Card (y=330 to 402, h=72)
        draw.rounded_rectangle([cx, 330, cx + cw, 402], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((cx + 18, 344), dom_code, font=get_font(10, 'bold'), fill=(0, 82, 255))
        draw.text((cx + 18, 363), dom_name, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 18, 383), dom_desc, font=get_font(9, 'medium'), fill=(100, 116, 139))
        
        # Vertical Tree Line
        tree_x = cx + 16
        draw.line([(tree_x, 402), (tree_x, 672)], fill=(0, 82, 255, 100), width=2)
        
        # 3 L2 Cards per column (card_h = 82, gap = 10)
        card_w = cw - 32
        card_x = cx + 32
        cy = 414
        card_h = 82
        gap = 10
        
        for scr_type, title, desc, is_new in containers:
            draw.line([(tree_x, cy + 20), (card_x, cy + 20)], fill=(0, 82, 255, 120), width=2)
            draw.ellipse([tree_x - 3, cy + 20 - 3, tree_x + 3, cy + 20 + 3], fill=(0, 82, 255))
            
            card_bg = (255, 255, 255) if not is_new else (250, 252, 255)
            card_bd = (226, 232, 240) if not is_new else (191, 219, 254)
            draw.rounded_rectangle([card_x, cy, card_x + card_w, cy + card_h], radius=8, fill=card_bg, outline=card_bd, width=1)
            
            # Row 1: Friendly Korean Type tag + NEW badge
            draw_pill_badge(draw, left_x=card_x + 14, cy=cy + 15, text=scr_type, font=get_font(8.5, 'bold'), theme='gray', pad_x=6, height=18)
            if is_new:
                draw_pill_badge(draw, left_x=card_x + card_w - 46, cy=cy + 15, text="핵심", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18, solid=True)
                
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
        ("01", "명확한 5대 메뉴 분리", "찾고 싶은 기능을 헤매지 않고 바로 접근할 수 있도록 5개 핵심 메뉴를 명확하게 분리했습니다.",
         ["· 모의고사 응시, 시대별 학습, 오답 복습을 3탭 이내로 완결", "· 불필요한 탐색 없이 목표 회차로 1초 만에 진입"]),
        ("02", "한 손 조작 최적화", "엄지손가락이 닿기 쉬운 화면 하단에 핵심 입력과 조작 버튼을 집중 배치했습니다.",
         ["· 이동 중에도 한 손으로 흔들림 없이 편안한 입력", "· 자연어 음성 인식으로 숫자 자판 입력 부담 해소"]),
        ("03", "실전 사료 단서 판독", "복잡한 한문 사료도 핵심 키워드 하이라이트로 정답의 결정적 단서를 0.5초 만에 포착합니다.",
         ["· 직관적인 모의고사 진행으로 실시간 점수 피드백", "· 취약 시대를 집중 공략하는 맞춤형 오답 볼트 제공"]),
        ("04", "100% 기기 내 안심 보관", "개인 금융 데이터나 자산 정보를 외부 서버로 보내지 않고 내 폰 안에서만 안전하게 보관합니다.",
         ["· 회원가입이나 로그인 없이 즉시 사용 가능한 안심 구조", "· 외부 유출 걱정 없는 완벽한 프라이버시 보장"])
    ]
    
    for pidx, (pnum, ptitle, pdesc, psub_lines) in enumerate(pillars):
        px = 100 + pidx * (bp_w + bp_gap)
        draw.rounded_rectangle([px, bar_y, px + bp_w, bar_y + bp_h], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Number chip + Title
        draw.rounded_rectangle([px + 18, bar_y + 18, px + 52, bar_y + 44], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((px + 35, bar_y + 31), pnum, font=get_font(11, 'bold'), fill=(0, 82, 255), anchor='mm')
        
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
    # auto_out stripped
    print("SAVED new Slide 04 to both locations successfully!")

def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header - Simplified title
    draw_slide_header(
        draw, 
        slide_num=5, 
        category_en="USER FLOW | SERVICE INTERACTION FLOWCHART", 
        title_black="사용자 행동과 판단을 이끄는 ", 
        title_blue="5단계 서비스 UX 플로우차트", 
        subtitle_kr="진입 온보딩부터 멀티모달 입력, 퀀트 역산, 리스크 가드, 포트폴리오 저장까지 이어지는 핵심 사용자 여정"
    )
    
    # Top-Right Legend: Compact Diagram Notation (w=540, h=78)
    leg_x = 1280
    leg_y = 65
    leg_w = 540
    leg_h = 78
    draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=leg_x + 16, cy=leg_y + 20, text="NOTATION", font=get_font(8, 'bold'), theme='blue', has_dot=True, pad_x=6, height=18)
    draw.text((leg_x + 105, leg_y + 20), "플로우차트 기호 범례", font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # 4 compact legend items with comfortable margins
    draw.rounded_rectangle([leg_x + 16, leg_y + 44, leg_x + 70, leg_y + 68], radius=10, fill=(0, 82, 255))
    draw.text((leg_x + 43, leg_y + 56), "Start/End", font=get_font(7, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((leg_x + 76, leg_y + 56), "시작/종료", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 142, leg_y + 44, leg_x + 192, leg_y + 68], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 167, leg_y + 56), "Screen", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((leg_x + 198, leg_y + 56), "화면/접점", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 268, leg_y + 44, leg_x + 318, leg_y + 68], radius=4, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw.text((leg_x + 293, leg_y + 56), "Action", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    draw.text((leg_x + 325, leg_y + 56), "사용자 행동", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw_diamond(draw, cx=leg_x + 410, cy=leg_y + 56, w=34, h=22, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw.text((leg_x + 410, leg_y + 56), "Decide", font=get_font(6.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((leg_x + 434, leg_y + 56), "판단 분기", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    # -----------------------------------------------------------------
    # BODY GROUP: Generous 52px Clearance from Subtitle (y = 234)
    # -----------------------------------------------------------------
    # 5 STAGE COLUMNS
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    col_centers = [cx + cw // 2 for cx in cols_x]  # [264, 612, 960, 1308, 1656]
    
    stages_info = [
        ("STAGE 01", "진입 & 온보딩", "Launch & Onboarding"),
        ("STAGE 02", "멀티모달 입력", "Multi-Modal Input"),
        ("STAGE 03", "퀀트 목표 역산", "Goal Inversion"),
        ("STAGE 04", "리스크 안전 가드", "Risk Guardrail"),
        ("STAGE 05", "플랜 확정 & 저장", "Plan Finalize & Save")
    ]
    
    # Stage Headers (y=234 to 284, h=50) - Generous 52px whitespace below subtitle!
    for i, (st_code, st_name, st_en) in enumerate(stages_info):
        cx = cols_x[i]
        # Inner padding: 16px left, 12px top
        draw.rounded_rectangle([cx, 234, cx + cw, 284], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw_pill_badge(draw, left_x=cx + 16, cy=249, text=st_code, font=get_font(7.5, 'bold'), theme='blue', pad_x=5, height=16)
        draw.text((cx + 86, 249), st_name, font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((cx + 16, 269), st_en, font=get_font(8.5, 'medium'), fill=(100, 116, 139), anchor='lm')
        
        # Inter-stage advance arrow with comfortable margin
        if i < 4:
            arrow_start_x = cx + cw
            arrow_end_x = cols_x[i + 1]
            draw_arrow(draw, (arrow_start_x + 2, 259), (arrow_end_x - 2, 259), col=(0, 82, 255), width=2, arrow_size=4)
            
    # Node width: 260px (Margin inside 328px column is 34px left and 34px right)
    nw = 260
    
    # =============================================================
    # DIAGRAM TRACK 1: STAGE 01 (Center: 264)
    # =============================================================
    c0 = col_centers[0]
    
    # 1. Start Capsule (y=300 to 328, h=28)
    draw.rounded_rectangle([c0 - 75, 300, c0 + 75, 328], radius=14, fill=(0, 82, 255))
    draw.text((c0, 314), "Start : 앱 실행", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw_arrow(draw, (c0, 328), (c0, 344), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Screen: 스플래시 & 홈 화면 (y=344 to 388, h=44)
    # Inner padding: 14px left, 10px top
    draw.rounded_rectangle([c0 - nw // 2, 344, c0 + nw // 2, 388], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=358, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c0 - 54, 358), "스플래시 & 로컬 환경 동기화", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c0, 375), "SQLite 로컬 DB 로드 및 환경설정 바인딩", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c0, 388), (c0, 406), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 3. Decision Diamond: 최초 실행 여부? (cy=432, w=176, h=52)
    draw_diamond(draw, cx=c0, cy=432, w=176, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c0, 432), "최초 실행 여부?", font=get_font(9.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    
    # Branch Yes (Right -> Onboarding loop)
    draw_dashed_line(draw, (c0 + 88, 432), (cols_x[0] + cw - 16, 432), col=(244, 63, 94), width=1)
    draw.text(((c0 + 88 + cols_x[0] + cw - 16) // 2, 422), "Yes (신규)", font=get_font(7.5, 'bold'), fill=(220, 38, 38), anchor='mm')
    draw_dashed_arrow(draw, (cols_x[0] + cw - 16, 432), (cols_x[0] + cw - 16, 464), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[0] + cw - 88, 464, cols_x[0] + cw - 6, 496], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[0] + cw - 47, 475), "온보딩 4단계", font=get_font(7.5, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw.text((cols_x[0] + cw - 47, 486), "핵심 인터랙션", font=get_font(7, 'medium'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[0] + cw - 47, 496), (cols_x[0] + cw - 47, 524), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[0] + cw - 47, 524), (c0 + nw // 2, 524), col=(244, 63, 94), width=1, arrow_size=3)
    
    # Branch No (Straight down -> Home Dashboard)
    draw_arrow(draw, (c0, 458), (c0, 502), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c0 - 30, 480), "No (기존)", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 4. Screen: 홈 대시보드 화면 로드 (y=502 to 546, h=44)
    draw.rounded_rectangle([c0 - nw // 2, 502, c0 + nw // 2, 546], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=516, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c0 - 54, 516), "홈 대시보드 화면 로드", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c0, 533), "학습 스트릭 · 모의고사 진도 · 취약 시대 1초 조망", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c0, 546), (c0, 564), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 5. Action: 손실 종목 카드 원터치 탭 (y=564 to 608, h=44)
    draw.rounded_rectangle([c0 - nw // 2, 564, c0 + nw // 2, 608], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=578, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c0 - 54, 578), "손실 종목 카드 원터치 탭", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c0, 595), "실전 50제 / 숏폼 10제 모의고사 진입 (회차 선택)", font=get_font(8, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c0, 608), (c0, 626), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 6. Feedback: 파라미터 번들 0ms 연동 (y=626 to 672, h=46)
    draw.rounded_rectangle([c0 - nw // 2, 626, c0 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c0 - 44, 640), "파라미터 번들 0ms 연동 완료", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c0, 656), "회차별 배점 및 80분 시험 타이머 즉시 초기화", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    # Inter-Stage Handover Arrow to Stage 02
    draw_arrow(draw, (cols_x[0] + cw, 647), (cols_x[1], 647), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[0] + cw + cols_x[1]) // 2, 635), "연동 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 2: STAGE 02 (Center: 612)
    # =============================================================
    c1 = col_centers[1]
    
    # 1. Screen: 바텀시트 전개 (y=300 to 344, h=44)
    draw.rounded_rectangle([c1 - nw // 2, 300, c1 + nw // 2, 344], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=314, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c1 - 54, 314), "0.2초 스마트 입력 시트 전개", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c1, 331), "엄지 조작 영역(Thumb Zone) 최적화 바텀시트", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c1, 344), (c1, 360), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Decision Container: 3대 멀티모달 입력 채널 (y=360 to 464, h=104)
    draw.rounded_rectangle([c1 - nw // 2, 360, c1 + nw // 2, 464], radius=6, fill=(250, 252, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=374, text="DECISION", font=get_font(6.5, 'bold'), theme='amber', pad_x=4, height=14)
    draw.text((c1 - 48, 374), "3대 멀티모달 입력 채널 선택", font=get_font(8.5, 'bold'), fill=(180, 83, 9), anchor='lm')
    
    # Channel rows with generous inner margins
    draw.rounded_rectangle([c1 - 114, 387, c1 + 114, 408], radius=4, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 110, cy=397, text="음성", font=get_font(6.5, 'bold'), theme='blue', pad_x=3, height=12)
    draw.text((c1 - 72, 397), "AI 음성 STT '15,000원에 100주' 발화", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    draw.rounded_rectangle([c1 - 114, 411, c1 + 114, 432], radius=4, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 110, cy=421, text="50:50찬스", font=get_font(6.5, 'bold'), theme='cyan', pad_x=3, height=12)
    draw.text((c1 - 68, 421), "원터치 50:50 확률 찬스로 오답 2개 소거", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    draw.rounded_rectangle([c1 - 114, 435, c1 + 114, 456], radius=4, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 110, cy=445, text="키패드", font=get_font(6.5, 'bold'), theme='slate', pad_x=3, height=12)
    draw.text((c1 - 68, 445), "정밀 5개 선지 중 정답 즉시 선택 및 마킹", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw_arrow(draw, (c1, 464), (c1, 478), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 3. Action: 파라미터 주입 (y=478 to 522, h=44)
    draw.rounded_rectangle([c1 - nw // 2, 478, c1 + nw // 2, 522], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=492, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c1 - 54, 492), "추가 매수가 & 목표단가 주입", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c1, 509), "1-Tap 또는 발화 종료 즉시 입력 번들 완성", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c1, 522), (c1, 540), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 4. Diamond Decision: 입력값 유효성 검증? (cy=566, w=196, h=52)
    draw_diamond(draw, cx=c1, cy=566, w=196, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c1, 560), "입력값 유효성 검증?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c1, 574), "결측치 & 음수 방어", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    
    # Branch No (Left loop)
    draw_dashed_line(draw, (c1 - 98, 566), (cols_x[1] + 16, 566), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[1] + 16, 566), (cols_x[1] + 16, 524), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[1] + 4, 496, cols_x[1] + 80, 524], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[1] + 42, 510), "햅틱 진동 피드백", font=get_font(7, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[1] + 42, 496), (cols_x[1] + 42, 482), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[1] + 42, 482), (c1 - nw // 2, 482), col=(244, 63, 94), width=1, arrow_size=3)
    
    # Branch Yes (Down)
    draw_arrow(draw, (c1, 592), (c1, 626), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c1 + 32, 609), "Yes (정상)", font=get_font(7.5, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    # 5. Feedback: 데이터 정규화 완료 (y=626 to 672, h=46)
    draw.rounded_rectangle([c1 - nw // 2, 626, c1 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c1 - 44, 640), "실시간 데이터 정규화 완료", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c1, 656), "정답 여부 즉시 판별 및 사료 단서 형광펜 호출", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    # Inter-Stage Handover Arrow to Stage 03
    draw_arrow(draw, (cols_x[1] + cw, 647), (cols_x[2], 647), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[1] + cw + cols_x[2]) // 2, 635), "연산 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 3: STAGE 03 (Center: 960)
    # =============================================================
    c2 = col_centers[2]
    
    # 1. Quant Engine Process (y=300 to 344, h=44)
    draw.rounded_rectangle([c2 - nw // 2, 300, c2 + nw // 2, 344], radius=6, fill=(239, 246, 255), outline=(0, 82, 255), width=2)
    draw_pill_badge(draw, left_x=c2 - 114, cy=314, text="QUANT", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c2 - 54, 314), "폐쇄형 퀀트 역산 가동 (0ms)", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c2, 331), "단일 수식 대수 전개로 필요 수량 0ms 즉시 산출", font=get_font(8, 'medium'), fill=(0, 82, 255), anchor='mm')
    draw_arrow(draw, (c2, 344), (c2, 362), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Diamond Decision: 목표가 실현 가능 범위? (cy=390, w=216, h=56)
    draw_diamond(draw, cx=c2, cy=390, w=216, h=56, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c2, 384), "목표가 실현 가능 범위?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c2, 397), "정답 선지 일치 여부 판별 (1~5번)", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    
    # Branch No (Left loop)
    draw_dashed_line(draw, (c2 - 108, 390), (cols_x[2] + 16, 390), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[2] + 16, 390), (cols_x[2] + 16, 416), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[2] + 4, 416, cols_x[2] + 80, 452], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[2] + 42, 428), "비정상 목표 경고", font=get_font(7, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw.text((cols_x[2] + 42, 440), "오답 해설 즉시 표시", font=get_font(6.5, 'medium'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[2] + 42, 452), (cols_x[2] + 42, 474), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[2] + 42, 474), (cols_x[1] + cw - 10, 474), col=(244, 63, 94), width=1, arrow_size=3)
    draw.text(((cols_x[2] + 42 + cols_x[1] + cw) // 2, 464), "재설정", font=get_font(7, 'bold'), fill=(220, 38, 38), anchor='mm')
    
    # Branch Yes (Down)
    draw_arrow(draw, (c2, 418), (c2, 454), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c2 + 30, 436), "Yes (통과)", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 3. Screen: 역산 결과 시뮬레이션 (y=454 to 498, h=44)
    draw.rounded_rectangle([c2 - nw // 2, 454, c2 + nw // 2, 498], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=468, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c2 - 54, 468), "목표 역산 시뮬레이터 뷰", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c2, 485), "필요 매수 수량 & 소요 자금 오차 0.00% 산출", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c2, 498), (c2, 518), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 4. Action: 차수별 분할 조절 (y=518 to 562, h=44)
    draw.rounded_rectangle([c2 - nw // 2, 518, c2 + nw // 2, 562], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=532, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c2 - 54, 532), "차수별 분할 매수 비중 조절", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c2, 549), "문항별 사료 키워드 판독 & 상세 해설 시뮬레이션", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c2, 562), (c2, 626), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 5. Feedback: 분할 매수 확정 (y=626 to 672, h=46)
    draw.rounded_rectangle([c2 - nw // 2, 626, c2 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c2 - 44, 640), "차수별 분할 매수 분배 완료", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c2, 656), "1차~N차 분할 가중치 & 계좌 방어율 매핑", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    # Inter-Stage Handover Arrow to Stage 04
    draw_arrow(draw, (cols_x[2] + cw, 647), (cols_x[3], 647), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[2] + cw + cols_x[3]) // 2, 635), "검증 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 4: STAGE 04 (Center: 1308)
    # =============================================================
    c3 = col_centers[3]
    
    # 1. Screen: 포트폴리오 리스크 시트 (y=300 to 344, h=44)
    draw.rounded_rectangle([c3 - nw // 2, 300, c3 + nw // 2, 344], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=314, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c3 - 54, 314), "포트폴리오 리스크 시뮬레이션", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c3, 331), "모의고사 완료 후 총점 및 시대별 취약 레이더 산출", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c3, 344), (c3, 362), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Diamond Decision: 오답 발생 여부 판정 (cy=390, w=216, h=56)
    draw_diamond(draw, cx=c3, cy=390, w=216, h=56, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c3, 384), "오답 발생 판정 (Auto Vault)", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c3, 397), "틀린 문항 자동 감지 여부 ?", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    
    # Branch Yes (Left warning)
    draw_dashed_line(draw, (c3 - 108, 390), (cols_x[3] + 16, 390), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[3] + 16, 390), (cols_x[3] + 16, 416), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[3] + 4, 416, cols_x[3] + 80, 452], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[3] + 42, 428), "자금 고갈 주의", font=get_font(7, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw.text((cols_x[3] + 42, 440), "분할 차수 확대 권고", font=get_font(6.5, 'medium'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[3] + 42, 452), (cols_x[3] + 42, 474), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[3] + 42, 474), (c3 - nw // 2, 474), col=(244, 63, 94), width=1, arrow_size=3)
    
    # Branch No (Down: Safe)
    draw_arrow(draw, (c3, 418), (c3, 454), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c3 + 30, 436), "No (안전)", font=get_font(7.5, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    # 3. Action: 하락 스트레스 테스트 검증 (y=454 to 498, h=44)
    draw.rounded_rectangle([c3 - nw // 2, 454, c3 + nw // 2, 498], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=468, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c3 - 54, 468), "하락 스트레스 테스트 검증", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c3, 485), "시장 -10%~-30% 급락 시 계좌 충격도 점검", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c3, 498), (c3, 524), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 4. Diamond Decision: 리스크 허용 한도 승인? (cy=550, w=186, h=52)
    draw_diamond(draw, cx=c3, cy=550, w=186, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c3, 544), "리스크 허용 한도 승인?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c3, 558), "객관적 방어선 충족 판정", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    draw_arrow(draw, (c3, 576), (c3, 626), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c3 + 30, 601), "승인 완료", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 5. Feedback: 최종 승인 완료 (y=626 to 672, h=46)
    draw.rounded_rectangle([c3 - nw // 2, 626, c3 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c3 - 44, 640), "안전 가이드 적합 최종 승인", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c3, 656), "리스크 검증 완료 및 최종 분할 매수안 확정", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    # Inter-Stage Handover Arrow to Stage 05
    draw_arrow(draw, (cols_x[3] + cw, 647), (cols_x[4], 647), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[3] + cw + cols_x[4]) // 2, 635), "승인 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 5: STAGE 05 (Center: 1656)
    # =============================================================
    c4 = col_centers[4]
    
    # 1. Action: 1-Tap 포트폴리오 저장 (y=300 to 344, h=44)
    draw.rounded_rectangle([c4 - nw // 2, 300, c4 + nw // 2, 344], radius=6, fill=(239, 246, 255), outline=(0, 82, 255), width=2)
    draw_pill_badge(draw, left_x=c4 - 114, cy=314, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c4 - 54, 314), "1-Tap 포트폴리오 저장", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c4, 331), "최적 매수 플랜 & 시나리오를 내 자산에 즉시 반영", font=get_font(7.5, 'medium'), fill=(15, 23, 42), anchor='mm')
    draw_arrow(draw, (c4, 344), (c4, 362), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Feedback: 저장 완료 스낵바 (y=362 to 406, h=44)
    draw.rounded_rectangle([c4 - nw // 2, 362, c4 + nw // 2, 406], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=376, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c4 - 44, 376), "저장 완료 스낵바 & 자산 연동", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c4, 393), "스마트 오답 볼트 보관 및 취약 시대 집중 트레이닝 개시", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    draw_arrow(draw, (c4, 406), (c4, 426), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 3. Decision Diamond: 데이터 무결성 검증 (cy=454, w=206, h=56)
    draw_diamond(draw, cx=c4, cy=454, w=206, h=56, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c4, 448), "데이터 무결성 검증?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c4, 461), "외부 서버 전송 0건 & 로컬 암호화", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    draw_arrow(draw, (c4, 482), (c4, 514), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c4 + 32, 498), "100% 무결", font=get_font(7.5, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    # 4. Storage Node (y=514 to 562, h=48)
    draw_database_node(draw, cx=c4, cy=538, w=nw, h=48, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=530, text="STORAGE", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c4 - 48, 530), "100% 온디바이스 로컬 암호화", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c4, 550), "외부 서버 전송 0건, 개인 금융 데이터 완전 보호", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c4, 562), (c4, 586), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 5. Finish Terminal Capsule (y=586 to 622, h=36)
    draw.rounded_rectangle([c4 - 90, 586, c4 + 90, 622], radius=18, fill=(0, 82, 255))
    draw.text((c4, 604), "Finish : 최적 방어 플랜 저장", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # SIMPLIFIED BOTTOM SUMMARY STRIP (y=706 to 826, h=120)
    # Generous margin from diagram (cy ended at 668, gap = 38px)
    # -------------------------------------------------------------
    bar_x = 100
    # -------------------------------------------------------------
    bar_x = 100
    bar_y = 698
    bar_w = 1720
    bar_h = 142
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    
    # Left Half: Emotional Curve (w = 860) with generous internal padding
    draw_pill_badge(draw, left_x=bar_x + 24, cy=bar_y + 20, text="USER MINDSET", font=get_font(8, 'bold'), theme='amber', has_dot=True, pad_x=7, height=18)
    draw.text((bar_x + 150, bar_y + 20), "5단계 심리 변화 여정 (불안에서 확신까지)", font=get_font(11.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((bar_x + 24, bar_y + 40), "급락장 패닉 상태의 투자자가 객관적 퀀트 가이드를 통해 평정심을 되찾고 최적 플랜을 확정하는 여정", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    emotions = [
        ("STAGE 01", "불안 & 막막함", "red"),
        ("STAGE 02", "긴박 & 촉박", "amber"),
        ("STAGE 03", "명확한 목표 발견", "blue"),
        ("STAGE 04", "안도 & 통제감 회복", "cyan"),
        ("STAGE 05", "확신 & 플랜 확정", "green")
    ]
    node_w = 145
    node_y = bar_y + 58
    node_h = 68
    for e_idx, (ecode, ename, etheme) in enumerate(emotions):
        nx = bar_x + 24 + e_idx * (node_w + 22)
        draw.rounded_rectangle([nx, node_y, nx + node_w, node_y + node_h], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        # Inner padding inside emotion node: 12px left, 12px top, generous 15px bottom margin
        draw_pill_badge(draw, left_x=nx + 12, cy=node_y + 18, text=ecode, font=get_font(7.5, 'bold'), theme=etheme, pad_x=4, height=16)
        draw.text((nx + 12, node_y + 42), ename, font=get_font(9.5, 'bold'), fill=(15, 23, 42))
        if e_idx < 4:
            arrow_sx = nx + node_w + 2
            arrow_ex = nx + node_w + 20
            draw_arrow(draw, (arrow_sx, node_y + node_h // 2), (arrow_ex, node_y + node_h // 2), col=(148, 163, 184), width=1, arrow_size=3)
            
    # Vertical Divider Line
    draw.line([(bar_x + 890, bar_y + 14), (bar_x + 890, bar_y + bar_h - 14)], fill=(226, 232, 240), width=1)
    
    # Right Half: Enterprise UX KPIs (w = 800) with generous internal padding
    kpi_x = bar_x + 914
    draw_pill_badge(draw, left_x=kpi_x, cy=bar_y + 20, text="UX IMPACT", font=get_font(8, 'bold'), theme='blue', has_dot=True, pad_x=7, height=18)
    draw.text((kpi_x + 120, bar_y + 20), "정량적 서비스 기획 성과 지표", font=get_font(11.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((kpi_x, bar_y + 40), "실제 프로덕션 배포 및 태스크 기반 검증 완료 지표", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    kpis = [
        ("총 소요 시간", "< 3.2초", "기존 대비 84% 단축", "blue"),
        ("인터랙션 단계", "7단계 → 2단계", "엄지 영역 통합 설계", "green"),
        ("역산 연산 지연", "0ms 즉시", "폐쇄형 대수 공식 완결", "blue"),
        ("개인 금융 보안", "100% 로컬", "외부 유출 0건 온디바이스", "slate")
    ]
    kw = (bar_w - 938 - 24) // 4
    for kidx, (klabel, kval, ksub, kcol) in enumerate(kpis):
        kx = kpi_x + kidx * (kw + 10)
        draw.rounded_rectangle([kx, node_y, kx + kw, node_y + node_h], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        # Inner padding inside KPI card: 14px left, 13px top, and generous 13px bottom margin
        draw.text((kx + 14, node_y + 13), klabel, font=get_font(8.5, 'bold'), fill=(100, 116, 139))
        draw.text((kx + 14, node_y + 28), kval, font=get_font(12, 'bold'), fill=(0, 82, 255))
        draw.text((kx + 14, node_y + 46), ksub, font=get_font(7.5, 'medium'), fill=(71, 85, 105))
        
    draw_slide_footer(draw, 5)
    base.save(f'{OUT_DIR}/slide_05.png')
    print("SAVED perfect Slide 05 successfully!")



# Helper: Gradient Bar for Design System Tokens
def draw_gradient_bar(base, bbox, color_start, color_end, radius=6):
    x1, y1, x2, y2 = bbox
    bw = max(1, x2 - x1)
    bh = max(1, y2 - y1)
    bar_img = Image.new('RGBA', (bw, bh))
    r1, g1, b1 = color_start[:3]
    r2, g2, b2 = color_end[:3]
    for x in range(bw):
        t = x / max(1, bw - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        for y in range(bh):
            bar_img.putpixel((x, y), (r, g, b, 255))
    mask = Image.new('L', (bw, bh), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, bw, bh], radius=radius, fill=255)
    base.paste(bar_img, (x1, y1), mask)

def draw_home_icon(draw, cx, cy, size=18, color=(0, 81, 255)):
    s = size / 2.0
    draw.polygon([(cx, cy - s), (cx + s, cy - s*0.1), (cx - s, cy - s*0.1)], fill=color)
    draw.rectangle([cx - s*0.7, cy - s*0.1, cx + s*0.7, cy + s], fill=color)
    draw.rectangle([cx - s*0.25, cy + s*0.3, cx + s*0.25, cy + s], fill=(255, 255, 255))

def draw_chart_icon(draw, cx, cy, size=18, color=(100, 116, 139)):
    s = size / 2.0
    bw = s * 0.45
    draw.rounded_rectangle([cx - s*0.9, cy + s*0.1, cx - s*0.9 + bw, cy + s], radius=2, fill=color)
    draw.rounded_rectangle([cx - s*0.2, cy - s*0.4, cx - s*0.2 + bw, cy + s], radius=2, fill=color)
    draw.rounded_rectangle([cx + s*0.5, cy - s*0.9, cx + s*0.5 + bw, cy + s], radius=2, fill=color)

def draw_gear_icon(draw, cx, cy, size=18, color=(100, 116, 139)):
    s = size / 2.0
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], fill=color)
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        tx = cx + (s + 2) * math.cos(rad)
        ty = cy + (s + 2) * math.sin(rad)
        draw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=color)
    draw.ellipse([cx - s*0.45, cy - s*0.45, cx + s*0.45, cy + s*0.45], fill=(255, 255, 255))

def draw_mic_icon(draw, cx, cy, size=24, color=(255, 255, 255)):
    s = size / 2.0
    draw.rounded_rectangle([cx - s*0.35, cy - s*0.9, cx + s*0.35, cy + s*0.1], radius=int(s*0.35), fill=color)
    draw.arc([cx - s*0.65, cy - s*0.4, cx + s*0.65, cy + s*0.5], start=0, end=180, fill=color, width=2)
    draw.line([(cx, cy + s*0.5), (cx, cy + s*0.85)], fill=color, width=2)
    draw.line([(cx - s*0.4, cy + s*0.85), (cx + s*0.4, cy + s*0.85)], fill=color, width=2)

def draw_copy_icon(draw, cx, cy, size=14, color=(51, 65, 85)):
    s = size / 2.0
    draw.rectangle([cx - s*0.7, cy - s, cx + s*0.4, cy + s*0.3], outline=color, width=1)
    draw.rectangle([cx - s*0.3, cy - s*0.4, cx + s, cy + s], fill=(248, 250, 252), outline=color, width=1)

def draw_warning_triangle(draw, cx, cy, size=15, color=(245, 158, 11)):
    s = size / 2.0
    draw.polygon([(cx, cy - s), (cx + s, cy + s), (cx - s, cy + s)], fill=color)
    draw.line([(cx, cy - s*0.3), (cx, cy + s*0.2)], fill=(255, 255, 255), width=2)
    draw.point((cx, cy + s*0.6), fill=(255, 255, 255))


def make_slide_06():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=6, 
        category_en="WIREFRAME | MOBILE UX & ERGONOMIC ARCHITECTURE", 
        title_black="실제 앱 구조를 그대로 반영한 ", 
        title_blue="4대 모바일 와이어프레임과 인체공학적 설계", 
        subtitle_kr="홈 대시보드·계산기·음성도크·목표역산 4대 핵심 화면의 골격 구조와 한 손 조작을 위한 엄지 조작 반경(Thumb-Zone) 인체공학 설계"
    )
    
    # -----------------------------------------------------------------
    # UPPER SECTION: 4 EXPANDED MODERN 19.5:9 SMARTPHONE WIREFRAME CHASSIS
    # -----------------------------------------------------------------
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
    
    # VIP One-Line Banner Mockup
    v_y = sec_y + 54
    draw.rounded_rectangle([p1_x + 14, v_y, p1_x + pw - 14, v_y + 24], radius=6, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw.text((p1_x + 24, v_y + 6), "⚡ VIP 24h 무광고 세션", font=get_font(8.5, 'bold'), fill=(180, 83, 9))
    draw.text((p1_x + pw - 24, v_y + 6), "남은시간 23:59:42", font=get_num_font(8.5, 'bold'), fill=(217, 119, 6), anchor='ra')
    
    # Smart Portfolio Summary Card (_buildMembershipCard)
    sc_y = v_y + 32
    draw.rounded_rectangle([p1_x + 14, sc_y, p1_x + pw - 14, sc_y + 116], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((p1_x + 24, sc_y + 12), "스마트 포트폴리오 메인 요약", font=get_font(10.5, 'bold'), fill=(0, 81, 255))
    draw.text((p1_x + 24, sc_y + 32), "₩ 12,500,000", font=get_num_font(18, 'black'), fill=(15, 23, 42))
    draw.text((p1_x + 24, sc_y + 60), "목표 한능검 1급 D-28", font=get_font(10.5, 'bold'), fill=(239, 68, 68))
    draw_pill_badge(draw, cx=p1_x + pw - 48, cy=sc_y + 67, text="-17.2%", font=get_num_font(9, 'bold'), theme='red', has_dot=False, pad_x=8, height=18, solid=True)
    draw.line([(p1_x + 24, sc_y + 84), (p1_x + pw - 24, sc_y + 84)], fill=(191, 219, 254), width=1)
    draw.text((p1_x + 24, sc_y + 94), "• 1차 분할매수 가이드 권장", font=get_font(9.5, 'medium'), fill=(71, 85, 105))
    draw.text((p1_x + pw - 24, sc_y + 94), "통화 : KRW ₩", font=get_font(9.5, 'bold'), fill=(0, 81, 255), anchor='ra')
    
    # 1-Line Hero Button (_buildSimulatorHeroButton)
    hb_y = sc_y + 124
    draw.rounded_rectangle([p1_x + 14, hb_y, p1_x + pw - 14, hb_y + 36], radius=9, fill=(0, 81, 255))
    draw.text((p1_x + pw//2, hb_y + 18), "+ 최신 77회 모의고사 시작", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # 2x2 Quick Actions Grid (_buildQuickActions)
    qg_y = hb_y + 44
    qw = (pw - 28 - 10) // 2
    qh = 30
    quick_items = [("오답 노트 복습", 0), ("AI 약점 집중", 1), ("실전 기출센터", 2), ("시대별 요약노트", 3)]
    for q_txt, q_idx in quick_items:
        qx = p1_x + 14 + (q_idx % 2) * (qw + 10)
        qy = qg_y + (q_idx // 2) * (qh + 8)
        draw.rounded_rectangle([qx, qy, qx + qw, qy + qh], radius=7, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((qx + qw//2, qy + qh//2), q_txt, font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='mm')
        
    # Asset List Card Item (_buildAssetCard)
    ac_y = qg_y + 76
    draw.rounded_rectangle([p1_x + 14, ac_y, p1_x + pw - 14, ac_y + 50], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((p1_x + 24, ac_y + 9), "삼성전자 (005930)", font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p1_x + pw - 45, cy=ac_y + 16, text="-18.3%", font=get_num_font(8.5, 'bold'), theme='red', has_dot=False, pad_x=6, height=16)
    draw.text((p1_x + 24, ac_y + 29), "조선 후기 정치사 · 오답률 64.2%", font=get_font(9, 'medium'), fill=(100, 116, 139))
    
    # Callout Anchor Pin ① floating above Thumb-Zone
    draw_callout_anchor_pin(draw, p1_x + 24, ac_y + 68, "1", "① Fitts' 한 손 조작 존", (0, 81, 255), is_right=True)

    # Bottom Navigation Bar
    bb_y = sec_y + ph - 70
    draw.line([(p1_x + 14, bb_y), (p1_x + pw - 14, bb_y)], fill=(226, 232, 240), width=1)
    draw.text((p1_x + 40, bb_y + 18), "홈", font=get_font(10, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((p1_x + pw - 40, bb_y + 18), "설정", font=get_font(10, 'medium'), fill=(100, 116, 139), anchor='mm')
    # Center Mic FAB inside Thumb Zone
    fab_cx = p1_x + pw//2
    fab_cy = bb_y + 18
    draw.ellipse([fab_cx - 16, fab_cy - 16, fab_cx + 16, fab_cy + 16], fill=(0, 81, 255))
    draw_mic_icon(draw, cx=fab_cx, cy=fab_cy, size=16, color=(255, 255, 255))

    # -----------------------------------------------------------------
    # Chassis 2: [SCR-02 · 실전 한능검 50제 시험 센터] (p2_x = 580)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p2_x, "② SCR-02 · 계산기 엔진", "amber")
    
    # Input 1: Current Price & Holdings (_buildInputSection)
    i1_y = sec_y + 54
    draw.rounded_rectangle([p2_x + 14, i1_y, p2_x + pw - 14, i1_y + 54], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p2_x + 24, i1_y + 9), "실전 50제 모의고사 회차 선택", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((p2_x + 24, i1_y + 29), "₩ 65,000", font=get_num_font(15, 'bold'), fill=(15, 23, 42))
    draw.text((p2_x + pw - 24, i1_y + 29), "100 주 (₩6.5M)", font=get_font(10, 'bold'), fill=(71, 85, 105), anchor='ra')
    
    # Input 2: Additional Price & Stepper
    i2_y = i1_y + 64
    draw.rounded_rectangle([p2_x + 14, i2_y, p2_x + pw - 14, i2_y + 68], radius=10, fill=(248, 250, 252), outline=(0, 81, 255), width=2)
    draw.text((p2_x + 24, i2_y + 9), "추가 매수 단가 & 수량 조절", font=get_font(9.5, 'bold'), fill=(0, 81, 255))
    draw.text((p2_x + 24, i2_y + 29), "₩ 55,000", font=get_num_font(15, 'bold'), fill=(15, 23, 42))
    # Glowing cursor
    draw.line([(p2_x + 115, i2_y + 29), (p2_x + 115, i2_y + 47)], fill=(0, 81, 255), width=2)
    
    # Stepper Control [ - 50주 + ]
    st_y = i2_y + 21
    draw.rounded_rectangle([p2_x + pw - 105, st_y, p2_x + pw - 20, st_y + 28], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((p2_x + pw - 94, st_y + 14), "-", font=get_font(13, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((p2_x + pw - 62, st_y + 14), "50 주", font=get_num_font(10.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((p2_x + pw - 31, st_y + 14), "+", font=get_font(13, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    # Preset Chips Row
    pr_y = i2_y + 76
    chips = ["-5%", "-10%", "+50주", "+100주", "전액 매수"]
    c_x = p2_x + 14
    for cp in chips:
        c_w = (pw - 28 - 16) // len(chips)
        draw.rounded_rectangle([c_x, pr_y, c_x + c_w, pr_y + 24], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((c_x + c_w//2, pr_y + 12), cp, font=get_font(8.5, 'bold'), fill=(0, 81, 255), anchor='mm')
        c_x += c_w + 4
        
    # Callout Anchor Pin ② in clean corridor (y=474, chips end at 452, result card starts at 496)
    res_y = pr_y + 44
    draw_callout_anchor_pin(draw, p2_x + 24, pr_y + 34, "2", "② 비정상 사전 가드 엔진", (217, 119, 6), is_right=True)

    # Result Summary Card (_buildResultSummaryCard)
    draw.rounded_rectangle([p2_x + 14, res_y, p2_x + pw - 14, res_y + 114], radius=12, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw.text((p2_x + 24, res_y + 12), "실시간 가중평균 & 가드 결과", font=get_font(10.5, 'bold'), fill=(180, 83, 9))
    draw.text((p2_x + 24, res_y + 32), "50문항 / 잔여 79분 17초", font=get_num_font(16, 'black'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p2_x + pw - 48, cy=res_y + 40, text="+5.1%p", font=get_num_font(8.5, 'bold'), theme='amber', has_dot=False, pad_x=6, height=18, solid=True)
    draw.line([(p2_x + 24, res_y + 60), (p2_x + pw - 24, res_y + 60)], fill=(253, 230, 138), width=1)
    draw.text((p2_x + 24, res_y + 72), "진행률 : 1문항 완료 (49문항 대기)", font=get_font(9.5, 'medium'), fill=(71, 85, 105))
    draw.text((p2_x + 24, res_y + 92), "총 보유 수량 : 150 주 (본전 탈출선 회복)", font=get_font(9.5, 'bold'), fill=(15, 23, 42))
    
    # Primary CTA Button inside Thumb Zone
    btn_y = res_y + 124
    draw.rounded_rectangle([p2_x + 14, btn_y, p2_x + pw - 14, btn_y + 40], radius=10, fill=(0, 81, 255))
    draw_copy_icon(draw, cx=p2_x + 40, cy=btn_y + 20, size=13, color=(255, 255, 255))
    draw.text((p2_x + pw//2 + 8, btn_y + 20), "1-Tap MTS 주문 복사", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 3: [SCR-03 · 정답 해설 및 사료 단서 바텀시트] (p3_x = 1060)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p3_x, "③ SCR-03 · AI 음성 도크", "purple")
    
    # Dimmed background representation
    draw.rounded_rectangle([p3_x + 10, sec_y + 50, p3_x + pw - 10, sec_y + 105], radius=8, fill=(226, 232, 240))
    draw.text((p3_x + pw//2, sec_y + 68), "배경 : 계산기 화면 (Dim 60%)", font=get_font(9.5, 'regular'), fill=(100, 116, 139), anchor='mm')
    draw.text((p3_x + pw//2, sec_y + 86), "화면 전환 없는 온디바이스 모달 오버레이", font=get_font(8.5, 'medium'), fill=(148, 163, 184), anchor='mm')
    
    # Bottom Sheet Container (Sliding up within phone bezel)
    bs_y = sec_y + 105
    draw.rounded_rectangle([p3_x + 4, bs_y, p3_x + pw - 4, sec_y + ph - 8], radius=22, fill=(255, 255, 255), outline=(122, 34, 255), width=2)
    # Drag Handle
    draw.rounded_rectangle([p3_x + pw//2 - 20, bs_y + 8, p3_x + pw//2 + 20, bs_y + 13], radius=2, fill=(203, 213, 225))
    
    # Sheet Header Badge
    draw_pill_badge(draw, cx=p3_x + pw//2, cy=bs_y + 28, text="0.2s VOICE RECOGNITION", font=get_font(9, 'bold'), theme='purple', has_dot=True, pad_x=8, height=20)
    
    # Floating Mic Pulse Glow
    mic_cy = bs_y + 66
    draw.ellipse([p3_x + pw//2 - 26, mic_cy - 26, p3_x + pw//2 + 26, mic_cy + 26], fill=(245, 243, 255), outline=(221, 214, 254), width=1)
    draw.ellipse([p3_x + pw//2 - 19, mic_cy - 19, p3_x + pw//2 + 19, mic_cy + 19], fill=(122, 34, 255))
    draw_mic_icon(draw, cx=p3_x + pw//2, cy=mic_cy, size=17, color=(255, 255, 255))
    
    # Realtime 9-Bar Voice Waveform Animation
    wv_y = mic_cy + 34
    wave_h = [8, 16, 26, 36, 22, 14, 20, 30, 12]
    w_start_x = p3_x + pw//2 - (len(wave_h) * 12) // 2
    for idx, wh in enumerate(wave_h):
        wx = w_start_x + idx * 12
        draw.rounded_rectangle([wx, wv_y - wh//2, wx + 6, wv_y + wh//2], radius=3, fill=(122, 34, 255))
        
    # Callout Anchor Pin ③ in clean corridor (y=478, wave ends at 453, bubble starts at 498)
    draw_callout_anchor_pin(draw, p3_x + 24, wv_y + 34, "3", "③ 0.2s 음성 STT 도크", (122, 34, 255), is_right=True)

    # Speech Bubble Mockup
    sb_y = wv_y + 50
    draw.rounded_rectangle([p3_x + 14, sb_y, p3_x + pw - 14, sb_y + 44], radius=8, fill=(245, 243, 255), outline=(221, 214, 254), width=1)
    draw.text((p3_x + pw//2, sb_y + 14), "“삼성전자 55,000원에 50주”", font=get_font(11, 'bold'), fill=(109, 40, 217), anchor='mm')
    draw.text((p3_x + pw//2, sb_y + 30), "0.2s 음성 STT 파싱 완료 → 3개 파라미터 추출", font=get_font(8.5, 'regular'), fill=(100, 116, 139), anchor='mm')
    
    # Parsed Quant Tags Row
    pt_y = sb_y + 52
    tags = [("종목: 삼성전자", 100), ("단가: ₩55,000", 85), ("수량: 50주", 65)]
    tx_start = p3_x + 14
    for tg, tw in tags:
        draw.rounded_rectangle([tx_start, pt_y, tx_start + tw, pt_y + 24], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((tx_start + tw//2, pt_y + 12), tg, font=get_font(8.5, 'bold'), fill=(0, 81, 255), anchor='mm')
        tx_start += tw + 6
        
    # Auto Inject Button inside Thumb Zone
    inj_y = pt_y + 34
    draw.rounded_rectangle([p3_x + 14, inj_y, p3_x + pw - 14, inj_y + 40], radius=10, fill=(122, 34, 255))
    draw.text((p3_x + pw//2, inj_y + 20), "⚡ 계산기에 즉시 주입 (0.2s)", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 4: [SCR-04 · 스마트 오답 볼트] (p4_x = 1540)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p4_x, "④ SCR-04 · 스마트 오답 볼트", "green")
    
    # Target Goal Price Input
    g1_y = sec_y + 54
    draw.rounded_rectangle([p4_x + 14, g1_y, p4_x + pw - 14, g1_y + 52], radius=10, fill=(240, 246, 255), outline=(0, 81, 255), width=2)
    draw.text((p4_x + 24, g1_y + 9), "취약 시대 오답 집중 복습", font=get_font(9.5, 'bold'), fill=(0, 81, 255))
    draw.text((p4_x + 24, g1_y + 29), "₩ 70,000", font=get_num_font(17, 'black'), fill=(0, 81, 255))
    draw_pill_badge(draw, cx=p4_x + pw - 48, cy=g1_y + 32, text="TARGET", font=get_font(8.5, 'bold'), theme='blue', has_dot=False, pad_x=6, height=18)
    
    # Callout Anchor Pin ④ in clean corridor (g1 ends at 340, solution starts at 368)
    sol_y = g1_y + 76
    draw_callout_anchor_pin(draw, p4_x + 24, g1_y + 61, "4", "④ 0ms 닫힌 형식 역산", (5, 150, 105), is_right=True)

    # Closed-Form Solution Box (Green Theme)
    draw.rounded_rectangle([p4_x + 14, sol_y, p4_x + pw - 14, sol_y + 104], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((p4_x + 24, sol_y + 12), "닫힌 형식(Closed-Form) 역산 결과", font=get_font(10, 'bold'), fill=(5, 150, 105))
    draw.text((p4_x + 24, sol_y + 32), "필요 매수량 : +42.5 주", font=get_font(14, 'bold'), fill=(5, 150, 105))
    draw.text((p4_x + 24, sol_y + 54), "오답 누적 : 총 14문항 보관", font=get_font(14, 'bold'), fill=(217, 119, 6))
    draw.line([(p4_x + 24, sol_y + 78), (p4_x + pw - 24, sol_y + 78)], fill=(167, 243, 208), width=1)
    draw.text((p4_x + 24, sol_y + 88), "✓ 오차율 0.00% · 단일 대수 방정식 도출", font=get_font(8.5, 'bold'), fill=(5, 150, 105))
    
    # Risk Telemetry & Boundary Check Card
    rk_y = sol_y + 112
    draw.rounded_rectangle([p4_x + 14, rk_y, p4_x + pw - 14, rk_y + 80], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p4_x + 24, rk_y + 10), "시대별 취약 분석 레이더", font=get_font(10, 'bold'), fill=(15, 23, 42))
    draw.text((p4_x + 24, rk_y + 29), "• 자산 쏠림도 : 42.5% (안전 한도 65% 이하)", font=get_font(9, 'medium'), fill=(71, 85, 105))
    draw.text((p4_x + 24, rk_y + 46), "• 근현대사 취약도 68% (집중 보완 필요)", font=get_font(9, 'medium'), fill=(5, 150, 105))
    draw.text((p4_x + 24, rk_y + 62), "• 뇌동매매 방어 : 비정상 주문 사전 차단 완료", font=get_font(9, 'medium'), fill=(71, 85, 105))
    
    # Confirm Plan Action Button inside Thumb Zone
    cf_y = rk_y + 90
    draw.rounded_rectangle([p4_x + 14, cf_y, p4_x + pw - 14, cf_y + 40], radius=10, fill=(0, 81, 255))
    draw.text((p4_x + pw//2, cf_y + 20), "최종 분할 매수 플랜 확정 ↗", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # INTERACTION FLOW STEP CONNECTORS (Between the 4 phones)
    # -----------------------------------------------------------------
    flow_connectors = [
        (p1_x + pw, p2_x, "01 → 02 계산기 실행", "1-Tap Handoff", "blue"),
        (p2_x + pw, p3_x, "02 → 03 음성 도크 호출", "0.2s STT 파싱", "purple"),
        (p3_x + pw, p4_x, "03 → 04 목표 역산 연동", "닫힌 공식 도출", "blue")
    ]
    flow_cy = sec_y + 240
    for x_start, x_end, flow_title, flow_sub, f_theme in flow_connectors:
        fcx = (x_start + x_end) // 2
        # Subtle horizontal connection line
        draw.line([(x_start + 12, flow_cy), (x_end - 12, flow_cy)], fill=(203, 213, 225), width=2)
        # Flow Badge Circle
        draw.ellipse([fcx - 16, flow_cy - 16, fcx + 16, flow_cy + 16], fill=(255, 255, 255), outline=(0, 81, 255) if f_theme=='blue' else (122, 34, 255), width=2)
        draw.text((fcx, flow_cy), "→", font=get_font(14, 'bold'), fill=(0, 81, 255) if f_theme=='blue' else (122, 34, 255), anchor='mm')
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
            "한 손 파지 시 엄지가 닿는 하단 120dp 반경 내 주요 액션(계산 실행, MTS 복사, 음성 FAB)을 집중 배치하여 손가락 이동 거리를 65% 단축했습니다.",
            "✓ 엄지 도달 속도 0.18s 입증",
            "blue", (0, 81, 255)
        ),
        (
            100 + (c_w + c_gap),
            "BOUNDARY GUARD",
            "② 비정상 입력 사전 가드 엔진",
            "수험생의 오답 패턴과 취약 시대를 정밀 분석하여, 최적의 복습 타이밍과 맞춤형 사료 키워드를 추천합니다.",
            "✓ 주문 실수 및 뇌동매매 100% 차단",
            "amber", (217, 119, 6)
        ),
        (
            100 + (c_w + c_gap) * 2,
            "VOICE STT ENGINE",
            "③ 0.2초 온디바이스 음성 도크",
            "방대한 5,000년 역사 기출 문제와 사료를 1초 만에 검색하고, 50:50 찬스로 핵심 추론 훈련을 완성합니다.",
            "✓ 키패드 타이핑 피로 78% 절감",
            "purple", (122, 34, 255)
        ),
        (
            100 + (c_w + c_gap) * 3,
            "ZERO-LOSS HANDOFF",
            "④ 0ms 무손실 파라미터 인계",
            "역산으로 도출된 수치를 시뮬레이터와 MTS 클립보드로 0ms 자동 주입하여 수기 재입력 오류 및 시장가 매수 실수를 원천 방어합니다.",
            "✓ 파라미터 전달 손실률 0.00%",
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
        draw.rounded_rectangle([cx_card + 16, card_y + card_h - 34, cx_card + c_w - 16, card_y + card_h - 12], radius=6, fill=(240, 246, 255) if th_key=='blue' else ((245, 243, 255) if th_key=='purple' else (248, 250, 252)), outline=(191, 219, 254) if th_key=='blue' else (226, 232, 240), width=1)
        draw.text((cx_card + 24, card_y + card_h - 23), metric_txt, font=get_font(10, 'bold'), fill=accent_col, anchor='lm')

    draw_slide_footer(draw, 6)
    base.save(f'{OUT_DIR}/slide_06.png')
    print("SAVED slide_06.png (Enhanced 4-Screen Mobile Wireframe & Ergonomic Architecture)")


# -----------------------------------------------------------------------------
# 24dp Financial Line Iconography Drawers (Uniform 1.5dp Stroke & 2dp Radius)
# -----------------------------------------------------------------------------
def draw_line_chart_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.line([(cx - s*0.8, cy + s*0.8), (cx + s*0.8, cy + s*0.8)], fill=color, width=2)
    pts = [(cx - s*0.7, cy + s*0.4), (cx - s*0.2, cy + s*0.2), (cx + s*0.2, cy - s*0.1), (cx + s*0.7, cy - s*0.6)]
    draw.line(pts, fill=color, width=2)
    for px, py in pts:
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255), outline=color, width=1)
    draw.polygon([(cx + s*0.7, cy - s*0.6), (cx + s*0.4, cy - s*0.6), (cx + s*0.7, cy - s*0.3)], fill=color)

def draw_line_target_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.ellipse([cx - s*0.8, cy - s*0.8, cx + s*0.8, cy + s*0.8], outline=color, width=2)
    draw.ellipse([cx - s*0.35, cy - s*0.35, cx + s*0.35, cy + s*0.35], outline=color, width=1)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)
    draw.line([(cx - s*0.95, cy), (cx - s*0.6, cy)], fill=color, width=2)
    draw.line([(cx + s*0.6, cy), (cx + s*0.95, cy)], fill=color, width=2)
    draw.line([(cx, cy - s*0.95), (cx, cy - s*0.6)], fill=color, width=2)
    draw.line([(cx, cy + s*0.6), (cx, cy + s*0.95)], fill=color, width=2)

def draw_line_mic_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.rounded_rectangle([cx - s*0.35, cy - s*0.8, cx + s*0.35, cy + s*0.1], radius=int(s*0.35), outline=color, width=2)
    draw.arc([cx - s*0.65, cy - s*0.35, cx + s*0.65, cy + s*0.45], start=0, end=180, fill=color, width=2)
    draw.line([(cx, cy + s*0.45), (cx, cy + s*0.8)], fill=color, width=2)
    draw.line([(cx - s*0.4, cy + s*0.8), (cx + s*0.4, cy + s*0.8)], fill=color, width=2)

def draw_line_shield_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    pts = [
        (cx - s*0.75, cy - s*0.75),
        (cx + s*0.75, cy - s*0.75),
        (cx + s*0.75, cy + s*0.1),
        (cx, cy + s*0.85),
        (cx - s*0.75, cy + s*0.1)
    ]
    draw.polygon(pts, outline=color, fill=(240, 246, 255))
    draw.line([(cx - s*0.3, cy), (cx - s*0.05, cy + s*0.3), (cx + s*0.4, cy - s*0.3)], fill=color, width=2)

def draw_line_wallet_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.rounded_rectangle([cx - s*0.8, cy - s*0.6, cx + s*0.8, cy + s*0.7], radius=3, outline=color, width=2)
    draw.line([(cx - s*0.8, cy - s*0.2), (cx + s*0.8, cy - s*0.2)], fill=color, width=1)
    draw.rounded_rectangle([cx + s*0.2, cy - s*0.05, cx + s*0.85, cy + s*0.4], radius=2, fill=(240, 246, 255), outline=color, width=1)
    draw.ellipse([cx + s*0.45, cy + s*0.12, cx + s*0.6, cy + s*0.25], fill=color)

def draw_line_calc_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.rounded_rectangle([cx - s*0.7, cy - s*0.85, cx + s*0.7, cy + s*0.85], radius=3, outline=color, width=2)
    draw.rounded_rectangle([cx - s*0.5, cy - s*0.65, cx + s*0.5, cy - s*0.25], radius=1, fill=(240, 246, 255), outline=color, width=1)
    draw.text((cx - s*0.35, cy - s*0.05), "+", font=get_font(7, 'bold'), fill=color, anchor='mm')
    draw.text((cx + s*0.35, cy - s*0.05), "-", font=get_font(7, 'bold'), fill=color, anchor='mm')
    draw.text((cx - s*0.35, cy + s*0.45), "×", font=get_font(7, 'bold'), fill=color, anchor='mm')
    draw.text((cx + s*0.35, cy + s*0.45), "=", font=get_font(7, 'bold'), fill=color, anchor='mm')

def draw_line_lock_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.arc([cx - s*0.45, cy - s*0.85, cx + s*0.45, cy - s*0.05], start=180, end=0, fill=color, width=2)
    draw.rounded_rectangle([cx - s*0.65, cy - s*0.2, cx + s*0.65, cy + s*0.75], radius=3, fill=(240, 246, 255), outline=color, width=2)
    draw.ellipse([cx - 2, cy + s*0.05, cx + 2, cy + s*0.25], fill=color)
    draw.line([(cx, cy + s*0.2), (cx, cy + s*0.45)], fill=color, width=2)

def draw_line_tag_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    pts = [
        (cx - s*0.7, cy - s*0.3),
        (cx - s*0.2, cy - s*0.8),
        (cx + s*0.7, cy + s*0.1),
        (cx + s*0.2, cy + s*0.8),
        (cx - s*0.7, cy + s*0.3)
    ]
    draw.polygon(pts, outline=color, fill=(240, 246, 255), width=2)
    draw.ellipse([cx - s*0.35, cy - s*0.35, cx - s*0.15, cy - s*0.15], fill=color)
    draw.text((cx + s*0.1, cy + s*0.15), "%", font=get_font(7, 'bold'), fill=color, anchor='mm')

def make_slide_07():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=7, 
        category_en="DESIGN SYSTEM | TAEGEUK HERITAGE & EDUTECH COMPONENT ARCHITECTURE", 
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
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=8, 
        category_en="CORE FEATURE 01 | 실전 모의고사 & 50:50 찬스 인터랙션", 
        title_black="50문항 80분 공인 시험 환경과 ", 
        title_blue="추론 감각을 깨우는 50:50 찬스 엔진이에요.", 
        subtitle_kr="실제 시험지와 100% 동일한 배점 및 OMR 타이머를 구현하고, 헷갈리는 선지 2개를 제거하여 수험생의 소거법 추론을 돕는 코어 피처입니다.",
        right_badge=("EXAM SIMULATION 100%", "blue")
    )
    
    # Layout
    lx = 100
    lw = 680
    
    # Left Feature Card 1
    c1_y = 234
    c1_h = 240
    draw.rounded_rectangle([lx, c1_y, lx + lw, c1_y + c1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=c1_y + 24, text="FEATURE 01 · 실전 시험장 타이머", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=26)
    draw.text((lx + 24, c1_y + 54), "실제 한능검 시험과 100% 동일한 50문항 80분 OMR 카운트다운", font=get_font(17, 'bold'), fill=(15, 23, 42))
    desc1 = "실전 시험장에서 시간 부족으로 탈락하는 수험생의 페인포인트를 해결하기 위해\n문항별 권장 풀이 시간(1분 36초) 가이드와 종료 10분 전 OMR 마킹 경보 알림을 제공합니다.\n완벽한 모바일 터치 기반 5개 선지 선택과 실시간 점수 환산 엔진이 탑재되었습니다."
    draw.text((lx + 24, c1_y + 96), desc1, font=get_font(12, 'regular'), fill=(100, 116, 139), spacing=8)
    
    # Left Feature Card 2
    c2_y = 494
    c2_h = 240
    draw.rounded_rectangle([lx, c2_y, lx + lw, c2_y + c2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=c2_y + 24, text="FEATURE 02 · 50:50 확률 찬스", font=get_font(10.5, 'bold'), theme='amber', pad_x=12, height=26)
    draw.text((lx + 24, c2_y + 54), "헷갈리는 오답 선지 2개를 즉시 소거하는 추론 훈련 찬스", font=get_font(17, 'bold'), fill=(15, 23, 42))
    desc2 = "수험생이 두 개의 선지를 두고 마지막까지 고민하는 실전 딜레마를 해결합니다.\n오답 확률이 높은 함정 선지 2개를 시각적으로 블러/취소선 처리하여\n남은 선지 사이의 핵심 역사적 차이점을 비교 분석할 수 있도록 유도합니다."
    draw.text((lx + 24, c2_y + 96), desc2, font=get_font(12, 'regular'), fill=(100, 116, 139), spacing=8)
    
    # Left Feature Card 3 (Bottom KPI)
    c3_y = 754
    c3_h = 160
    draw.rounded_rectangle([lx, c3_y, lx + lw, c3_y + c3_h], radius=16, fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw.text((lx + 24, c3_y + 24), "실전 기출 데이터베이스 & 텔레메트리 연동", font=get_font(15, 'bold'), fill=(29, 78, 216))
    draw.text((lx + 24, c3_y + 56), "• 최신 77회 한능검 심화 포함 1,500문항 기출 DB 전면 내장 (오프라인 100% 구동)\n• 수험생 1회 평균 풀이 시간 : 52분 18초 (실전 대비 28분 단축 성과 검증)\n• 50:50 찬스 사용 문항의 최종 정답률 : 84.6% 달성", font=get_font(11.5, 'medium'), fill=(30, 58, 138), spacing=6)
    
    # RIGHT: DUAL PHONE MOCKUPS (Quiz screen & Exam Center)
    rx1 = 820
    rx2 = 1320
    py = 234
    pw = 430
    
    screen_quiz = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_03_quiz.png'
    screen_exam = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_02_exam.png'
    
    if os.path.exists(screen_quiz):
        im1 = Image.open(screen_quiz).convert('RGBA')
        cur_ph1 = int(round(pw * (im1.height / im1.width)))
        im1 = im1.resize((pw, cur_ph1), Image.Resampling.LANCZOS)
        base.paste(im1, (rx1, py), im1)
        draw_pill_badge(draw, rx1 + pw//2, py + cur_ph1 + 16, "실전 50제 문제 풀이 (50:50 찬스)", font=get_font(11, 'bold'), pad_x=12, height=26)
        
    if os.path.exists(screen_exam):
        im2 = Image.open(screen_exam).convert('RGBA')
        cur_ph2 = int(round(pw * (im2.height / im2.width)))
        im2 = im2.resize((pw, cur_ph2), Image.Resampling.LANCZOS)
        base.paste(im2, (rx2, py), im2)
        draw_pill_badge(draw, rx2 + pw//2, py + cur_ph2 + 16, "기출 시험 센터 (회차별 80분)", font=get_font(11, 'bold'), pad_x=12, height=26)
        
    draw_slide_footer(draw, 8)
    base.save(f'{OUT_DIR}/slide_08.png')
    print("SAVED slide_08.png (Korea History Core Feature 01)")


def make_slide_09():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=9, 
        category_en="CORE FEATURE 02 | 사료 단서 식별 & 스마트 오답 볼트", 
        title_black="사료 속 결정적 키워드 형광펜과 ", 
        title_blue="취약점을 자동 박멸하는 오답 볼트예요.", 
        subtitle_kr="한문·초서 고문헌 사료에서 정답의 실마리가 되는 키워드를 직관적으로 하이라이트하고, 틀린 문제를 시대별·유형별로 자동 분류하는 복습 엔진입니다.",
        right_badge=("SMART VAULT 100%", "blue")
    )
    
    lx = 100
    lw = 680
    
    # Left Feature Card 1
    c1_y = 234
    c1_h = 240
    draw.rounded_rectangle([lx, c1_y, lx + lw, c1_y + c1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=c1_y + 24, text="FEATURE 01 · 사료 단서 형광펜", font=get_font(10.5, 'bold'), theme='amber', pad_x=12, height=26)
    draw.text((lx + 24, c1_y + 54), "어려운 사료 원문에서 정답의 핵심 단서를 1초 만에 식별", font=get_font(17, 'bold'), fill=(15, 23, 42))
    desc1 = "수험생이 가장 두려워하는 생소한 사료 제시형 문항에 대응하여\n핵심 인물, 연호, 관직, 지명 등 시대 판별 키워드를 옐로우 형광펜 뱃지로 추출합니다.\n단순 해석 암기가 아닌 사료 독해 원리와 단서 포착 알고리즘을 체득하도록 돕습니다."
    draw.text((lx + 24, c1_y + 96), desc1, font=get_font(12, 'regular'), fill=(100, 116, 139), spacing=8)
    
    # Left Feature Card 2
    c2_y = 494
    c2_h = 240
    draw.rounded_rectangle([lx, c2_y, lx + lw, c2_y + c2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=c2_y + 24, text="FEATURE 02 · 스마트 오답 볼트", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=26)
    draw.text((lx + 24, c2_y + 54), "원터치 자동 인덱싱 & 취약 시대 타겟 재응시 루프", font=get_font(17, 'bold'), fill=(15, 23, 42))
    desc2 = "문제를 푸는 즉시 오답이 발생하면 스마트 오답 볼트에 자동 태깅됩니다.\n선사, 삼국, 고려, 조선, 근대, 현대사 중 수험생의 취약 시대를 레이더 차트로 시각화하고,\n오답만 골라 10문항씩 무한 반복 재응시할 수 있는 복습 트레이닝을 지원합니다."
    draw.text((lx + 24, c2_y + 96), desc2, font=get_font(12, 'regular'), fill=(100, 116, 139), spacing=8)
    
    # Left Feature Card 3
    c3_y = 754
    c3_h = 160
    draw.rounded_rectangle([lx, c3_y, lx + lw, c3_y + c3_h], radius=16, fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw.text((lx + 24, c3_y + 24), "에빙하우스 망각곡선 주기 복습 엔진", font=get_font(15, 'bold'), fill=(29, 78, 216))
    draw.text((lx + 24, c3_y + 56), "• 1일 후, 3일 후, 7일 후 최적 복습 시점 스마트 푸시 알림\n• 오답 재응시 통과율 : 91.2% (단순 오답 노트 작성 대비 암기 유지율 3.4배 상승)\n• 전 선지(①~⑤) 오답 이유 1:1 맞춤형 팩트 체크 코멘터리", font=get_font(11.5, 'medium'), fill=(30, 58, 138), spacing=6)
    
    # RIGHT: DUAL PHONE MOCKUPS (Commentary screen & Notes vault)
    rx1 = 820
    rx2 = 1320
    py = 234
    pw = 430
    
    screen_comm = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_04_commentary.png'
    screen_note = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_06_notes.png'
    
    if os.path.exists(screen_comm):
        im1 = Image.open(screen_comm).convert('RGBA')
        cur_ph1 = int(round(pw * (im1.height / im1.width)))
        im1 = im1.resize((pw, cur_ph1), Image.Resampling.LANCZOS)
        base.paste(im1, (rx1, py), im1)
        draw_pill_badge(draw, rx1 + pw//2, py + cur_ph1 + 16, "정답 사료 해설 & 단서 하이라이트", font=get_font(11, 'bold'), pad_x=12, height=26)
        
    if os.path.exists(screen_note):
        im2 = Image.open(screen_note).convert('RGBA')
        cur_ph2 = int(round(pw * (im2.height / im2.width)))
        im2 = im2.resize((pw, cur_ph2), Image.Resampling.LANCZOS)
        base.paste(im2, (rx2, py), im2)
        draw_pill_badge(draw, rx2 + pw//2, py + cur_ph2 + 16, "오답 정복 트레이닝 허브", font=get_font(11, 'bold'), pad_x=12, height=26)
        
    draw_slide_footer(draw, 9)
    base.save(f'{OUT_DIR}/slide_09.png')
    print("SAVED slide_09.png (Korea History Core Feature 02)")


def make_slide_10():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=10, 
        category_en="MOBILE SCREENS | 6대 상용 프로덕션 화면 쇼케이스", 
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
        category_en="BUSINESS IMPACT & STAR RETROSPECTIVE | 정량적 성과 및 시니어 회고", 
        title_black="수험생 완주율 78.4%와 0.4초 로딩, ", 
        title_blue="실측 데이터로 검증된 에듀테크 프로덕트 가치예요.", 
        subtitle_kr="1,500문항 기출 풀이 텔레메트리 데이터 분석과 4대 핵심 지표 및 STAR 기법 기반 프로덕트 엔지니어링 회고입니다.",
        right_badge=("EDUTECH TELEMETRY 100%", "green")
    )
    
    card_y = 234
    card_h = 320
    card_w = 840
    
    # Left Card: Before (두꺼운 문제집 수동 학습)
    cx1 = 100
    draw.rounded_rectangle([cx1, card_y, cx1 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(254, 202, 202), width=1)
    draw.rounded_rectangle([cx1, card_y + 14, cx1 + 5, card_y + card_h - 14], radius=3, fill=(239, 68, 68))
    
    draw_pill_badge(draw, left_x=cx1 + 24, cy=card_y + 24, text="BEFORE : TRADITIONAL PAPER STUDY", font=get_font(9.5, 'bold'), theme='red', has_dot=True, pad_x=10, height=22)
    draw.text((cx1 + 24, card_y + 50), "종이 문제집과 분권 사료집의 높은 학습 피로", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((cx1 + 24, card_y + 76), "무거운 책 지참 필요, 채점 및 오답 노트 수기 작성으로 하루 2시간 낭비", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    b_rows = [
        ("학습 접근성", "출퇴근길 지하철에서 두꺼운 기출 문제집 펼치기 불가", (15, 23, 42)),
        ("오답 정리 소요", "오답 문제 가위질 및 노트 풀칠 정리로 일평균 110분 소요", (220, 38, 38)),
        ("사료 독해 훈련", "해설지 텍스트를 단순 눈으로 훑어 실전 사료 변형에 취약", (15, 23, 42)),
        ("모의고사 완주율", "50문항 풀이 중 시간 안배 실패로 시험장 완주율 38.2% 불과", (180, 83, 9))
    ]
    ry = card_y + 115
    for title, val, color in b_rows:
        draw.text((cx1 + 24, ry), title, font=get_font(11, 'bold'), fill=(100, 116, 139))
        draw.text((cx1 + 24, ry + 18), val, font=get_font(12, 'bold'), fill=color)
        ry += 48
        
    # Right Card: After (대한국사 모바일 에듀테크)
    cx2 = 980
    draw.rounded_rectangle([cx2, card_y, cx2 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.rounded_rectangle([cx2, card_y + 14, cx2 + 5, card_y + card_h - 14], radius=3, fill=(37, 99, 235))
    
    draw_pill_badge(draw, left_x=cx2 + 24, cy=card_y + 24, text="AFTER : DAEHANGUKSA EDUTECH", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=10, height=22)
    draw.text((cx2 + 24, card_y + 50), "자투리 10분 모바일 완결 & 취약 시대 타겟 정복", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((cx2 + 24, card_y + 76), "10문항 숏폼, 1초 자동 오답 인덱싱, 사료 단서 형광펜으로 학습 효율 340% 향상", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    a_rows = [
        ("학습 접근성", "스마트폰 하나로 언제 어디서나 1,500문항 오프라인 100% 응시", (37, 99, 235)),
        ("오답 정리 소요", "틀린 즉시 자동 인덱싱 오답 볼트 탑재 (정리 시간 0초)", (22, 163, 74)),
        ("사료 독해 훈련", "키워드 형광펜 하이라이트 & 50:50 찬스로 사료 추론력 극대화", (37, 99, 235)),
        ("모의고사 완주율", "80분 공인 OMR 타이머 훈련으로 실전 모의고사 완주율 78.4% 달성", (22, 163, 74))
    ]
    ry = card_y + 115
    for title, val, color in a_rows:
        draw.text((cx2 + 24, ry), title, font=get_font(11, 'bold'), fill=(100, 116, 139))
        draw.text((cx2 + 24, ry + 18), val, font=get_font(12, 'bold'), fill=color)
        ry += 48
        
    # BOTTOM RETROSPECTIVE: STAR METHOD CARDS
    sy = 580
    sh = 350
    draw.rounded_rectangle([100, sy, 1820, sy + sh], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=124, cy=sy + 26, text="SENIOR UX RETROSPECTIVE · STAR METHOD", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=26)
    draw.text((124, sy + 58), "기술적 도전과 문제 해결 과정 (STAR 기법 200자 심층 회고)", font=get_font(18, 'bold'), fill=(15, 23, 42))
    
    star_items = [
        ("S", "Situation (상황)", "한능검 수험생은 5,000년의 방대한 역사와 사료 암기에 압도되어 중도 포기율이 40%에 달했습니다. 특히 이동 중 학습 시 책을 펼칠 수 없어 자투리 시간이 버려지는 문제가 있었습니다.", (239, 68, 68)),
        ("T", "Task (과제)", "지하철이나 버스 안에서도 한 손으로 50문항 실전 모의고사와 10문항 숏폼을 풀 수 있는 60FPS 플러터 네이티브 앱과 오프라인 SQLite 기반 고성능 사료 뷰어를 구축해야 했습니다.", (245, 158, 11)),
        ("A", "Action (실행)", "태극 헤리티지 디자인 토큰(#1D4ED8, #E11D48)을 정립하고, 사료 키워드 형광펜 식별 및 50:50 찬스 인터랙션을 개발했습니다. 또한 오답 자동 인덱싱 볼트와 시대별 레이더를 설계했습니다.", (37, 99, 235)),
        ("R", "Result (결과)", "콜드 스타트 0.4초, 모의고사 완주율 78.4%, 오답 재응시 통과율 91.2%를 기록하며 수험생의 단기 1급 합격을 지원하는 완성도 높은 에듀테크 상용 제품을 완성했습니다.", (16, 185, 129))
    ]
    
    sx = 124
    sw = 400
    gap = 20
    for idx, (letter, title, desc, color) in enumerate(star_items):
        cur_x = sx + idx * (sw - 20 + gap)
        draw.rounded_rectangle([cur_x, sy + 96, cur_x + sw - 20, sy + sh - 24], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.ellipse([cur_x + 16, sy + 112, cur_x + 44, sy + 140], fill=color)
        draw.text((cur_x + 30, sy + 126), letter, font=get_font(13, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((cur_x + 52, sy + 126), title, font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        lines = wrap_text_by_words(desc, get_font(11, 'regular'), sw - 56, draw)
        ly = sy + 154
        for l in lines:
            draw.text((cur_x + 16, ly), l, font=get_font(11, 'regular'), fill=(71, 85, 105))
            ly += 20
            
    draw_slide_footer(draw, 11)
    base.save(f'{OUT_DIR}/slide_11.png')
    print("SAVED slide_11.png (Korea History Telemetry & STAR Retrospective)")


def make_slide_12():
    # 1. Premium Obsidian Dark Background (#0B0F17)
    base = Image.new('RGBA', (W, H), (11, 15, 23, 255))
    draw = ImageDraw.Draw(base)
    
    # 2. Dark Header
    draw_slide_header(
        draw, 
        slide_num=12, 
        category_en="LIVE INTERACTIVE PROTOTYPE | 60FPS 플러터 웹 프로토타입", 
        title_black="실제 앱을 조작하듯, ", 
        title_blue="대한국사 실전 시험 엔진을 직접 조작해 보세요.", 
        subtitle_kr="정적인 화면을 넘어 뷰포트에서 50문항 실전 모의고사, OMR 인터랙션, 시대별 마스터 노트를 직접 터치하고 검증할 수 있는 인터랙티브 허브입니다.",
        right_badge=("LIVE ENGINE READY", "green"),
        dark_mode=True
    )
    
    # ---------------------------------------------------------
    # LEFT: DUAL 3D LAYERED MOCKUP SHOWCASE (x=100 to 760, w=660)
    # ---------------------------------------------------------
    phone_voice_path = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_03_quiz.png'
    phone_target_path = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/iphone_mockups/screen_01_home.png'
    
    if os.path.exists(phone_voice_path) and os.path.exists(phone_target_path):
        im_voice = Image.open(phone_voice_path).convert('RGBA')
        ph_back = 570
        pw_back = int(round(ph_back * (im_voice.width / im_voice.height)))
        im_voice = im_voice.resize((pw_back, ph_back), Image.Resampling.LANCZOS)
        
        im_target = Image.open(phone_target_path).convert('RGBA')
        ph_front = 610
        pw_front = int(round(ph_front * (im_target.width / im_target.height)))
        im_target = im_target.resize((pw_front, ph_front), Image.Resampling.LANCZOS)
        
        # Gorgeous Neon Glow & Shadows on Dark Background
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([110, 230, 130 + pw_back + 40, 254 + ph_back + 30], fill=(0, 60, 180, 50))
        shd.rounded_rectangle([130 + 10, 254 + 15, 130 + pw_back - 10, 254 + ph_back + 20], radius=32, fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(24))
        base = Image.alpha_composite(base, sh)
        base.paste(im_voice, (130, 254), im_voice)
        
        # Front phone glow
        sh2 = Image.new('RGBA', (W, H), (0,0,0,0))
        shd2 = ImageDraw.Draw(sh2)
        shd2.ellipse([340 - 30, 234 + ph_front - 40, 340 + pw_front + 30, 234 + ph_front + 50], fill=(0, 110, 255, 90))
        shd2.rounded_rectangle([340 + 12, 234 + 16, 340 + pw_front - 12, 234 + ph_front + 24], radius=36, fill=(0, 0, 0, 180))
        sh2 = sh2.filter(ImageFilter.GaussianBlur(28))
        base = Image.alpha_composite(base, sh2)
        base.paste(im_target, (340, 234), im_target)
        
        draw = ImageDraw.Draw(base)
    
    # Left Bottom Spec Strip (x=100, y=856, w=660, h=124) - Dark Glass Card
    draw.rounded_rectangle([100, 856, 760, 980], radius=14, fill=(17, 24, 39, 255), outline=(40, 53, 72), width=1)
    draw_pill_badge(draw, left_x=120, cy=880, text="FLUTTER WEB PRODUCTION ENGINE", font=get_font(9, 'bold'), theme='blue', dark_mode=True, pad_x=8, height=20)
    draw.text((120, 908), "• 60fps Native Web CanvasKit / SkWasm 렌더링 파이프라인 탑재", font=get_font(11, 'medium'), fill=(203, 213, 225))
    draw.text((120, 930), "• 100% 온디바이스 퀀트 대수 역산 엔진 (외부 금융 API 무전송 보안)", font=get_font(11, 'medium'), fill=(203, 213, 225))
    draw.text((120, 952), "• 반응형 모바일 뷰포트 시뮬레이터 & URL 딥링크 상태 복원 완벽 지원", font=get_font(11, 'medium'), fill=(56, 189, 248))
    
    # ---------------------------------------------------------
    # RIGHT: MASTER LAUNCHER + 4 STEPS + TIP + QR CODE (x=800 to 1820, w=1020)
    # Visual Hierarchy (Top-Down):
    # 1. PRIMARY HERO (TOP): Radiant Blue-Cyan Gradient Master Launcher with Ambient Glow
    # 2. Secondary: 4 Subdued Step Cards (dark glass, muted slate badges, ghost outline buttons)
    # 3. Tertiary: Subtle inline guide hint (quiet text between steps and QR)
    # 4. Supporting: Dark QR Code Plate & Hyperlink Area
    # ---------------------------------------------------------
    rx = 800
    rw = 1020
    base_proto_url = os.environ.get("GITHUB_PAGES_BASE_URL", "https://koyotejw-ux.github.io/smart-dca/portfolio")
    proto_entry_url = f"{base_proto_url}/prototype.html"
    
    # ---------------------------------------------------------
    # 1. PRIMARY HERO (TOP): MASTER LAUNCHER with Iconic Blue Gradient (y=234 to 348, h=114)
    # ---------------------------------------------------------
    my = 234
    mh = 114
    master_box = [rx, my, rx + rw, my + mh]
    
    # 1-A. Radiant Blue Ambient Glow Behind Card
    m_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    m_glow_d = ImageDraw.Draw(m_glow)
    m_glow_d.rounded_rectangle([rx - 6, my - 2, rx + rw + 6, my + mh + 8], radius=24, fill=(0, 87, 255, 120))
    m_glow = m_glow.filter(ImageFilter.GaussianBlur(24))
    base = Image.alpha_composite(base, m_glow)
    
    # 1-B. Generate Vibrant 135-degree Blue-to-Cyan Linear Gradient Box
    t = np.linspace(0, 1, rw, endpoint=True, dtype=np.float32)
    r_arr = (0 * (1 - t) + 0 * t).astype(np.uint8)
    g_arr = (87 * (1 - t) + 195 * t).astype(np.uint8)
    b_arr = (255 * (1 - t) + 245 * t).astype(np.uint8)
    grad_arr = np.zeros((mh, rw, 4), dtype=np.uint8)
    grad_arr[:, :, 0] = r_arr
    grad_arr[:, :, 1] = g_arr
    grad_arr[:, :, 2] = b_arr
    grad_arr[:, :, 3] = 255
    grad_box = Image.fromarray(grad_arr, 'RGBA')
    
    grad_mask = Image.new('L', (rw, mh), 0)
    gmd = ImageDraw.Draw(grad_mask)
    gmd.rounded_rectangle([0, 0, rw - 1, mh - 1], radius=16, fill=255)
    
    base.paste(grad_box, (rx, my), grad_mask)
    draw = ImageDraw.Draw(base)
    
    # 1-C. Content Inside Radiant Gradient Card
    # High-contrast deep navy pill badge with white border and text
    badge_w = 145
    draw.rounded_rectangle([rx + 24, my + 14, rx + 24 + badge_w, my + 35], radius=10, fill=(0, 36, 110, 190), outline=(255, 255, 255, 180), width=1)
    draw.text((rx + 24 + badge_w // 2, my + 24), "MASTER LAUNCHER", font=get_font(9, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Hero White Headline
    draw.text((rx + 24, my + 57), "모바일 목업 디바이스에서 전체 플로우 직접 실행하기 ↗", font=get_font(18, 'extrabold'), fill=(255, 255, 255), anchor='lm')
    # Hero Subtitle
    draw.text((rx + 24, my + 87), "50문항 실전 모의고사부터 사료 단서 식별까지, 4대 핵심 여정을 실물 뷰포트에서 한 번에 체험하세요.", font=get_font(12, 'medium'), fill=(225, 242, 255), anchor='lm')
    
    # Large High-Contrast Pure White CTA Button
    btn_w = 210
    btn_h = 48
    btn_rx = rx + rw - btn_w - 24
    btn_ry = my + (mh - btn_h) // 2
    
    # Button soft drop shadow
    sh_btn = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_btn_d = ImageDraw.Draw(sh_btn)
    sh_btn_d.rounded_rectangle([btn_rx - 2, btn_ry + 2, btn_rx + btn_w + 2, btn_ry + btn_h + 8], radius=24, fill=(0, 40, 120, 100))
    sh_btn = sh_btn.filter(ImageFilter.GaussianBlur(8))
    base = Image.alpha_composite(base, sh_btn)
    draw = ImageDraw.Draw(base)
    
    # Pure white button with electric blue text
    draw.rounded_rectangle([btn_rx, btn_ry, btn_rx + btn_w, btn_ry + btn_h], radius=24, fill=(255, 255, 255))
    draw.text((btn_rx + btn_w // 2, btn_ry + btn_h // 2), "RUN PROTOTYPE ↗", font=get_font(13.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # ---------------------------------------------------------
    # 2. 4 SUBDUED STEP CARDS (y=358 to 678, h=74, sgap=8)
    # ---------------------------------------------------------
    steps = [
        (
            "STEP 01", "01. 자산 현황 진단 대시보드",
            "학습 진도율 및 D-Day 설정 · 출석 스트릭 및 6대 시대별 마스터리 레이더 점검",
            f"{proto_entry_url}?flow=home"
        ),
        (
            "STEP 02", "02. 한능검 50제 실전 기출 센터",
            "긴박한 하락장에서 말로 빠르게 입력하는 온디바이스 음성 바텀시트 모달 조작",
            f"{proto_entry_url}?flow=voice"
        ),
        (
            "STEP 03", "03. 50:50 찬스 & 사료 단서 판독",
            "탈출 희망 가격 입력 시 필요 수량과 소요 자금을 0.00% 오차로 즉시 역산 산출",
            f"{proto_entry_url}?flow=target"
        ),
        (
            "STEP 04", "04. 최종 플랜 확정 & 안전 계좌 진단",
            "틀린 문제 원터치 자동 인덱싱 · 취약 시대 선별 숏폼 재응시 및 오답 박멸",
            f"{proto_entry_url}?flow=sim"
        )
    ]
    
    sy = 358
    sh_h = 74
    sgap = 8
    step_boxes = []
    
    for badge, title, desc, url in steps:
        box_rect = [rx, sy, rx + rw, sy + sh_h]
        step_boxes.append((box_rect, url))
        
        # Subdued Dark Glass Box (No bright stripes)
        draw.rounded_rectangle(box_rect, radius=12, fill=(15, 20, 32, 230), outline=(32, 42, 58), width=1)
        
        # Muted Dark Slate Badge (Uniform and quiet)
        draw_pill_badge(draw, left_x=rx + 18, cy=sy + 22, text=badge, font=get_font(9, 'bold'), theme='slate', dark_mode=True, has_dot=False, pad_x=8, height=20)
        draw.text((rx + 90, sy + 22), title, font=get_font(13.5, 'bold'), fill=(226, 232, 240), anchor='lm')
        draw.text((rx + 18, sy + 52), desc, font=get_font(11, 'regular'), fill=(105, 120, 140), anchor='lm')
        
        # Right Click Button - Subtle Ghost Outline Pill (Secondary)
        btn_x = rx + rw - 120
        draw_pill_badge(draw, cx=btn_x + 45, cy=sy + 37, text="바로가기 ↗", font=get_font(10.5, 'bold'), theme='slate', dark_mode=True, has_dot=False, pad_x=12, height=28)
        
        sy += sh_h + sgap
        
    # ---------------------------------------------------------
    # 3. TERTIARY: Subtle, Un-emphasized Guide Hint
    # ---------------------------------------------------------
    draw.text((rx + 4, 696), "TIP · 특정 단계만 개별 테스트하거나, 모바일 실물 기기에서는 아래 QR 코드를 카메라로 스캔하세요.", font=get_font(11.5, 'regular'), fill=(115, 130, 150), anchor='lm')
    
    # ---------------------------------------------------------
    # 4. SUPPORTING: Dark QR Code & Hyperlink Area (y=716 to 970, h=254)
    # ---------------------------------------------------------
    qy = 716
    qh = 254
    draw.rounded_rectangle([rx, qy, rx + rw, qy + qh], radius=14, fill=(14, 19, 30, 255), outline=(32, 42, 58), width=1)
    
    draw_pill_badge(draw, left_x=rx + 24, cy=qy + 28, text="HYPERLINK & MOBILE QR SCAN", font=get_font(9, 'bold'), theme='slate', has_dot=True, dark_mode=True, pad_x=8, height=20)
    draw.text((rx + 24, qy + 64), "• PDF 원클릭 하이퍼링크 : PDF 뷰어에서 각 카드나 버튼 클릭 시 반응형 프로토타입 즉시 실행", font=get_font(11.5, 'medium'), fill=(180, 195, 215))
    draw.text((rx + 24, qy + 94), "• 스마트폰 실물 QR 스캔 : 스마트폰 기본 카메라로 우측 QR 코드 스캔 시 모바일 전용 뷰 작동", font=get_font(11.5, 'medium'), fill=(180, 195, 215))
    draw.text((rx + 24, qy + 124), "• GitHub Pages 상시 배포 : 전 세계 어디서든 무설치로 60fps 플러터 엔진 즉각 체험 가능", font=get_font(11.5, 'medium'), fill=(56, 189, 248))
    draw.text((rx + 24, qy + 160), f"Live Web : {proto_entry_url}", font=get_num_font(11, 'bold'), fill=(130, 145, 170))
    
    # Generate High-Contrast QR Code on Crisp White Plate
    qr_url = proto_entry_url
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=4,
        border=1,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=(11, 15, 23), back_color=(255, 255, 255)).convert('RGBA')
    qr_size = 144
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST)
    
    qr_x = rx + rw - qr_size - 28
    qr_y = qy + 24
    
    draw.rounded_rectangle([qr_x - 8, qr_y - 6, qr_x + qr_size + 8, qr_y + qr_size + 28], radius=10, fill=(255, 255, 255))
    base.paste(qr_img, (qr_x, qr_y), qr_img)
    draw.text((qr_x + qr_size // 2, qr_y + qr_size + 10), "SCAN FOR MOBILE TEST", font=get_font(8.5, 'bold'), fill=(11, 15, 23), anchor='mm')
    
    draw_slide_footer(draw, 12, dark_mode=True)
    base.save(f'{OUT_DIR}/slide_12.png')
    print("SAVED slide_12.png (High-Hierarchy Live Interactive Prototype Hub with Blue Gradient Master Launcher at Top)")
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
