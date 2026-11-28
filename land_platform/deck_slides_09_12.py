import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 09: CORE FEATURE · STEP 2 · SMARTFARM FACILITY SIMULATION (Figma Screen sec_04)
# -------------------------------------------------------------
def make_slide_09():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 9, 
        "CORE FEATURE · STEP 2", 
        "Simulation Step 2 | ", 
        "STEP 2. 스마트 단지 설계 & 온실 모듈 최적 배치 화면 (Figma UI 원본)", 
        "피그마 공식 화면설계서 UI: 온실 규격 선택, 6m 내부 관통 도로 구획, 부대시설 배치 및 생산량 시뮬레이션", 
        right_badge=("SIMULATOR STEP 2", "green")
    )
    
    lw = 460
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="STEP 2 · FACILITY DESIGNER", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 72), "스마트 단지 설계 UI", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((130, ly + 96), "토지 경계 내 온실 모듈 & 부대시설 자동 구획", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)

    cards = [
        ("01. 온실 모듈 규격 최적화", "단동/연동형 비닐온실, 첨단 유리온실, 수직농장 등 작물별 최적 규격을 토지 경계선 내에 오차 5% 이내로 자동 정렬"),
        ("02. 도로망 & 부대시설 연계", "수확물 대형 트럭 반출을 위한 6m 내부 관통 도로망, 저온저장고, 선별장, ICT 관제센터 등 지원시설 자동 배치"),
        ("03. 농진청 DB 기반 수확량 산출", "딸기, 파프리카, 토마토 등 고부가가치 작물의 재배 주기와 3개년 가락시장 경락가를 연동해 연간 예상 생산량 즉시 도출")
    ]
    cy = ly + 120
    for title, desc in cards:
        draw.rounded_rectangle([125, cy, 100 + lw - 25, cy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, cy + 22), title, font=get_font(14, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(11.5, 'regular'), lw - 70, draw)
        dy = cy + 48
        for l in lines:
            draw.text((145, dy), l, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        cy += 145

    # Bottom Key Metric Callout in Left Card
    draw.rounded_rectangle([125, ly + 575, 100 + lw - 25, ly + 715], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((145, ly + 596), "💡 STEP 2 핵심 설계 전략 및 가치", font=get_font(13, 'bold'), fill=BRAND_DARK)
    val_desc = "복잡한 CAD나 3D 그래픽 툴 숙련 없이도, 일반 농민이 클릭 한 번으로 유효 부지 면적 대비 최고 수익률을 내는 최적 온실 배치를 완성할 수 있도록 공간 알고리즘을 단순화했습니다."
    lines_val = wrap_text(val_desc, get_font(11, 'regular'), lw - 70, draw)
    vy = ly + 620
    for l in lines_val:
        draw.text((145, vy), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_MAIN)
        vy += 17

    # Right: High-Res Real Desktop Browser Mockup with Authentic Figma Screen sec_04
    rx = 585
    rw = 1235
    s_p = os.path.join(ASSETS_DIR, "figma_screen_sec_04.png")
    if not os.path.exists(s_p):
        s_p = os.path.join(ASSETS_DIR, "screen_03_facility_simulation.png")
    draw_browser_mockup(img, s_p, x=rx, y=ly, w=rw, h=lh, title="FARMINGSYS ENTERPRISE · STEP 2 FACILITY LAYOUT SIMULATOR", url="https://farmingsys.io/app/step-02-facility")

    draw_slide_footer(draw, 9, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_09.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 10: CORE FEATURE · STEP 3 · ECONOMIC VALUATION & CAPEX MODEL (Figma Screen sec_06)
# -------------------------------------------------------------
def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 10, 
        "CORE FEATURE · STEP 3", 
        "Simulation Step 3 | ", 
        "STEP 3. 총사업비 산출 & CAPEX/OPEX 경제성 모델링 화면 (Figma UI 원본)", 
        "피그마 공식 화면설계서 UI: 토지매입비, ICT 온실 시공비, 연간 운영비, 10개년 현금흐름 및 투자 회수기간 자동 도출", 
        right_badge=("SIMULATOR STEP 3", "green")
    )
    
    lw = 460
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="STEP 3 · ECONOMIC MODELING", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 72), "총사업비 경제성 모델 UI", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((130, ly + 96), "정량적 재무 지표 및 투자 타당성 실시간 연산", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)

    cards = [
        ("01. CAPEX/OPEX 세부 분해표", "토지 매입비, 토목 기초공사비, ICT 스마트 온실 설비비(CAPEX)와 연간 인건비, 냉난방비, 종묘비(OPEX)를 투명하게 분해"),
        ("02. 10개년 현금흐름 & 회수기간", "시설 감가상각비, 정부 정책자금 융자 금리(2.0%), 법인세 혜택을 종합 반영하여 사업 손익분기점(BEP) 및 회수연수 산출"),
        ("03. 실시간 재무 지표 연동 피드백", "작물 선택이나 재배 면적을 변경할 때마다 IRR(내부수익률 12.8%+)과 NPV(순현재가치)가 지연 없이 재연산되어 의사결정 지원")
    ]
    cy = ly + 120
    for title, desc in cards:
        draw.rounded_rectangle([125, cy, 100 + lw - 25, cy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, cy + 22), title, font=get_font(14, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(11.5, 'regular'), lw - 70, draw)
        dy = cy + 48
        for l in lines:
            draw.text((145, dy), l, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        cy += 145

    # Bottom Key Metric Callout in Left Card
    draw.rounded_rectangle([125, ly + 575, 100 + lw - 25, ly + 715], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((145, ly + 596), "💡 STEP 3 핵심 설계 전략 및 가치", font=get_font(13, 'bold'), fill=BRAND_DARK)
    val_desc = "단순한 토지 가격 비교를 넘어, 10년간 실제 발생할 운영비용과 매출을 금융 공학 모델로 분석하여 무리한 대출로 인한 부실 위험을 원천 차단하고 투자 성공 확률을 극대화했습니다."
    lines_val = wrap_text(val_desc, get_font(11, 'regular'), lw - 70, draw)
    vy = ly + 620
    for l in lines_val:
        draw.text((145, vy), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_MAIN)
        vy += 17

    # Right: High-Res Real Desktop Browser Mockup with Authentic Figma Screen sec_06
    rx = 585
    rw = 1235
    s_p = os.path.join(ASSETS_DIR, "figma_screen_sec_06.png")
    if not os.path.exists(s_p):
        s_p = os.path.join(ASSETS_DIR, "screen_04_economic_modeling.png")
    draw_browser_mockup(img, s_p, x=rx, y=ly, w=rw, h=lh, title="FARMINGSYS ENTERPRISE · STEP 3 FINANCIAL VALUATION ENGINE", url="https://farmingsys.io/app/step-03-valuation")

    draw_slide_footer(draw, 10, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_10.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 11: CORE FEATURE · STEP 4 · VALUATION REPORT & FINANCING (Figma Screen sec_08)
# -------------------------------------------------------------
def make_slide_11():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 11, 
        "CORE FEATURE · STEP 4", 
        "Simulation Step 4 | ", 
        "STEP 4. 사업 타당성 평가서 & 금융 표준 리포트 발급 화면 (Figma UI 원본)", 
        "피그마 공식 화면설계서 UI: 지적도 개요, 법적 적합도 요약, 배치 평면도, 재무 전망을 집약한 금융기관 심사용 20p PDF 보고서", 
        right_badge=("SIMULATOR STEP 4", "green")
    )
    
    lw = 460
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="STEP 4 · REPORT GENERATOR", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 72), "금융 리포트 발급 UI", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((130, ly + 96), "정책금융 심사 제출용 표준 타당성 보고서", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)

    cards = [
        ("01. 표준 타당성 평가서 생성", "지번 기본정보, 용도지역 규제 분석표, 온실 배치 조감도, 재무성 분석표를 종합 수록한 은행 심사용 공인 보고서"),
        ("02. 금융 심사 표준 20p PDF 발급", "농협, 수협, 신용보증기금 등 정책금융 대출 심사에 즉시 제출 가능한 공인 포맷의 다면 보고서 원클릭 다운로드"),
        ("03. 투자자·시공사 매칭 연결", "검토 완료된 프로젝트를 플랫폼 내 인증 스마트팜 전문 시공사 및 정책자금 전문 컨설턴트와 다이렉트 매칭 지원")
    ]
    cy = ly + 120
    for title, desc in cards:
        draw.rounded_rectangle([125, cy, 100 + lw - 25, cy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, cy + 22), title, font=get_font(14, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(11.5, 'regular'), lw - 70, draw)
        dy = cy + 48
        for l in lines:
            draw.text((145, dy), l, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        cy += 145

    # Bottom Key Metric Callout in Left Card
    draw.rounded_rectangle([125, ly + 575, 100 + lw - 25, ly + 715], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((145, ly + 596), "💡 STEP 4 핵심 설계 전략 및 가치", font=get_font(13, 'bold'), fill=BRAND_DARK)
    val_desc = "단순 화면 조회를 넘어 '실제 자금 조달과 시공 계약'이라는 최종 현실 목표를 달성할 수 있도록, 금융 기관이 요구하는 공인 양식에 맞춘 20페이지 보고서를 원클릭 자동 생성하도록 완결성을 부여했습니다."
    lines_val = wrap_text(val_desc, get_font(11, 'regular'), lw - 70, draw)
    vy = ly + 620
    for l in lines_val:
        draw.text((145, vy), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_MAIN)
        vy += 17

    # Right: High-Res Real Desktop Browser Mockup with Authentic Figma Screen sec_08
    rx = 585
    rw = 1235
    s_p = os.path.join(ASSETS_DIR, "figma_screen_sec_08.png")
    if not os.path.exists(s_p):
        s_p = os.path.join(ASSETS_DIR, "screen_05_valuation_report.png")
    draw_browser_mockup(img, s_p, x=rx, y=ly, w=rw, h=lh, title="FARMINGSYS ENTERPRISE · STEP 4 VALUATION REPORT EXPORT", url="https://farmingsys.io/app/step-04-report")

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
