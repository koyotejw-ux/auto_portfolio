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
        ("05. 가상계좌 신청", "screen_pay_virtual.png", "입금 전용 가상계좌 발급 및 문자/카톡 전송"),
        ("06. 대형 PIN 키패드", "screen_login_pin.png", "48px 대형 숫자 키패드로 오터치 원천 차단"),
        ("07. 전자서명 선택", "screen_sign_select.png", "카카오/토스/PASS 등 4대 간편인증 완비"),
        ("08. 일반모드 대시보드", "screen_general_main_clean.png", "일반 ↔ 고령자모드 원클릭 스위칭 연동 대시보드")
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
            "screen": "screen_claim_step1.png",
            "desc": "진단서/영수증 필수 서류를 대형 아이콘과 큰 글씨로 안내하여 서류 누락 방지"
        },
        {
            "tag": "STEP 02",
            "title": "영수증/진단서 OCR 촬영",
            "screen": "screen_claim_step2.png",
            "desc": "카메라 뷰파인더 모서리 자동인식, 진료비/병원명 자동 파싱으로 수기입력 제로화"
        },
        {
            "tag": "STEP 03",
            "title": "사고내용 & 수령계좌",
            "screen": "screen_claim_step3.png",
            "desc": "평소 보험료 납부 계좌 자동 세팅 및 1-Tap 수령 계좌 선택으로 오입력 방지"
        },
        {
            "tag": "STEP 04",
            "title": "청구 접수 완료 & 심사",
            "screen": "screen_claim_step4.png",
            "desc": "접수 번호 부여, 카카오 알림톡 실시간 전송 및 메인 게이트 접수현황 실시간 연동"
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
def make_slide_11():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 11, 
        "PROJECT REFLECTION & OUTCOMES", 
        "Project Reflection & Outcomes | ", 
        "검증된 성과 지표 & 200자 STAR 회고", 
        "금융위 가이드라인 100% 충족, 폰트 2배 확대, 완수율 90%, 소요시간 50% 단축 정량 지표와 문제해결 회고", 
        right_badge=("KEY OUTCOMES", "red")
    )
    
    # Left Column: 4 Stat KPI Cards (2x2 Grid, W=760)
    card_y = 220
    card_h = 730
    
    lx = 100
    lw = 760
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="KEY QUANTITATIVE METRICS", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 65), "정량적 사용성 개선 성과 지표", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    metrics = [
        {"val": "100%", "label": "금융위 가이드라인 충족률", "sub": "18pt 이상 활자 & 고대비 명도비 AAA 완벽 달성"},
        {"val": "2x", "label": "핵심 텍스트 크기 확대", "sub": "일반 14pt 대비 고령자 모드 18~28pt 2배 확대"},
        {"val": "90%", "label": "고령층 보험료 납부 완수율", "sub": "기존 42% 대비 +48%p 대폭 상승 (사용성 테스트)"},
        {"val": "-50%", "label": "과업 완수 소요시간 단축", "sub": "평균 6분 30초에서 3분 10초로 대폭 단축"}
    ]
    
    gw = 335
    gh = 260
    grid_coords = [
        (lx + 25, card_y + 115),
        (lx + 395, card_y + 115),
        (lx + 25, card_y + 400),
        (lx + 395, card_y + 400)
    ]
    
    for (gx, gy), m in zip(grid_coords, metrics):
        draw.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((gx + gw//2, gy + 85), m["val"], font=get_num_font(52, 'black'), fill=AIA_RED, anchor='mm')
        draw.text((gx + gw//2, gy + 155), m["label"], font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
        lines = wrap_text(m["sub"], get_font(11.5, 'regular'), gw - 40, draw)
        ly = gy + 195
        for line in lines:
            draw.text((gx + gw//2, ly), line, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
            ly += 18
            
    # Right Column: Senior UX Strategy & 200자 STAR Reflection (W=920)
    rx = 900
    rw = 920
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=card_y + 35, text="STAR METHOD RETROSPECTIVE", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 25, card_y + 65), "시니어 프로덕트 디자이너 문제해결 회고", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    star_steps = [
        {
            "step": "S",
            "title": "Situation (상황 및 배경)",
            "text": "보험사 디지털 전환 가속화로 모바일 앱 이용률이 급증했으나, 65세 이상 고령 고객은 작은 폰트(12~14pt), 복잡한 증권번호 나열, 수많은 뎁스로 인해 보험료 납부 및 청구 과정에서 이탈률 58%에 달하며 심각한 디지털 소외와 콜센터 과부하가 발생했습니다."
        },
        {
            "step": "T",
            "title": "Task (과제 및 목표)",
            "text": "금융위원회 고령자 친화 모바일 앱 가이드라인을 100% 충족하면서, AIA생명 글로벌 표준 디자인 시스템(Qi v3.3)의 브랜드 일관성을 훼손하지 않는 독립적인 '고령자 전용 모드'와 '원터치 코어 저니'를 구축하는 것을 핵심 과제로 설정했습니다."
        },
        {
            "step": "A",
            "title": "Action (설계 및 해결 과정)",
            "text": "Figma 변수 기반 시니어 전용 18~28pt 폰트 스케일 및 56dp 풀와이드 고정 CTA 컴포넌트를 설계했습니다. 화면당 1개 과업만 제시하는 원칙을 수립하고, 기등록 주거래 계좌 자동 연동과 비밀번호 분실 시 가상계좌 대체 발급 경로를 도입하여 인지적 마찰을 원천 제거했습니다."
        },
        {
            "step": "R",
            "title": "Result (성과 및 배운 점)",
            "text": "고령층 대상 사용성 테스트에서 과업 완수율 90%(+48%p 개선), 소요시간 50% 단축을 달성했습니다. 배리어프리 디자인이 특정 연령대뿐만 아니라 전체 사용자의 인지 피로도를 줄이는 유니버설 디자인의 핵심 가치임을 데이터로 입증했습니다."
        }
    ]
    
    sy = card_y + 115
    for s in star_steps:
        draw.rounded_rectangle([rx + 25, sy, rx + rw - 25, sy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        # STAR Badge
        draw.rounded_rectangle([rx + 45, sy + 18, rx + 80, sy + 53], radius=8, fill=AIA_RED if s["step"] in ['S', 'R'] else (59, 130, 246))
        draw.text((rx + 62, sy + 35), s["step"], font=get_font(18, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        draw.text((rx + 95, sy + 25), s["title"], font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN)
        lines = wrap_text(s["text"], get_font(12, 'regular'), rw - 130, draw)
        ly = sy + 58
        for line in lines:
            draw.text((rx + 45, ly), line, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 18
        sy += 145
        
    draw_slide_footer(draw, 11, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_11.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 12: OUTRO & SYSTEM ECOSYSTEM (Dark Theme Enterprise Finish)
# -------------------------------------------------------------
def make_slide_12():
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 12, 
        "ECOSYSTEM & CONTACT", 
        "Ecosystem & Contact | ", 
        "AIA생명 디지털 포트폴리오 에코시스템", 
        "시니어 배리어프리 혁신이 만든 포용적 금융 플랫폼의 미래", 
        right_badge=("END OF DECK", "red"),
        dark_mode=True
    )
    
    # Left Card: Summary Pillar (W=820)
    card_y = 220
    card_h = 730
    
    lx = 100
    lw = 820
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_DARK, outline=BORDER_DARK, width=1)
    draw_pill_badge(draw, left_x=lx + 30, cy=card_y + 40, text="AIA+ ACCESSIBILITY CORE", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 30, card_y + 75), "더 건강하게, 더 오랫동안, 더 나은 삶", font=get_font(22, 'bold'), fill=TEXT_DARK_MAIN)
    draw.text((lx + 30, card_y + 115), "Healthier, Longer, Better Lives - Inclusive Mobile Experience", font=get_font(13.5, 'regular'), fill=AIA_RED_LIGHT)
    
    pillars = [
        ("01", "배리어프리 금융 플랫폼 표준 수립", "대한민국 65세 이상 1,000만 초고령화 사회에 대응하여, 디지털 금융 서비스의 배리어프리 표준 가이드라인을 실제 프로덕트로 완벽히 구현했습니다."),
        ("02", "디자인 시스템 확장성과 일관성 유지", "AIA 글로벌 표준 디자인 시스템 Qi v3.3의 거버넌스를 엄격히 준수하면서도, 시니어 스케일 토큰을 체계적으로 확장하여 브랜드 아이덴티티를 확고히 했습니다."),
        ("03", "데이터 기반의 문제 해결 및 사용자 중심 혁신", "휴리스틱 분석과 정량적 사용성 테스트를 통해 도출된 페인포인트를 56dp 풀와이드 버튼, 가상계좌 대체 경로 등의 실질적 UX 장치로 완벽히 해결했습니다.")
    ]
    
    py = card_y + 170
    for pnum, ptitle, pdesc in pillars:
        draw.rounded_rectangle([lx + 30, py, lx + lw - 30, py + 145], radius=12, fill=(15, 23, 42), outline=BORDER_DARK, width=1)
        draw.text((lx + 55, py + 25), pnum, font=get_num_font(22, 'black'), fill=AIA_RED)
        draw.text((lx + 105, py + 25), ptitle, font=get_font(15, 'bold'), fill=TEXT_DARK_MAIN)
        lines = wrap_text(pdesc, get_font(12, 'regular'), lw - 140, draw)
        ly = py + 62
        for line in lines:
            draw.text((lx + 55, ly), line, font=get_font(12, 'regular'), fill=TEXT_DARK_SUB)
            ly += 19
        py += 165
        
    # Right Card: Designer Profile & Verification Contact (W=880)
    rx = 940
    rw = 880
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_DARK, outline=BORDER_DARK, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=card_y + 40, text="DESIGNER PROFILE & PORTFOLIO", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 30, card_y + 75), "시니어 UI/UX 프로덕트 디자이너", font=get_font(22, 'bold'), fill=TEXT_DARK_MAIN)
    
    # Portfolio Metadata Box
    draw.rounded_rectangle([rx + 30, card_y + 130, rx + rw - 30, card_y + 360], radius=14, fill=(15, 23, 42), outline=BORDER_DARK, width=1)
    draw.text((rx + 55, card_y + 160), "PROFIT & VALUE DRIVEN DESIGN", font=get_font(12, 'bold'), fill=AIA_RED)
    draw.text((rx + 55, card_y + 190), "AIA+ Phase 2 고령자 모드 전면 개편 포트폴리오", font=get_font(17, 'bold'), fill=TEXT_DARK_MAIN)
    
    infos = [
        ("Project Role", "Lead Product Designer & Design System Architect"),
        ("Deliverables", "12-Slide High-Resolution Portfolio, UI Wireframes, Production Specs"),
        ("Compliance", "Financial Services Commission Accessibility Standards (100% AAA)"),
        ("System Stack", "Figma Design Tokens, Qi v3.3, Flutter Universal Mobile/Web"),
        ("Live Preview", "http://localhost:5000/aia_phase2/index.html")
    ]
    iy = card_y + 225
    for ilabel, ival in infos:
        draw.text((rx + 55, iy), f"•  {ilabel}:", font=get_font(11.5, 'bold'), fill=(148, 163, 184))
        draw.text((rx + 220, iy), ival, font=get_font(11.5, 'regular'), fill=TEXT_DARK_MAIN)
        iy += 24
        
    # Thank You Banner at Bottom
    draw.rounded_rectangle([rx + 30, card_y + 390, rx + rw - 30, card_y + card_h - 40], radius=14, fill=(211, 17, 69, 40), outline=AIA_RED, width=2)
    draw.text((rx + rw//2, card_y + 470), "THANK YOU FOR WATCHING", font=get_num_font(28, 'black'), fill=(255, 255, 255), anchor='mm')
    draw.text((rx + rw//2, card_y + 520), "디지털 격차 없는 따뜻한 금융 경험을 만들어갑니다.", font=get_font(15, 'bold'), fill=AIA_RED_LIGHT, anchor='mm')
    draw.text((rx + rw//2, card_y + 570), "AIA Life Korea · Inclusive UX Design Strategy · 2026", font=get_font(12, 'medium'), fill=(148, 163, 184), anchor='mm')
    
    draw_slide_footer(draw, 12, 12, dark_mode=True)
    out_path = os.path.join(OUT_DIR, "slide_12.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_09()
    make_slide_10()
    make_slide_11()
    make_slide_12()
