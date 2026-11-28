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

    draw_slide_footer(draw, 11, 13, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_11.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 12: CORE FEATURE · SIMULATION ARCHIVE & HISTORY (Figma UI 실물)
# -------------------------------------------------------------
def make_slide_12():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 12, 
        "SIMULATION ARCHIVE", 
        "Simulation History | ", 
        "시뮬레이션 내역 조회 데스크톱 및 모바일 화면 (Figma UI 실물)", 
        "피그마 공식 UI 원본: [1] 데스크톱 시뮬레이션명·장소·면적·작물·조성비·NPV·IRR·회수기간 데이터 그리드(1024x576)  |  [2] 모바일 내역 카드 뷰", 
        right_badge=("OFFICIAL FIGMA UI", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # 3-Zone Architecture:
    # Zone 1 (Left Card, w=440, x=80): Core Specs & Project Archive Management
    # Zone 2 (Middle Card, w=840, x=540): Desktop Simulation History Data Grid (1024x576)
    # Zone 3 (Right Card, w=440, x=1400): Mobile Simulation History Card View (420x1024)
    
    # =========================================================================
    # ZONE 1: LEFT SPECS CARD (w=440, x=80)
    # =========================================================================
    lx, lw = 80, 440
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="SIMULATION ARCHIVE & AUDIT", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 68), "시뮬레이션 내역 관리 UI", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 25, card_y + 92), "진행 프로젝트 전수 보관 & 다면 재무 지표 즉시 비교", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)

    specs = [
        ("01. 다차원 재무 지표 한눈에 비교", "시뮬레이션명, 장소, 총면적(790㎡), 품목(딸기·버터헤드), 총 조성비(2.89억), NPV, IRR, 투자회수기간(3년)을 단일 테이블에서 대조"),
        ("02. 실시간 검색 & 스마트 페이징", "지번, 대상지명, 작물명 키워드 검색 인풋 및 10개 단위 페이지네이션을 지원하여 수백 건의 시뮬레이션 이력 초고속 탐색"),
        ("03. 모바일 최적화 반응형 카드 리스트", "모바일 화면에서는 복잡한 8컬럼 테이블을 세로형 요약 카드로 재구성하여 현장 실사 중에도 스마트폰으로 이전 분석 데이터 원터치 열람")
    ]
    cy = card_y + 118
    for title, desc in specs:
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
    draw.text((lx + 40, card_y + 586), "💡 지속적 프로젝트 자산화 가치", font=get_font(12.5, 'bold'), fill=BRAND_DARK)
    val_desc = "단발성 시뮬레이션으로 끝나지 않고, 토지 매수 및 개발 조건 변경 시 과거 분석 프로젝트를 즉시 재호출·수정하여 다자간(토지주-시공사-금융기관) 의사결정 속도를 극대화합니다."
    lines_val = wrap_text(val_desc, get_font(10.5, 'regular'), lw - 70, draw)
    vy = card_y + 610
    for l in lines_val:
        draw.text((lx + 40, vy), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_MAIN)
        vy += 17

    # =========================================================================
    # ZONE 2: DESKTOP SIMULATION HISTORY BROWSER (w=840, x=540)
    # =========================================================================
    m1_x, m1_w = 540, 840
    draw.rounded_rectangle([m1_x, card_y, m1_x + m1_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=m1_x + 25, cy=card_y + 35, text="DESKTOP VIEW (1920px)", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((m1_x + 215, card_y + 35), "피그마 공식 데스크톱 화면 (시뮬레이션 내역 조회 데이터 그리드)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    asset1 = os.path.join(ASSETS_DIR, "figma_simulation_history_desktop.png")
    im1 = Image.open(asset1)
    vp1_w = m1_w - 40 - 4
    vp1_h = int(vp1_w * (im1.height / im1.width))
    tot1_h = 36 + 2 + vp1_h
    b1_y = card_y + 75 + (card_h - 95 - tot1_h) // 2
    draw_browser_mockup(img, asset1, x=m1_x + 20, y=b1_y, w=m1_w - 40, h=tot1_h, title="FARMINGSYS ENTERPRISE · SIMULATION HISTORY & ARCHIVE (DESKTOP)", url="https://farmingsys.io/app/simulation-history")

    # =========================================================================
    # ZONE 3: MOBILE SIMULATION HISTORY PHONE MOCKUP (w=440, x=1400)
    # =========================================================================
    m2_x, m2_w = 1400, 440
    draw.rounded_rectangle([m2_x, card_y, m2_x + m2_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=m2_x + 25, cy=card_y + 35, text="MOBILE VIEW (390px)", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((m2_x + 195, card_y + 35), "시뮬레이션 내역 모바일 UI", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    mob_asset = os.path.join(ASSETS_DIR, "figma_simulation_history_mobile.png")
    draw_phone_mockup(img, mob_asset, cx=m2_x + m2_w//2, cy=card_y + 75 + (card_h - 95)//2, target_h=640, bezel=7, radius=28)

    draw_slide_footer(draw, 12, 13, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_12.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 13: OUTCOMES & RETROSPECTIVE (AIA+ Style Full Retrospective)
# -------------------------------------------------------------
def make_slide_13():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 13, 
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

    draw_slide_footer(draw, 13, 13, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_13.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_09()
    make_slide_10()
    make_slide_11()
    make_slide_12()
