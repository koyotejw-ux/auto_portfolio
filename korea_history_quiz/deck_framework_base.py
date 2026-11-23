# -*- coding: utf-8 -*-
"""
Full, production-grade Behance slide generator for 대한국사 (Korea History Quiz).
Mirrors 100% of the visual density, layout structure, 3-column hero showcases,
telemetry grids, and editorial aesthetic of Smart DCA, while infusing authentic
대한국사 UX/UI content, real production screenshots, and Taegeuk Heritage design tokens.
"""

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
        cur_line = ''
        for w in words:
            test_line = (cur_line + ' ' + w).strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                cur_line = test_line
            else:
                if cur_line:
                    lines.append(cur_line)
                cur_line = w
        if cur_line:
            lines.append(cur_line)
    return lines

THEME_STYLES = {
    'blue':  {'bg': (240, 246, 255), 'border': (191, 219, 254), 'text': (29, 78, 216), 'dot': (29, 78, 216)},
    'cyan':  {'bg': (236, 254, 255), 'border': (165, 243, 252), 'text': (8, 145, 178), 'dot': (8, 145, 178)},
    'green': {'bg': (240, 253, 244), 'border': (187, 247, 208), 'text': (22, 101, 52), 'dot': (22, 163, 74)},
    'amber': {'bg': (254, 243, 199), 'border': (253, 230, 138), 'text': (146, 64, 14), 'dot': (217, 119, 6)},
    'red':   {'bg': (254, 242, 242), 'border': (254, 202, 202), 'text': (153, 27, 27), 'dot': (225, 29, 72)},
    'slate': {'bg': (248, 250, 252), 'border': (226, 232, 240), 'text': (71, 85, 105), 'dot': (100, 116, 139)},
    'purple':{'bg': (250, 245, 255), 'border': (233, 213, 255), 'text': (107, 33, 168), 'dot': (147, 51, 234)}
}

def draw_pill_badge(draw, cx=None, cy=None, text="", font=None, theme='blue', has_dot=False, pad_x=10, height=22, left_x=None, dark_mode=False):
    if font is None:
        font = get_font(9.5, 'bold')
    st = THEME_STYLES.get(theme, THEME_STYLES['blue'])
    bg_col = st['bg']
    border_col = st['border']
    txt_col = st['text']
    dot_col = st['dot']
    
    if dark_mode:
        bg_col = (20, 27, 45, 220)
        border_col = (40, 55, 85, 255)
        txt_col = (148, 163, 184)
        dot_col = (59, 130, 246)
        
    dot_space = 14 if has_dot else 0
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    total_w = tw + pad_x * 2 + dot_space
    
    if left_x is not None:
        x1 = left_x
        x2 = left_x + total_w
    else:
        x1 = cx - total_w // 2
        x2 = cx + total_w // 2
        
    y1 = cy - height // 2
    y2 = cy + height // 2
    
    draw.rounded_rectangle([x1, y1, x2, y2], radius=height//2, fill=bg_col, outline=border_col, width=1)
    
    tx_start = x1 + pad_x
    if has_dot:
        dot_y = cy
        draw.ellipse([tx_start, dot_y - 3, tx_start + 6, dot_y + 3], fill=dot_col)
        tx_start += dot_space
        
    draw.text((tx_start, cy), text, font=font, fill=txt_col, anchor='lm')
    return (x1, y1, x2, y2)

def draw_slide_header(draw, slide_num, category_en, title_black, title_blue, subtitle_kr, right_badge=None, dark_mode=False):
    draw.line([(100, 52), (1820, 52)], fill=(40, 50, 70) if dark_mode else (226, 232, 240), width=1)
    kicker_txt = f"{slide_num:02d} {category_en}"
    draw_pill_badge(draw, left_x=100, cy=78, text=kicker_txt, font=get_font(10.5, 'bold'), theme='blue', has_dot=True, dark_mode=dark_mode, pad_x=10, height=26)
    
    if right_badge:
        rb_txt, rb_theme = right_badge
        draw_pill_badge(draw, left_x=None, cx=1740, cy=78, text=rb_txt, font=get_font(10, 'bold'), theme=rb_theme, has_dot=True, dark_mode=dark_mode, pad_x=12, height=26)
        
    f_title = get_font(33, 'extrabold')
    w_tb = draw.textlength(title_black, font=f_title)
    
    t_black_col = (255, 255, 255) if dark_mode else (15, 23, 42)
    t_blue_col = (59, 130, 246) if dark_mode else (29, 78, 216)
    
    draw.text((100, 116), title_black, font=f_title, fill=t_black_col)
    draw.text((100 + w_tb, 116), title_blue, font=f_title, fill=t_blue_col)
    
    sub_col = (148, 163, 184) if dark_mode else (100, 116, 139)
    draw.text((100, 168), subtitle_kr, font=get_font(13.5, 'regular'), fill=sub_col)

def draw_slide_footer(draw, slide_num, meta_tags="KOREA HISTORY QUIZ · EDUTECH CASE STUDY", dark_mode=False):
    draw.line([(100, 1000), (1820, 1000)], fill=(40, 50, 70) if dark_mode else (226, 232, 240), width=1)
    f_col = (100, 116, 139) if dark_mode else (148, 163, 184)
    draw.text((100, 1018), "DAEHANGUKSA · KOREA HISTORY QUIZ", font=get_font(11, 'bold'), fill=f_col)
    draw.text((960, 1018), meta_tags, font=get_font(10.5, 'medium'), fill=f_col, anchor='mm')
    draw.text((1820, 1018), f"{slide_num:02d} / 12", font=get_font(12, 'bold'), fill=(29, 78, 216) if not dark_mode else (96, 165, 250), anchor='rm')

def draw_arrow(draw, start, end, col=(29, 78, 216), width=2, arrow_size=6):
    draw.line([start, end], fill=col, width=width)
    x1, y1 = start
    x2, y2 = end
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=col)

def draw_diamond(draw, cx, cy, w, h, fill=(255, 255, 255), outline=(29, 78, 216), width=1):
    hw = w // 2
    hh = h // 2
    points = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
    draw.polygon(points, fill=fill, outline=outline)

def draw_dashed_line(draw, start, end, col=(203, 213, 225), width=1, dash=6, gap=4):
    x1, y1 = start
    x2, y2 = end
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist == 0:
        return
    d_x = (x2 - x1) / dist
    d_y = (y2 - y1) / dist
    cur = 0
    while cur < dist:
        seg_len = min(dash, dist - cur)
        sx = x1 + cur * d_x
        sy = y1 + cur * d_y
        ex = sx + seg_len * d_x
        ey = sy + seg_len * d_y
        draw.line([(sx, sy), (ex, ey)], fill=col, width=width)
        cur += dash + gap

def draw_dashed_arrow(draw, start, end, col=(203, 213, 225), width=1, dash=6, gap=4, arrow_size=4):
    draw_dashed_line(draw, start, end, col=col, width=width, dash=dash, gap=gap)
    x1, y1 = start
    x2, y2 = end
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=col)

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

print("Core framework for Korea History Quiz initialized.")
