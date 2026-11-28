import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 09: CORE FEATURE 02 · MULTI-SCREEN SMARTFARM & CAPEX
# (4 Real Figma Screens: 2 Mobile + 2 Desktop + 3-Col Spec Strip)
# -------------------------------------------------------------
def make_slide_09():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 9, 
        "CORE FEATURE 02 · FACILITY & CAPEX", 
        "Simulation Step 3~5 | ", 
        "스마트팜 시설 배치부터 LH 표준 조성비·대안 비교까지 원클릭", 
        "멀티스크린 4종 연동: [1] 모바일 시설배치 & 조성비 플로우  |  [2] 데스크톱 조성비 4분할 테이블 & 비용 비교 뷰어", 
        right_badge=("4-SCREEN MULTI-VIEW", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # LEFT ZONE: 2 MOBILE SCREENS SIDE-BY-SIDE (x=100, w=580)
    lx, lw = 100, 580
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_l = draw_pill_badge(draw, left_x=lx + 24, cy=card_y + 34, text="MOBILE FLOW · STEP 4 → 5", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24)
    draw.text((lx + 24 + bw_l + 12, card_y + 34), "시설 설계 및 조성비 모바일 연동", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    # Two phone mockups side by side
    p1_cx = lx + 150
    p2_cx = lx + 430
    p_cy = card_y + 340
    
    mob_s4 = os.path.join(ASSETS_DIR, "figma_step4_smartfarm_mobile.png")
    mob_s5 = os.path.join(ASSETS_DIR, "figma_step5_construction_cost_mobile.png")
    draw_phone_mockup(img, mob_s4, cx=p1_cx, cy=p_cy, target_h=490, bezel=6, radius=24, fixed_aspect=0.465)
    draw_phone_mockup(img, mob_s5, cx=p2_cx, cy=p_cy, target_h=490, bezel=6, radius=24, fixed_aspect=0.465)
    
    # Step Arrow between 2 phones
    draw_arrow(draw, (lx + 268, p_cy), (lx + 306, p_cy), col=BRAND_GREEN, width=3, arrow_size=6)
    
    # Captions under phones
    draw_pill_badge(draw, cx=p1_cx, cy=card_y + 612, text="STEP 4 · 스마트팜 설계", font=get_font(9.5, 'bold'), theme='green', pad_x=10, height=22)
    draw.text((p1_cx, card_y + 638), "비닐·유리·수직농장 모듈 선택", font=get_font(10.5, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    draw_pill_badge(draw, cx=p2_cx, cy=card_y + 612, text="STEP 5 · 조성비 산출", font=get_font(9.5, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((p2_cx, card_y + 638), "LH 표준단가 원클릭 토글 적용", font=get_font(10.5, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')

    # Bottom highlight bar in Left Zone
    draw.rounded_rectangle([lx + 24, card_y + card_h - 76, lx + lw - 24, card_y + card_h - 20], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((lx + lw//2, card_y + card_h - 48), "CAD 없이 온실 모듈 클릭 → 자동 면적 계산 → 실시간 공사비 반영", font=get_font(11.5, 'bold'), fill=BRAND_DARK, anchor='mm')

    # RIGHT ZONE: 2 DESKTOP SCREENS + 3-COL CAPEX SPECS (x=700, w=1120)
    rx, rw = 700, 1120
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_r = draw_pill_badge(draw, left_x=rx + 24, cy=card_y + 34, text="DESKTOP CAPEX ENGINE · STEP 5 & 6", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((rx + 24 + bw_r + 12, card_y + 34), "LH 표준건축비 4분할 적산 테이블 & 대안별 비용 비교 (Figma 실물)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    # Top 2 Desktop Screens side by side
    d_w = 524
    d_y = card_y + 68
    d1_path = os.path.join(ASSETS_DIR, "figma_step5_construction_cost_desktop.png")
    d2_path = os.path.join(ASSETS_DIR, "figma_step6_cost_comparison_desktop.png")
    draw_browser_mockup(img, d1_path, x=rx + 24, y=d_y, w=d_w, h=404, title="", url="https://farmingsys.io/app/step-05-capex")
    draw_browser_mockup(img, d2_path, x=rx + 24 + d_w + 24, y=d_y, w=d_w, h=404, title="", url="https://farmingsys.io/app/step-06-compare")

    # Bottom 3-Column Spec Cards inside Right Zone
    spec_y = card_y + 506
    spec_h = card_h - 528
    sc_w = (rw - 48 - 2 * 18) // 3
    capex_specs = [
        ("01. LH 표준건축비 자동 연동", "한국토지주택공사(LH) 표준건축비 DB를 실시간 연동하여 기본공사비·건축비·우수공·가로등 비용을 원클릭 산출합니다."),
        ("02. 전항목 표준값 원클릭 토글", "복잡한 적산 내역 입력 없이 체크박스 및 '전항목 표준값 사용' 토글로 비전문가도 총 조성비(약 23.6억)를 즉시 도출합니다."),
        ("03. 다중 시나리오 비용 비교", "비닐온실·유리온실 등 복수 대안의 단위공사비와 초기 투자 규모를 병렬 비교하여 예산 초과 리스크를 사전에 차단합니다.")
    ]
    for idx, (st, sd) in enumerate(capex_specs):
        sx = rx + 24 + idx * (sc_w + 18)
        draw.rounded_rectangle([sx, spec_y, sx + sc_w, spec_y + spec_h], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=sx + 16, cy=spec_y + 26, text=f"CAPEX LOGIC 0{idx+1}", font=get_font(9, 'bold'), theme='green' if idx != 1 else 'blue', pad_x=8, height=20)
        draw.text((sx + 16, spec_y + 52), st, font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN)
        lines = wrap_text(sd, get_font(10.5, 'regular'), sc_w - 32, draw)
        dy = spec_y + 82
        for l in lines[:4]:
            draw.text((sx + 16, dy), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 19

    draw_slide_footer(draw, 9, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_09.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 10: CORE FEATURE 03 · MULTI-SCREEN OPEX, REVENUE & REPORT
# (4 Real Figma Screens: 2 Stacked Desktop + 1 Full Report + 1 Mobile)
# -------------------------------------------------------------
def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 10, 
        "CORE FEATURE 03 · OPEX & VALUATION", 
        "Simulation Step 7~8 | ", 
        "매출·운영비(OPEX) 정밀 적산부터 금융 표준 분석 보고서 발급까지", 
        "멀티스크린 4종 연동: [1] 작물 매출 & 운영비 데스크톱 2단  |  [2] 최종 타당성 분석 보고서  |  [3] 모바일 매출 설계 UI", 
        right_badge=("4-SCREEN VALUATION", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # LEFT ZONE: 2 STACKED DESKTOP SCREENS (x=100, w=600)
    lx, lw = 100, 600
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_l = draw_pill_badge(draw, left_x=lx + 24, cy=card_y + 34, text="STEP 7 · REVENUE & OPEX", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((lx + 24 + bw_l + 12, card_y + 34), "작물별 매출 & 운영비·인건비 설계 (2단 실물)", font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    d_rev1 = os.path.join(ASSETS_DIR, "figma_step7_revenue_part1_desktop.png")
    d_rev2 = os.path.join(ASSETS_DIR, "figma_step7_revenue_part2_operating_cost_desktop.png")
    
    # Stack 2 16:9 desktop screens cleanly (w=500 -> h=315 each)
    dw_s = 504
    dx_s = lx + (lw - dw_s) // 2
    h1 = draw_browser_mockup(img, d_rev1, x=dx_s, y=card_y + 66, w=dw_s, h=318, title="", url="https://farmingsys.io/app/step-07-revenue")
    draw_browser_mockup(img, d_rev2, x=dx_s, y=card_y + 66 + h1 + 18, w=dw_s, h=318, title="", url="https://farmingsys.io/app/step-07-opex")

    # CENTER ZONE: FINAL VALUATION REPORT VIEWER (x=720, w=430)
    mx, mw = 720, 430
    draw.rounded_rectangle([mx, card_y, mx + mw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_c = draw_pill_badge(draw, left_x=mx + 24, cy=card_y + 34, text="STEP 8 · FINAL REPORT", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24)
    draw.text((mx + 24 + bw_c + 12, card_y + 34), "최종 시뮬레이션 분석 보고서", font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    rep_full = os.path.join(ASSETS_DIR, "figma_step8_simulation_report_full.jpg")
    rep_im = Image.open(rep_full)
    target_rh = 640
    rvp_h = target_rh - 34 - 4
    rvp_w = int(rvp_h * (rep_im.width / rep_im.height))
    tot_rw = rvp_w + 4
    rx_rep = mx + (mw - tot_rw) // 2
    draw_browser_mockup(img, rep_full, x=rx_rep, y=card_y + 72, w=tot_rw, h=target_rh, title="", url="https://farmingsys.io/report/pdf")

    # RIGHT ZONE: MOBILE REVENUE UI + 3 FINANCIAL ENGINE SPECS (x=1170, w=650)
    rx, rw = 1170, 650
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_r = draw_pill_badge(draw, left_x=rx + 24, cy=card_y + 34, text="MOBILE & VALUATION LOGIC", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24)
    draw.text((rx + 24 + bw_r + 12, card_y + 34), "모바일 수익 설계 및 금융 평가 엔진", font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    mob_rev = os.path.join(ASSETS_DIR, "figma_step7_revenue_design_mobile.png")
    draw_phone_mockup(img, mob_rev, cx=rx + 145, cy=card_y + 398, target_h=618, bezel=7, radius=26)
    
    ax, aw = rx + 286, rw - 310
    fin_specs = [
        ("OPEX ENGINE", "중간재비·판관비 자동 보정", "비료·농약 등 중간재비와 유지관리 판관비를 표준값 토글로 자동 보정해 오차 차단"),
        ("WAGE SYNC", "최저시급 연동 고정비 산출", "가공유통 투입인원(47명) 및 연봉을 국가 최저시급 공공 DB와 연동해 투명성 확보"),
        ("BANK-READY PDF", "10개년 현금흐름 보고서", "지적도·규제·조성비·IRR/NPV가 집약된 금융 심사용 보고서를 원클릭 PDF 발급")
    ]
    ay = card_y + 84
    for badge_t, ft, fd in fin_specs:
        draw.rounded_rectangle([ax, ay, ax + aw, ay + 186], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=ax + 16, cy=ay + 26, text=badge_t, font=get_font(9, 'bold'), theme='blue' if badge_t=="WAGE SYNC" else 'green', pad_x=8, height=20)
        draw.text((ax + 16, ay + 52), ft, font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN)
        lines = wrap_text(fd, get_font(10.5, 'regular'), aw - 32, draw)
        dy = ay + 82
        for l in lines[:4]:
            draw.text((ax + 16, dy), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 19
        ay += 204

    draw_slide_footer(draw, 10, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_10.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 11: PRODUCTION MULTI-SCREEN GALLERY (Water Calculator Slide 10 Style!)
# (6 Real Mobile Screens Side-by-Side + Bottom User Journey Flow Bar)
# -------------------------------------------------------------
def make_slide_11():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 11, 
        "PRODUCTION UI GALLERY · 6-STEP FLOW", 
        "End-to-End Mobile UI | ", 
        "대상지 탐색부터 이력 관리까지, 일관된 6대 상용 화면 시스템", 
        "사용자의 토지개발 전체 여정(User Journey)을 빈틈없이 지원하도록 Figma 디자인 토큰으로 완성한 6대 반응형 핵심 화면", 
        right_badge=("6-SCREEN SHOWCASE", "green")
    )
    
    gallery_items = [
        ("01. 대상지 규제 탐색", "연속지적도 오버레이\n& 3초 인허가 판정", "figma_step2_land_analysis_mobile.png", "green"),
        ("02. 스마트팜 시설 설계", "비닐·유리·수직농장\n모듈 원클릭 구획", "figma_step4_smartfarm_mobile.png", "green"),
        ("03. 조성비 견적 산출", "LH 표준건축비 연동\n실시간 공사비 계산", "figma_step5_construction_cost_mobile.png", "blue"),
        ("04. 투자 대안 비교", "복수 설계 시나리오\n예산·효율 병렬 대조", "figma_step6_cost_comparison_mobile.png", "blue"),
        ("05. 매출·수익성 설계", "작물별 생산량 예측\n& 최저시급 OPEX 연동", "figma_step7_revenue_design_mobile.png", "green"),
        ("06. 시뮬레이션 이력", "과거 프로젝트 아카이브\n& 원클릭 PDF 재호출", "figma_simulation_history_mobile.png", "gray")
    ]
    
    # Evenly space 6 phone mockups across x=100..1820 (total 1720px -> ~286px slot each)
    slot_w = 1720 // 6
    phone_cy = 485
    phone_h = 505
    
    for idx, (pill_txt, cap_txt, asset_fn, theme) in enumerate(gallery_items):
        cx = 100 + idx * slot_w + slot_w // 2
        asset_p = os.path.join(ASSETS_DIR, asset_fn)
        draw_phone_mockup(img, asset_p, cx=cx, cy=phone_cy, target_h=phone_h, bezel=6, radius=24, fixed_aspect=0.465)
        
        # Pill label + 2-line caption underneath
        pill_y = phone_cy + phone_h // 2 + 34
        draw_pill_badge(draw, cx=cx, cy=pill_y, text=pill_txt, font=get_font(10.5, 'bold'), theme=theme, pad_x=12, height=26)
        
        cap_lines = cap_txt.split('\n')
        draw.text((cx, pill_y + 30), cap_lines[0], font=get_font(11, 'medium'), fill=TEXT_LIGHT_MAIN, anchor='mm')
        draw.text((cx, pill_y + 49), cap_lines[1], font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')

    # Bottom Full-Width USER JOURNEY Flow Bar (Inspired by Smart DCA Slide 10)
    bar_y = 878
    bar_h = 68
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    bw_uj = draw_pill_badge(draw, left_x=128, cy=bar_y + bar_h // 2, text="USER JOURNEY", font=get_font(10, 'bold'), theme='green', solid=True, pad_x=12, height=26)
    
    steps_flow = ["01 지번·규제 탐색", "02 스마트팜 설계", "03 조성비 적산", "04 대안 비교", "05 수익성 분석", "06 이력·보고서"]
    flow_start_x = 128 + bw_uj + 42
    flow_span = 1790 - flow_start_x
    step_dx = flow_span // len(steps_flow)
    
    for idx, st_txt in enumerate(steps_flow):
        sx = flow_start_x + idx * step_dx
        draw.text((sx, bar_y + bar_h // 2), st_txt, font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        if idx < len(steps_flow) - 1:
            arrow_x = sx + step_dx - 34
            draw.text((arrow_x, bar_y + bar_h // 2), "→", font=get_font(14, 'bold'), fill=BRAND_GREEN, anchor='mm')

    draw_slide_footer(draw, 11, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_11.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 12: BUSINESS IMPACT & STAR RETROSPECTIVE (Water Calculator Slide 11 Style!)
# (Zero Overlap: Before/After Cards + 4 KPI Cards + 4-Col STAR Retrospective)
# -------------------------------------------------------------
def make_slide_12():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 12, 
        "BUSINESS IMPACT & RETROSPECTIVE", 
        "Outcomes & STAR | ", 
        "인허가 리드타임 90% 단축, 정량 성과 지표 및 시니어 UX 회고", 
        "기존 수작업 토지개발 프로세스 대비 플랫폼 도입 성과 비교(Before/After)와 4대 정량 KPI 및 STAR 기술 회고", 
        right_badge=("PROJECT OUTCOMES", "green")
    )
    
    # =========================================================================
    # TIER 1: BEFORE vs AFTER COMPARISON CARDS (y=215..475, h=260)
    # =========================================================================
    t1_y = 215
    t1_h = 260
    half_w = 848
    
    # Left Card: BEFORE (Red-accented)
    lx = 100
    draw.rounded_rectangle([lx, t1_y, lx + half_w, t1_y + t1_h], radius=16, fill=(255, 250, 250), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=lx + 26, cy=t1_y + 32, text="BEFORE · 기존 수작업 토지개발", font=get_font(10, 'bold'), theme='red', pad_x=10, height=22)
    draw.text((lx + 26, t1_y + 58), "파편화된 공적 장부와 고비용 외부 컨설팅 의존", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    before_rows = [
        ("규제 및 입지 검토", "토지이음·지자체 조례 수작업 대조로 평균 14일 이상 소요"),
        ("시설 설계 및 적산", "전문 CAD 및 외부 견적 용역 의존으로 회당 수백만 원 비용 발생"),
        ("사업 타당성 검증", "주관적 어림짐작으로 예산 초과 및 금융기관 대출 심사 지연")
    ]
    by = t1_y + 94
    for b_k, b_v in before_rows:
        draw.rounded_rectangle([lx + 26, by, lx + half_w - 26, by + 44], radius=8, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
        draw.text((lx + 42, by + 22), b_k, font=get_font(11.5, 'bold'), fill=(159, 18, 57), anchor='lm')
        draw.text((lx + 215, by + 22), b_v, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        by += 52

    # Right Card: AFTER (Green-accented)
    rx = 972
    draw.rounded_rectangle([rx, t1_y, rx + half_w, t1_y + t1_h], radius=16, fill=(246, 254, 249), outline=(167, 243, 208), width=1)
    draw_pill_badge(draw, left_x=rx + 26, cy=t1_y + 32, text="AFTER · 토지개발분석플랫폼", font=get_font(10, 'bold'), theme='green', solid=True, pad_x=10, height=22)
    draw.text((rx + 26, t1_y + 58), "지번 입력 원클릭 자동 분석 및 금융 표준 보고서 즉시 발급", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    after_rows = [
        ("규제 및 입지 검토", "100여 개 공공 규제 자동 파싱으로 3~5초 만에 적합도 판정 (-90%)"),
        ("시설 설계 및 적산", "온실 모듈 자동 배치 & LH 표준건축비 연동으로 무료 즉시 산출"),
        ("사업 타당성 검증", "10개년 현금흐름(IRR/NPV) 기반 정형 PDF로 의사결정 정확도 +40%")
    ]
    ay = t1_y + 94
    for a_k, a_v in after_rows:
        draw.rounded_rectangle([rx + 26, ay, rx + half_w - 26, ay + 44], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
        draw.text((rx + 42, ay + 22), a_k, font=get_font(11.5, 'bold'), fill=BRAND_DARK, anchor='lm')
        draw.text((rx + 215, ay + 22), a_v, font=get_font(11.5, 'semibold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        ay += 52

    # =========================================================================
    # TIER 2: 4 QUANTITATIVE KPI CARDS (y=495..620, h=125)
    # =========================================================================
    t2_y = 495
    t2_h = 125
    metrics = [
        ("REGULATION DB", "100+", "분석 가능 토지 규제 조건", "국토계획법 등 100여 개 공공 규제 자동 매칭", "green"),
        ("LEAD TIME", "90%", "분석 소요 시간 단축", "기존 14일 수작업 조사를 3~5초로 단축", "green"),
        ("SPEED", "3~5s", "원터치 시뮬레이션 도출", "지번 입력 즉시 시설 구획 및 공사비 산출", "blue"),
        ("ACCURACY", "+40%", "의사결정 정확도 향상", "정량 데이터 기반 사전 투자 리스크 차단", "blue")
    ]
    mw = 412
    for idx, (m_badge, m_val, m_title, m_desc, m_th) in enumerate(metrics):
        mx = 100 + idx * (mw + 24)
        draw.rounded_rectangle([mx, t2_y, mx + mw, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=mx + 22, cy=t2_y + 24, text=m_badge, font=get_font(9, 'bold'), theme=m_th, pad_x=8, height=18)
        val_col = BRAND_GREEN if m_th == "green" else (37, 99, 235)
        draw.text((mx + 22, t2_y + 42), m_val, font=get_num_font(26, 'black'), fill=val_col)
        draw.text((mx + 22, t2_y + 82), m_title, font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((mx + 22, t2_y + 102), m_desc, font=get_font(10, 'regular'), fill=TEXT_LIGHT_SUB)

    # =========================================================================
    # TIER 3: STAR METHOD SENIOR UX RETROSPECTIVE (y=640..960, h=320)
    # =========================================================================
    star_y = 640
    star_w = 1720
    star_h = 320
    draw.rounded_rectangle([100, star_y, 100 + star_w, star_y + star_h], radius=16, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    
    bw_st = draw_pill_badge(draw, left_x=126, cy=star_y + 32, text="SENIOR UX STRATEGY RETROSPECTIVE (STAR)", font=get_font(10, 'bold'), theme='green', solid=True, pad_x=12, height=24)
    draw.text((126 + bw_st + 16, star_y + 32), "공간 GIS와 금융 데이터가 융합된 복잡계를 직관적 디지털 경험으로 전환한 여정", font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    star_items = [
        ("S · Situation (상황)", "토지 지적도, 지자체 조례, 복잡한 인허가 법률과 수십 장의 공적 장부로 인해 비전문가 농가 및 창업자의 진입 장벽과 정보 비대칭이 극심했습니다."),
        ("T · Task (과제)", "별도 전문 학습이나 CAD 도구 없이 대상지 탐색부터 스마트팜 시설배치, 공사비 적산, 금융 표준 타당성 보고서까지 원클릭으로 완결되는 워크플로우를 구축해야 했습니다."),
        ("A · Action (실행)", "데스크톱 12-Col 듀얼 스플릿 GIS 뷰와 모바일 바텀시트 반응형 UI를 설계하고, 100여 개 공공 규제 및 LH 표준건축비를 3초 만에 파싱하는 단계형 인터페이스를 구현했습니다."),
        ("R · Result (성과)", "평균 2주 소요되던 토지 타당성 분석 리드타임을 3~5초로 90% 단축하고, 토지소유주·개발사·금융기관을 단일 정량 데이터로 잇는 신뢰 플랫폼을 완성했습니다.")
    ]
    
    sc_w = (star_w - 52 - 3 * 20) // 4
    for s_idx, (s_tag, s_text) in enumerate(star_items):
        sc_x = 126 + s_idx * (sc_w + 20)
        card_top = star_y + 66
        card_bot = star_y + star_h - 22
        draw.rounded_rectangle([sc_x, card_top, sc_x + sc_w, card_bot], radius=12, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=sc_x + 18, cy=card_top + 26, text=s_tag, font=get_font(10, 'bold'), theme='green' if s_idx in [0, 3] else 'blue', pad_x=10, height=22)
        lines = wrap_text(s_text, get_font(11, 'regular'), sc_w - 36, draw)
        ly = card_top + 54
        for l in lines:
            draw.text((sc_x + 18, ly), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 21

    draw_slide_footer(draw, 12, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_12.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_09()
    make_slide_10()
    make_slide_11()
    make_slide_12()
