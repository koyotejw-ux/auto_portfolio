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
    
    card_y = 220
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
# SLIDE 03: COMPETITOR ANALYSIS (7 Major Insurers Benchmark Matrix)
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 3, 
        "COMPETITOR BENCHMARK ANALYSIS", 
        "Competitor Analysis | ", 
        "7대 생·손보사 고령자 모드 실물 벤치마크 및 메뉴 매핑 분석", 
        "업계 명칭, UI 차별성, 색상대비, UX라이팅 실태 비교 및 AIA+와 타사 간 7단계 메뉴 구조 분석", 
        right_badge=("COMPETITIVE AUDIT", "red")
    )
    
    card_x, card_y, card_w, card_h = 100, 220, 1720, 730
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    # ---------------------------------------------------------
    # PART 1: Top Benchmark Feature Matrix (Table 1)
    # ---------------------------------------------------------
    t1_y = card_y + 20
    draw_pill_badge(draw, left_x=card_x + 25, cy=t1_y + 16, text="TABLE 01. 7대 보험사 고령자 모드 지원 현황 비교", font=get_font(10.5, 'bold'), theme='red', pad_x=10, height=22)
    
    cols = ["비교 항목", "A 생명", "B 생명", "C 화재", "D 손해보험", "E 손해보험", "F 화재", "G 라이프", "AIA+ (TO-BE)"]
    col_w = [180, 160, 160, 160, 170, 170, 160, 160, 200]
    col_x = [card_x + 25]
    for w in col_w[:-1]:
        col_x.append(col_x[-1] + w)
        
    # Table Header Row
    th_y = t1_y + 35
    draw.rounded_rectangle([col_x[0], th_y, col_x[-1] + col_w[-1], th_y + 32], radius=6, fill=(30, 41, 59))
    for i, col in enumerate(cols):
        draw.text((col_x[i] + col_w[i]//2, th_y + 16), col, font=get_font(11, 'bold'), fill=(255, 255, 255) if i<8 else (255, 220, 230), anchor='mm')
        
    t1_rows = [
        ("고령자 모드 명칭", "간편홈", "간편모드", "큰글씨", "편한", "간편", "쉬운", "간편홈", "간편홈 (표준화)"),
        ("메인 전용 간편 구성", "O", "O", "O", "O", "O", "O", "O", "O (원터치 게이트)"),
        ("전용 레이아웃 분기", "O", "O", "O", "O", "O", "O", "O", "O (독립 화면 분기)"),
        ("전용 텍스트 크기 확대", "O", "△", "O", "O", "O", "O", "O", "O (18~28pt 2배)"),
        ("전용 터치 버튼 확대", "O", "O", "O", "O", "O", "O", "O", "O (56dp 풀와이드)"),
        ("전용 색상대비 (AAA)", "X", "X", "X", "X", "X", "X", "X", "O (WCAG 7:1 달성)"),
        ("전용 버튼 UX라이팅", "X", "X", "X", "X", "X", "X", "X", "O (쉬운 명확 용어)"),
        ("전용 아이콘 메뉴 레이블", "O", "X", "X", "X", "X", "X", "X", "O (아이콘+텍스트)")
    ]
    
    r_y = th_y + 34
    for r_idx, row in enumerate(t1_rows):
        is_highlight = "색상대비" in row[0] or "UX라이팅" in row[0]
        bg_col = (255, 241, 244) if is_highlight else ((255, 255, 255) if r_idx % 2 == 0 else (248, 250, 252))
        draw.rectangle([col_x[0], r_y, col_x[-1] + col_w[-1], r_y + 24], fill=bg_col)
        draw.line([(col_x[0], r_y + 24), (col_x[-1] + col_w[-1], r_y + 24)], fill=BORDER_LIGHT, width=1)
        
        for c_idx, val in enumerate(row):
            txt_col = TEXT_LIGHT_MAIN
            if val == "O" or "O (" in val:
                txt_col = (5, 150, 105)
            elif val == "X":
                txt_col = (220, 38, 38)
            elif val == "△":
                txt_col = (217, 119, 6)
            if c_idx == 8:
                txt_col = AIA_RED
            draw.text((col_x[c_idx] + col_w[c_idx]//2, r_y + 12), val, font=get_font(10.5, 'bold' if c_idx==8 or is_highlight else 'regular'), fill=txt_col, anchor='mm')
        r_y += 25
        
    # ---------------------------------------------------------
    # PART 2: Bottom Menu Architecture Comparison (Table 2)
    # ---------------------------------------------------------
    t2_y = r_y + 15
    draw_pill_badge(draw, left_x=card_x + 25, cy=t2_y + 14, text="TABLE 02. 금융사별 모바일 간편모드 메뉴 뎁스 및 매핑 실태 분석 (AS-IS vs Competitors)", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=22)
    
    t2_cols = ["AIA (AS-IS)", "A 생명", "B 화재", "C 생명", "D 손해보험", "E 손해보험", "F 화재", "G 라이프", "AIA+ (TO-BE)"]
    t2_col_w = [175, 175, 175, 175, 175, 175, 175, 175, 220]
    t2_col_x = [card_x + 25]
    for w in t2_col_w[:-1]:
        t2_col_x.append(t2_col_x[-1] + w)
        
    # Table 2 Header
    th2_y = t2_y + 32
    draw.rounded_rectangle([t2_col_x[0], th2_y, t2_col_x[-1] + t2_col_w[-1], th2_y + 28], radius=6, fill=(51, 65, 85))
    for i, col in enumerate(t2_cols):
        draw.text((t2_col_x[i] + t2_col_w[i]//2, th2_y + 14), col, font=get_font(10.5, 'bold'), fill=(255, 255, 255) if i<8 else (255, 220, 230), anchor='mm')
        
    menu_rows = [
        ("큰글씨 전환 (헤더)", "간편홈", "큰글씨 전환", "간편모드 전환", "편한 전환", "간편 전환", "쉬운 전환", "간편홈 전환", "상단 1-Tap 토글"),
        ("알림 (미납안내)", "챗봇", "전체메뉴", "알림", "자동차", "알림", "알림", "전체메뉴", "개인화 알림 3건"),
        ("로그인 / 공지사항", "알림", "로그인/내정보", "my (계약조회)", "운전자", "질병/상해 교통사고", "전체", "이벤트", "내보험 계약 스와이프"),
        ("보험금 청구 (필수)", "메뉴", "보험계약 조회", "보험금 청구", "해외여행", "계약조회", "보험상품 전체보기", "로그인", "보험금 청구 (OCR)"),
        ("계약 조회 (필수)", "내계약", "보험금 청구", "보험료 납입", "주택종합", "장기보험료 납입", "보험계약 확인", "보험계약조회", "보험료 바로 내기"),
        ("보험료 납입 (필수)", "보험금 청구", "보험료 납입", "연금/만기/보험금", "원데이 자동차", "보험료납입 내역조회", "자동차보험 계약변경", "보험료납입", "자동이체 / 가상계좌"),
        ("자동이체 / 대출", "보험료 납입", "보험계약 대출신청", "대출신청", "골프", "자동차 사고접수", "보험료 납입", "보험금청구", "계약대출 / 1:1 상담")
    ]
    
    r2_y = th2_y + 30
    for r_idx, row in enumerate(menu_rows):
        is_core = r_idx in [3, 4, 5]
        bg_col = (255, 241, 244) if is_core else ((255, 255, 255) if r_idx % 2 == 0 else (248, 250, 252))
        draw.rectangle([t2_col_x[0], r2_y, t2_col_x[-1] + t2_col_w[-1], r2_y + 24], fill=bg_col)
        draw.line([(t2_col_x[0], r2_y + 24), (t2_col_x[-1] + t2_col_w[-1], r2_y + 24)], fill=BORDER_LIGHT, width=1)
        
        for c_idx, val in enumerate(row):
            txt_col = TEXT_LIGHT_MAIN
            if is_core and c_idx in [0, 8]:
                txt_col = AIA_RED
            elif is_core:
                txt_col = (15, 23, 42)
            if c_idx == 8:
                txt_col = AIA_RED
            draw.text((t2_col_x[c_idx] + t2_col_w[c_idx]//2, r2_y + 12), val, font=get_font(10, 'bold' if c_idx==8 or is_core else 'regular'), fill=txt_col, anchor='mm')
        r2_y += 25
        
    # Legend & Summary Note
    sum_y = card_y + card_h - 60
    draw.rounded_rectangle([card_x + 25, sum_y, card_x + card_w - 25, sum_y + 45], radius=8, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((card_x + 40, sum_y + 22), "💡 벤치마크 핵심 시사점", font=get_font(11.5, 'bold'), fill=AIA_RED, anchor='lm')
    draw.text((card_x + 190, sum_y + 22), "기존 금융사는 색상대비(WCAG AAA) 및 전용 UX라이팅 미흡. AIA+는 타사 대비 '5대 핵심 업무 1-Tap 집중 + 고대비 전용 테마'로 독보적 사용성 확보.", font=get_font(11, 'regular'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
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
