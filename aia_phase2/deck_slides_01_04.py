import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from deck_common import (
    W, H, BASE_DIR, CORE_DIR, QI_DIR, OUT_DIR,
    AIA_RED, AIA_RED_DARK, AIA_RED_LIGHT, AIA_RED_BORDER,
    BG_DARK, CARD_DARK, BORDER_DARK, TEXT_DARK_MAIN, TEXT_DARK_SUB,
    BG_LIGHT, CARD_LIGHT, BORDER_LIGHT, BORDER_LIGHT_ACCENT,
    TEXT_LIGHT_MAIN, TEXT_LIGHT_SUB,
    get_font, get_num_font, wrap_text, draw_pill_badge, draw_arrow,
    draw_slide_header, draw_slide_footer, draw_phone_mockup
)

# -------------------------------------------------------------
# SLIDE 01: HERO COVER (AIA+ SENIOR MODE)
# -------------------------------------------------------------
def make_slide_01():
    img = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 1. Subtle warm background gradient/glow
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([800, 100, 1800, 1000], fill=(211, 17, 69, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    img.paste(glow, (0, 0), glow)
    
    draw = ImageDraw.Draw(img)
    
    # Top Category Pill
    draw_pill_badge(draw, left_x=120, cy=105, text="AIA LIFE · SENIOR ACCESSIBILITY INNOVATION", font=get_font(11, 'bold'), theme='red', pad_x=14, height=28)
    draw_pill_badge(draw, left_x=440, cy=105, text="Qi DESIGN SYSTEM v3.3", font=get_font(11, 'bold'), theme='gray', pad_x=12, height=28)
    
    # Hero Title matching Behance: AIA+ SENIOR MODE
    draw.text((120, 155), "AIA+", font=get_font(60, 'black'), fill=(15, 23, 42))
    draw.text((275, 155), "SENIOR MODE", font=get_font(60, 'black'), fill=AIA_RED)
    draw.text((120, 235), "고령자 친화 배리어프리 금융 UX & 10대 비대면 서비스 리뉴얼", font=get_font(26, 'bold'), fill=(51, 65, 85))
    
    # Subtitle Description
    desc_kr = (
        "금융위원회 '고령자 친화적 모바일 금융앱 가이드라인' 100% 완벽 준수\n"
        "6070 액티브 시니어를 위한 제로-뎁스(Zero-Depth) 직관 탐색 아키텍처와\n"
        "Qi 글로벌 디자인 시스템 v3.3 기반의 단일 소스 멀티 테마 프로덕트 디자인"
    )
    draw.text((120, 295), desc_kr, font=get_font(15.5, 'regular'), fill=(100, 116, 139), spacing=8)
    
    # Overview 5 Core Action Spheres
    draw.text((120, 400), "AIA+ 고령자 모드 5대 핵심 서비스 (Overview)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    spheres = [
        ("조회", "계약/납입액 확인", (59, 130, 246)),
        ("납입", "보험료 바로 내기", AIA_RED),
        ("청구", "병원비 서류 접수", (168, 85, 247)),
        ("대출", "환급금 계약대출", (16, 185, 129)),
        ("상담", "큰글씨 고객센터", (71, 85, 105))
    ]
    for idx, (s_name, s_sub, s_col) in enumerate(spheres):
        sx = 120 + idx * 125
        sy = 450
        draw.ellipse([sx, sy, sx + 95, sy + 95], fill=s_col)
        draw.text((sx + 47, sy + 38), s_name, font=get_font(18, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((sx + 47, sy + 62), s_sub, font=get_font(9.5, 'medium'), fill=(255, 255, 255), anchor='mm')
        
    # Bottom 4 Metric Cards (100% 가이드라인, 2x 폰트, 90% 완수율, 50% 시간단축)
    stats = [
        ("100%", "금융위 규제 가이드라인 준수"),
        ("2x", "본문 및 버튼 폰트 크기 확대"),
        ("90%", "시니어 코어 과업 완수율 달성"),
        ("50%", "비대면 업무 소요 시간 단축")
    ]
    card_y = 610
    for idx, (val, label) in enumerate(stats):
        cx = 120 + (idx % 2) * 280
        cy = card_y + (idx // 2) * 110
        cw, ch = 265, 95
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((cx + 20, cy + 20), val, font=get_num_font(32, 'black'), fill=AIA_RED if idx==0 else (15, 23, 42))
        lines = wrap_text(label, get_font(11.5, 'medium'), cw - 40, draw)
        ly = cy + 56
        for line in lines:
            draw.text((cx + 20, ly), line, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_SUB)
            ly += 16
            
    # Bottom Specs Bar
    spec_y = 860
    draw.rounded_rectangle([120, spec_y, 680, spec_y + 110], radius=14, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    specs = [
        ("프로젝트", "AIA생명 AIA+ Phase 2 고령자 모드 & 비대면 서비스 리뉴얼"),
        ("역할 / 기여도", "수석 프로덕트 디자이너 / 기획 및 UX/UI 100% 총괄"),
        ("핵심 표준", "금융위원회 가이드라인 준수 · WCAG 2.1 AAA 8.4:1 고대비")
    ]
    for idx, (label, val) in enumerate(specs):
        sy = spec_y + 15 + idx * 30
        draw.text((140, sy), label, font=get_font(11.5, 'bold'), fill=AIA_RED)
        draw.text((235, sy), val, font=get_font(11.5, 'medium'), fill=(15, 23, 42))
        
    # Right Column: Actual Devices (Large Center Senior Home + 2 Supporting)
    draw_phone_mockup(img, os.path.join(CORE_DIR, "screen_general_main.png"), cx=930, cy=570, phone_w=280, phone_h=600)
    draw_phone_mockup(img, os.path.join(CORE_DIR, "screen_senior_main_home.png"), cx=1260, cy=530, phone_w=330, phone_h=700)
    draw_phone_mockup(img, os.path.join(CORE_DIR, "screen_pay_list_senior.png"), cx=1590, cy=570, phone_w=280, phone_h=600)
    
    # Floating feature pill
    draw_pill_badge(draw, cx=1260, cy=180, text="고령자 친화 제로-뎁스 원터치 홈", font=get_font(12, 'bold'), theme='red', solid=True, pad_x=16, height=32)
    
    draw_slide_footer(draw, 1, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_01.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 02: PROBLEM & RESEARCH (Charts & Statistical Data)
# -------------------------------------------------------------
def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 2, 
        "PROBLEM & RESEARCH", 
        "Problem & Research | ", 
        "고령층 디지털 금융 소외와 통계 분석", 
        "인구 구조 고령화와 모바일 금융앱 이용 장벽에 관한 실증 데이터 조사", 
        right_badge=("EMPIRICAL RESEARCH", "red")
    )
    
    # 2 Big Cards: Left = Pie Chart & Demographics, Right = Bar Chart & Pain Points
    # Left Card (W=800)
    lx = 100
    ly = 220
    lw = 820
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=ly + 35, text="AGE DEMOGRAPHICS & MOBILE ADOPTION", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((lx + 25, ly + 65), "고령자 인구 비율 & 모바일 뱅킹 이용 현황", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Pie Chart Graphic (Clean vector drawing)
    cx, cy, cr = lx + 220, ly + 250, 110
    draw.pieslice([cx - cr, cy - cr, cx + cr, cy + cr], start=0, end=73, fill=(211, 17, 69))       # 65세 이상 20.3%
    draw.pieslice([cx - cr, cy - cr, cx + cr, cy + cr], start=73, end=190, fill=(59, 130, 246))     # 50-64세 32.5%
    draw.pieslice([cx - cr, cy - cr, cx + cr, cy + cr], start=190, end=360, fill=(203, 213, 225))   # 50세 미만 47.2%
    # Donut center
    draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=(255, 255, 255))
    draw.text((cx, cy), "2025\n20.3%", font=get_num_font(14, 'black'), fill=AIA_RED, anchor='mm')
    
    # Pie Legend
    legends = [
        ("■ 65세 이상 (초고령 진입)", "20.3%", AIA_RED),
        ("■ 50-64세 (준고령 은퇴층)", "32.5%", (59, 130, 246)),
        ("■ 50세 미만 (청장년층)", "47.2%", (148, 163, 184))
    ]
    for idx, (ltxt, lval, lcol) in enumerate(legends):
        ly_leg = ly + 180 + idx * 45
        draw.text((lx + 400, ly_leg), ltxt, font=get_font(13.5, 'bold'), fill=lcol)
        draw.text((lx + 680, ly_leg), lval, font=get_num_font(14, 'black'), fill=TEXT_LIGHT_MAIN)
        
    # Demographic Insights
    iy = ly + 420
    draw.text((lx + 25, iy), "핵심 조사 결과 (Research Insights)", font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN)
    pinsights = [
        ("모바일 금융 비이용 사유 1위", "글씨가 작아서 읽기 힘들고 인증 절차가 너무 복잡함 (58.4%)"),
        ("오프라인 창구 방문 이유", "모바일 앱으로 처리하려다 오류가 발생하거나 실패할까 봐 불안함 (47.2%)"),
        ("타인의 도움 요청 빈도", "고령층의 68.2%가 비대면 금융 거래 시 자녀나 타인의 도움을 받아 수행")
    ]
    iy += 35
    for h_txt, b_txt in pinsights:
        draw.rounded_rectangle([lx + 25, iy, lx + lw - 25, iy + 70], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, iy + 14), h_txt, font=get_font(12.5, 'bold'), fill=AIA_RED)
        draw.text((lx + 40, iy + 38), b_txt, font=get_font(12, 'regular'), fill=TEXT_LIGHT_MAIN)
        iy += 85
        
    # Right Card (W=880): Horizontal Bar Chart & Competitor Inconveniences
    rx = 940
    rw = 880
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 35, text="PAIN POINTS & BARRIERS RANKING", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((rx + 25, ly + 65), "고령자 모바일 금융앱 이용 시 주요 불편 사항 (복수응답)", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Horizontal Bar Chart
    bars = [
        ("작은 글씨 크기 & 가독성 저하", 72.4, AIA_RED),
        ("복잡한 본인 인증 & 로그인 절차", 64.8, (239, 68, 68)),
        ("원하는 메뉴 찾기 어려움 (깊은 뎁스)", 58.2, (249, 115, 22)),
        ("어려운 금융 전문 용어 & 설명 부족", 46.5, (59, 130, 246)),
        ("작은 버튼으로 인한 오터치 발생", 38.9, (107, 114, 128))
    ]
    
    by = ly + 120
    for label, pct, bcol in bars:
        draw.text((rx + 25, by), label, font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((rx + rw - 70, by), f"{pct}%", font=get_num_font(13.5, 'black'), fill=bcol)
        # Bar track
        draw.rounded_rectangle([rx + 25, by + 24, rx + rw - 30, by + 40], radius=8, fill=(241, 245, 249))
        bar_w = int((rw - 55) * (pct / 100))
        draw.rounded_rectangle([rx + 25, by + 24, rx + 25 + bar_w, by + 40], radius=8, fill=bcol)
        by += 64
        
    # Summary Callout Box
    draw.rounded_rectangle([rx + 25, ly + 460, rx + rw - 25, ly + 700], radius=12, fill=(255, 241, 244), outline=(254, 205, 217), width=1)
    draw_pill_badge(draw, left_x=rx + 45, cy=ly + 490, text="DESIGN MISSION", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((rx + 45, ly + 520), "AIA+ Phase 2 리뉴얼의 핵심 해결 과제", font=get_font(16, 'bold'), fill=AIA_RED)
    mission_text = (
        "1. 18pt 이상의 큰글씨와 WCAG AAA 8.4:1 고대비 컬러를 전면 도입하여 노안 극복\n"
        "2. 8단계의 복잡한 납부 프로세스를 3-Step으로 압축하고 가상계좌 1-Tap 발급 연동\n"
        "3. 48x48dp 이상의 인체공학 대형 터치 영역과 하단 고정 CTA 버튼으로 오터치 제로화\n"
        "4. 난해한 보험 한자어를 일상적 쉬운 언어로 전면 순화하여 인지 부담 최소화"
    )
    draw.text((rx + 45, ly + 555), mission_text, font=get_font(13, 'regular'), fill=TEXT_LIGHT_MAIN, spacing=8)
    
    draw_slide_footer(draw, 2, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_02.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 03: COMPETITOR ANALYSIS & BENCHMARKING
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 3, 
        "COMPETITOR ANALYSIS", 
        "Competitor Analysis | ", 
        "국내 주요 보험사 시니어 서비스 비교 분석", 
        "삼성화재, 교보생명, 현대해상, 한화생명 등 주요 경쟁사 간편모드 기능 및 UX 벤치마킹", 
        right_badge=("UX BENCHMARKING", "blue")
    )
    
    # Large Comparison Table matching Behance
    table_x = 100
    table_y = 220
    table_w = 1720
    table_h = 730
    draw.rounded_rectangle([table_x, table_y, table_x + table_w, table_y + table_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    # Table Header Row
    headers = [
        ("구분 / 평가 항목", 280),
        ("AIA생명 AIA+ (개선안)", 360),
        ("S사 (삼성화재)", 270),
        ("K사 (교보생명)", 270),
        ("H사 (현대해상)", 270),
        ("W사 (한화생명)", 270)
    ]
    
    hx = table_x
    for htitle, hw in headers:
        draw.rounded_rectangle([hx, table_y, hx + hw, table_y + 55], radius=0, fill=(241, 245, 249) if "AIA" not in htitle else (255, 241, 244))
        draw.line([(hx, table_y), (hx, table_y + table_h)], fill=BORDER_LIGHT, width=1)
        hcol = AIA_RED if "AIA" in htitle else TEXT_LIGHT_MAIN
        draw.text((hx + hw // 2, table_y + 27), htitle, font=get_font(13.5, 'bold'), fill=hcol, anchor='mm')
        hx += hw
    draw.line([(table_x, table_y + 55), (table_x + table_w, table_y + 55)], fill=BORDER_LIGHT, width=2)
    
    # Rows
    rows = [
        ("고령자 전용 간편모드 탑재 여부", "● 원터치 전용 홈 완비", "● 간편모드 제공", "▲ 폰트 확대만 지원", "● 간편모드 제공", "▲ 단순 뷰 모드"),
        ("금융위 가이드라인 충족률", "100% 완전 준수", "85% 부분 준수", "60% 미흡", "80% 부분 준수", "65% 미흡"),
        ("기본 활자 크기 (본문 기준)", "18pt ~ 24pt (초대형)", "16pt", "14pt", "16pt", "14pt"),
        ("보험료 납입 프로세스 뎁스", "3-Step 초간편 여정", "5단계 (인증 복잡)", "7단계 (웹뷰 전환)", "5단계", "6단계"),
        ("가상계좌 1-Tap 즉시 발급", "● 지원 (문자/카톡 발송)", "▲ 신청 후 유선 확인", "X 미지원", "● 지원", "X 미지원"),
        ("영수증 OCR 자동 스캔 청구", "● 실시간 AI 모서리 인식", "▲ 단순 사진 첨부", "▲ 단순 사진 첨부", "● OCR 적용", "▲ 단순 사진 첨부"),
        ("하단 고정 풀와이드 CTA 버튼", "● 56dp 엄지터치 고정", "▲ 상단/중간 혼재", "X 스크롤 하단 숨김", "● 하단 고정", "▲ 중간 배치"),
        ("난해한 보험 한자어 순화", "100% 쉬운 일상어 순화", "일부 순화 (50%)", "레거시 한자어 유지", "일부 순화 (40%)", "레거시 한자어 유지"),
        ("오프라인 고객센터 연결 지원", "● 전담 상담사 원터치 연결", "▲ ARS 번호 연결", "▲ ARS 번호 연결", "● 상담사 연결", "▲ 일반 ARS")
    ]
    
    row_h = 70
    for r_idx, r_data in enumerate(rows):
        ry = table_y + 55 + r_idx * row_h
        # Alternating background
        row_bg = (255, 248, 250) if r_idx % 2 == 1 else (255, 255, 255)
        draw.rectangle([table_x, ry, table_x + table_w, ry + row_h], fill=row_bg)
        draw.line([(table_x, ry + row_h), (table_x + table_w, ry + row_h)], fill=BORDER_LIGHT, width=1)
        
        # Draw columns
        cx = table_x
        for c_idx, (htitle, hw) in enumerate(headers):
            cell_val = r_data[c_idx]
            # Center or Left align
            if c_idx == 0:
                draw.text((cx + 25, ry + row_h // 2), cell_val, font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
            elif c_idx == 1:
                # AIA Column: highlight with red
                draw.rectangle([cx, ry, cx + hw, ry + row_h], fill=(255, 241, 244, 180))
                draw.text((cx + hw // 2, ry + row_h // 2), cell_val, font=get_font(13, 'bold'), fill=AIA_RED, anchor='mm')
            else:
                draw.text((cx + hw // 2, ry + row_h // 2), cell_val, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
            cx += hw
            
    # Bottom Summary Chip
    draw.rounded_rectangle([table_x + 25, table_y + table_h - 45, table_x + table_w - 25, table_y + table_h - 12], radius=8, fill=(241, 245, 249))
    draw.text((table_x + table_w // 2, table_y + table_h - 28), "💡 벤치마킹 결론: AIA생명은 3-Step 납입, 가상계좌 1-Tap, 18pt 대형 활자, 하단 고정 CTA로 경쟁사 대비 압도적인 고령자 접근성을 확보함", font=get_font(12, 'bold'), fill=AIA_RED, anchor='mm')
    
    draw_slide_footer(draw, 3, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_03.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 04: KEY INSIGHTS & STRATEGY (4 Rounded Grey Cards)
# -------------------------------------------------------------
def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 4, 
        "KEY INSIGHTS", 
        "Key Insights | ", 
        "사용자 리서치 기반 4대 디자인 전략 도출", 
        "조사 및 벤치마킹을 통해 정립한 시니어 금융 UX의 핵심 방향성", 
        right_badge=("CORE STRATEGY", "purple")
    )
    
    # 4 Large Horizontal Cards matching Behance Key Insights section
    insights = [
        {
            "num": "INSIGHT 01",
            "title": "가독성(Readability) 극대화: 18pt+ 대형 활자 및 고대비 8.4:1 보장",
            "desc": "노안 및 시력 저하가 발생한 고령 고객이 별도의 돋보기 안경 없이도 계약 정보와 납입 금액을 즉각 판독할 수 있도록 기본 본문 18pt, 핵심 금액 24pt 이상의 대형 활자를 적용하고 WCAG AAA 등급 고대비율을 완벽하게 구현합니다.",
            "theme": "red"
        },
        {
            "num": "INSIGHT 02",
            "title": "단순성(Simplicity) 원칙: 복잡한 단계를 3-Step으로 압축한 제로-마찰 여정",
            "desc": "레거시 앱의 8단계 메뉴 탐색 및 중도 이탈을 방지하기 위해, 홈 화면에서 한 번의 터치로 당월 미납 내역을 확인하고 기등록 계좌 또는 가상계좌를 통해 3단계 이내에 즉시 납부를 완결할 수 있는 초단축 플로우를 구축합니다.",
            "theme": "blue"
        },
        {
            "num": "INSIGHT 03",
            "title": "조작성(Usability) 혁신: 48x48dp 이상 인체공학 터치 타겟 & 하단 고정 CTA",
            "desc": "손떨림 및 관절 유연성 저하로 인한 인접 버튼 오터치 문제를 원천 차단하기 위해 모든 인터랙션 버튼에 48dp 이상의 크기와 16dp의 안전 마진을 부여하고, 엄지손가락 파지 구역인 하단에 56dp 풀와이드 액션 버튼을 영구 고정합니다.",
            "theme": "green"
        },
        {
            "num": "INSIGHT 04",
            "title": "안심성(Reassurance) 케어: 쉬운 일상어 순화 및 실시간 문자/알림톡 피드백",
            "desc": "'실효', '부활', '기납입' 등 난해한 금융 한자어를 '효력 회복하기', '지금까지 낸 돈' 등으로 100% 일상어로 순화하고, 결제 및 신청 완료 즉시 카카오 알림톡으로 확인증을 전송하여 고령층의 심리적 불안감을 해소합니다.",
            "theme": "amber"
        }
    ]
    
    card_w = 1720
    card_h = 160
    start_x = 100
    start_y = 220
    
    for idx, ins in enumerate(insights):
        cy = start_y + idx * (card_h + 25)
        # Rounded grey card container matching Behance
        draw.rounded_rectangle([start_x, cy, start_x + card_w, cy + card_h], radius=16, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
        
        # Left Tag
        draw_pill_badge(draw, left_x=start_x + 30, cy=cy + 40, text=ins["num"], font=get_font(11, 'bold'), theme=ins["theme"], pad_x=14, height=26)
        draw.text((start_x + 160, cy + 30), ins["title"], font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        # Description
        lines = wrap_text(ins["desc"], get_font(13.5, 'regular'), card_w - 60, draw)
        py = cy + 78
        for line in lines:
            draw.text((start_x + 30, py), line, font=get_font(13.5, 'regular'), fill=TEXT_LIGHT_SUB)
            py += 22
            
    draw_slide_footer(draw, 4, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_04.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
