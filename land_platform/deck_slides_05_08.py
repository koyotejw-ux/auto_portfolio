import os
from PIL import Image, ImageDraw
from deck_common import *

def make_slide_05():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 5, "GIS WIREFRAME & UX LOGIC", "GIS UX Architecture", "대화면 공간 GIS 기반 와이어프레임 및 레이아웃 설계", "좌측 제어 패널과 우측 인터랙티브 GIS 지도의 듀얼 스플릿 뷰를 통한 조작 직관성 극대화")

    # Left Column: Structure Logic
    lx = 80
    lw = 540
    draw.rounded_rectangle([lx, 260, lx + lw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, lx + 25, 295, "DUAL-SPLIT INTERACTION LOGIC", get_font(10.5, 'bold'), theme='green')
    draw.text((lx + 25, 335), "GIS 공간 분석 특화 UI 그리드", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    logic_cards = [
        ("좌측 420px 고정 워크플로우 패널", "STEP 1(대상지)부터 STEP 3(타당성)까지 스텝 인디케이터와 입력 폼을 단일 시선 동선에 집중 배치"),
        ("우측 가변 인터랙티브 GIS 캔버스", "카카오/V-World 고해상도 위성지도, 지적도 레이어, 고도/경사도 히트맵 및 시설 3D 메쉬 동적 렌더링"),
        ("하단 플로팅 종합 서머리 바", "토지 면적, 가용 면적, 총 소요 비용, 연간 추정 수익률의 실시간 누적 연산 결과를 즉시 피드백")
    ]
    ly = 385
    for title, desc in logic_cards:
        draw.rounded_rectangle([lx + 20, ly, lx + lw - 20, ly + 145], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, ly + 35), title, font=get_font(16, 'bold'), fill=BRAND_GREEN)
        draw.text((lx + 40, ly + 72), desc, font=get_font(13, 'regular'), fill=TEXT_LIGHT_SUB)
        ly += 175

    # Right Column: Visual Wireframe Mockup
    rx = 650
    rw = W - 80 - rx
    draw.rounded_rectangle([rx, 260, rx + rw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    wf_p = os.path.join(ASSETS_DIR, "screen_02_map_analysis.png")
    if os.path.exists(wf_p):
        w_img = Image.open(wf_p).convert('RGBA')
        scale = min((rw - 40) / w_img.width, (950 - 260 - 40) / w_img.height)
        nw = int(w_img.width * scale)
        nh = int(w_img.height * scale)
        w_res = w_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(w_res, (rx + (rw - nw) // 2, 260 + (950 - 260 - nh) // 2), w_res)

    draw_slide_footer(draw, 5, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_05.png"), quality=95)
    print("Generated slide_05.png")

def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 6, "DESIGN SYSTEM & ATOMIC TOKENS", "Design System & Tokens", "토지개발 B2B 엔터프라이즈 디자인 시스템", "자연의 신뢰를 상징하는 에머랄드 그린 컬러와 고대비 폰트, 반응형 모듈 컴포넌트 규격")

    # Left: Typography & Hierarchy
    c1_x = 80
    c1_w = 540
    draw.rounded_rectangle([c1_x, 260, c1_x + c1_w, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, c1_x + 25, 295, "TYPOGRAPHY TOKENS", get_font(10.5, 'bold'), theme='green')
    draw.text((c1_x + 25, 335), "프리텐다드 기반 정보 계층 구조", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    typos = [
        ("Display 1 (36pt Bold)", "메인 헤드라인 및 핵심 지표 수치"),
        ("Headline 1 (24pt Bold)", "섹션 타이틀 및 단계별 핵심 모듈명"),
        ("Subtitle 1 (18pt SemiBold)", "카드 및 위젯 상단 서브헤더"),
        ("Body 1 (15pt Medium)", "데이터 라벨, 토지 정보 설명 문구"),
        ("Caption (12pt Regular)", "공시지가 고시일, 법적 기준 주석")
    ]
    ty = 385
    for t_name, t_use in typos:
        draw.rounded_rectangle([c1_x + 20, ty, c1_x + c1_w - 20, ty + 85], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((c1_x + 35, ty + 25), t_name, font=get_font(14, 'bold'), fill=BRAND_GREEN)
        draw.text((c1_x + 35, ty + 50), t_use, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
        ty += 105

    # Middle: Color Palette & WCAG
    c2_x = 650
    c2_w = 540
    draw.rounded_rectangle([c2_x, 260, c2_x + c2_w, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, c2_x + 25, 295, "COLOR & ACCESSIBILITY", get_font(10.5, 'bold'), theme='green')
    draw.text((c2_x + 25, 335), "신뢰 기반 친환경 엔터프라이즈 팔레트", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    palette = [
        ("Primary Emerald", "#059669", (5, 150, 105), "브랜드 메인 및 액션 CTA 버튼"),
        ("Dark Green", "#047857", (4, 120, 87), "강조 헤더 및 호버 스테이트"),
        ("Mint Accent", "#10B981", (16, 185, 129), "수익률 긍정 지표 및 포커스 링"),
        ("Slate Deep", "#0F172A", (15, 23, 42), "본문 고대비 텍스트 (WCAG AAA)"),
        ("Light Slate", "#F8FAFC", (248, 250, 252), "컨테이너 배경 및 패널 베이스")
    ]
    py = 385
    for name, hex_code, rgb_val, desc in palette:
        draw.rounded_rectangle([c2_x + 20, py, c2_x + c2_w - 20, py + 85], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([c2_x + 35, py + 18, c2_x + 85, py + 68], radius=8, fill=rgb_val)
        draw.text((c2_x + 105, py + 25), f"{name} ({hex_code})", font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((c2_x + 105, py + 50), desc, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
        py += 105

    # Right: UI Components
    c3_x = 1220
    c3_w = W - 80 - c3_x
    draw.rounded_rectangle([c3_x, 260, c3_x + c3_w, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, c3_x + 25, 295, "UI COMPONENTS", get_font(10.5, 'bold'), theme='green')
    draw.text((c3_x + 25, 335), "4대 핵심 컴포넌트 규격", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    comps = [
        ("Step Workflow Indicator", "STEP 1 ~ STEP 4 진행 상태 시각화 칩"),
        ("GIS Layer Floating Controller", "지적도/위성/로드뷰 원클릭 토글러"),
        ("Facility Preset Card", "스마트팜/온실/태양광 모듈 셀렉터"),
        ("Feasibility Gauge Widget", "IRR 및 회수기간 가시화 반원형 차트")
    ]
    cy = 385
    for c_title, c_desc in comps:
        draw.rounded_rectangle([c3_x + 20, cy, c3_x + c3_w - 20, cy + 115], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((c3_x + 35, cy + 30), c_title, font=get_font(15, 'bold'), fill=BRAND_GREEN)
        draw.text((c3_x + 35, cy + 65), c_desc, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
        cy += 135

    draw_slide_footer(draw, 6, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_06.png"), quality=95)
    print("Generated slide_06.png")

def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 7, "CORE FEATURE 01", "GIS Land Analysis", "STEP 1. 공간 GIS 토지 탐색 및 3초 규제 분석", "지번 입력 즉시 공공 데이터 연동을 통해 토지이용계획과 법적 인허가 제한 사항을 실시간 판별")

    # Left: Feature Details
    lx = 80
    lw = 600
    draw.rounded_rectangle([lx, 260, lx + lw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, lx + 25, 295, "FEATURE BREAKDOWN", get_font(10.5, 'bold'), theme='green')
    draw.text((lx + 25, 335), "공공 데이터 융합 토지 분석 엔진", font=get_font(22, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    f_cards = [
        ("원터치 주소/지번 통합 검색", "전국 단위 지번 및 도로명 주소를 정밀 인덱싱하여 오탈자 자동 보정 및 인근 필지 동시 추천"),
        ("12대 공공 데이터 실시간 파싱", "용도지역, 건폐율/용적률, 접도 의무, 고도제한, 상수원보호구역, 생태자연도 등 규제 일괄 진단"),
        ("개발 불가 영역 자동 마스킹", "경사도 25도 초과 구역, 보전산지, 맹지 등 개발 리스크 구역을 GIS 지도상에 붉은색 히트맵으로 즉시 시각화")
    ]
    fy = 400
    for title, desc in f_cards:
        draw.rounded_rectangle([lx + 20, fy, lx + lw - 20, fy + 150], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, fy + 35), title, font=get_font(17, 'bold'), fill=BRAND_GREEN)
        draw.text((lx + 40, fy + 75), desc, font=get_font(13.5, 'regular'), fill=TEXT_LIGHT_SUB)
        fy += 175

    # Right: High Resolution Screen View
    rx = 710
    rw = W - 80 - rx
    draw.rounded_rectangle([rx, 260, rx + rw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    s_p = os.path.join(ASSETS_DIR, "screen_02_map_analysis.png")
    if os.path.exists(s_p):
        s_img = Image.open(s_p).convert('RGBA')
        scale = min((rw - 30) / s_img.width, (950 - 260 - 30) / s_img.height)
        sw = int(s_img.width * scale)
        sh = int(s_img.height * scale)
        s_res = s_img.resize((sw, sh), Image.Resampling.LANCZOS)
        img.paste(s_res, (rx + (rw - sw) // 2, 260 + (950 - 260 - sh) // 2), s_res)

    draw_slide_footer(draw, 7, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_07.png"), quality=95)
    print("Generated slide_07.png")

def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 8, "CORE FEATURE 02", "Facility Layout Simulation", "STEP 2. 스마트 단지 설계 및 최적 시설 배치", "선택된 토지의 가용 면적에 최적화된 스마트팜 온실, 부대시설, 진입 도로 자동 모듈 배치")

    # Left: Feature Details
    lx = 80
    lw = 600
    draw.rounded_rectangle([lx, 260, lx + lw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, lx + 25, 295, "SMART FACILITY LAYOUT", get_font(10.5, 'bold'), theme='green')
    draw.text((lx + 25, 335), "알고리즘 기반 최적 시설 배치", font=get_font(22, 'bold'), fill=TEXT_LIGHT_MAIN)

    layout_cards = [
        ("다양한 스마트팜 온실 모듈 지원", "단동/연동형 비닐온실, 유리온실, 수직농장 등 작물별 최적화 규격(폭/길이/동고) 선택"),
        ("토지 형상에 맞춘 자동 구획 배치", "불규칙한 토지 경계선 내에서 일조량과 향(남향)을 고려하여 최대 가용 면적을 도출하는 자동 배치 엔진"),
        ("진입도로 및 부대시설 연동", "차량 통행을 위한 6m 도로 구획, 관리동, 선별장, 폐수처리 설비 배치 자동 연산")
    ]
    fy = 400
    for title, desc in layout_cards:
        draw.rounded_rectangle([lx + 20, fy, lx + lw - 20, fy + 150], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, fy + 35), title, font=get_font(17, 'bold'), fill=BRAND_GREEN)
        draw.text((lx + 40, fy + 75), desc, font=get_font(13.5, 'regular'), fill=TEXT_LIGHT_SUB)
        fy += 175

    # Right: High Resolution Screen View
    rx = 710
    rw = W - 80 - rx
    draw.rounded_rectangle([rx, 260, rx + rw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    s_p = os.path.join(ASSETS_DIR, "screen_03_facility_layout.png")
    if os.path.exists(s_p):
        s_img = Image.open(s_p).convert('RGBA')
        scale = min((rw - 30) / s_img.width, (950 - 260 - 30) / s_img.height)
        sw = int(s_img.width * scale)
        sh = int(s_img.height * scale)
        s_res = s_img.resize((sw, sh), Image.Resampling.LANCZOS)
        img.paste(s_res, (rx + (rw - sw) // 2, 260 + (950 - 260 - sh) // 2), s_res)

    draw_slide_footer(draw, 8, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_08.png"), quality=95)
    print("Generated slide_08.png")

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
