import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 09: CORE STEP 1 · GIS LAND REGULATION ANALYSIS (Browser Mockup + 3 Specs)
# -------------------------------------------------------------
def make_slide_09():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 9, 
        "CORE FEATURE · STEP 1", 
        "GIS Land Analysis | ", 
        "STEP 1. 공간 GIS 토지 탐색 및 3초 공적 규제 진단", 
        "지번 입력 즉시 12대 공공 데이터 연동을 통해 토지이용계획과 법적 인허가 제한 사항을 실시간 판별", 
        right_badge=("CORE FEATURE 01", "green")
    )
    
    lw = 540
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="3-SECOND REGULATION ENGINE", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "12대 공공 데이터 실시간 파싱", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    cards = [
        ("원터치 지번/주소 통합 검색", "전국 단위 지번 및 도로명 주소를 정밀 인덱싱하여 오탈자 자동 보정 및 인근 필지 동시 추천"),
        ("12대 공공 규제 실시간 진단", "용도지역, 건폐율/용적률, 접도 의무, 고도제한, 상수원보호구역, 생태자연도 등 규제 일괄 진단"),
        ("개발 불가 구역 자동 마스킹", "경사도 25도 초과 구역, 보전산지, 맹지 등 개발 리스크 구역을 GIS 지도상에 붉은색 히트맵으로 시각화")
    ]
    cy = ly + 115
    for title, desc in cards:
        draw.rounded_rectangle([125, cy, 100 + lw - 25, cy + 175], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, cy + 35), title, font=get_font(16, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12.5, 'regular'), lw - 70, draw)
        dy = cy + 75
        for l in lines:
            draw.text((145, dy), l, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 22
        cy += 195

    # Right: Authentic High Resolution Browser Mockup
    rx = 665
    rw = 1155
    s_p = os.path.join(ASSETS_DIR, "screen_02_cadastral_map.png")
    if not os.path.exists(s_p):
        s_p = os.path.join(ASSETS_DIR, "screen_02_map_analysis.png")
        
    draw_browser_mockup(img, s_p, x=rx, y=ly, w=rw, h=lh, title="FARMINGSYS ENTERPRISE · STEP 1 CADASTRAL & REGULATION ENGINE", url="https://farmingsys.io/workspace/step-01-cadastral")

    draw_slide_footer(draw, 9, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_09.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 10: CORE STEP 2 · FACILITY LAYOUT & CROP SIMULATION (Browser Mockup + 3 Specs)
# -------------------------------------------------------------
def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 10, 
        "CORE FEATURE · STEP 2", 
        "Facility & Crop Layout | ", 
        "STEP 2. 스마트 단지 설계 및 최적 시설·작물 시뮬레이션", 
        "가용 면적에 최적화된 스마트팜 온실, 진입 도로, 부대시설 자동 배치 및 농진청 DB 기반 수확량 예측", 
        right_badge=("CORE FEATURE 02", "green")
    )
    
    lw = 540
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="FACILITY & CROP MATCHING", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "단지 설계 및 생산량 시뮬레이션", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    cards = [
        ("스마트 온실 모듈 최적 구획", "단동/연동형 비닐온실, 유리온실, 수직농장 등 작물별 최적 규격을 토지 형상에 맞추어 자동 모듈화"),
        ("도로 및 부대시설 자동 연계", "차량 교행을 위한 6m 도로 구획, 선별장, 저온저장고, 관리동 설비 배치 면적 자동 연산"),
        ("농진청 DB 기반 작물 생산성 예측", "딸기, 토마토, 파프리카 등 고부가가치 작물의 재배 주기와 3개년 평균 경락가를 매칭하여 매출 추정")
    ]
    cy = ly + 115
    for title, desc in cards:
        draw.rounded_rectangle([125, cy, 100 + lw - 25, cy + 175], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, cy + 35), title, font=get_font(16, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12.5, 'regular'), lw - 70, draw)
        dy = cy + 75
        for l in lines:
            draw.text((145, dy), l, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 22
        cy += 195

    # Right: Authentic High Resolution Browser Mockup
    rx = 665
    rw = 1155
    s_p = os.path.join(ASSETS_DIR, "screen_03_facility_simulation.png")
    if not os.path.exists(s_p):
        s_p = os.path.join(ASSETS_DIR, "screen_03_facility_layout.png")
        
    draw_browser_mockup(img, s_p, x=rx, y=ly, w=rw, h=lh, title="FARMINGSYS ENTERPRISE · STEP 2 FACILITY LAYOUT SIMULATOR", url="https://farmingsys.io/workspace/step-02-facility")

    draw_slide_footer(draw, 10, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_10.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 11: CORE STEP 3 · FINANCIAL VALUATION & REPORT (Browser Mockup + 3 Specs)
# -------------------------------------------------------------
def make_slide_11():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 11, 
        "CORE FEATURE · STEP 3", 
        "Financial Feasibility | ", 
        "STEP 3. 경제성 타당성 분석 모델 & 종합 보고서 생성", 
        "총사업비, 시설조성비, 10개년 현금흐름, IRR 산출 및 금융 심사용 20페이지 표준 PDF 보고서 발급", 
        right_badge=("CORE FEATURE 03", "green")
    )
    
    lw = 540
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="FINANCIAL VALUATION MODEL", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "정량 경제성 평가 & 리포트", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    cards = [
        ("세부 CAPEX / OPEX 산출 명세", "토지 매입비, 토목/건축공사비, ICT 온실 설비비, 연간 인건비 및 난방비 정밀 분해 내역 제공"),
        ("10개년 현금흐름 & 손익분기점", "감가상각, 법인세, 금융 이자율을 반영한 연차별 순수익 추정과 투자금 회수기간 도출"),
        ("금융 심사 표준 보고서 PDF 발급", "토지 개요, 규제 진단, 배치도, 재무 예측표를 집약한 20페이지 분량의 심사 보고서 즉시 출력")
    ]
    cy = ly + 115
    for title, desc in cards:
        draw.rounded_rectangle([125, cy, 100 + lw - 25, cy + 175], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, cy + 35), title, font=get_font(16, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12.5, 'regular'), lw - 70, draw)
        dy = cy + 75
        for l in lines:
            draw.text((145, dy), l, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 22
        cy += 195

    # Right: Authentic High Resolution Browser Mockup
    rx = 665
    rw = 1155
    s_p = os.path.join(ASSETS_DIR, "screen_04_economic_modeling.png")
    if not os.path.exists(s_p):
        s_p = os.path.join(ASSETS_DIR, "screen_06_economic_analysis.png")
        
    draw_browser_mockup(img, s_p, x=rx, y=ly, w=rw, h=lh, title="FARMINGSYS ENTERPRISE · STEP 3 FINANCIAL VALUATION & REPORT", url="https://farmingsys.io/workspace/step-03-valuation")

    draw_slide_footer(draw, 11, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_11.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 12: OUTCOMES & RETROSPECTIVE (AIA+ Style Full Retrospective)
# -------------------------------------------------------------
def make_slide_12():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 12, 
        "OUTCOMES & RETROSPECTIVE", 
        "Project Retrospective | ", 
        "토지개발 플랫폼 성과 지표 및 STAR 기법 회고", 
        "인허가 분석 시간 90% 단축과 100+ 규제 자동 매칭 달성, 200자 이상 시니어 UX 전략 기술 회고", 
        right_badge=("PROJECT OUTCOMES", "green")
    )
    
    metrics = [
        {
            "val": "100+",
            "title": "분석 가능 토지 규제 조건",
            "desc": "국토계획법, 산지관리법, 농지법 등 100여 개 공공 인허가 조건 및 행위 제한 자동 매칭"
        },
        {
            "val": "90%",
            "title": "분석 소요 시간 단축",
            "desc": "기존 2주(14일) 이상 소요되던 복잡한 현장·서류 검토를 3~5초 내 실시간 자동 진단"
        },
        {
            "val": "3~5s",
            "title": "원터치 시뮬레이션 도출",
            "desc": "지번 입력 즉시 최적 단지 구획, 스마트팜 모듈 및 시설 조성비 산출 자동화 완성"
        },
        {
            "val": "40%",
            "title": "의사결정 정확도 향상",
            "desc": "정량적 데이터와 공공 지적도 기반의 타당성 검토를 통해 사업 투자 리스크 사전 차단"
        }
    ]
    
    m_y = 220
    m_w = 412
    m_h = 190
    for i, m in enumerate(metrics):
        mx = 100 + i * (m_w + 24)
        draw.rounded_rectangle([mx, m_y, mx + m_w, m_y + m_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw.text((mx + 25, m_y + 25), m["val"], font=get_num_font(34, 'black'), fill=BRAND_GREEN)
        draw.text((mx + 25, m_y + 75), m["title"], font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
        lines = wrap_text(m["desc"], get_font(12, 'regular'), m_w - 50, draw)
        ly = m_y + 110
        for l in lines:
            draw.text((mx + 25, ly), l, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 20

    # STAR Retrospective Full Card
    r_y = 440
    r_w = 1720
    r_h = 520
    draw.rounded_rectangle([100, r_y, 100 + r_w, r_y + r_h], radius=16, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=135, cy=r_y + 40, text="SENIOR UX STRATEGY RETROSPECTIVE (STAR)", font=get_font(11, 'bold'), theme='green', pad_x=14, height=28)
    draw.text((135, r_y + 90), "공간 GIS와 금융 데이터가 융합된 복잡계를 직관적 디지털 경험으로 전환한 여정", font=get_font(23, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    star_items = [
        ("Situation (상황 및 배경)", "토지개발은 공간 지적도, 수많은 지자체 조례, 복잡한 인허가 법률, 대규모 자금 조달이 얽혀 있어 정보 비대칭이 극심하고, 비전문가인 토지 소유주가 사업성을 검토하기에는 진입 장벽이 매우 높은 고위험 시장이었습니다."),
        ("Task (해결 과제 및 목표)", "복잡한 법률·규제 데이터를 사용자가 학습하지 않고도 직관적으로 이해할 수 있는 단일 워크플로우를 구축하고, 대상지 선택부터 시설 배치, 작물별 수확량 예측, 경제성 타당성 보고서 출력까지 원스톱으로 지원하는 B2B 플랫폼 아키텍처를 완성해야 했습니다."),
        ("Action (실행 전략 및 디자인 결정)", "좌측 420px 워크플로우 패널과 우측 인터랙티브 GIS 캔버스의 듀얼 스플릿 뷰를 설계하여 조작 편의성을 극대화했습니다. 12대 공공 데이터를 3단계 계층 구조로 정제하고, 개발 불가 구역을 붉은색 히트맵으로 시각화하여 리스크 인지율을 100% 확보했습니다. 또한 고대비 에머랄드 그린(#00C65F) 디자인 시스템을 구축하여 복잡한 재무 지표를 한눈에 파악하도록 최적화했습니다."),
        ("Result & Learning (성과 및 회고)", "기존 2주 이상 소요되던 토지 타당성 분석 기간을 3~5초로 90% 이상 단축했으며, 토지주-개발사-투자사 간 신뢰 기반의 협업 허브를 구축했습니다. 방대한 전문 도메인 지식을 프로덕트 디자이너의 직관적 UX 아키텍처로 체계화함으로써 비즈니스 가치를 극대화한 프로젝트였습니다.")
    ]
    sy = r_y + 140
    for tag, text in star_items:
        draw.text((135, sy), tag, font=get_font(14, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(text, get_font(13, 'regular'), r_w - 70, draw)
        ly = sy + 25
        for l in lines:
            draw.text((135, ly), l, font=get_font(13, 'regular'), fill=TEXT_LIGHT_MAIN)
            ly += 22
        sy += 88

    draw_slide_footer(draw, 12, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_12.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_09()
    make_slide_10()
    make_slide_11()
    make_slide_12()
