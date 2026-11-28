import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 05: INFORMATION ARCHITECTURE (Native Vector Tree)
# -------------------------------------------------------------
def make_slide_05():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 5, 
        "INFORMATION ARCHITECTURE", 
        "Information Architecture | ", 
        "토지개발 플랫폼 인포메이션 아키텍처 (IA) 및 5대 핵심 모듈", 
        "홈 중심의 로그인/회원가입, 시뮬레이터(시작/통계), 사용자 통계, 마이페이지, 관리자(위젯/데이터) 계층 설계", 
        right_badge=("PLATFORM IA TREE", "green")
    )
    
    lw = 480
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="5-DOMAIN IA PRINCIPLES", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "5대 핵심 도메인 아키텍처", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    principles = [
        ("01. 회원 및 인증 체계", "일반 토지주, 소농, 전문 개발사, 투자사 유형별 맞춤 권한 부여 및 비밀번호 찾기, 서비스 정책 연결"),
        ("02. 코어 시뮬레이터 엔진", "시뮬레이션 시작(대상지-토지분석-시설배치-설계-매출)과 시뮬레이션 이력 및 통계 대시보드"),
        ("03. 사용자 통계 센터", "지역별 인기 토지 개발 유형, 최근 시뮬레이션 추이 및 평균 소요 비용/수익률 실시간 집계"),
        ("04. 마이페이지 & 결제 관리", "회원 프로필 설정, 저장된 시뮬레이션 프로젝트 관리 및 심층 타당성 보고서 결제/영수증 관리"),
        ("05. 엔터프라이즈 관리자 콘솔", "위젯 설정, 공공 API 데이터 싱크 관리, 토지 규제 조례 DB 업데이트 및 회원 관리")
    ]
    py = ly + 115
    for title, desc in principles:
        draw.rounded_rectangle([125, py, 100 + lw - 25, py + 105], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, py + 25), title, font=get_font(15, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12, 'regular'), lw - 70, draw)
        dy = py + 52
        for l in lines:
            draw.text((145, dy), l, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        py += 120

    rx = 605
    rw = 1215
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ly + 35, text="DIRECT VECTOR HIERARCHY TREE", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 265, ly + 35), "피그마 원본 정보 구조도 (Home 중심 4대 도메인 및 16대 서브 노드 완전 구현)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    root_x, root_y, root_w, root_h = rx + rw//2 - 90, ly + 80, 180, 52
    draw.rounded_rectangle([root_x, root_y, root_x + root_w, root_y + root_h], radius=26, fill=BRAND_GREEN)
    draw.text((root_x + root_w//2, root_y + root_h//2), "Home (홈 메인)", font=get_font(16, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    categories = [
        ("01. 회원가입/로그인", ["로그인", "회원가입", "비밀번호 찾기", "서비스 이용약관"]),
        ("02. 시뮬레이터 (Core)", ["시뮬레이션 시작", "시뮬레이션 통계", "진행 이력 관리", "보고서 뷰어"]),
        ("03. 사용자 통계 & 마이", ["지역별 개발 통계", "비용/수익률 집계", "내 프로젝트 보관", "결제 및 영수증"]),
        ("04. 관리자 콘솔", ["메인 위젯 관리", "공공 API 연동", "토지 규제 DB", "회원 권한 관리"])
    ]
    
    cat_w = 265
    cat_gap = 25
    cat_start_x = rx + (rw - (4 * cat_w + 3 * cat_gap)) // 2
    cat_y = ly + 200
    
    stem_y = ly + 160
    draw.line([(root_x + root_w//2, root_y + root_h), (root_x + root_w//2, stem_y)], fill=(148, 163, 184), width=2)
    draw.line([(cat_start_x + cat_w//2, stem_y), (cat_start_x + 3 * (cat_w + cat_gap) + cat_w//2, stem_y)], fill=(148, 163, 184), width=2)
    
    for idx, (cat_name, sub_items) in enumerate(categories):
        cx = cat_start_x + idx * (cat_w + cat_gap)
        draw.line([(cx + cat_w//2, stem_y), (cx + cat_w//2, cat_y)], fill=(148, 163, 184), width=2)
        
        cat_col = BRAND_DARK if idx==1 else (BRAND_TEAL if idx==2 else (51, 65, 85))
        draw.rounded_rectangle([cx, cat_y, cx + cat_w, cat_y + 48], radius=10, fill=cat_col)
        draw.text((cx + cat_w//2, cat_y + 24), cat_name, font=get_font(13.5, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        sub_stem_x = cx + cat_w//2
        sub_y_start = cat_y + 48
        draw.line([(sub_stem_x, sub_y_start), (sub_stem_x, sub_y_start + 420)], fill=(203, 213, 225), width=2)
        
        for s_idx, s_text in enumerate(sub_items):
            s_box_y = cat_y + 75 + s_idx * 95
            s_box_w = cat_w - 20
            s_box_h = 68
            s_box_x = cx + 10
            
            draw.line([(sub_stem_x, s_box_y + s_box_h//2), (s_box_x, s_box_y + s_box_h//2)], fill=(148, 163, 184), width=2)
            
            box_fill = (236, 253, 245) if idx==1 else (248, 250, 252)
            box_border = BRAND_GREEN if idx==1 else BORDER_LIGHT
            draw.rounded_rectangle([s_box_x, s_box_y, s_box_x + s_box_w, s_box_y + s_box_h], radius=8, fill=box_fill, outline=box_border, width=2 if idx==1 else 1)
            
            draw.rounded_rectangle([s_box_x + 12, s_box_y + 12, s_box_x + 36, s_box_y + 32], radius=4, fill=BRAND_GREEN if idx==1 else (100, 116, 139))
            draw.text((s_box_x + 24, s_box_y + 22), f"{s_idx+1}", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
            draw.text((s_box_x + 44, s_box_y + 22), s_text, font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
            
            sub_descs = {
                "로그인": "소셜/이메일 간편인증",
                "회원가입": "토지주/전문사 유형선택",
                "비밀번호 찾기": "SMS/이메일 본인인증",
                "서비스 이용약관": "개인정보/위치기반 동의",
                "시뮬레이션 시작": "지번검색 → 분석 → 배치",
                "시뮬레이션 통계": "프로젝트별 수치 대시보드",
                "진행 이력 관리": "임시저장 및 버전 비교",
                "보고서 뷰어": "웹 인터랙티브/PDF 출력",
                "지역별 개발 통계": "시군구별 개발 트렌드",
                "비용/수익률 집계": "평균 CAPEX/IRR 지표",
                "내 프로젝트 보관": "즐겨찾기 및 폴더링",
                "결제 및 영수증": "정기구독 / 건별 리포트",
                "메인 위젯 관리": "배너/추천토지 컴포넌트",
                "공공 API 연동": "토지이음/지적도 상태",
                "토지 규제 DB": "지자체별 조례 룰셋",
                "회원 권한 관리": "승인/차단/엔터프라이즈"
            }
            draw.text((s_box_x + 14, s_box_y + 48), sub_descs.get(s_text, ""), font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)

    draw_slide_footer(draw, 5, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_05.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 06: USER FLOW & DECISION LOGIC (Flawless Native Vector Flow Chart)
# -------------------------------------------------------------
# -------------------------------------------------------------
# SLIDE 06: RESPONSIVE WIREFRAME ARCHITECTURE (Native Vector Wireframes)
# -------------------------------------------------------------
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 6, 
        "RESPONSIVE WIREFRAME SYSTEM", 
        "Wireframe Architecture | ", 
        "반응형 랜딩페이지 및 코어 GIS 시뮬레이터 와이어프레임 설계", 
        "프로덕트 2대 핵심 경험: [1] 고객 유입용 패럴랙스 랜딩페이지  |  [2] B2B 듀얼 스플릿 GIS 시뮬레이터 워크스페이스 구조", 
        right_badge=("PREDICTIVE WIREFRAME", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # 2-Column High-Fidelity Vector Wireframe Architecture
    # Left Card (w=830, x=100): Responsive Landing Page Wireframe
    # Right Card (w=830, x=990): Enterprise GIS Simulator Workspace Wireframe
    
    # =========================================================================
    # COLUMN 1: RESPONSIVE LANDING PAGE WIREFRAME (w=830, x=100)
    # =========================================================================
    c1_x, c1_w = 100, 830
    draw.rounded_rectangle([c1_x, card_y, c1_x + c1_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c1_x + 25, cy=card_y + 35, text="WIREFRAME 01 · LANDING PAGE", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((c1_x + 25, card_y + 68), "반응형 랜딩페이지 와이어프레임", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c1_x + 25, card_y + 92), "가치 제안 ➔ 3단계 핵심 기능 체험 ➔ 고객 전환(CTA) 최적화 구조", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    # Mockup Viewport Container
    vp1_x = c1_x + 25
    vp1_y = card_y + 120
    vp1_w = c1_w - 50
    vp1_h = card_h - 145
    draw.rounded_rectangle([vp1_x, vp1_y, vp1_x + vp1_w, vp1_y + vp1_h], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    
    # Wireframe GNB Bar
    gnb_h = 42
    draw.rounded_rectangle([vp1_x, vp1_y, vp1_x + vp1_w, vp1_y + gnb_h], radius=12, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    draw.rectangle([vp1_x + 20, vp1_y + 14, vp1_x + 100, vp1_y + 28], fill=BRAND_GREEN)
    draw.text((vp1_x + 24, vp1_y + 15), "FARMINGSYS", font=get_font(10, 'bold'), fill=(255, 255, 255))
    
    menu_items = ["서비스 소개", "시뮬레이터", "사용자 통계", "요금 안내"]
    mx_cur = vp1_x + 130
    for m in menu_items:
        draw.text((mx_cur, vp1_y + 21), m, font=get_font(10.5, 'medium'), fill=TEXT_LIGHT_SUB, anchor='lm')
        mx_cur += 85
        
    draw.rounded_rectangle([vp1_x + vp1_w - 110, vp1_y + 10, vp1_x + vp1_w - 20, vp1_y + 32], radius=6, fill=BRAND_GREEN)
    draw.text((vp1_x + vp1_w - 65, vp1_y + 21), "무료 시작하기", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Wireframe Hero Block (y = vp1_y + 48)
    h_y = vp1_y + 50
    h_h = 195
    draw.rounded_rectangle([vp1_x + 12, h_y, vp1_x + vp1_w - 12, h_y + h_h], radius=10, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    
    # Hero Texts
    draw.text((vp1_x + 30, h_y + 30), "고객의 토지개발 사업에 동행하다", font=get_font(21, 'bold'), fill=BRAND_DARK)
    draw.text((vp1_x + 30, h_y + 60), "12대 공공 GIS 데이터와 스마트팜 시뮬레이션으로", font=get_font(12, 'medium'), fill=TEXT_LIGHT_SUB)
    draw.text((vp1_x + 30, h_y + 78), "복잡한 인허가 및 공사비를 3초 만에 원스톱 자동 분석", font=get_font(12, 'medium'), fill=TEXT_LIGHT_SUB)
    
    # Hero CTA Button
    draw.rounded_rectangle([vp1_x + 30, h_y + 115, vp1_x + 190, h_y + 155], radius=8, fill=BRAND_GREEN)
    draw.text((vp1_x + 110, h_y + 135), "시뮬레이터 시작하기 →", font=get_font(11.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Hero Right Interactive Search Wireframe Box
    s_box_x = vp1_x + vp1_w - 320
    s_box_y = h_y + 20
    draw.rounded_rectangle([s_box_x, s_box_y, s_box_x + 300, s_box_y + 155], radius=8, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    draw.text((s_box_x + 16, s_box_y + 18), "📍 지번 또는 도로명 검색", font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.rounded_rectangle([s_box_x + 16, s_box_y + 40, s_box_x + 284, s_box_y + 72], radius=6, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((s_box_x + 26, s_box_y + 56), "예: 서울시 마포구 신수동 250-27", font=get_font(10, 'regular'), fill=(148, 163, 184), anchor='lm')
    draw.rounded_rectangle([s_box_x + 16, s_box_y + 85, s_box_x + 284, s_box_y + 140], radius=6, fill=(236, 253, 245))
    draw.text((s_box_x + 26, s_box_y + 102), "✓ 12개 공공 인허가 조례 즉시 매칭", font=get_font(10, 'bold'), fill=BRAND_DARK)
    draw.text((s_box_x + 26, s_box_y + 122), "✓ 예상 조성비 및 수확량 시뮬레이션", font=get_font(10, 'bold'), fill=BRAND_GREEN)
    
    # Wireframe 3 Features Grid (y = h_y + h_h + 16)
    f_y = h_y + h_h + 16
    f_w = (vp1_w - 48) // 3
    features = [
        ("01. 토지분석", "지적도·지목·용도지역 100여 개 규제 자동 판정", BRAND_GREEN),
        ("02. 시설배치", "온실·APC물류센터 경계선 내 최적 구획", BRAND_TEAL),
        ("03. 금융보고서", "236억 공사비 산출 및 대출 심사용 20p PDF", (30, 58, 138))
    ]
    for i, (f_title, f_desc, f_col) in enumerate(features):
        fx = vp1_x + 12 + i * (f_w + 12)
        draw.rounded_rectangle([fx, f_y, fx + f_w, f_y + 130], radius=10, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([fx + 16, f_y + 16, fx + 44, f_y + 44], radius=6, fill=f_col)
        draw.text((fx + 30, f_y + 30), f"{i+1}", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((fx + 52, f_y + 30), f_title, font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        lines = wrap_text(f_desc, get_font(11, 'regular'), f_w - 32, draw)
        ly = f_y + 58
        for l in lines:
            draw.text((fx + 16, ly), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 18
            
    # Bottom Callout in Col 1
    b_y = f_y + 144
    draw.rounded_rectangle([vp1_x + 12, b_y, vp1_x + vp1_w - 12, vp1_y + vp1_h - 12], radius=10, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((vp1_x + 28, b_y + 18), "💡 랜딩페이지 UX 전략: 진입 장벽 제거와 즉각적 데이터 가치 증명", font=get_font(11.5, 'bold'), fill=BRAND_DARK)
    draw.text((vp1_x + 28, b_y + 38), "비전문가 토지 소유주가 첫 화면에서 지번만 입력해도 자신의 토지 가치와 규제 적합도를 3초 만에 체감하게 유도", font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)

    # =========================================================================
    # COLUMN 2: ENTERPRISE GIS SIMULATOR WORKSPACE WIREFRAME (w=830, x=990)
    # =========================================================================
    c2_x, c2_w = 990, 830
    draw.rounded_rectangle([c2_x, card_y, c2_x + c2_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c2_x + 25, cy=card_y + 35, text="WIREFRAME 02 · SIMULATOR SAAS", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((c2_x + 25, card_y + 68), "코어 GIS 시뮬레이터 와이어프레임", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c2_x + 25, card_y + 92), "좌측 380px 컨트롤 패널 + 우측 인터랙티브 GIS 캔버스의 듀얼 스플릿 뷰", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    # Mockup Viewport Container
    vp2_x = c2_x + 25
    vp2_y = card_y + 120
    vp2_w = c2_w - 50
    vp2_h = card_h - 145
    draw.rounded_rectangle([vp2_x, vp2_y, vp2_x + vp2_w, vp2_y + vp2_h], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    
    # SaaS Stepper Header (y = vp2_y)
    draw.rounded_rectangle([vp2_x, vp2_y, vp2_x + vp2_w, vp2_y + gnb_h], radius=12, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    draw.text((vp2_x + 20, vp2_y + 21), "STEP 2. 토지분석", font=get_font(12, 'bold'), fill=BRAND_DARK, anchor='lm')
    draw_pill_badge(draw, left_x=vp2_x + 130, cy=vp2_y + 21, text="STEP 선택", font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
    
    # Stepper Indicators on Right of Header
    steps = ["1.대상지선택", "2.토지분석", "3.시설배치", "4.조성비/매출"]
    sx_cur = vp2_x + 250
    for s_idx, st in enumerate(steps):
        is_active = (s_idx == 1)
        col = BRAND_GREEN if is_active else (148, 163, 184)
        draw.text((sx_cur, vp2_y + 21), st, font=get_font(10.5, 'bold' if is_active else 'regular'), fill=col, anchor='lm')
        sx_cur += 110
        if s_idx < 3:
            draw.text((sx_cur - 25, vp2_y + 21), "➔", font=get_font(9, 'regular'), fill=(203, 213, 225), anchor='lm')

    draw.rounded_rectangle([vp2_x + vp2_w - 95, vp2_y + 10, vp2_x + vp2_w - 20, vp2_y + 32], radius=6, fill=(15, 23, 42))
    draw.text((vp2_x + vp2_w - 57, vp2_y + 21), "새로시작", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Dual Split Workspace Layout: Left Panel (w=300) + Right Map (w=460)
    split_y = vp2_y + gnb_h + 10
    split_h = vp2_h - gnb_h - 20
    
    # Left Control Panel Wireframe (w=310)
    lp_w = 310
    draw.rounded_rectangle([vp2_x + 10, split_y, vp2_x + 10 + lp_w, split_y + split_h], radius=8, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    
    # 4 Analysis Tabs
    tabs = ["기본정보", "자연환경", "토지건물", "도시계획"]
    tw = lp_w // 4
    for t_idx, t_name in enumerate(tabs):
        tx = vp2_x + 10 + t_idx * tw
        is_t_active = (t_idx == 0)
        draw.text((tx + tw//2, split_y + 18), t_name, font=get_font(10.5, 'bold' if is_t_active else 'regular'), fill=BRAND_GREEN if is_t_active else TEXT_LIGHT_SUB, anchor='mm')
        if is_t_active:
            draw.rectangle([tx + 4, split_y + 30, tx + tw - 4, split_y + 32], fill=BRAND_GREEN)
            
    # Chips Row
    chips = ["지목현황", "소유현황", "공시지가"]
    cx_cur = vp2_x + 22
    for c_idx, ch in enumerate(chips):
        draw_pill_badge(draw, left_x=cx_cur, cy=split_y + 52, text=ch, font=get_font(9.5, 'bold'), theme='green' if c_idx==0 else 'gray', pad_x=8, height=20)
        cx_cur += 75
        
    # Table Wireframe Rows
    draw.rounded_rectangle([vp2_x + 20, split_y + 75, vp2_x + 10 + lp_w - 10, split_y + 175], radius=6, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((vp2_x + 30, split_y + 92), "구분: 대 (171.9㎡ / 82.5%)", font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((vp2_x + 30, split_y + 114), "소유: 개인 (100% 단독 소유)", font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)
    draw.text((vp2_x + 30, split_y + 134), "공시지가: 4,857,000원/㎡", font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)
    draw.text((vp2_x + 30, split_y + 154), "용도지역: 제2종일반주거지역", font=get_font(10.5, 'regular'), fill=BRAND_GREEN)
    
    # Secondary Box (제외면적 필터)
    draw.rounded_rectangle([vp2_x + 20, split_y + 190, vp2_x + 10 + lp_w - 10, split_y + 280], radius=6, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
    draw.text((vp2_x + 30, split_y + 208), "⚠️ 인허가 제외면적 필터링", font=get_font(11, 'bold'), fill=(225, 29, 72))
    draw.text((vp2_x + 30, split_y + 230), "• 건축 한계선 이격거리: 0㎡", font=get_font(10, 'regular'), fill=TEXT_LIGHT_SUB)
    draw.text((vp2_x + 30, split_y + 248), "• 실제 개발 가용면적: 750㎡ (100%)", font=get_font(10, 'bold'), fill=BRAND_DARK)
    
    # Left Bottom Actions
    draw.rounded_rectangle([vp2_x + 20, split_y + split_h - 45, vp2_x + 110, split_y + split_h - 15], radius=6, fill=(241, 245, 249))
    draw.text((vp2_x + 65, split_y + split_h - 30), "이전", font=get_font(11, 'bold'), fill=TEXT_LIGHT_SUB, anchor='mm')
    draw.rounded_rectangle([vp2_x + 120, split_y + split_h - 45, vp2_x + 10 + lp_w - 10, split_y + split_h - 15], radius=6, fill=BRAND_GREEN)
    draw.text((vp2_x + 205, split_y + split_h - 30), "다음 단계 (시설배치) ➔", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Right GIS Canvas Wireframe (w=440)
    rp_x = vp2_x + 10 + lp_w + 10
    rp_w = vp2_w - lp_w - 30
    draw.rounded_rectangle([rp_x, split_y, rp_x + rp_w, split_y + split_h], radius=8, fill=(226, 232, 240), outline=BORDER_LIGHT, width=1)
    
    # Map Layer Buttons
    draw.rounded_rectangle([rp_x + rp_w - 130, split_y + 12, rp_x + rp_w - 12, split_y + 40], radius=6, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    draw.text((rp_x + rp_w - 71, split_y + 26), "지적도 | 일반 | 위성", font=get_font(9.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    # Map Polygon Outline Vector Simulation
    poly = [(rp_x + 100, split_y + 80), (rp_x + 280, split_y + 60), (rp_x + 340, split_y + 200), (rp_x + 260, split_y + 280), (rp_x + 80, split_y + 220)]
    draw.polygon(poly, fill=(209, 250, 229), outline=BRAND_GREEN)
    draw.text((rp_x + 210, split_y + 160), "대상지 750㎡", font=get_font(13, 'bold'), fill=BRAND_DARK, anchor='mm')
    draw.text((rp_x + 210, split_y + 182), "가용률 100%", font=get_font(10.5, 'bold'), fill=BRAND_GREEN, anchor='mm')
    
    # Map Floating Zoom Controls
    draw.rounded_rectangle([rp_x + rp_w - 40, split_y + split_h - 85, rp_x + rp_w - 12, split_y + split_h - 15], radius=6, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    draw.text((rp_x + rp_w - 26, split_y + split_h - 68), "+", font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.line([(rp_x + rp_w - 35, split_y + split_h - 50), (rp_x + rp_w - 17, split_y + split_h - 50)], fill=BORDER_LIGHT, width=1)
    draw.text((rp_x + rp_w - 26, split_y + split_h - 32), "-", font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')

    draw_slide_footer(draw, 6, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_06.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 7, 
        "CORE FEATURE · STEP 1", 
        "Simulation Step 1 | ", 
        "STEP 1. 대상지 분석 및 토지 분석 보고서 데스크톱 & 모바일 화면 (Figma UI 실물)", 
        "피그마 공식 UI 원본: [1] 데스크톱 토지 분석 보고서(위치·면적·토지분석종합·가용선별)  |  [2] 모바일 원클릭 토지 분석 보고서 뷰어", 
        right_badge=("OFFICIAL FIGMA REPORT UI", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # 3-Zone Layout:
    # Zone 1 (Left Card, w=440, x=80): Core Specs & Land Analysis Decision Logic
    # Zone 2 (Middle Card, w=840, x=540): Desktop Land Analysis Report Mockup (821x1024)
    # Zone 3 (Right Card, w=440, x=1400): Mobile Land Analysis Report Mockup (216x1024)
    
    # =========================================================================
    # ZONE 1: LEFT SPECS CARD (w=440, x=80)
    # =========================================================================
    lx, lw = 80, 440
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="STEP 1 · LAND ANALYSIS REPORT", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 68), "토지 분석 보고서 UI 로직", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 25, card_y + 92), "지번 입력 즉시 고정밀 공적 장부 & 가용부지 실시간 판정", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
    
    step1_specs = [
        ("01. 위치 및 면적 고해상도 지적도", "경기도 고양시 덕양구 대상지 위성/지적도 오버레이를 통해 총 면적(750㎡) 및 경계선을 직관적으로 시각화"),
        ("02. 6대 토지 분석 종합 테이블", "기본정보, 토지정보, 토지이용, 건축물정보, 자연환경분석(경사도·표고), 도시계획분석(제2종일반주거지역)을 원페이지로 집약"),
        ("03. 가용 vs 비가용 대상지 선별", "개발 인허가 불가 구역을 제외한 순수 사용 가능 대상지(750㎡)를 정밀 필터링하여 초기 매입 및 사업 착수 리스크 100% 차단")
    ]
    
    sy = card_y + 118
    for s_title, s_desc in step1_specs:
        draw.rounded_rectangle([lx + 25, sy, lx + lw - 25, sy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, sy + 22), s_title, font=get_font(13.5, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(s_desc, get_font(11, 'regular'), lw - 70, draw)
        dy = sy + 46
        for l in lines:
            draw.text((lx + 40, dy), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        sy += 144

    # Bottom Key Metric Callout in Left Card
    draw.rounded_rectangle([lx + 25, card_y + 565, lx + lw - 25, card_y + 715], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((lx + 40, card_y + 586), "💡 공공 데이터 집약 설계 가치", font=get_font(12.5, 'bold'), fill=BRAND_DARK)
    val_desc = "수십 장의 토지대장, 건축물대장, 토지이용계획확인원을 열람할 필요 없이, 플랫폼 자체 AI 분석 엔진이 단 3초 만에 표준 '토지 분석 보고서'로 자동 정제하여 의사결정 속도를 획기적으로 개선합니다."
    lines_val = wrap_text(val_desc, get_font(10.5, 'regular'), lw - 70, draw)
    vy = card_y + 610
    for l in lines_val:
        draw.text((lx + 40, vy), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_MAIN)
        vy += 17

    # =========================================================================
    # ZONE 2: DESKTOP LAND ANALYSIS REPORT MOCKUP (w=840, x=540)
    # =========================================================================
    mx, mw = 540, 840
    draw.rounded_rectangle([mx, card_y, mx + mw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=mx + 25, cy=card_y + 35, text="DESKTOP REPORT VIEW", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((mx + 215, card_y + 35), "피그마 공식 데스크톱 화면 (토지 분석 보고서 실물)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    desk_asset = os.path.join(ASSETS_DIR, "figma_step2_land_analysis_report_desktop.jpg")
    desk_im = Image.open(desk_asset)
    
    # Calculate zero-distortion dimensions for desktop report mockup
    target_d_h = 640
    d_vp_h = target_d_h - 36 - 2
    d_vp_w = int(d_vp_h * (desk_im.width / desk_im.height))
    tot_d_w = d_vp_w + 4
    
    d_cx = mx + mw // 2
    d_x = d_cx - tot_d_w // 2
    d_y = card_y + 75 + (card_h - 95 - target_d_h) // 2
    
    draw_browser_mockup(img, desk_asset, x=d_x, y=d_y, w=tot_d_w, h=target_d_h, title="LAND ANALYSIS REPORT (DESKTOP)", url="https://farmingsys.io/report/land-analysis-summary")

    # =========================================================================
    # ZONE 3: MOBILE LAND ANALYSIS REPORT MOCKUP (w=440, x=1400)
    # =========================================================================
    rx, rw = 1400, 440
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=card_y + 35, text="MOBILE REPORT VIEW", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 205, card_y + 35), "토지 분석 보고서 모바일 UI", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    mob_asset = os.path.join(ASSETS_DIR, "figma_step2_land_analysis_report_mobile.jpg")
    draw_phone_mockup(img, mob_asset, cx=rx + rw//2, cy=card_y + 75 + (card_h - 95)//2, target_h=640, bezel=7, radius=28)

    draw_slide_footer(draw, 7, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_07.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 08: DESIGN SYSTEM (Figma Typography Scale + Tokens Matrix 1:1 Matching)
# -------------------------------------------------------------
# -------------------------------------------------------------
# SLIDE 08: DESIGN SYSTEM (Figma Typography Scale + Tokens Matrix 1:1 Matching)
# -------------------------------------------------------------
def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 8, 
        "DESIGN SYSTEM · ATOMIC TOKENS", 
        "Design System | ", 
        "피그마 공식 디자인 시스템: 타이포그래피 계층 및 아토믹 토큰 매트릭스", 
        "Figma 토큰 1:1 규격화: Pretendard 6대 핵심 텍스트 스케일, 10색 아토믹 컬러 팔레트, 16종 대표 벡터 아이콘, 8-pt 그리드 시스템", 
        right_badge=("OFFICIAL FIGMA DESIGN SYSTEM", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # 3-Column Clean Spacious Architecture:
    # Col 1: Typography System (w=520, x=100) - 6 Essential Hierarchy Levels (Headline down to Caption)
    # Col 2: Color Palette & Core Iconography (w=600, x=640) - 10 Essential Swatches + 16 Primary Icons
    # Col 3: Spacing, Radius & Interactive Component States (w=560, x=1260) - 8-pt Grid & Component States
    
    # =========================================================================
    # COLUMN 1: TYPOGRAPHY SYSTEM (w=520, x=100)
    # =========================================================================
    c1_x, c1_w = 100, 520
    draw.rounded_rectangle([c1_x, card_y, c1_x + c1_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c1_x + 25, cy=card_y + 35, text="TYPOGRAPHY SYSTEM", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((c1_x + 25, card_y + 68), "Pretendard 타이포그래피 스케일", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c1_x + 25, card_y + 92), "피그마 원본 6대 핵심 텍스트 위계 (Bold / Medium / Regular)", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    # 6 Curated High-Impact Typography Levels with ample vertical padding (no crowding!)
    typo_specs = [
        ("Headline 48", "48px / Bold", "Pretendard Bold", "메인 대시보드 타이틀 및 핵심 통계 지표 대형 숫자", 20, BRAND_GREEN),
        ("Headline 32", "32px / Bold", "Pretendard Bold", "카드 섹션 타이틀 및 시뮬레이션 단계별 명칭", 17, BRAND_DARK),
        ("Subhead 20", "20px / Bold", "Pretendard Bold", "테이블 헤더, 탭 메뉴 및 위젯 그룹 타이틀", 14.5, TEXT_LIGHT_MAIN),
        ("Body 16", "16px / Medium", "Pretendard Medium", "기본 입력 폼 필드, 셀렉트박스 및 메인 리스트 텍스트", 13, TEXT_LIGHT_MAIN),
        ("Body 14", "14px / Regular", "Pretendard Regular", "테이블 데이터 행, 세부 규제 설명 및 조례 가이드", 12, TEXT_LIGHT_SUB),
        ("Caption 12", "12px / Regular", "Pretendard Regular", "배지 라벨, 메타데이터 타임스탬프 및 툴팁 출처 표기", 11, (148, 163, 184))
    ]
    
    ty_start = card_y + 124
    row_h = 96
    for i, (t_name, t_size, t_family, t_usage, font_sz, bar_col) in enumerate(typo_specs):
        r_y = ty_start + i * row_h
        bg_col = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rounded_rectangle([c1_x + 20, r_y, c1_x + c1_w - 20, r_y + 86], radius=10, fill=bg_col, outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([c1_x + 28, r_y + 14, c1_x + 32, r_y + 72], radius=2, fill=bar_col)
        draw.text((c1_x + 42, r_y + 16), t_name, font=get_font(font_sz, 'bold' if 'Bold' in t_family else 'medium'), fill=TEXT_LIGHT_MAIN)
        draw_pill_badge(draw, left_x=c1_x + c1_w - 130, cy=r_y + 24, text=t_size, font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
        draw.text((c1_x + 42, r_y + 44), f"Font: {t_family}", font=get_font(10.5, 'medium'), fill=BRAND_TEAL)
        draw.text((c1_x + 42, r_y + 62), t_usage, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)

    # =========================================================================
    # COLUMN 2: COLOR PALETTE & CORE ICONOGRAPHY (w=600, x=640)
    # =========================================================================
    c2_x, c2_w = 640, 600
    draw.rounded_rectangle([c2_x, card_y, c2_x + c2_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c2_x + 25, cy=card_y + 35, text="COLOR & ICONOGRAPHY TOKENS", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((c2_x + 25, card_y + 68), "컬러 팔레트 및 24px 벡터 아이콘", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c2_x + 25, card_y + 92), "Agri-Tech 브랜드 아이덴티티 및 직관적 시각 언어 규격", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    color_tokens = [
        {"name": "Primary-500", "code": "#16C666", "rgb": (22, 198, 102)},
        {"name": "Primary-300", "code": "#38E085", "rgb": (56, 224, 133)},
        {"name": "Secondary", "code": "#14B8A6", "rgb": (20, 184, 166)},
        {"name": "Neutral-900", "code": "#1E293B", "rgb": (30, 41, 59)},
        {"name": "Neutral-700", "code": "#334155", "rgb": (51, 65, 85)},
        {"name": "Neutral-400", "code": "#94A3B8", "rgb": (148, 163, 184)},
        {"name": "Neutral-100", "code": "#F1F5F9", "rgb": (241, 245, 249)},
        {"name": "White", "code": "#FFFFFF", "rgb": (255, 255, 255)},
        {"name": "Error-500", "code": "#EF4444", "rgb": (239, 68, 68)},
        {"name": "Warning-500", "code": "#F59E0B", "rgb": (245, 158, 11)}
    ]
    
    pal_y = card_y + 124
    sw_w = 104
    sw_h = 92
    gap_x = 10
    gap_y = 12
    
    for idx, c in enumerate(color_tokens):
        row = idx // 5
        col = idx % 5
        bx = c2_x + 20 + col * (sw_w + gap_x)
        by = pal_y + row * (sw_h + gap_y)
        draw.rounded_rectangle([bx, by, bx + sw_w, by + sw_h], radius=10, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        c_outline = (203, 213, 225) if c["name"] == "White" else None
        draw.rounded_rectangle([bx + 8, by + 8, bx + sw_w - 8, by + 42], radius=6, fill=c["rgb"], outline=c_outline, width=1)
        draw.text((bx + 8, by + 50), c["name"], font=get_font(10.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((bx + 8, by + 68), c["code"], font=get_font(9.5, 'medium'), fill=TEXT_LIGHT_SUB)
        
    mid_div_y = pal_y + 2 * (sw_h + gap_y) + 24
    draw.line([(c2_x + 20, mid_div_y), (c2_x + c2_w - 20, mid_div_y)], fill=BORDER_LIGHT, width=1)
    
    icon_hdr_y = mid_div_y + 20
    draw_pill_badge(draw, left_x=c2_x + 20, cy=icon_hdr_y + 10, text="FIGMA 24px VECTOR ICONS", font=get_font(10, 'bold'), theme='gray', pad_x=10, height=20)
    draw.text((c2_x + 205, icon_hdr_y + 10), "16종 핵심 시스템 벡터 심볼 (지도 탐색·분석·필터·제어)", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    icon_list = [
        "새로고침", "필터정렬", "토지경계", "레이어", "지적도", "위성스카이", "데이터분석", "보고서출력",
        "보안인증", "검색조회", "승인체크", "경고안내", "위치마커", "시간기록", "확대줌인", "축소줌아웃"
    ]
    
    ic_start_y = icon_hdr_y + 36
    ic_box_w = 64
    ic_box_h = 76
    ic_gap_x = 7
    ic_gap_y = 12
    
    for idx, ic_name in enumerate(icon_list):
        i_row = idx // 8
        i_col = idx % 8
        ix = c2_x + 20 + i_col * (ic_box_w + ic_gap_x)
        iy = ic_start_y + i_row * (ic_box_h + ic_gap_y)
        draw.rounded_rectangle([ix, iy, ix + ic_box_w, iy + ic_box_h], radius=8, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        sym_col = BRAND_GREEN if idx in [0, 2, 4, 7, 10] else (BRAND_TEAL if idx in [3, 6, 12] else (100, 116, 139))
        draw.ellipse([ix + ic_box_w//2 - 12, iy + 14, ix + ic_box_w//2 + 12, iy + 38], fill=(255, 255, 255), outline=sym_col, width=1)
        draw.ellipse([ix + ic_box_w//2 - 3, iy + 23, ix + ic_box_w//2 + 3, iy + 29], fill=sym_col)
        draw.text((ix + ic_box_w//2, iy + 54), ic_name, font=get_font(10, 'medium'), fill=TEXT_LIGHT_MAIN, anchor='mm')

    # =========================================================================
    # COLUMN 3: SPACING, RADIUS & COMPONENT STATES (w=560, x=1260)
    # =========================================================================
    c3_x, c3_w = 1260, 560
    draw.rounded_rectangle([c3_x, card_y, c3_x + c3_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c3_x + 25, cy=card_y + 35, text="ATOMIC METRICS & COMPONENTS", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((c3_x + 25, card_y + 68), "규격 단위 및 컴포넌트 토큰", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c3_x + 25, card_y + 92), "8-pt 그리드 Spacing, Radius 및 인터랙티브 상태 규격", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    t_y = card_y + 124
    sp_x, sp_w = c3_x + 20, 245
    draw.rounded_rectangle([sp_x, t_y, sp_x + sp_w, t_y + 270], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=sp_x + 14, cy=t_y + 20, text="SPACING SCALE (8-PT)", font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
    
    spacings = [
        ("Spacing / 4", "4px", "초밀착 인라인 여백"),
        ("Spacing / 8", "8px", "컴포넌트 내부 패딩 (S)"),
        ("Spacing / 16", "16px", "기본 카드/모듈 패딩 (M)"),
        ("Spacing / 24", "24px", "카드 간격 / 컴포넌트 갭"),
        ("Spacing / 32", "32px", "섹션 그룹 간격 (L)"),
        ("Spacing / 48", "48px", "대형 모듈 외부 여백 (XL)")
    ]
    sy_cur = t_y + 42
    for s_label, s_val, s_desc in spacings:
        draw.text((sp_x + 14, sy_cur + 6), s_label, font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw_pill_badge(draw, left_x=sp_x + sp_w - 55, cy=sy_cur + 11, text=s_val, font=get_font(9.5, 'bold'), theme='blue', pad_x=6, height=16)
        draw.text((sp_x + 14, sy_cur + 21), s_desc, font=get_font(9.5, 'regular'), fill=TEXT_LIGHT_SUB)
        draw.line([(sp_x + 14, sy_cur + 34), (sp_x + sp_w - 14, sy_cur + 34)], fill=(226, 232, 240), width=1)
        sy_cur += 36
        
    rad_x, rad_w = c3_x + 285, 255
    draw.rounded_rectangle([rad_x, t_y, rad_x + rad_w, t_y + 270], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rad_x + 14, cy=t_y + 20, text="RADIUS & STROKE TOKENS", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    
    geom_tokens = [
        ("Radius / Small", "4px", "태그/체크박스/뱃지"),
        ("Radius / Medium", "8px", "버튼/인풋/셀렉트박스"),
        ("Radius / Large", "16px", "카드 컨테이너/모달"),
        ("Radius / Circle", "999px", "원형 아바타/알약형"),
        ("Stroke / Default", "1.0px", "기본 카드 테두리"),
        ("Stroke / Strong", "2.0px", "포커스/활성 테두리")
    ]
    gy_cur = t_y + 42
    for g_label, g_val, g_desc in geom_tokens:
        draw.text((rad_x + 14, gy_cur + 6), g_label, font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw_pill_badge(draw, left_x=rad_x + rad_w - 60, cy=gy_cur + 11, text=g_val, font=get_font(9.5, 'bold'), theme='green', pad_x=6, height=16)
        draw.text((rad_x + 14, gy_cur + 21), g_desc, font=get_font(9.5, 'regular'), fill=TEXT_LIGHT_SUB)
        draw.line([(rad_x + 14, gy_cur + 34), (rad_x + rad_w - 14, gy_cur + 34)], fill=(226, 232, 240), width=1)
        gy_cur += 36

    comp_y = t_y + 295
    comp_h = card_y + card_h - comp_y - 20
    draw.rounded_rectangle([c3_x + 20, comp_y, c3_x + c3_w - 20, comp_y + comp_h], radius=14, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c3_x + 35, cy=comp_y + 24, text="UI COMPONENT STATES SPEC", font=get_font(10, 'bold'), theme='green', pad_x=10, height=20)
    draw.text((c3_x + 225, comp_y + 24), "실제 앱 화면 적용 인터랙티브 상태 규격", font=get_font(12, 'bold'), fill=BRAND_DARK, anchor='lm')
    
    ex1_y = comp_y + 54
    draw.text((c3_x + 35, ex1_y + 14), "버튼 상태", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.rounded_rectangle([c3_x + 120, ex1_y, c3_x + 235, ex1_y + 32], radius=8, fill=BRAND_GREEN)
    draw.text((c3_x + 177, ex1_y + 16), "분석 시작 (Default)", font=get_font(10.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.rounded_rectangle([c3_x + 250, ex1_y, c3_x + 365, ex1_y + 32], radius=8, fill=BRAND_DARK)
    draw.text((c3_x + 307, ex1_y + 16), "분석 시작 (Hover)", font=get_font(10.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.rounded_rectangle([c3_x + 380, ex1_y, c3_x + 495, ex1_y + 32], radius=8, fill=(226, 232, 240))
    draw.text((c3_x + 437, ex1_y + 16), "선택 대기 (Disabled)", font=get_font(10.5, 'bold'), fill=(148, 163, 184), anchor='mm')

    ex2_y = ex1_y + 54
    draw.text((c3_x + 35, ex2_y + 14), "인허가 뱃지", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw_pill_badge(draw, left_x=c3_x + 120, cy=ex2_y + 16, text="적합 · 개발가능", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=28)
    draw_pill_badge(draw, left_x=c3_x + 250, cy=ex2_y + 16, text="조건부 · 심의필요", font=get_font(10.5, 'bold'), theme='yellow', pad_x=12, height=28)
    draw_pill_badge(draw, left_x=c3_x + 380, cy=ex2_y + 16, text="불가 · 보전관리지역", font=get_font(10.5, 'bold'), theme='red', pad_x=12, height=28)

    draw_slide_footer(draw, 8, 13, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_08.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
