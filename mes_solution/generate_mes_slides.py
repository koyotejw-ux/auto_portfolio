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

def draw_pill_badge(draw, cx=None, cy=0, text="", font=None, theme='blue', dark_mode=False, pad_x=14, height=30, left_x=None, solid=False):
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
    draw.line([(100, 52), (1820, 52)], fill=line_col, width=1)
    
    badge_text = f"{slide_num:02d} {category_kr}"
    draw_pill_badge(draw, left_x=100, cy=78, text=badge_text, font=get_font(10.5, 'bold'), theme='blue', dark_mode=dark_mode, pad_x=10, height=26)
    
    if right_badge:
        txt, theme = right_badge
        draw_pill_badge(draw, cx=1700, cy=78, text=txt, font=get_font(10.5, 'bold'), theme=theme, solid=True, dark_mode=dark_mode, pad_x=14, height=28)
        
    font_title = get_font(34, 'bold')
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
    # Pristine white executive canvas matching Korea History Quiz / Behance Standard
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    # 1. Top Header Rule & Pills
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=100, cy=76, text="2026 ENTERPRISE CLOUD SAAS CASE STUDY", font=get_font(11.5, 'bold'), theme='blue', pad_x=14, height=28)
    
    meta_txt = "반응형 웹 아키텍처 · 13대 비즈니스 모듈 & 59개 표준 화면 · 실시간 OEE 텔레메트리 · 1인 단독 기획·디자인 총괄"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=(71, 85, 105))
    
    # 2. Main Hero Title & Subtitle (Left)
    draw.text((100, 138), "CODEBRIDGEX MES SOLUTION · 클라우드 제조 플랫폼", font=get_font(14, 'bold'), fill=(0, 81, 255))
    
    title_p1 = "분절된 제조 현장 데이터를 "
    title_p2 = "반응형 원격 관제로 통합하다"
    w_p1 = draw.textlength(title_p1, font=get_font(50, 'black'))
    draw.text((100, 168), title_p1, font=get_font(50, 'black'), fill=(15, 23, 42))
    draw.text((100 + w_p1, 168), title_p2, font=get_font(50, 'black'), fill=(0, 81, 255))
    
    sub1 = "대화면 관제실부터 10인치 현장 터치 태블릿, 모바일 스마트폰까지 완벽하게 대응하는 반응형 웹 아키텍처와"
    sub2 = "수주·생산 실시간 MRP 파이프라인, 스마트 간트 공정 스케줄러, 무결점 LOT 추적으로 수기 취합 공수를 99.9% 절감한 B2B SaaS"
    draw.text((100, 248), sub1, font=get_font(14.5, 'regular'), fill=(51, 65, 85))
    draw.text((100, 274), sub2, font=get_font(14.5, 'regular'), fill=(51, 65, 85))
    
    # 3. 4 Key Impact Metric Pods (card_w=195, card_h=135)
    metrics = [
        ("99.9%", "실적 집계 소요 시간", "24시간 수기 일지 → 1초 즉시 수집", "blue"),
        ("13대 모듈", "전사 엔터프라이즈", "59개 이상 인터랙티브 표준 화면", "purple"),
        ("88.5%", "설비종합효율(OEE)", "실시간 텔레메트리 병목 해소", "green"),
        ("Multi", "데스크톱·태블릿·모바일", "100% 반응형 최적화 인터페이스", "blue")
    ]
    card_y = 335
    card_w = 195
    card_h = 135
    for idx, (m_val, m_lbl, m_desc, theme) in enumerate(metrics):
        cx = 100 + idx * (card_w + 18)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=16, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        val_col = (0, 81, 255) if theme == 'blue' else ((124, 58, 237) if theme == 'purple' else (16, 185, 129))
        draw.text((cx + 18, card_y + 18), m_val, font=get_num_font(30, 'black'), fill=val_col)
        draw.text((cx + 18, card_y + 66), m_lbl, font=get_font(13, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 18, card_y + 92), m_desc, font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        
    # 4. Project Specification & Architecture Pod (scope_w=834, scope_h=255)
    scope_y = 495
    scope_w = 834
    scope_h = 255
    draw.rounded_rectangle([100, scope_y, 100 + scope_w, scope_y + scope_h], radius=18, fill=(248, 250, 252), outline=(219, 234, 254), width=1)
    draw.text((125, scope_y + 22), "PROJECT SPECIFICATION & ARCHITECTURE OVERVIEW", font=get_font(12, 'bold'), fill=(0, 81, 255))
    
    spec_rows = [
        ("담당 역할", "엔터프라이즈 UX/UI 아키텍처, 디자인 시스템 구축, 기획 총괄 (100% 1인 단독)"),
        ("핵심 과제", "데이터 파편화 극복, 복잡한 SI 구축 장벽 제거, 현장 터치 및 모바일 접근성 극대화"),
        ("기술 스택", "Vite + React 18, TypeScript, Tailwind CSS, Atomic Design System (150+ Tokens)"),
        ("지원 플랫폼", '데스크톱 브라우저 (1920x1080), 10" 현장 태블릿 (1024x768), 모바일 (390x844)'),
        ("적용 상태", "엔터프라이즈 클라우드 SaaS 프로덕션 라이브 배포 및 현장 검증 완료")
    ]
    for r_idx, (k, v) in enumerate(spec_rows):
        ry = scope_y + 54 + r_idx * 35
        draw.text((125, ry), f"• {k}", font=get_font(12, 'bold'), fill=(0, 81, 255))
        draw.text((225, ry), f":  {v}", font=get_font(12, 'medium'), fill=(51, 65, 85))
        
    # 5. Bottom Hashtags
    tags = ["#스마트팩토리", "#클라우드_MES", "#반응형_웹", "#아토믹_디자인", "#OEE_텔레메트리", "#LOT_추적성"]
    tx = 100
    for t in tags:
        draw_pill_badge(draw, left_x=tx, cy=785, text=t, font=get_font(11, 'bold'), theme='slate', height=28, pad_x=12)
        tx += int(draw.textlength(t, font=get_font(11, 'bold')) + 24 + 10)

    # 6. Hero Multi-Device Mockup Showcase on Right (Matching User Attached Device Trio)
    trio_thumb = r"d:\097.flutter_project\auto_portfolio\assets\mes_hero_device_trio.png"
    if os.path.exists(trio_thumb):
        trio_img = Image.open(trio_thumb).convert('RGBA')
        
        # Scale to hero right space (avail_w approx 850, avail_h approx 720)
        scale = min(850 / trio_img.width, 700 / trio_img.height)
        new_w = int(round(trio_img.width * scale))
        new_h = int(round(trio_img.height * scale))
        trio_resized = trio_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        pos_x = 970 + (850 - new_w) // 2
        pos_y = 145 + (700 - new_h) // 2
        
        # Soft elegant drop shadow for the 3 devices
        sh = make_shadow(trio_resized, radius=40, alpha=85)
        base.paste(sh, (pos_x - 32, pos_y - 20), sh)
        base.paste(trio_resized, (pos_x, pos_y), trio_resized)
        
    # 7. Official App / Solution Icon Floating Badge (Bottom-Right of Left Column)
    icon_path = r"d:\097.flutter_project\auto_portfolio\assets\mes_solution_app_icon.png"
    if os.path.exists(icon_path):
        ic = Image.open(icon_path).convert('RGBA')
        ic_w = 96
        ic_sc = ic.resize((ic_w, ic_w), Image.Resampling.LANCZOS)
        badge_im = Image.new('RGBA', (116, 116), (0, 0, 0, 0))
        bd = ImageDraw.Draw(badge_im)
        bd.rounded_rectangle([0, 0, 116, 116], radius=24, fill=(255, 255, 255, 250), outline=(226, 232, 240), width=2)
        badge_im.paste(ic_sc, ((116 - ic_w)//2, (116 - ic_w)//2), ic_sc)
        sh_b = make_shadow(badge_im, radius=20, alpha=70)
        base.paste(sh_b, (900 - 32, 685 - 20), sh_b)
        base.paste(badge_im, (900, 685), badge_im)
    
    draw_slide_footer(draw, 1, dark_mode=False)
    base.save(os.path.join(OUT_DIR, 'slide_01.png'))
    print("SAVED slide_01.png (Executive White Hero Cover Matching Behance Standard)")
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
    # TOP: 3 Problem -> Solution Strategic Cards (y=200, h=105 each, gap=15)
    # -------------------------------------------------------------
    cards_data = [
        (
            "01. 분절된 데이터 파편화 → 전사 데이터 일원화 파이프라인",
            "수주, 생산, 재고, 회계 데이터가 부서별 엑셀과 수기 전산으로 파편화되어 데이터 누락 및 정산 오류 빈번",
            "생산(MES) 실적과 자금(ERP) 데이터가 실시간 연동되는 단일 대시보드 구축으로 수기 취합 공수 제거"
        ),
        (
            "02. 현장 의존적 유선 보고 → 멀티 디바이스 실시간 원격 관제",
            "공장 현장 상황을 파악하기 위해 직접 방문하거나 담당자의 유선 보고에 의존하여 경영진의 즉각적인 의사결정 지연",
            "PC 브라우저뿐만 아니라 태블릿·모바일에 최적화된 반응형 실시간 관제 UI를 제공하여 이동 중에도 병목 현상 즉시 파악 지원"
        ),
        (
            "03. 복잡한 구축형 UI 장벽 → 역할(Role) 기반의 경량화 인터페이스",
            "기존 대기업형 SI 솔루션은 높은 초기 비용과 실무자에게 불필요한 과도한 기능 노출로 사용성 저하",
            "생산직, 품질검사관, 경영진 등 직무별 필수 기능만 드래그 앤 드롭으로 배치할 수 있는 '메뉴 커스텀' 및 직관적인 디자인 시스템 적용"
        )
    ]
    
    top_sy = 205
    top_card_w = 1720
    top_card_h = 105
    top_gap = 16
    
    for c_idx, (c_title, c_prob, c_sol) in enumerate(cards_data):
        cy = top_sy + c_idx * (top_card_h + top_gap)
        # Light blue / gray container card
        draw.rounded_rectangle(
            [100, cy, 100 + top_card_w, cy + top_card_h],
            radius=16,
            fill=(240, 246, 255),  # Soft blue tinted bg matching user spec
            outline=(219, 234, 254),
            width=1
        )
        
        # Title (Bold 18px black)
        draw.text((130, cy + 16), c_title, font=get_font(17, 'bold'), fill=(15, 23, 42))
        
        # Problem Line
        draw.text((130, cy + 48), "Problem", font=get_font(13.5, 'bold'), fill=(239, 68, 68)) # Red
        draw.text((200, cy + 48), c_prob, font=get_font(13, 'medium'), fill=(51, 65, 85))
        
        # Solution Line
        draw.text((130, cy + 73), "Solution", font=get_font(13.5, 'bold'), fill=(0, 81, 255)) # Vibrant Blue
        draw.text((200, cy + 73), c_sol, font=get_font(13, 'medium'), fill=(51, 65, 85))
        
    # -------------------------------------------------------------
    # BOTTOM: 2 Authentic Survey & Data Analysis Cards (y=580, h=390)
    # -------------------------------------------------------------
    bot_y = 580
    bot_w = 845
    bot_h = 390
    bot_gap = 30
    
    # -------------------------------------------------------------
    # Left Bottom: Donut Chart "정보 파편화 -> 전사 데이터 통합 필요성 강조"
    # -------------------------------------------------------------
    lb_x = 100
    draw.rounded_rectangle([lb_x, bot_y, lb_x + bot_w, bot_y + bot_h], radius=20, fill=(240, 246, 255), outline=(219, 234, 254), width=1)
    
    # Card Header
    draw.text((lb_x + 35, bot_y + 30), "정보 파편화 → 전사 데이터 통합 필요성 강조", font=get_font(19, 'bold'), fill=(15, 23, 42))
    
    # Donut Chart Geometry (Center)
    dc_x = lb_x + bot_w // 2
    dc_y = bot_y + 195
    outer_r = 120
    inner_r = 50
    
    # Data slices:
    # 1. 기존 시스템 UI 불만족 30% -> Teal (0, 168, 181)
    # 2. 부서별 엑셀 관리 25% -> Blue (0, 114, 206)
    # 3. 구축 비용 부담 20% -> Orange (217, 83, 79 or 220, 85, 0)
    # 4. 수작업 및 유선 보고 25% -> Purple (108, 92, 231)
    # Total = 100%
    
    slices = [
        # (label, pct, color, text_color, start_ratio, end_ratio)
        ("구축 비용 부담\n20%", 0.20, (217, 83, 7), (255, 255, 255)),     # Orange/Amber
        ("수작업 및\n유선 보고\n25%", 0.25, (108, 92, 231), (255, 255, 255)),   # Purple
        ("기존 시스템\nUI 불만족\n30%", 0.30, (0, 163, 174), (255, 255, 255)),    # Cyan / Teal
        ("부서별 엑셀 관리\n25%", 0.25, (29, 105, 188), (255, 255, 255)),    # Slate Blue
    ]
    
    # Draw Pie slices
    curr_angle = -45  # Start from top-right so Orange is at top-right
    for s_label, s_pct, s_col, s_tcol in slices:
        sweep = s_pct * 360.0
        draw.pieslice(
            [dc_x - outer_r, dc_y - outer_r, dc_x + outer_r, dc_y + outer_r],
            start=curr_angle,
            end=curr_angle + sweep,
            fill=s_col
        )
        curr_angle += sweep
        
    # Cut out inner hole for Donut
    draw.ellipse([dc_x - inner_r, dc_y - inner_r, dc_x + inner_r, dc_y + inner_r], fill=(240, 246, 255))
    
    # Draw Slice Labels inside the donut bands
    # Slice 1 (Orange, ~20%): angle center approx 0 deg
    draw.text((dc_x + 55, dc_y - 45), "구축 비용 부담\n20%", font=get_font(10.5, 'bold'), fill=(255, 255, 255), align='center')
    # Slice 2 (Purple, ~25%): angle center approx 80 deg
    draw.text((dc_x + 35, dc_y + 40), "수작업 및\n유선 보고\n25%", font=get_font(10, 'bold'), fill=(255, 255, 255), align='center')
    # Slice 3 (Teal, ~30%): angle center approx 190 deg
    draw.text((dc_x - 90, dc_y + 35), "기존 시스템\nUI 불만족\n30%", font=get_font(10.5, 'bold'), fill=(255, 255, 255), align='center')
    # Slice 4 (Blue, ~25%): angle center approx 280 deg
    draw.text((dc_x - 70, dc_y - 45), "부서별 엑셀 관리\n25%", font=get_font(10.5, 'bold'), fill=(255, 255, 255), align='center')

    # Source footnote
    draw.text((dc_x, bot_y + bot_h - 28), "(출처: 사내 임직원 조사 및 시장 동향 기반 AI 모델 추정치)", font=get_font(12, 'regular'), fill=(100, 116, 139), anchor='mm')
    
    # -------------------------------------------------------------
    # Right Bottom: Horizontal Bar Chart "중소 제조사 CEO가 겪는 가장 큰 관리 애로사항은?"
    # -------------------------------------------------------------
    rb_x = lb_x + bot_w + bot_gap
    draw.rounded_rectangle([rb_x, bot_y, rb_x + bot_w, bot_y + bot_h], radius=20, fill=(240, 246, 255), outline=(219, 234, 254), width=1)
    
    # Card Header
    draw.text((rb_x + 35, bot_y + 30), "중소 제조사 CEO가 겪는 가장 큰 관리 애로사항은?", font=get_font(19, 'bold'), fill=(15, 23, 42))
    
    # H-Bar Data
    # 1. 미수금/자금 흐름: 37.8
    # 2. 실시간 생산 진척: 26.8
    # 3. 수주/발주 현황: 12.2
    # 4. 타 부서 데이터 취합: 12.2
    # 5. 납기관리: 6.8
    # 6. 개인정보변경: 4.2
    bar_items = [
        ("미수금/자금 흐름", 37.8),
        ("실시간 생산 진척", 26.8),
        ("수주/발주 현황", 12.2),
        ("타 부서 데이터 취합", 12.2),
        ("납기관리", 6.8),
        ("개인정보변경", 4.2)
    ]
    
    axis_x = rb_x + 195  # Vertical axis line x
    bar_sy = bot_y + 85
    bar_h = 16
    bar_gap_y = 39
    max_pct = 40.0
    bar_max_w = 520
    
    # Axis Line
    draw.line([axis_x, bar_sy - 10, axis_x, bar_sy + len(bar_items) * bar_gap_y - 12], fill=(148, 163, 184), width=2)
    
    for b_idx, (b_label, b_val) in enumerate(bar_items):
        by = bar_sy + b_idx * bar_gap_y
        
        # Label (Right-aligned to axis)
        draw.text((axis_x - 14, by + 8), b_label, font=get_font(12.5, 'medium'), fill=(30, 41, 59), anchor='rm')
        
        # Bar
        curr_w = int(round((b_val / max_pct) * bar_max_w))
        # Blue gradient / pill shape
        draw.rounded_rectangle([axis_x + 2, by, axis_x + 2 + curr_w, by + bar_h], radius=bar_h // 2, fill=(43, 127, 255))
        
        # Value text (next to bar)
        draw.text((axis_x + 2 + curr_w + 12, by + 8), f"{b_val:.1f}", font=get_num_font(14, 'medium'), fill=(30, 41, 59), anchor='lm')
        
    # Source footnote
    draw.text((rb_x + bot_w // 2, bot_y + bot_h - 28), "(출처 : 사내 임직원 조사 및 시장 동향 기반 AI 모델 추정치)", font=get_font(12, 'regular'), fill=(100, 116, 139), anchor='mm')
    
    draw_slide_footer(draw, 2)
    base.save(os.path.join(OUT_DIR, 'slide_02.png'))
    print("SAVED slide_02.png (Research with Exact Problem/Solution & 2 High-Density Charts)")

# ==============================================================
# SLIDE 03: Target Users & Roles (Executive Dashboard vs Field Touch)
def make_slide_03():
    base = Image.new('RGB', (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=3, 
        category_kr="Target Users & Roles | 사용자 역할별 맞춤형 접근성 및 페르소나 아키텍처", 
        title_black="경영진의 실시간 의사결정부터 현장 터치까지, ", 
        title_blue="Target Users & Roles 기반 맞춤형 인터페이스", 
        subtitle_kr="경영진 및 현장 작업자의 직무 특성을 반영한 2대 핵심 사용자 프로필과 2x2 세그멘테이션 매트릭스"
    )
    
    # -------------------------------------------------------------
    # TOP: 2 Authentic User Role Cards (Matching Behance Deck Spec)
    # -------------------------------------------------------------
    top_sy = 205
    top_w = 845
    top_h = 240
    top_gap = 30
    
    # Role 1: 공장 총괄 책임자 / 경영진
    r1_x = 100
    draw.rounded_rectangle([r1_x, top_sy, r1_x + top_w, top_sy + top_h], radius=16, fill=(240, 246, 255), outline=(219, 234, 254), width=1)
    
    # Avatar badge circle (Executive)
    draw.ellipse([r1_x + 28, top_sy + 24, r1_x + 76, top_sy + 72], fill=(0, 81, 255))
    draw.text((r1_x + 52, top_sy + 48), "CEO", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    draw.text((r1_x + 92, top_sy + 28), "공장 총괄 책임자 / 경영진 (Executive)", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, left_x=r1_x + 92, cy=top_sy + 60, text="실시간 손익 · 가동률 의사결정", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
    
    draw.line([(r1_x + 28, top_sy + 88), (r1_x + top_w - 28, top_sy + 88)], fill=(219, 234, 254), width=1)
    draw.text((r1_x + 28, top_sy + 102), "주요 요구사항 및 페인포인트", font=get_font(12, 'bold'), fill=(0, 81, 255))
    r1_desc = (
        "· 유선 보고나 엑셀 수기 취합 없이 전 공장의 가동률(OEE) 및 납기 진척률을 1초 만에 확인\n"
        "· 미수금, 매출 실적, 수주 대비 생산 병목 현상을 멀티 디바이스(PC/태블릿)로 실시간 원격 관제\n"
        "· 불필요한 세부 입력 폼 대신 한눈에 파악 가능한 고밀도 KPI 위젯 중심의 인터페이스 선호"
    )
    draw.text((r1_x + 28, top_sy + 128), r1_desc, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
    
    # Role 2: 현장 오퍼레이터 / 생산 라인 작업자
    r2_x = r1_x + top_w + top_gap
    draw.rounded_rectangle([r2_x, top_sy, r2_x + top_w, top_sy + top_h], radius=16, fill=(240, 246, 255), outline=(219, 234, 254), width=1)
    
    # Avatar badge circle (Operator)
    draw.ellipse([r2_x + 28, top_sy + 24, r2_x + 76, top_sy + 72], fill=(16, 185, 129))
    draw.text((r2_x + 52, top_sy + 48), "OP", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    draw.text((r2_x + 92, top_sy + 28), "현장 작업자 / 생산 라인 오퍼레이터 (Field Operator)", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, left_x=r2_x + 92, cy=top_sy + 60, text="1-Tap 간편 실적 등록 · 바코드 스캔", font=get_font(10, 'bold'), theme='green', pad_x=8, height=22)
    
    draw.line([(r2_x + 28, top_sy + 88), (r2_x + top_w - 28, top_sy + 88)], fill=(219, 234, 254), width=1)
    draw.text((r2_x + 28, top_sy + 102), "주요 요구사항 및 페인포인트", font=get_font(12, 'bold'), fill=(16, 185, 129))
    r2_desc = (
        "· 방진 장갑을 착용한 터치 환경에서도 오입력 없는 48px 이상의 대형 버튼 및 숫자 키패드 지원\n"
        "· 복잡한 텍스트 입력 없이 바코드 스캐너 연동으로 투입 원자재 LOT 매핑 및 작업 개시 즉시 처리\n"
        "· 설비 비가동 및 불량 발생 시 3초 이내에 사유를 선택할 수 있는 간결한 바텀시트 모달 필요"
    )
    draw.text((r2_x + 28, top_sy + 128), r2_desc, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
    
    # -------------------------------------------------------------
    # BOTTOM: 2x2 Target Matrix & 4-Way Competitive Benchmark
    # -------------------------------------------------------------
    bot_sy = 475
    bot_h = 495
    
    # 1. 2x2 Matrix (Left: w=845)
    draw.rounded_rectangle([100, bot_sy, 100 + top_w, bot_sy + bot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=124, cy=bot_sy + 28, text="TARGET MATRIX", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((250, bot_sy + 28), "데이터 조작 깊이 vs. 현장 이동성 세그멘테이션", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    qw = 385
    qh = 195
    q1_x = 124
    q1_y = bot_sy + 60
    q2_x = q1_x + qw + 20
    q2_y = q1_y
    q3_x = q1_x
    q3_y = q1_y + qh + 16
    q4_x = q2_x
    q4_y = q3_y
    
    # Q1: CEO / 경영진
    draw.rounded_rectangle([q1_x, q1_y, q1_x + qw, q1_y + qh], radius=12, fill=(239, 246, 255), outline=(0, 81, 255, 120), width=1)
    draw.text((q1_x + 16, q1_y + 18), "경영진 / CEO (Executive)", font=get_font(13.5, 'bold'), fill=(0, 81, 255))
    draw.text((q1_x + 16, q1_y + 44), "· 데이터 분석: 종합 KPI, 손익, OEE, 납기준수율\n· 디바이스: 모바일 / 태블릿 반응형 뷰포트\n· 사용 패턴: 이동 중 실시간 알림 수신 및 즉시 승인", font=get_font(11, 'medium'), fill=(71, 85, 105))
    
    # Q2: 생산/공정 관리자
    draw.rounded_rectangle([q2_x, q2_y, q2_x + qw, q2_y + qh], radius=12, fill=(245, 243, 255), outline=(124, 58, 237, 120), width=1)
    draw.text((q2_x + 16, q2_y + 18), "공장장 / 생산관리자 (Operational Planner)", font=get_font(13.5, 'bold'), fill=(124, 58, 237))
    draw.text((q2_x + 16, q2_y + 44), "· 데이터 조작: 스마트 간트 스케줄링, 호기별 배정\n· 디바이스: 데스크톱 대화면 + 현장 점검용 패드\n· 사용 패턴: 공정 병목 사전 감지 및 긴급 지시 배포", font=get_font(11, 'medium'), fill=(71, 85, 105))
    
    # Q3: 현장 작업자
    draw.rounded_rectangle([q3_x, q3_y, q3_x + qw, q3_y + qh], radius=12, fill=(236, 253, 245), outline=(16, 185, 129, 120), width=1)
    draw.text((q3_x + 16, q3_y + 18), "현장 작업자 (Field Operator)", font=get_font(13.5, 'bold'), fill=(16, 185, 129))
    draw.text((q3_x + 16, q3_y + 44), "· 데이터 조작: 1-Tap 바코드 스캔, 양품/불량 집계\n· 디바이스: 라인별 7~10인치 방진 터치 패널\n· 사용 패턴: 초·중·종물 검사 실측치 즉시 전송", font=get_font(11, 'medium'), fill=(71, 85, 105))
    
    # Q4: 품질/자재 관리자
    draw.rounded_rectangle([q4_x, q4_y, q4_x + qw, q4_y + qh], radius=12, fill=(254, 243, 199), outline=(217, 119, 6, 120), width=1)
    draw.text((q4_x + 16, q4_y + 18), "품질/자재 관리자 (Quality Inspector)", font=get_font(13.5, 'bold'), fill=(217, 119, 6))
    draw.text((q4_x + 16, q4_y + 44), "· 데이터 조작: SPC 관리도 통계 분석, LOT 역추적\n· 디바이스: PC 웹 브라우저 + 휴대용 바코드 단말\n· 사용 패턴: 부적합품 발생 시 즉시 라인 홀드 조치", font=get_font(11, 'medium'), fill=(71, 85, 105))
    
    # 2. Benchmark Comparison (Right: w=845)
    r_bench_x = 100 + top_w + top_gap
    draw.rounded_rectangle([r_bench_x, bot_sy, r_bench_x + top_w, bot_sy + bot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=r_bench_x + 24, cy=bot_sy + 28, text="COMPETITIVE BENCHMARK", font=get_font(10, 'bold'), theme='purple', pad_x=8, height=22)
    draw.text((r_bench_x + 215, bot_sy + 28), "글로벌 외산 대비 독보적인 사용성 및 경량화 강점", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # Table Header
    th_y = bot_sy + 60
    draw.rounded_rectangle([r_bench_x + 20, th_y, r_bench_x + top_w - 20, th_y + 36], radius=8, fill=(241, 245, 249))
    draw.text((r_bench_x + 35, th_y + 18), "비교 항목", font=get_font(11.5, 'bold'), fill=(71, 85, 105), anchor='lm')
    draw.text((r_bench_x + 250, th_y + 18), "CodeBridgeX MES", font=get_font(12, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((r_bench_x + 440, th_y + 18), "외산 SAP / Siemens", font=get_font(11, 'bold'), fill=(71, 85, 105), anchor='mm')
    draw.text((r_bench_x + 630, th_y + 18), "국내 구축형 SI", font=get_font(11, 'bold'), fill=(71, 85, 105), anchor='mm')
    
    bench_rows = [
        ("반응형 멀티 디바이스", "완벽 지원 (PC/태블릿/모바일)", "PC 온프레미스 고정", "태블릿 미지원 / 왜곡 발생"),
        ("디자인 시스템 완성도", "아토믹 디자인 150+ 토큰", "레거시 폐쇄형 프레임워크", "통일성 없는 화면별 파편화"),
        ("도입 및 학습 기간", "2일 이내 즉시 현장 투입", "2~3개월 고난도 전문 교육", "3주 이상 매뉴얼 숙지 필요"),
        ("수기 취합 공수 절감", "99.9% (실시간 단일 파이프라인)", "60% (일부 수기 입력 상존)", "40% (부서별 엑셀 병행)"),
        ("초기 도입 비용(TCO)", "합리적 SaaS 구독 체계", "수억~수십억 원대 고부담", "수천만 원대 SI 개발비")
    ]
    
    r_sy = th_y + 44
    for ri, (item_lbl, cbx_val, sap_val, si_val) in enumerate(bench_rows):
        row_y = r_sy + ri * 72
        draw.rounded_rectangle([r_bench_x + 20, row_y, r_bench_x + top_w - 20, row_y + 64], radius=8, fill=(248, 250, 252) if ri%2==0 else (255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((r_bench_x + 35, row_y + 32), item_lbl, font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
        
        # CodeBridgeX (Highlighted Blue)
        draw.rounded_rectangle([r_bench_x + 145, row_y + 10, r_bench_x + 355, row_y + 54], radius=6, fill=(239, 246, 255), outline=(0, 81, 255), width=1)
        draw.text((r_bench_x + 250, row_y + 32), cbx_val, font=get_font(11, 'bold'), fill=(0, 81, 255), anchor='mm')
        
        # Competitors
        draw.text((r_bench_x + 440, row_y + 32), sap_val, font=get_font(10.5, 'medium'), fill=(100, 116, 139), anchor='mm')
        draw.text((r_bench_x + 630, row_y + 32), si_val, font=get_font(10.5, 'medium'), fill=(100, 116, 139), anchor='mm')

    draw_slide_footer(draw, 3)
    base.save(os.path.join(OUT_DIR, 'slide_03.png'))
    print("SAVED slide_03.png (Target Users & Roles)")

# SLIDE 04: Information Architecture (Exact Centered Tree)
def make_slide_04():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=4, 
        category_kr="IA & Access Structure | 정보 구조 및 역할별 접근성 계층", 
        title_black="전사 제조 라이프사이클을 관통하는 ", 
        title_blue="체계적인 정보 계층 구조", 
        subtitle_kr="기준정보 설정부터 영업 수주, 생산 실행, 품질 보증, 출하 재고까지 유기적으로 연동된 엔터프라이즈 IA"
    )
    
    root_x1, root_y1, root_x2, root_y2 = 700, 220, 1220, 284
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=12, fill=(255, 255, 255), outline=(0, 81, 255), width=2)
    root_cy = (root_y1 + root_y2) // 2
    b_root = draw_pill_badge(draw, left_x=root_x1 + 18, cy=root_cy, text="통합 플랫폼", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=26)
    draw.text((b_root[2] + 16, root_cy - 11), "CodeBridgeX Cloud MES & ERP 아키텍처", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((b_root[2] + 16, root_cy + 11), "멀티테넌트 SaaS 기반 13개 핵심 비즈니스 도메인 및 59개 표준 화면", font=get_font(10.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
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
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=6, 
        category_kr="와이어프레임 & 화면 설계서 | 251229 엔터프라이즈 실물 규격", 
        title_black="태블릿 및 모바일 현장 터치에 최적화된 ", 
        title_blue="실제 설계서 화면 와이어프레임", 
        subtitle_kr="D:\\102_1.codebridgex\\MES Solution Website Structure 251229 프로젝트에서 직접 추출한 표준 화면 규격서와 현장 UI (비율 유지 1:1 정렬)"
    )
    
    wf_items = [
        ("01. 태블릿 대시보드 규격", "wireframe_tablet_dashboard.png", "10-inch Tablet (Land) CEO 종합 관제 화면"),
        ("02. 모바일 생산관리 규격", "wireframe_phone_production.png", "Phone 해상도 호기별 작업지시 및 라인 제어"),
        ("03. 모바일 품질관리 규격", "wireframe_phone_quality.png", "AQL 수입/공정 검사 및 불량 판정 규격"),
        ("04. 공정 기준정보 규격", "wireframe_phone_process.png", "표준 작업 공순, 설비 매핑 및 사이클타임")
    ]
    
    card_w = (W - 200 - 3 * 24) // 4
    top_y = 220
    card_h = 740
    
    for i, (title, fname, desc) in enumerate(wf_items):
        cx = 100 + i * (card_w + 24)
        draw.rounded_rectangle([cx, top_y, cx + card_w, top_y + card_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        draw_pill_badge(draw, left_x=cx + 20, cy=top_y + 36, text="251229 화면설계서", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=26)
        draw.text((cx + 20, top_y + 76), title, font=get_font(16, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 20, top_y + 104), desc, font=get_font(11, 'medium'), fill=(71, 85, 105))
        
        fpath = os.path.join(MOCKUP_DIR, fname)
        frame_y = top_y + 135
        frame_h = card_h - 155
        frame_w = card_w - 32
        
        draw.rounded_rectangle([cx + 16, frame_y, cx + 16 + frame_w, frame_y + frame_h], radius=10, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
        
        if os.path.exists(fpath):
            try:
                wf_img = Image.open(fpath).convert('RGB')
                src_w, src_h = wf_img.size
                scale = min((frame_w - 8) / src_w, (frame_h - 8) / src_h)
                target_w = int(round(src_w * scale))
                target_h = int(round(src_h * scale))
                wf_resized = wf_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                paste_x = cx + 16 + (frame_w - target_w) // 2
                paste_y = frame_y + (frame_h - target_h) // 2
                base.paste(wf_resized, (paste_x, paste_y))
            except Exception as e:
                print(f"Error loading {fname}:", e)
                
    draw_slide_footer(draw, 6)
    base.save(os.path.join(OUT_DIR, 'slide_06.png'))
    print("SAVED slide_06.png")


def make_slide_07():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=7, 
        category_kr="디자인 시스템 | 아토믹 디자인 토큰 & 재사용 컴포넌트", 
        title_black="150개 이상의 표준 UI 에셋으로 구축한 ", 
        title_blue="확장 가능한 엔터프라이즈 디자인 시스템", 
        subtitle_kr="원자(Atoms), 분자(Molecules), 유기체(Organisms), 템플릿(Templates) 계층으로 완성된 고품격 B2B UI 킷"
    )
    
    levels = [
        ("Level 1: Atoms", "원자 단위 토큰", "색상, 타이포그래피, 버튼, 배지, 입력 필드", [
            ("Color Tokens", "Primary Blue (#0051FF), Slate, Alert"),
            ("Typography", "Pretendard Variable 9단계 스케일"),
            ("Button Kits", "Solid, Outline, Ghost, Danger (48px)"),
            ("Status Badges", "가동, 비가동, 대기, 검사중 8종")
        ], "blue"),
        ("Level 2: Molecules", "분자 컴포넌트", "검색 입력바, 페이지네이션, KPI 메트릭 카드", [
            ("Metric Card", "수치, 증감율, 미니 스파크라인"),
            ("Search Filter", "기간 선택기 + 셀렉트박스 + 버튼"),
            ("Action Group", "엑셀 다운로드, 인쇄, 신규 등록"),
            ("Breadcrumb", "13개 모듈 단계별 현재 위치 경로")
        ], "purple"),
        ("Level 3: Organisms", "유기체 블록", "실시간 데이터 그리드, 스케줄러, 모달 다이얼로그", [
            ("Data Table", "가상 스크롤, 정렬, 필터, 컬럼 리사이즈"),
            ("Gantt Chart", "타임라인 드래그 앤 드롭 일정 블록"),
            ("SPC Chart", "관리 한계선(UCL/LCL) 실시간 플롯"),
            ("BOM Tree", "다단계 품목 전개 및 소요량 테이블")
        ], "cyan"),
        ("Level 4: Templates", "표준 페이지 템플릿", "대시보드형, 목록조회형, 등록편집형, 탭문서형", [
            ("Dashboard", "헤더 + 요약 카드 + 차트 4분할 그리드"),
            ("List-Detail", "좌측 그리드 + 우측 슬라이드 드로어"),
            ("Form Spec", "2열 인풋 필드 + 유효성 검증 + 저장 바"),
            ("Tabbed View", "서브 모듈 멀티 탭 전환 컨테이너")
        ], "green")
    ]
    
    card_w = (W - 200 - 3 * 24) // 4
    top_y = 220
    card_h = 740
    
    for i, (lvl, lvl_sub, desc, items, theme) in enumerate(levels):
        cx = 100 + i * (card_w + 24)
        draw.rounded_rectangle([cx, top_y, cx + card_w, top_y + card_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        draw_pill_badge(draw, left_x=cx + 24, cy=top_y + 36, text=lvl, font=get_font(10.5, 'bold'), theme=theme, pad_x=10, height=26)
        draw.text((cx + 24, top_y + 80), lvl_sub, font=get_font(18, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 24, top_y + 112), desc, font=get_font(11.5, 'medium'), fill=(71, 85, 105))
        
        draw.line([(cx + 24, top_y + 145), (cx + card_w - 24, top_y + 145)], fill=(226, 232, 240), width=1)
        
        iy = top_y + 170
        for it_title, it_desc in items:
            draw.rounded_rectangle([cx + 20, iy, cx + card_w - 20, iy + 115], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
            draw.text((cx + 34, iy + 22), it_title, font=get_font(13.5, 'bold'), fill=(0, 81, 255))
            lines = textwrap.wrap(it_desc, width=22)
            ly = iy + 52
            for l in lines:
                draw.text((cx + 34, ly), l, font=get_font(11.5, 'medium'), fill=(71, 85, 105))
                ly += 22
            iy += 135
            
    draw_slide_footer(draw, 7)
    base.save(os.path.join(OUT_DIR, 'slide_07.png'))
    print("SAVED slide_07.png")

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
        category_kr="핵심 기능 | 실시간 생산 스케줄링 & 스마트 작업 지시", 
        title_black="지연 없는 라인 가동을 실현하는 ", 
        title_blue="인텔리전트 공정 스케줄러", 
        subtitle_kr="수주 납기와 설비 부하를 고려한 간트차트 드래그 앤 드롭 일정 조정 및 호기별 작업지시 자동 배포 (현장 다크모드 적용)",
        dark_mode=True
    )
    
    lx, ly, lw, lh = 100, 220, 520, 740
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=14, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    
    draw_pill_badge(draw, left_x=lx + 30, cy=ly + 40, text="공정 관리 핵심 혁신", font=get_font(10.5, 'bold'), theme='cyan', dark_mode=True, pad_x=12, height=28)
    draw.text((lx + 30, ly + 80), "작업 지시 & 실시간 추적", font=get_font(20, 'bold'), fill=(255, 255, 255))
    draw.text((lx + 30, ly + 115), "기존 엑셀 기반 배포 대비 지시서 생성 시간을 85% 단축하고,\n현장 호기별 진행 상태를 1초 단위로 실시간 관제합니다.", font=get_font(12.5, 'medium'), fill=(148, 163, 184))
    
    feats = [
        ("스마트 간트차트 일정 조정", "라인별 가동 현황과 잔여 케파를 시각화하여 드래그 앤 드롭으로 작업 순서 즉시 재배치."),
        ("자재 부족 사전 알림 (MRP)", "작업 지시 발행 전 필요한 원자재의 재고 유무를 검증하여 결품으로 인한 라인 정지 예방."),
        ("모바일/태블릿 디지털 작업표", "현장 모니터에 도면과 표준작업서(SOP)를 고화질로 스트리밍하여 페이퍼리스 공장 구현."),
        ("바코드 기반 1-Tap 실적 보고", "작업 완료 시 바코드 스캔 한 번으로 양품/불량 수량 및 소요 시간이 중앙 DB에 즉시 전송.")
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
    print("SAVED slide_08.png (Dark Production Mode)")

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
    base = Image.new('RGB', (W, H), (15, 23, 42)) # High-tech dark mode showcase
    draw = ImageDraw.Draw(base)
    
    for gx in range(0, W, 40):
        draw.line([(gx, 0), (gx, H)], fill=(23, 33, 56), width=1)
    for gy in range(0, H, 40):
        draw.line([(0, gy), (W, gy)], fill=(23, 33, 56), width=1)
        
    draw_slide_header(
        draw, 
        slide_num=10, 
        category_kr="프로덕션 화면 | 6대 핵심 상용 웹 대시보드 쇼케이스", 
        title_black="현장 조도에 최적화된 고대비 인터페이스, ", 
        title_blue="다크모드 & 반응형 UI 컬렉션", 
        subtitle_kr="랜딩 포털, 다크모드 관제 대시보드, 다크 생산·품질·자재 관리 및 태블릿 화면을 아우르는 상용 인터페이스",
        dark_mode=True
    )
    
    screens = [
        ("01. SaaS 랜딩 포털", "screen_01_landing.png", "솔루션 소개 및 데모 체험 신청"),
        ("02. 경영 종합 대시보드 (Dark)", "screen_02_dashboard_dark.png", "전사 KPI, 생산성 및 OEE 텔레메트리"),
        ("03. 생산 공정 관리 (Dark)", "screen_03_production_dark.png", "작업 지시서 발행 및 라인별 실적"),
        ("04. 품질 보증 & 검사 (Dark)", "screen_04_quality_dark.png", "수입/공정 검사 및 불량률 SPC"),
        ("05. 자재/재고 실사 (Dark)", "screen_05_inventory_dark.png", "창고 로케이션별 실시간 재고량"),
        ("06. 태블릿 10-inch 관제 규격", "wireframe_tablet_dashboard.png", "현장 태블릿 반응형 랜드스케이프")
    ]
    
    cols = 3
    rows = 2
    cell_w = (W - 200 - 2 * 24) // cols
    cell_h = (740 - 24) // rows
    
    for idx, (title, fname, desc) in enumerate(screens):
        c = idx % cols
        r = idx // cols
        cx = 100 + c * (cell_w + 24)
        cy = 220 + r * (cell_h + 24)
        
        draw.rounded_rectangle([cx, cy, cx + cell_w, cy + cell_h], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        
        draw.rounded_rectangle([cx, cy, cx + cell_w, cy + 32], radius=10, fill=(15, 23, 42))
        draw.rectangle([cx, cy + 20, cx + cell_w, cy + 32], fill=(15, 23, 42))
        draw.text((cx + 12, cy + 16), title, font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='lm')
        draw.text((cx + cell_w - 12, cy + 16), desc, font=get_font(9, 'medium'), fill=(148, 163, 184), anchor='rm')
        
        fpath = os.path.join(MOCKUP_DIR, fname)
        if not os.path.exists(fpath):
            fpath = os.path.join(MOCKUP_DIR, fname.replace('_dark', ''))
            
        if os.path.exists(fpath):
            try:
                img = Image.open(fpath).convert('RGB')
                thumb_w = cell_w - 4
                thumb_h = cell_h - 36
                img_resized = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                base.paste(img_resized, (cx + 2, cy + 34))
            except Exception as e:
                print(f"Error thumbnailing {fname}:", e)
                
    draw_slide_footer(draw, 10, dark_mode=True)
    base.save(os.path.join(OUT_DIR, 'slide_10.png'))
    print("SAVED slide_10.png (Dark Mode Collection)")

# ==============================================================
# SLIDE 11: Business Impact & STAR Retrospective
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
    
    metrics = [
        ("실적 집계 소요 시간", "24시간 → 1초", "▼ 99.9% 단축", "현장 종이 작업일지 취합 방식에서 웹 1-Tap 실시간 수집 체계로 전면 전환", "blue"),
        ("공정 불량률 감소", "3.8% → 1.2%", "▼ 42% 감소", "3단계 품질 게이트와 SPC 실시간 이상 징후 감지로 불량 유출 사전 차단", "green"),
        ("납기 준수율(OTD)", "84.2% → 98.7%", "▲ 14.5%p 향상", "스마트 간트 스케줄러와 BOM 자재 사전 결품 방지 알고리즘 적용", "purple"),
        ("작업자 교육 시간", "2주 → 2일", "▼ 85% 단축", "아토믹 디자인 기반 일관된 3단 반응형 UI로 신규 작업자 진입 장벽 최소화", "amber"),
    ]
    
    mw = (W - 200 - 3 * 24) // 4
    top_y = 220
    mh = 190
    
    for i, (label, val, delta, desc, theme) in enumerate(metrics):
        cx = 100 + i * (mw + 24)
        draw.rounded_rectangle([cx, top_y, cx + mw, top_y + mh], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        draw_pill_badge(draw, left_x=cx + 20, cy=top_y + 32, text=label, font=get_font(10, 'bold'), theme=theme, pad_x=10, height=24)
        draw.text((cx + 20, top_y + 80), val, font=get_font(21, 'bold'), fill=(15, 23, 42))
        draw_pill_badge(draw, left_x=cx + 20, cy=top_y + 115, text=delta, font=get_font(9.5, 'bold'), theme='solid' if theme=='blue' else theme, solid=True, pad_x=8, height=20)
        draw.text((cx + 20, top_y + 150), desc, font=get_font(10, 'medium'), fill=(71, 85, 105))
        
    star_y = top_y + mh + 30
    star_h = 520
    draw.rounded_rectangle([100, star_y, W - 100, star_y + star_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, left_x=130, cy=star_y + 36, text="STAR 기법 상세 회고 (200자 이상)", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=28)
    draw.text((130, star_y + 78), "스마트 팩토리 엔터프라이즈 UX/UI 아키텍처 구축 회고", font=get_font(20, 'bold'), fill=(15, 23, 42))
    
    star_items = [
        ("Situation (상황)", "중소·중견 제조 현장의 90% 이상이 종이 일지와 파편화된 엑셀로 생산 현황을 관리하여 재고 오차와 납기 지연이 만성화되어 있었으며, 외산 레거시 ERP의 난해한 조작성으로 인해 현장 작업자의 시스템 도입 기피 현상이 심각했습니다."),
        ("Task (과제)", "경영진의 실시간 의사결정(OEE, 매출, 납기)을 지원하는 Executive Dashboard와 현장 오퍼레이터가 장갑을 착용한 상태에서도 3초 내에 직관적으로 실적을 등록할 수 있는 인체공학적 반응형 웹 MES 아키텍처를 100% 단독 설계해야 했습니다."),
        ("Action (행동)", "Vite + React 18과 Tailwind CSS 기반으로 아토믹 디자인 토큰 150종을 정의하고, 13대 비즈니스 카테고리 및 59개 표준 화면 규격을 완성했습니다. 가상 스크롤 데이터 그리드와 간트차트 스케줄러, 실시간 SPC 관리도 및 1-Tap 바코드 LOT 추적 뷰어를 전면 구현했습니다."),
        ("Result (결과)", "도입 기업 실측 결과 실적 집계 지연을 24시간에서 1초로 단축(99.9% 개선), 공정 불량률 42% 감소, 납기 준수율 98.7% 달성 및 신규 작업자 UI 교육 기간을 2주에서 2일로 85% 단축시키는 괄목할 만한 생산성 혁신을 이끌어냈습니다.")
    ]
    
    sy = star_y + 125
    for title, content in star_items:
        draw.text((130, sy), title, font=get_font(13.5, 'bold'), fill=(0, 81, 255))
        lines = textwrap.wrap(content, width=110)
        ly = sy + 25
        for l in lines:
            draw.text((130, ly), l, font=get_font(12, 'medium'), fill=(51, 65, 85))
            ly += 22
        sy += 90
        
    draw_slide_footer(draw, 11)
    base.save(os.path.join(OUT_DIR, 'slide_11.png'))
    print("SAVED slide_11.png")

# ==============================================================
# SLIDE 12: Live Prototype & Interactive Hub (Dark Mode Finale)
def make_slide_12():
    base = Image.new('RGB', (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(base)
    
    for gx in range(0, W, 40):
        draw.line([(gx, 0), (gx, H)], fill=(23, 33, 56), width=1)
    for gy in range(0, H, 40):
        draw.line([(0, gy), (W, gy)], fill=(23, 33, 56), width=1)
        
    draw_slide_header(
        draw, 
        slide_num=12, 
        category_kr="라이브 프로토타입 | 클라우드 MES 웹 인터랙티브 허브", 
        title_black="지금 바로 웹 브라우저에서 체험하는 ", 
        title_blue="차세대 스마트 팩토리 MES", 
        subtitle_kr="포트폴리오 허브 및 인터랙티브 슬라이드 뷰어, 실시간 데모 환경으로 연결되는 원클릭 게이트웨이",
        dark_mode=True
    )
    
    lx, ly, lw, lh = 100, 220, 800, 740
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    
    draw_pill_badge(draw, left_x=lx + 36, cy=ly + 46, text="프로덕트 런처", font=get_font(11, 'bold'), theme='cyan', dark_mode=True, pad_x=12, height=28)
    draw.text((lx + 36, ly + 90), "CodeBridgeX Cloud MES Live Demo", font=get_font(24, 'bold'), fill=(255, 255, 255))
    draw.text((lx + 36, ly + 130), "본 포트폴리오는 실제 배포된 엔터프라이즈 SaaS 아키텍처를 기반으로 제작되었습니다.\n아래 링크 또는 우측 QR 코드를 스캔하여 인터랙티브 뷰어를 즉시 확인하실 수 있습니다.", font=get_font(13.5, 'regular'), fill=(148, 163, 184))
    
    features = [
        ("반응형 슬라이드 뷰어 (Fit-Screen)", "데스크톱 및 모바일 화면비에 맞춰 12장 슬라이드가 100% 자동 스케일링되는 웹 전용 뷰어"),
        ("단축키 & 제스처 내비게이션", "키보드 좌우 방향키 및 모바일 스와이프 터치로 페이지를 매끄럽게 탐색하는 인체공학적 UX"),
        ("고해상도 PDF 다운로드", "오프라인 발표 및 인쇄용 1920×1080 FHD 벡터급 슬라이드 PDF 번들 즉시 다운로드 제공"),
        ("마스터 포트폴리오 허브 연동", "스마트 물타기 계산기, 대한국사, 체크앤페이와 함께 중앙 허브에 정식 등록된 엔터프라이즈 솔루션")
    ]
    
    fy = ly + 210
    for title, desc in features:
        draw.rounded_rectangle([lx + 30, fy, lx + lw - 30, fy + 105], radius=10, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        draw.text((lx + 46, fy + 20), title, font=get_font(14, 'bold'), fill=(56, 189, 248))
        draw.text((lx + 46, fy + 48), desc, font=get_font(11.5, 'medium'), fill=(203, 213, 225))
        fy += 120
        
    rx = 940
    rw = W - rx - 100
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    
    draw_pill_badge(draw, left_x=rx + 36, cy=ly + 46, text="스마트 모바일 접속 QR", font=get_font(11, 'bold'), theme='blue', dark_mode=True, pad_x=12, height=28)
    draw.text((rx + 36, ly + 90), "스캔하여 포트폴리오 열람", font=get_font(22, 'bold'), fill=(255, 255, 255))
    
    qr_url = "https://koyotejw-ux.github.io/auto_portfolio/mes_solution/index.html"
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_size = 260
    qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    
    draw.rounded_rectangle([rx + (rw - qr_size - 24) // 2, ly + 150, rx + (rw + qr_size + 24) // 2, ly + 150 + qr_size + 24], radius=12, fill=(255, 255, 255))
    base.paste(qr_resized, (rx + (rw - qr_size) // 2, ly + 162))
    
    draw.text((rx + rw // 2, ly + 460), "스마트폰 카메라로 스캔 시 즉시 실행됩니다.", font=get_font(12.5, 'medium'), fill=(148, 163, 184), anchor='mm')
    draw.text((rx + rw // 2, ly + 490), qr_url, font=get_font(11.5, 'bold'), fill=(56, 189, 248), anchor='mm')
    
    draw_pill_badge(draw, cx=rx + rw // 2, cy=ly + 560, text="GitHub Pages 프로덕션 배포 완료", font=get_font(11, 'bold'), theme='green', dark_mode=True, pad_x=16, height=32)
    
    draw_slide_footer(draw, 12, dark_mode=True)
    base.save(os.path.join(OUT_DIR, 'slide_12.png'))
    print("SAVED slide_12.png")

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
