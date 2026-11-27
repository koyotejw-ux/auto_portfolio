import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 01: HERO COVER (AIA+ Style Layout)
# -------------------------------------------------------------
def make_slide_01():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    
    # Header tag
    draw_pill_badge(draw, left_x=120, cy=105, text="B2B PROPTECH & GIS CLOUD", font=get_font(11, 'bold'), theme='green', pad_x=12, height=26)
    draw.text((310, 105), "FARMINGSYS ENTERPRISE PLATFORM", font=get_font(12, 'bold'), fill=BRAND_GREEN, anchor='lm')
    
    # Title
    draw.text((120, 155), "FARMINGSYS", font=get_font(58, 'black'), fill=(15, 23, 42))
    draw.text((495, 155), "LAND PLATFORM", font=get_font(58, 'black'), fill=BRAND_GREEN)
    draw.text((120, 235), "공간 GIS 빅데이터 & 토지개발 사업 타당성 분석 플랫폼", font=get_font(26, 'bold'), fill=(51, 65, 85))
    
    desc_kr = (
        "복잡한 공적 규제와 인허가, 토지이용계획 공간 데이터를 3초 내 자동 진단하고\n"
        "비전문가 토지 소유주부터 전문 개발사, 금융 투자자까지 원스톱으로 연결하는\n"
        "국내 유일의 엔터프라이즈급 토지개발 사업 타당성 및 경제성 자동 시뮬레이션 SaaS"
    )
    draw.text((120, 295), desc_kr, font=get_font(15.5, 'regular'), fill=(100, 116, 139), spacing=8)
    
    # 5 Spheres (from user's Figma Overview bubble network)
    draw.text((120, 400), "토지개발 플랫폼 5대 핵심 도메인 (Overview)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    spheres = [
        ("토지탐색", "지번/지적도 조회", BRAND_GREEN),
        ("인허가", "3초 규제 판별", BRAND_DARK),
        ("시설배치", "스마트팜 단지설계", BRAND_TEAL),
        ("경제성", "투자비용/IRR 산출", (99, 102, 241)),
        ("보고서", "표준 리포트/매칭", (71, 85, 105))
    ]
    for idx, (s_name, s_sub, s_col) in enumerate(spheres):
        sx = 120 + idx * 125
        sy = 450
        draw.ellipse([sx, sy, sx + 95, sy + 95], fill=s_col)
        draw.text((sx + 47, sy + 38), s_name, font=get_font(17, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((sx + 47, sy + 62), s_sub, font=get_font(9.5, 'medium'), fill=(255, 255, 255), anchor='mm')
        
    # 4 Quantitative Impact Cards (Exact from User Figma)
    stats = [
        ("100+", "분석 가능 토지 규제 조건"),
        ("90%", "분석 소요 시간 단축"),
        ("3~5s", "원터치 시뮬레이션 도출"),
        ("40%", "의사결정 정확도 향상")
    ]
    card_y = 610
    for idx, (val, label) in enumerate(stats):
        cx = 120 + (idx % 2) * 280
        cy = card_y + (idx // 2) * 110
        cw, ch = 265, 95
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((cx + 20, cy + 20), val, font=get_num_font(32, 'black'), fill=BRAND_GREEN if idx==0 else (15, 23, 42))
        lines = wrap_text(label, get_font(11.5, 'medium'), cw - 40, draw)
        ly = cy + 56
        for line in lines:
            draw.text((cx + 20, ly), line, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_SUB)
            ly += 16

    # Project Meta Info
    draw.rounded_rectangle([120, 850, 680, 950], radius=12, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    metas = [
        ("프로젝트", "토지개발사업 분석 플랫폼 B2B 클라우드 SaaS"),
        ("수행 역할", "B2B UX/UI 아키텍처 및 디자인 시스템 총괄 (100% 단독)"),
        ("핵심 혁신", "12대 공공 데이터 실시간 파싱 & 3단계 시뮬레이션 자동화")
    ]
    my = 862
    for k, v in metas:
        draw.text((140, my), k, font=get_font(11.5, 'bold'), fill=BRAND_GREEN)
        draw.text((210, my), v, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN)
        my += 28

    # Right Hero Mockup Frame
    mock_p = os.path.join(ASSETS_DIR, "screen_01_landing.png")
    if os.path.exists(mock_p):
        m_img = Image.open(mock_p).convert('RGBA')
        mw = 1000
        mh = int(m_img.height * (mw / m_img.width))
        m_res = m_img.resize((mw, mh), Image.Resampling.LANCZOS)
        fx = 760
        fy = 140
        draw.rounded_rectangle([fx - 10, fy - 10, fx + mw + 10, fy + 800], radius=16, fill=(15, 23, 42), outline=BORDER_DARK, width=2)
        crop_view = m_res.crop((0, 0, mw, min(780, mh)))
        img.paste(crop_view, (fx, fy), crop_view)

    draw_slide_footer(draw, 1, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_01.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 02: PROBLEMS & EMPIRICAL RESEARCH (AIA+ 3-Tier Layout)
# -------------------------------------------------------------
def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 2, 
        "PROBLEMS & RESEARCH", 
        "Problems & Research | ", 
        "토지개발 시장 실태 조사 및 4대 핵심 문제점 분석", 
        "정보 파편화, 비전문가 접근 장벽, 디지털화 부재, UX 단절과 정량적 사용자 리서치 통계 차트", 
        right_badge=("EMPIRICAL RESEARCH", "green")
    )
    
    # 4 Problem Cards (Row 1 - Exact from User Figma)
    problems = [
        {
            "num": "1",
            "title": "정보의 파편화 및 비표준화",
            "desc": "토지개발에 필요한 정보(지역 특성, 규제, 경제성)가 여러 기관과 플랫폼에 흩어져 있어 사용자마다 수작업 및 추정에 의존하여 정보 비대칭 심화."
        },
        {
            "num": "2",
            "title": "비전문가의 접근 장벽",
            "desc": "지도 기반 분석, 공적 규제 확인, 설계 시뮬레이션, 경제성 분석이 CAD·GIS 등 전문가 도구나 고가 컨설팅에 의존하여 소농·예비창업자 진입 난항."
        },
        {
            "num": "3",
            "title": "디지털화/자동화의 부재",
            "desc": "토지개발 프로세스 전반에 걸쳐 워크플로우 자동화, 시각화 시뮬레이션 도구, 맞춤형 가이드가 부족하여 반복 작업과 시간·비용 낭비 극심."
        },
        {
            "num": "4",
            "title": "사용자 경험(UX)의 단절",
            "desc": "토지 선택, 규제 확인, 시설 설계, 경제성 분석이 각기 별개의 단계로 단절되어 있어 일관된 엔드투엔드 디지털 사용자 경험이 부재함."
        }
    ]
    
    t1_y = 215
    t1_w = 412
    t1_h = 220
    for i, p in enumerate(problems):
        px = 100 + i * (t1_w + 24)
        draw.rounded_rectangle([px, t1_y, px + t1_w, t1_y + t1_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([px + 20, t1_y + 18, px + 50, t1_y + 48], radius=6, fill=BRAND_GREEN)
        draw.text((px + 35, t1_y + 33), p["num"], font=get_font(15, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((px + 62, t1_y + 33), p["title"], font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw.line([(px + 20, t1_y + 60), (px + t1_w - 20, t1_y + 60)], fill=BORDER_LIGHT, width=1)
        
        lines = wrap_text(p["desc"], get_font(12, 'regular'), t1_w - 40, draw)
        ly = t1_y + 75
        for line in lines:
            draw.text((px + 20, ly), line, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 20
            
    # Row 2 (Tier 2): Empirical Research Charts (from User Figma ref_02_research_charts.png)
    t2_y = 455
    t2_w = 1720
    t2_h = 490
    draw.rounded_rectangle([100, t2_y, 100 + t2_w, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    # Header inside chart card
    draw_pill_badge(draw, left_x=130, cy=t2_y + 35, text="EMPIRICAL RESEARCH DATA", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((345, t2_y + 35), "사용자 어려움 지표 및 정보 통합 필요성 설문 데이터 (KCI 연구 및 공공포털 기준)", font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    r_img_path = os.path.join(ASSETS_DIR, "ref_02_research_charts.png")
    if os.path.exists(r_img_path):
        r_img = Image.open(r_img_path).convert('RGBA')
        scale = min((t2_w - 60) / r_img.width, (t2_h - 90) / r_img.height)
        rw = int(r_img.width * scale)
        rh = int(r_img.height * scale)
        r_res = r_img.resize((rw, rh), Image.Resampling.LANCZOS)
        img.paste(r_res, (100 + (t2_w - rw) // 2, t2_y + 70 + (t2_h - 80 - rh) // 2), r_res)

    draw_slide_footer(draw, 2, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_02.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 03: USER PERSONAS & ECOSYSTEM (AIA+ 2-Column Split)
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 3, 
        "USER PERSONAS", 
        "Target Personas | ", 
        "토지개발 플랫폼 2대 타깃 페르소나 및 핵심 니즈", 
        "귀촌 준비 직장인 김도현(35)과 청년 창업가 박예진(28)의 세부 Pain Points 및 Needs 심층 분석", 
        right_badge=("CORE PERSONAS", "green")
    )
    
    # 2 Persona Cards Side-by-Side (from User Figma part_user_personas.png)
    card_w = 848
    card_h = 740
    cy = 220
    
    # Persona 1: 김도현
    c1_x = 100
    draw.rounded_rectangle([c1_x, cy, c1_x + card_w, cy + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c1_x + 30, cy=cy + 40, text="PERSONA 01 · 소농/예비창업", font=get_font(11, 'bold'), theme='green', pad_x=12, height=26)
    draw.text((c1_x + 30, cy + 90), "김도현", font=get_font(26, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c1_x + 120, cy + 94), "35세 / 직장인 (귀촌 준비자)", font=get_font(16, 'medium'), fill=TEXT_LIGHT_SUB)
    draw.text((c1_x + 30, cy + 130), '"귀촌 준비 중인데, 어디서부터 어떻게 시작해야 할지 모르겠어요."', font=get_font(15, 'bold'), fill=BRAND_DARK)
    
    draw.line([(c1_x + 30, cy + 165), (c1_x + card_w - 30, cy + 165)], fill=BORDER_LIGHT, width=1)
    
    # Pain Points
    draw.text((c1_x + 30, cy + 195), "⚠️ 핵심 불편 사항 (Pain Points)", font=get_font(16, 'bold'), fill=(225, 29, 72))
    pains_1 = [
        "개발 가능한 토지인지 확인하기 위해 전문가 컨설팅을 의뢰했으나 비용이 비싸고 답변이 매우 느림",
        "토지이용계획원, 지적도 등 정보를 공공기관별로 하나하나 검색하여 엑셀에 수작업 정리하는 비효율",
        "실제 스마트팜이나 시설을 지었을 때 수익이 날지 객관적 경제성 계산이 안 돼 사업성 판단 불가"
    ]
    py = cy + 230
    for p in pains_1:
        draw.rounded_rectangle([c1_x + 30, py, c1_x + card_w - 30, py + 55], radius=8, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
        draw.text((c1_x + 45, py + 28), "• " + p, font=get_font(12.5, 'regular'), fill=(159, 18, 57), anchor='lm')
        py += 65
        
    # Needs
    draw.text((c1_x + 30, cy + 450), "💡 핵심 요구 가치 (User Needs)", font=get_font(16, 'bold'), fill=BRAND_GREEN)
    needs_1 = [
        "지번 검색 한 번으로 복잡한 공적 규제 정보를 지도 위에 한눈에 시각화하여 확인",
        "토지 개발 가능성과 예상 수익률, 회수 기간을 시스템이 자동으로 계산하여 제시",
        "전문 지식이 없는 초보자도 한 번에 전체 프로세스를 흐름처럼 따라갈 수 있는 가이드"
    ]
    ny = cy + 485
    for n in needs_1:
        draw.rounded_rectangle([c1_x + 30, ny, c1_x + card_w - 30, ny + 55], radius=8, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
        draw.text((c1_x + 45, ny + 28), "✔ " + n, font=get_font(12.5, 'medium'), fill=(6, 95, 70), anchor='lm')
        ny += 65

    # Persona 2: 박예진
    c2_x = 972
    draw.rounded_rectangle([c2_x, cy, c2_x + card_w, cy + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c2_x + 30, cy=cy + 40, text="PERSONA 02 · 청년 스마트팜 창업가", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=26)
    draw.text((c2_x + 30, cy + 90), "박예진", font=get_font(26, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c2_x + 120, cy + 94), "28세 / 청년 농업 창업가", font=get_font(16, 'medium'), fill=TEXT_LIGHT_SUB)
    draw.text((c2_x + 30, cy + 130), '"제가 생각한 온실과 부대시설 배치를 직접 시뮬레이션해보고 싶어요."', font=get_font(15, 'bold'), fill=(37, 99, 235))
    
    draw.line([(c2_x + 30, cy + 165), (c2_x + card_w - 30, cy + 165)], fill=BORDER_LIGHT, width=1)
    
    # Pain Points
    draw.text((c2_x + 30, cy + 195), "⚠️ 핵심 불편 사항 (Pain Points)", font=get_font(16, 'bold'), fill=(225, 29, 72))
    pains_2 = [
        "경사도, 진입로 너비, 용도지역 등 땅을 고르는 기초 단계부터 고려할 변수가 너무 많아 막막함",
        "CAD나 전문 건축 설계 프로그램은 다루기 너무 어려워 종이에 손그림으로 스케치하는 한계",
        "스마트팜 온실 조성비와 재배 작물 연동 생산량 분석을 결국 외부 고가 컨설턴트에 의존"
    ]
    py = cy + 230
    for p in pains_2:
        draw.rounded_rectangle([c2_x + 30, py, c2_x + card_w - 30, py + 55], radius=8, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
        draw.text((c2_x + 45, py + 28), "• " + p, font=get_font(12.5, 'regular'), fill=(159, 18, 57), anchor='lm')
        py += 65
        
    # Needs
    draw.text((c2_x + 30, cy + 450), "💡 핵심 요구 가치 (User Needs)", font=get_font(16, 'bold'), fill=BRAND_GREEN)
    needs_2 = [
        "지도 상에서 스마트팜 규격 모듈을 드래그 앤 드롭으로 직접 배치할 수 있는 인터랙티브 도구",
        "기본 시나리오에 따라 온실 규격, 재배 작물, 설비 옵션을 단계별로 쉽게 진행하는 가이드",
        "토지를 선택하면서 자동으로 법적 인허가 조건과 예상 수익성 지표를 동시에 검증"
    ]
    ny = cy + 485
    for n in needs_2:
        draw.rounded_rectangle([c2_x + 30, ny, c2_x + card_w - 30, ny + 55], radius=8, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
        draw.text((c2_x + 45, ny + 28), "✔ " + n, font=get_font(12.5, 'medium'), fill=(6, 95, 70), anchor='lm')
        ny += 65

    draw_slide_footer(draw, 3, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_03.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 04: USER JOURNEY MAP & STRATEGIC INSIGHTS (AIA+ Style)
# -------------------------------------------------------------
def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 4, 
        "JOURNEY & INSIGHTS", 
        "User Journey & Insights | ", 
        "사용자 6단계 여정 맵 (Journey Map) 및 4대 전략적 인사이트", 
        "인식부터 정보탐색, 토지선택, 규제확인, 설계시도, 분석결과까지의 행동·생각·Pain Point와 해결 전략", 
        right_badge=("USER JOURNEY & INSIGHTS", "green")
    )
    
    # Left: User Journey Map Table (from User Figma part_user_journey_map.png)
    lw = 1040
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="6-STEP END-TO-END JOURNEY MAP", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((365, ly + 35), "사용자 관점의 단계별 행동, Pain Point 및 전환 기회(Opportunity)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    j_path = os.path.join(ASSETS_DIR, "part_user_journey_map.png")
    if os.path.exists(j_path):
        j_img = Image.open(j_path).convert('RGBA')
        scale = min((lw - 40) / j_img.width, (lh - 75) / j_img.height)
        jw = int(j_img.width * scale)
        jh = int(j_img.height * scale)
        j_res = j_img.resize((jw, jh), Image.Resampling.LANCZOS)
        img.paste(j_res, (100 + (lw - jw) // 2, ly + 65 + (lh - 75 - jh) // 2), j_res)

    # Right: 4 Key Strategic Insights (from User Figma ref_04_key_insights.png)
    rx = 1165
    rw = 655
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 35, text="4 CORE STRATEGIC INSIGHTS", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 25, ly + 75), "리서치 기반 4대 디자인 전략", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    insights = [
        ("1. 정보를 하나의 흐름으로 통합", "다양한 공공 플랫폼에 흩어진 토지 규제·인허가·시세를 단일 지도 인터페이스에 집약하여 탐색 피로도 해소"),
        ("2. 규제와 수익성을 쉽게 판단", "복잡한 법령 해석과 수작업 수익 계산 기준을 시스템이 표준화하여 3초 만에 객관적 적합성 도출"),
        ("3. 설계 과정을 시각적으로 시뮬레이션", "전문 CAD 없이도 드래그 앤 드롭으로 스마트팜 온실과 부대시설을 지도상에 직접 배치하는 환경 제공"),
        ("4. 초보자도 따라갈 수 있는 UX 흐름", "정보 탐색, 설계, 경제성 분석, 보고서 생성이 끊기지 않고 물 흐르듯 자연스럽게 이어지는 스텝형 안내")
    ]
    iy = ly + 115
    for title, desc in insights:
        draw.rounded_rectangle([rx + 20, iy, rx + rw - 20, iy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((rx + 35, iy + 30), title, font=get_font(15, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12, 'regular'), rw - 70, draw)
        dy = iy + 60
        for l in lines:
            draw.text((rx + 35, dy), l, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 20
        iy += 148

    draw_slide_footer(draw, 4, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_04.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
