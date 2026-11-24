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
            img_resized = img.resize((content_w, content_h), Image.Resampling.LANCZOS)
            base_img.paste(img_resized, (x + 1, y + 39))
        except Exception as e:
            print(f"Error loading screenshot {screenshot_path}:", e)

# ==============================================================
# SLIDE 01: Hero Cover with Multi-Device Responsive Composition
def make_slide_01():
    base = Image.new('RGB', (W, H), (15, 23, 42)) # High-impact dark theme hero
    draw = ImageDraw.Draw(base)
    
    for gx in range(0, W, 40):
        draw.line([(gx, 0), (gx, H)], fill=(23, 33, 56), width=1)
    for gy in range(0, H, 40):
        draw.line([(0, gy), (W, gy)], fill=(23, 33, 56), width=1)
        
    draw_slide_header(
        draw, 
        slide_num=1, 
        category_kr="엔터프라이즈 제조 클라우드 플랫폼", 
        title_black="데스크톱부터 모바일·태블릿까지 연결하는 ", 
        title_blue="반응형 스마트 MES 솔루션", 
        subtitle_kr="수주·발주부터 공정 스케줄링, 설비 텔레메트리, 무결점 품질 검사까지 전 기기 반응형으로 제어하는 올인원 B2B SaaS",
        dark_mode=True
    )
    
    # Left Hero Specs Box
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
        
    # Right Responsive Multi-Device Showcase
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
    print("SAVED slide_01.png (Dark Multi-Device Hero)")

