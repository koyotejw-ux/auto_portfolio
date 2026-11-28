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
# SLIDE 09: UI SCREENS PART 2 (Virtual Account, PIN, Signature, Revival)
# -------------------------------------------------------------
def make_slide_09():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 9, 
        "UI SCREENS · EXPANDED SERVICES", 
        "UI Screens | ", 
        "가상계좌, 인증 및 부활 서비스 화면 (Row 2)", 
        "가상계좌 즉시 발급, 48px 대형 PIN 키패드, 간편 전자서명 수단 선택, 실효부활", 
        right_badge=("PRODUCTION UI", "blue")
    )
    
    screens = [
        ("05. 본인인증 & 주민번호", "figma_id_verification.png", "주민등록번호 뒤 7자리 간편 입력 및 보안 인증"),
        ("06. 보험사 다이렉트 선택", "figma_select_insurer.png", "AIA생명 및 주요 제휴 보험사 간편 조회/선택"),
        ("07. 전자서명 확인/완료", "figma_signature_done.png", "터치 전자서명 날인 및 수령 계좌 1-Tap 확정"),
        ("08. 대형 PIN 키패드", "screen_login_pin.png", "48px 대형 숫자 키패드로 오터치 방지 간편 인증")
    ]
    
    sw = 395
    sh = 730
    start_x = 100
    start_y = 220
    
    for i, (stitle, s_file, s_desc) in enumerate(screens):
        sx = start_x + i * (sw + 23)
        draw.rounded_rectangle([sx, start_y, sx + sw, start_y + sh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Tag & Title (Clean top positioning with generous 25px breathing margin)
        draw_pill_badge(draw, left_x=sx + 20, cy=start_y + 32, text=f"SCREEN 0{i+5}", font=get_font(10.5, 'bold'), theme='blue' if i<3 else 'purple', pad_x=12, height=22)
        draw.text((sx + 20, start_y + 58), stitle, font=get_font(16.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        screen_path = os.path.join(CORE_DIR, s_file)
        if not os.path.exists(screen_path) and s_file == "screen_general_main_clean.png":
            screen_path = os.path.join(CORE_DIR, "screen_general_main.png")
        draw_phone_mockup(img, screen_path, cx=sx + sw // 2, cy=start_y + 348, phone_w=225, phone_h=485, bezel=6, radius=26)
        
        if i < 3:
            arrow_x = sx + sw + 4
            draw_arrow(draw, (arrow_x, start_y + 348), (arrow_x + 15, start_y + 348), col=(59, 130, 246), width=2, arrow_size=6)
        
        draw.rounded_rectangle([sx + 20, start_y + sh - 85, sx + sw - 20, start_y + sh - 20], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        lines = wrap_text(s_desc, get_font(11.5, 'regular'), sw - 56, draw)
        dy = start_y + sh - 74
        for line in lines:
            draw.text((sx + 28, dy), line, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN)
            dy += 18
            
    draw_slide_footer(draw, 9, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_09.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 10: CORE JOURNEY - SENIOR MODE CLAIMS (고령자모드 보험금 청구 전용)
# -------------------------------------------------------------
def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 10, 
        "CORE JOURNEY · SENIOR CLAIMS", 
        "Core Journey | ", 
        "고령자모드 보험금 청구 화면설계 및 4단계 UI", 
        "화면설계서 원본 기반: 서류 준비 안내, 영수증 OCR 촬영, 수령 계좌 선택, 청구서 접수 완료까지 4단계 엔드투엔드", 
        right_badge=("SENIOR CLAIMS CORE", "green")
    )
    
    # 4 Sequential UI Screens for Insurance Claims (From authentic Figma file)
    claim_steps = [
        {
            "tag": "STEP 01",
            "title": "청구 서류 준비 안내",
            "screen": "figma_claim_step1.png",
            "desc": "병원비 청구 필수 서류 안내 및 간편 청구 가이드 제공으로 서류 누락 원천 방지"
        },
        {
            "tag": "STEP 02",
            "title": "서류 등록 & 사진 촬영",
            "screen": "figma_claim_step2.png",
            "desc": "진단서/영수증 글씨 식별 안내, 구겨짐·그림자 자동 보정 및 모바일 사진 업로드"
        },
        {
            "tag": "STEP 03",
            "title": "청구 정보 & 전자서명",
            "screen": "figma_claim_step3.png",
            "desc": "지정 수령 계좌(카카오뱅크 등) 자동 세팅 및 원터치 전자서명 날인 지원"
        },
        {
            "tag": "STEP 04",
            "title": "내용 최종확인 및 제출",
            "screen": "figma_claim_step4.png",
            "desc": "피보험자·사고내용 최종 확인, 1-Tap 청구서 제출 및 실시간 접수 번호 발급"
        }
    ]
    
    sw = 395
    sh = 730
    start_x = 100
    start_y = 220
    
    for i, step in enumerate(claim_steps):
        sx = start_x + i * (sw + 23)
        draw.rounded_rectangle([sx, start_y, sx + sw, start_y + sh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Tag & Title (Clean top positioning with generous 25px breathing margin)
        draw_pill_badge(draw, left_x=sx + 20, cy=start_y + 32, text=step["tag"], font=get_font(10.5, 'bold'), theme='green' if i in [0, 3] else 'blue', pad_x=12, height=22)
        draw.text((sx + 20, start_y + 58), step["title"], font=get_font(16.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        screen_path = os.path.join(CORE_DIR, step["screen"])
        draw_phone_mockup(img, screen_path, cx=sx + sw // 2, cy=start_y + 348, phone_w=225, phone_h=485, bezel=6, radius=26)
        
        if i < 3:
            arrow_x = sx + sw + 4
            draw_arrow(draw, (arrow_x, start_y + 348), (arrow_x + 15, start_y + 348), col=(16, 185, 129), width=2, arrow_size=6)
        
        # Bottom Description Card
        draw.rounded_rectangle([sx + 20, start_y + sh - 85, sx + sw - 20, start_y + sh - 20], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        lines = wrap_text(step["desc"], get_font(11.5, 'regular'), sw - 56, draw)
        dy = start_y + sh - 74
        for line in lines:
            draw.text((sx + 28, dy), line, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN)
            dy += 18
            
    draw_slide_footer(draw, 10, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_10.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 11: PROJECT REFLECTION & OUTCOMES (4 Stat Cards & STAR)
# -------------------------------------------------------------
# -------------------------------------------------------------
# SLIDE 11: PROJECT REFLECTION & OUTCOMES (KPIs, STAR & AIA Production Assets)
# -------------------------------------------------------------
def make_slide_11():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 11, 
        "PROJECT REFLECTION & OUTCOMES", 
        "Project Reflection & Outcomes | ", 
        "AIA+ 실물 작업물 검증 성과 지표 & 200자 STAR 회고", 
        "금융위 가이드라인 100% 충족, 폰트 2배 확대, 완수율 90%, 소요시간 50% 단축 정량 지표와 AIA 실물 설계 회고", 
        right_badge=("KEY OUTCOMES", "red")
    )
    
    card_y = 220
    card_h = 730
    
    # Left Column: 4 Stat KPI Cards + Standards Compliance Box (W=680)
    lx = 100
    lw = 680
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="KEY QUANTITATIVE METRICS", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 65), "정량적 사용성 개선 성과 지표", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    metrics = [
        {"val": "100%", "label": "금융위 가이드라인 충족률", "sub": "18pt 이상 활자 & 고대비 명도비 AAA 완벽 달성"},
        {"val": "2x", "label": "핵심 텍스트 크기 확대", "sub": "일반 14pt 대비 고령자 모드 18~28pt 2배 확대"},
        {"val": "90%", "label": "고령층 보험료 납부 완수율", "sub": "기존 42% 대비 +48%p 대폭 상승 (사용성 테스트)"},
        {"val": "-50%", "label": "과업 완수 소요시간 단축", "sub": "평균 6분 30초에서 3분 10초로 대폭 단축"}
    ]
    
    gw = 300
    gh = 230
    grid_coords = [
        (lx + 25, card_y + 105),
        (lx + 355, card_y + 105),
        (lx + 25, card_y + 355),
        (lx + 355, card_y + 355)
    ]
    
    for (gx, gy), m in zip(grid_coords, metrics):
        draw.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((gx + gw//2, gy + 75), m["val"], font=get_num_font(48, 'black'), fill=AIA_RED, anchor='mm')
        draw.text((gx + gw//2, gy + 140), m["label"], font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
        lines = wrap_text(m["sub"], get_font(11, 'regular'), gw - 35, draw)
        ly = gy + 175
        for line in lines:
            draw.text((gx + gw//2, ly), line, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
            ly += 17

    # Bottom Compliance & Standards Box in Left Card
    draw.rounded_rectangle([lx + 25, card_y + 605, lx + lw - 25, card_y + card_h - 25], radius=12, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((lx + 45, card_y + 625), "• 가이드라인 준수", font=get_font(11.5, 'bold'), fill=AIA_RED)
    draw.text((lx + 155, card_y + 625), "금융위원회 고령자 친화 모바일 금융앱 가이드라인 100% 충족", font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 45, card_y + 652), "• 접근성 인증 지표", font=get_font(11.5, 'bold'), fill=(16, 185, 129))
    draw.text((lx + 155, card_y + 652), "WCAG 2.1 AAA 고대비 명도비(7:1 이상) 및 최소 48px 터치 영역", font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 45, card_y + 679), "• 유니버설 가치", font=get_font(11.5, 'bold'), fill=(59, 130, 246))
    draw.text((lx + 155, card_y + 679), "고령층뿐 아니라 전 연령대 사용자 인지 피로도 40% 이상 경감", font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN)

    # Right Column: AIA Production Work Deliverables & 200자 STAR Method (W=1000)
    rx = 820
    rw = 1000
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=card_y + 35, text="AIA PRODUCTION DELIVERABLES & STAR RETROSPECTIVE", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 30, card_y + 65), "AIA 실물 설계 작업물 기반 문제해결 STAR 회고", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # 4 STAR Cards with Embedded Authentic AIA Screen Mockups
    # S (Situation): 복잡한 일반모드 화면 (screen_general_main.png)
    # T (Task): 고령자 친화 메인 게이트 설계 (clean_phone_gate.png)
    # A (Action): 원터치 핵심 비대면 과업 화면 (inner_pay1.png)
    # R (Result): 청구 완료 및 대출 상환 성공 (inner_loan1.png)
    star_items = [
        {
            "step": "S",
            "title": "Situation (상황 및 배경)",
            "text": "보험사 디지털 전환 가속화로 모바일 앱 이용률이 급증했으나, 기존 일반모드는 작은 폰트(12~14pt), 복잡한 증권번호 나열, 수많은 서브메뉴로 인해 65세 이상 고령 고객의 비대면 과업 이탈률이 58%에 달하며 심각한 디지털 소외와 콜센터 과부하가 발생했습니다.",
            "img": "aia_phase2/core_screens/screen_general_main.png",
            "img_label": "BEFORE: 일반모드 복잡한 UI"
        },
        {
            "step": "T",
            "title": "Task (과제 및 설계 목표)",
            "text": "금융위원회 고령자 친화 모바일 앱 가이드라인을 100% 충족하면서, AIA생명 글로벌 표준 디자인 시스템(Qi v3.3) 거버넌스를 엄격히 준수하는 독립적인 '고령자 전용 모드'와 제로-뎁스 5대 핵심 비대면 과업 구조를 확립하는 것을 최우선 목표로 설정했습니다.",
            "img": "aia_phase2/core_screens/clean_phone_gate.png",
            "img_label": "AFTER: 간편홈 메인 게이트"
        },
        {
            "step": "A",
            "title": "Action (AIA 실물 설계 및 해결 과정)",
            "text": "Figma 공식 화면설계서(PLSCMV002) 기반 시니어 전용 18~28pt 폰트 스케일과 56dp 풀와이드 고정 CTA를 설계했습니다. 화면당 1개 과업만 제시하고, 기등록 주거래 계좌 자동 연동과 비밀번호 분실 시 가상계좌 대체 발급 경로를 구축하여 인지적 마찰을 원천 제거했습니다.",
            "img": "aia_phase2/core_screens/inner_pay1.png",
            "img_label": "AIA 실물: 보험료 즉시납입 UI"
        },
        {
            "step": "R",
            "title": "Result (성과 지표 및 유니버설 가치)",
            "text": "고령층 대상 사용성 테스트에서 과업 완수율 90%(+48%p 개선), 소요시간 50% 단축을 달성했습니다. 배리어프리 디자인이 특정 연령대 전유물이 아닌, 모든 사용자의 인지 피로도를 줄이고 브랜드 신뢰도를 극대화하는 금융 플랫폼의 핵심 경쟁력임을 실증했습니다.",
            "img": "aia_phase2/core_screens/inner_loan1.png",
            "img_label": "AIA 실물: 계약대출 상환 UI"
        }
    ]
    
    sy = card_y + 105
    for s in star_items:
        draw.rounded_rectangle([rx + 25, sy, rx + rw - 25, sy + 140], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        
        # Left Badge for Step
        draw.rounded_rectangle([rx + 40, sy + 15, rx + 75, sy + 50], radius=8, fill=AIA_RED if s["step"] in ['S', 'R'] else (59, 130, 246))
        draw.text((rx + 57, sy + 32), s["step"], font=get_font(18, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        # Title
        draw.text((rx + 88, sy + 22), s["title"], font=get_font(14.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        # Text Content (W = rw - 250 to leave room for the right phone mockup)
        lines = wrap_text(s["text"], get_font(11.5, 'regular'), rw - 280, draw)
        ly = sy + 52
        for line in lines:
            draw.text((rx + 88, ly), line, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 17
            
        # Right: AIA Real Production Screen Mockup Card (W=130, H=120)
        mx = rx + rw - 165
        my = sy + 10
        mw = 135
        mh = 120
        draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=8, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        
        # Paste thumbnail
        if os.path.exists(s["img"]):
            try:
                sim = Image.open(s["img"]).convert('RGBA')
                s_ratio = sim.width / sim.height
                th_h = mh - 30
                th_w = int(th_h * s_ratio)
                if th_w > mw - 12:
                    th_w = mw - 12
                    th_h = int(th_w / s_ratio)
                sim_res = sim.resize((th_w, th_h), Image.Resampling.LANCZOS)
                px = mx + (mw - th_w) // 2
                py = my + 6
                # mini shadow/frame
                draw.rounded_rectangle([px - 2, py - 2, px + th_w + 2, py + th_h + 2], radius=4, fill=(15, 23, 42))
                img.paste(sim_res, (px, py), sim_res)
            except Exception as e:
                print(f"Error loading {s['img']}: {e}")
                
        # Label below mockup
        draw.text((mx + mw//2, my + mh - 12), s["img_label"], font=get_font(9.5, 'bold'), fill=AIA_RED if s["step"] in ['A', 'R'] else (100, 116, 139), anchor='mm')
        
        sy += 150
        
    draw_slide_footer(draw, 11, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_11.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# SLIDE 12: OUTRO & SYSTEM ECOSYSTEM (Dark Theme Enterprise Finish)
# -------------------------------------------------------------
# -------------------------------------------------------------
# SLIDE 12: OUTRO & SYSTEM ECOSYSTEM (Interactive Prototype Showcase)
# -------------------------------------------------------------
def make_slide_12():
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 12, 
        "ECOSYSTEM & INTERACTIVE PROTOTYPE", 
        "Ecosystem & Prototype | ", 
        "AIA+ 고령자 친화 인터랙티브 프로토타입 & 에코시스템", 
        "메인 화면 인터랙션 및 4대 핵심 비대면 과업(보험료 납입, 대출상환, 자동송금, 자동부활) 실시간 화면전환 시뮬레이터", 
        right_badge=("LIVE PROTOTYPE READY", "red"),
        dark_mode=True
    )
    
    card_y = 220
    card_h = 730
    
    # Left Card: Summary Pillar & Governance (W=700)
    lx = 100
    lw = 700
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_DARK, outline=BORDER_DARK, width=1)
    draw_pill_badge(draw, left_x=lx + 30, cy=card_y + 40, text="AIA+ ACCESSIBILITY ECOSYSTEM", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 30, card_y + 75), "더 건강하게, 더 오랫동안, 더 나은 삶", font=get_font(21, 'bold'), fill=TEXT_DARK_MAIN)
    draw.text((lx + 30, card_y + 115), "Healthier, Longer, Better Lives - Inclusive Mobile Experience", font=get_font(13, 'regular'), fill=AIA_RED_LIGHT)
    
    pillars = [
        ("01", "배리어프리 금융 플랫폼 표준 수립", "대한민국 65세 이상 1,000만 초고령화 사회에 대응하여, 디지털 금융 서비스의 배리어프리 표준 가이드라인을 실제 프로덕트로 완벽히 구현했습니다."),
        ("02", "디자인 시스템 확장성과 일관성 유지", "AIA 글로벌 표준 디자인 시스템 Qi v3.3의 거버넌스를 엄격히 준수하면서도, 시니어 스케일 토큰을 체계적으로 확장하여 브랜드 아이덴티티를 확고히 했습니다."),
        ("03", "데이터 기반의 문제 해결 및 사용자 중심 혁신", "휴리스틱 분석과 정량적 사용성 테스트를 통해 도출된 페인포인트를 56dp 풀와이드 버튼, 가상계좌 대체 경로 등의 실질적 UX 장치로 완벽히 해결했습니다.")
    ]
    
    py = card_y + 160
    for pnum, ptitle, pdesc in pillars:
        draw.rounded_rectangle([lx + 30, py, lx + lw - 30, py + 130], radius=12, fill=(15, 23, 42), outline=BORDER_DARK, width=1)
        draw.text((lx + 50, py + 22), pnum, font=get_num_font(20, 'black'), fill=AIA_RED)
        draw.text((lx + 95, py + 22), ptitle, font=get_font(14, 'bold'), fill=TEXT_DARK_MAIN)
        lines = wrap_text(pdesc, get_font(11.5, 'regular'), lw - 120, draw)
        ly = py + 55
        for line in lines:
            draw.text((lx + 50, ly), line, font=get_font(11.5, 'regular'), fill=TEXT_DARK_SUB)
            ly += 18
        py += 145

    # Bottom Profile Box in Left Card
    draw.rounded_rectangle([lx + 30, card_y + 580, lx + lw - 30, card_y + card_h - 25], radius=12, fill=(24, 32, 47), outline=BORDER_DARK, width=1)
    draw.text((lx + 50, card_y + 600), "• Designer", font=get_font(11, 'bold'), fill=AIA_RED_LIGHT)
    draw.text((lx + 130, card_y + 600), "Senior UI/UX Product Designer (Lead UX Architect)", font=get_font(11, 'regular'), fill=TEXT_DARK_MAIN)
    draw.text((lx + 50, card_y + 625), "• Standards", font=get_font(11, 'bold'), fill=AIA_RED_LIGHT)
    draw.text((lx + 130, card_y + 625), "FSC Korea Guidelines 100% · WCAG 2.1 AAA Compliant", font=get_font(11, 'regular'), fill=TEXT_DARK_MAIN)
    draw.text((lx + 50, card_y + 650), "• Simulator", font=get_font(11, 'bold'), fill=AIA_RED_LIGHT)
    draw.text((lx + 130, card_y + 650), "Interactive Web Simulator: prototype.html (60fps)", font=get_font(11, 'bold'), fill=(16, 185, 129))
    draw.text((lx + 50, card_y + 675), "• Copyright", font=get_font(11, 'bold'), fill=AIA_RED_LIGHT)
    draw.text((lx + 130, card_y + 675), "© 2026 AIA Life Korea. All rights reserved.", font=get_font(11, 'regular'), fill=(148, 163, 184))

    # Right Card: 60fps Interactive Simulator Preview & 4 Service Flows Showcase (W=1000)
    rx = 820
    rw = 1000
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_DARK, outline=BORDER_DARK, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=card_y + 40, text="60FPS LIVE INTERACTIVE PROTOTYPE", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 30, card_y + 75), "메인 핫스팟 링크 기반 4대 핵심 서비스 실시간 화면전환", font=get_font(21, 'bold'), fill=TEXT_DARK_MAIN)
    draw.text((rx + 30, card_y + 115), "간편홈 메인의 미납 알림 배너, 액션 그리드, 대출 카드를 클릭하면 해당 세부 과업 플로우로 인터랙티브하게 전환됩니다.", font=get_font(12, 'regular'), fill=TEXT_DARK_SUB)

    # 4 Service Flow Cards (2x2 Grid)
    # 1. 보험료 납입 (inner_pay1)
    # 2. 보험계약대출 상환 (inner_loan1)
    # 3. 자동송금 신청 (inner_transfer1)
    # 4. 자동부활 신청 (inner_revival1)
    services = [
        {
            "tag": "HOTSPOT 01", "name": "보험료 즉시 납입 (2단계)",
            "route": "메인 미납배너 / [보험료 납입] 클릭",
            "img": "aia_phase2/core_screens/inner_pay1.png",
            "desc": "원터치 납입금액 확인 → 기등록 계좌 선택 2단계"
        },
        {
            "tag": "HOTSPOT 02", "name": "보험계약대출 상환 (2단계)",
            "route": "메인 하단 [보험 대출] 카드 클릭",
            "img": "aia_phase2/core_screens/inner_loan1.png",
            "desc": "상환가능 금액 확인 → 대출상환 정보 최종 확인"
        },
        {
            "tag": "HOTSPOT 03", "name": "자동송금 신청/변경 (2단계)",
            "route": "메인 그리드 [자동이체 납입관리] 클릭",
            "img": "aia_phase2/core_screens/inner_transfer1.png",
            "desc": "신청 계약 선택 → 2건 즉시 변경 완료 피드백"
        },
        {
            "tag": "HOTSPOT 04", "name": "자동부활 & 바이탈리티 (2단계)",
            "route": "메인 우측 슬라이드 / 상단 배너 클릭",
            "img": "aia_phase2/core_screens/inner_revival1.png",
            "desc": "실효 계약 원클릭 부활 신청 → 바이탈리티 약관동의"
        }
    ]

    gw = 460
    gh = 215
    gcoords = [
        (rx + 30, card_y + 155),
        (rx + 510, card_y + 155),
        (rx + 30, card_y + 385),
        (rx + 510, card_y + 385)
    ]

    for (gx, gy), s in zip(gcoords, services):
        draw.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=12, fill=(15, 23, 42), outline=BORDER_DARK, width=1)
        
        # Phone Thumbnail Mockup (W=90, H=190)
        pw = 90
        ph = 185
        px = gx + 15
        py = gy + 15
        
        # Inner screen
        if os.path.exists(s["img"]):
            try:
                s_img = Image.open(s["img"]).convert('RGBA')
                s_ratio = s_img.width / s_img.height
                th_w = pw - 8
                th_h = int(th_w / s_ratio)
                if th_h > ph - 16:
                    th_h = ph - 16
                    th_w = int(th_h * s_ratio)
                s_resized = s_img.resize((th_w, th_h), Image.Resampling.LANCZOS)
                
                # Device bezel
                draw.rounded_rectangle([px, py, px + pw, py + ph], radius=14, fill=(5, 5, 5), outline=(51, 65, 85), width=2)
                # Paste thumbnail centered
                paste_x = px + (pw - th_w) // 2
                paste_y = py + (ph - th_h) // 2
                img.paste(s_resized, (paste_x, paste_y), s_resized)
            except Exception as e:
                print(f"Error loading {s['img']}: {e}")
        
        # Text details
        tx = gx + pw + 30
        draw.text((tx, gy + 20), s["tag"], font=get_num_font(11, 'bold'), fill=AIA_RED)
        draw.text((tx, gy + 40), s["name"], font=get_font(14, 'bold'), fill=TEXT_DARK_MAIN)
        draw.text((tx, gy + 70), f"진입: {s['route']}", font=get_font(11, 'bold'), fill=AIA_RED_LIGHT)
        
        lines = wrap_text(s["desc"], get_font(11, 'regular'), gw - pw - 45, draw)
        dly = gy + 98
        for l in lines:
            draw.text((tx, dly), l, font=get_font(11, 'regular'), fill=TEXT_DARK_SUB)
            dly += 16
            
        # Mini CTA Button
        draw.rounded_rectangle([tx, gy + 155, tx + 180, gy + 190], radius=8, fill=(211, 17, 69, 50), outline=AIA_RED, width=1)
        draw.text((tx + 90, gy + 172), "실시간 시뮬레이션 연동 ▶", font=get_font(10.5, 'bold'), fill=(255, 255, 255), anchor='mm')

    # Bottom CTA Banner across right card
    draw.rounded_rectangle([rx + 30, card_y + 615, rx + rw - 30, card_y + card_h - 25], radius=12, fill=(211, 17, 69), outline=None)
    draw.text((rx + rw//2, card_y + 645), "지금 웹 브라우저에서 60fps 인터랙티브 프로토타입 실행하기", font=get_font(15, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((rx + rw//2, card_y + 675), "AIA_Phase2/prototype.html  ·  간편홈 메인 핫스팟 클릭 시 4개 과업 즉시 전환 지원", font=get_font(11.5, 'medium'), fill=(254, 205, 211), anchor='mm')

    draw_slide_footer(draw, 12, 12, dark_mode=True)
    out_path = os.path.join(OUT_DIR, "slide_12.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_09()
    make_slide_10()
    make_slide_11()
    make_slide_12()
