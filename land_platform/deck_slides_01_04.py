import os
from PIL import Image, ImageDraw, ImageFilter
from deck_common import *

# -------------------------------------------------------------
# SLIDE 01: HERO COVER (Clean Open Storyline & Water Calculator Style)
# -------------------------------------------------------------
def make_slide_01():
    base = Image.new('RGBA', (W, H), (250, 252, 255, 255))
    
    # 1. Subtle Ambient Radial Glow (Soft Emerald/Mint Tint)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([800, 100, 1850, 850], fill=(22, 198, 102, 18))
    g_draw.ellipse([1050, 180, 1750, 780], fill=(59, 235, 133, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    
    draw = ImageDraw.Draw(base)
    
    # 2. Hairline Top Boundary
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    # 3. Top Kicker & Metadata
    draw_pill_badge(draw, left_x=100, cy=76, text="2025 PORTFOLIO CASE STUDY", font=get_font(11.5, 'bold'), theme='green', pad_x=12, height=28)
    
    meta_txt = "WEB (Responsive)  ·  2025.01 - 2025.02  ·  참여율 100%  ·  UX 리서치 · UI 설계 · GUI 디자인"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=(100, 116, 139))
    
    # 4. Category Label
    draw.text((100, 136), "SMARTFARM CENTER · RESPONSIVE WEB", font=get_font(13.5, 'bold'), fill=BRAND_GREEN)
    
    # 5. Big Clean Headline (Exact Title from User, 2 Stacked Lines to Prevent Collision)
    # Line 1: '토지를 분석하다,' in Dark Slate
    # Line 2: '토지개발분석플랫폼' in Brand Green Black
    draw.text((100, 166), "토지를 분석하다,", font=get_font(38, 'bold'), fill=(15, 23, 42))
    draw.text((100, 214), "토지개발분석플랫폼", font=get_font(52, 'black'), fill=BRAND_GREEN)
    
    # 6. Clean UX Subtitle (2 balanced lines, cleanly distanced)
    sub1 = "수많은 공적 장부와 복잡한 인허가 법률에 가로막혀 있던 토지개발의 진입 장벽을 완전히 허물고,"
    sub2 = "지번 입력 한 번으로 대상지 규제 판정, 스마트팜 시설배치, 공사비 적산 및 타당성 보고서를 원클릭 도출합니다."
    draw.text((100, 282), sub1, font=get_font(15, 'regular'), fill=(71, 85, 105))
    draw.text((100, 308), sub2, font=get_font(15, 'semibold'), fill=(30, 41, 59))
    
    # 7. OPEN STORYLINE: 4 Key Strengths (Clean, open layout with zero enclosing heavy boxes)
    strengths = [
        ("01", "정보 통합", "3초 규제 판정 및 지적도 통합", "GIS & Legal Analysis Engine",
         "연속지적도와 국토계획법 등 100여 개 공공 규제를 지도 위에 오버레이하여 개발 가능 여부를 3초 만에 판별합니다."),
        ("02", "스마트팜 설계", "온실 모듈 원클릭 자동 배치", "Intelligent Facility Layout",
         "전문 CAD 도면 없이도 비닐·유리온실과 에너지 부대시설을 부지 형상에 맞추어 최적 정렬하고 유효 생산 면적을 계산합니다."),
        ("03", "실시간 적산", "LH 표준건축비 연동 재무 모델", "Automated CapEx/OpEx Estimation",
         "토목·건축·설비비와 최저시급 연동 운영비를 실시간 자동 산출하여 예산 초과 리스크와 금융 심사 지연을 방지합니다."),
        ("04", "타당성 보고서", "금융 표준 분석 보고서 원클릭 발급", "Institutional-Grade Valuation PDF",
         "지번 현황, 시설 조감도, 10개년 현금흐름(IRR/ROI)이 담긴 정형화된 보고서를 PDF로 즉시 발급해 사업화를 가속합니다.")
    ]
    
    max_badge_w = max(draw.textlength(tag, font=get_font(10, 'bold')) + 16 for _, tag, _, _, _ in strengths)
    title_x = int(round(144 + max_badge_w + 20))
    
    k_y = 368
    for idx, (num, tag, title_ko, sub_en, desc) in enumerate(strengths):
        # Open number pill
        draw.rounded_rectangle([100, k_y + 2, 136, k_y + 28], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.text((118, k_y + 15), num, font=get_font(11, 'bold'), fill=BRAND_GREEN, anchor='mm')
        
        # Tag & Title & EN Subtitle
        draw_pill_badge(draw, left_x=144, cy=k_y + 15, text=tag, font=get_font(10, 'bold'), theme='green', pad_x=8, height=22)
        
        draw.text((title_x, k_y + 4), title_ko, font=get_font(15, 'bold'), fill=(15, 23, 42))
        
        w_title = draw.textlength(title_ko, font=get_font(15, 'bold'))
        draw.text((title_x + w_title + 10, k_y + 6), f"·  {sub_en}", font=get_font(12, 'medium'), fill=(100, 116, 139))
        
        # Description lines (strictly within 720px width to avoid any touch with right mockup)
        lines = wrap_text(desc, get_font(12, 'regular'), 720, draw)
        desc_y = k_y + 36
        for l in lines[:2]:
            draw.text((144, desc_y), l, font=get_font(12, 'regular'), fill=(71, 85, 105))
            desc_y += 20
            
        # Subtle hairline divider
        if idx < 3:
            draw.line([(100, k_y + 88), (880, k_y + 88)], fill=(226, 232, 240), width=1)
            
        k_y += 106

    # 8. Right Side: Flagship 3D Tablet + Mobile Mockup (Hero Podium)
    mockup_path = os.path.join(ASSETS_DIR, "figma_hero_podium_mockup.png")
    if os.path.exists(mockup_path):
        m_img = Image.open(mockup_path).convert('RGBA')
        target_w = 820
        aspect = m_img.height / m_img.width
        target_h = int(target_w * aspect)
        m_resized = m_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Position right side: px = 970, py = 205 (bottom will be 205 + 591 = 796, cleanly above bar_y = 842)
        px = 970
        py = 205
        
        # Soft clean shadow strictly conforming to the alpha mask and kept above bar_y
        m_alpha = m_resized.split()[3]
        sh_img = Image.new('RGBA', (m_resized.width + 80, m_resized.height + 80), (0, 0, 0, 0))
        sh_color = Image.new('RGBA', m_resized.size, (15, 23, 42, 45))
        sh_img.paste(sh_color, (40, 48), m_alpha)
        sh_img = sh_img.filter(ImageFilter.GaussianBlur(28))
        
        base.paste(sh_img, (px - 40, py - 32), sh_img)
        # Direct alpha composite paste - no white box artifact
        base.paste(m_resized, (px, py), m_resized)
        
    draw = ImageDraw.Draw(base)

    # 9. Bottom 4-Column Specification Strip (Spanning x=100 to 1820, y=842 to 956)
    bar_y = 842
    bar_h = 114
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    col_w = 1720 // 4
    specs = [
        ("PROJECT ROLE", "UX 리서치 · UI 설계 · GUI 디자인 100%", "사용자 리서치 · 페르소나/여정맵 · IA 설계 · 와이어프레임 · 피그마 GUI 총괄"),
        ("PERIOD & TIMELINE", "2025.01 - 2025.02 (2개월 완결)", "토지개발 타당성 분석 코어 기능 기획, 데스크톱 및 모바일 반응형 디자인 완성"),
        ("DESIGN SYSTEM", "Agri-Tech Trust 디자인 시스템", "Pretendard 12단계 텍스트 스케일 · 10색 아토믹 컬러 팔레트 · 8-pt 그리드 시스템"),
        ("PLATFORM SCOPE", "Web (Desktop & Mobile 반응형)", "B2B 데스크톱 12-Col 대화면 분석 뷰어 및 모바일 4-Col 현장 실사용 최적화")
    ]
    
    for i, (cat, val_bold, val_desc) in enumerate(specs):
        cx = 100 + i * col_w
        if i > 0:
            draw.line([(cx, bar_y + 18), (cx, bar_y + bar_h - 18)], fill=(226, 232, 240), width=1)
        
        draw.text((cx + 28, bar_y + 18), cat, font=get_font(11, 'bold'), fill=BRAND_GREEN)
        draw.text((cx + 28, bar_y + 42), val_bold, font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 28, bar_y + 68), val_desc, font=get_font(11, 'regular'), fill=(100, 116, 139))

    draw_slide_footer(draw, 1, 12, dark_mode=False)
    
    final_rgb = base.convert('RGB')
    out_path = os.path.join(OUT_DIR, "slide_01.png")
    final_rgb.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 02: PROBLEMS & RESEARCH (Minimal & Impactful)
# -------------------------------------------------------------
def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 2, 
        "PROBLEMS & RESEARCH", 
        "Problems & Research | ", 
        "토지개발 시장 핵심 문제점 및 사용자 리서치 분석", 
        "파편화된 정보와 복잡한 인허가로 인한 진입 장벽을 해결하기 위한 실태 조사와 정량 데이터", 
        right_badge=("EMPIRICAL RESEARCH", "green")
    )
    
    problems = [
        ("01", "정보의 파편화", "지역 규제, 공적장부, 시세가 여러 기관에 흩어져 수작업 탐색에 과도한 시간 소모"),
        ("02", "비전문가 진입 장벽", "GIS·CAD 등 전문 프로그램과 비싼 컨설팅 의존으로 일반 농가 및 창업자의 접근 난항"),
        ("03", "자동화 도구 부재", "토지 맞춤형 배치나 생산량·수익률 시뮬레이션 도구가 없어 주먹구구식 기획 반복"),
        ("04", "단절된 프로세스", "토지 확인부터 시설 설계, 재무 타당성 검토까지 하나의 흐름으로 연결되지 못함")
    ]
    
    t1_y = 215
    t1_w = 412
    t1_h = 190
    for i, (num, title, desc) in enumerate(problems):
        px = 100 + i * (t1_w + 24)
        draw.rounded_rectangle([px, t1_y, px + t1_w, t1_y + t1_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([px + 20, t1_y + 20, px + 52, t1_y + 52], radius=6, fill=BRAND_GREEN)
        draw.text((px + 36, t1_y + 36), num, font=get_font(14, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((px + 64, t1_y + 36), title, font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw.line([(px + 20, t1_y + 66), (px + t1_w - 20, t1_y + 66)], fill=BORDER_LIGHT, width=1)
        
        lines = wrap_text(desc, get_font(12, 'regular'), t1_w - 40, draw)
        ly = t1_y + 84
        for line in lines:
            draw.text((px + 20, ly), line, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 22
            
    t2_y = 435
    t2_w = 848
    t2_h = 515
    
    # Chart 1: Bar Chart
    lx = 100
    draw.rounded_rectangle([lx, t2_y, lx + t2_w, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=t2_y + 25, text="EMPIRICAL METRICS", font=get_font(10.5, 'bold'), theme='green', pad_x=10, height=22)
    draw.text((lx + 25, t2_y + 58), "사용자가 가장 어려워하는 토지개발 과정", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + t2_w - 25, t2_y + 60), "(KCI 및 공공데이터 연구 조사)", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='ra')
    
    bar_items = [
        ("수익성 계산 (사업성)", 4.5, BRAND_GREEN),
        ("인허가 정보 찾기", 4.3, (16, 185, 129)),
        ("설계 툴 사용 (CAD)", 4.1, BRAND_TEAL),
        ("단계 간 흐름 이해 (UX)", 4.0, (71, 85, 105))
    ]
    
    bar_base_y = t2_y + 415
    bar_max_h = 240
    bw = 120
    for idx, (b_label, b_val, b_col) in enumerate(bar_items):
        bx = lx + 80 + idx * 180
        bh = int(bar_max_h * (b_val / 5.0))
        draw.rounded_rectangle([bx, bar_base_y - bar_max_h, bx + bw, bar_base_y], radius=8, fill=(241, 245, 249))
        draw.rounded_rectangle([bx, bar_base_y - bh, bx + bw, bar_base_y], radius=8, fill=b_col)
        draw.text((bx + bw//2, bar_base_y - bh - 16), f"{b_val}", font=get_num_font(16, 'bold'), fill=b_col, anchor='mm')
        draw.text((bx + bw//2, bar_base_y + 24), b_label, font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
        draw.text((bx + bw//2, bar_base_y + 46), f"5점 만점 중 {b_val}점", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')

    # Chart 2: Donut Chart
    rx = 972
    draw.rounded_rectangle([rx, t2_y, rx + t2_w, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=t2_y + 25, text="MARKET SURVEY", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((rx + 25, t2_y + 58), "정보 파편화 원인 및 통합 필요성 비중", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((rx + t2_w - 25, t2_y + 60), "(토지이음 · CAD 포럼 조사)", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='ra')
    
    pie_cx, pie_cy, pie_r = rx + 190, t2_y + 255, 120
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=0, end=108, fill=BRAND_GREEN)
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=108, end=198, fill=(99, 102, 241))
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=198, end=270, fill=(51, 65, 85))
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=270, end=360, fill=BRAND_TEAL)
    draw.ellipse([pie_cx - 55, pie_cy - 55, pie_cx + 55, pie_cy + 55], fill=CARD_LIGHT)
    draw.text((pie_cx, pie_cy - 10), "통합 필요성", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((pie_cx, pie_cy + 12), "100%", font=get_num_font(16, 'bold'), fill=BRAND_GREEN, anchor='mm')
    
    pie_legends = [
        ("수익성 자동 계산", "30%", BRAND_GREEN, "복잡한 세무, 보조금, IRR/NPV 연산"),
        ("규제·공적장부 통합", "25%", (99, 102, 241), "토지이용계획 및 조례 인허가 판별"),
        ("지역 입지 분석", "20%", (51, 65, 85), "접도 조건, 경사도, 고도 분석"),
        ("설계 도면 시뮬레이션", "25%", BRAND_TEAL, "온실 규격 및 부대시설 구획")
    ]
    leg_y = t2_y + 115
    for l_title, l_pct, l_col, l_sub in pie_legends:
        draw.rounded_rectangle([rx + 360, leg_y, rx + t2_w - 30, leg_y + 70], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([rx + 375, leg_y + 15, rx + 395, leg_y + 35], radius=4, fill=l_col)
        draw.text((rx + 410, leg_y + 25), l_title, font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw.text((rx + t2_w - 50, leg_y + 25), l_pct, font=get_num_font(16, 'bold'), fill=l_col, anchor='rm')
        draw.text((rx + 410, leg_y + 48), l_sub, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB, anchor='lm')
        leg_y += 82

    draw.rounded_rectangle([rx + 25, t2_y + 455, rx + t2_w - 25, t2_y + 500], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((rx + 40, t2_y + 477), "💡 리서치 결론: 분절된 4대 핵심 과정을 단일 SaaS 파이프라인으로 통합하는 것이 최우선 과제", font=get_font(12, 'bold'), fill=BRAND_DARK, anchor='lm')

    draw_slide_footer(draw, 2, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_02.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 03: USER PERSONAS (Clear, Focused Contrast)
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 3, 
        "USER PERSONAS", 
        "Target Personas | ", 
        "핵심 타깃 페르소나 및 사용자 니즈 분석", 
        "귀촌 준비 직장인과 청년 스마트팜 창업가의 핵심 Pain Points와 솔루션 니즈 비교", 
        right_badge=("CORE PERSONAS", "green")
    )
    
    card_w = 848
    card_h = 740
    cy = 220
    
    # Persona 1: 김도현
    c1_x = 100
    draw.rounded_rectangle([c1_x, cy, c1_x + card_w, cy + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c1_x + 30, cy=cy + 40, text="PERSONA 01 · 귀촌 준비 / 초보 농업인", font=get_font(11, 'bold'), theme='green', pad_x=12, height=26)
    draw.text((c1_x + 30, cy + 90), "김도현", font=get_font(26, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c1_x + 120, cy + 94), "35세 · 직장인 (귀촌 준비자)", font=get_font(15, 'medium'), fill=TEXT_LIGHT_SUB)
    draw.text((c1_x + 30, cy + 130), '"귀촌을 준비 중인데, 어디서부터 어떻게 시작해야 할지 막막합니다."', font=get_font(15, 'bold'), fill=BRAND_DARK)
    
    draw.line([(c1_x + 30, cy + 165), (c1_x + card_w - 30, cy + 165)], fill=BORDER_LIGHT, width=1)
    
    draw.text((c1_x + 30, cy + 195), "⚠️ 핵심 불편 사항 (Pain Points)", font=get_font(16, 'bold'), fill=(225, 29, 72))
    pains_1 = [
        ("고비용 컨설팅 의존", "개발 가능 여부 확인을 위해 외부 컨설팅에 의존하나 비용이 비싸고 회신이 느림"),
        ("수작업 공적장부 취합", "토지이용계획원, 지적도 등 정보를 기관별로 일일이 검색하고 수작업 정리하는 비효율"),
        ("수익성 예측 불가", "스마트팜 설치 시 실제 수익 발생 여부와 회수 기간을 객관적으로 가늠하기 어려움")
    ]
    py = cy + 230
    for p_title, p_desc in pains_1:
        draw.rounded_rectangle([c1_x + 30, py, c1_x + card_w - 30, py + 62], radius=10, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
        draw.text((c1_x + 45, py + 18), "• " + p_title, font=get_font(13, 'bold'), fill=(159, 18, 57))
        draw.text((c1_x + 45, py + 38), p_desc, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
        py += 72
        
    draw.text((c1_x + 30, cy + 470), "💡 핵심 요구 가치 (User Needs)", font=get_font(16, 'bold'), fill=BRAND_GREEN)
    needs_1 = [
        ("원스톱 지번 규제 분석", "지번 검색 한 번으로 복잡한 공적 규제와 인허가 가능 여부를 지도 위에 시각화"),
        ("자동 투자 타당성 도출", "토지 개발 적합도와 예상 수익률, 투자 회수 기간을 시스템이 원클릭 자동 산출"),
        ("초보자 맞춤형 스텝 가이드", "전문 지식이 없어도 단계별 안내를 따라가며 손쉽게 의사결정할 수 있는 UI")
    ]
    ny = cy + 505
    for n_title, n_desc in needs_1:
        draw.rounded_rectangle([c1_x + 30, ny, c1_x + card_w - 30, ny + 62], radius=10, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
        draw.text((c1_x + 45, ny + 18), "✔ " + n_title, font=get_font(13, 'bold'), fill=(6, 95, 70))
        draw.text((c1_x + 45, ny + 38), n_desc, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN)
        ny += 72

    # Persona 2: 박예진
    c2_x = 972
    draw.rounded_rectangle([c2_x, cy, c2_x + card_w, cy + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c2_x + 30, cy=cy + 40, text="PERSONA 02 · 청년 스마트팜 창업가", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=26)
    draw.text((c2_x + 30, cy + 90), "박예진", font=get_font(26, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c2_x + 120, cy + 94), "28세 · 청년 농업 창업가", font=get_font(15, 'medium'), fill=TEXT_LIGHT_SUB)
    draw.text((c2_x + 30, cy + 130), '"제가 구상한 온실과 부대시설 배치를 직접 시뮬레이션해보고 싶어요."', font=get_font(15, 'bold'), fill=(37, 99, 235))
    
    draw.line([(c2_x + 30, cy + 165), (c2_x + card_w - 30, cy + 165)], fill=BORDER_LIGHT, width=1)
    
    draw.text((c2_x + 30, cy + 195), "⚠️ 핵심 불편 사항 (Pain Points)", font=get_font(16, 'bold'), fill=(225, 29, 72))
    pains_2 = [
        ("입지 변수 파악 난항", "경사도, 진입로 너비, 용도지역 등 땅 선택 기초 단계부터 고려할 변수가 너무 많음"),
        ("전문 CAD 툴의 높은 장벽", "건축 설계 프로그램의 난이도가 높아 원하는 시설 배치를 시각적으로 검토 불가"),
        ("작물별 생산량 예측 한계", "온실 유형과 재배 작물 연동 생산량 및 적산 분석을 외부 업체에 전적으로 의존")
    ]
    py = cy + 230
    for p_title, p_desc in pains_2:
        draw.rounded_rectangle([c2_x + 30, py, c2_x + card_w - 30, py + 62], radius=10, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
        draw.text((c2_x + 45, py + 18), "• " + p_title, font=get_font(13, 'bold'), fill=(159, 18, 57))
        draw.text((c2_x + 45, py + 38), p_desc, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
        py += 72
        
    draw.text((c2_x + 30, cy + 470), "💡 핵심 요구 가치 (User Needs)", font=get_font(16, 'bold'), fill=(37, 99, 235))
    needs_2 = [
        ("직관적 GIS 시설 배치", "웹 화면에서 지도 위 온실 규격과 시설을 드래그하여 최적으로 배치하는 툴"),
        ("작물 데이터베이스 연동", "딸기, 토마토 등 고부가가치 작물별 수확량과 표준 단가를 반영한 수익 시뮬레이션"),
        ("금융 심사용 표준 보고서", "지자체 인허가 신청 및 금융기관 자금 조달에 즉시 제출 가능한 정형화된 리포트")
    ]
    ny = cy + 505
    for n_title, n_desc in needs_2:
        draw.rounded_rectangle([c2_x + 30, ny, c2_x + card_w - 30, ny + 62], radius=10, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((c2_x + 45, ny + 18), "✔ " + n_title, font=get_font(13, 'bold'), fill=(30, 64, 175))
        draw.text((c2_x + 45, ny + 38), n_desc, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN)
        ny += 72

    draw_slide_footer(draw, 3, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_03.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 04: JOURNEY & INSIGHTS (Streamlined Table + 4 Insights)
# -------------------------------------------------------------
def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 4, 
        "JOURNEY & INSIGHTS", 
        "User Journey & Insights | ", 
        "사용자 6단계 여정 맵 및 4대 전략적 인사이트", 
        "인식부터 타당성 평가까지의 단계별 Pain Points와 이를 해결하는 핵심 디자인 전략", 
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
        draw.rounded_rectangle([cur_x, gy, cur_x + c_w, gy + 36], radius=6, fill=fill_col)
        t_col = (255, 255, 255) if idx > 0 else TEXT_LIGHT_MAIN
        draw.text((cur_x + c_w//2, gy + 18), c_name, font=get_font(12, 'bold'), fill=t_col, anchor='mm')
        cur_x += c_w + 5
        
    journey_rows = [
        ("행동 (Action)", [
            "귀농·귀촌 기사 검색",
            "부동산·공공포털 탐색",
            "후보 지번 현장 방문",
            "토지이용계획원 확인",
            "스마트팜 배치 구상",
            "견적서 및 보고서 작성"
        ], (255, 255, 255)),
        ("불편 (Pain Point)", [
            "정보가 제각각이라 혼란",
            "플랫폼 분산으로 비교 난항",
            "경사도·진입로 파악 곤란",
            "복잡한 법적 용어 난해함",
            "CAD 툴 다루기 어려움",
            "컨설팅 비용과 불투명성"
        ], (255, 241, 242)),
        ("요구 (Needs)", [
            "맞춤형 기초 가이드라인",
            "한눈에 보는 통합 정보",
            "기초 조건 자동 분석",
            "시각화된 규제 요약 뷰",
            "쉬운 시뮬레이션 인터페이스",
            "원클릭 사업성 분석 보고서"
        ], (240, 253, 244)),
        ("기회 (Opportunity)", [
            "온보딩 맞춤 설문 제공",
            "지도 기반 통합 뷰 제공",
            "개발 적합도 자동 진단",
            "규제 요약 3초 카드",
            "원클릭 온실 모듈 배치",
            "금융 표준 PDF 즉시 생성"
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

    # Right: 4 Key Strategic Insights (Clear, Generous Padding)
    rx = 1185
    rw = 635
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 32, text="4 CORE STRATEGIC INSIGHTS", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 25, ly + 72), "리서치 기반 4대 디자인 전략", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    insights = [
        ("01. 단일 지도 인터페이스 통합", "분산된 토지 규제·인허가·시세를 단일 지도 인터페이스에 집약하여 탐색 피로도 해소"),
        ("02. 3초 규제 판별 & 객관화", "복잡한 법령 해석을 표준화하여 지번 입력 즉시 3초 만에 개발 적합도 도출"),
        ("03. 직관적 시각 시뮬레이션", "전문 CAD 없이도 지도상에서 온실 규격과 시설을 손쉽게 배치하는 환경 제공"),
        ("04. 끊김 없는 스텝형 워크플로우", "탐색-배치-적산-보고서 출력이 물 흐르듯 자연스럽게 이어지는 엔드투엔드 UX 구축")
    ]
    iy = ly + 115
    for title, desc in insights:
        draw.rounded_rectangle([rx + 20, iy, rx + rw - 20, iy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((rx + 35, iy + 28), title, font=get_font(15, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12, 'regular'), rw - 70, draw)
        dy = iy + 58
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
