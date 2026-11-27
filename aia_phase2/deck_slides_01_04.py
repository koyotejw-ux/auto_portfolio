import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from deck_common import (
    W, H, BASE_DIR, CORE_DIR, QI_DIR, OUT_DIR,
    AIA_RED, AIA_RED_DARK, AIA_RED_LIGHT, AIA_RED_BORDER,
    BG_DARK, CARD_DARK, BORDER_DARK, TEXT_DARK_MAIN, TEXT_DARK_SUB,
    BG_LIGHT, CARD_LIGHT, BORDER_LIGHT, BORDER_LIGHT_ACCENT,
    TEXT_LIGHT_MAIN, TEXT_LIGHT_SUB,
    get_font, get_num_font, wrap_text, draw_pill_badge, draw_arrow,
    draw_slide_header, draw_slide_footer, draw_phone_mockup
)

# -------------------------------------------------------------
# SLIDE 01: HERO COVER (AIA+ SENIOR MODE - REAL HERO SCREEN)
# -------------------------------------------------------------
def make_slide_01():
    img = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Subtle warm background gradient/glow
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([800, 100, 1800, 1000], fill=(211, 17, 69, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    img.paste(glow, (0, 0), glow)
    
    draw = ImageDraw.Draw(img)
    
    # Top Category Pill
    draw_pill_badge(draw, left_x=120, cy=105, text="AIA LIFE · SENIOR ACCESSIBILITY INNOVATION", font=get_font(11, 'bold'), theme='red', pad_x=14, height=28)
    draw_pill_badge(draw, left_x=440, cy=105, text="Qi DESIGN SYSTEM v3.3", font=get_font(11, 'bold'), theme='gray', pad_x=12, height=28)
    
    # Hero Title matching Behance: AIA+ SENIOR MODE
    draw.text((120, 155), "AIA+", font=get_font(60, 'black'), fill=(15, 23, 42))
    draw.text((275, 155), "SENIOR MODE", font=get_font(60, 'black'), fill=AIA_RED)
    draw.text((120, 235), "고령자 친화 배리어프리 금융 UX & 10대 비대면 서비스 리뉴얼", font=get_font(26, 'bold'), fill=(51, 65, 85))
    
    desc_kr = (
        "금융위원회 '고령자 친화적 모바일 금융앱 가이드라인' 100% 완벽 준수\n"
        "6070 액티브 시니어를 위한 제로-뎁스(Zero-Depth) 직관 탐색 아키텍처와\n"
        "Qi 글로벌 디자인 시스템 v3.3 기반의 단일 소스 멀티 테마 프로덕트 디자인"
    )
    draw.text((120, 295), desc_kr, font=get_font(15.5, 'regular'), fill=(100, 116, 139), spacing=8)
    
    # Overview 5 Core Action Spheres
    draw.text((120, 400), "AIA+ 고령자 모드 5대 핵심 서비스 (Overview)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    spheres = [
        ("조회", "계약/납입액 확인", (59, 130, 246)),
        ("납입", "보험료 바로 내기", AIA_RED),
        ("청구", "병원비 서류 접수", (168, 85, 247)),
        ("대출", "환급금 계약대출", (16, 185, 129)),
        ("상담", "큰글씨 고객센터", (71, 85, 105))
    ]
    for idx, (s_name, s_sub, s_col) in enumerate(spheres):
        sx = 120 + idx * 125
        sy = 450
        draw.ellipse([sx, sy, sx + 95, sy + 95], fill=s_col)
        draw.text((sx + 47, sy + 38), s_name, font=get_font(18, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((sx + 47, sy + 62), s_sub, font=get_font(9.5, 'medium'), fill=(255, 255, 255), anchor='mm')
        
    # Bottom 4 Metric Cards
    stats = [
        ("100%", "금융위 규제 가이드라인 준수"),
        ("2x", "본문 및 버튼 폰트 크기 확대"),
        ("90%", "시니어 코어 과업 완수율 달성"),
        ("50%", "비대면 업무 소요 시간 단축")
    ]
    card_y = 610
    for idx, (val, label) in enumerate(stats):
        cx = 120 + (idx % 2) * 280
        cy = card_y + (idx // 2) * 110
        cw, ch = 265, 95
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((cx + 20, cy + 20), val, font=get_num_font(32, 'black'), fill=AIA_RED if idx==0 else (15, 23, 42))
        lines = wrap_text(label, get_font(11.5, 'medium'), cw - 40, draw)
        ly = cy + 56
        for line in lines:
            draw.text((cx + 20, ly), line, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_SUB)
            ly += 16
            
    # Bottom Specs Bar
    spec_y = 855
    draw.rounded_rectangle([120, spec_y, 680, spec_y + 115], radius=14, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    specs = [
        ("프로젝트", "AIA생명 AIA+ Phase 2 고령자 모드 & 비대면 서비스 리뉴얼"),
        ("수행 역할", "메인화면(일반/고령자) & 전체 서비스 아키텍처/화면설계 100% 단독 총괄"),
        ("핵심 혁신", "일반모드 ↔ 고령자모드 원클릭 스위칭 & 금융위 가이드라인 완전 준수")
    ]
    for idx, (label, val) in enumerate(specs):
        sy = spec_y + 15 + idx * 31
        draw.text((140, sy), label, font=get_font(12, 'bold'), fill=AIA_RED)
        draw.text((225, sy), val, font=get_font(12, 'bold' if idx==1 else 'medium'), fill=(15, 23, 42))
        
    # Right Column: Actual Devices with Authentic Hero Main Screen
    gen_screen = os.path.join(CORE_DIR, "screen_general_main_clean.png")
    if not os.path.exists(gen_screen):
        gen_screen = os.path.join(CORE_DIR, "screen_general_main.png")
    
    sen_screen = os.path.join(CORE_DIR, "screen_senior_main_hero.png")
    if not os.path.exists(sen_screen):
        sen_screen = os.path.join(CORE_DIR, "screen_senior_main_home.png")
        
    pay_screen = os.path.join(CORE_DIR, "screen_pay_list_senior.png")
    
    draw_phone_mockup(img, gen_screen, cx=930, cy=565, phone_w=280, phone_h=605, bezel=6, radius=32, show_toggle_badge="[일반모드] 메인화면")
    draw_phone_mockup(img, sen_screen, cx=1260, cy=530, phone_w=335, phone_h=715, bezel=7, radius=36, show_toggle_badge="[고령자모드] 원터치 홈 (총괄설계)")
    draw_phone_mockup(img, pay_screen, cx=1590, cy=565, phone_w=280, phone_h=605, bezel=6, radius=32, show_toggle_badge="[간편납부] 56dp CTA")
    
    draw_arrow(draw, (1075, 565), (1095, 565), col=AIA_RED, width=3, arrow_size=8)
    draw_pill_badge(draw, cx=1085, cy=535, text="1-Tap 전환", font=get_font(10, 'bold'), theme='red', solid=True, pad_x=8, height=20)
    
    draw_pill_badge(draw, cx=1260, cy=145, text="고령자 친화 제로-뎁스 원터치 홈 · 직접 기획 및 화면설계", font=get_font(12, 'bold'), theme='red', solid=True, pad_x=16, height=32)
    
    draw_slide_footer(draw, 1, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_01.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 02: PROBLEMS & RESEARCH (4 Core Industry Problems & Solution)
# -------------------------------------------------------------
def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 2, 
        "PROBLEMS & RESEARCH", 
        "Problems & Research | ", 
        "금융사 고령자 모드 실태 조사 및 4대 핵심 문제점", 
        "보험사/금융사의 형식적 모드 도입 한계와 AIA+ Phase 2의 배리어프리 해결 방향성", 
        right_badge=("KEY RESEARCH", "red")
    )
    
    # 4 Core Problems Grid matching User's Exact Deliverable (2 Columns x 2 Rows)
    card_y = 220
    card_h = 730
    
    problems = [
        {
            "num": "1",
            "title": "고령자 배려 부족",
            "as_is": "각 보험사 및 금융사들이 '고령자 모드' 또는 '간편 모드'를 도입했지만, 글씨 크기와 화면 배치 차이가 미미하고 모드 전환 기능도 찾기 어려워 형식적 대응에 그침.",
            "to_be": "AIA+ 솔루션: 18pt 이상 대형 활자 규격화, 폰트 2배 확대 및 상단 1-Tap 토글 스위치 전면 배치로 직관적 모드 전환 보장."
        },
        {
            "num": "2",
            "title": "명칭과 UI 차이로 혼란 초래",
            "as_is": "각 금융사마다 서로 다른 명칭(예: KB국민·하나은행 '간편홈', 신한·우리은행 '쉬운홈')을 사용해 소비자가 쉽게 인식하지 못함. 통일성 확보 필요.",
            "to_be": "AIA+ 솔루션: '간편홈(고령자모드)' 표준 명칭 정립 및 인지적 혼란을 없앤 일관된 직관적 심볼과 명확한 텍스트 병기."
        },
        {
            "num": "3",
            "title": "접근성 낮은 UI 설계",
            "as_is": "모드 전환 버튼이 앱 하단에 위치하거나 글씨가 작아 고령층이 사용하기 어려움. 가독성과 접근성 개선 절실.",
            "to_be": "AIA+ 솔루션: 엄지손가락 인체공학적 터치 영역(Thumb Zone)을 고려한 56dp 풀와이드 버튼 및 헤더 최상단 원터치 스위치 설계."
        },
        {
            "num": "4",
            "title": "보험업권 모바일 금융앱 간편모드 지침 및 AIA 휴리스틱 고려",
            "as_is": "금융감독원/금융위원회에서 권장하는 고령자 친화 간편모드 지침(글자크기, 명도대비, 대체수단) 미준수 사례 다수.",
            "to_be": "AIA+ 솔루션: 금융당국 가이드라인 100% 충족 + AIA 글로벌 Qi 디자인 시스템 v3.3 휴리스틱 검증 체계 완벽 결합."
        }
    ]
    
    gw = 840
    gh = 330
    coords = [
        (100, card_y),
        (980, card_y),
        (100, card_y + 360),
        (980, card_y + 360)
    ]
    
    for (gx, gy), p in zip(coords, problems):
        draw.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Number Badge
        draw.rounded_rectangle([gx + 25, gy + 22, gx + 60, gy + 57], radius=8, fill=AIA_RED)
        draw.text((gx + 42, gy + 39), p["num"], font=get_font(18, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        draw.text((gx + 75, gy + 32), p["title"], font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        # Problem Box (AS-IS)
        draw.rounded_rectangle([gx + 25, gy + 75, gx + gw - 25, gy + 185], radius=10, fill=(255, 241, 244), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=gx + 40, cy=gy + 98, text="AS-IS 문제점 (현 금융사 실태)", font=get_font(10, 'bold'), theme='red', pad_x=8, height=20)
        lines = wrap_text(p["as_is"], get_font(12, 'regular'), gw - 80, draw)
        ly = gy + 120
        for line in lines:
            draw.text((gx + 40, ly), line, font=get_font(12, 'regular'), fill=TEXT_LIGHT_MAIN)
            ly += 19
            
        # Solution Box (TO-BE)
        draw.rounded_rectangle([gx + 25, gy + 200, gx + gw - 25, gy + 310], radius=10, fill=(236, 253, 245), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=gx + 40, cy=gy + 223, text="TO-BE 혁신 설계 (AIA+ 해결책)", font=get_font(10, 'bold'), theme='green', pad_x=8, height=20)
        lines_to = wrap_text(p["to_be"], get_font(12, 'bold'), gw - 80, draw)
        ly_to = gy + 245
        for line in lines_to:
            draw.text((gx + 40, ly_to), line, font=get_font(12, 'medium'), fill=(5, 150, 105))
            ly_to += 19
            
    draw_slide_footer(draw, 2, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_02.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 03: RESEARCH & HEURISTIC ANALYSIS (Pie Charts & Bars)
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 3, 
        "RESEARCH & HEURISTIC ANALYSIS", 
        "Research & Heuristic Analysis | ", 
        "고령층 디지털 금융 이용 행태 및 페인포인트 분석", 
        "정량 데이터 분석과 금융감독원 가이드라인 진단을 통해 도출된 개선 우선순위", 
        right_badge=("DATA DRIVEN", "red")
    )
    
    # Left Column: Demographics & Problem Definition (W=760)
    lx = 100
    ly = 220
    lw = 760
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 30, cy=ly + 38, text="USER DEMOGRAPHICS & BEHAVIOR", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 30, ly + 72), "고령자 모바일 이용 행태 정량 분석", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # 1. Pie Chart: Age Distribution
    pie_cx, pie_cy, pie_r = lx + 180, ly + 220, 95
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=0, end=151, fill=AIA_RED)
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=151, end=277, fill=(59, 130, 246))
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=277, end=360, fill=(71, 85, 105))
    draw.ellipse([pie_cx - 45, pie_cy - 45, pie_cx + 45, pie_cy + 45], fill=CARD_LIGHT)
    draw.text((pie_cx, pie_cy), "60-70대", font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    # Pie Legend
    draw.rounded_rectangle([lx + 330, ly + 145, lx + 346, ly + 161], radius=3, fill=AIA_RED)
    draw.text((lx + 355, ly + 144), "60~64세 (42%) · 모바일 금융 숙련", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    draw.rounded_rectangle([lx + 330, ly + 195, lx + 346, ly + 211], radius=3, fill=(59, 130, 246))
    draw.text((lx + 355, ly + 194), "65~69세 (35%) · 가독성/안내 필요", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    draw.rounded_rectangle([lx + 330, ly + 245, lx + 346, ly + 261], radius=3, fill=(71, 85, 105))
    draw.text((lx + 355, ly + 244), "70세 이상 (23%) · 대면/전화 의존", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    draw.line([(lx + 30, ly + 345), (lx + lw - 30, ly + 345)], fill=BORDER_LIGHT, width=1)
    
    # 2. Bar Chart: Pain Point Distribution
    draw.text((lx + 30, ly + 375), "모바일 앱 이용 시 5대 핵심 불편사항 (Pain Points)", font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN)
    bar_items = [
        ("작은 글씨와 불명확한 대비 (1. 배려 부족)", 88, AIA_RED),
        ("금융사별 용어 혼란 (2. 명칭 통일성 부재)", 74, (245, 158, 11)),
        ("접근하기 어려운 버튼 위치 (3. 낮은 접근성)", 62, (59, 130, 246)),
        ("복잡한 본인인증 및 가상계좌 부재", 54, (168, 85, 247)),
        ("진행 상태 확인 불가로 인한 불안감", 41, (100, 116, 139))
    ]
    by = ly + 420
    for blabel, bval, bcol in bar_items:
        draw.text((lx + 30, by), blabel, font=get_font(12, 'medium'), fill=TEXT_LIGHT_MAIN)
        draw.rounded_rectangle([lx + 30, by + 24, lx + 30 + int(bval * 6.5), by + 40], radius=4, fill=bcol)
        draw.text((lx + 45 + int(bval * 6.5), by + 22), f"{bval}%", font=get_num_font(12, 'bold'), fill=bcol)
        by += 56
        
    # Right Column: Heuristic Evaluation & Regulatory Matrix (W=880)
    rx = 900
    rw = 880
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ly + 38, text="HEURISTIC & REGULATORY AUDIT", font=get_font(11, 'bold'), theme='gray', pad_x=12, height=24)
    draw.text((rx + 30, ly + 72), "금융위 고령자 모바일앱 가이드라인 진단 매트릭스", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Table Header
    th_y = ly + 120
    draw.rounded_rectangle([rx + 30, th_y, rx + rw - 30, th_y + 40], radius=8, fill=(241, 245, 249))
    draw.text((rx + 50, th_y + 20), "가이드라인 세부 항목", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    draw.text((rx + 300, th_y + 20), "AS-IS 문제점 (기존)", font=get_font(12, 'bold'), fill=AIA_RED, anchor='lm')
    draw.text((rx + 570, th_y + 20), "TO-BE 솔루션 (Phase 2)", font=get_font(12, 'bold'), fill=(16, 185, 129), anchor='lm')
    draw.text((rx + 790, th_y + 20), "준수 상태", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    audit_rows = [
        ("화면 구조 단순화", "메뉴 뎁스 4~5단계, 탐색 혼선", "단일 화면 원터치 5대 핵심 메뉴", "100% 충족"),
        ("글자 크기 확대", "기본 12~14pt, 읽기 어려움", "18pt 이상 대형 폰트 전면 적용", "100% 충족"),
        ("명도 대비 강화", "명도비 3:1 이하 회색 텍스트", "WCAG AAA 7:1 이상 고대비 준수", "100% 충족"),
        ("터치 영역 확장", "32dp 소형 아이콘, 오터치 유발", "최소 48dp & 56dp 풀와이드 버튼", "100% 충족"),
        ("대체 수단 제공", "비밀번호 분실 시 업무 중단", "가상계좌 즉시 발급 대체 경로", "100% 충족"),
        ("전환 편의성", "고령자 모드 진입 메뉴 숨겨짐", "상단 원터치 [일반/간편] 토글", "100% 충족"),
        ("심리적 불안 해소", "완료 피드백 부재, 전화 문의", "카카오 알림톡 실시간 연동", "100% 충족")
    ]
    
    row_y = th_y + 50
    for item, asis, tobe, status in audit_rows:
        draw.rectangle([rx + 30, row_y, rx + rw - 30, row_y + 58], fill=(255, 248, 250) if "100%" in status and audit_rows.index((item, asis, tobe, status))%2==0 else (255, 255, 255))
        draw.line([(rx + 30, row_y + 58), (rx + rw - 30, row_y + 58)], fill=BORDER_LIGHT, width=1)
        draw.text((rx + 50, row_y + 29), item, font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw.text((rx + 300, row_y + 29), asis, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB, anchor='lm')
        draw.text((rx + 570, row_y + 29), tobe, font=get_font(12, 'bold'), fill=(5, 150, 105), anchor='lm')
        draw_pill_badge(draw, cx=rx + 825, cy=row_y + 29, text=status, font=get_font(10.5, 'bold'), theme='green', pad_x=10, height=22)
        row_y += 60
        
    draw_slide_footer(draw, 3, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_03.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 04: INFORMATION ARCHITECTURE & USER FLOW (IA Tree)
# -------------------------------------------------------------
def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 4, 
        "INFORMATION ARCHITECTURE & USER FLOW", 
        "Information Architecture | ", 
        "제로-뎁스(Zero-Depth) 정보 구조도 및 사용자 여정", 
        "일반 모드와 고령자 모드의 상호 연동 체계 및 원터치 5대 핵심 비대면 과업 구조", 
        right_badge=("IA & USER FLOW", "red")
    )
    
    card_x, card_y, card_w, card_h = 100, 220, 1720, 730
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    # Root Node: AIA+ Single App Entry
    root_x, root_y, root_w, root_h = 760, 260, 400, 70
    draw.rounded_rectangle([root_x, root_y, root_x + root_w, root_y + root_h], radius=14, fill=AIA_RED, outline=AIA_RED_BORDER, width=2)
    draw.text((root_x + root_w//2, root_y + 24), "AIA+ 모바일 통합 플랫폼", font=get_font(16, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((root_x + root_w//2, root_y + 48), "단일 앱 내 이원화 모드 지원 (Single Codebase Multi-Theme)", font=get_font(11, 'medium'), fill=AIA_RED_LIGHT, anchor='mm')
    
    # Branch line down
    draw.line([(root_x + root_w//2, root_y + root_h), (root_x + root_w//2, 380)], fill=BORDER_LIGHT, width=2)
    draw.line([(380, 380), (1540, 380)], fill=BORDER_LIGHT, width=2)
    
    # Mode 1: General Mode Box (Left)
    g_x, g_y, g_w, g_h = 180, 410, 400, 80
    draw.rounded_rectangle([g_x, g_y, g_x + g_w, g_y + g_h], radius=12, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.line([(380, 380), (380, 410)], fill=BORDER_LIGHT, width=2)
    draw_pill_badge(draw, cx=g_x + g_w//2, cy=g_y + 24, text="DEFAULT MODE", font=get_font(10, 'bold'), theme='gray', pad_x=10, height=20)
    draw.text((g_x + g_w//2, g_y + 54), "일반 사용자 모드 (전 기능 종합 제공)", font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    # Mode 2: Senior Mode Box (Right - Highlighted)
    s_x, s_y, s_w, s_h = 940, 410, 800, 80
    draw.rounded_rectangle([s_x, s_y, s_x + s_w, s_y + s_h], radius=12, fill=(255, 241, 244), outline=AIA_RED, width=2)
    draw.line([(1340, 380), (1340, 410)], fill=AIA_RED, width=2)
    draw_pill_badge(draw, cx=s_x + s_w//2, cy=s_y + 24, text="SENIOR ACCESSIBLE MODE (PHASE 2 RENEWAL)", font=get_font(10.5, 'bold'), theme='red', pad_x=14, height=22)
    draw.text((s_x + s_w//2, s_y + 54), "고령자 친화 모드 (제로-뎁스 5대 핵심 비대면 과업 집중)", font=get_font(15, 'bold'), fill=AIA_RED, anchor='mm')
    
    # Connecting Switching Toggle Arrow between Modes
    draw_arrow(draw, (g_x + g_w, g_y + g_h//2), (s_x, s_y + s_h//2), col=AIA_RED, width=2, arrow_size=6)
    draw_arrow(draw, (s_x, s_y + s_h//2 + 15), (g_x + g_w, g_y + g_h//2 + 15), col=(100, 116, 139), width=2, arrow_size=6)
    draw_pill_badge(draw, cx=(g_x + g_w + s_x)//2, cy=g_y + g_h//2 + 8, text="상단 1-Tap 토글 스위치", font=get_font(10, 'bold'), theme='red', solid=True, pad_x=8, height=20)
    
    # 5 Sub-Nodes under Senior Mode
    draw.line([(1340, s_y + s_h), (1340, 540)], fill=AIA_RED, width=2)
    draw.line([(960, 540), (1720, 540)], fill=AIA_RED, width=2)
    
    senior_tasks = [
        ("01. 내 계약 조회", "보유 계약 목록\n납입 보험료 확인\n보장 내용 큰글씨 요약", (59, 130, 246)),
        ("02. 보험료 바로 내기", "당월 미납금 원터치\n주거래 계좌 자동 연동\n가상계좌 즉시 발급", AIA_RED),
        ("03. 간편 보험금 청구", "병원 영수증 카메라 촬영\nOCR 자동 텍스트 입력\n카카오 알림톡 실시간", (168, 85, 247)),
        ("04. 계약 대출 신청", "대출 가능 금액 한도 조회\n즉시 이체 지급 요청\n간편 비밀번호 인증", (16, 185, 129)),
        ("05. 안심 고객 상담", "전담 상담사 원클릭 연결\n가까운 고객센터 찾기\n자주 묻는 질문 음성지원", (71, 85, 105))
    ]
    
    tw = 145
    th = 200
    for idx, (ttitle, titems, tcol) in enumerate(senior_tasks):
        tx = 950 + idx * 158
        ty = 560
        draw.line([(tx + tw//2, 540), (tx + tw//2, ty)], fill=AIA_RED, width=2)
        draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=12, fill=(255, 255, 255), outline=tcol, width=2 if idx==1 else 1)
        draw.rounded_rectangle([tx + 8, ty + 12, tx + tw - 8, ty + 38], radius=6, fill=tcol)
        draw.text((tx + tw//2, ty + 25), ttitle, font=get_font(10.5, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        ilines = titems.split('\n')
        iy = ty + 55
        for line in ilines:
            draw.text((tx + 12, iy), "•", font=get_font(10, 'bold'), fill=tcol)
            draw.text((tx + 22, iy), line, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_MAIN)
            iy += 44
            
    # General Mode Branch Features
    draw.line([(380, g_y + g_h), (380, 560)], fill=BORDER_LIGHT, width=2)
    gw_box = 360
    draw.rounded_rectangle([200, 560, 200 + gw_box, 560 + th], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((200 + gw_box//2, 585), "일반 모드 종합 메뉴 트리", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    g_features = [
        "마이페이지 및 계약 종합 관리 (12개 뎁스)",
        "신규 다이렉트 보험 상품 비교 및 가입",
        "AIA Vitality 건강 리워드 & 만보기 연동",
        "자산관리 및 퇴직연금 펀드 포트폴리오",
        "보안센터 (인증서, OTP, 생체인증 관리)"
    ]
    gy = 620
    for gf in g_features:
        draw.text((220, gy), "•", font=get_font(11, 'bold'), fill=(100, 116, 139))
        draw.text((235, gy), gf, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
        gy += 25
        
    draw_slide_footer(draw, 4, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_04.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
