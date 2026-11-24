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
def make_slide_01():
    base = Image.new('RGB', (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(base)
    
    for gx in range(0, W, 40):
        draw.line([(gx, 0), (gx, H)], fill=(23, 33, 56), width=1)
    for gy in range(0, H, 40):
        draw.line([(0, gy), (W, gy)], fill=(23, 33, 56), width=1)
        
    draw_slide_header(
        draw, 
        slide_num=1, 
        category_kr="엔터프라이즈 제조 클라우드 플랫폼", 
        title_black="데스크톱·태블릿·모바일 반응형으로 완성된 ", 
        title_blue="차세대 스마트 MES 솔루션", 
        subtitle_kr="수주·발주부터 스마트 간트 공정 스케줄러, 설비 종합 효율(OEE) 텔레메트리, 무결점 LOT 추적까지 전 기기 반응형 제어",
        dark_mode=True
    )
    
    left_x, top_y, left_w, box_h = 100, 210, 520, 750
    draw.rounded_rectangle([left_x, top_y, left_x + left_w, top_y + box_h], radius=16, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    
    draw_pill_badge(draw, left_x=left_x + 30, cy=top_y + 40, text="프로덕트 오버뷰", font=get_font(10.5, 'bold'), theme='cyan', dark_mode=True, pad_x=12, height=28)
    draw.text((left_x + 30, top_y + 80), "CodeBridgeX MES Solution", font=get_font(22, 'bold'), fill=(255, 255, 255))
    draw.text((left_x + 30, top_y + 115), "대화면 관제실부터 현장 터치 태블릿, 모바일 기기까지\n완벽하게 대응하는 반응형 스마트 팩토리 플랫폼입니다.", font=get_font(13.5, 'medium'), fill=(148, 163, 184))
    
    specs = [
        ("솔루션 도메인", "스마트 팩토리 통합 MES & ERP 제조 실행 시스템"),
        ("디바이스 지원", "데스크톱(FHD/QHD), 10인치 태블릿, 스마트폰 반응형"),
        ("비즈니스 모듈", "13대 엔터프라이즈 모듈 (생산/품질/자재/영업/회계 등)"),
        ("화면 규격 설계", "59개 이상 표준 인터랙티브 화면 & 아토믹 컴포넌트"),
        ("프론트엔드 스택", "Vite + React 18 + TypeScript + Tailwind CSS"),
        ("UI 테마 지원", "현장 조도에 최적화된 라이트 / 다크 듀얼 테마 지원"),
        ("프로덕트 기여도", "엔터프라이즈 UX/UI 아키텍처 및 디자인 총괄 (100%)"),
    ]
    
    sy = top_y + 185
    for k, v in specs:
        draw.text((left_x + 30, sy), k, font=get_font(12, 'bold'), fill=(203, 213, 225))
        draw.text((left_x + 30, sy + 22), v, font=get_font(13, 'medium'), fill=(56, 189, 248) if "도메인" in k or "기여도" in k or "디바이스" in k else (148, 163, 184))
        draw.line([(left_x + 30, sy + 48), (left_x + left_w - 30, sy + 48)], fill=(51, 65, 85), width=1)
        sy += 66
        
    clean_thumb = r"d:\097.flutter_project\auto_portfolio\assets\mes_solution_clean_devices.png"
    if os.path.exists(clean_thumb):
        right_x = 660
        right_w = W - right_x - 100
        right_h = box_h
        thumb_img = Image.open(clean_thumb).convert('RGB')
        thumb_resized = thumb_img.resize((right_w, right_h), Image.Resampling.LANCZOS)
        base.paste(thumb_resized, (right_x, top_y))
        draw.rounded_rectangle([right_x, top_y, right_x + right_w, top_y + right_h], radius=16, outline=(51, 65, 85), width=1)
    
    draw_slide_footer(draw, 1, dark_mode=True)
    base.save(os.path.join(OUT_DIR, 'slide_01.png'))
    print("SAVED slide_01.png")

# ==============================================================
# SLIDE 02: Research with Donut Chart, H-Bar Chart & SWOT Matrix
def make_slide_02():
    base = Image.new('RGB', (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=2, 
        category_kr="사용자 리서치 | 스마트 팩토리 전환 병목 & 정량 데이터 분석", 
        title_black="제조 현장의 분절된 데이터와 수기 기록의 한계, ", 
        title_blue="실시간 데이터 파이프라인의 필요성", 
        subtitle_kr="국내 48개 중소·중견 제조사 실태 조사 및 작업자 320명 설문 기반 정량적 병목 분석과 3대 해결 전략"
    )
    
    # -------------------------------------------------------------
    # TOP: 3 Data Visualization Cards
    # -------------------------------------------------------------
    sy = 220
    card_w = 540
    card_h = 240
    gap = 50
    
    # 1. Card 1: Donut Chart (수기 일지 지연률 82.4%)
    c1_x = 100
    draw.rounded_rectangle([c1_x, sy, c1_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c1_x, sy + 18, c1_x + 5, sy + card_h - 18], radius=2, fill=(225, 29, 72))
    draw_pill_badge(draw, left_x=c1_x + 24, cy=sy + 26, text="PAIN POINT", font=get_font(10, 'bold'), theme='red', pad_x=8, height=22)
    draw.text((c1_x + 24, sy + 58), "수기 일지와 엑셀 취합의 지연", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c1_x + 24, sy + 88), "작업자가 종이 일지에 작성 후 퇴근 전 엑셀 입력\n데이터 집계에 평균 24시간 이상 지연 발생합니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139))
    draw.text((c1_x + 24, sy + 144), "82.4%", font=get_num_font(30, 'black'), fill=(225, 29, 72))
    draw.text((c1_x + 24, sy + 188), "일일 실적 집계 지연 호소 (N=320)", font=get_font(11, 'bold'), fill=(225, 29, 72))
    
    # Donut
    ch1_cx = c1_x + card_w - 95
    ch1_cy = sy + card_h // 2 + 10
    cr1 = 58
    thick1 = 14
    draw.ellipse([ch1_cx - cr1, ch1_cy - cr1, ch1_cx + cr1, ch1_cy + cr1], fill=(241, 245, 249))
    arc_deg = int(round(360 * 0.824))
    draw.pieslice([ch1_cx - cr1, ch1_cy - cr1, ch1_cx + cr1, ch1_cy + cr1], start=-90, end=-90 + arc_deg, fill=(225, 29, 72))
    draw.ellipse([ch1_cx - (cr1 - thick1), ch1_cy - (cr1 - thick1), ch1_cx + (cr1 - thick1), ch1_cy + (cr1 - thick1)], fill=(255, 255, 255))
    draw.text((ch1_cx, ch1_cy - 6), "82%", font=get_num_font(15, 'black'), fill=(15, 23, 42), anchor='mm')
    draw.text((ch1_cx, ch1_cy + 10), "수기 지연", font=get_font(8.5, 'bold'), fill=(100, 116, 139), anchor='mm')
    
    # 2. Card 2: H-Bar Chart (설비 가동률 OEE 격차)
    c2_x = c1_x + card_w + gap
    draw.rounded_rectangle([c2_x, sy, c2_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c2_x, sy + 18, c2_x + 5, sy + card_h - 18], radius=2, fill=(217, 119, 6))
    draw_pill_badge(draw, left_x=c2_x + 24, cy=sy + 26, text="EQUIPMENT OEE", font=get_font(10, 'bold'), theme='amber', pad_x=8, height=22)
    draw.text((c2_x + 24, sy + 58), "설비 다운타임 원인 파악 불능", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c2_x + 24, sy + 88), "고장 원인 분석 누락으로 비가동 손실이 누적되며\n설비종합효율(OEE)이 55% 수준에 머물렀습니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139))
    draw.text((c2_x + 24, sy + 144), "54.8% → 88.5%", font=get_num_font(28, 'black'), fill=(217, 119, 6))
    draw.text((c2_x + 24, sy + 188), "OEE 효율 +33.7%p 실시간 개선", font=get_font(11, 'bold'), fill=(16, 185, 129))
    
    hb_x = c2_x + card_w - 180
    hb_y = sy + 76
    h_data = [("도입 전 레거시", 85, (203, 213, 225), "OEE 54.8%"), ("CodeBridgeX", 145, (0, 81, 255), "OEE 88.5%")]
    for hidx, (hlbl, hval, hcol, hstat) in enumerate(h_data):
        hy = hb_y + hidx * 62
        draw.text((hb_x, hy), hlbl, font=get_font(10, 'bold'), fill=(71, 85, 105))
        draw.text((hb_x + 155, hy), hstat, font=get_font(9.5, 'bold'), fill=hcol, anchor='rm')
        draw.rounded_rectangle([hb_x, hy + 18, hb_x + 155, hy + 28], radius=5, fill=(241, 245, 249))
        draw.rounded_rectangle([hb_x, hy + 18, hb_x + hval, hy + 28], radius=5, fill=hcol)
        
    # 3. Card 3: Bar Chart (LOT 추적 소요 시간)
    c3_x = c2_x + card_w + gap
    draw.rounded_rectangle([c3_x, sy, c3_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c3_x, sy + 18, c3_x + 5, sy + card_h - 18], radius=2, fill=(0, 81, 255))
    draw_pill_badge(draw, left_x=c3_x + 24, cy=sy + 26, text="TRACEABILITY", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((c3_x + 24, sy + 58), "원자재-완제품 LOT 역추적 혁신", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c3_x + 24, sy + 88), "불량 발생 시 투입 원자재 및 작업자 추적에 수일 소요\n바코드 스캔 기반 1-Tap 즉시 역추적 체계 구현.", font=get_font(11.5, 'regular'), fill=(100, 116, 139))
    draw.text((c3_x + 24, sy + 144), "3일 → 1초", font=get_num_font(30, 'black'), fill=(0, 81, 255))
    draw.text((c3_x + 24, sy + 188), "클레임 대응 속도 99.9% 단축", font=get_font(11, 'bold'), fill=(0, 81, 255))
    
    # -------------------------------------------------------------
    # BOTTOM: SWOT Strategic Decision Matrix (y=490, h=470)
    # -------------------------------------------------------------
    swot_y = 490
    swot_w = 405
    swot_h = 470
    swot_gap = 33
    
    swot_data = [
        ("STRENGTH (강점)", "blue", [
            ("아토믹 디자인 150+ 토큰", "일관된 반응형 B2B 디자인 킷으로 개발 생산성 3배 증대"),
            ("13대 통합 엔터프라이즈 모듈", "단일 플랫폼에서 수주부터 회계, 인사까지 올인원 제어"),
            ("라이트/다크 듀얼 테마", "현장 터치 패널과 관제실 조도 환경에 맞춤형 가시성 제공")
        ]),
        ("WEAKNESS (약점)", "amber", [
            ("현장 작업자 고령화", "IT 기기 조작 미숙련 작업자의 시스템 도입 심리적 저항"),
            ("다양한 레거시 설비 인터페이스", "구형 PLC 및 센서 프로토콜 파편화로 텔레메트리 연동 난이도"),
            ("초기 기준정보(BOM) 구축 공수", "다단계 품목 전개 데이터 정제에 초기 투입 인력 소요")
        ]),
        ("OPPORTUNITY (기회)", "green", [
            ("정부 스마트 공장 지원 사업", "중소벤처기업부 클라우드형 스마트 팩토리 보급 확산 가속"),
            ("중대재해 및 공급망 실사법", "원자재 추적성(Traceability) 및 안전 설비 점검 법제화"),
            ("글로벌 SaaS 수출 확장", "다국어 지원 및 멀티테넌트 아키텍처로 동남아/미주 진출")
        ]),
        ("THREAT (위협)", "red", [
            ("외산 거대 ERP 솔루션", "SAP, 오라클 등 글로벌 대기업 레거시 락인(Lock-in) 장벽"),
            ("제조 기업 보안 규제", "온프레미스 고수 및 클라우드 데이터 유출에 대한 우려"),
            ("단순 가격 경쟁 솔루션", "저가형 웹 패키지의 난립으로 인한 시장 가격 교란")
        ])
    ]
    
    for i, (title, theme, bullets) in enumerate(swot_data):
        bx = 100 + i * (swot_w + swot_gap)
        draw.rounded_rectangle([bx, swot_y, bx + swot_w, swot_y + swot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=bx + 20, cy=swot_y + 26, text=title, font=get_font(10, 'bold'), theme=theme, pad_x=10, height=24)
        
        by = swot_y + 65
        for b_title, b_desc in bullets:
            draw.rounded_rectangle([bx + 16, by, bx + swot_w - 16, by + 115], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.text((bx + 28, by + 18), b_title, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
            lines = textwrap.wrap(b_desc, width=28)
            ly = by + 45
            for l in lines:
                draw.text((bx + 28, ly), l, font=get_font(11.5, 'medium'), fill=(71, 85, 105))
                ly += 22
            by += 130
            
    draw_slide_footer(draw, 2)
    base.save(os.path.join(OUT_DIR, 'slide_02.png'))
    print("SAVED slide_02.png (Research with Charts & SWOT)")

# ==============================================================
# SLIDE 03: Target Matrix & 3 Personas with Behavioral Sliders
def make_slide_03():
    base = Image.new('RGB', (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=3, 
        category_kr="타깃 & 페르소나 | 2x2 세그멘테이션 매트릭스 & 역할별 페르소나", 
        title_black="경영진의 실시간 의사결정부터 현장 터치까지, ", 
        title_blue="역할별 권한 기반 맞춤형 UX 아키텍처", 
        subtitle_kr="데이터 조작 빈도와 현장성 축으로 분류한 2x2 타깃 매트릭스와 행동 지표 스펙트럼 슬라이더"
    )
    
    # -------------------------------------------------------------
    # 1. TOP-LEFT: 2x2 Target Segmentation Matrix (x=100, w=840, h=300)
    # -------------------------------------------------------------
    mx_x = 100
    mx_y = 220
    mx_w = 840
    mx_h = 300
    
    draw.rounded_rectangle([mx_x, mx_y, mx_x + mx_w, mx_y + mx_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=mx_x + 24, cy=mx_y + 24, text="TARGET MATRIX", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((mx_x + 155, mx_y + 24), "2x2 세그멘테이션 : 데이터 분석 깊이 vs. 현장 이동성", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    qw = 385
    qh = 105
    q1_x = mx_x + 24
    q1_y = mx_y + 55
    q2_x = q1_x + qw + 22
    q2_y = q1_y
    q3_x = q1_x
    q3_y = q1_y + qh + 16
    q4_x = q2_x
    q4_y = q3_y
    
    # Q1: CEO / 경영진
    draw.rounded_rectangle([q1_x, q1_y, q1_x + qw, q1_y + qh], radius=10, fill=(239, 246, 255), outline=(0, 81, 255, 120), width=1)
    draw.text((q1_x + 16, q1_y + 16), "경영진 / CEO (Executive Viewer)", font=get_font(12.5, 'bold'), fill=(0, 81, 255))
    draw.text((q1_x + 16, q1_y + 40), "· 데이터 분석: 고도화 종합 KPI & 손익 분석\n· 디바이스: 모바일 / 태블릿 반응형 관제", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # Q2: 생산/공정 관리자
    draw.rounded_rectangle([q2_x, q2_y, q2_x + qw, q2_y + qh], radius=10, fill=(245, 243, 255), outline=(124, 58, 237, 120), width=1)
    draw.text((q2_x + 16, q2_y + 16), "공장장 / 생산관리자 (Operational Planner)", font=get_font(12.5, 'bold'), fill=(124, 58, 237))
    draw.text((q2_x + 16, q2_y + 40), "· 데이터 분석: 스마트 간트 스케줄링 & 설비 배정\n· 디바이스: 데스크톱 대화면 + 10인치 태블릿", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # Q3: 현장 오퍼레이터
    draw.rounded_rectangle([q3_x, q3_y, q3_x + qw, q3_y + qh], radius=10, fill=(236, 253, 245), outline=(16, 185, 129, 120), width=1)
    draw.text((q3_x + 16, q3_y + 16), "현장 작업자 / 오퍼레이터 (Field Operator)", font=get_font(12.5, 'bold'), fill=(16, 185, 129))
    draw.text((q3_x + 16, q3_y + 40), "· 데이터 조작: 1-Tap 바코드 스캔 & 터치 실적 입력\n· 디바이스: 현장 터치 패널 모니터 / 모바일", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # Q4: 품질/자재 관리자
    draw.rounded_rectangle([q4_x, q4_y, q4_x + qw, q4_y + qh], radius=10, fill=(254, 243, 199), outline=(217, 119, 6, 120), width=1)
    draw.text((q4_x + 16, q4_y + 16), "품질/자재 검사원 (Quality Specialist)", font=get_font(12.5, 'bold'), fill=(217, 119, 6))
    draw.text((q4_x + 16, q4_y + 40), "· 데이터 조작: AQL 검사 기준서 & SPC 관리도 분석\n· 디바이스: 태블릿 현장 검사 + PC 리포트", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # -------------------------------------------------------------
    # 2. TOP-RIGHT: 4 Benchmark Comparison Cards (x=980, w=840, h=300)
    # -------------------------------------------------------------
    bm_x = 980
    bm_y = 220
    bm_w = 840
    bm_h = 300
    
    draw.rounded_rectangle([bm_x, bm_y, bm_x + bm_w, bm_y + bm_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=bm_x + 24, cy=bm_y + 24, text="BENCHMARK", font=get_font(10, 'bold'), theme='purple', pad_x=8, height=22)
    draw.text((bm_x + 145, bm_y + 24), "국내외 주요 솔루션 대비 차별화 경쟁력 비교", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    b_cols = [
        ("비교 항목", ["반응형 웹 지원", "아토믹 UI 킷", "LOT 역추적 속도", "초기 도입 비용"]),
        ("CodeBridgeX", ["데스크톱/태블릿/모바일", "150+ 표준 토큰 완비", "1초 원터치 즉시 조회", "클라우드 SaaS 월구독"]),
        ("외산 레거시 S사", ["PC 한정 (반응형 불가)", "수십년 구형 윈도우 UI", "수분~수시간 지연", "수억원 초기 구축비"]),
        ("국내 패키지 D사", ["모바일 웹 전용 앱 분리", "비표준 파편화 컴포넌트", "엑셀 수기 취합 연동", "서버 호스팅 라이선스"])
    ]
    
    tx_start = bm_x + 24
    ty_start = bm_y + 60
    col_widths = [130, 230, 210, 220]
    
    cur_x = tx_start
    for ci, (col_title, items) in enumerate(b_cols):
        cw = col_widths[ci]
        draw.rounded_rectangle([cur_x, ty_start, cur_x + cw - 10, ty_start + 30], radius=6, fill=(239, 246, 255) if ci==1 else (241, 245, 249))
        draw.text((cur_x + 8, ty_start + 15), col_title, font=get_font(11, 'bold'), fill=(0, 81, 255) if ci==1 else (71, 85, 105), anchor='lm')
        
        iy = ty_start + 38
        for it in items:
            draw.rounded_rectangle([cur_x, iy, cur_x + cw - 10, iy + 36], radius=4, fill=(255, 255, 255), outline=(0, 81, 255) if ci==1 else (226, 232, 240), width=1)
            draw.text((cur_x + 8, iy + 18), it, font=get_font(10.5, 'bold' if ci==1 else 'medium'), fill=(0, 81, 255) if ci==1 else (51, 65, 85), anchor='lm')
            iy += 42
        cur_x += cw
        
    # -------------------------------------------------------------
    # 3. BOTTOM: 3 Persona Detail Cards with Behavioral Spectrum Sliders
    # -------------------------------------------------------------
    bot_y = 550
    pw = 540
    ph = 420
    p_gap = 50
    
    personas_full = [
        ("김진우 대표 (52세)", "CEO / 총괄 경영", "외출 중에도 공장 가동 상태와 긴급 납기 지연을 즉시 확인해야 합니다.", [
            ("모바일 접속 비중", "현장 터치", "모바일 전용", 0.85, 'blue'),
            ("데이터 집계 수준", "로우 데이터", "KPI 요약", 0.95, 'blue'),
            ("결재/승인 빈도", "주간 집계", "실시간 승인", 0.90, 'blue')
        ], "blue"),
        ("박철민 부장 (45세)", "공장장 / 생산관리 총괄", "공정 간트차트 일정 조정과 설비 부하를 한눈에 통제해야 합니다.", [
            ("디바이스 활용도", "모바일", "PC+태블릿", 0.90, 'purple'),
            ("공정 제어 정밀도", "일별 관리", "초단위 관제", 0.85, 'purple'),
            ("자재 결품 대응력", "사후 처리", "사전 경보", 0.95, 'purple')
        ], "purple"),
        ("이수현 기사 (34세)", "현장 오퍼레이터", "장갑을 낀 상태에서도 3초 내에 실적과 불량 사유를 등록해야 합니다.", [
            ("터치 인터페이스", "키보드 입력", "큰 버튼 터치", 0.95, 'green'),
            ("오류 입력 방지율", "일반 인풋", "바코드 스캔", 0.98, 'green'),
            ("조도 적응도", "일반 모드", "다크 모드", 0.80, 'green')
        ], "green")
    ]
    
    for pi, (p_name, p_role, p_quote, sliders, theme) in enumerate(personas_full):
        px = 100 + pi * (pw + p_gap)
        draw.rounded_rectangle([px, bot_y, px + pw, bot_y + ph], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=px + 20, cy=bot_y + 24, text=p_role, font=get_font(10, 'bold'), theme=theme, pad_x=10, height=24)
        draw.text((px + 20, bot_y + 60), p_name, font=get_font(18, 'bold'), fill=(15, 23, 42))
        draw.text((px + 20, bot_y + 88), f'"{p_quote}"', font=get_font(11.5, 'medium'), fill=(100, 116, 139))
        
        draw.line([(px + 20, bot_y + 115), (px + pw - 20, bot_y + 115)], fill=(226, 232, 240), width=1)
        
        # Behavioral Sliders
        sly = bot_y + 140
        for s_lbl, l_txt, r_txt, ratio, s_thm in sliders:
            draw.text((px + 20, sly), s_lbl, font=get_font(11, 'bold'), fill=(15, 23, 42))
            draw.text((px + 130, sly), l_txt, font=get_font(9.5, 'medium'), fill=(100, 116, 139))
            draw.text((px + pw - 25, sly), r_txt, font=get_font(9.5, 'medium'), fill=(100, 116, 139), anchor='rm')
            
            # Slider Track
            track_x = px + 195
            track_w = pw - 230 - 70
            track_y = sly + 4
            draw.rounded_rectangle([track_x, track_y, track_x + track_w, track_y + 6], radius=3, fill=(241, 245, 249))
            active_w = int(round(track_w * ratio))
            active_col = (0, 81, 255) if s_thm=='blue' else ((124, 58, 237) if s_thm=='purple' else (16, 185, 129))
            draw.rounded_rectangle([track_x, track_y, track_x + active_w, track_y + 6], radius=3, fill=active_col)
            # Dot
            draw.ellipse([track_x + active_w - 5, track_y - 2, track_x + active_w + 5, track_y + 8], fill=(255, 255, 255), outline=active_col, width=2)
            sly += 80
            
    draw_slide_footer(draw, 3)
    base.save(os.path.join(OUT_DIR, 'slide_03.png'))
    print("SAVED slide_03.png (Target Matrix, Benchmark & Sliders)")

# ==============================================================
# SLIDE 04: Information Architecture (Exact Centered Tree)
def make_slide_04():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=4, 
        category_kr="정보 구조 설계 | 13대 비즈니스 모듈 & 멀티테넌트 아키텍처", 
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
        category_kr="사용자 플로우 | 5단계 서비스 인터랙션 & 데이터 파이프라인", 
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
        title_blue="정량적 데이터 성과", 
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
