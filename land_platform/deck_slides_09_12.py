import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 09: CORE FEATURE · STEP 2 · SMARTFARM FACILITY SIMULATION (Figma sec_04, sec_05 & Mobile)
# -------------------------------------------------------------
def make_slide_09():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 9, 
        "CORE FEATURE · STEP 2", 
        "Simulation Step 2 | ", 
        "STEP 2. 시설 배치 & 스마트팜 설계 데스크톱 및 모바일 화면 (Figma UI 실물)", 
        "피그마 공식 UI 원본: [1] 데스크톱 온실 규격 선택 & 부지 배치(sec_04)  |  [2] 모바일 스마트팜 종류 선택(비닐/유리/수직농장) 적응형 UI", 
        right_badge=("OFFICIAL FIGMA UI", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # 3-Zone Architecture matching Slide 07:
    # Zone 1 (Left Card, w=450, x=100): Core Specs & Decision Logic
    # Zone 2 (Middle Card, w=880, x=560): Desktop Web Browser Mockup (sec_04 온실배치 시뮬레이터)
    # Zone 3 (Right Card, w=340, x=1480): Mobile Phone Mockup (피그마 원본 모바일 스마트팜 설계 화면)
    
    # =========================================================================
    # ZONE 1: LEFT SPECS CARD (w=450, x=100)
    # =========================================================================
    lx, lw = 100, 450
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="STEP 2 · FACILITY & CROPS", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 68), "시설배치 & 스마트팜 설계 UI", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 25, card_y + 92), "온실 모듈 규격 선택 및 스마트팜 종류별 다면 설계", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)

    step2_specs = [
        ("01. 온실 모듈 규격 최적화 (sec_04)", "비닐온실(단동/연동형), 플라스틱 온실, 유리온실, 수직농장 등 부지 형상에 맞춘 자동 구획 및 최적 정렬"),
        ("02. 스마트팜 다중 종류 선택 (모바일 UI)", "스마트팜 1, 스마트팜 2로 분할 구획하여 복합 영농 단지(비닐+유리온실 연계)를 원클릭으로 선택/비교"),
        ("03. 에너지 시설 & 재배 작물 연동", "지열·태양광 연계 에너지 시설, 딸기·파프리카 재배 작물 주기와 결합하여 유효 생산 면적 및 연간 생산량 도출")
    ]
    
    sy = card_y + 118
    for s_title, s_desc in step2_specs:
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
    draw.text((lx + 40, card_y + 586), "💡 STEP 2 핵심 설계 전략 및 가치", font=get_font(12.5, 'bold'), fill=BRAND_DARK)
    val_desc = "비전문가 농민도 CAD 도면 없이 '온실 모듈 클릭 ➔ 필지 자동 스케일링 ➔ 생산량 시뮬레이션'으로 즉시 이어지도록 모바일과 데스크톱 환경 모두에서 직관적인 칩 선택 인터페이스를 구현했습니다."
    lines_val = wrap_text(val_desc, get_font(10.5, 'regular'), lw - 70, draw)
    vy = card_y + 610
    for l in lines_val:
        draw.text((lx + 40, vy), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_MAIN)
        vy += 17

    # =========================================================================
    # ZONE 2: DESKTOP WEB BROWSER MOCKUP (w=880, x=560)
    # =========================================================================
    mx, mw = 560, 880
    draw.rounded_rectangle([mx, card_y, mx + mw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=mx + 25, cy=card_y + 35, text="DESKTOP VIEW (1920px)", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((mx + 215, card_y + 35), "피그마 공식 데스크톱 화면 (STEP 2-1 시설배치 시뮬레이터 sec_04)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    desk_asset = os.path.join(ASSETS_DIR, "figma_screen_sec_04.png")
    desk_im = Image.open(desk_asset)
    desk_vp_w = mw - 40 - 4
    desk_vp_h = int(desk_vp_w * (desk_im.height / desk_im.width))
    desk_total_h = 36 + 2 + desk_vp_h
    desk_y = card_y + 75 + (card_h - 95 - desk_total_h) // 2
    draw_browser_mockup(img, desk_asset, x=mx + 20, y=desk_y, w=mw - 40, h=desk_total_h, title="FARMINGSYS ENTERPRISE · STEP 2 FACILITY LAYOUT SIMULATOR (DESKTOP)", url="https://farmingsys.io/app/step-02-facility")

    # =========================================================================
    # ZONE 3: MOBILE PHONE MOCKUP (w=340, x=1480)
    # =========================================================================
    rx, rw = 1480, 340
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=card_y + 35, text="MOBILE VIEW (390px)", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 195, card_y + 35), "스마트팜 설계 모바일 UI", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    mob_asset = os.path.join(ASSETS_DIR, "figma_step4_smartfarm_mobile.png")
    draw_phone_mockup(img, mob_asset, cx=rx + rw//2, cy=card_y + 75 + (card_h - 95)//2, target_h=640, bezel=7, radius=28)

    draw_slide_footer(draw, 9, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_09.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 10: CORE FEATURE · STEP 3 · CONSTRUCTION COST & FINANCIAL MODELING
# -------------------------------------------------------------
def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 10, 
        "CORE FEATURE · STEP 3", 
        "Simulation Step 3 | ", 
        "STEP 3. 조성비 설계 데스크톱 및 모바일 화면 (Figma UI 실물)", 
        "피그마 공식 UI 원본: [1] 데스크톱 기본시설·조사설계·시설조성비 4분할 테이블(1024x722)  |  [2] 모바일 표준값 적용 토글 & 전용면적별 조성비 산출 UI", 
        right_badge=("OFFICIAL FIGMA UI", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # 3-Zone Architecture matching Slide 07 & Slide 09:
    # Zone 1 (Left Card, w=450, x=100): Core Specs & Decision Logic
    # Zone 2 (Middle Card, w=880, x=560): Desktop Web Browser Mockup (피그마 원본 조성비 설계 화면)
    # Zone 3 (Right Card, w=340, x=1480): Mobile Phone Mockup (피그마 원본 모바일 조성비 설계 화면)
    
    # =========================================================================
    # ZONE 1: LEFT SPECS CARD (w=450, x=100)
    # =========================================================================
    lx, lw = 100, 450
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="STEP 3 · CONSTRUCTION COST", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 68), "조성비 설계 & CAPEX 모델 UI", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 25, card_y + 92), "한국토지주택공사(LH) 표준건축비 연동 공사비 산출", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)

    step3_specs = [
        ("01. 표준건축비 연동 자동 산출", "한국토지주택공사(LH) 표준건축비 DB와 연동하여 기본공사비, 건축공사비, 우수공, 가로등공을 원클릭으로 자동 계산"),
        ("02. 전항목 표준값 원클릭 토글", "체크박스 선택 및 [전항목 표준값 사용] 원클릭 토글을 통해 비전문가도 복잡한 내역 입력 없이 예상 조성비(총 23.6억) 즉시 산출"),
        ("03. 조사설계비 & 세부항목 커스텀", "토목/지질 조사설계비, 부대비, 시설조성비 항목을 자유롭게 추가(+항목 추가하기) 및 단위공사비(원/㎡) 수동 보정 지원")
    ]
    cy = card_y + 118
    for title, desc in step3_specs:
        draw.rounded_rectangle([lx + 25, cy, lx + lw - 25, cy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, cy + 22), title, font=get_font(13.5, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(11, 'regular'), lw - 70, draw)
        dy = cy + 46
        for l in lines:
            draw.text((lx + 40, dy), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        cy += 144

    # Bottom Key Metric Callout in Left Card
    draw.rounded_rectangle([lx + 25, card_y + 565, lx + lw - 25, card_y + 715], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((lx + 40, card_y + 586), "💡 STEP 3 핵심 설계 전략 및 가치", font=get_font(12.5, 'bold'), fill=BRAND_DARK)
    val_desc = "수백 페이지에 달하는 복잡한 적산 내역서를 웹과 모바일에서 'LH 표준 단가 기반 4개 블록 테이블'로 압축하여, 시공 견적 조율 시 발생하는 비용 거품과 정보 비대칭을 100% 해소했습니다."
    lines_val = wrap_text(val_desc, get_font(10.5, 'regular'), lw - 70, draw)
    vy = card_y + 610
    for l in lines_val:
        draw.text((lx + 40, vy), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_MAIN)
        vy += 17

    # =========================================================================
    # ZONE 2: DESKTOP WEB BROWSER MOCKUP (w=880, x=560)
    # =========================================================================
    mx, mw = 560, 880
    draw.rounded_rectangle([mx, card_y, mx + mw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=mx + 25, cy=card_y + 35, text="DESKTOP VIEW (1920px)", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((mx + 215, card_y + 35), "피그마 공식 데스크톱 화면 (STEP 5 조성비 설계 4분할 테이블)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    desk_asset = os.path.join(ASSETS_DIR, "figma_step5_construction_cost_desktop.png")
    desk_im = Image.open(desk_asset)
    desk_vp_w = mw - 40 - 4
    desk_vp_h = int(desk_vp_w * (desk_im.height / desk_im.width))
    desk_total_h = 36 + 2 + desk_vp_h
    desk_y = card_y + 75 + (card_h - 95 - desk_total_h) // 2
    draw_browser_mockup(img, desk_asset, x=mx + 20, y=desk_y, w=mw - 40, h=desk_total_h, title="FARMINGSYS ENTERPRISE · STEP 5 CONSTRUCTION COST ENGINE (DESKTOP)", url="https://farmingsys.io/app/step-05-construction-cost")

    # =========================================================================
    # ZONE 3: MOBILE PHONE MOCKUP (w=340, x=1480)
    # =========================================================================
    rx, rw = 1480, 340
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=card_y + 35, text="MOBILE VIEW (390px)", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 195, card_y + 35), "조성비 설계 모바일 UI", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    mob_asset = os.path.join(ASSETS_DIR, "figma_step5_construction_cost_mobile.png")
    draw_phone_mockup(img, mob_asset, cx=rx + rw//2, cy=card_y + 75 + (card_h - 95)//2, target_h=640, bezel=7, radius=28)

    draw_slide_footer(draw, 10, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_10.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 11: CORE FEATURE · STEP 4 · REVENUE & SIMULATION REPORT (Figma Step 7 & Report)
# -------------------------------------------------------------
def make_slide_11():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 11, 
        "CORE FEATURE · STEP 4", 
        "Simulation Step 4 | ", 
        "STEP 4. 운영비(OPEX)·판관비 설계 및 최종 시뮬레이션 분석 보고서 (Figma UI 실물)", 
        "피그마 공식 UI 원본 2종: [1] 데스크톱 중간재비·판관비·인건비 최저시급 연동 화면(1024x576)  |  [2] 최종 시뮬레이션 분석 보고서 풀페이지 뷰어(379x1024)", 
        right_badge=("OFFICIAL FIGMA UI 2-PART", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # 3-Zone Architecture:
    # Zone 1 (Left Card, w=440, x=80): Core Specs & Feasibility Report Decision Logic
    # Zone 2 (Middle Card, w=840, x=540): Desktop Browser STEP 7 중간재비·판관비·인건비 설정 (1024x576)
    # Zone 3 (Right Card, w=440, x=1400): Final Simulation Analysis Report Full-Page Mockup (379x1024)
    
    # =========================================================================
    # ZONE 1: LEFT SPECS CARD (w=440, x=80)
    # =========================================================================
    lx, lw = 80, 440
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="STEP 4 · OPEX & FINAL REPORT", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 68), "운영비 설계 & 종합 리포트 UI", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 25, card_y + 92), "최저시급 인건비 연동 & 금융 심사용 다면 보고서 완성", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)

    step4_specs = [
        ("01. 중간재비 & 판관비 표준값 토글", "비료, 농약 등 중간재비와 우수공·가로등공 판관비 항목별 단위비용(원/㎡)을 표준값 원클릭 토글로 자동 보정 및 총 236억 검증"),
        ("02. 국가 최저시급 연동 운영비 산출", "가공유통시설 투입인원(47명) 및 1인 연봉을 국가 최저시급 기준 공공 DB와 연동하여 실제 운영 단계의 고정비 투명성 확보"),
        ("03. 원클릭 시뮬레이션 분석 보고서", "토지 지적도, 법률 규제, 연차별 현금흐름(IRR/ROI), 시설배치 조감도가 망라된 금융 표준 분석 보고서 실시간 발급")
    ]
    cy = card_y + 118
    for title, desc in step4_specs:
        draw.rounded_rectangle([lx + 25, cy, lx + lw - 25, cy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, cy + 22), title, font=get_font(13.5, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(11, 'regular'), lw - 70, draw)
        dy = cy + 46
        for l in lines:
            draw.text((lx + 40, dy), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        cy += 144

    # Bottom Key Metric Callout in Left Card
    draw.rounded_rectangle([lx + 25, card_y + 565, lx + lw - 25, card_y + 715], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((lx + 40, card_y + 586), "💡 STEP 4 핵심 설계 전략 및 가치", font=get_font(12.5, 'bold'), fill=BRAND_DARK)
    val_desc = "단순한 계산기를 넘어 국가 공공 데이터 기반의 정밀 적산과 실제 대출 심사용 '시뮬레이션 분석 보고서'를 단일 파이프라인으로 연결하여, 사업 기획부터 금융 승인까지의 리드타임을 90% 이상 단축했습니다."
    lines_val = wrap_text(val_desc, get_font(10.5, 'regular'), lw - 70, draw)
    vy = card_y + 610
    for l in lines_val:
        draw.text((lx + 40, vy), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_MAIN)
        vy += 17

    # =========================================================================
    # ZONE 2: DESKTOP BROWSER [STEP 7] 중간재비 & 운영비/판관비 (w=840, x=540)
    # =========================================================================
    m1_x, m1_w = 540, 840
    draw.rounded_rectangle([m1_x, card_y, m1_x + m1_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=m1_x + 25, cy=card_y + 35, text="DESKTOP VIEW (1920px)", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((m1_x + 215, card_y + 35), "피그마 공식 데스크톱 화면 (STEP 7 중간재비·판관비·운영비 설정)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    asset1 = os.path.join(ASSETS_DIR, "figma_step7_revenue_part2_desktop.png")
    im1 = Image.open(asset1)
    vp1_w = m1_w - 40 - 4
    vp1_h = int(vp1_w * (im1.height / im1.width))
    tot1_h = 36 + 2 + vp1_h
    b1_y = card_y + 75 + (card_h - 95 - tot1_h) // 2
    draw_browser_mockup(img, asset1, x=m1_x + 20, y=b1_y, w=m1_w - 40, h=tot1_h, title="FARMINGSYS ENTERPRISE · STEP 7 OPEX & OPERATING COST ENGINE", url="https://farmingsys.io/app/step-07-opex")

    # =========================================================================
    # ZONE 3: FINAL SIMULATION REPORT FULL-PAGE VIEWER (w=440, x=1400)
    # =========================================================================
    m2_x, m2_w = 1400, 440
    draw.rounded_rectangle([m2_x, card_y, m2_x + m2_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=m2_x + 25, cy=card_y + 35, text="FINAL REPORT VIEW", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((m2_x + 195, card_y + 35), "시뮬레이션 분석 보고서 (Figma 실물)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    rep_asset = os.path.join(ASSETS_DIR, "figma_step8_simulation_report_full.jpg")
    rep_im = Image.open(rep_asset)
    
    # Calculate zero-distortion dimensions for the full report page viewer
    target_rep_h = 640
    rep_vp_h = target_rep_h - 36 - 2
    rep_vp_w = int(rep_vp_h * (rep_im.width / rep_im.height))
    tot_rep_w = rep_vp_w + 4
    
    rep_cx = m2_x + m2_w // 2
    rep_x = rep_cx - tot_rep_w // 2
    rep_y = card_y + 75 + (card_h - 95 - target_rep_h) // 2
    
    draw_browser_mockup(img, rep_asset, x=rep_x, y=rep_y, w=tot_rep_w, h=target_rep_h, title="SIMULATION VALUATION REPORT (FULL)", url="https://farmingsys.io/report/valuation-summary.pdf")

    draw_slide_footer(draw, 11, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_11.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 12: CORE FEATURE · SIMULATION ARCHIVE & HISTORY (Figma UI 실물)
# -------------------------------------------------------------
# -------------------------------------------------------------
# SLIDE 12: SIMULATION ARCHIVE & PROJECT RETROSPECTIVE (AIA+ Style STAR)
# -------------------------------------------------------------
def make_slide_12():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 12, 
        "ARCHIVE & RETROSPECTIVE", 
        "Project Retrospective | ", 
        "시뮬레이션 내역 관리 실물 화면 및 STAR 기법 성과 회고", 
        "피그마 공식 시뮬레이션 내역 조회(데스크톱 그리드 + 모바일 카드) 실물 탑재 및 인허가 90% 단축 시니어 UX 전략 기술 회고", 
        right_badge=("PROJECT RETROSPECTIVE", "green")
    )
    
    # 2-Tier Architecture:
    # Tier 1 (Top Half, y=215, h=395): Figma Simulation History & Archive UI (Desktop w=1080 + Mobile w=600)
    # Tier 2 (Bottom Half, y=625, h=335): 4 Quantitative Metrics + STAR Senior UX Retrospective
    
    # =========================================================================
    # TIER 1: SIMULATION ARCHIVE & HISTORY (TOP HALF, y=215, h=395)
    # =========================================================================
    t1_y = 215
    t1_h = 395
    
    # Left Box: Desktop Data Grid Mockup (w=1120, x=100)
    d_x, d_w = 100, 1120
    draw.rounded_rectangle([d_x, t1_y, d_x + d_w, t1_y + t1_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=d_x + 25, cy=t1_y + 30, text="SIMULATION ARCHIVE · DESKTOP GRID", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((d_x + 285, t1_y + 30), "시뮬레이션 내역 조회 데이터 그리드 (Figma 실물)", font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    desk_asset = os.path.join(ASSETS_DIR, "figma_simulation_history_desktop.png")
    desk_im = Image.open(desk_asset)
    desk_vp_w = d_w - 40 - 4
    desk_vp_h = int(desk_vp_w * (desk_im.height / desk_im.width))
    desk_tot_h = 36 + 2 + desk_vp_h
    desk_y = t1_y + 55
    draw_browser_mockup(img, desk_asset, x=d_x + 20, y=desk_y, w=d_w - 40, h=desk_tot_h, title="FARMINGSYS ENTERPRISE · SIMULATION HISTORY & ARCHIVE (1024x576)", url="https://farmingsys.io/app/simulation-history")
    
    # Right Box: Mobile History Card Mockup + Key Highlights (w=580, x=1240)
    m_x, m_w = 1240, 580
    draw.rounded_rectangle([m_x, t1_y, m_x + m_w, t1_y + t1_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=m_x + 25, cy=t1_y + 30, text="MOBILE VIEW", font=get_font(10, 'bold'), theme='green', pad_x=10, height=22)
    draw.text((m_x + 145, t1_y + 30), "모바일 내역 카드 뷰 (Figma 실물)", font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    # Phone mockup positioned inside right box
    mob_asset = os.path.join(ASSETS_DIR, "figma_simulation_history_mobile.png")
    draw_phone_mockup(img, mob_asset, cx=m_x + 120, cy=t1_y + 225, target_h=320, bezel=5, radius=18)
    
    # Side Specs in Right Box
    sp_x = m_x + 230
    sp_w = m_w - 250
    specs_h = [
        ("01. 다면 재무 지표 즉시 대조", "총면적(790㎡), 품목(딸기·버터헤드), 총 조성비(2.89억), 회수기간(3년) 단일 행 대조"),
        ("02. 실시간 검색 & 스마트 페이징", "지번·작물명 키워드 검색 인풋 및 10개 단위 페이지네이션"),
        ("03. 프로젝트 지속적 자산화", "토지 매수 조건 변경 시 이전 시뮬레이션을 즉시 재호출·수정 지원")
    ]
    sy_cur = t1_y + 70
    for s_title, s_desc in specs_h:
        draw.rounded_rectangle([sp_x, sy_cur, sp_x + sp_w, sy_cur + 92], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((sp_x + 14, sy_cur + 16), s_title, font=get_font(11.5, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(s_desc, get_font(10.5, 'regular'), sp_w - 28, draw)
        ly = sy_cur + 38
        for l in lines:
            draw.text((sp_x + 14, ly), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 16
        sy_cur += 102

    # =========================================================================
    # TIER 2: OUTCOMES & STAR RETROSPECTIVE (BOTTOM HALF, y=625, h=335)
    # =========================================================================
    t2_y = 625
    t2_h = 335
    
    # 4 Quantitative Metrics along top of Tier 2
    metrics = [
        ("100+", "분석 가능 토지 규제 조건", "국토계획법 등 100여 개 공공 규제 자동 매칭"),
        ("90%", "분석 소요 시간 단축", "기존 14일 수작업 조사를 3~5초로 단축"),
        ("3~5s", "원터치 시뮬레이션 도출", "지번 입력 즉시 시설 구획 및 공사비 산출"),
        ("40%", "의사결정 정확도 향상", "정량 데이터 기반 사전 투자 리스크 차단")
    ]
    mw = 310
    for idx, (m_val, m_title, m_desc) in enumerate(metrics):
        mx = 100 + idx * (mw + 20)
        draw.rounded_rectangle([mx, t2_y, mx + mw, t2_y + 85], radius=12, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw.text((mx + 18, t2_y + 14), m_val, font=get_num_font(26, 'black'), fill=BRAND_GREEN if idx==0 else (15, 23, 42))
        draw.text((mx + 18, t2_y + 48), m_title, font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((mx + 18, t2_y + 66), m_desc, font=get_font(9.5, 'regular'), fill=TEXT_LIGHT_SUB)

    # STAR Method Senior UX Retrospective Box (y = t2_y + 100, h = 230)
    star_y = t2_y + 100
    star_w = 1720
    star_h = 235
    draw.rounded_rectangle([100, star_y, 100 + star_w, star_y + star_h], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=125, cy=star_y + 24, text="SENIOR UX STRATEGY RETROSPECTIVE (STAR)", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=22)
    draw.text((125, star_y + 54), "공간 GIS와 금융 데이터가 융합된 복잡계를 직관적 디지털 경험으로 전환한 여정", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    star_items = [
        ("Situation (상황)", "공간 지적도, 수많은 지자체 조례, 복잡한 인허가 법률, 대규모 자금 조달이 얽혀 있어 정보 비대칭이 극심하고 비전문가 토지주의 진입 장벽이 높았습니다."),
        ("Task (과제)", "복잡한 법률·규제 데이터를 학습 없이 이해할 수 있는 단일 워크플로우를 구축하고, 대상지 선택부터 경제성 타당성 보고서 출력까지 원스톱으로 지원해야 했습니다."),
        ("Action (실행)", "좌측 컨트롤 패널과 우측 인터랙티브 GIS의 듀얼 스플릿 뷰를 설계하고, 12대 공공 데이터를 3단계 계층으로 정제하여 개발 불가 구역을 명확히 시각화했습니다."),
        ("Result (성과)", "기존 2주 소요되던 토지 타당성 분석 기간을 3~5초로 90% 단축했으며, 토지주-개발사-투자사 간 신뢰 기반 협업 플랫폼을 성공적으로 완성했습니다.")
    ]
    
    # 4 Columns for STAR
    sc_w = (star_w - 60 - 3 * 20) // 4
    for s_idx, (s_tag, s_text) in enumerate(star_items):
        sc_x = 125 + s_idx * (sc_w + 20)
        draw.rounded_rectangle([sc_x, star_y + 75, sc_x + sc_w, star_y + star_h - 18], radius=10, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw.text((sc_x + 14, star_y + 90), s_tag, font=get_font(12, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(s_text, get_font(10.5, 'regular'), sc_w - 28, draw)
        ly = star_y + 115
        for l in lines:
            draw.text((sc_x + 14, ly), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 16

    draw_slide_footer(draw, 12, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_12.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")
