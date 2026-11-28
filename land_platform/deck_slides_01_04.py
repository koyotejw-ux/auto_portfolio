import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 01: HERO COVER (Executive Web SaaS Mockup & Specs)
# -------------------------------------------------------------
def make_slide_01():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    
    # Clean, Spacious Header Tag
    draw_pill_badge(draw, left_x=100, cy=85, text="DUAL PRODUCT: RESPONSIVE LANDING & GIS SIMULATION SAAS", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=26)
    draw.text((545, 85), "FARMINGSYS ENTERPRISE PLATFORM", font=get_font(12, 'bold'), fill=BRAND_GREEN, anchor='lm')
    
    # Left Hero Text Content (w=680) - Strong Typography Hierarchy
    lx = 100
    draw.text((lx, 130), "FARMINGSYS", font=get_font(46, 'black'), fill=(15, 23, 42))
    draw.text((lx + 305, 130), "LAND PLATFORM", font=get_font(46, 'black'), fill=BRAND_GREEN)
    draw.text((lx, 196), "반응형 랜딩페이지 & 4단계 토지개발 타당성 시뮬레이터", font=get_font(20, 'bold'), fill=(51, 65, 85))
    
    desc_kr = (
        "토지 소유주 유입 및 서비스 가치 전달을 위한 '인터랙티브 랜딩페이지'와\n"
        "12대 공공 데이터 기반의 '4단계 엔드투엔드 토지개발 타당성 시뮬레이션 SaaS'를\n"
        "동시에 구축하여, 탐색-분석-설계-금융보고서 발급까지 일관된 반응형 경험을 완성했습니다."
    )
    draw.text((lx, 248), desc_kr, font=get_font(13.5, 'regular'), fill=(100, 116, 139), spacing=6)
    
    # 4 Quantitative Impact Cards - Spacious 2x2 Grid (y=345, h=195)
    stats = [
        ("100+", "분석 가능 토지 규제 조건", "국토계획법 등 100여 개 공적 규제 3초 자동 판정"),
        ("90%", "분석 소요 시간 단축", "기존 14일 수작업 조사를 원터치 실시간 진단으로 단축"),
        ("3~5s", "원터치 시뮬레이션 도출", "지번 입력 즉시 최적 단지 구획 및 시설 조성비 산출"),
        ("40%", "의사결정 정확도 향상", "공공 지적도 및 경제성 모델링 기반 사전 리스크 차단")
    ]
    card_y = 345
    for idx, (val, label, sub) in enumerate(stats):
        cx = lx + (idx % 2) * 350
        cy = card_y + (idx // 2) * 105
        cw, ch = 330, 92
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((cx + 20, cy + 16), val, font=get_num_font(26, 'black'), fill=BRAND_GREEN if idx==0 else (15, 23, 42))
        draw.text((cx + 20, cy + 50), label, font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((cx + 20, cy + 70), sub, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)

    # 2 Product Cores: Landing Page & Multi-Step Simulator (y=575)
    draw.text((lx, 575), "2대 핵심 프로덕트 아키텍처 (Dual Cores)", font=get_font(15, 'bold'), fill=(15, 23, 42))
    
    # Box 1: Landing Page
    draw.rounded_rectangle([lx, 605, lx + 340, 715], radius=12, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=lx + 18, cy=626, text="CORE 01 · 랜딩페이지", font=get_font(10, 'bold'), theme='green', pad_x=8, height=20)
    draw.text((lx + 18, 655), "패럴랙스 스크롤 & 전환 중심 브랜딩", font=get_font(13, 'bold'), fill=BRAND_DARK)
    draw.text((lx + 18, 680), "문제제기 ➔ 솔루션 ➔ 체험 ➔ 후기 ➔ 상담 CTA", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)

    # Box 2: Multi-step Simulator
    draw.rounded_rectangle([lx + 360, 605, lx + 700, 715], radius=12, fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw_pill_badge(draw, left_x=lx + 378, cy=626, text="CORE 02 · 시뮬레이터", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=20)
    draw.text((lx + 378, 655), "GIS 공간 분석 & 자동 사업타당성 엔진", font=get_font(13, 'bold'), fill=(30, 58, 138))
    draw.text((lx + 378, 680), "대상지선택 ➔ 규제진단 ➔ 온실배치 ➔ 금융보고서", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)

    # Project Meta Info Box (Clean 4-Row Grid)
    draw.rounded_rectangle([lx, 735, lx + 700, 955], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    metas = [
        ("프로젝트", "토지개발사업 분석 플랫폼 (반응형 랜딩페이지 및 엔터프라이즈 SaaS)"),
        ("수행 역할", "B2B UX/UI 아키텍처, 인터랙션 설계 및 디자인 시스템 총괄 (100%)"),
        ("반응형 환경", "Desktop (1920px), Tablet (1024px), Mobile (390px) 멀티 브레이크포인트"),
        ("핵심 차별점", "12대 공공 데이터 실시간 파싱 및 3초 인허가/경제성 모델링 자동화")
    ]
    my = 758
    for k, v in metas:
        draw.text((lx + 24, my), k, font=get_font(12, 'bold'), fill=BRAND_GREEN)
        draw.text((lx + 115, my), v, font=get_font(12, 'medium'), fill=TEXT_LIGHT_MAIN)
        my += 48

    # Right: High-Res Real Tablet & Mobile 3D Podium Mockup Composition
    hero_asset = os.path.join(ASSETS_DIR, "figma_hero_mockup_composition.png")
    if os.path.exists(hero_asset):
        hero_im = Image.open(hero_asset).convert('RGBA')
        
        # Exact aspect ratio fit in right zone
        target_w = 980
        target_h = int(target_w * (hero_im.height / hero_im.width))
        hero_x = 840
        hero_y = 120 + (840 - target_h) // 2
        
        # Premium Frameless Clean Mounting with Soft Glass Backdrop
        draw.rounded_rectangle([hero_x - 10, hero_y - 10, hero_x + target_w + 10, hero_y + target_h + 10], radius=24, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=hero_x + 15, cy=hero_y + 15, text="RESPONSIVE PLATFORM ECOSYSTEM", font=get_font(10, 'bold'), theme='green', pad_x=10, height=22)
        draw.text((hero_x + 235, hero_y + 15), "태블릿 웹 & 모바일 동시 시뮬레이션 실물 (Figma 3D Mockup)", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')

        resized_hero = hero_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        img.paste(resized_hero, (hero_x, hero_y + 15), resized_hero)
    else:
        hero_screen = os.path.join(ASSETS_DIR, "screen_hero_dashboard_3128.png")
        draw_browser_mockup(img, hero_screen, x=830, y=120, w=990, h=825, title="FARMINGSYS ENTERPRISE · CORE WORKSPACE", url="https://farmingsys.io/app/dashboard")

    draw_slide_footer(draw, 1, 13, dark_mode=False)
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
    
    # 4 Problem Cards (Row 1)
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
            
    # Row 2: Direct Vector Charts
    t2_y = 455
    t2_w = 848
    t2_h = 495
    
    # Chart 1: Bar Chart (사용자가 가장 어려워하는 과정은?)
    lx = 100
    draw.rounded_rectangle([lx, t2_y, lx + t2_w, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=t2_y + 25, text="EMPIRICAL METRICS", font=get_font(10.5, 'bold'), theme='green', pad_x=10, height=22)
    draw.text((lx + 25, t2_y + 55), "사용자가 가장 어려워하는 토지개발 과정", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + t2_w - 25, t2_y + 58), "(출처: KCI 연구(2014), 서울시 GIS 정책(2011))", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='ra')
    
    bar_items = [
        ("수익성 계산 (사업성)", 4.5, BRAND_GREEN),
        ("인허가 정보 찾기", 4.3, (16, 185, 129)),
        ("설계 툴 사용 (CAD)", 4.1, BRAND_TEAL),
        ("단계 간 흐름 이해 (UX)", 4.0, (71, 85, 105))
    ]
    
    bar_base_y = t2_y + 400
    bar_max_h = 240
    bw = 120
    for idx, (b_label, b_val, b_col) in enumerate(bar_items):
        bx = lx + 80 + idx * 180
        bh = int(bar_max_h * (b_val / 5.0))
        draw.rounded_rectangle([bx, bar_base_y - bar_max_h, bx + bw, bar_base_y], radius=8, fill=(241, 245, 249))
        draw.rounded_rectangle([bx, bar_base_y - bh, bx + bw, bar_base_y], radius=8, fill=b_col)
        draw.text((bx + bw//2, bar_base_y - bh - 16), f"{b_val}", font=get_num_font(16, 'bold'), fill=b_col, anchor='mm')
        draw.text((bx + bw//2, bar_base_y + 24), b_label, font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
        draw.text((bx + bw//2, bar_base_y + 45), f"5점 만점 중 {b_val}점", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')

    # Chart 2: Donut Chart
    rx = 972
    draw.rounded_rectangle([rx, t2_y, rx + t2_w, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=t2_y + 25, text="MARKET SURVEY", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((rx + 25, t2_y + 55), "정보 파편화 원인 및 통합 필요성 비중", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((rx + t2_w - 25, t2_y + 58), "(출처: 공공데이터포털, 토지이음, CAD 포럼)", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='ra')
    
    pie_cx, pie_cy, pie_r = rx + 190, t2_y + 245, 120
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=0, end=108, fill=BRAND_GREEN)
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=108, end=198, fill=(99, 102, 241))
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=198, end=270, fill=(51, 65, 85))
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=270, end=360, fill=BRAND_TEAL)
    draw.ellipse([pie_cx - 55, pie_cy - 55, pie_cx + 55, pie_cy + 55], fill=CARD_LIGHT)
    draw.text((pie_cx, pie_cy - 10), "통합 수요", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((pie_cx, pie_cy + 12), "100%", font=get_num_font(15, 'bold'), fill=BRAND_GREEN, anchor='mm')
    
    pie_legends = [
        ("수익성 계산 (자동화)", "30%", BRAND_GREEN, "복잡한 세무, 보조금, IRR/NPV 연산"),
        ("규제 정보 (공적장부)", "25%", (99, 102, 241), "토지이용계획 및 조례 인허가 판별"),
        ("지역 특성 (입지/도로)", "20%", (51, 65, 85), "접도 조건, 경사도, 고도 분석"),
        ("설계 도면 (배치/CAD)", "25%", BRAND_TEAL, "온실 규격 및 부대시설 구획")
    ]
    leg_y = t2_y + 115
    for l_title, l_pct, l_col, l_sub in pie_legends:
        draw.rounded_rectangle([rx + 360, leg_y, rx + t2_w - 30, leg_y + 70], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([rx + 375, leg_y + 15, rx + 395, leg_y + 35], radius=4, fill=l_col)
        draw.text((rx + 410, leg_y + 25), l_title, font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw.text((rx + t2_w - 50, leg_y + 25), l_pct, font=get_num_font(16, 'bold'), fill=l_col, anchor='rm')
        draw.text((rx + 410, leg_y + 48), l_sub, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB, anchor='lm')
        leg_y += 82

    draw.rounded_rectangle([rx + 25, t2_y + 440, rx + t2_w - 25, t2_y + 485], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((rx + 40, t2_y + 462), "💡 리서치 결론: 4개 영역이 분절되어 있어, 단일 SaaS 플랫폼으로의 통합 요구가 100%에 달함", font=get_font(12, 'bold'), fill=BRAND_DARK, anchor='lm')

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
# SLIDE 04: USER JOURNEY MAP & STRATEGIC INSIGHTS (AIA+ Style Direct Drawing)
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
    
    lw = 1060
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=130, cy=ly + 32, text="6-STEP END-TO-END JOURNEY MAP", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((365, ly + 32), "사용자 관점의 단계별 행동, Pain Point 및 전환 기회(Opportunity)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    cols = ["구분", "01. 인식", "02. 정보 탐색", "03. 토지 선택", "04. 규제 확인", "05. 설계 시도", "06. 타당성 평가"]
    col_widths = [100, 155, 155, 155, 155, 155, 155]
    
    gx = 125
    gy = ly + 65
    
    cur_x = gx
    for idx, (c_name, c_w) in enumerate(zip(cols, col_widths)):
        fill_col = BRAND_GREEN if idx > 0 else (241, 245, 249)
        text_col = (255, 255, 255) if idx > 0 else TEXT_LIGHT_MAIN
        draw.rounded_rectangle([cur_x, gy, cur_x + c_w, gy + 34], radius=6, fill=fill_col)
        draw.text((cur_x + c_w//2, gy + 17), c_name, font=get_font(11, 'bold'), fill=text_col, anchor='mm')
        cur_x += c_w + 5
        
    journey_rows = [
        ("행동 (Behavior)", [
            "유튜브, 블로그, 귀촌 사례 검색",
            "포털, 지자체 공고, 토지정보 비교",
            "지도 보며 위치 탐색, 네이버/공공정보 비교",
            "지자체 전화 문의, 인터넷 규제 검색",
            "엑셀에 수작업 배치, 손그림 구상",
            "컨설턴트 의뢰, 세무사/시공사 견적"
        ], (248, 250, 252)),
        ("생각 (Thoughts)", [
            "나도 가능할까? 어디서 시작하지?",
            "필요한 게 너무 많고 용어가 어렵다",
            "여기가 정말 괜찮고 합법적인 땅인가?",
            "도대체 무슨 규제이고 건폐율이 얼마지?",
            "그림은 그렸는데 이게 시공 가능한가?",
            "초기 투자비 회수까지 몇 년 걸리지?"
        ], (255, 255, 255)),
        ("불편 (Pain Point)", [
            "귀촌 사례마다 정보가 제각각이라 혼란",
            "정보가 분산되어 비교 기준이 전무",
            "경사도, 진입로, 용도 파악 극심한 난이도",
            "용도지역, 건폐율 등 법적 용어가 난해함",
            "실제 시도해도 기준도 없고 반영 불가",
            "컨설팅 비용이 비싸고 결과도 불투명"
        ], (255, 241, 242)),
        ("요구 (Needs)", [
            "내 상황에 맞는 맞춤형 가이드라인",
            "한눈에 비교 가능한 통합 정보 탐색 도구",
            "기초 조건 자동 분석 및 초보자 해설",
            "시각화된 규제 요약 뷰 및 등급 표시",
            "간단한 인터랙티브 설계 시뮬레이션",
            "원클릭 사업성 분석 및 은행 제출 리포트"
        ], (240, 253, 244)),
        ("기회 (Opportunity)", [
            "온보딩 맞춤 설문 & 유형별 시나리오 제공",
            "지도 기반 통합 뷰 + 원터치 필터 검색",
            "개발 적합도 자동 진단 및 요약 뱃지",
            "지도 기반 규제 레이어 + 3초 해석 카드",
            "드래그 앤 드롭 스마트팜 배치 + 최적 가이드",
            "원클릭 20p 금융/기술 종합 보고서 PDF 생성"
        ], (239, 246, 255))
    ]
    
    r_y = gy + 42
    r_h = 118
    for r_label, r_vals, r_bg in journey_rows:
        draw.rounded_rectangle([gx, r_y, gx + col_widths[0], r_y + r_h], radius=6, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
        r_title_col = (225, 29, 72) if "Pain" in r_label else (BRAND_DARK if "Needs" in r_label else (BRAND_TEAL if "기회" in r_label else TEXT_LIGHT_MAIN))
        draw.text((gx + col_widths[0]//2, r_y + r_h//2), r_label, font=get_font(11, 'bold'), fill=r_title_col, anchor='mm')
        
        cur_x = gx + col_widths[0] + 5
        for v_idx, val_text in enumerate(r_vals):
            c_w = col_widths[v_idx + 1]
            draw.rounded_rectangle([cur_x, r_y, cur_x + c_w, r_y + r_h], radius=6, fill=r_bg, outline=BORDER_LIGHT, width=1)
            lines = wrap_text(val_text, get_font(10.5, 'regular'), c_w - 14, draw)
            vy = r_y + (r_h - len(lines)*16)//2
            for l in lines:
                draw.text((cur_x + c_w//2, vy), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_MAIN, anchor='mm')
                vy += 16
            cur_x += c_w + 5
        r_y += r_h + 6

    # Right: 4 Key Strategic Insights
    rx = 1185
    rw = 635
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 32, text="4 CORE STRATEGIC INSIGHTS", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 25, ly + 72), "리서치 기반 4대 디자인 전략", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    
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
