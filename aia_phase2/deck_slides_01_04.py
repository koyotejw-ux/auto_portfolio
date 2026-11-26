import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from deck_common import (
    W, H, BASE_DIR, CORE_DIR, QI_DIR, OUT_DIR,
    AIA_RED, AIA_RED_DARK, AIA_RED_LIGHT, BG_DARK, CARD_DARK, BORDER_DARK,
    TEXT_DARK_MAIN, TEXT_DARK_SUB, BG_LIGHT, CARD_LIGHT, BORDER_LIGHT,
    TEXT_LIGHT_MAIN, TEXT_LIGHT_SUB,
    get_font, get_num_font, wrap_text, draw_pill_badge,
    draw_slide_header, draw_slide_footer, draw_phone_mockup
)

# -------------------------------------------------------------
# SLIDE 01: HERO COVER (Dark Mode Luxury Obsidian Red)
# -------------------------------------------------------------
def make_slide_01():
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # 1. Subtle glowing radial background
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([60, 100, 900, 940], fill=(211, 17, 69, 28))
    gdraw.ellipse([1000, 200, 1800, 1000], fill=(158, 0, 43, 22))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    img.paste(glow, (0, 0), glow)
    
    # Grid lines for high-tech architectural feeling
    for gx in range(100, 1821, 140):
        draw.line([(gx, 60), (gx, 1020)], fill=(25, 32, 45), width=1)
    for gy in range(80, 1021, 140):
        draw.line([(100, gy), (1820, gy)], fill=(25, 32, 45), width=1)
        
    draw = ImageDraw.Draw(img)
    
    # 2. Left Column: Typography & Project Meta
    # Top Tag
    draw_pill_badge(draw, left_x=120, cy=130, text="AIA LIFE · GLOBAL FINTECH INNOVATION", font=get_font(11, 'bold'), theme='red', dark_mode=True, pad_x=14, height=28)
    draw_pill_badge(draw, left_x=430, cy=130, text="Qi DESIGN SYSTEM v3.3", font=get_font(11, 'bold'), theme='gray', dark_mode=True, pad_x=12, height=28)
    
    # Main Title
    draw.text((120, 185), "AIA생명 AIA+ Phase 2", font=get_font(48, 'black'), fill=(255, 255, 255))
    draw.text((120, 255), "고령자 친화 배리어프리 금융 UX", font=get_font(38, 'bold'), fill=(255, 80, 120))
    draw.text((120, 315), "& 10대 비대면 코어 서비스 리뉴얼", font=get_font(34, 'bold'), fill=(241, 245, 249))
    
    # Project Subtitle & Description
    desc_kr = (
        "금융위원회 '고령자 친화적 모바일 금융앱 가이드라인' 100% 준수\n"
        "6070 액티브 시니어를 위한 제로-뎁스(Zero-Depth) 직관 탐색 아키텍처와\n"
        "Qi 글로벌 디자인 시스템 v3.3 기반의 단일 소스 멀티 테마 프로덕트 디자인"
    )
    draw.text((120, 395), desc_kr, font=get_font(16.5, 'regular'), fill=(160, 175, 195), spacing=10)
    
    # Key Metric Cards (Left Bottom)
    metrics = [
        ("완수율 (Senior Task)", "89.4%", "▲ 31.2%p 향상"),
        ("과업 소요 시간", "1분 20초", "▼ 58% 단축"),
        ("CS 문의 감소율", "-44.6%", "가상계좌 1-Tap 즉시발급"),
        ("디자인 토큰 규격", "150+ Tokens", "Qi DS v3.3 준수")
    ]
    card_y = 525
    for i, (m_title, m_val, m_sub) in enumerate(metrics):
        cx = 120 + (i % 2) * 260
        cy = card_y + (i // 2) * 115
        cw, ch = 245, 100
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=14, fill=CARD_DARK, outline=BORDER_DARK, width=1)
        draw.text((cx + 18, cy + 18), m_title, font=get_font(12, 'medium'), fill=(148, 163, 184))
        draw.text((cx + 18, cy + 40), m_val, font=get_num_font(24, 'black'), fill=(255, 255, 255))
        draw.text((cx + 18, cy + 72), m_sub, font=get_font(11, 'bold'), fill=(255, 90, 130) if "▲" in m_sub or "단축" in m_sub else (52, 211, 153))
        
    # Project Scope & Specs Bar
    spec_box_y = 780
    draw.rounded_rectangle([120, spec_box_y, 640, spec_box_y + 160], radius=16, fill=(20, 26, 38), outline=BORDER_DARK, width=1)
    specs = [
        ("플랫폼", "Android · iOS (Flutter / Web Hybrid)"),
        ("기간 / 기여도", "2024.08 - 2024.11 (4개월) / UI/UX 100% 총괄"),
        ("핵심 도메인", "보험료 납입, 계약대출 상환, 보험금 간편청구, 실효부활"),
        ("표준 및 인증", "금융위 고령자 가이드라인 · WCAG 2.1 AAA 8.4:1 고대비")
    ]
    for idx, (label, val) in enumerate(specs):
        sy = spec_box_y + 18 + idx * 34
        draw.text((140, sy), label, font=get_font(12, 'bold'), fill=(255, 90, 130))
        draw.text((245, sy), val, font=get_font(12, 'medium'), fill=(226, 232, 240))
        
    # 3. Right Column: Device Trio Mockup (AIA+ Actual App Screens)
    # Screen 1: General Main (Left angled/backdrop)
    draw_phone_mockup(img, os.path.join(CORE_DIR, "screen_general_main.png"), cx=880, cy=580, phone_w=280, phone_h=580)
    # Screen 2: Senior Home Hero (Center, larger & front)
    draw_phone_mockup(img, os.path.join(CORE_DIR, "screen_senior_main_home.png"), cx=1190, cy=540, phone_w=320, phone_h=660)
    # Screen 3: Premium Payment (Right, front)
    draw_phone_mockup(img, os.path.join(CORE_DIR, "screen_pay_list_senior.png"), cx=1500, cy=580, phone_w=280, phone_h=580)
    
    # 4. Floating Feature Badges on right side
    badges = [
        (1050, 230, "고령자 전용 원터치 대시보드", 'green'),
        (1360, 200, "18pt+ 대형 활자 & 고대비 8.4:1", 'red'),
        (1650, 750, "3-Step 초간편 보험료 납부", 'blue')
    ]
    for bx, by, btext, btheme in badges:
        draw_pill_badge(draw, cx=bx, cy=by, text=btext, font=get_font(11.5, 'bold'), theme=btheme, solid=True, dark_mode=True, pad_x=16, height=32)
        
    draw_slide_footer(draw, 1, 12, dark_mode=True)
    out_path = os.path.join(OUT_DIR, "slide_01.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 02: MARKET CONTEXT & PROBLEM DEFINITION
# -------------------------------------------------------------
def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 2, "MARKET BACKGROUND & PROBLEM", "초고령 사회 진입과 금융 디지털 격차,", " 비대면 금융의 치명적 한계", "디지털 소외 계층의 급증과 금융위원회 가이드라인 준수를 위한 전략적 리뉴얼 배경", right_badge=("REGULATION COMPLIANCE", "red"))
    
    # 3 Column Comparison Layout
    cols = [
        {
            "tag": "MARKET SHIFT",
            "title": "초고령 사회 진입 & 자산 세대 이동",
            "stat": "20.3%",
            "stat_label": "2025년 대한민국 65세 이상 인구 비중",
            "points": [
                ("보험 가입자 중 60대 이상 42.8%", "보험 유지 및 수령의 핵심 고객층이 고령층으로 급격히 전환"),
                ("디지털 비대면 전환 압력 가속화", "영업점 및 대면 설계사 창구 축소로 앱을 통한 비대면 업무 필수화"),
                ("금융 자산 집중 세대의 모바일 요구", "연금, 저축성 보험, 계약 대출 등 핵심 금융 거래의 55% 보유")
            ]
        },
        {
            "tag": "PAIN POINTS",
            "title": "레거시 모바일 금융의 3대 장벽",
            "stat": "68.4%",
            "stat_label": "고령층 비대면 금융앱 중도 이탈률",
            "points": [
                ("정보 과밀 & 8pt 미세 폰트", "작은 텍스트와 과도한 배너로 주요 계약 내용 및 납입 금액 인지 불가"),
                ("복잡한 8단계 뎁스 & 딥 네비게이션", "메뉴 탐색에만 평균 4.2분 소요, 목표 기능 진입 전 세션 타임아웃"),
                ("난해한 보험 한자어 & 금융 전문 용어", "'부활(Revival)', '실효(Lapse)', '기납입보험료' 등 직관적 이해 불가능")
            ]
        },
        {
            "tag": "GOVERNMENT POLICY",
            "title": "금융위원회 가이드라인 의무화",
            "stat": "100%",
            "stat_label": "고령자 친화적 모바일 금융앱 준수 기준",
            "points": [
                ("원터치 간편모드 별도 탑재 의무", "진입 즉시 핵심 기능(조회, 납입, 청구)만 배치하는 전용 홈 제공"),
                ("최소 터치 영역 48x48dp 보장", "오터치 및 실수 방지를 위한 버튼 마진 및 피드백 진동 의무"),
                ("가상계좌 & 쉬운 인증 체계 도입", "공동인증서/복잡한 본인인증 탈피, 6자리 PIN & 계좌 1-Tap 연동")
            ]
        }
    ]
    
    col_w = 520
    col_gap = 30
    start_x = 100
    start_y = 220
    
    for i, col in enumerate(cols):
        cx = start_x + i * (col_w + col_gap)
        draw.rounded_rectangle([cx, start_y, cx + col_w, start_y + 730], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Col Header
        draw_pill_badge(draw, left_x=cx + 25, cy=start_y + 35, text=col["tag"], font=get_font(10.5, 'bold'), theme='red' if i==1 else ('blue' if i==0 else 'amber'), pad_x=12, height=24)
        draw.text((cx + 25, start_y + 65), col["title"], font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        # Stat Box
        stat_bg = (255, 241, 244) if i==1 else (241, 245, 249)
        draw.rounded_rectangle([cx + 25, start_y + 115, cx + col_w - 25, start_y + 205], radius=12, fill=stat_bg)
        stat_col = AIA_RED if i==1 else ((0, 81, 255) if i==0 else (217, 119, 6))
        draw.text((cx + 45, start_y + 130), col["stat"], font=get_num_font(34, 'black'), fill=stat_col)
        draw.text((cx + 45, start_y + 175), col["stat_label"], font=get_font(12, 'medium'), fill=TEXT_LIGHT_SUB)
        
        # Points
        py = start_y + 235
        for h_text, b_text in col["points"]:
            draw.ellipse([cx + 28, py + 6, cx + 34, py + 12], fill=AIA_RED if i==1 else (59, 130, 246))
            draw.text((cx + 45, py), h_text, font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN)
            lines = wrap_text(b_text, get_font(12.5, 'regular'), col_w - 70, draw)
            ly = py + 24
            for line in lines:
                draw.text((cx + 45, ly), line, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
                ly += 18
            py = ly + 22
            
    draw_slide_footer(draw, 2, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_02.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 03: TARGET PERSONA & USER EMPATHY
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 3, "PERSONA & USER RESEARCH", "세대별 금융 행동 분석을 통한", " 듀얼 모드 페르소나 설계", "6070 시니어 실버 세대와 3040 디지털 네이티브의 극명한 니즈 격차 해소", right_badge=("DUAL PERSONA MAPPING", "blue"))
    
    personas = [
        {
            "tag": "PRIMARY PERSONA · 시니어 6070",
            "name": "박정자 님 (68세 · 은퇴 후 자영업)",
            "badge": "고령자 간편 모드 대상",
            "quote": "\"글씨가 너무 작고 뭐가 뭔지 몰라서 매번 딸한테 물어보거나 은행 창구에 직접 갔어요.\"",
            "char": "보유 계약 3건 (건강보험 2건, 연금보험 1건) · 노안 및 손떨림 증상 · 스마트폰은 주로 카카오톡과 유튜브 이용",
            "goals": [
                "이번 달 내야 할 보험료가 얼마인지 한눈에 바로 알고 싶음",
                "복잡한 공인인증서 없이 기존 통장이나 가상계좌로 바로 입금하고 싶음",
                "병원 다녀온 영수증을 사진 찍어 쉽게 병원비 청구하고 싶음"
            ],
            "frustrations": [
                "약관 동의 화면의 깨알 같은 글씨와 끝없는 스크롤로 인한 피로감",
                "버튼이 너무 작아 옆 버튼이 잘못 눌려 처음부터 다시 시작하는 번거로움",
                "'계약자', '피보험자', '수익자' 용어가 헷갈려 신청 오류 빈번"
            ],
            "solution": "18pt+ 대형 활자, 단일 화면 1개 과업, 제로-뎁스 원터치 홈, 가상계좌 문자 발송 연동"
        },
        {
            "tag": "SECONDARY PERSONA · 3040 세대",
            "name": "이민호 님 (39세 · IT 기업 팀장)",
            "badge": "일반 통합 모드 대상",
            "quote": "\"보험료 납입뿐 아니라 계약 대출 한도와 헬스케어 리워드까지 한곳에서 빠르게 관리하고 싶습니다.\"",
            "char": "보유 계약 4건 (종신 1건, 암보험 2건, 실손 1건) · 금융 핀테크 앱 헤비 유저 · 신속한 자산 관리 선호",
            "goals": [
                "보장 내역 및 해약환급금 추이를 실시간 차트로 종합 관제",
                "보험계약대출 신청 후 1분 이내 주거래 통장으로 즉시 입금 희망",
                "바이오/지문 인증을 통한 무자각 초고속 로그인 및 결제"
            ],
            "frustrations": [
                "불필요한 설명이 길고 화면 전환이 느려 빠른 업무 처리가 지연될 때",
                "자주 쓰는 메뉴가 깊은 카테고리에 숨겨져 있어 탐색 번거로움"
            ],
            "solution": "10대 코어 서비스 원스톱 퀵 내비게이션, 맞춤형 자산 대시보드, 바이오 간편 인증"
        }
    ]
    
    pw = 800
    ph = 730
    for idx, p in enumerate(personas):
        px = 100 + idx * 820
        py = 220
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Tag & Name
        draw_pill_badge(draw, left_x=px + 30, cy=py + 35, text=p["tag"], font=get_font(11, 'bold'), theme='red' if idx==0 else 'blue', pad_x=12, height=24)
        draw_pill_badge(draw, left_x=px + pw - 180, cy=py + 35, text=p["badge"], font=get_font(10.5, 'bold'), theme='gray', pad_x=10, height=24)
        
        draw.text((px + 30, py + 65), p["name"], font=get_font(22, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        # Quote Box
        q_bg = (255, 241, 244) if idx==0 else (239, 246, 255)
        draw.rounded_rectangle([px + 30, py + 110, px + pw - 30, py + 175], radius=10, fill=q_bg)
        draw.text((px + 45, py + 128), p["quote"], font=get_font(13.5, 'bold'), fill=AIA_RED if idx==0 else (29, 78, 216))
        
        # Characteristics
        draw.text((px + 30, py + 195), "사용자 특성 및 모바일 숙련도", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((px + 30, py + 220), p["char"], font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
        
        # Goals
        draw.text((px + 30, py + 265), "핵심 니즈 & 목표 (Key Goals)", font=get_font(13, 'bold'), fill=(16, 185, 129))
        gy = py + 295
        for g in p["goals"]:
            draw.text((px + 30, gy), "✔", font=get_font(12, 'bold'), fill=(16, 185, 129))
            draw.text((px + 52, gy), g, font=get_font(12.5, 'medium'), fill=TEXT_LIGHT_MAIN)
            gy += 28
            
        # Frustrations
        draw.text((px + 30, gy + 15), "기존 레거시 페인포인트 (Frustrations)", font=get_font(13, 'bold'), fill=AIA_RED)
        fy = gy + 45
        for f in p["frustrations"]:
            draw.text((px + 30, fy), "✖", font=get_font(12, 'bold'), fill=AIA_RED)
            draw.text((px + 52, fy), f, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
            fy += 28
            
        # Solution Box
        s_bg = (248, 250, 252)
        draw.rounded_rectangle([px + 30, py + ph - 105, px + pw - 30, py + ph - 25], radius=12, fill=s_bg, outline=BORDER_LIGHT, width=1)
        draw.text((px + 45, py + ph - 92), "💡 UX 아키텍처 대응 전략", font=get_font(12, 'bold'), fill=AIA_RED if idx==0 else (0, 81, 255))
        draw.text((px + 45, py + ph - 68), p["solution"], font=get_font(12.5, 'medium'), fill=TEXT_LIGHT_MAIN)
        
    draw_slide_footer(draw, 3, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_03.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 04: DUAL-MODE INFORMATION ARCHITECTURE (IA)
# -------------------------------------------------------------
def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 4, "INFORMATION ARCHITECTURE", "고령자 간편 모드와 일반 모드의", " 듀얼 IA 구조 설계", "금융위 가이드라인에 따른 원터치 모드 전환 및 제로-뎁스(Zero-Depth) 탐색 트리", right_badge=("DUAL IA MATRIX", "purple"))
    
    # 2 Big Cards: Left = Senior Mode (Zero-Depth), Right = General Mode (10 Domains)
    # Left Box
    lw = 780
    lh = 730
    lx = 100
    ly = 220
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=(254, 205, 217), width=2)
    draw_pill_badge(draw, left_x=lx + 25, cy=ly + 35, text="고령자 친화 간편 모드 (SENIOR SIMPLE MODE)", font=get_font(11, 'bold'), theme='red', pad_x=14, height=26)
    draw.text((lx + 25, ly + 68), "단일 뎁스 기반 직관적 카드 4대 핵심 과업 집중형 IA", font=get_font(17, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    senior_modules = [
        ("01. 내 보험 한눈에 보기", "보유 계약 건수 및 이번 달 내야 할 보험료 즉시 확인 (조회)", ["계약 상태 표시", "당월 납입액", "미납 안내 알림"]),
        ("02. 보험료 바로 내기", "복잡한 단계 없는 3-Step 즉시 납부 (주거래 계좌 or 가상계좌)", ["기등록 계좌 1-Tap", "가상계좌 문자발송", "자동이체 계좌 등록"]),
        ("03. 병원비 보험금 청구", "영수증 사진 촬영 즉시 청구 접수 (카메라 OCR 연동)", ["영수증 즉시 촬영", "수령 계좌 확인", "진행 현황 문자 알림"]),
        ("04. 큰글씨 고객센터 연결", "ARS 복잡한 버튼 없이 전문 상담원 1:1 즉시 연결", ["전담 시니어 상담원", "원격 화면 지원", "가장 가까운 고객센터"])
    ]
    
    sy = ly + 115
    for title, desc, tags in senior_modules:
        draw.rounded_rectangle([lx + 25, sy, lx + lw - 25, sy + 130], radius=12, fill=(255, 248, 250), outline=(254, 226, 232), width=1)
        draw.text((lx + 45, sy + 18), title, font=get_font(15, 'bold'), fill=AIA_RED)
        draw.text((lx + 45, sy + 44), desc, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
        # tags
        tx = lx + 45
        for tag in tags:
            tw = draw_pill_badge(draw, left_x=tx, cy=sy + 92, text=tag, font=get_font(10.5, 'medium'), theme='gray', pad_x=10, height=22)
            tx += tw + 10
        sy += 145
        
    # Right Box
    rx = 920
    draw.rounded_rectangle([rx, ly, rx + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 35, text="일반 모드 통합 IA (GENERAL ENTERPRISE MODE)", font=get_font(11, 'bold'), theme='blue', pad_x=14, height=26)
    draw.text((rx + 25, ly + 68), "10대 비대면 금융 도메인 및 개인화 자산 포트폴리오", font=get_font(17, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    general_domains = [
        ("계약 관리 도메인", ["보유계약 상세조회", "해약환급금 모의계산", "보장내역 분석", "증권 및 증명서 발급"]),
        ("보험료 납입 도메인", ["실시간 보험료 납부", "자동이체 계좌 변경", "납입 일자 변경", "실효계약 부활신청"]),
        ("대출 및 금융 도메인", ["보험계약대출 신청", "대출 원리금 상환", "대출 한도 조회", "자동송금 서비스"]),
        ("보상 및 청구 도메인", ["사고보험금 청구", "청구 진행상태 조회", "추가서류 제출", "청구 이력 조회"]),
        ("헬스케어 & AIA 바이탈리티", ["걸음수 리워드 연동", "건강검진 데이터 연동", "통합 웰니스 미션", "멤버십 혜택 관리"])
    ]
    
    gy = ly + 115
    for d_title, d_items in general_domains:
        draw.rounded_rectangle([rx + 25, gy, rx + lw - 25, gy + 105], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((rx + 45, gy + 16), d_title, font=get_font(14.5, 'bold'), fill=(29, 78, 216))
        # items in 2x2 grid
        for i_idx, item in enumerate(d_items):
            ix = rx + 45 + (i_idx % 2) * 340
            iy = gy + 45 + (i_idx // 2) * 26
            draw.text((ix, iy), f"•  {item}", font=get_font(12, 'regular'), fill=TEXT_LIGHT_MAIN)
        gy += 120
        
    draw_slide_footer(draw, 4, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_04.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
