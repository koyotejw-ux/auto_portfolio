import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 07: WIREFRAME & GIS INTERACTION (Figma Step 1 Cadastral Map Screen Focus)
# -------------------------------------------------------------
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 7, 
        "WIREFRAME & GIS UX", 
        "Figma UI Architecture | ", 
        "STEP 1. 공간 GIS 토지 탐색 & 필지 규제 분석 화면 (Figma UI 원본)", 
        "피그마 공식 화면설계서 UI: 지번 검색, 지적도 경계선 시각화, 좌측 420px 컨트롤 패널 및 실시간 규제 검증", 
        right_badge=("FIGMA UI SCREEN", "green")
    )
    
    lw = 460
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="STEP 1 · FIGMA UI SPECS", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "토지 탐색 UI 인터랙션", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    specs = [
        ("01. 지번 검색 & 자동 완성", "전국 단위 지번/도로명 주소 입력 시 인근 필지 경계선 및 지목(전·답·임야)을 실시간 매칭하는 검색바 UI"),
        ("02. 지적도 & 용도지역 레이어", "국토계획법 용도지역(농림/관리/도시)을 컬러 오버레이로 시각화하고 필지 경계선 및 접도 도로 너비 표시"),
        ("03. 3초 인허가 판정 카드", "건폐율/용적률 조례 대조, 경사도 15도 이하 적합 여부를 녹색/황색/적색 3색 뱃지로 즉각 피드백")
    ]
    sy = ly + 115
    for title, desc in specs:
        draw.rounded_rectangle([125, sy, 100 + lw - 25, sy + 175], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, sy + 35), title, font=get_font(15.5, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12, 'regular'), lw - 70, draw)
        dy = sy + 68
        for l in lines:
            draw.text((145, dy), l, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 22
        sy += 195

    # Right: High-Res Real Desktop Browser Mockup with Step 1 Screen (screen_02_cadastral_map.png)
    rx = 585
    rw = 1235
    s_p = os.path.join(ASSETS_DIR, "screen_02_cadastral_map.png")
    draw_browser_mockup(img, s_p, x=rx, y=ly, w=rw, h=lh, title="FARMINGSYS ENTERPRISE · STEP 1 CADASTRAL GIS WORKSPACE", url="https://farmingsys.io/app/step-01-cadastral")

    draw_slide_footer(draw, 7, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_07.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 08: DESIGN SYSTEM & ATOMIC TOKENS (AIA+ Style Standards)
# -------------------------------------------------------------
def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 8, 
        "DESIGN SYSTEM & TOKENS", 
        "Design System | ", 
        "토지개발 플랫폼 디자인 시스템 및 아토믹 토큰 (Atomic Tokens)", 
        "Agri-Tech 친환경 컬러 토큰, Pretendard 타이포그래피 스케일, 48dp 터치 타겟, WCAG AAA 7:1 고대비 표준", 
        right_badge=("DESIGN SYSTEM STANDARDS", "green")
    )
    
    lw = 540
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="TYPOGRAPHY & ACCESSIBILITY", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "타이포그래피 및 접근성 표준", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    ds_rules = [
        ("Pretendard 본문 가독성", "현장 모바일 및 야외 태블릿 환경을 고려하여 기본 본문 16pt 이상, 장평 98%, 자간 -0.02em 적용"),
        ("WCAG AAA 고대비 검증", "야외 직사광선 환경에서도 지목/규제 텍스트가 식별되도록 배경 대비 7:1 이상의 고대비 팔레트 엄격 준수"),
        ("48dp 최소 터치 영역", "소농 및 고령 토지주를 위해 지도 위 필지 선택 핀 및 하단 CTA 버튼에 최소 48dp 터치 타깃 보장")
    ]
    dy = ly + 115
    for title, desc in ds_rules:
        draw.rounded_rectangle([125, dy, 100 + lw - 25, dy + 175], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, dy + 35), title, font=get_font(16, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12.5, 'regular'), lw - 70, draw)
        ldy = dy + 68
        for l in lines:
            draw.text((145, ldy), l, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ldy += 22
        dy += 195

    # Right: Authentic Design Tokens Graphic
    rx = 665
    rw = 1155
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ly + 35, text="ATOMIC DESIGN TOKENS MATRIX", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 285, ly + 35), "색상 팔레트, 아이콘 그리드, 버튼 컴포넌트 토큰 세트", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')

    dt_path = os.path.join(ASSETS_DIR, "part_design_tokens.png")
    if os.path.exists(dt_path):
        dt_img = Image.open(dt_path).convert('RGBA')
        scale = min((rw - 60) / dt_img.width, (lh - 90) / dt_img.height)
        dw = int(dt_img.width * scale)
        dh = int(dt_img.height * scale)
        d_res = dt_img.resize((dw, dh), Image.Resampling.LANCZOS)
        img.paste(d_res, (rx + (rw - dw) // 2, ly + 70 + (lh - 90 - dh) // 2), d_res)

    draw_slide_footer(draw, 8, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_08.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

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
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 6, 
        "USER FLOW & DECISION LOGIC", 
        "User Flow & Logic | ", 
        "원스톱 토지개발 시뮬레이션 유저 플로우 및 의사결정 분기 로직", 
        "메인(홈) → 지번 검색 → 12대 공공 API 분석 → 개발 적합 판별 분기 → 시설 배치 → 재무 평가 → 리포트 생성", 
        right_badge=("SERVICE FLOW CHART", "green")
    )
    
    card_x, card_y, card_w, card_h = 100, 210, 1720, 750
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=card_x + 30, cy=card_y + 32, text="END-TO-END DECISION TREE & FLOW CHART", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((card_x + 30, card_y + 60), "토지개발 플랫폼 핵심 사용자 흐름 및 시스템 조건 분기 로직 (완전판)", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    n1_x, n1_y, n1_w, n1_h = card_x + 30, card_y + 110, 140, 60
    draw.rounded_rectangle([n1_x, n1_y, n1_x + n1_w, n1_y + n1_h], radius=30, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((n1_x + n1_w//2, n1_y + n1_h//2), "메인(홈)", font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw_arrow(draw, (n1_x + n1_w, n1_y + n1_h//2), (n1_x + n1_w + 35, n1_y + n1_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    
    n2_x, n2_y, n2_w, n2_h = n1_x + n1_w + 35, card_y + 100, 170, 80
    draw.rounded_rectangle([n2_x, n2_y, n2_x + n2_w, n2_y + n2_h], radius=12, fill=(255, 255, 255), outline=BRAND_GREEN, width=2)
    draw_pill_badge(draw, cx=n2_x + n2_w//2, cy=n2_y + 16, text="INPUT ACTION", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    draw.text((n2_x + n2_w//2, n2_y + 42), "대상지 지번 검색", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((n2_x + n2_w//2, n2_y + 62), "또는 지도 클릭 선택", font=get_font(11.5, 'medium'), fill=BRAND_DARK, anchor='mm')
    
    draw_arrow(draw, (n2_x + n2_w, n2_y + n2_h//2), (n2_x + n2_w + 35, n2_y + n2_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    
    d1_x, d1_y, d1_w, d1_h = n2_x + n2_w + 35, card_y + 95, 175, 90
    draw.rounded_rectangle([d1_x, d1_y, d1_x + d1_w, d1_y + d1_h], radius=14, fill=(240, 246, 255), outline=(59, 130, 246), width=2)
    draw_pill_badge(draw, cx=d1_x + d1_w//2, cy=d1_y + 18, text="CHECK 01 · GIS API", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=18)
    draw.text((d1_x + d1_w//2, d1_y + 42), "공공 데이터", font=get_font(13, 'bold'), fill=(29, 78, 216), anchor='mm')
    draw.text((d1_x + d1_w//2, d1_y + 64), "파싱 성공?", font=get_font(13, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    draw.line([(d1_x + d1_w//2, d1_y + d1_h), (d1_x + d1_w//2, card_y + 245)], fill=(225, 29, 72), width=2)
    draw_arrow(draw, (d1_x + d1_w//2, card_y + 245), (d1_x + d1_w//2, card_y + 260), col=(225, 29, 72), width=2, arrow_size=6)
    draw_pill_badge(draw, cx=d1_x + d1_w//2 + 18, cy=d1_y + d1_h + 15, text="N", font=get_font(9.5, 'bold'), theme='red', pad_x=6, height=16)
    
    fb1_x, fb1_y, fb1_w, fb1_h = d1_x - 15, card_y + 260, 205, 60
    draw.rounded_rectangle([fb1_x, fb1_y, fb1_x + fb1_w, fb1_y + fb1_h], radius=12, fill=(255, 241, 242), outline=(254, 205, 211), width=2)
    draw.text((fb1_x + fb1_w//2, fb1_y + 20), "지적도 캐시 데이터 전환", font=get_font(12, 'bold'), fill=(225, 29, 72), anchor='mm')
    draw.text((fb1_x + fb1_w//2, fb1_y + 40), "수동 지번/면적 입력 팝업", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    draw_arrow(draw, (d1_x + d1_w, d1_y + d1_h//2), (d1_x + d1_w + 40, d1_y + d1_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    draw.text((d1_x + d1_w + 16, d1_y + d1_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    d2_x, d2_y, d2_w, d2_h = d1_x + d1_w + 40, card_y + 95, 180, 90
    draw.rounded_rectangle([d2_x, d2_y, d2_x + d2_w, d2_y + d2_h], radius=14, fill=(236, 253, 245), outline=BRAND_GREEN, width=2)
    draw_pill_badge(draw, cx=d2_x + d2_w//2, cy=d2_y + 18, text="CHECK 02 · 규제 적합", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    draw.text((d2_x + d2_w//2, d2_y + 42), "개발 적합 토지?", font=get_font(13.5, 'bold'), fill=BRAND_DARK, anchor='mm')
    draw.text((d2_x + d2_w//2, d2_y + 64), "(용도지역/접도/경사)", font=get_font(11, 'medium'), fill=BRAND_GREEN, anchor='mm')
    
    draw.line([(d2_x + d2_w//2, d2_y + d2_h), (d2_x + d2_w//2, card_y + 245)], fill=(225, 29, 72), width=2)
    draw_arrow(draw, (d2_x + d2_w//2, card_y + 245), (d2_x + d2_w//2, card_y + 260), col=(225, 29, 72), width=2, arrow_size=6)
    draw_pill_badge(draw, cx=d2_x + d2_w//2 + 18, cy=d2_y + d2_h + 15, text="N", font=get_font(9.5, 'bold'), theme='red', pad_x=6, height=16)
    
    fb2_x, fb2_y, fb2_w, fb2_h = d2_x - 15, card_y + 260, 210, 60
    draw.rounded_rectangle([fb2_x, fb2_y, fb2_x + fb2_w, fb2_y + fb2_h], radius=12, fill=(255, 241, 242), outline=(254, 205, 211), width=2)
    draw.text((fb2_x + fb2_w//2, fb2_y + 20), "인허가 저촉 사유 안내", font=get_font(12, 'bold'), fill=(225, 29, 72), anchor='mm')
    draw.text((fb2_x + fb2_w//2, fb2_y + 40), "대체 작물/완충 솔루션 제시", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    draw_arrow(draw, (d2_x + d2_w, d2_y + d2_h//2), (d2_x + d2_w + 40, d2_y + d2_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    draw.text((d2_x + d2_w + 16, d2_y + d2_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    n4_x, n4_y, n4_w, n4_h = d2_x + d2_w + 40, card_y + 100, 190, 80
    draw.rounded_rectangle([n4_x, n4_y, n4_x + n4_w, n4_y + n4_h], radius=12, fill=(255, 255, 255), outline=BRAND_TEAL, width=2)
    draw_pill_badge(draw, cx=n4_x + n4_w//2, cy=n4_y + 16, text="SIMULATOR", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=18)
    draw.text((n4_x + n4_w//2, n4_y + 42), "스마트팜 단지 배치", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((n4_x + n4_w//2, n4_y + 62), "온실/부대시설/작물 연동", font=get_font(11, 'medium'), fill=BRAND_TEAL, anchor='mm')
    
    draw_arrow(draw, (n4_x + n4_w, n4_y + n4_h//2), (n4_x + n4_w + 40, n4_y + n4_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    
    d3_x, d3_y, d3_w, d3_h = n4_x + n4_w + 40, card_y + 95, 180, 90
    draw.rounded_rectangle([d3_x, d3_y, d3_x + d3_w, d3_y + d3_h], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=2)
    draw_pill_badge(draw, cx=d3_x + d3_w//2, cy=d3_y + 18, text="CHECK 03 · 리포트", font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
    draw.text((d3_x + d3_w//2, d3_y + 42), "상세 금융 리포트", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((d3_x + d3_w//2, d3_y + 64), "발급 요청?", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw.line([(d3_x + d3_w//2, d3_y + d3_h), (d3_x + d3_w//2, card_y + 245)], fill=(100, 116, 139), width=2)
    draw_arrow(draw, (d3_x + d3_w//2, card_y + 245), (d3_x + d3_w//2, card_y + 260), col=(100, 116, 139), width=2, arrow_size=6)
    draw.text((d3_x + d3_w//2 + 10, d3_y + d3_h + 12), "N", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    out1_x, out1_y, out1_w, out1_h = d3_x - 15, card_y + 260, 210, 60
    draw.rounded_rectangle([out1_x, out1_y, out1_x + out1_w, out1_y + out1_h], radius=28, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((out1_x + out1_w//2, out1_y + out1_h//2), "기본 요약 웹 대시보드 열람", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw_arrow(draw, (d3_x + d3_w, d3_y + d3_h//2), (d3_x + d3_w + 40, d3_y + d3_h//2), col=BRAND_GREEN, width=2, arrow_size=7)
    draw.text((d3_x + d3_w + 16, d3_y + d3_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=BRAND_GREEN)
    
    goal_x, goal_y, goal_w, goal_h = d3_x + d3_w + 40, card_y + 100, 240, 80
    draw.rounded_rectangle([goal_x, goal_y, goal_x + goal_w, goal_y + goal_h], radius=16, fill=(236, 253, 245), outline=BRAND_GREEN, width=2)
    draw_pill_badge(draw, cx=goal_x + goal_w//2, cy=goal_y + 18, text="FINAL GOAL", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    draw.text((goal_x + goal_w//2, goal_y + 44), "종합 타당성 리포트 발급", font=get_font(14, 'bold'), fill=BRAND_DARK, anchor='mm')
    draw.text((goal_x + goal_w//2, goal_y + 64), "20p PDF 및 금융기관 제출용", font=get_font(11.5, 'medium'), fill=BRAND_GREEN, anchor='mm')

    bot_y = card_y + 360
    draw.line([(card_x + 30, bot_y - 20), (card_x + card_w - 30, bot_y - 20)], fill=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=card_x + 30, cy=bot_y + 5, text="CORE DECISION NODES SPECIFICATION", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((card_x + 320, bot_y + 5), "개발/시스템 연동을 위한 4대 의사결정 노드 상세 정의 및 예외 처리 정책", font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    nodes_detail = [
        {
            "num": "1",
            "title": "공공 GIS API 실시간 연동 및 Fallback",
            "tag": "API & 캐싱",
            "desc": "토지이음, 국토교통부 지적도, 수치표고모델(DEM) 12대 공공 API를 비동기 병렬 호출합니다. 3초 이상 응답 지연 시 최근 30일 이내 동기화된 지적 캐시 데이터로 자동 전환하여 서비스 중단 방지."
        },
        {
            "num": "2",
            "title": "3초 법적 인허가 및 조례 룰셋 자동 진단",
            "tag": "규제 엔진",
            "desc": "선택 필지의 용도지역(농림/관리/도시), 건폐율/용적률, 개발행위허가 기준(경사도 15도 이하, 도로 접도 4m 이상)을 지자체 조례 엔진과 대조하여 적합(녹색)/조건부(황색)/불가(적색) 3색 뱃지로 즉시 판정."
        },
        {
            "num": "3",
            "title": "스마트팜 모듈 최적 배치 & 작물 연동",
            "tag": "공간 시뮬레이션",
            "desc": "비전문가를 위해 연동형 온실 규격을 토지 경계선 내에 자동 최적 정렬합니다. 딸기, 토마토 등 선택 작물별 표준 생산 주기와 단가 DB를 연계하여 유효 재배 면적 및 예상 생산량을 오차 5% 이내로 시뮬레이션."
        },
        {
            "num": "4",
            "title": "CAPEX/OPEX 경제성 산출 & 금융 표준 리포트",
            "tag": "금융 모델링",
            "desc": "토지 매입비, 온실 시공비, 시설비(CAPEX)와 운영비/인건비(OPEX)를 10개년 현금흐름으로 분석합니다. 순현재가치(NPV) 및 내부수익률(IRR)을 자동 도출하여 농협 등 금융기관 대출 심사용 20p 표준 PDF를 원클릭 발급."
        }
    ]
    
    card_cols = 4
    col_w = (card_w - 60 - (card_cols - 1) * 20) // card_cols
    cy_p = bot_y + 35
    for i, nd in enumerate(nodes_detail):
        cx_p = card_x + 30 + i * (col_w + 20)
        draw.rounded_rectangle([cx_p, cy_p, cx_p + col_w, cy_p + 310], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([cx_p + 16, cy_p + 16, cx_p + 42, cy_p + 42], radius=6, fill=BRAND_GREEN)
        draw.text((cx_p + 29, cy_p + 29), nd["num"], font=get_font(13, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw_pill_badge(draw, left_x=cx_p + col_w - 95, cy=cy_p + 29, text=nd["tag"], font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=20)
        draw.text((cx_p + 16, cy_p + 58), nd["title"], font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.line([(cx_p + 16, cy_p + 82), (cx_p + col_w - 16, cy_p + 82)], fill=BORDER_LIGHT, width=1)
        
        lines = wrap_text(nd["desc"], get_font(11.5, 'regular'), col_w - 32, draw)
        ly_p = cy_p + 95
        for l in lines:
            draw.text((cx_p + 16, ly_p), l, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly_p += 18

    draw_slide_footer(draw, 6, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_06.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
