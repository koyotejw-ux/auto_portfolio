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
        category_en="TARGET & PERSONA | SEGMENTATION MATRIX & BENCHMARK", 
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
    
    draw_slide_header(
        draw, 
        slide_num=4, 
        category_en="INFORMATION ARCHITECTURE · 5대 핵심 메뉴 구조", 
        title_black="수험생이 한눈에 파악하는 ", 
        title_blue="5대 합격 학습 내비게이션", 
        subtitle_kr="홈·학습관·시험센터·오답노트·설정 5대 핵심 바텀 내비게이션 기반 한 손 완결형 정보 아키텍처"
    )
    
    # Top-Right Badge
    top_badge_x = 1480
    top_badge_y = 65
    draw.rounded_rectangle([top_badge_x, top_badge_y, top_badge_x + 340, top_badge_y + 60], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=top_badge_x + 16, cy=top_badge_y + 30, text="서비스 구성", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=24)
    draw.text((top_badge_x + 110, top_badge_y + 20), "5대 메인 탭", font=get_font(12, 'bold'), fill=(15, 23, 42))
    draw.text((top_badge_x + 110, top_badge_y + 38), "Flutter IndexedStack 구조", font=get_font(10, 'regular'), fill=(100, 116, 139))
    
    # 5 Tab Columns
    cols_data = [
        ("01. 홈 대시보드", "종합 학습 관제", "출석 스트릭, D-Day, 오늘의 추천 기출 및 시대별 정답률 레이더", [
            ("스트릭 카드", "연속 출석 달성", "매일 이어지는 학습 습관과 잔여 목표 일수 확인", False),
            ("추천 기출", "1-Tap 즉시 응시", "최신 77회 심화 기출 및 추천 숏폼 바로가기", True),
            ("마스터리 레이더", "시대별 완성도", "6대 시대별 취약 영역과 정답률 실시간 분석", False)
        ], (29, 78, 216)),
        ("02. 학습관 (서고)", "시대별 사료 바이블", "선사부터 현대사까지 6대 시대별 핵심 요약 노트 및 고해상도 유물 도감", [
            ("시대별 요약관", "6대 시대 마스터", "선사·삼국·고려·조선·근대·현대사 핵심 정리", True),
            ("유물 갤러리", "시각 사료 도감", "시험 빈출 국보·보물 유물 고화질 사진 및 해설", False),
            ("사료 힌트 바이블", "빈출 키워드", "사료 속 인물·연호·관직·지명 핵심 단서 사전", False)
        ], (217, 119, 6)),
        ("03. 실전 시험 센터", "공인 기출 모의고사", "최신 77회 한능검 심화 50문항 실전 응시, 80분 OMR 타이머, 숏폼 10제", [
            ("77회 실전 응시", "50문항 80분", "실제 시험지와 100% 동일한 배점 및 OMR 카운트다운", True),
            ("랜덤 50제", "전 범위 무작위", "1,500제 기출 풀에서 무작위 50문항 추출 모의고사", False),
            ("10문항 숏폼", "자투리 10분", "출퇴근길 5분 만에 푸는 핵심 기출 압축 테스트", True)
        ], (225, 29, 72)),
        ("04. 스마트 오답 볼트", "취약점 자동 인덱싱", "틀린 문제 1초 만에 자동 분류, 에빙하우스 망각곡선 주기 복습, 1:1 해설", [
            ("오답 보관함", "자동 인덱싱", "틀린 문제의 문항 번호, 시대, 정답률 자동 태깅", True),
            ("AI 취약 트레이닝", "오답만 골라 풀기", "누적된 오답 중 취약 시대만 선별하여 즉시 재도전", True),
            ("사료 단서 형광펜", "정답 키워드 식별", "오답 문제 사료 속 결정적 정답 키워드 형광펜 분석", False)
        ], (5, 150, 105)),
        ("05. 수험 환경 설정", "학습 편의 커스텀", "목표 급수 설정, 시험 D-Day 카운트다운, 음성 낭독 속도, OLED 다크 테마", [
            ("목표 급수 관리", "1급/2급/3급", "목표 급수별 커트라인 및 시험 일정 자동 동기화", False),
            ("오디오 낭독 설정", "TTS 배속 조절", "사료 및 해설 음성 낭독 재생 속도(1.0x~2.0x) 설정", False),
            ("OLED 다크 테마", "야간 학습 배려", "어두운 독서실 및 이동 중 눈의 피로를 덜어주는 테마", True)
        ], (71, 85, 105))
    ]
    
    col_w = 328
    col_gap = 20
    sy = 234
    col_h = 700
    
    for c_idx, (t_name, t_sub, t_desc, sub_items, t_col) in enumerate(cols_data):
        cx = 100 + c_idx * (col_w + col_gap)
        draw.rounded_rectangle([cx, sy, cx + col_w, sy + col_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Header Badge
        draw.rounded_rectangle([cx, sy, cx + col_w, sy + 70], radius=16, fill=(248, 250, 252))
        draw.rectangle([cx, sy + 54, cx + col_w, sy + 70], fill=(248, 250, 252))
        draw.line([(cx, sy + 70), (cx + col_w, sy + 70)], fill=(226, 232, 240), width=1)
        
        draw.text((cx + 18, sy + 18), t_name, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 18, sy + 42), t_sub, font=get_font(10.5, 'bold'), fill=t_col)
        
        # Tab Purpose Description
        draw.text((cx + 18, sy + 84), t_desc, font=get_font(9.5, 'regular'), fill=(100, 116, 139))
        draw.line([(cx + 18, sy + 130), (cx + col_w - 18, sy + 130)], fill=(241, 245, 249), width=1)
        
        # Sub Cards
        card_y = sy + 144
        card_h = 160
        for s_title, s_badge, s_detail, is_core in sub_items:
            card_bg = (238, 242, 255) if is_core and c_idx in [0, 2, 3] else (248, 250, 252)
            card_border = (199, 210, 254) if is_core and c_idx in [0, 2, 3] else (226, 232, 240)
            draw.rounded_rectangle([cx + 14, card_y, cx + col_w - 14, card_y + card_h], radius=10, fill=card_bg, outline=card_border, width=1)
            
            draw_pill_badge(draw, left_x=cx + 26, cy=card_y + 22, text=s_badge, font=get_font(8, 'bold'), theme='blue' if is_core else 'slate', pad_x=6, height=18)
            draw.text((cx + 26, card_y + 48), s_title, font=get_font(12, 'bold'), fill=(15, 23, 42))
            draw.text((cx + 26, card_y + 74), s_detail, font=get_font(9.5, 'regular'), fill=(71, 85, 105), spacing=4)
            card_y += card_h + 16
            
    draw_slide_footer(draw, 4)
    base.save(f'{OUT_DIR}/slide_04.png')
    print("SAVED new Slide 04 to both locations successfully!")


def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=5, 
        category_en="USER FLOW | SERVICE INTERACTION FLOWCHART", 
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
        category_en="WIREFRAME | MOBILE UX & ERGONOMIC ARCHITECTURE", 
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
    
    def draw_wireframe_chassis(draw_obj, px, title_text, theme_key):
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([px + 8, sec_y + 12, px + pw - 8, sec_y + ph + 16], radius=28, fill=(0, 0, 0, 30))
        sh_blur = sh.filter(ImageFilter.GaussianBlur(14))
        base.paste(sh_blur, (0, 0), sh_blur)
        
        draw.rounded_rectangle([px, sec_y, px + pw, sec_y + ph], radius=26, fill=(255, 255, 255), outline=(15, 23, 42), width=2)
        draw.rounded_rectangle([px + pw//2 - 40, sec_y + 10, px + pw//2 + 40, sec_y + 24], radius=7, fill=(15, 23, 42))
        draw_pill_badge(draw, left_x=px + 20, cy=sec_y + 38, text=title_text, font=get_font(8.5, 'bold'), theme=theme_key, pad_x=8, height=18)
        
    # --- Chassis 1: [SCR-01 · 홈 대시보드] ---
    draw_wireframe_chassis(draw, p1_x, "① SCR-01 · 홈 대시보드", "blue")
    
    # 1. Streak & Heart Header Card
    sc_y = sec_y + 56
    draw.rounded_rectangle([p1_x + 16, sc_y, p1_x + pw - 16, sc_y + 68], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((p1_x + 26, sc_y + 14), "연속 출석 스트릭", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((p1_x + 26, sc_y + 36), "7일 연속 달성 (D-28)", font=get_font(13, 'bold'), fill=(29, 78, 216))
    
    # 2. Main Exam Launcher Banner
    hb_y = sc_y + 80
    draw.rounded_rectangle([p1_x + 16, hb_y, p1_x + pw - 16, hb_y + 90], radius=10, fill=(29, 78, 216))
    draw.text((p1_x + 26, hb_y + 18), "제77회 심화 실전 모의고사", font=get_font(11, 'bold'), fill=(255, 255, 255))
    draw.text((p1_x + 26, hb_y + 40), "50문항 · 80분 타이머 · 실전 배점", font=get_font(9, 'regular'), fill=(191, 219, 254))
    draw.rounded_rectangle([p1_x + 26, hb_y + 60, p1_x + pw - 26, hb_y + 80], radius=6, fill=(255, 255, 255))
    draw.text((p1_x + pw//2, hb_y + 70), "지금 바로 응시하기 →", font=get_font(9.5, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    # 3. 2x2 Quick Action Grid
    qg_y = hb_y + 102
    q_items = [("기출 시험센터", "77회~50회"), ("오답 복습", "14문항 대기"), ("시대별 서고", "6대 시대 요약"), ("마스터리 통계", "정답률 레이더")]
    for qidx, (qname, qdesc) in enumerate(q_items):
        qcol = qidx % 2
        qrow = qidx // 2
        qx = p1_x + 16 + qcol * 128
        qy = qg_y + qrow * 56
        draw.rounded_rectangle([qx, qy, qx + 120, qy + 50], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((qx + 10, qy + 12), qname, font=get_font(9.5, 'bold'), fill=(15, 23, 42))
        draw.text((qx + 10, qy + 30), qdesc, font=get_font(8, 'medium'), fill=(100, 116, 139))
        
    # 4. Era Mastery Progress Card
    ep_y = qg_y + 122
    draw.rounded_rectangle([p1_x + 16, ep_y, p1_x + pw - 16, ep_y + 60], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((p1_x + 26, ep_y + 12), "조선 후기 정치사 정답률", font=get_font(9.5, 'bold'), fill=(15, 23, 42))
    draw.rounded_rectangle([p1_x + 26, ep_y + 34, p1_x + pw - 26, ep_y + 44], radius=5, fill=(241, 245, 249))
    draw.rounded_rectangle([p1_x + 26, ep_y + 34, p1_x + 180, ep_y + 44], radius=5, fill=(5, 150, 105))
    draw.text((p1_x + pw - 26, ep_y + 20), "68%", font=get_font(9.5, 'bold'), fill=(5, 150, 105), anchor='rm')
    
    # 5. Bottom Navigation Bar
    bn_y = sec_y + ph - 42
    draw.rounded_rectangle([p1_x + 8, bn_y, p1_x + pw - 8, bn_y + 34], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    b_icons = ["홈", "학습관", "시험센터", "오답노트", "설정"]
    for bidx, bname in enumerate(b_icons):
        bx = p1_x + 14 + bidx * 52
        draw.text((bx + 24, bn_y + 17), bname, font=get_font(8.5, 'bold' if bidx == 0 else 'medium'), fill=(29, 78, 216) if bidx == 0 else (100, 116, 139), anchor='mm')
        
    # --- Chassis 2: [SCR-02 · 실전 기출 시험 센터] ---
    draw_wireframe_chassis(draw, p2_x, "② SCR-02 · 실전 기출 센터", "red")
    
    # 1. Header Card with Timer Pill
    e_hc_y = sec_y + 56
    draw.rounded_rectangle([p2_x + 16, e_hc_y, p2_x + pw - 16, e_hc_y + 60], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p2_x + 24, cy=e_hc_y + 20, text="실전 50제", font=get_font(8, 'bold'), theme='red', pad_x=6, height=18)
    draw.text((p2_x + 95, e_hc_y + 20), "제77회 한능검 심화", font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((p2_x + 24, e_hc_y + 42), "국사편찬위원회 공인 실전 기출 문제 완비", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    # 2. Exam Action Cards (50제 vs 숏폼)
    ac1_y = e_hc_y + 72
    draw.rounded_rectangle([p2_x + 16, ac1_y, p2_x + pw - 16, ac1_y + 76], radius=10, fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw.text((p2_x + 26, ac1_y + 16), "77회 실전 응시 (50문항/80분)", font=get_font(11, 'bold'), fill=(29, 78, 216))
    draw.text((p2_x + 26, ac1_y + 36), "실제 시험장과 100% 동일한 OMR 타이머", font=get_font(9, 'regular'), fill=(71, 85, 105))
    draw.rounded_rectangle([p2_x + pw - 80, ac1_y + 24, p2_x + pw - 24, ac1_y + 54], radius=6, fill=(29, 78, 216))
    draw.text((p2_x + pw - 52, ac1_y + 39), "응시", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    ac2_y = ac1_y + 86
    draw.rounded_rectangle([p2_x + 16, ac2_y, p2_x + pw - 16, ac2_y + 76], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p2_x + 26, ac2_y + 16), "10문항 숏폼 모의고사 (10분)", font=get_font(11, 'bold'), fill=(15, 23, 42))
    draw.text((p2_x + 26, ac2_y + 36), "출퇴근 자투리 시간에 푸는 핵심 기출", font=get_font(9, 'regular'), fill=(100, 116, 139))
    draw.rounded_rectangle([p2_x + pw - 80, ac2_y + 24, p2_x + pw - 24, ac2_y + 54], radius=6, fill=(15, 23, 42))
    draw.text((p2_x + pw - 52, ac2_y + 39), "숏폼", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # 3. Exam Center List (76회, 75회, 74회...)
    ls_y = ac2_y + 88
    draw.text((p2_x + 20, ls_y + 4), "역대 심화 기출 회차 선택", font=get_font(10, 'bold'), fill=(15, 23, 42))
    ex_list = [("제76회 심화 기출", "2024년 10월", "86점"), ("제75회 심화 기출", "2024년 8월", "미응시")]
    for lidx, (lname, ldate, lscore) in enumerate(ex_list):
        ly = ls_y + 20 + lidx * 48
        draw.rounded_rectangle([p2_x + 16, ly, p2_x + pw - 16, ly + 40], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((p2_x + 26, ly + 14), lname, font=get_font(9.5, 'bold'), fill=(15, 23, 42))
        draw.text((p2_x + 130, ly + 14), ldate, font=get_font(8.5, 'regular'), fill=(100, 116, 139))
        draw.text((p2_x + pw - 26, ly + 14), lscore, font=get_font(9, 'bold'), fill=(29, 78, 216) if "점" in lscore else (100, 116, 139), anchor='rm')
        
    # --- Chassis 3: [SCR-03 · 실전 문제 풀이 (50:50 찬스)] ---
    draw_wireframe_chassis(draw, p3_x, "③ SCR-03 · 문제 풀이 & 50:50", "amber")
    
    # 1. Timer & Chance Bar
    tb_y = sec_y + 56
    draw.rounded_rectangle([p3_x + 16, tb_y, p3_x + pw - 16, tb_y + 36], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p3_x + 24, cy=tb_y + 18, text="잔여 79:17", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18)
    draw.text((p3_x + 95, tb_y + 18), "제1문항 (2점)", font=get_font(9.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw_pill_badge(draw, left_x=p3_x + pw - 75, cy=tb_y + 18, text="50:50 찬스", font=get_font(8, 'bold'), theme='amber', pad_x=6, height=18)
    
    # 2. Passage Card with Keyword Highlight
    ps_y = tb_y + 44
    draw.rounded_rectangle([p3_x + 16, ps_y, p3_x + pw - 16, ps_y + 110], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((p3_x + 24, ps_y + 12), "밑줄 그은 '이 시대'의 생활 모습으로 옳은 것은?", font=get_font(9.5, 'bold'), fill=(15, 23, 42))
    draw.rounded_rectangle([p3_x + 24, ps_y + 36, p3_x + pw - 24, ps_y + 98], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p3_x + 30, ps_y + 44), "[제주 고산리 유적 체험 프로그램]", font=get_font(8, 'bold'), fill=(100, 116, 139))
    draw.text((p3_x + 30, ps_y + 60), "사우 해안과 해골이 발견된 빗살무늬 토기...", font=get_font(8, 'regular'), fill=(71, 85, 105))
    draw.rounded_rectangle([p3_x + 120, ps_y + 58, p3_x + 180, ps_y + 72], radius=3, fill=(254, 240, 138))
    draw.text((p3_x + 150, ps_y + 65), "빗살무늬 토기", font=get_font(7.5, 'bold'), fill=(133, 77, 14), anchor='mm')
    
    # 3. 5 Options with Green Circle Check
    op_y = ps_y + 118
    options = [
        ("①", "철제 무기로 정복 활동을 벌였다.", False, False),
        ("②", "소를 이용한 깊이갈이가 일반화되었다.", False, True),  # Blurred by 50:50
        ("③", "많은 인력을 동원하여 고인돌을 축조하였다.", False, True), # Blurred by 50:50
        ("④", "가락바퀴와 뼈바늘을 이용해 옷을 만들었다.", True, False),  # Correct
        ("⑤", "거푸집을 이용해 비파형 동검을 제작하였다.", False, False)
    ]
    for oidx, (onum, otxt, is_ans, is_elim) in enumerate(options):
        oy = op_y + oidx * 40
        obg = (240, 253, 244) if is_ans else ((248, 250, 252) if is_elim else (255, 255, 255))
        oborder = (187, 247, 208) if is_ans else ((226, 232, 240) if is_elim else (203, 213, 225))
        draw.rounded_rectangle([p3_x + 16, oy, p3_x + pw - 16, oy + 34], radius=6, fill=obg, outline=oborder, width=1)
        
        circle_col = (22, 163, 74) if is_ans else ((203, 213, 225) if is_elim else (100, 116, 139))
        draw.text((p3_x + 28, oy + 17), onum, font=get_font(9, 'bold'), fill=circle_col, anchor='lm')
        txt_col = (22, 101, 52) if is_ans else ((148, 163, 184) if is_elim else (15, 23, 42))
        draw.text((p3_x + 48, oy + 17), otxt, font=get_font(8, 'bold' if is_ans else 'regular'), fill=txt_col, anchor='lm')
        if is_elim:
            draw.line([(p3_x + 48, oy + 17), (p3_x + pw - 30, oy + 17)], fill=(244, 63, 94), width=1)
            
    # --- Chassis 4: [SCR-04 · 스마트 오답 볼트] ---
    draw_wireframe_chassis(draw, p4_x, "④ SCR-04 · 스마트 오답 볼트", "green")
    
    # 1. Incorrect Summary Hub Card
    ih_y = sec_y + 56
    draw.rounded_rectangle([p4_x + 16, ih_y, p4_x + pw - 16, ih_y + 80], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=p4_x + 24, cy=ih_y + 20, text="취약점 보관함", font=get_font(8, 'bold'), theme='red', pad_x=6, height=18)
    draw.text((p4_x + 95, ih_y + 20), "총 14문항 오답 보관 중", font=get_font(11, 'bold'), fill=(153, 27, 27), anchor='lm')
    draw.text((p4_x + 24, ih_y + 44), "가장 취약한 시대 : 조선 후기 정치사 (오답률 68%)", font=get_font(8.5, 'regular'), fill=(153, 27, 27))
    draw.rounded_rectangle([p4_x + 24, ih_y + 58, p4_x + pw - 24, ih_y + 74], radius=4, fill=(225, 29, 72))
    draw.text((p4_x + pw//2, ih_y + 66), "오답 14문항 즉시 재도전 풀기 →", font=get_font(8.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # 2. Incorrect List by Era
    il_y = ih_y + 92
    draw.text((p4_x + 20, il_y + 4), "시대별 취약 오답 목록", font=get_font(10, 'bold'), fill=(15, 23, 42))
    in_items = [
        ("조선 시대", "제77회 14번 · 대동법 시행 배경", "오답 선지 ③번 선택"),
        ("근대 개항기", "제77회 28번 · 갑신정변 14개조 혁신안", "오답 선지 ①번 선택"),
        ("현대사", "제76회 45번 · 6·15 남북 공동 선언", "오답 선지 ④번 선택")
    ]
    for iidx, (iera, ititle, idesc) in enumerate(in_items):
        iy = il_y + 20 + iidx * 64
        draw.rounded_rectangle([p4_x + 16, iy, p4_x + pw - 16, iy + 56], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=p4_x + 24, cy=iy + 16, text=iera, font=get_font(7, 'bold'), theme='slate', pad_x=5, height=16)
        draw.text((p4_x + 75, iy + 16), ititle, font=get_font(8.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((p4_x + 24, iy + 38), idesc, font=get_font(8, 'medium'), fill=(225, 29, 72))
        
    # 3. Ebbinghaus Review Scheduler Pill
    eb_y = il_y + 220
    draw.rounded_rectangle([p4_x + 16, eb_y, p4_x + pw - 16, eb_y + 46], radius=8, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw.text((p4_x + 24, eb_y + 14), "에빙하우스 주기 복습 알림", font=get_font(9, 'bold'), fill=(22, 101, 52))
    draw.text((p4_x + 24, eb_y + 30), "내일 오전 9시 취약 오답 5제 스마트 푸시 예약", font=get_font(8, 'regular'), fill=(21, 128, 61))
    
    # -------------------------------------------------------------
    # LOWER SECTION: ERGONOMIC THUMB-ZONE ARCHITECTURE (y=775 to 945)
    # -------------------------------------------------------------
    tz_y = 775
    tz_h = 170
    draw.rounded_rectangle([100, tz_y, 1820, tz_y + tz_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, left_x=124, cy=tz_y + 24, text="ERGONOMIC ARCHITECTURE", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((310, tz_y + 24), "인체공학적 엄지 조작 반경(Thumb-Zone) 및 정보 위계 설계", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    ez_cards = [
        ("상단 30% : 인지 관찰 존", "시각 정보 소비", "80분 OMR 잔여 타이머, 문항 배점(1·2·3점), 사료 본문 및 사진 유물을 배치하여 손가락 가림 없이 사료를 정밀 독해하도록 설계했습니다.", (100, 116, 139)),
        ("중단 30% : 인터랙션 존", "50:50 찬스 & 선지", "엄지가 가장 편안하게 닿는 중단 영역에 50:50 찬스 버튼과 5개 선지 카드를 배치하여 원터치 선택 및 소거법 추론을 지원합니다.", (29, 78, 216)),
        ("하단 40% : 원핸드 액션 존", "이동 및 오답 인덱싱", "이전/다음 문항 이동 플로팅 버튼, OMR 마킹 시트 호출, 해설 보기, 5대 메인 바텀 내비게이션을 한 손 엄지로 100% 조작할 수 있습니다.", (5, 150, 105))
    ]
    ew = (1720 - 40) // 3
    for eidx, (etitle, ebadge, edesc, ecol) in enumerate(ez_cards):
        ex = 124 + eidx * (ew + 20)
        draw.rounded_rectangle([ex, tz_y + 54, ex + ew, tz_y + tz_h - 18], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=ex + 16, cy=tz_y + 72, text=ebadge, font=get_font(8, 'bold'), theme='blue' if ecol == (29, 78, 216) else ('green' if ecol == (5, 150, 105) else 'slate'), pad_x=6, height=18)
        draw.text((ex + 16, tz_y + 98), etitle, font=get_font(11.5, 'bold'), fill=(15, 23, 42))
        lines = wrap_text_by_words(edesc, get_font(9.5, 'regular'), ew - 32, draw)
        ly = tz_y + 118
        for l in lines:
            draw.text((ex + 16, ly), l, font=get_font(9.5, 'regular'), fill=(71, 85, 105))
            ly += 17
            
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
