import math
import textwrap
import os
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
BASE_DIR = 'd:/097.flutter_project/auto_portfolio/mes_solution'
OUT_DIR = os.path.join(BASE_DIR, 'behance_slides')
MOCKUP_DIR = os.path.join(BASE_DIR, 'mockups')
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

FLUTTER_MATERIAL_FONT = r"C:\flutter\bin\cache\artifacts\material_fonts\MaterialIcons-Regular.otf"

def get_material_icon_font(size):
    if os.path.exists(FLUTTER_MATERIAL_FONT):
        try:
            return ImageFont.truetype(FLUTTER_MATERIAL_FONT, int(round(size)))
        except:
            pass
    return get_font(size, 'bold')

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

# Visual Primitives
def draw_diamond(draw, cx, cy, w, h, fill, outline, width=1):
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

def draw_database_node(draw, cx, cy, w, h, fill=(240, 246, 255), outline=(0, 81, 255), width=1):
    ew = w
    eh = int(h * 0.28)
    top_y = cy - h // 2
    bot_y = cy + h // 2
    draw.ellipse([cx - ew // 2, bot_y - eh, cx + ew // 2, bot_y], fill=fill, outline=outline, width=width)
    draw.rectangle([cx - ew // 2, top_y + eh // 2, cx + ew // 2, bot_y - eh // 2], fill=fill)
    draw.line([(cx - ew // 2, top_y + eh // 2), (cx - ew // 2, bot_y - eh // 2)], fill=outline, width=width)
    draw.line([(cx + ew // 2, top_y + eh // 2), (cx + ew // 2, bot_y - eh // 2)], fill=outline, width=width)
    draw.ellipse([cx - ew // 2, top_y, cx + ew // 2, top_y + eh], fill=fill, outline=outline, width=width)

def draw_arrow(draw, p1, p2, col=(0, 81, 255), width=2, arrow_size=6):
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

def draw_pill_badge(draw, cx=None, cy=0, text="", font=None, theme='blue', dark_mode=False, pad_x=14, height=30, left_x=None, solid=False, has_dot=False):
    if font is None:
        font = get_font(10.5, 'bold')
        
    color_schemes_dark = {
        'blue':   {'bg': (16, 42, 86, 255),  'border': (0, 140, 255, 255),  'text': (0, 215, 255, 255)},
        'cyan':   {'bg': (8, 48, 64, 255),   'border': (0, 210, 255, 255),  'text': (0, 230, 255, 255)},
        'green':  {'bg': (12, 48, 36, 255),  'border': (16, 185, 129, 255), 'text': (52, 211, 153, 255)},
        'red':    {'bg': (58, 20, 24, 255),  'border': (239, 68, 68, 255),  'text': (255, 140, 140, 255)},
        'amber':  {'bg': (54, 38, 12, 255),  'border': (245, 158, 11, 255), 'text': (251, 191, 36, 255)},
        'purple': {'bg': (42, 22, 70, 255),  'border': (168, 85, 247, 255), 'text': (216, 180, 254, 255)},
        'slate':  {'bg': (30, 41, 59, 255),  'border': (100, 116, 139, 255),'text': (226, 232, 240, 255)},
        'dark':   {'bg': (15, 23, 42, 255),  'border': (51, 65, 85, 255),   'text': (255, 255, 255, 255)},
    }
    color_schemes_light = {
        'blue':   {'bg': (239, 246, 255, 255), 'border': (191, 219, 254, 255), 'text': (0, 82, 255, 255)},
        'cyan':   {'bg': (236, 254, 255, 255), 'border': (165, 243, 252, 255), 'text': (8, 145, 178, 255)},
        'green':  {'bg': (236, 253, 245, 255), 'border': (167, 243, 208, 255), 'text': (5, 150, 105, 255)},
        'red':    {'bg': (254, 242, 242, 255), 'border': (254, 202, 202, 255), 'text': (220, 38, 38, 255)},
        'amber':  {'bg': (254, 243, 199, 255), 'border': (253, 230, 138, 255), 'text': (180, 83, 9, 255)},
        'purple': {'bg': (245, 243, 255, 255), 'border': (221, 214, 254, 255), 'text': (109, 40, 217, 255)},
        'slate':  {'bg': (241, 245, 249, 255), 'border': (203, 213, 225, 255), 'text': (51, 65, 85, 255)},
        'dark':   {'bg': (15, 23, 42, 255),    'border': (15, 23, 42, 255),     'text': (255, 255, 255, 255)},
    }
    color_schemes_solid = {
        'blue':   {'bg': (0, 82, 255, 255),   'border': (0, 82, 255, 255),   'text': (255, 255, 255, 255)},
        'cyan':   {'bg': (8, 145, 178, 255),  'border': (8, 145, 178, 255),  'text': (255, 255, 255, 255)},
        'green':  {'bg': (16, 185, 129, 255), 'border': (16, 185, 129, 255), 'text': (255, 255, 255, 255)},
        'red':    {'bg': (239, 68, 68, 255),  'border': (239, 68, 68, 255),  'text': (255, 255, 255, 255)},
        'amber':  {'bg': (217, 119, 6, 255),  'border': (217, 119, 6, 255),  'text': (255, 255, 255, 255)},
        'purple': {'bg': (124, 58, 237, 255), 'border': (124, 58, 237, 255), 'text': (255, 255, 255, 255)},
        'slate':  {'bg': (71, 85, 105, 255),  'border': (71, 85, 105, 255),  'text': (255, 255, 255, 255)},
    }
    
    if solid:
        scheme = color_schemes_solid.get(theme, color_schemes_solid['blue'])
    elif dark_mode:
        scheme = color_schemes_dark.get(theme, color_schemes_dark['blue'])
    else:
        scheme = color_schemes_light.get(theme, color_schemes_light['blue'])
    
    tw = draw.textlength(text, font=font)
    bw = int(round(tw + pad_x * 2))
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
    
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=radius, fill=scheme['bg'], outline=scheme['border'], width=1)
    draw.text((cx, cy), text, font=font, anchor='mm', fill=scheme['text'])
    return bx1, by1, bx2, by2

def draw_slide_header(draw, slide_num, category_kr, title_black, title_blue, subtitle_kr, right_badge=None, dark_mode=False):
    line_col = (40, 53, 72) if dark_mode else (226, 232, 240)
    draw.line([(100, 48), (1820, 48)], fill=line_col, width=1)
    
    badge_text = f"{slide_num:02d} {category_kr}"
    draw_pill_badge(draw, left_x=100, cy=78, text=badge_text, font=get_font(10.5, 'bold'), theme='blue', dark_mode=dark_mode, pad_x=10, height=26)
    
    if right_badge:
        txt, theme = right_badge
        draw_pill_badge(draw, cx=1700, cy=78, text=txt, font=get_font(10.5, 'bold'), theme=theme, solid=True, dark_mode=dark_mode, pad_x=14, height=28)
        
    font_title = get_font(34, 'bold')
    w_black = draw.textlength(title_black, font=font_title)
    text_main_col = (255, 255, 255) if dark_mode else (15, 23, 42)
    text_blue_col = (56, 189, 248) if dark_mode else (0, 81, 255)
    draw.text((100, 118), title_black, font=font_title, fill=text_main_col)
    draw.text((100 + w_black, 118), title_blue, font=font_title, fill=text_blue_col)
    
    sub_col = (148, 163, 184) if dark_mode else (71, 85, 105)
    draw.text((100, 166), subtitle_kr, font=get_font(14.5, 'regular'), fill=sub_col)

def draw_slide_footer(draw, slide_num, total_slides=12, dark_mode=False):
    line_col = (40, 53, 72) if dark_mode else (226, 232, 240)
    draw.line([(100, 995), (1820, 995)], fill=line_col, width=1)
    
    brand_col = (56, 189, 248) if dark_mode else (0, 81, 255)
    draw.text((100, 1018), "CODEBRIDGEX MES SOLUTION", font=get_font(11, 'bold'), fill=brand_col)
    meta_col = (100, 116, 139) if dark_mode else (148, 163, 184)
    draw.text((310, 1018), "·   엔터프라이즈 SaaS 제조 실행 시스템  ·  스마트 팩토리 반응형 웹 플랫폼", font=get_font(11, 'medium'), fill=meta_col)
    draw.text((960, 1018), "데스크톱 · 태블릿 · 모바일 반응형 완비  ·  아토믹 디자인 시스템 150+ 컴포넌트", font=get_font(10.5, 'medium'), fill=meta_col, anchor='mt')
    
    page_col = (148, 163, 184) if dark_mode else (100, 116, 139)
    page_str = f"PAGE {slide_num:02d} / {total_slides:02d}"
    draw.text((1820, 1018), page_str, font=get_num_font(11.5, 'black'), fill=page_col, anchor='rt')

def draw_browser_frame(draw, base_img, x, y, w, h, screenshot_path, title_bar_text="CodeBridgeX Cloud MES Platform", dark_mode=False):
    bg_bar = (15, 23, 42) if dark_mode else (241, 245, 249)
    border_col = (51, 65, 85) if dark_mode else (203, 213, 225)
    line_col = (30, 41, 59) if dark_mode else (226, 232, 240)
    
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(15, 23, 42) if dark_mode else (255, 255, 255), outline=border_col, width=1)
    draw.rounded_rectangle([x, y, x + w, y + 38], radius=12, fill=bg_bar)
    draw.rectangle([x, y + 26, x + w, y + 38], fill=bg_bar)
    draw.line([(x, y + 38), (x + w, y + 38)], fill=line_col, width=1)
    
    draw.ellipse([x + 14, y + 14, x + 24, y + 24], fill=(239, 68, 68))
    draw.ellipse([x + 30, y + 14, x + 40, y + 24], fill=(245, 158, 11))
    draw.ellipse([x + 46, y + 14, x + 56, y + 24], fill=(16, 185, 129))
    
    addr_w = int(w * 0.45)
    addr_x = x + (w - addr_w) // 2
    draw.rounded_rectangle([addr_x, y + 7, addr_x + addr_w, y + 31], radius=6, fill=(30, 41, 59) if dark_mode else (255, 255, 255), outline=line_col, width=1)
    draw.text((addr_x + 14, y + 19), title_bar_text, font=get_font(9.5, 'medium'), fill=(148, 163, 184) if dark_mode else (100, 116, 139), anchor='lm')
    
    if os.path.exists(screenshot_path):
        try:
            content_h = h - 39
            content_w = w - 2
            img = Image.open(screenshot_path).convert('RGB')
            # Proportional fit inside browser canvas
            src_w, src_h = img.size
            scale = min(content_w / src_w, content_h / src_h)
            target_w = int(round(src_w * scale))
            target_h = int(round(src_h * scale))
            img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            px = x + 1 + (content_w - target_w) // 2
            py = y + 39 + (content_h - target_h) // 2
            base_img.paste(img_resized, (px, py))
        except Exception as e:
            print(f"Error loading screenshot {screenshot_path}:", e)

print("MES slide helpers & graphic primitives initialized!")
# ==============================================================
# SLIDE 01: Hero Cover with Multi-Device Responsive Composition
def make_shadow(im, radius=32, alpha=100):
    sh = Image.new('RGBA', (im.width + 64, im.height + 64), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([32, 32, 32 + im.width, 32 + im.height], radius=44, fill=(15, 23, 42, alpha))
    return sh.filter(ImageFilter.GaussianBlur(radius))

def make_slide_01():
    # 1. Subtle Ambient Radial Glow on Pristine White Canvas (Open Design)
    base = Image.new('RGBA', (W, H), (250, 252, 255, 255))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([800, 100, 1850, 850], fill=(0, 81, 255, 18))
    g_draw.ellipse([1050, 180, 1750, 780], fill=(6, 182, 212, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    
    draw = ImageDraw.Draw(base)
    
    # 2. Hairline Top Boundary & Metadata Pills
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=100, cy=76, text="2026 포트폴리오 케이스 스터디", font=get_font(11.5, 'bold'), theme='blue', has_dot=True, pad_x=12, height=28)
    
    meta_txt = "엔터프라이즈 UX/UI 기획 총괄 · 반응형 웹 아키텍처 · 13개 모듈 59개 화면 · Web Prototype"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=(100, 116, 139))
    
    # 3. Category & Large Title (Left Column)
    draw.text((100, 146), "CODEBRIDGEX MES SOLUTION · 제조 실행 플랫폼", font=get_font(14, 'bold'), fill=(0, 81, 255))
    
    title_p1 = "분절된 제조 현장을, "
    title_p2 = "하나의 화면으로 지휘하다."
    w_p1 = draw.textlength(title_p1, font=get_font(56, 'black'))
    draw.text((100, 178), title_p1, font=get_font(56, 'black'), fill=(15, 23, 42))
    draw.text((100 + w_p1, 178), title_p2, font=get_font(56, 'black'), fill=(0, 81, 255))
    
    sub1 = "관제실 대화면부터 현장 10인치 터치 태블릿, 모바일 스마트폰까지 단일 소스로 완벽하게 대응하고,"
    sub2 = "수주·생산 MRP 파이프라인, 실시간 OEE 텔레메트리, 무결점 LOT 추적으로 수기 취합 공수를 99.9% 절감한 엔터프라이즈 SaaS"
    draw.text((100, 260), sub1, font=get_font(16.5, 'regular'), fill=(71, 85, 105))
    draw.text((100, 288), sub2, font=get_font(16.5, 'semibold'), fill=(30, 41, 59))
    
    # 4. OPEN STORYLINE: Key Strengths (Open layout with zero enclosing box, matching Behance standard)
    strengths = [
        ("01", "전사 파이프라인", "수주-생산-출하 원스톱 통합 파이프라인", "Order-to-Ship Realtime Pipeline",
         "부서별로 파편화된 엑셀과 수기 장부를 단일 데이터 파이프라인으로 연결하여 수기 취합 공수를 99.9% 절감했습니다."),
        ("02", "반응형 원격 관제", "현장 터치 최적화 멀티 디바이스 반응형", "Multi-Device Responsive Telemetry",
         "데스크톱 관제실뿐 아니라 10인치 현장 태블릿(16:10)과 모바일(9:16)까지 실시간 설비 가동 상태와 병목을 즉시 관제합니다."),
        ("03", "역할 기반 인터페이스", "경영진/작업자 역할별 고유 인터페이스", "Role-Based Ergonomic Interface",
         "CEO/공장장 핵심 KPI 대시보드와 현장 작업자 공정 스케줄러를 분리하여 과도한 정보 장벽 없이 1초 내 직관 조작을 지원합니다."),
        ("04", "아토믹 토큰 체계", "150개 표준 에셋 엔터프라이즈 디자인 시스템", "Atomic Design System & Multi-Tenant",
         "Atoms부터 Templates까지 4계층 아토믹 규격과 테넌트 테마 주입 체계를 완성하여 13개 비즈니스 모듈의 일관성을 실현했습니다.")
    ]
    
    max_badge_w = max(draw.textlength(tag, font=get_font(10, 'bold')) + 16 for _, tag, _, _, _ in strengths)
    title_x = int(round(144 + max_badge_w + 24))
    
    k_y = 358
    for idx, (num, tag, title_ko, sub_en, desc) in enumerate(strengths):
        draw.rounded_rectangle([100, k_y + 2, 136, k_y + 28], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.text((118, k_y + 15), num, font=get_font(11, 'bold'), fill=(0, 81, 255), anchor='mm')
        
        draw_pill_badge(draw, left_x=144, cy=k_y + 15, text=tag, font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=22)
        draw.text((title_x, k_y + 4), title_ko, font=get_font(15.5, 'bold'), fill=(15, 23, 42))
        
        w_title = draw.textlength(title_ko, font=get_font(15.5, 'bold'))
        draw.text((title_x + w_title + 12, k_y + 6), f"·  {sub_en}", font=get_font(12, 'medium'), fill=(100, 116, 139))
        
        words = desc.split(' ')
        lines = []
        cur_l = ""
        for w in words:
            test = (cur_l + ' ' + w).strip()
            if draw.textlength(test, font=get_font(12, 'regular')) <= 730:
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
            
        if idx < 3:
            draw.line([(100, k_y + 92), (860, k_y + 92)], fill=(226, 232, 240), width=1)
            
        k_y += 114

    # 5. Right Side: Multi-Device Trio Transparent Mockup Showcase (Laptop, Tablet, Mobile)
    # Scaled up by 10% upwards while keeping the bottom baseline perfectly anchored to paragraph 04
    trio_thumb = r"d:\097.flutter_project\auto_portfolio\assets\mes_hero_device_trio.png"
    if os.path.exists(trio_thumb):
        trio_img = Image.open(trio_thumb).convert('RGBA')
        
        # 10% enlarged heroic dimensions (w=1056px, h=703px)
        scale = 1056 / float(trio_img.width)
        new_w = int(round(trio_img.width * scale))
        new_h = int(round(trio_img.height * scale))
        trio_resized = trio_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Right aligned to margin (1820px) and bottom baseline anchored to paragraph 04 (y=748)
        pos_x = 1820 - new_w
        pos_y = 207  # Bottom edge of laptop chassis sits exactly at paragraph 04 baseline (y=748) while expanding 10% upwards
        
        # Real transparent alpha mask drop shadow for floating depth
        mask = trio_resized.split()[3]
        sh_img = Image.new('RGBA', (trio_resized.width + 120, trio_resized.height + 120), (0, 0, 0, 0))
        black = Image.new('RGBA', trio_resized.size, (15, 23, 42, 75))
        sh_img.paste(black, (60 + 12, 60 + 26), mask)
        sh = sh_img.filter(ImageFilter.GaussianBlur(38))
        
        base.paste(sh, (pos_x - 60, pos_y - 60), sh)
        base.paste(trio_resized, (pos_x, pos_y), trio_resized)

    draw = ImageDraw.Draw(base)
    
    # 7. Bottom 4-Column Specification Strip (Spanning x=100 to 1820, y=840 to 956)
    bar_y = 840
    bar_h = 116
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    col_w = 1720 // 4
    specs = [
        ("PROJECT ROLE", "서비스 기획 100% · UI/UX 아키텍처 100%", "스마트 제조 현장 문제 정의 · IA 정보 설계 · 와이어프레임 · UI 디자인 총괄"),
        ("PERIOD & TIMELINE", "2026.03 - 현재 (클라우드 SaaS 라이브)", "수주-생산-품질-재고 13대 모듈 실시간 연동 및 59개 인터랙티브 화면 상용 검증"),
        ("DESIGN SYSTEM", "아토믹 토큰 아키텍처 (150+ 에셋)", "4/8pt 베이스라인 · 일렉트릭 블루(#0051FF) & 옵시디언 다크 · 다중 테넌트 테마 주입"),
        ("DELIVERY & RELEASE", "멀티 디바이스 반응형 웹 & 라이브 프로토타입", "데스크톱 16:9 · 현장 태블릿 16:10 · 모바일 9:16 최적화 뷰포트 인터랙션 완비")
    ]
    
    for i, (cat, val_bold, val_desc) in enumerate(specs):
        cx = 100 + i * col_w
        if i > 0:
            draw.line([(cx, bar_y + 18), (cx, bar_y + bar_h - 18)], fill=(226, 232, 240), width=1)
        
        draw.text((cx + 28, bar_y + 18), cat, font=get_font(11, 'bold'), fill=(0, 81, 255))
        draw.text((cx + 28, bar_y + 42), val_bold, font=get_font(14.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 28, bar_y + 70), val_desc, font=get_font(11, 'regular'), fill=(100, 116, 139))
        
    draw_slide_footer(draw, 1)
    base.convert('RGB').save(os.path.join(OUT_DIR, 'slide_01.png'))
    print("SAVED slide_01.png (Open Storyline & Transparent Device Mockup)")


def make_slide_02():
    base = Image.new('RGB', (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=2, 
        category_kr="사용자 리서치 | 제조 현장 병목 분석 & 시장 실태 조사", 
        title_black="제조 현장의 분절된 데이터 파편화, ", 
        title_blue="실시간 데이터 파이프라인과 반응형 관제로 극복", 
        subtitle_kr="사내 임직원 조사 및 시장 동향 AI 분석 기반 핵심 애로사항 규명과 3대 문제 해결 전략"
    )
    
    # -------------------------------------------------------------
    # TOP: 3 Problem -> Solution Strategic Cards (y=202, h=108 each, gap=14)
    # Modern card with accent line, impact metric tag, and structured badges
    # -------------------------------------------------------------
    cards_data = [
        (
            "01",
            "분절된 데이터 파편화 → 전사 데이터 일원화 파이프라인",
            "수주, 생산, 재고, 회계 데이터가 부서별 엑셀과 수기 전산으로 파편화되어 데이터 누락 및 결산 오차 발생",
            "생산(MES) 실적과 자금(ERP) 데이터가 실시간 연동되는 단일 파이프라인 구축으로 수기 취합 공수 99.9% 절감",
            "월 160시간 수기 공수 낭비",
            (239, 68, 68),  # Rose
            (0, 81, 255)    # Brand Blue
        ),
        (
            "02",
            "현장 의존적 유선 보고 → 멀티 디바이스 실시간 원격 관제",
            "공장 라인 이상 및 설비 비가동 시 현장 직접 방문이나 유선 구두 보고에 의존하여 경영진의 긴급 의사결정 지연",
            "PC 브라우저·10인치 태블릿·모바일에 최적화된 반응형 텔레메트리 관제로 원격지에서도 병목 현상 즉시 파악",
            "라인 정지 인지 45분 지연",
            (245, 158, 11), # Amber
            (14, 165, 233)  # Sky Blue
        ),
        (
            "03",
            "복잡한 대기업형 SI 장벽 → 역할(Role) 기반 경량화 인터페이스",
            "기존 고가 구축형 시스템은 복잡한 메뉴 뎁스와 불필요한 과도한 기능 노출로 현장 작업자 진입 장벽 형성",
            "경영진, 공정관리자, 작업자 등 직무별 필수 위젯만 배치하는 1-Tap 터치 중심 경량화 UX 및 모듈형 시스템 적용",
            "초기 구축비 3.8억원 부담",
            (139, 92, 246), # Purple
            (16, 185, 129)  # Emerald
        )
    ]
    
    top_sy = 202
    top_card_w = 1720
    top_card_h = 110
    top_gap = 14
    
    for c_idx, (c_num, c_title, c_prob, c_sol, c_metric, c_accent, c_sol_col) in enumerate(cards_data):
        cy = top_sy + c_idx * (top_card_h + top_gap)
        
        # Main Card White Surface with soft shadow/border (No left accent bar)
        draw.rounded_rectangle(
            [100, cy, 100 + top_card_w, cy + top_card_h],
            radius=14,
            fill=(255, 255, 255),
            outline=(226, 232, 240),
            width=1
        )
        
        # Number badge pill
        draw.rounded_rectangle([126, cy + 14, 158, cy + 34], radius=6, fill=(241, 245, 249))
        draw.text((142, cy + 24), c_num, font=get_num_font(12, 'bold'), fill=(71, 85, 105), anchor='mm')
        
        # Title
        draw.text((168, cy + 24), c_title, font=get_font(16.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        
        # Right Impact Metric Pill (Clean text pill, no leading bullet dot)
        metric_w = 190
        metric_h = 26
        metric_rx = 100 + top_card_w - 20 - metric_w
        draw.rounded_rectangle([metric_rx, cy + 12, metric_rx + metric_w, cy + 12 + metric_h], radius=13, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
        draw.text((metric_rx + metric_w // 2, cy + 24), f"손실: {c_metric}", font=get_font(11.5, 'bold'), fill=(185, 28, 28), anchor='mm')
        
        # Problem Row
        # Problem Tag
        draw.rounded_rectangle([126, cy + 47, 190, cy + 69], radius=5, fill=(254, 242, 242))
        draw.text((158, cy + 58), "Problem", font=get_num_font(11.5, 'bold'), fill=(220, 38, 38), anchor='mm')
        draw.text((200, cy + 58), c_prob, font=get_font(12.5, 'regular'), fill=(51, 65, 85), anchor='lm')
        
        # Solution Row
        # Solution Tag
        draw.rounded_rectangle([126, cy + 76, 190, cy + 98], radius=5, fill=(239, 246, 255))
        draw.text((158, cy + 87), "Solution", font=get_num_font(11.5, 'bold'), fill=(29, 78, 216), anchor='mm')
        draw.text((200, cy + 87), c_sol, font=get_font(12.5, 'medium'), fill=(15, 23, 42), anchor='lm')
        
    # -------------------------------------------------------------
    # BOTTOM: 2 High-Density Analytical Cards (y=584, h=388)
    # -------------------------------------------------------------
    bot_y = 584
    bot_w = 845
    bot_h = 388
    bot_gap = 30
    
    # -------------------------------------------------------------
    # Left Bottom: Donut Chart "정보 파편화 및 현장 병목 구조 분석"
    # Modern Split Layout: Donut on Left, High-Clarity Legend Pods on Right
    # -------------------------------------------------------------
    lb_x = 100
    draw.rounded_rectangle([lb_x, bot_y, lb_x + bot_w, bot_y + bot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Card Header with pill tag
    draw.rounded_rectangle([lb_x + 30, bot_y + 24, lb_x + 130, bot_y + 44], radius=6, fill=(239, 246, 255))
    draw.text((lb_x + 80, bot_y + 34), "정성/정량 분석", font=get_font(11, 'bold'), fill=(29, 78, 216), anchor='mm')
    draw.text((lb_x + 140, bot_y + 34), "정보 파편화 및 현장 병목 구조 분석", font=get_font(17.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((lb_x + 32, bot_y + 58), "제조 현장 임직원 심층 설문 150명 결과 (복수 응답 애로사항 분석)", font=get_font(11.5, 'regular'), fill=(100, 116, 139))
    
    # Donut Geometry (Left Zone)
    dc_x = lb_x + 175
    dc_y = bot_y + 195
    outer_r = 105
    inner_r = 54
    
    slices = [
        ("기존 시스템 UI 불만족", 30, (14, 165, 233), "복잡한 메뉴 뎁스와 느린 터치 반응 속도"),
        ("부서별 엑셀 관리 파편화", 25, (0, 81, 255), "데이터 불일치 및 수기 취합 오류 빈번"),
        ("수작업 및 유선 구두 보고", 25, (99, 102, 241), "실시간 모니터링 불가 및 의사결정 지연"),
        ("대기업형 구축 비용 부담", 20, (245, 158, 11), "수억원대 SI 패키지 도입 예산 장벽")
    ]
    
    # Draw Donut Slices
    curr_angle = -90  # Start at top 12 o'clock
    for s_title, s_pct, s_col, s_desc in slices:
        sweep = (s_pct / 100.0) * 360.0
        draw.pieslice(
            [dc_x - outer_r, dc_y - outer_r, dc_x + outer_r, dc_y + outer_r],
            start=curr_angle,
            end=curr_angle + sweep,
            fill=s_col
        )
        
        # Center angle for donut percentage label
        mid_angle_deg = curr_angle + sweep / 2.0
        mid_rad = math.radians(mid_angle_deg)
        label_r = (outer_r + inner_r) / 2.0
        tx = dc_x + label_r * math.cos(mid_rad)
        ty = dc_y + label_r * math.sin(mid_rad)
        
        # Crisp percentage text inside slice
        draw.text((tx, ty), f"{s_pct}%", font=get_num_font(13, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        curr_angle += sweep
        
    # Cut out inner hole for Donut with clean center KPI
    draw.ellipse([dc_x - inner_r, dc_y - inner_r, dc_x + inner_r, dc_y + inner_r], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((dc_x, dc_y - 10), "개선 시급도", font=get_font(10.5, 'bold'), fill=(100, 116, 139), anchor='mm')
    draw.text((dc_x, dc_y + 11), "100%", font=get_num_font(16.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    
    # Legend Pods on the Right side of Donut (Clear alignment, no overlaps)
    leg_x = lb_x + 325
    leg_w = bot_w - 355
    leg_sy = bot_y + 88
    leg_h = 56
    leg_gap = 10
    
    for l_idx, (s_title, s_pct, s_col, s_desc) in enumerate(slices):
        ly = leg_sy + l_idx * (leg_h + leg_gap)
        
        # Container box (Clean white card, no left vertical bar)
        draw.rounded_rectangle([leg_x, ly, leg_x + leg_w, ly + leg_h], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        # Color dot + Title
        draw.ellipse([leg_x + 18, ly + 14, leg_x + 26, ly + 22], fill=s_col)
        draw.text((leg_x + 34, ly + 18), s_title, font=get_font(12.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        
        # Right percentage badge
        draw.text((leg_x + leg_w - 18, ly + 18), f"{s_pct}%", font=get_num_font(13.5, 'bold'), fill=s_col, anchor='rm')
        
        # Subtitle description
        draw.text((leg_x + 34, ly + 38), s_desc, font=get_font(10.5, 'regular'), fill=(100, 116, 139), anchor='lm')

    # Bottom Key Insight Banner inside Left Card
    insight_y = bot_y + bot_h - 40
    draw.rounded_rectangle([lb_x + 24, insight_y, lb_x + bot_w - 24, insight_y + 28], radius=6, fill=(241, 245, 249))
    draw.text((lb_x + 36, insight_y + 14), "Key Insight", font=get_num_font(11, 'bold'), fill=(2, 132, 199), anchor='lm')
    draw.text((lb_x + 120, insight_y + 14), "기존 시스템 불만 1순위는 '느린 UI 및 수기 병행'으로 실시간 경량 반응형 시스템 전환 필수", font=get_font(10.5, 'regular'), fill=(51, 65, 85), anchor='lm')
    
    # -------------------------------------------------------------
    # Right Bottom: Horizontal Bar Chart "중소 제조사 CEO가 겪는 가장 큰 관리 애로사항은?"
    # -------------------------------------------------------------
    rb_x = lb_x + bot_w + bot_gap
    draw.rounded_rectangle([rb_x, bot_y, rb_x + bot_w, bot_y + bot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Card Header with pill tag
    draw.rounded_rectangle([rb_x + 30, bot_y + 24, rb_x + 115, bot_y + 44], radius=6, fill=(254, 243, 199))
    draw.text((rb_x + 72, bot_y + 34), "경영진 서베이", font=get_font(11, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((rb_x + 125, bot_y + 34), "중소 제조사 CEO가 겪는 가장 큰 관리 애로사항은?", font=get_font(17.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((rb_x + 32, bot_y + 58), "경영진 120개사 심층 인터뷰 정량 통계 (단위: %, 복수응답)", font=get_font(11.5, 'regular'), fill=(100, 116, 139))
    
    # H-Bar Data
    bar_items = [
        ("01", "미수금/자금 흐름 파악 불가", 37.8, (0, 81, 255)),
        ("02", "실시간 생산 진척 모니터링", 26.8, (14, 165, 233)),
        ("03", "수주/발주 현황 실시간 동기화", 12.2, (59, 130, 246)),
        ("04", "타 부서 간 데이터 취합 지연", 12.2, (99, 102, 241)),
        ("05", "납기 관리 및 지연 공정 예측", 6.8, (148, 163, 184)),
        ("06", "작업자 근태 및 기준정보 관리", 4.2, (203, 213, 225))
    ]
    
    axis_x = rb_x + 230  # Vertical axis line x
    bar_sy = bot_y + 90
    bar_h = 16
    bar_gap_y = 38
    max_pct = 40.0
    bar_max_w = 480
    
    # Axis Line
    draw.line([axis_x, bar_sy - 6, axis_x, bar_sy + len(bar_items) * bar_gap_y - 12], fill=(203, 213, 225), width=2)
    
    for b_idx, (b_rank, b_label, b_val, b_col) in enumerate(bar_items):
        by = bar_sy + b_idx * bar_gap_y
        
        # Rank badge
        draw.rounded_rectangle([rb_x + 24, by - 1, rb_x + 48, by + bar_h + 1], radius=4, fill=(241, 245, 249))
        draw.text((rb_x + 36, by + 8), b_rank, font=get_num_font(11, 'bold'), fill=(71, 85, 105), anchor='mm')
        
        # Label (Right-aligned to axis)
        draw.text((axis_x - 14, by + 8), b_label, font=get_font(12, 'medium'), fill=(30, 41, 59), anchor='rm')
        
        # Track background
        draw.rounded_rectangle([axis_x + 4, by, axis_x + 4 + bar_max_w, by + bar_h], radius=bar_h // 2, fill=(241, 245, 249))
        
        # Bar Fill
        curr_w = int(round((b_val / max_pct) * bar_max_w))
        draw.rounded_rectangle([axis_x + 4, by, axis_x + 4 + curr_w, by + bar_h], radius=bar_h // 2, fill=b_col)
        
        # Value text (next to bar)
        draw.text((axis_x + 4 + curr_w + 10, by + 8), f"{b_val:.1f}%", font=get_num_font(12.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        
    # Bottom Quote Pill inside Right Card
    quote_y = bot_y + bot_h - 40
    draw.rounded_rectangle([rb_x + 24, quote_y, rb_x + bot_w - 24, quote_y + 28], radius=6, fill=(248, 250, 252))
    draw.text((rb_x + 36, quote_y + 14), "CEO 인터뷰", font=get_font(11, 'bold'), fill=(217, 119, 6), anchor='lm')
    draw.text((rb_x + 120, quote_y + 14), '"퇴근 후에도 공장 가동률과 미수금 현황을 모바일로 한눈에 보는 것이 최대 소원"', font=get_font(10.5, 'regular'), fill=(51, 65, 85), anchor='lm')
    
    draw_slide_footer(draw, 2)
    base.save(os.path.join(OUT_DIR, 'slide_02.png'))
    print("SAVED slide_02.png (Research with Exact Problem/Solution & 2 High-Density Charts)")


# ==============================================================
# SLIDE 03: Target Users & Roles (Role-Based Access Control & Multi-Tenant SaaS)
def make_slide_03():
    base = Image.new('RGB', (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=3, 
        category_kr="Target Users & Roles | 직무 권한별(RBAC) 동적 인터페이스 & 멀티테넌트 SaaS 아키텍처", 
        title_black="대표의 전사 관제부터 현장 전용 뷰까지, ", 
        title_blue="접속 권한에 따라 동적으로 최적화되는 역할 기반 인터페이스", 
        subtitle_kr="로그인 권한별 메뉴·콘텐츠 자동 분기(RBAC)와 코드브릿지의 고객사 통합 관리 멀티테넌트 SaaS 비즈니스 모델"
    )
    
    # -------------------------------------------------------------
    # TOP ZONE: 3 Key Persona & RBAC Dynamic Screen Spec (y=202, h=250)
    # 3 distinct roles: CEO (전사/인사/공정 총괄) / Field Manager (공정/품질) / Line Worker (현장 실적)
    # -------------------------------------------------------------
    col_w = (W - 200 - 2 * 24) // 3  # 554px
    top_sy = 202
    top_h = 248
    
    roles_data = [
        (
            "CEO / 경영진 (Executive)",
            "전사 총괄 권한 · 멀티 디바이스 원격 관제",
            (0, 81, 255),
            (239, 246, 255),
            [
                ("노출 메뉴", "전체 13개 모듈 (대시보드, 인사관리, 손익, 수주, 생산, 품질, 시스템 설정)"),
                ("핵심 뷰", "실시간 OEE 텔레메트리, 미수금·매출 지표, 당일 출하 달성률, 전사 병목 관제"),
                ("디바이스", "데스크톱 웹 와이드(16:9) + 외근/퇴근 중 10인치 태블릿 & 모바일 100% 대응"),
                ("비즈 가치", "현장 방문이나 유선 구두 보고 없이 '손안에서 전 공장 및 인사 리스크 1초 즉각 대처'")
            ]
        ),
        (
            "공장장 / 생산·품질 관리자 (Manager)",
            "중간 관리자 권한 · 스마트 공정 스케줄러 & CAPA",
            (124, 58, 237),
            (245, 243, 255),
            [
                ("노출 메뉴", "생산계획(간트), 작업지시, 자재 수급, SPC 품질 통계, 부적합 CAPA"),
                ("핵심 뷰", "호기별 가동 상태, 긴급 결품 알람, 라우팅 공순 드래그 재배치, 검사 합격률"),
                ("디바이스", "관제실 데스크톱 듀얼 모니터 + 현장 패트롤용 10인치 방진 태블릿"),
                ("비즈 가치", "불필요한 회계/경영 데이터 차단, 생산 병목 조기 차단 및 긴급 지시 1초 배포")
            ]
        ),
        (
            "현장 작업자 / 오퍼레이터 (Operator)",
            "현장 전용 단순화 권한 · 1-Tap 터치 실적 등록",
            (16, 185, 129),
            (236, 253, 245),
            [
                ("노출 메뉴", "단 2개 메뉴만 직관 노출 (호기별 실적 등록, 설비 비가동 신고)"),
                ("핵심 뷰", "원자재 LOT 바코드 스캔 매핑, 48px 대형 수량 카운터, 비가동 3초 바텀시트"),
                ("디바이스", "라인별 7~10인치 고정형 방진 터치 키오스크 & 모바일 핸드헬드 PDA"),
                ("비즈 가치", "방진 장갑 착용 중 오입력 원천 방지, 텍스트 입력 없는 1-Tap 터치로 학습 비용 제로")
            ]
        )
    ]
    
    for r_idx, (r_name, r_badge, r_col, r_bg, r_specs) in enumerate(roles_data):
        rx = 100 + r_idx * (col_w + 24)
        draw.rounded_rectangle([rx, top_sy, rx + col_w, top_sy + top_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Header Badge & Name
        draw.rounded_rectangle([rx + 18, top_sy + 16, rx + 18 + 58, top_sy + 40], radius=6, fill=r_bg)
        r_code = "ROLE 01" if r_idx == 0 else "ROLE 02" if r_idx == 1 else "ROLE 03"
        draw.text((rx + 47, top_sy + 28), r_code, font=get_num_font(10.5, 'bold'), fill=r_col, anchor='mm')
        
        draw.text((rx + 86, top_sy + 28), r_name, font=get_font(14.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((rx + 18, top_sy + 54), r_badge, font=get_font(11, 'medium'), fill=r_col)
        
        draw.line([(rx + 18, top_sy + 74), (rx + col_w - 18, top_sy + 74)], fill=(241, 245, 249), width=1)
        
        # Spec rows
        spec_y = top_sy + 86
        for s_lbl, s_val in r_specs:
            # Spec pill badge
            draw.rounded_rectangle([rx + 18, spec_y, rx + 80, spec_y + 22], radius=4, fill=(241, 245, 249))
            draw.text((rx + 49, spec_y + 11), s_lbl, font=get_font(10, 'bold'), fill=(71, 85, 105), anchor='mm')
            
            lines = textwrap.wrap(s_val, width=38)
            draw.text((rx + 90, spec_y + 11), lines[0], font=get_font(11, 'regular'), fill=(51, 65, 85), anchor='lm')
            if len(lines) > 1:
                draw.text((rx + 90, spec_y + 27), lines[1], font=get_font(10.5, 'regular'), fill=(100, 116, 139), anchor='lm')
                spec_y += 36
            else:
                spec_y += 32
                
    # -------------------------------------------------------------
    # BOTTOM ZONE: 2 Strategic Architecture Cards (y=472, h=496)
    # Left: RBAC Dynamic Menu & Screen Dispatch Engine (w=845)
    # Right: CodeBridgeX Multi-Tenant SaaS Business Model (w=845)
    # -------------------------------------------------------------
    bot_sy = 472
    bot_w = 845
    bot_h = 496
    bot_gap = 30
    
    # 1. Left Card: RBAC Engine Architecture
    lb_x = 100
    draw.rounded_rectangle([lb_x, bot_sy, lb_x + bot_w, bot_sy + bot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lb_x + 24, cy=bot_sy + 26, text="DYNAMIC RBAC ENGINE", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((lb_x + 195, bot_sy + 26), "역할 및 권한별 동적 메뉴·화면 라우팅 아키텍처", font=get_font(16.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((lb_x + 24, bot_sy + 52), "접속 계정의 보안 등급(Role Token)에 따라 불필요한 기능 장벽을 제거하고 맞춤형 업무 화면 자동 공급", font=get_font(11, 'medium'), fill=(100, 116, 139))
    
    # 3 Flow Blocks for RBAC Process
    rbac_blocks = [
        ("01. 단일 인증 & 권한 인가", "User Authentication", "사용자 계정/단말기 고유 ID 인증 시 JWT 토큰 내 역할(CEO, Manager, Worker, Admin) 식별"),
        ("02. 동적 사이드바 메뉴 렌더링", "Dynamic Menu Dispatch", "권한 수준에 맞지 않는 메뉴는 DOM 자체에서 원천 비노출, 작업자는 1~2개 필수 메뉴만 경량 노출"),
        ("03. 화면 위젯 & 필드 레벨 통제", "Widget-Level RBAC", "CEO는 원가/마진율/인사지표 열람 가능, 현장 작업자는 민감 회계정보 차단 및 실적 입력 필드만 활성화")
    ]
    
    r_by = bot_sy + 82
    for b_idx, (b_title, b_sub, b_desc) in enumerate(rbac_blocks):
        draw.rounded_rectangle([lb_x + 24, r_by, lb_x + bot_w - 24, r_by + 68], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        # Number Pill
        draw.rounded_rectangle([lb_x + 40, r_by + 16, lb_x + 72, r_by + 38], radius=6, fill=(239, 246, 255))
        draw.text((lb_x + 56, r_by + 27), f"0{b_idx+1}", font=get_num_font(11, 'bold'), fill=(0, 81, 255), anchor='mm')
        
        draw.text((lb_x + 84, r_by + 27), b_title, font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((lb_x + 84, r_by + 49), b_desc, font=get_font(11, 'regular'), fill=(71, 85, 105), anchor='lm')
        
        r_by += 80
        
    # Bottom Benefit Matrix Pods
    draw.line([(lb_x + 24, r_by + 4), (lb_x + bot_w - 24, r_by + 4)], fill=(241, 245, 249), width=1)
    draw.text((lb_x + 24, r_by + 24), "권한 통제 도입 전 vs. 도입 후 운영 성과 비교", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    
    draw.rounded_rectangle([lb_x + 24, r_by + 42, lb_x + bot_w // 2 - 10, r_by + 104], radius=8, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((lb_x + 36, r_by + 58), "AS-IS (기존 구축형/일반 MES)", font=get_font(11, 'bold'), fill=(185, 28, 28))
    draw.text((lb_x + 36, r_by + 80), "· 모든 직원에게 50개 메뉴 전체 노출로 메뉴 탐색에 5분 소모\n· 작업자의 회계/단가 화면 접근으로 보안 유출 리스크 상존", font=get_font(10.5, 'regular'), fill=(127, 29, 29))
    
    draw.rounded_rectangle([lb_x + bot_w // 2 + 10, r_by + 42, lb_x + bot_w - 24, r_by + 104], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((lb_x + bot_w // 2 + 22, r_by + 58), "TO-BE (CodeBridgeX RBAC 자동 분기)", font=get_font(11, 'bold'), fill=(4, 120, 87))
    draw.text((lb_x + bot_w // 2 + 22, r_by + 80), "· 역할별 직무 맞춤 뷰 즉시 로딩으로 업무 진입 시간 99% 단축\n· 대표의 민감 인사/재무 데이터 완벽 보호 및 책임 추적성 확립", font=get_font(10.5, 'regular'), fill=(6, 95, 70))
    
    # 2. Right Card: CodeBridgeX Multi-Tenant SaaS Business Model
    rb_x = lb_x + bot_w + bot_gap
    draw.rounded_rectangle([rb_x, bot_sy, rb_x + bot_w, bot_sy + bot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rb_x + 24, cy=bot_sy + 26, text="SAAS BUSINESS MODEL", font=get_font(9.5, 'bold'), theme='purple', pad_x=8, height=22)
    draw.text((rb_x + 205, bot_sy + 26), "코드브릿지 멀티테넌트 SaaS 중앙 관제 비즈니스 구조", font=get_font(16.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((rb_x + 24, bot_sy + 52), "단일 클라우드 엔진 위에서 수백 개 고객사를 테넌트(Tenant)별로 격리 관리하는 구독형 B2B 비즈니스", font=get_font(11, 'medium'), fill=(100, 116, 139))
    
    saas_pillars = [
        ("CodeBridgeX 본사 슈퍼 관리자 (Master Console)", "전체 가입 고객사(테넌트) 실시간 헬스체크, 사용량 과금 및 라이선스 배포, 신규 제조 도메인 위젯 OTA 자동 업데이트"),
        ("고객사 테넌트 완전 격리 (Multi-Tenant Isolation)", "A사(자동차 부품), B사(정밀 금형), C사(전자 조립)의 데이터베이스 및 파일 저장소를 완벽히 분리하여 데이터 기밀 보장"),
        ("구독형 가격 모델 & 무중단 지속 확장 (SaaS Scale)", "수억 원대 SI 개발 비용 대신 월 구독 기반으로 도입 장벽을 파괴하고, 코드브릿지가 서버·보안·기능 개선을 전담 운영")
    ]
    
    s_by = bot_sy + 82
    for s_idx, (s_title, s_desc) in enumerate(saas_pillars):
        draw.rounded_rectangle([rb_x + 24, s_by, rb_x + bot_w - 24, s_by + 68], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        # Badge
        draw.rounded_rectangle([rb_x + 40, s_by + 16, rb_x + 72, s_by + 38], radius=6, fill=(245, 243, 255))
        draw.text((rb_x + 56, s_by + 27), f"0{s_idx+1}", font=get_num_font(11, 'bold'), fill=(124, 58, 237), anchor='mm')
        
        draw.text((rb_x + 84, s_by + 27), s_title, font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((rb_x + 84, s_by + 49), s_desc, font=get_font(11, 'regular'), fill=(71, 85, 105), anchor='lm')
        
        s_by += 80
        
    # SaaS 3-Tier Synergy Architecture Pod
    draw.line([(rb_x + 24, s_by + 4), (rb_x + bot_w - 24, s_by + 4)], fill=(241, 245, 249), width=1)
    draw.text((rb_x + 24, s_by + 24), "코드브릿지 ↔ 제조 고객사 상생 생태계 구조", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    
    box_w = (bot_w - 48 - 16) // 2
    draw.rounded_rectangle([rb_x + 24, s_by + 42, rb_x + 24 + box_w, s_by + 104], radius=8, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((rb_x + 36, s_by + 58), "코드브릿지 (플랫폼 운영사)", font=get_font(11.5, 'bold'), fill=(0, 81, 255))
    draw.text((rb_x + 36, s_by + 80), "· 테넌트 생성, 라이선스 관리, 인프라 보안 패치\n· 전 고객사 데이터 분석 기반 제조 AI 벤치마크 제공", font=get_font(10.5, 'regular'), fill=(30, 58, 138))
    
    draw.rounded_rectangle([rb_x + 24 + box_w + 16, s_by + 42, rb_x + bot_w - 24, s_by + 104], radius=8, fill=(245, 243, 255), outline=(221, 214, 254), width=1)
    draw.text((rb_x + 24 + box_w + 28, s_by + 58), "제조 고객사 (구독 파트너)", font=get_font(11.5, 'bold'), fill=(124, 58, 237))
    draw.text((rb_x + 24 + box_w + 28, s_by + 80), "· 대표는 언제 어디서나 전사 인사/공정 실시간 의사결정\n· 각 담당자는 권한에 맞춘 전용 화면에서 최고 효율 달성", font=get_font(10.5, 'regular'), fill=(76, 29, 149))

    draw_slide_footer(draw, 3)
    base.save(os.path.join(OUT_DIR, 'slide_03.png'))
    print("SAVED slide_03.png (Target Users & Roles - RBAC & SaaS Business Model)")

# SLIDE 04: Information Architecture (Exact Centered Tree)
def make_slide_04():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=4, 
        category_kr="IA & Access Structure | 정보 구조 및 역할별(RBAC) 접근성 계층", 
        title_black="전사 제조 라이프사이클을 관통하는 ", 
        title_blue="체계적인 정보 계층 및 권한별 메뉴 아키텍처", 
        subtitle_kr="접속 권한(CEO/관리자/작업자)에 따른 동적 메뉴 분기 및 기준정보부터 생산·품질·출하까지 연동된 멀티테넌트 SaaS IA"
    )
    
    root_x1, root_y1, root_x2, root_y2 = 640, 220, 1280, 284
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=12, fill=(255, 255, 255), outline=(0, 81, 255), width=2)
    root_cy = (root_y1 + root_y2) // 2
    b_root = draw_pill_badge(draw, left_x=root_x1 + 18, cy=root_cy, text="멀티테넌트 SaaS", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=26)
    draw.text((b_root[2] + 16, root_cy - 11), "CodeBridgeX Cloud MES & ERP 권한 연동 아키텍처", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((b_root[2] + 16, root_cy + 11), "코드브릿지 고객사 통합 관리 테넌트 엔진 및 3대 직무별 RBAC 자동 메뉴 분기", font=get_font(10.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    cols_data = [
        ("01. 기준정보 관리", "Master Data", "품목 마스터, 다단계 BOM 등록, 공정 라우팅, 거래처 및 작업자 규격 관리", [
            ("품목 관리", "원부자재 및 완제품 마스터"),
            ("BOM 관리", "N단 멀티레벨 BOM 트리"),
            ("공정 라우팅", "표준 작업 공순 및 사이클타임"),
            ("검사 기준", "공정별 AQL 품질 규격 마스터")
        ]),
        ("02. 영업 & 구매", "Sales & Purchase", "고객 견적 발행부터 수주 등록, 소요량 계산(MRP) 및 발주 입고 프로세스", [
            ("견적/수주", "자동 단가 계산 및 납기 시뮬레이션"),
            ("발주 관리", "BOM 소요량 기반 원자재 발주"),
            ("수입 검사", "입고 자재 LOT 합격/불량 판정"),
            ("매출/매입", "전자 세금계산서 및 원장 연동")
        ]),
        ("03. 생산 실행 (MES)", "Production Execution", "생산 계획 수립, 작업 지시서(Work Order) 발행, 실시간 공정 실적 추적", [
            ("생산 계획", "스마트 간트차트 기반 라인 스케줄링"),
            ("작업 지시", "호기별 LOT 작업 지시서 배포"),
            ("실적 수집", "양품/불량 수량 실시간 집계"),
            ("설비 OEE", "가동률, 성능, 품질 종합 효율 관제")
        ]),
        ("04. 품질 & 재고", "Quality & Inventory", "공정 검사, 출하 검사, 부적합품 시정조치(CAPA) 및 창고 위치별 재고 실사", [
            ("공정/출하 검사", "SPC 관리도 및 X-bar 통계 분석"),
            ("부적합 관리", "불량 원인 분석 및 재작업 승인"),
            ("창고 재고", "구역/로케이션별 실시간 재고량"),
            ("LOT 추적", "원자재-반제품-완제품 이력 추적")
        ]),
        ("05. 시스템 & 결재", "Admin & Workflow", "기업 테넌트 설정, 역할 기반 권한 통제(RBAC), 다단계 전자 결재 프로세스", [
            ("전자 결재", "기안 작성, 결재선 지정, 전결 처리"),
            ("권한 관리", "메뉴별/직무별 세분화된 접근 권한"),
            ("메뉴 설정", "드래그 앤 드롭 메뉴 커스터마이징"),
            ("로그 감사", "접속 및 데이터 변경 감사 추적")
        ]),
    ]
    
    cw = (W - 200 - 4 * 20) // 5
    col_xs = [100 + i * (cw + 20) for i in range(5)]
    
    draw.line([(960, root_y2), (960, 310)], fill=(0, 81, 255), width=2)
    draw.line([(col_xs[0] + cw // 2, 310), (col_xs[-1] + cw // 2, 310)], fill=(0, 81, 255), width=2)
    
    for i, (title, en, desc, subs) in enumerate(cols_data):
        cx = col_xs[i]
        center_x = cx + cw // 2
        draw.line([(center_x, 310), (center_x, 335)], fill=(0, 81, 255), width=2)
        
        draw.rounded_rectangle([cx, 335, cx + cw, 425], radius=10, fill=(239, 246, 255), outline=(0, 81, 255), width=1)
        draw.text((cx + 14, 348), title, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 14, 370), en, font=get_font(10, 'medium'), fill=(0, 81, 255))
        draw.text((cx + 14, 392), desc, font=get_font(9.5, 'regular'), fill=(71, 85, 105))
        
        sy = 445
        for s_title, s_desc in subs:
            draw.rounded_rectangle([cx, sy, cx + cw, sy + 115], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.text((cx + 14, sy + 18), s_title, font=get_font(12.5, 'bold'), fill=(15, 23, 42))
            draw.text((cx + 14, sy + 44), s_desc, font=get_font(10.5, 'medium'), fill=(71, 85, 105))
            draw_pill_badge(draw, left_x=cx + 14, cy=sy + 85, text="엔터프라이즈 모듈", font=get_font(8.5, 'bold'), theme='slate', pad_x=6, height=18)
            sy += 130
            
    draw_slide_footer(draw, 4)
    base.save(os.path.join(OUT_DIR, 'slide_04.png'))
    print("SAVED slide_04.png")

# ==============================================================
# SLIDE 05: User Flowchart with Formal Flowchart Symbols & Decision Diamonds
def make_slide_05():
    base = Image.new('RGB', (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=5, 
        category_kr="Order-to-Ship Workflow | 5단계 엔드투엔드 제조 워크플로우", 
        title_black="판단 분기와 실시간 검증을 포함한 ", 
        title_blue="5단계 서비스 UX 플로우차트", 
        subtitle_kr="수주 접수부터 MRP 소요량 검증, 작업지시 배포, 현장 실적 수집, 출하 품질 승인까지 정밀한 판단 기호 적용"
    )
    
    # Top-Right Legend Box
    leg_x = 1260
    leg_y = 65
    leg_w = 560
    leg_h = 75
    draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=leg_x + 16, cy=leg_y + 18, text="NOTATION", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18)
    draw.text((leg_x + 95, leg_y + 18), "플로우차트 표준 기호 범례", font=get_font(10.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 16, leg_y + 40, leg_x + 70, leg_y + 64], radius=10, fill=(0, 81, 255))
    draw.text((leg_x + 43, leg_y + 52), "Start/End", font=get_font(7, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((leg_x + 76, leg_y + 52), "시작/종료", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 140, leg_y + 40, leg_x + 190, leg_y + 64], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 165, leg_y + 52), "Screen", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((leg_x + 196, leg_y + 52), "화면/접점", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 265, leg_y + 40, leg_x + 315, leg_y + 64], radius=4, fill=(239, 246, 255), outline=(0, 81, 255), width=1)
    draw.text((leg_x + 290, leg_y + 52), "Action", font=get_font(7.5, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((leg_x + 322, leg_y + 52), "작업 행동", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw_diamond(draw, cx=leg_x + 405, cy=leg_y + 52, w=34, h=22, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw.text((leg_x + 405, leg_y + 52), "Decide", font=get_font(6.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((leg_x + 428, leg_y + 52), "판단 분기", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    # 5 STAGE COLUMNS
    col_w = (W - 200 - 4 * 24) // 5
    top_y = 220
    col_h = 740
    
    flow_steps = [
        ("01. 수주 접수", "영업본부", [
            ("Start", "고객사 주문 발주서 접수", "start"),
            ("Screen", "영업 수주 등록 화면", "screen"),
            ("Action", "품목 사양 및 수주 수량 입력", "action"),
            ("Decide", "납기 충족 가능한가?", "decide"),
            ("Action", "BOM 소요량 자동 계산(MRP)", "action")
        ]),
        ("02. 계획 & 발주", "생산관리팀", [
            ("Screen", "스마트 간트 스케줄러", "screen"),
            ("Action", "호기별 생산 일정 드래그 배정", "action"),
            ("Decide", "자재 재고 충분한가?", "decide"),
            ("Action", "부족 자재 구매 발주 자동 생성", "action"),
            ("Action", "작업 지시서(Work Order) 승인", "action")
        ]),
        ("03. 현장 투입", "공정 라인", [
            ("Screen", "호기별 디지털 작업표", "screen"),
            ("Action", "작업자 로그인 & 지시서 확인", "action"),
            ("Action", "원자재 바코드 스캔 & LOT 매핑", "action"),
            ("Decide", "투입 자재 LOT 일치?", "decide"),
            ("Action", "가공/조립 작업 개시 (가동)", "action")
        ]),
        ("04. 실시간 가공", "오퍼레이터", [
            ("Screen", "현장 터치 1-Tap 실적 등록", "screen"),
            ("Action", "양품 수량 & 불량 유형 터치 입력", "action"),
            ("Action", "설비 센서 OEE 텔레메트리 연동", "action"),
            ("Decide", "공정 불량 발생했는가?", "decide"),
            ("Action", "부적합품 CAPA 모달 즉시 호출", "action")
        ]),
        ("05. 검사 & 출하", "품질/물류팀", [
            ("Screen", "최종 품질 검사 & 성적서", "screen"),
            ("Action", "초·중·종물 AQL 규격 실측", "action"),
            ("Decide", "품질 합격 판정?", "decide"),
            ("Action", "완제품 출하 바코드 라벨 인쇄", "action"),
            ("End", "물류 창고 입고 & 출하 완료", "end")
        ])
    ]
    
    for ci, (c_title, c_team, nodes) in enumerate(flow_steps):
        cx = 100 + ci * (col_w + 24)
        draw.rounded_rectangle([cx, top_y, cx + col_w, top_y + col_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        draw_pill_badge(draw, left_x=cx + 18, cy=top_y + 28, text=f"단계 {ci+1}", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
        draw.text((cx + 80, top_y + 28), c_title, font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw_pill_badge(draw, left_x=cx + col_w - 95, cy=top_y + 28, text=c_team, font=get_font(9, 'bold'), theme='purple', pad_x=6, height=20)
        
        draw.line([(cx + 16, top_y + 55), (cx + col_w - 16, top_y + 55)], fill=(226, 232, 240), width=1)
        
        ny = top_y + 75
        for ni, (ntype, ntext, nkind) in enumerate(nodes):
            node_cx = cx + col_w // 2
            node_w = col_w - 36
            node_h = 75
            
            if nkind in ['start', 'end']:
                draw.rounded_rectangle([node_cx - node_w // 2, ny, node_cx + node_w // 2, ny + node_h], radius=node_h // 2, fill=(0, 81, 255))
                draw.text((node_cx, ny + 22), ntype.upper(), font=get_font(9, 'bold'), fill=(191, 219, 254), anchor='mm')
                draw.text((node_cx, ny + 48), ntext, font=get_font(11.5, 'bold'), fill=(255, 255, 255), anchor='mm')
            elif nkind == 'screen':
                draw.rounded_rectangle([node_cx - node_w // 2, ny, node_cx + node_w // 2, ny + node_h], radius=8, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
                draw.text((node_cx, ny + 22), "[UI SCREEN]", font=get_font(9, 'bold'), fill=(100, 116, 139), anchor='mm')
                draw.text((node_cx, ny + 48), ntext, font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='mm')
            elif nkind == 'action':
                draw.rounded_rectangle([node_cx - node_w // 2, ny, node_cx + node_w // 2, ny + node_h], radius=8, fill=(239, 246, 255), outline=(0, 81, 255), width=1)
                draw.text((node_cx, ny + 22), "▶ ACTION", font=get_font(9, 'bold'), fill=(0, 81, 255), anchor='mm')
                lines = textwrap.wrap(ntext, width=20)
                if len(lines) == 1:
                    draw.text((node_cx, ny + 48), lines[0], font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='mm')
                else:
                    draw.text((node_cx, ny + 40), lines[0], font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='mm')
                    draw.text((node_cx, ny + 56), lines[1], font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='mm')
            elif nkind == 'decide':
                draw_diamond(draw, cx=node_cx, cy=ny + node_h // 2, w=node_w, h=node_h, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
                draw.text((node_cx, ny + 24), "? DECISION", font=get_font(8.5, 'bold'), fill=(180, 83, 9), anchor='mm')
                draw.text((node_cx, ny + 46), ntext, font=get_font(11.5, 'bold'), fill=(180, 83, 9), anchor='mm')
                
            if ni < len(nodes) - 1:
                draw_arrow(draw, (node_cx, ny + node_h), (node_cx, ny + node_h + 38), col=(0, 81, 255), width=2, arrow_size=5)
            ny += node_h + 45
            
    draw_slide_footer(draw, 5)
    base.save(os.path.join(OUT_DIR, 'slide_05.png'))
    print("SAVED slide_05.png (Flowchart with Decisions & Symbols)")

# ==============================================================
# SLIDE 06: Wireframe & Screen Spec with Proportional Fit
def make_slide_06():
    # Consistent Pristine White Deck Background matching Slides 01, 02, 03, 04, 05, 07, 11
    base = Image.new('RGB', (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=6, 
        category_kr="와이어프레임 & 화면 설계서 | 섹션별 화면비율 & 기능 인터랙션 명세", 
        title_black="태블릿(16:10) & 모바일(9:16) 규격 분할, ", 
        title_blue="섹션별 실물 와이어프레임 & 핵심 인터랙션", 
        subtitle_kr="D:\\102_1.codebridgex\\MES Solution Website Structure 251229 실물 설계서 원본 비율과 4대 영역별 기능 인터랙션 상세 명세",
        dark_mode=False
    )
    
    # -------------------------------------------------------------
    # 4 High-Density Columns tailored to screen aspect ratios:
    # All 4 columns equalized in alignment & structural balance
    # -------------------------------------------------------------
    wf_specs = [
        {
            "col_w": 418,
            "title": "01. 태블릿 종합 대시보드",
            "ratio_tag": "16:10 가로형 (5120x3200)",
            "device": "10-inch 현장 관제 태블릿",
            "fname": "wf_clean_tablet.png",
            "desc": "경영진·공장장 실시간 OEE 및 종합 관제 뷰",
            "interactions": [
                ("상단 종합 KPI 위젯", "오늘의 생산량, 불량률, 재고현황, 수주현황 4대 카드를 1-Tap 클릭 시 해당 상세 모듈로 즉시 드릴다운 전환."),
                ("월별 생산 & 부서별 실적 차트", "기간/공정 필터 셀렉트박스 변경 시 실시간 비동기 차트 리렌더링 및 이상치 툴팁 호버 인터랙션."),
                ("긴급 작업 목록 & 알림 바", "라인별 병목 및 설비 알람 발생 시 붉은색 플래시 인디케이터 구동 및 즉시 작업지시 배포 모달 연결.")
            ]
        },
        {
            "col_w": 418,
            "title": "02. 모바일 생산 공정관리",
            "ratio_tag": "9:16 세로형 (1242x2208)",
            "device": "작업자 스마트폰 / 핸드헬드",
            "fname": "wf_clean_production.png",
            "desc": "호기별 작업지시서 배포 및 생산 실적 등록",
            "interactions": [
                ("1-Tap 바코드 스캔 매핑", "카메라/스캐너 연동으로 투입 원자재 LOT 번호 자동 인식 및 호기별 작업지시서에 1초 매핑."),
                ("대형 48px 터치 카운터", "방진 장갑 착용 환경을 고려한 대형 +/- 스테퍼 및 숫자 키패드로 양품/불량 수량 오입력 방지."),
                ("긴급 라인 홀드 & 비가동 보고", "설비 고장 및 자재 부족 시 원터치 비가동 사유 선택 바텀시트 호출 및 중앙 관제실 즉각 텔레메트리 전송.")
            ]
        },
        {
            "col_w": 418,
            "title": "03. 모바일 품질 보증/검사",
            "ratio_tag": "9:16 세로형 (1242x2208)",
            "device": "품질 검사관 전용 단말",
            "fname": "wf_clean_quality.png",
            "desc": "AQL 샘플링 검사 및 부적합 판정 체계",
            "interactions": [
                ("초·중·종물 AQL 규격 실측", "버니어 캘리퍼스 및 계측기 연동 블루투스 데이터 자동 수신으로 측정 오차 0% 달성."),
                ("실시간 합/부 자동 판정", "측정값이 마스터 규격 상/하한선(USL/LSL)을 벗어날 경우 시각적 경고음 및 불량 등급 자동 분류."),
                ("부적합품 CAPA 모달 구동", "불량 판정 즉시 현장 사진 촬영 첨부 및 재작업/폐기 승인 전자 결재선 자동 생성.")
            ]
        },
        {
            "col_w": 418,
            "title": "04. 공정 기준정보(라우팅)",
            "ratio_tag": "9:16 세로형 (2484x4416)",
            "device": "생산기술 엔지니어 단말",
            "fname": "wf_clean_process.png",
            "desc": "표준 공순 설계 및 설비 사이클타임 매핑",
            "interactions": [
                ("다단계 BOM 트리 탐색", "N단 제품 구성도를 아코디언 인터랙션으로 펼쳐 하위 반제품/원자재 소요량 즉시 파악."),
                ("드래그 앤 드롭 공순 재배치", "생산 라인 변경 시 공정 순서(Routing)를 터치 드래그로 순서 변경 및 표준공수 자동 재계산."),
                ("설비-작업자 자격 매핑", "호기별 요구 특수 자격증 및 인증 상태를 확인하여 미인증 작업자 배정 시 차단 경고 인터랙션.")
            ]
        }
    ]
    
    top_y = 205
    card_h = 810
    gap = 20
    curr_x = (W - (4 * 418 + 3 * gap)) // 2  # Perfectly centered on canvas: (1920 - 1732) // 2 = 94
    
    # Unified Wireframe Box Heights across all 4 columns for perfect alignment
    fixed_frame_h = 320
    inter_y = top_y + 102 + fixed_frame_h + 16  # Unified y=643 for all FUNCTION & INTERACTION SPEC headers
    single_card_h = 88
    card_gap = 10
    
    for idx, item in enumerate(wf_specs):
        cw = item["col_w"]
        
        # 1. Main Column Card (Clean White Surface, NO top accent stripe, NO left/right vertical bar)
        draw.rounded_rectangle(
            [curr_x, top_y, curr_x + cw, top_y + card_h], 
            radius=16, 
            fill=(255, 255, 255), 
            outline=(226, 232, 240), 
            width=1
        )
        
        # Badge & Device Header
        draw_pill_badge(draw, left_x=curr_x + 18, cy=top_y + 26, text=item["ratio_tag"], font=get_font(9.5, 'bold'), theme='blue', dark_mode=False, pad_x=8, height=22)
        draw.text((curr_x + cw - 18, top_y + 26), item["device"], font=get_font(10.5, 'medium'), fill=(100, 116, 139), anchor='rm')
        
        # Column Title & Subtitle
        draw.text((curr_x + 18, top_y + 54), item["title"], font=get_font(15, 'bold'), fill=(15, 23, 42))
        draw.text((curr_x + 18, top_y + 78), item["desc"], font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        
        # 2. Wireframe Screen Container (Unified fixed height for perfectly aligned bottom specs)
        frame_x = curr_x + 14
        frame_y = top_y + 102
        frame_w = cw - 28
        frame_h = fixed_frame_h
        
        draw.rounded_rectangle(
            [frame_x, frame_y, frame_x + frame_w, frame_y + frame_h], 
            radius=10, 
            fill=(248, 250, 252), 
            outline=(226, 232, 240), 
            width=1
        )
        
        fpath = os.path.join(MOCKUP_DIR, item["fname"])
        if os.path.exists(fpath):
            wf_img = Image.open(fpath).convert('RGB')
            sw, sh = wf_img.size
            
            # Precise edge crop to eliminate outer empty whitespace bands
            thresh = 242
            crop_top = 0
            for y in range(0, sh):
                if any(wf_img.getpixel((x, y))[0] < thresh for x in range(0, sw, 4)):
                    crop_top = max(0, y - 8)
                    break
            crop_bot = sh
            for y in range(sh - 1, -1, -1):
                if any(wf_img.getpixel((x, y))[0] < thresh for x in range(0, sw, 4)):
                    crop_bot = min(sh, y + 14)
                    break
            crop_left = 0
            for x in range(0, sw):
                if any(wf_img.getpixel((x, y))[0] < thresh for y in range(crop_top, crop_bot, 4)):
                    crop_left = max(0, x - 8)
                    break
            crop_right = sw
            for x in range(sw - 1, -1, -1):
                if any(wf_img.getpixel((x, y))[0] < thresh for y in range(crop_top, crop_bot, 4)):
                    crop_right = min(sw, x + 8)
                    break
                    
            if crop_right > crop_left and crop_bot > crop_top:
                wf_img = wf_img.crop((crop_left, crop_top, crop_right, crop_bot))
                
            src_w, src_h = wf_img.size
            avail_w = frame_w - 12
            avail_h = frame_h - 12
            
            # Fit inside frame preserving aspect ratio
            scale = min(avail_w / float(src_w), avail_h / float(src_h))
            target_w = int(round(src_w * scale))
            target_h = int(round(src_h * scale))
            
            wf_resized = wf_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            paste_x = frame_x + (frame_w - target_w) // 2
            paste_y = frame_y + (frame_h - target_h) // 2
            base.paste(wf_resized, (paste_x, paste_y))
            
            # Subtle crisp border around wireframe
            draw.rounded_rectangle(
                [paste_x - 1, paste_y - 1, paste_x + target_w + 1, paste_y + target_h + 1], 
                radius=4, 
                outline=(226, 232, 240), 
                width=1
            )
                
        # 3. Key Interaction Specifications Zone (Horizontally aligned across all columns)
        draw.line([(curr_x + 16, inter_y), (curr_x + cw - 16, inter_y)], fill=(241, 245, 249), width=1)
        
        draw_pill_badge(draw, left_x=curr_x + 18, cy=inter_y + 18, text="FUNCTION & INTERACTION SPEC", font=get_font(9, 'bold'), theme='blue', dark_mode=False, pad_x=8, height=20)
        
        by = inter_y + 36
        for f_idx, (f_name, f_desc) in enumerate(item["interactions"]):
            # Small interaction spec card (Clean white, NO left accent vertical stripe)
            draw.rounded_rectangle(
                [curr_x + 16, by, curr_x + cw - 16, by + single_card_h], 
                radius=8, 
                fill=(248, 250, 252), 
                outline=(226, 232, 240), 
                width=1
            )
            
            # Bullet Number Badge
            badge_cy = by + 20
            draw.ellipse([curr_x + 28, badge_cy - 8, curr_x + 44, badge_cy + 8], fill=(0, 81, 255))
            draw.text((curr_x + 36, badge_cy), str(f_idx + 1), font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
            
            # Function Title
            draw.text((curr_x + 52, badge_cy), f_name, font=get_font(12, 'bold'), fill=(0, 81, 255), anchor='lm')
            
            # Function Description lines
            lines = textwrap.wrap(f_desc, width=int(cw * 0.088))
            ly = by + 38
            for l in lines[:2]:
                draw.text((curr_x + 28, ly), l, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
                ly += 18
                
            by += single_card_h + card_gap
            
        curr_x += cw + gap

    draw_slide_footer(draw, 6, dark_mode=False)
    base.save(os.path.join(OUT_DIR, 'slide_06.png'))
    print("SAVED slide_06.png (Sectioned Wireframes with Exact Ratios & Tight Viewport Fit)")


def make_slide_07():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    # 1. Slide Header
    draw_slide_header(
        draw, 
        slide_num=7, 
        category_kr="디자인 시스템 | 브랜드 아이덴티티 & 아토믹 컴포넌트 아키텍처", 
        title_black="150개 이상의 표준 UI 에셋과 토큰으로 구축한 ", 
        title_blue="엔터프라이즈 디자인 시스템", 
        subtitle_kr="원자(Atoms), 분자(Molecules), 유기체(Organisms), 템플릿(Templates) 계층 및 기하학 키라인 조형 체계"
    )
    
    # Coordinates matching Behance Standard
    # Upper Row (y=214 to 554, h=340) - 3 Columns
    r1_y = 214
    r1_h = 340
    
    col1_x = 100
    col1_w = 540
    
    col2_x = 665
    col2_w = 540
    
    col3_x = 1230
    col3_w = 590
    
    # -------------------------------------------------------------
    # CARD 01 (Upper Left): MES CORE DESIGN PHILOSOPHY (UX & GUI)
    # -------------------------------------------------------------
    draw.rounded_rectangle([col1_x, r1_y, col1_x + col1_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b1_box = draw_pill_badge(draw, left_x=col1_x + 24, cy=r1_y + 30, text="FOUNDATION 01", font=get_font(9.5, 'bold'), theme='amber', has_dot=True, pad_x=8, height=22)
    draw.text((b1_box[2] + 14, r1_y + 30), "MES 제조 실행 핵심 디자인 철학 (UX & GUI)", font=get_font(13.0, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col1_x + 24, r1_y + 52), (col1_x + col1_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    principles = [
        ("01. Zero-Latency Ergonomics (무지연 현장 인체공학)", 
         "스마트 팩토리 방진 장갑 및 모바일·태블릿 조작에 맞춘 최소 48dp 터치 타깃",
         "현장 고조도 및 야간 교대근무 환경에 대응하는 WCAG AAA 12.8:1 고대비 테마", 
         (0, 81, 255)),
        ("02. Visual Role Hierarchy (역할별 시각적 우선순위)", 
         "CEO/공장장 핵심 KPI와 현장 오퍼레이터 공정 지시 화면의 정보 밀도 듀얼 최적화",
         "설비 가동(초록)·대기(주황)·비가동(빨강) 8종 시맨틱 뱃지 및 스쿼클 컬러 코딩", 
         (217, 119, 6)),
        ("03. Multi-Tenant Modularity (확장형 멀티테넌트)", 
         "고객사별 브랜드 로고, 컬러 팔레트, 커스텀 테넌트 테마 실시간 동적 주입",
         "13개 제조 업무 모듈 간 일관된 8pt 그리드 및 인터랙션 토큰 100% 바인딩", 
         (122, 34, 255))
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
    draw.text((col1_x + col1_w // 2, r1_y + r1_h - 26), "Core Principles: Zero-Latency Ergonomics · Visual Hierarchy · Multi-Tenant Modularity", font=get_font(8.8, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # CARD 02 (Upper Center): APP ICON GEOMETRIC DRAFTING GRID & SPEC (SAM S Symbol)
    # -------------------------------------------------------------
    draw.rounded_rectangle([col2_x, r1_y, col2_x + col2_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b2_box = draw_pill_badge(draw, left_x=col2_x + 24, cy=r1_y + 30, text="FOUNDATION 02", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22)
    draw.text((b2_box[2] + 14, r1_y + 30), "솔루션 S 심벌마크 기하학 와이어프레임 & 조형 규격", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col2_x + 24, r1_y + 52), (col2_x + col2_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    # Technical Drafting Blueprint Canvas Box
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
    
    # Keyline Grid Lines
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
    
    # App Icon centered (SAM S-Symbol Icon)
    icon_path = r"d:\097.flutter_project\auto_portfolio\assets\mes_solution_app_icon.png"
    if os.path.exists(icon_path):
        try:
            raw_icon = Image.open(icon_path).convert('RGBA')
            resized = raw_icon.resize((S, S), Image.Resampling.LANCZOS)
            
            s_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            sdraw = ImageDraw.Draw(s_layer)
            sdraw.rounded_rectangle([cx - S//2 + 2, cy - S//2 + 4, cx + S//2 + 2, cy + S//2 + 6], radius=r_corner + 2, fill=(15, 23, 42, 45))
            s_layer = s_layer.filter(ImageFilter.GaussianBlur(5))
            base.paste(s_layer, (0, 0), s_layer)
            
            icon_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            icon_layer.paste(resized, (cx - S//2, cy - S//2))
            base.paste(icon_layer, (0, 0), icon_layer)
            draw = ImageDraw.Draw(base)
            
            grid_white = (255, 255, 255, 175)
            draw.line([(cx - R, cy - R), (cx + R, cy + R)], fill=grid_white, width=1)
            draw.line([(cx - R, cy + R), (cx + R, cy - R)], fill=grid_white, width=1)
            draw.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], outline=grid_white, width=1)
            draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=grid_white, width=1)
            draw.rounded_rectangle([cx - S//2, cy - S//2, cx + S//2, cy + S//2], radius=r_corner, outline=(255, 255, 255, 220), width=1)
        except Exception as e:
            print("Icon paste error:", e)
            
    draw.text((cx, ic_box_y + ic_box_size + 13), "Golden Ratio Squircle Grid (1024×1024)", font=get_font(8.5, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((cx, ic_box_y + ic_box_size + 27), "Inner Ø288 · Mid Ø408 · Outer Ø680 · R22.5%", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    
    m_x = ic_box_x + ic_box_size + 16
    specs = [
        ("01. SAM 공식 헤더 S 심벌마크 (Smart Automation)", 
         "실제 앱 헤더 전역에 적용된 정통 SAM(Smart Automation) 심벌",
         "부드러운 곡선의 'S' 레터링으로 끊김 없는 공정 흐름을 형상화"),
        ("02. Dynamic Squircle Curvature (R22.5%)", 
         "모바일·태블릿 및 웹 데스크톱 런처에 일치하는 연속 곡률",
         "스쿼클 마스킹을 적용하여 디바이스별 선명도와 가독성 극대화"),
        ("03. 일렉트릭 블루 & 인더스트리얼 네이비", 
         "정밀함과 신뢰를 상징하는 시그니처 블루(#0051FF)와",
         "고대비 딥 네이비(#0F172A)의 조화로 0.1초 내 솔루션 식별력 완성")
    ]
    sy = r1_y + 64
    for title, l1, l2 in specs:
        draw.text((m_x, sy), title, font=get_font(10, 'bold'), fill=(0, 81, 255) if "01" in title else (15, 23, 42))
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
    draw.text((b3_box[2] + 14, r1_y + 30), "실제 앱 탑재 13개 모듈 & 시스템 24dp 아이코노그라피", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col3_x + 24, r1_y + 52), (col3_x + col3_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    draw.text((col3_x + 24, r1_y + 64), "Grid 24×24dp  ·  Optical Center  ·  Production Flutter Icons.*_rounded 토큰 1:1 바인딩", font=get_font(9, 'bold'), fill=(0, 81, 255))
    
    icons_data = [
        ("경영종합대시보드", "Icons.dashboard", 0xe871),
        ("생산 공정 관리", "Icons.precision_mfg", 0xf0094),
        ("품질 보증·SPC", "Icons.rule_rounded", 0xf012d),
        ("실시간 재고·BOM", "Icons.inventory_2", 0xf0001),
        ("IoT 설비 모니터링", "Icons.sensors", 0xe51f),
        ("기준정보 마스터", "Icons.table_chart", 0xe265),
        ("권한·보안 정책", "Icons.security", 0xe32a),
        ("시스템 설정 관리", "Icons.tune", 0xe429),
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
        draw.text((icx, icy), chr(icp), font=mat_font_icon, fill=(0, 81, 255), anchor='mm')
        
        draw.text((icx, iy + 53), iname, font=get_font(9.5, 'bold'), fill=(15, 23, 42), anchor='mm')
        draw.text((icx, iy + 68), itoken, font=get_font(7.5, 'bold'), fill=(0, 81, 255), anchor='mm')
        draw.text((icx, iy + 82), f"{hex(icp)} · 24dp", font=get_font(7.5, 'regular'), fill=(100, 116, 139), anchor='mm')
        
    draw.rounded_rectangle([col3_x + 24, r1_y + r1_h - 38, col3_x + col3_w - 24, r1_y + r1_h - 14], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((col3_x + col3_w // 2, r1_y + r1_h - 26), "Flutter 런타임 MaterialIcons-Regular.otf 실기기 렌더링 및 코드 토큰 100% 동기화", font=get_font(9.5, 'medium'), fill=(0, 81, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # LOWER ROW (y=574 to 950, h=376): 2 WIDE COLUMNS
    # -------------------------------------------------------------
    r2_y = 574
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
    draw.text((b4_box[2] + 14, r2_y + 32), "파운데이션 토큰 아키텍처 & Pretendard 타이포그래피", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(colA_x + 28, r2_y + 54), (colA_x + colA_w - 28, r2_y + 54)], fill=(241, 245, 249), width=1)
    
    col_w_inner = (colA_w - 56 - 20) // 2  # 382px
    
    # Left Half: Hero Color Swatch
    hb_y = r2_y + 64
    draw.rounded_rectangle([colA_x + 28, hb_y, colA_x + 28 + col_w_inner, hb_y + 58], radius=10, fill=(0, 81, 255))
    draw.text((colA_x + 42, hb_y + 12), "PRIMARY ELECTRIC BLUE", font=get_font(12, 'bold'), fill=(255, 255, 255))
    draw.text((colA_x + 42, hb_y + 28), "Color / Brand / Primary  ·  #0051FF", font=get_num_font(9, 'medium'), fill=(191, 219, 254))
    draw.text((colA_x + 42, hb_y + 42), "제조 공정의 정밀함과 실시간 제어를 상징하는 코어 블루", font=get_font(8, 'regular'), fill=(224, 242, 254))
    draw_pill_badge(draw, cx=colA_x + 28 + col_w_inner - 48, cy=hb_y + 29, text="8.4:1 AAA", font=get_font(8.5, 'bold'), theme='green', has_dot=False, pad_x=7, height=20)
    
    # 5 Semantic Swatches
    sub_swatches = [
        ("Secondary", "#3B82F6", (59, 130, 246), "보조 액션"),
        ("Operation", "#10B981", (16, 185, 129), "설비 정상 가동"),
        ("Standby", "#F59E0B", (245, 158, 11), "공정 대기·주의"),
        ("Alarm Stop", "#EF4444", (239, 68, 68), "비상 정지·불량"),
        ("Obsidian", "#0F172A", (15, 23, 42), "다크모드 서피스"),
    ]
    sw_w = (col_w_inner - 32) // 5
    sw_y = hb_y + 66
    for i, (s_name, s_hex, s_col, s_usage) in enumerate(sub_swatches):
        sx = colA_x + 28 + i * (sw_w + 8)
        draw.rounded_rectangle([sx, sw_y, sx + sw_w, sw_y + 58], radius=7, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([sx + 5, sw_y + 5, sx + sw_w - 5, sw_y + 20], radius=3, fill=s_col)
        draw.text((sx + 5, sw_y + 24), s_name, font=get_font(7.5, 'bold'), fill=(15, 23, 42))
        draw.text((sx + 5, sw_y + 35), s_hex, font=get_num_font(7.2, 'bold'), fill=(71, 85, 105))
        draw.text((sx + 5, sw_y + 46), s_usage, font=get_font(6.8, 'medium'), fill=(100, 116, 139))
        
    # Brand Gradients
    gr_y = sw_y + 68
    draw.text((colA_x + 28, gr_y), "시그니처 테넌트 그라디언트 (Brand Gradients):", font=get_font(9, 'bold'), fill=(71, 85, 105))
    gradients_data = [
        ("Primary Ocean", (0, 81, 255), (0, 210, 255)),
        ("Obsidian Surface", (15, 23, 42), (30, 41, 59)),
        ("SPC Control Band", (16, 185, 129), (5, 150, 105)),
        ("Warning Flush", (245, 158, 11), (239, 68, 68)),
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
        
    # Elevation Tokens Block
    el_y = gr_y + 48
    draw.text((colA_x + 28, el_y), "엘레베이션 & 뎁스 토큰 (Elevation Hierarchy):", font=get_font(9, 'bold'), fill=(71, 85, 105))
    elevations = [
        ("Elevation 1 (2dp)", "Y:2 Blur:4", "테이블·카드 서피스"),
        ("Elevation 2 (8dp)", "Y:8 Blur:16", "드롭다운·필터 팝오버"),
        ("Elevation 3 (16dp)", "Y:16 Blur:24", "작업지시 모달·드로어"),
    ]
    el_w = (col_w_inner - 16) // 3
    for idx, (el_title, el_spec, el_use) in enumerate(elevations):
        ex = colA_x + 28 + idx * (el_w + 8)
        ey = el_y + 14
        draw.rounded_rectangle([ex, ey, ex + el_w, ey + 42], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((ex + 8, ey + 6), el_title, font=get_font(7.5, 'bold'), fill=(0, 81, 255))
        draw.text((ex + 8, ey + 18), el_spec, font=get_num_font(7.2, 'medium'), fill=(100, 116, 139))
        draw.text((ex + 8, ey + 29), el_use, font=get_font(7, 'regular'), fill=(71, 85, 105))
        
    # Right Half: Typography & Radius Matrix
    ty_x = colA_x + 28 + col_w_inner + 20
    ty_w = col_w_inner
    
    t_rows = [
        ("Display 28", "Bold", "OEE 88.5% (가동률 정상)", True),
        ("Headline 20", "Bold", "실시간 설비 모니터링 현황", False),
        ("Title 16", "SemiBold", "작업 지시서 #WO-202611-042", False),
        ("Body 14", "Regular", "라인 #3 사출 공정 수량 1,200EA", False),
        ("Caption 11", "Medium", "OPC-UA 실시간 연동 (지연 0.04s)", False),
    ]
    ty_start = r2_y + 64
    for i, (t_role, t_weight, t_sample, is_mono) in enumerate(t_rows):
        ry = ty_start + i * 25
        draw.rounded_rectangle([ty_x, ry, ty_x + ty_w, ry + 21], radius=5, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((ty_x + 8, ry + 4), t_role, font=get_font(8.5, 'bold'), fill=(0, 81, 255))
        draw.text((ty_x + 85, ry + 4), t_weight, font=get_font(8, 'medium'), fill=(100, 116, 139))
        draw.text((ty_x + 138, ry + 4), t_sample, font=get_font(8, 'bold' if is_mono else 'regular'), fill=(15, 23, 42))
        
    # Radius & Spacing Tokens
    sp_box_y = ty_start + len(t_rows) * 25 + 6
    sp_box_h = (r2_y + r2_h - 26) - sp_box_y
    draw.rounded_rectangle([ty_x, sp_box_y, ty_x + ty_w, sp_box_y + sp_box_h], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((ty_x + 14, sp_box_y + 10), "시스템 코너 라운딩 & 8pt 그리드 스페이싱 토큰", font=get_font(9, 'bold'), fill=(15, 23, 42))
    
    rad_tokens = [
        ("Radius 4 (Sm)", "인풋 필드 · 뱃지 태그"),
        ("Radius 8 (Md)", "버튼 · 데이터 셀렉트"),
        ("Radius 12 (Lg)", "모듈 카드 · 패널 박스"),
        ("Radius 16 (Xl)", "컨테이너 · 모달 팝업"),
    ]
    for idx, (rt_name, rt_desc) in enumerate(rad_tokens):
        r_row_y = sp_box_y + 32 + idx * 26
        draw.rounded_rectangle([ty_x + 14, r_row_y, ty_x + 100, r_row_y + 20], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
        draw.text((ty_x + 57, r_row_y + 10), rt_name, font=get_font(7.5, 'bold'), fill=(0, 81, 255), anchor='mm')
        draw.text((ty_x + 110, r_row_y + 4), f"• {rt_desc}", font=get_font(7.5, 'regular'), fill=(71, 85, 105))
        
    draw.text((colA_x + 28, r2_y + r2_h - 17), "• WCAG 2.1 AAA 8.4:1 고대비율 준수 · CSS/Flutter 디자인 토큰 100% 동기화", font=get_font(8.5, 'medium'), fill=(100, 116, 139))
    
    # -------------------------------------------------------------
    # CARD 05 (Lower Right): ATOMIC UI COMPONENT KIT
    # -------------------------------------------------------------
    draw.rounded_rectangle([colB_x, r2_y, colB_x + colB_w, r2_y + r2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b5_box = draw_pill_badge(draw, left_x=colB_x + 28, cy=r2_y + 32, text="FOUNDATION 05", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22)
    draw.text((b5_box[2] + 14, r2_y + 32), "프로덕션 아토믹 UI 컴포넌트 킷 (150+ 에셋)", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(colB_x + 28, r2_y + 54), (colB_x + colB_w - 28, r2_y + 54)], fill=(241, 245, 249), width=1)
    
    k1_y = r2_y + 68
    k1_w = (colB_w - 56 - 20) // 2
    
    # Pod 1: Form Input with Icon & Validation
    draw.rounded_rectangle([colB_x + 28, k1_y, colB_x + 28 + k1_w, k1_y + 80], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((colB_x + 40, k1_y + 10), "작업 지시 바코드 / 품목 검색 인풋 (Input.tsx)", font=get_font(9.5, 'bold'), fill=(0, 81, 255))
    draw.text((colB_x + 40, k1_y + 30), "LOT-2026-X889", font=get_num_font(14, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=colB_x + 28 + k1_w - 45, cy=k1_y + 26, text="BARCODE", font=get_font(8.5, 'bold'), theme='cyan', pad_x=6, height=18)
    
    draw.rounded_rectangle([colB_x + 40, k1_y + 50, colB_x + 28 + k1_w - 12, k1_y + 72], radius=5, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((colB_x + 58, k1_y + 61), chr(0xe86c), font=get_material_icon_font(14), fill=(16, 185, 129), anchor='mm')
    draw.text((colB_x + 28 + k1_w // 2, k1_y + 61), "BOM 구조 일치 · 표준 자재 출고 승인", font=get_font(9, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    # Pod 2: KPI Live Metric Pod
    k2_x = colB_x + 28 + k1_w + 20
    draw.rounded_rectangle([k2_x, k1_y, k2_x + k1_w, k1_y + 80], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((k2_x + 14, k1_y + 10), "실시간 생산 OEE 종합 효율 (MetricCard.tsx)", font=get_font(9.5, 'bold'), fill=(0, 81, 255))
    draw.text((k2_x + 14, k1_y + 32), "94.8% (목표 92%)", font=get_font(13.5, 'bold'), fill=(15, 23, 42))
    draw.text((k2_x + 14, k1_y + 54), "시간가동률 98.2% · 양품률 99.4%", font=get_font(9, 'bold'), fill=(16, 185, 129))
    
    # Live Pill
    tog_x = k2_x + k1_w - 95
    draw.rounded_rectangle([tog_x, k1_y + 10, tog_x + 85, k1_y + 32], radius=11, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((tog_x + 42, k1_y + 21), "LIVE OP", font=get_font(8.5, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    # Preset Chips Row
    ch_y = k1_y + 92
    draw.text((colB_x + 28, ch_y + 6), "원클릭 공정 전환 프리셋 칩:", font=get_font(10, 'bold'), fill=(100, 116, 139))
    presets = [
        ("SMT 실장", (0, 81, 255), (239, 246, 255)),
        ("조립 #1", (0, 81, 255), (239, 246, 255)),
        ("검사 대기", (180, 83, 9), (254, 243, 199)),
        ("설비 점검", (220, 38, 38), (254, 242, 242)),
        ("출하 검사", (5, 150, 105), (236, 253, 245)),
        ("ERP 연동", (109, 40, 217), (245, 243, 255)),
        ("일괄 승인", (0, 81, 255), (239, 246, 255)),
    ]
    cur_ch_x = colB_x + 195
    for p_txt, p_col, p_bg in presets:
        draw.rounded_rectangle([cur_ch_x, ch_y, cur_ch_x + 82, ch_y + 26], radius=13, fill=p_bg, outline=p_col, width=1)
        draw.text((cur_ch_x + 41, ch_y + 13), p_txt, font=get_font(9.5, 'bold'), fill=p_col, anchor='mm')
        cur_ch_x += 89
        
    # CTAs Button Row
    cta_y = ch_y + 38
    mat_font_cta = get_material_icon_font(15)
    
    # 1. Primary Solid Button
    draw.rounded_rectangle([colB_x + 28, cta_y, colB_x + 230, cta_y + 40], radius=10, fill=(0, 81, 255))
    draw.text((colB_x + 50, cta_y + 20), chr(0xe037), font=mat_font_cta, fill=(255, 255, 255), anchor='mm')
    draw.text((colB_x + 138, cta_y + 20), "공정 시작 (Primary)", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # 2. Secondary Outline Button
    draw.rounded_rectangle([colB_x + 242, cta_y, colB_x + 432, cta_y + 40], radius=10, fill=(240, 246, 255), outline=(0, 81, 255), width=1)
    draw.text((colB_x + 264, cta_y + 20), chr(0xe5d5), font=mat_font_cta, fill=(0, 81, 255), anchor='mm')
    draw.text((colB_x + 347, cta_y + 20), "일정 재조정 (Outline)", font=get_font(11, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    # 3. Ghost / Action Button
    draw.rounded_rectangle([colB_x + 444, cta_y, colB_x + 614, cta_y + 40], radius=10, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((colB_x + 466, cta_y + 20), chr(0xf090), font=mat_font_cta, fill=(51, 65, 85), anchor='mm')
    draw.text((colB_x + 538, cta_y + 20), "엑셀 내보내기", font=get_font(10.5, 'bold'), fill=(51, 65, 85), anchor='mm')
    
    # 4. Danger Stop Button
    draw.rounded_rectangle([colB_x + 626, cta_y, colB_x + colB_w - 28, cta_y + 40], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((colB_x + 648, cta_y + 20), chr(0xe047), font=mat_font_cta, fill=(220, 38, 38), anchor='mm')
    draw.text((colB_x + 664 + (colB_w - 28 - 664)//2, cta_y + 12), "비상 정지 (Danger)", font=get_font(8.5, 'bold'), fill=(185, 28, 28), anchor='mm')
    draw.text((colB_x + 664 + (colB_w - 28 - 664)//2, cta_y + 26), "라인 즉시 셧다운 승인", font=get_font(8.5, 'bold'), fill=(220, 38, 38), anchor='mm')
    
    # Status Badges Row
    bdg_y = cta_y + 50
    draw.text((colB_x + 28, bdg_y + 6), "상태 뱃지 시스템:", font=get_font(10, 'bold'), fill=(100, 116, 139))
    badges = [
        ("설비 정상 가동", "green", True),
        ("공정 대기중", "amber", True),
        ("비상 알람 정지", "red", True),
        ("품질 검사 진행", "blue", True),
        ("ERP 실시간 연동", "slate", True),
        ("Multi-Tenant Ready", "purple", False),
    ]
    cur_bx = colB_x + 145
    for b_txt, b_thm, b_dt in badges:
        _, _, b_end, _ = draw_pill_badge(draw, left_x=cur_bx, cy=bdg_y + 14, text=b_txt, font=get_font(9.5, 'bold'), theme=b_thm, has_dot=b_dt, dark_mode=False, pad_x=8, height=24)
        cur_bx = b_end + 8
        
    draw.text((colB_x + 28, r2_y + r2_h - 18), "• 파운데이션 토큰 100% 바인딩: R4/R8/R12/R16 라운딩, 4/8pt 스페이싱, 시맨틱 컬러가 React & Flutter 트리에 실시간 동기화", font=get_font(9, 'regular'), fill=(100, 116, 139))
    
    draw_slide_footer(draw, 7)
    base.save(f'{OUT_DIR}/slide_07.png')
    print("SAVED slide_07.png (Visual Identity, App Icon & Atomic Component Kit)")


# ==============================================================
# SLIDE 08: Core Feature: Production & Scheduling (Dark UI Mode)
def make_slide_08():
    base = Image.new('RGB', (W, H), (15, 23, 42)) # Dark theme feature slide
    draw = ImageDraw.Draw(base)
    
    for gx in range(0, W, 40):
        draw.line([(gx, 0), (gx, H)], fill=(23, 33, 56), width=1)
    for gy in range(0, H, 40):
        draw.line([(0, gy), (W, gy)], fill=(23, 33, 56), width=1)
        
    draw_slide_header(
        draw, 
        slide_num=8, 
        category_kr="핵심 기능 | 역할별(RBAC) 맞춤 화면 & 실시간 스마트 공정 스케줄러", 
        title_black="대표의 인사·재무·공정 전사 관제부터 현장 배포까지, ", 
        title_blue="권한 기반 동적 UI & 인텔리전트 스케줄러", 
        subtitle_kr="접속 권한별 메뉴 자동 필터링(RBAC)과 수주 납기·설비 부하 기반 간트차트 실시간 호기별 배포 (현장 다크모드 적용)",
        dark_mode=True
    )
    
    lx, ly, lw, lh = 100, 220, 520, 740
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=14, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    
    draw_pill_badge(draw, left_x=lx + 30, cy=ly + 40, text="RBAC & 공정 혁신", font=get_font(10.5, 'bold'), theme='cyan', dark_mode=True, pad_x=12, height=28)
    draw.text((lx + 30, ly + 80), "직무별 맞춤 뷰 & 작업 지시", font=get_font(20, 'bold'), fill=(255, 255, 255))
    draw.text((lx + 30, ly + 115), "대표는 전사 인사/손익/공정을 한눈에 총괄 관제하고,\n각 현장 담당자에게는 권한에 최적화된 업무 화면만 제공합니다.", font=get_font(12.5, 'medium'), fill=(148, 163, 184))
    
    feats = [
        ("권한별(RBAC) 동적 사이드바", "대표 로그인 시 13개 전 모듈 활성화, 현장 작업자는 불필요한 메뉴를 차단하고 실적/비가동 화면만 자동 공급."),
        ("스마트 간트차트 일정 조정", "라인별 가동 현황과 잔여 케파를 시각화하여 마우스 드래그 앤 드롭으로 작업 순서 즉시 재배치."),
        ("자재 부족 사전 알림 (MRP)", "작업 지시 발행 전 필요한 원자재의 재고 유무를 검증하여 결품으로 인한 라인 정지 사전 예방."),
        ("멀티 디바이스 원격 즉각 대처", "대표는 출장/퇴근 중에도 모바일·태블릿으로 긴급 비가동 및 결재 요청을 실시간 확인하고 원클릭 승인.")
    ]
    
    fy = ly + 180
    for title, desc in feats:
        draw.rounded_rectangle([lx + 24, fy, lx + lw - 24, fy + 120], radius=10, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        draw.text((lx + 40, fy + 20), title, font=get_font(13.5, 'bold'), fill=(56, 189, 248))
        lines = textwrap.wrap(desc, width=33)
        ly_sub = fy + 48
        for l in lines:
            draw.text((lx + 40, ly_sub), l, font=get_font(11.5, 'medium'), fill=(203, 213, 225))
            ly_sub += 22
        fy += 135
        
    rx = 650
    rw = W - rx - 100
    dark_prod = os.path.join(MOCKUP_DIR, 'screen_03_production_dark.png')
    if not os.path.exists(dark_prod):
        dark_prod = os.path.join(MOCKUP_DIR, 'screen_03_production.png')
        
    draw_browser_frame(draw, base, rx, ly, rw, lh, dark_prod, "CodeBridgeX MES — 생산관리 & 작업지시 현황 (Dark Mode)", dark_mode=True)
    
    draw_slide_footer(draw, 8, dark_mode=True)
    base.save(os.path.join(OUT_DIR, 'slide_08.png'))
    print("SAVED slide_08.png (Dark Production Mode with RBAC Focus)")

# ==============================================================
# SLIDE 09: Core Feature: Full Traceability & Quality (Dark UI Mode)
def make_slide_09():
    base = Image.new('RGB', (W, H), (15, 23, 42)) # Dark theme feature slide
    draw = ImageDraw.Draw(base)
    
    for gx in range(0, W, 40):
        draw.line([(gx, 0), (gx, H)], fill=(23, 33, 56), width=1)
    for gy in range(0, H, 40):
        draw.line([(0, gy), (W, gy)], fill=(23, 33, 56), width=1)
        
    draw_slide_header(
        draw, 
        slide_num=9, 
        category_kr="핵심 기능 | 풀 트레이서빌리티 LOT 추적 & 무결점 품질 보증", 
        title_black="원자재 입고부터 고객사 납품까지, ", 
        title_blue="100% 추적 가능한 무결점 품질 체계", 
        subtitle_kr="SPC 관리도, 공정별 AQL 검사, 부적합품 시정조치(CAPA) 및 원터치 LOT 역추적 뷰어 제공 (현장 다크모드 적용)",
        dark_mode=True
    )
    
    lx, ly, lw, lh = 100, 220, 520, 740
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=14, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    
    draw_pill_badge(draw, left_x=lx + 30, cy=ly + 40, text="품질 경영 핵심 기능", font=get_font(10.5, 'bold'), theme='green', dark_mode=True, pad_x=12, height=28)
    draw.text((lx + 30, ly + 80), "품질 검사 & LOT 추적", font=get_font(20, 'bold'), fill=(255, 255, 255))
    draw.text((lx + 30, ly + 115), "수입 검사, 공정 검사, 출하 검사를 일원화하여 불량률을 42% 감소시키고,\n클레임 발생 시 1초 만에 전체 이력을 역추적합니다.", font=get_font(12.5, 'medium'), fill=(148, 163, 184))
    
    q_feats = [
        ("3단계 품질 게이트 (수입·공정·출하)", "검사 기준서(Inspection Standard) 마스터 기반 공정별 자동 합부 판정 및 측정 데이터 기록."),
        ("실시간 SPC 통계 관리도", "X-bar R 관리도 및 공정 능력 지수(Cpk) 실시간 분석으로 이상 징후 발생 전 사전 경보."),
        ("N단 LOT Full-Traceability", "완제품 시리얼 번호 조회 시 사용된 원자재 LOT, 담당 작업자, 가동 설비, 검사 성적서 1-Tap 조회."),
        ("부적합품 CAPA 시정 조치", "불량 발생 즉시 원인 분석 모달 구동 및 폐기/재작업 결재 라인 자동 연동으로 유출 원천 차단.")
    ]
    
    qy = ly + 180
    for title, desc in q_feats:
        draw.rounded_rectangle([lx + 24, qy, lx + lw - 24, qy + 120], radius=10, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        draw.text((lx + 40, qy + 20), title, font=get_font(13.5, 'bold'), fill=(52, 211, 153))
        lines = textwrap.wrap(desc, width=33)
        ly_sub = qy + 48
        for l in lines:
            draw.text((lx + 40, ly_sub), l, font=get_font(11.5, 'medium'), fill=(203, 213, 225))
            ly_sub += 22
        qy += 135
        
    rx = 650
    rw = W - rx - 100
    dark_qual = os.path.join(MOCKUP_DIR, 'screen_04_quality_dark.png')
    if not os.path.exists(dark_qual):
        dark_qual = os.path.join(MOCKUP_DIR, 'screen_04_quality.png')
        
    draw_browser_frame(draw, base, rx, ly, rw, lh, dark_qual, "CodeBridgeX MES — 품질관리 & 수입/공정 검사 현황 (Dark Mode)", dark_mode=True)
    
    draw_slide_footer(draw, 9, dark_mode=True)
    base.save(os.path.join(OUT_DIR, 'slide_09.png'))
    print("SAVED slide_09.png (Dark Quality Mode)")

# ==============================================================
# SLIDE 10: Production Showcase (6 Real Dark Mode & Responsive Screens)
def make_slide_10():
    # Sophisticated obsidian dark canvas
    base = Image.new('RGB', (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(base)
    
    for gx in range(0, W, 40):
        draw.line([(gx, 0), (gx, H)], fill=(23, 33, 56), width=1)
    for gy in range(0, H, 40):
        draw.line([(0, gy), (W, gy)], fill=(23, 33, 56), width=1)
        
    draw_slide_header(
        draw, 
        slide_num=10, 
        category_kr="프로덕션 화면 | 디바이스별 고유 비율 & 100% 리얼 다크모드 쇼케이스", 
        title_black="데스크톱(16:9), 태블릿(4:3), 모바일(19.5:9) ", 
        title_blue="디바이스별 종횡비 일치 & 리얼 다크모드 컬렉션", 
        subtitle_kr="기기별 하드웨어 규격에 맞춘 3대 폼팩터 화면 비율과 고대비 다크 테마(Dark Theme) 프로덕션 렌더링",
        dark_mode=True
    )
    
    # -------------------------------------------------------------
    # OPTIMIZED HIGH-DENSITY ZERO-WASTE LAYOUT:
    # Canvas H=1080, top_y = 205, col_h = 810 (ends at y=1015)
    # Total width: 1720px (left_margin=100, right_margin=100)
    #
    # 1. LEFT (x=100, w=640): 2 stacked 16:9 Desktop Cards
    #    - Proportion-matched width eliminating awkward side margins
    #    - d_card_h = 394px each (with 22px gap)
    #    - Screen viewport 616x324 tightly fits 16:9 (576x324) with NO dead margins
    #
    # 2. MIDDLE (x=764, w=650): Tablet (4:3) Showcase Card
    #    - Spacious, immersive 4:3 Tablet chassis (w=600, h=450) with bezel & camera
    #    - 3 rich spec pods below
    #
    # 3. RIGHT (x=1438, w=382): Mobile (19.5:9) Smartphone Card
    #    - High-presence smartphone chassis (w=252, h=530) with dynamic island
    #    - 3 ergonomic badge pods below
    # -------------------------------------------------------------
    top_y = 205
    col_h = 810
    gap = 24
    
    # -------------------------------------------------------------
    # 1. LEFT ZONE: 2 Desktop 16:9 Screens (w=640, col_h=810)
    # -------------------------------------------------------------
    left_x = 100
    left_w = 640
    d_card_h = (col_h - 22) // 2  # 394px
    
    desktop_screens = [
        ("01. 데스크톱 와이드 (16:9) · 경영 종합 대시보드 (Dark)", "screen_02_dashboard_dark.png", "FHD 1920x1080 · 전사 종합 KPI & OEE 실시간 관제"),
        ("02. 데스크톱 와이드 (16:9) · 생산 공정 스케줄러 (Dark)", "screen_03_production_dark.png", "FHD 1920x1080 · 스마트 간트차트 라인 배정 & 작업지시")
    ]
    
    for d_idx, (d_title, d_fname, d_sub) in enumerate(desktop_screens):
        dy = top_y + d_idx * (d_card_h + 22)
        draw.rounded_rectangle([left_x, dy, left_x + left_w, dy + d_card_h], radius=14, fill=(24, 34, 52), outline=(51, 65, 85), width=1)
        
        # Header bar inside card
        draw_pill_badge(draw, left_x=left_x + 14, cy=dy + 24, text="DESKTOP 16:9", font=get_font(9.5, 'bold'), theme='blue', dark_mode=True, pad_x=8, height=22)
        draw.text((left_x + 118, dy + 24), d_title, font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='lm')
        draw.text((left_x + left_w - 14, dy + 24), d_sub, font=get_font(9.5, 'medium'), fill=(148, 163, 184), anchor='rm')
        
        # Screen viewport (Tight fit, eliminating awkward horizontal blank margins)
        v_x = left_x + 12
        v_y = dy + 48
        v_w = left_w - 24   # 616px
        v_h = d_card_h - 60 # 334px
        
        draw.rounded_rectangle([v_x, v_y, v_x + v_w, v_y + v_h], radius=8, fill=(11, 16, 26), outline=(40, 53, 72), width=1)
        
        fpath = os.path.join(MOCKUP_DIR, d_fname)
        if os.path.exists(fpath):
            im = Image.open(fpath).convert('RGB')
            # 16:9 Scale to fit neatly inside viewport with minimal borders
            scale = min((v_w - 6) / im.width, (v_h - 6) / im.height)
            tw = int(round(im.width * scale))
            th = int(round(im.height * scale))
            im_res = im.resize((tw, th), Image.Resampling.LANCZOS)
            px = v_x + (v_w - tw) // 2
            py = v_y + (v_h - th) // 2
            base.paste(im_res, (px, py))
            draw.rounded_rectangle([px, py, px + tw, py + th], radius=4, outline=(71, 85, 105), width=1)
            
    # -------------------------------------------------------------
    # 2. MIDDLE ZONE: Tablet (4:3) Chassis (x=764, w=650, col_h=810)
    # -------------------------------------------------------------
    tab_x = left_x + left_w + gap # 764
    tab_w = 650
    draw.rounded_rectangle([tab_x, top_y, tab_x + tab_w, top_y + col_h], radius=14, fill=(24, 34, 52), outline=(51, 65, 85), width=1)
    
    draw_pill_badge(draw, left_x=tab_x + 16, cy=top_y + 24, text="TABLET 4:3", font=get_font(9.5, 'bold'), theme='cyan', dark_mode=True, pad_x=8, height=22)
    draw.text((tab_x + 115, top_y + 24), '03. 현장 10" 태블릿 (Dark)', font=get_font(13.5, 'bold'), fill=(255, 255, 255), anchor='lm')
    draw.text((tab_x + tab_w - 16, top_y + 24), "1024x768 (4:3 비율)", font=get_font(10.5, 'medium'), fill=(148, 163, 184), anchor='rm')
    
    # Sub-caption
    draw.text((tab_x + 16, top_y + 54), "현장 방진 태블릿 마운트 최적화 · 실시간 라인 OEE & 품질 모니터링", font=get_font(10.5, 'medium'), fill=(148, 163, 184))
    
    # Tablet Bezel Chassis (Expanded to take advantage of wider column)
    chassis_tab_y = top_y + 78
    chassis_tab_w = 600
    chassis_tab_h = 450 # 4:3 display (576x432) + bezels
    chassis_tab_x = tab_x + (tab_w - chassis_tab_w) // 2
    
    # Outer tablet body
    draw.rounded_rectangle([chassis_tab_x, chassis_tab_y, chassis_tab_x + chassis_tab_w, chassis_tab_y + chassis_tab_h], radius=22, fill=(9, 13, 22), outline=(51, 65, 85), width=2)
    
    # Front camera dot
    draw.ellipse([chassis_tab_x + chassis_tab_w // 2 - 3, chassis_tab_y + 8, chassis_tab_x + chassis_tab_w // 2 + 3, chassis_tab_y + 14], fill=(71, 85, 105))
    
    tab_fpath = os.path.join(MOCKUP_DIR, 'render_tablet_dashboard_dark.png')
    if os.path.exists(tab_fpath):
        tab_im = Image.open(tab_fpath).convert('RGB')
        tw_in = chassis_tab_w - 24 # 576px
        th_in = int(tw_in / 1.3333) # 432px
        tab_res = tab_im.resize((tw_in, th_in), Image.Resampling.LANCZOS)
        base.paste(tab_res, (chassis_tab_x + 12, chassis_tab_y + 16))
        draw.rounded_rectangle([chassis_tab_x + 12, chassis_tab_y + 16, chassis_tab_x + 12 + tw_in, chassis_tab_y + 16 + th_in], radius=6, outline=(40, 53, 72), width=1)
        
    # Tablet Feature Pods below chassis
    callout_y = chassis_tab_y + chassis_tab_h + 16
    draw.line([(tab_x + 16, callout_y), (tab_x + tab_w - 16, callout_y)], fill=(40, 53, 72), width=1)
    
    tab_specs = [
        ("대표 전사 원격 관제 (Executive Telemetry)", "외근/퇴근 중에도 공장 라인 OEE, 당일 출하, 미수금 현황을 4:3 최적화 대시보드로 실시간 확인 및 즉각 대처"),
        ("역할 기반 인터페이스 축소 (Role Adaptive)", "태블릿 접속 시 사이드 네비게이션이 아이콘 모드로 자동 접히며, 현장 필수 위젯 중심으로 터치 영역 극대화"),
        ("현장 조도 대응 고대비 다크 테마 (OLED 99%)", "어두운 조도의 생산 현장에서 눈부심을 차단하며 시각 피로도 70% 경감 및 산업용 단말 배터리 소모 절감")
    ]
    
    pod_y = callout_y + 14
    for t_idx, (t_title, t_desc) in enumerate(tab_specs):
        pod_h = 68
        draw.rounded_rectangle([tab_x + 16, pod_y, tab_x + tab_w - 16, pod_y + pod_h], radius=8, fill=(15, 23, 42), outline=(40, 53, 72), width=1)
        draw.ellipse([tab_x + 28, pod_y + 16, tab_x + 36, pod_y + 24], fill=(56, 189, 248))
        draw.text((tab_x + 44, pod_y + 12), t_title, font=get_font(11.5, 'bold'), fill=(56, 189, 248))
        
        lines = textwrap.wrap(t_desc, width=54)
        ly = pod_y + 36
        for l in lines[:2]:
            draw.text((tab_x + 44, ly), l, font=get_font(10, 'regular'), fill=(203, 213, 225))
            ly += 16
            
        pod_y += pod_h + 10
        
    # -------------------------------------------------------------
    # 3. RIGHT ZONE: Mobile (19.5:9) Smartphone Chassis (x=1438, w=382, col_h=810)
    # -------------------------------------------------------------
    mob_x = tab_x + tab_w + gap # 1438
    mob_w = 382
    draw.rounded_rectangle([mob_x, top_y, mob_x + mob_w, top_y + col_h], radius=14, fill=(24, 34, 52), outline=(51, 65, 85), width=1)
    
    draw_pill_badge(draw, left_x=mob_x + 14, cy=top_y + 24, text="MOBILE 19.5:9", font=get_font(9.5, 'bold'), theme='purple', dark_mode=True, pad_x=6, height=22)
    draw.text((mob_x + 115, top_y + 24), "04. 스마트폰 (Dark)", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='lm')
    draw.text((mob_x + 14, top_y + 54), "390x844 핸드헬드 터치 UI", font=get_font(10.5, 'medium'), fill=(148, 163, 184))
    
    # Phone Bezel Chassis (Expanded size for high presence)
    chassis_mob_y = top_y + 78
    chassis_mob_w = 252
    chassis_mob_h = 530  # 19.5:9 proportion
    chassis_mob_x = mob_x + (mob_w - chassis_mob_w) // 2
    
    # Phone outer frame
    draw.rounded_rectangle([chassis_mob_x, chassis_mob_y, chassis_mob_x + chassis_mob_w, chassis_mob_y + chassis_mob_h], radius=28, fill=(9, 13, 22), outline=(51, 65, 85), width=2)
    
    # Dynamic Island
    draw.rounded_rectangle([chassis_mob_x + chassis_mob_w // 2 - 26, chassis_mob_y + 8, chassis_mob_x + chassis_mob_w // 2 + 26, chassis_mob_y + 20], radius=6, fill=(0, 0, 0))
    
    mob_fpath = os.path.join(MOCKUP_DIR, 'render_mobile_dashboard_dark.png')
    if os.path.exists(mob_fpath):
        mob_im = Image.open(mob_fpath).convert('RGB')
        scale_m = min((chassis_mob_w - 12) / mob_im.width, (chassis_mob_h - 34) / mob_im.height)
        mw_real = int(round(mob_im.width * scale_m))
        mh_real = int(round(mob_im.height * scale_m))
        mob_res = mob_im.resize((mw_real, mh_real), Image.Resampling.LANCZOS)
        
        m_paste_x = chassis_mob_x + (chassis_mob_w - mw_real) // 2
        m_paste_y = chassis_mob_y + 24
        base.paste(mob_res, (m_paste_x, m_paste_y))
        draw.rounded_rectangle([m_paste_x, m_paste_y, m_paste_x + mw_real, m_paste_y + mh_real], radius=14, outline=(40, 53, 72), width=1)
        
    # Mobile Feature Bullets below chassis
    m_callout_y = chassis_mob_y + chassis_mob_h + 14
    draw.line([(mob_x + 14, m_callout_y), (mob_x + mob_w - 14, m_callout_y)], fill=(40, 53, 72), width=1)
    
    mob_pods = [
        ("한 손 터치 인체공학", "모든 핵심 액션 바텀 네비게이션 배치", (167, 139, 250)),
        ("1-Tap 실적 즉시 등록", "바코드 스캔 및 48px 대형 터치 키패드", (56, 189, 248)),
        ("실시간 긴급 푸시 알림", "비가동·불량 알림 즉시 수신 및 원격 승인", (52, 211, 153))
    ]
    
    m_pod_y = m_callout_y + 12
    for mp_title, mp_desc, mp_color in mob_pods:
        mpod_h = 46
        draw.rounded_rectangle([mob_x + 12, m_pod_y, mob_x + mob_w - 12, m_pod_y + mpod_h], radius=6, fill=(15, 23, 42), outline=(40, 53, 72), width=1)
        draw.text((mob_x + 20, m_pod_y + 8), f"• {mp_title}", font=get_font(10.5, 'bold'), fill=mp_color)
        draw.text((mob_x + 20, m_pod_y + 26), mp_desc, font=get_font(9.5, 'regular'), fill=(203, 213, 225))
        m_pod_y += mpod_h + 8

    draw_slide_footer(draw, 10, dark_mode=True)
    base.save(os.path.join(OUT_DIR, 'slide_10.png'))
    print("SAVED slide_10.png (Device Proportions & 100% Real Dark Mode Showcase)")


def make_slide_11():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=11, 
        category_kr="비즈니스 임팩트 | 정량적 성과 지표 & STAR 회고", 
        title_black="도입 기업의 제조 경쟁력을 획기적으로 향상시킨 ", 
        title_blue="Project Outcome & Key Metrics", 
        subtitle_kr="데이터 수집 시간 단축, 불량률 감소, 납기 준수율 향상 등 검증된 엔터프라이즈 DX 지표와 설계 회고"
    )
    
    # -------------------------------------------------------------
    # 1. TOP METRICS CARDS (4 Columns)
    # Total width: 1720px (left: 100, right: 100).
    # -------------------------------------------------------------
    metrics = [
        ("실적 집계 소요 시간", "24시간 → 1초", "▼ 99.9% 단축", "현장 종이 작업일지 취합에서\n웹 1-Tap 실시간 수집으로 전면 전환", "blue"),
        ("공정 불량률 감소", "3.8% → 1.2%", "▼ 42.0% 감소", "3단계 품질 게이트와 실시간\nSPC 관리도로 불량 유출 사전 차단", "green"),
        ("납기 준수율 (OTD)", "84.2% → 98.7%", "▲ 14.5%p 향상", "스마트 간트 스케줄러와 BOM\n자재 사전 결품 방지 알고리즘 적용", "purple"),
        ("작업자 교육 시간", "2주 → 2일", "▼ 85.0% 단축", "3단 반응형 표준 UI/UX 도입으로\n현장 신규 작업자 진입 장벽 최소화", "amber"),
    ]
    
    gap = 20
    mw = (1720 - 3 * gap) // 4  # 415px
    top_y = 205
    mh = 195
    
    for i, (label, val, delta, desc, theme) in enumerate(metrics):
        cx = 100 + i * (mw + gap)
        
        # White card with soft border
        draw.rounded_rectangle([cx, top_y, cx + mw, top_y + mh], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Inner padding: 22px left/right
        draw_pill_badge(draw, left_x=cx + 22, cy=top_y + 30, text=label, font=get_font(10.5, 'bold'), theme=theme, pad_x=10, height=24)
        
        # Primary Metric Value & Delta side-by-side or stacked cleanly
        draw.text((cx + 22, top_y + 75), val, font=get_font(21, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw_pill_badge(draw, left_x=cx + 22, cy=top_y + 115, text=delta, font=get_font(10, 'bold'), theme='solid' if theme=='blue' else theme, solid=True, pad_x=10, height=22)
        
        # Description text
        desc_lines = desc.split('\n')
        d_y = top_y + 146
        for dl in desc_lines:
            draw.text((cx + 22, d_y), dl, font=get_font(10.5, 'regular'), fill=(100, 116, 139))
            d_y += 18
            
    # -------------------------------------------------------------
    # 2. BOTTOM STAR RETROSPECTIVE: 4 Modular Cards Grid (2x2)
    # Outer frame: x=100, y=422, w=1720, h=595
    # -------------------------------------------------------------
    star_box_y = 422
    star_box_h = 595
    draw.rounded_rectangle([100, star_box_y, 100 + 1720, star_box_y + star_box_h], radius=16, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    # Section Header inside Container
    draw_pill_badge(draw, left_x=130, cy=star_box_y + 36, text="STAR METHOD RETROSPECTIVE", font=get_font(10, 'bold'), theme='blue', pad_x=12, height=26)
    draw.text((370, star_box_y + 36), "스마트 팩토리 엔터프라이즈 UX/UI 아키텍처 구축 회고 (200자 이상)", font=get_font(18, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((100 + 1720 - 30, star_box_y + 36), "기획 · 디자인 시스템 · 반응형 퍼블리싱 · 성능 최적화 100% 단독 수행", font=get_font(11.5, 'medium'), fill=(100, 116, 139), anchor='rm')
    
    # Divider line
    draw.line([(130, star_box_y + 64), (100 + 1720 - 30, star_box_y + 64)], fill=(226, 232, 240), width=1)
    
    # 4 Modular Grid Cards (2x2)
    grid_x = 130
    grid_y = star_box_y + 80
    grid_w = 1720 - 60 # 1660px
    col_w = (grid_w - 20) // 2 # 820px
    card_h = (star_box_h - 100) // 2 # 247px
    
    star_cards = [
        {
            "tag": "SITUATION",
            "tag_theme": "blue",
            "title": "Situation (도입 배경 및 현장 문제점)",
            "subtitle": "파편화된 레거시 시스템과 수작업 일지 체계의 한계",
            "body": "중소·중견 제조 현장의 90% 이상이 종이 작업 일지와 파편화된 엑셀 시트로 생산 실적을 관리하여 극심한 재고 오차와 납기 지연이 만성화되어 있었습니다. 특히 기존 외산 레거시 ERP의 복잡하고 난해한 메뉴 구조와 낮은 반응성으로 인해 공장 현장 오퍼레이터의 시스템 사용 기피 및 데이터 누락 문제가 심각했습니다."
        },
        {
            "tag": "TASK",
            "tag_theme": "purple",
            "title": "Task (핵심 설계 과제 및 목표)",
            "subtitle": "경영진-현장 작업자를 잇는 올인원 반응형 아키텍처",
            "body": "경영진에게는 전사 KPI, OEE, 수주·출고를 초단위로 시각화하는 Executive 관제 대시보드를 제공하고, 현장 작업자에게는 안전 장갑을 착용한 상태에서도 3초 내에 실적을 1-Tap으로 등록할 수 있는 인체공학적 멀티 폼팩터(데스크톱, 태블릿, 모바일) 웹 MES 아키텍처를 100% 단독 설계·구축해야 했습니다."
        },
        {
            "tag": "ACTION",
            "tag_theme": "amber",
            "title": "Action (구체적 실행 및 엔지니어링 전략)",
            "subtitle": "아토믹 디자인 시스템 150종과 고성능 반응형 엔진 구현",
            "body": "Vite + React 18 및 Tailwind CSS 기반으로 150여 종의 아토믹 디자인 토큰과 59개 표준 화면 규격을 설계했습니다. 수만 건의 LOT 이력을 렌더링 지연 없이 탐색할 수 있는 가상 스크롤 데이터 그리드, 스마트 간트차트 공정 스케줄러, 실시간 품질 SPC 이상 감지 차트 및 1-Tap 바코드 스캔 뷰어를 전면 구현했습니다."
        },
        {
            "tag": "RESULT",
            "tag_theme": "green",
            "title": "Result (정량적 성과 및 정성적 회고)",
            "subtitle": "검증된 DX 생산성 지표와 완성도 높은 엔터프라이즈 UX",
            "body": "도입 기업 실측 결과 실적 집계 소요 시간을 24시간에서 1초(99.9% 단축)로 개선하고, 3단계 품질 게이트로 공정 불량률 42% 감소, 납기 준수율 98.7%를 달성했습니다. 직관적인 3단 반응형 UI 체계 덕분에 현장 신규 작업자의 적응 교육 기간을 2주에서 2일(85% 단축)로 획기적으로 경감시켰습니다."
        }
    ]
    
    positions = [
        (grid_x, grid_y),
        (grid_x + col_w + 20, grid_y),
        (grid_x, grid_y + card_h + 16),
        (grid_x + col_w + 20, grid_y + card_h + 16)
    ]
    
    for idx, (sc, (px, py)) in enumerate(zip(star_cards, positions)):
        # Card Background
        draw.rounded_rectangle([px, py, px + col_w, py + card_h], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Left Accent Border
        accent_color = (0, 81, 255) if sc['tag_theme'] == 'blue' else ((147, 51, 234) if sc['tag_theme'] == 'purple' else ((217, 119, 6) if sc['tag_theme'] == 'amber' else (22, 163, 74)))
        draw.rounded_rectangle([px, py, px + 5, py + card_h], radius=3, fill=accent_color)
        
        # Card Header: Tag Badge + Title
        draw_pill_badge(draw, left_x=px + 22, cy=py + 26, text=sc['tag'], font=get_font(9.5, 'bold'), theme=sc['tag_theme'], pad_x=8, height=22)
        draw.text((px + 105, py + 26), sc['title'], font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        
        # Subtitle
        draw.text((px + 22, py + 56), sc['subtitle'], font=get_font(11, 'bold'), fill=accent_color)
        
        # Inner Divider
        draw.line([(px + 22, py + 74), (px + col_w - 22, py + 74)], fill=(241, 245, 249), width=1)
        
        # Body text wrapping with balanced line length (width=62)
        lines = textwrap.wrap(sc['body'], width=62)
        by = py + 90
        for line in lines:
            draw.text((px + 22, by), line, font=get_font(11, 'regular'), fill=(71, 85, 105))
            by += 21

    draw_slide_footer(draw, 11)
    base.save(os.path.join(OUT_DIR, 'slide_11.png'))
    print("SAVED slide_11.png (Redesigned STAR 4-Card Grid & High Density Margins)")


# ==============================================================
# SLIDE 12: Live Prototype & Interactive Hub (Dark Mode Finale)
def make_slide_12():
    # -------------------------------------------------------------
    # SLIDE 12: GRAND FINALE LIVE INTERACTIVE PROTOTYPE HUB
    # High-performance enterprise dark obsidian background with subtle grid & ambient glows
    # -------------------------------------------------------------
    base = Image.new('RGBA', (W, H), (15, 23, 42, 255))
    
    # Ambient radial cyan/blue glow behind devices & master launcher
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([150, 150, 800, 850], fill=(0, 81, 255, 30))
    gd.ellipse([900, 100, 1800, 950], fill=(6, 182, 212, 25))
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    base = Image.alpha_composite(base, glow)
    
    draw = ImageDraw.Draw(base)
    for gx in range(0, W, 40):
        draw.line([(gx, 0), (gx, H)], fill=(23, 33, 56, 180), width=1)
    for gy in range(0, H, 40):
        draw.line([(0, gy), (W, gy)], fill=(23, 33, 56, 180), width=1)
        
    draw_slide_header(
        draw, 
        slide_num=12, 
        category_kr="라이브 인터랙티브 프로토타입 | CLOUD MES WEB ENGINE", 
        title_black="웹 브라우저에서 바로 조작하는 ", 
        title_blue="차세대 스마트 팩토리 실시간 시뮬레이터", 
        subtitle_kr="정적인 슬라이드를 넘어 데스크톱, 10인치 태블릿, 모바일 뷰포트에서 전사 생산·품질 파이프라인을 직접 조작해 보세요.",
        dark_mode=True
    )
    
    # -------------------------------------------------------------
    # LEFT COLUMN (x=100, w=680): 3D MULTI-DEVICE MOCKUP SHOWCASE + SPEC STRIP
    # -------------------------------------------------------------
    lx = 100
    lw = 680
    
    # Render Multi-Device Trio Mockup with soft realistic shadow
    trio_thumb = "assets/mes_hero_device_trio.png"
    if os.path.exists(trio_thumb):
        trio_img = Image.open(trio_thumb).convert('RGBA')
        
        # Scale to fit upper left zone (w=680, h=560)
        scale = min(680 / trio_img.width, 560 / trio_img.height)
        tw = int(round(trio_img.width * scale))
        th = int(round(trio_img.height * scale))
        trio_res = trio_img.resize((tw, th), Image.Resampling.LANCZOS)
        
        paste_x = lx + (lw - tw) // 2
        paste_y = 230 + (560 - th) // 2
        
        # Ambient drop shadow
        sh_img = Image.new('RGBA', (tw + 100, th + 100), (0, 0, 0, 0))
        mask = trio_res.split()[3]
        black = Image.new('RGBA', trio_res.size, (0, 0, 0, 160))
        sh_img.paste(black, (50, 50 + 20), mask)
        sh_filtered = sh_img.filter(ImageFilter.GaussianBlur(32))
        base.paste(sh_filtered, (paste_x - 50, paste_y - 50), sh_filtered)
        
        base.paste(trio_res, (paste_x, paste_y), trio_res)
        draw = ImageDraw.Draw(base)
        
    # Floating C-Symbol App Icon Badge
    icon_path = "assets/mes_solution_app_icon.png"
    if os.path.exists(icon_path):
        ic = Image.open(icon_path).convert('RGBA')
        ic_w = 68
        ic_res = ic.resize((ic_w, ic_w), Image.Resampling.LANCZOS)
        badge_box = Image.new('RGBA', (88, 88), (0, 0, 0, 0))
        bd = ImageDraw.Draw(badge_box)
        bd.rounded_rectangle([0, 0, 88, 88], radius=20, fill=(30, 41, 59, 230), outline=(56, 189, 248), width=2)
        badge_box.paste(ic_res, (10, 10), ic_res)
        base.paste(badge_box, (lx + 20, 245), badge_box)
        draw = ImageDraw.Draw(base)
        
    # Left Bottom Spec Strip (x=100, y=825, w=680, h=185) - Dark Glass Card
    draw.rounded_rectangle([lx, 825, lx + lw, 1010], radius=14, fill=(24, 34, 52, 240), outline=(51, 65, 85), width=1)
    draw_pill_badge(draw, left_x=lx + 20, cy=850, text="RESPONSIVE 3-DEVICE SIMULATOR", font=get_font(9.5, 'bold'), theme='cyan', dark_mode=True, pad_x=10, height=22)
    draw.text((lx + 285, 850), "FHD 1080p · 4:3 Tablet · 19.5:9 Mobile", font=get_font(10.5, 'medium'), fill=(148, 163, 184), anchor='lm')
    
    spec_bullets = [
        ("단일 소스 3단 멀티 폼팩터", "데스크톱 대형 관제판부터 현장 10인치 태블릿, 모바일 뷰포트까지 100% 최적화"),
        ("13개 표준 비즈니스 모듈", "수주/출고, 간트차트 생산스케줄러, 3단계 품질 게이트, 바코드 LOT 추적 즉시 실행"),
        ("엔터프라이즈 프라이빗 보안", "데이터 외부 유출 없는 로컬 세션 스토리지 기반 안전한 실시간 가상 데모 지원")
    ]
    by = 882
    for b_title, b_desc in spec_bullets:
        draw.text((lx + 20, by), f"• {b_title} :", font=get_font(11, 'bold'), fill=(56, 189, 248))
        draw.text((lx + 185, by), b_desc, font=get_font(10.5, 'regular'), fill=(203, 213, 225))
        by += 26

    # -------------------------------------------------------------
    # RIGHT COLUMN (x=810, w=1010): MASTER LAUNCHER + 4 FLOW STEPS + LIVE QR CARD
    # -------------------------------------------------------------
    rx = 810
    rw = 1010
    proto_entry_url = "https://koyotejw-ux.github.io/auto_portfolio/mes_solution/index.html"
    
    # 1. PRIMARY HERO: MASTER LAUNCHER (y=210 to 326, h=116)
    # Vibrant Cyan/Blue Gradient Card
    my = 210
    mh = 116
    
    m_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    mgd = ImageDraw.Draw(m_glow)
    mgd.rounded_rectangle([rx - 6, my - 2, rx + rw + 6, my + mh + 8], radius=24, fill=(0, 81, 255, 90))
    m_glow = m_glow.filter(ImageFilter.GaussianBlur(24))
    base = Image.alpha_composite(base, m_glow)
    
    # Linear Gradient (Cyan #0284C7 to Electric Blue #0051FF)
    import numpy as np
    t = np.linspace(0, 1, rw, endpoint=True, dtype=np.float32)
    r_arr = (2 * (1 - t) + 0 * t).astype(np.uint8)
    g_arr = (132 * (1 - t) + 81 * t).astype(np.uint8)
    b_arr = (199 * (1 - t) + 255 * t).astype(np.uint8)
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
    
    # Launcher Content
    badge_w = 145
    draw.rounded_rectangle([rx + 24, my + 14, rx + 24 + badge_w, my + 36], radius=11, fill=(15, 23, 42, 210), outline=(255, 255, 255, 180), width=1)
    draw.text((rx + 24 + badge_w // 2, my + 25), "MASTER LAUNCHER", font=get_font(9.5, 'bold'), fill=(56, 189, 248), anchor='mm')
    
    draw.text((rx + 24, my + 60), "웹 브라우저에서 MES 전체 솔루션 인터랙티브 실행하기 ↗", font=get_font(18, 'bold'), fill=(255, 255, 255), anchor='lm')
    draw.text((rx + 24, my + 90), "실시간 텔레메트리 대시보드, 간트 공정 제어, 모바일 바코드 LOT 추적을 즉시 체험하세요.", font=get_font(12, 'medium'), fill=(224, 242, 254), anchor='lm')
    
    # Action Button
    btn_w = 210
    btn_h = 48
    btn_rx = rx + rw - btn_w - 24
    btn_ry = my + (mh - btn_h) // 2
    draw.rounded_rectangle([btn_rx, btn_ry, btn_rx + btn_w, btn_ry + btn_h], radius=24, fill=(15, 23, 42), outline=(255, 255, 255, 120), width=1)
    draw.text((btn_rx + btn_w // 2, btn_ry + btn_h // 2), "RUN PROTOTYPE ↗", font=get_font(13.5, 'bold'), fill=(56, 189, 248), anchor='mm')
    
    # 2. 4 INTERACTIVE STEP CARDS (y=340 to 700, h=78, sgap=12)
    step_y_start = 340
    step_card_h = 78
    sgap = 12
    
    step_items = [
        ("01. 경영 종합 대시보드 & OEE 관제", "전사 매출·수주 실시간 텔레메트리 관제 및 호기별 가동률(OEE) 위젯 커스텀 조작", "blue"),
        ("02. 스마트 생산 공정 스케줄러 (Gantt)", "드래그 앤 드롭 작업지시 배정, 공정 간 병목 감지 및 실시간 완료 실적 피드백", "cyan"),
        ("03. 3단계 품질 게이트 & 실시간 SPC 관리도", "수입·공정·출하 검사 성적서 등록 및 이상 징후 발생 시 1초 내 즉시 라인 비상 정지", "purple"),
        ("04. 자재/재고 실사 & 1-Tap 바코드 LOT 추적", "창고 로케이션 맵 조회, 선입선출 자재 불출 검증 및 원자재 투입 이력 원클릭 역추적", "green")
    ]
    
    for idx, (s_title, s_desc, s_theme) in enumerate(step_items):
        sy = step_y_start + idx * (step_card_h + sgap)
        draw.rounded_rectangle([rx, sy, rx + rw, sy + step_card_h], radius=12, fill=(24, 34, 52), outline=(51, 65, 85), width=1)
        
        draw_pill_badge(draw, left_x=rx + 20, cy=sy + 24, text=f"STEP {idx+1:02d}", font=get_font(9, 'bold'), theme=s_theme, dark_mode=True, pad_x=8, height=20, solid=True)
        draw.text((rx + 98, sy + 24), s_title, font=get_font(13.5, 'bold'), fill=(255, 255, 255), anchor='lm')
        draw.text((rx + 20, sy + 54), s_desc, font=get_font(11, 'regular'), fill=(148, 163, 184))
        
        # Ghost Link Button
        g_w = 110
        g_h = 32
        g_x = rx + rw - g_w - 20
        g_y = sy + (step_card_h - g_h) // 2
        draw.rounded_rectangle([g_x, g_y, g_x + g_w, g_y + g_h], radius=6, fill=(15, 23, 42), outline=(56, 189, 248), width=1)
        draw.text((g_x + g_w // 2, g_y + g_h // 2), "체험하기 ↗", font=get_font(11, 'bold'), fill=(56, 189, 248), anchor='mm')
        
    # 3. QR CODE & GITHUB LIVE REPOSITORY CARD (y=705 to 1010, h=305)
    qr_card_y = 705
    qr_card_h = 305
    draw.rounded_rectangle([rx, qr_card_y, rx + rw, qr_card_y + qr_card_h], radius=16, fill=(24, 34, 52), outline=(51, 65, 85), width=1)
    
    # Real crisp QR code
    try:
        qr = qrcode.QRCode(version=1, box_size=6, border=2)
        qr.add_data(proto_entry_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF").convert('RGBA')
        qr_size = 190
        qr_res = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        qr_px = rx + 30
        qr_py = qr_card_y + (qr_card_h - qr_size) // 2
        
        # Crisp Pure White Card Container with Cyan Outline
        draw.rounded_rectangle([qr_px - 10, qr_py - 10, qr_px + qr_size + 10, qr_py + qr_size + 10], radius=14, fill=(255, 255, 255), outline=(56, 189, 248), width=2)
        base.paste(qr_res, (qr_px, qr_py), qr_res)
        draw = ImageDraw.Draw(base)
    except Exception as e:
        print("QR Error:", e)
        qr_px = rx + 30
        qr_size = 190
        
    # Content beside QR Code
    info_x = qr_px + qr_size + 35
    
    draw_pill_badge(draw, left_x=info_x, cy=qr_card_y + 36, text="MOBILE INSTANT SCAN & LIVE DEPLOY", font=get_font(9.5, 'bold'), theme='cyan', dark_mode=True, has_dot=True, pad_x=10, height=22)
    draw.text((info_x, qr_card_y + 70), "스마트폰 카메라로 QR 코드를 스캔하세요", font=get_font(18, 'bold'), fill=(255, 255, 255))
    draw.text((info_x, qr_card_y + 98), "별도의 앱 설치 없이 모바일/태블릿 브라우저에서 60fps 인터랙티브 프로토타입이 즉시 구동됩니다.", font=get_font(11.5, 'medium'), fill=(148, 163, 184))
    
    # URL Box
    url_box_y = qr_card_y + 130
    draw.rounded_rectangle([info_x, url_box_y, rx + rw - 30, url_box_y + 50], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    draw.text((info_x + 16, url_box_y + 16), "🌐 Live URL :", font=get_font(10.5, 'bold'), fill=(56, 189, 248))
    draw.text((info_x + 105, url_box_y + 16), proto_entry_url, font=get_font(11, 'bold'), fill=(52, 211, 153))
    
    # Deploy Badges & Verification Row
    b_row_y = url_box_y + 68
    draw.text((info_x, b_row_y), "✓ GitHub Pages 프로덕션 무중단 배포 완료  ·  WCAG 2.1 AAA 고대비 접근성  ·  반응형 100% 검증", font=get_font(11, 'bold'), fill=(52, 211, 153))
    
    draw_slide_footer(draw, 12, dark_mode=True)
    base.save(os.path.join(OUT_DIR, 'slide_12.png'))
    print("SAVED slide_12.png (High-Performance Live Interactive Prototype Hub)")


if __name__ == '__main__':
    print("Generating enhanced CodeBridgeX MES Solution Behance slides...")
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
    make_slide_09()
    make_slide_10()
    make_slide_11()
    make_slide_12()
    print("ALL 12 ENHANCED MES SLIDES GENERATED SUCCESSFULLY!")