# ==============================================================
# SLIDE 02: User & Market Research
def make_slide_02():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=2, 
        category_kr="사용자 리서치 | 스마트 팩토리 전환 병목 분석", 
        title_black="제조 현장의 분절된 데이터와 수기 기록의 한계, ", 
        title_blue="실시간 데이터 파이프라인의 필요성", 
        subtitle_kr="공장장, 현장 작업자, 품질 관리자 심층 인터뷰를 통해 도출한 4대 핵심 페인포인트와 해결 솔루션"
    )
    
    cards = [
        ("01", "수기 작업일지와 엑셀 취합의 지연", "현장 작업자가 종이 작업일지에 수기로 기입 후 퇴근 전 엑셀에 재입력하여 데이터 취합에 최소 24시간 이상 지연 발생.", "전 공정 모바일/태블릿 1-Tap 실적 등록 및 즉시 중앙 DB 동기화 파이프라인 구축", "green"),
        ("02", "설비 고장 및 비가동 시간 파악 불가", "설비 다운타임 원인과 가동률(OEE)이 실시간 집계되지 않아 병목 라인 조기 식별 불가 및 납기 지연 빈발.", "설비종합효율(OEE) 및 라인별 실시간 가동 상태 텔레메트리 대시보드 제공", "blue"),
        ("03", "LOT 추적 불능으로 인한 클레임 리스크", "불량품 발생 시 어느 원자재 LOT와 작업자가 투입되었는지 역추적하는 데 수일이 소요되어 고객사 신뢰도 하락.", "원자재 입고부터 완제품 출하까지 100% Full-Traceability 바코드/QR 추적 체계", "amber"),
        ("04", "과도하게 복잡한 레거시 ERP UI", "외산/레거시 ERP는 입력 필드가 수십 개에 달해 현장 작업자의 거부감이 심하고 교육 비용 과다 소요.", "아토믹 디자인 기반 직관적 데이터 그리드와 인체공학적 터치 최적화 UI", "purple")
    ]
    
    card_w = (W - 200 - 3 * 24) // 4
    top_y = 220
    card_h = 740
    
    for i, (num, title, pain, sol, theme) in enumerate(cards):
        cx = 100 + i * (card_w + 24)
        draw.rounded_rectangle([cx, top_y, cx + card_w, top_y + card_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        draw_pill_badge(draw, left_x=cx + 24, cy=top_y + 36, text=f"페인포인트 {num}", font=get_font(10.5, 'bold'), theme=theme, pad_x=10, height=26)
        draw.text((cx + 24, top_y + 80), title, font=get_font(17, 'bold'), fill=(15, 23, 42))
        
        draw.rounded_rectangle([cx + 20, top_y + 140, cx + card_w - 20, top_y + 390], radius=10, fill=(255, 255, 255), outline=(239, 68, 68, 120), width=1)
        draw_pill_badge(draw, left_x=cx + 34, cy=top_y + 165, text="현장의 고질적 문제", font=get_font(9.5, 'bold'), theme='red', pad_x=8, height=22)
        lines = textwrap.wrap(pain, width=19)
        ly = top_y + 205
        for l in lines:
            draw.text((cx + 34, ly), l, font=get_font(12.5, 'medium'), fill=(51, 65, 85))
            ly += 25
            
        draw.rounded_rectangle([cx + 20, top_y + 410, cx + card_w - 20, top_y + 700], radius=10, fill=(239, 246, 255), outline=(0, 81, 255, 120), width=1)
        draw_pill_badge(draw, left_x=cx + 34, cy=top_y + 435, text="코드브릿지엑스 UX 해결책", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22)
        lines = textwrap.wrap(sol, width=19)
        ly = top_y + 475
        for l in lines:
            draw.text((cx + 34, ly), l, font=get_font(13, 'bold'), fill=(15, 23, 42))
            ly += 26
            
    draw_slide_footer(draw, 2)
    base.save(os.path.join(OUT_DIR, 'slide_02.png'))
    print("SAVED slide_02.png")

# ==============================================================
# SLIDE 03: Target Audience & Personas
def make_slide_03():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=3, 
        category_kr="타깃 & 페르소나 | 엔터프라이즈 다중 사용자 정의", 
        title_black="경영진부터 현장 실무자까지, ", 
        title_blue="역할별 권한 기반 3대 핵심 페르소나", 
        subtitle_kr="CEO의 경영 인사이트 분석, 생산 관리자의 공정 통제, 작업자의 무오류 실적 입력을 아우르는 맞춤형 UX"
    )
    
    personas = [
        ("CEO / 경영진", "전사 생산성 지표 실시간 관제 및 납기 리스크 선제 대응", "김진우 대표 (52세)", "제조 기업 총괄 경영", [
            ("주요 목표", "일별/월별 생산 목표 달성률 및 종합 수익성 한눈에 조망"),
            ("핵심 니즈", "모바일/태블릿 반응형 경영 대시보드와 OEE 이상 징후 알림"),
            ("UX 솔루션", "Executive KPI 위젯, 매출/납기 예측 차트, 원터치 결재 승인함")
        ], "blue"),
        ("생산관리자 (공장장)", "스마트 간트 공정 계획 수립 및 설비/인력 최적 배치", "박철민 부장 (45세)", "생산본부 공정 관리 총괄", [
            ("주요 목표", "작업 지시서 발행 및 공정별 진척도, 설비 가동 상태 실시간 통제"),
            ("핵심 니즈", "드래그 앤 드롭 일정 조정, 자재 부족 시 선제적 결품 경고"),
            ("UX 솔루션", "인터랙티브 스케줄러, 실시간 병목 공정 히트맵, BOM 역전개 뷰어")
        ], "purple"),
        ("현장 오퍼레이터 (작업자)", "복잡한 키보드 입력 없는 직관적 터치 실적 입력", "이수현 기사 (34세)", "CNC 가공 및 품질 검사 작업", [
            ("주요 목표", "작업 지시 확인, 생산 수량 및 불량 사유를 3초 이내 무오류 등록"),
            ("핵심 니즈", "글러브 착용 시에도 터치 가능한 큰 버튼과 직관적인 바코드 스캔"),
            ("UX 솔루션", "모바일 터치 최적화 숫자 패드, 불량 유형 퀵 셀렉터, 사진 첨부 지원")
        ], "green"),
    ]
    
    card_w = (W - 200 - 2 * 30) // 3
    top_y = 220
    card_h = 740
    
    for i, (role, role_sub, name, job, details, theme) in enumerate(personas):
        cx = 100 + i * (card_w + 30)
        draw.rounded_rectangle([cx, top_y, cx + card_w, top_y + card_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        draw_pill_badge(draw, left_x=cx + 28, cy=top_y + 40, text=role, font=get_font(11, 'bold'), theme=theme, pad_x=12, height=28)
        draw.text((cx + 28, top_y + 80), name, font=get_font(20, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 28, top_y + 112), f"{job} · {role_sub}", font=get_font(12.5, 'medium'), fill=(71, 85, 105))
        
        draw.line([(cx + 28, top_y + 145), (cx + card_w - 28, top_y + 145)], fill=(226, 232, 240), width=1)
        
        dy = top_y + 175
        for k, v in details:
            draw.rounded_rectangle([cx + 24, dy, cx + card_w - 24, dy + 155], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
            draw_pill_badge(draw, left_x=cx + 40, cy=dy + 25, text=k, font=get_font(10, 'bold'), theme=theme, pad_x=8, height=22)
            lines = textwrap.wrap(v, width=32)
            ly = dy + 55
            for l in lines:
                draw.text((cx + 40, ly), l, font=get_font(13.5, 'medium'), fill=(15, 23, 42))
                ly += 26
            dy += 175
            
    draw_slide_footer(draw, 3)
    base.save(os.path.join(OUT_DIR, 'slide_03.png'))
    print("SAVED slide_03.png")

# ==============================================================
# SLIDE 04: Information Architecture (13 Modules) - Centered Alignment
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
    
    # Root Node: Mathematically centered
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
# SLIDE 05: User Flowchart (End-to-End Manufacturing)
def make_slide_05():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=5, 
        category_kr="사용자 플로우 | 완결형 제조 실행 프로세스 파이프라인", 
        title_black="수주부터 생산 계획, 실적 수집, 출하까지의 ", 
        title_blue="무결점 제조 데이터 흐름", 
        subtitle_kr="각 부서 간 병목을 없애고 전사 ERP와 실시간 동기화되는 단계별 사용자 인터랙션 플로우차트"
    )
    
    steps = [
        ("01. 수주 및 납기 검토", "영업팀 수주 등록", "고객사 주문 사양 확인 및 표준 단가 산출", "BOM 소요량 시뮬레이션 및 납기 자동 예측"),
        ("02. 생산 계획 & 자재 발주", "생산관리팀 스케줄링", "간트차트 드래그 앤 드롭 일정 수립", "부족 자재 자동 MRP 발주 및 입고 수입검사"),
        ("03. 작업 지시 & 배포", "현장 라인 투입", "호기별 작업 지시서 및 도면/SOP 전송", "투입 원자재 바코드 스캔 및 LOT 매핑"),
        ("04. 실시간 가공 & 실적 수집", "오퍼레이터 작업 수행", "양품 수량, 불량 사유, 비가동 시간 터치 등록", "설비 센서 텔레메트리 자동 연동 및 OEE 산출"),
        ("05. 최종 품질 검사 & 출하", "품질팀 검사 및 승인", "초/중/종물 검사 및 출하 성적서 자동 발행", "완제품 바코드 부착 및 창고 입고 / 출하 완료")
    ]
    
    step_w = (W - 200 - 4 * 28) // 5
    top_y = 230
    step_h = 710
    
    for i, (num, team, act, sub) in enumerate(steps):
        sx = 100 + i * (step_w + 28)
        draw.rounded_rectangle([sx, top_y, sx + step_w, top_y + step_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        draw_pill_badge(draw, left_x=sx + 20, cy=top_y + 36, text=f"단계 {i+1}", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=26)
        draw.text((sx + 20, top_y + 80), num, font=get_font(15, 'bold'), fill=(15, 23, 42))
        draw_pill_badge(draw, left_x=sx + 20, cy=top_y + 130, text=team, font=get_font(10, 'bold'), theme='purple', pad_x=10, height=24)
        
        draw.rounded_rectangle([sx + 16, top_y + 175, sx + step_w - 16, top_y + 400], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=sx + 30, cy=top_y + 200, text="주요 작업 액션", font=get_font(9.5, 'bold'), theme='cyan', pad_x=8, height=22)
        lines = textwrap.wrap(act, width=19)
        ly = top_y + 235
        for l in lines:
            draw.text((sx + 30, ly), l, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
            ly += 26
            
        draw.rounded_rectangle([sx + 16, top_y + 420, sx + step_w - 16, top_y + 670], radius=10, fill=(239, 246, 255), outline=(0, 81, 255, 120), width=1)
        draw_pill_badge(draw, left_x=sx + 30, cy=top_y + 445, text="시스템 자동 검증 및 기록", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22)
        lines = textwrap.wrap(sub, width=19)
        ly = top_y + 485
        for l in lines:
            draw.text((sx + 30, ly), l, font=get_font(12.5, 'medium'), fill=(51, 65, 85))
            ly += 25
            
        if i < 4:
            arrow_x = sx + step_w + 14
            draw.text((arrow_x, top_y + 350), "▶", font=get_font(18, 'bold'), fill=(0, 81, 255), anchor='mm')
            
    draw_slide_footer(draw, 5)
    base.save(os.path.join(OUT_DIR, 'slide_05.png'))
    print("SAVED slide_05.png")

# ==============================================================
# SLIDE 06: Wireframe & Screen Spec (Using D:\102_1.codebridgex\MES Solution Website Structure 251229)
def make_slide_06():
    base = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=6, 
        category_kr="와이어프레임 & 화면 설계서 | 251229 엔터프라이즈 실물 규격", 
        title_black="태블릿 및 모바일 현장 터치에 최적화된 ", 
        title_blue="실제 설계서 화면 와이어프레임", 
        subtitle_kr="D:\\102_1.codebridgex\\MES Solution Website Structure 251229 프로젝트에서 직접 추출한 표준 화면 규격서와 현장 UI"
    )
    
    # 4 Real Wireframe Screens from 251229
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
        
        # Header in card
        draw_pill_badge(draw, left_x=cx + 20, cy=top_y + 36, text="251229 화면설계서", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=26)
        draw.text((cx + 20, top_y + 76), title, font=get_font(16, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 20, top_y + 104), desc, font=get_font(11, 'medium'), fill=(71, 85, 105))
        
        # Real Wireframe Screenshot Container
        fpath = os.path.join(MOCKUP_DIR, fname)
        frame_y = top_y + 135
        frame_h = card_h - 155
        frame_w = card_w - 32
        
        draw.rounded_rectangle([cx + 16, frame_y, cx + 16 + frame_w, frame_y + frame_h], radius=10, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
        
        if os.path.exists(fpath):
            try:
                wf_img = Image.open(fpath).convert('RGB')
                # Proportional fit inside container (contain mode without stretching!)
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
    print("SAVED slide_06.png (251229 Wireframe Showcase)")

# ==============================================================
# SLIDE 07: Atomic Design System & Tokens
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
        ("01. 데스크톱 대시보드 (라이트)", "render_desktop_dashboard.png", "1920x1080 FHD 상용 관제 UI"),
        ("02. 데스크톱 대시보드 (다크)", "render_desktop_dashboard_dark.png", "현장 조도 최적화 고대비 다크모드"),
        ("03. 태블릿 10-inch (라이트)", "render_tablet_dashboard.png", "공장장 태블릿 반응형 뷰"),
        ("04. 태블릿 10-inch (다크)", "render_tablet_dashboard_dark.png", "현장 패널용 다크 테마 UI"),
        ("05. 모바일 스마트폰 (라이트)", "render_mobile_dashboard.png", "390x844 모바일 1-Tap 터치"),
        ("06. 모바일 스마트폰 (다크)", "render_mobile_dashboard_dark.png", "현장 오퍼레이터 다크 모바일")
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
                thumb_box_w = cell_w - 4
                thumb_box_h = cell_h - 36
                src_w, src_h = img.size
                scale = min(thumb_box_w / src_w, thumb_box_h / src_h)
                target_w = int(round(src_w * scale))
                target_h = int(round(src_h * scale))
                img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                px = cx + 2 + (thumb_box_w - target_w) // 2
                py = cy + 34 + (thumb_box_h - target_h) // 2
                base.paste(img_resized, (px, py))
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
