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
# SLIDE 10: CORE JOURNEY 03 - SMART OCR CLAIMS & REVIVAL
# -------------------------------------------------------------
def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 10, 
        "CORE JOURNEY · CLAIMS & REVIVAL", 
        "Core Journey | ", 
        "스마트 영수증 OCR 보험금 청구 & 실효계약 부활", 
        "사진 한 장으로 서류 접수 완료 및 하단 56dp 풀와이드 청구 접수 CTA 완벽 배치", 
        right_badge=("OCR AUTO-RECOGNITION", "green")
    )
    
    # Left Mockup Box (W=820)
    lx = 100
    ly = 220
    lw = 820
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=ly + 35, text="SMART OCR CLAIMS & FORM INTERFACES", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((lx + 25, ly + 65), "영수증 자동 스캔 & 청구 사유 간편 입력", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    draw_phone_mockup(img, os.path.join(CORE_DIR, "screen_claim_receipt.png"), cx=lx + 210, cy=ly + 390, phone_w=252, phone_h=545, bezel=6, radius=28)
    draw_phone_mockup(img, os.path.join(CORE_DIR, "screen_claim_form.png"), cx=lx + 600, cy=ly + 390, phone_w=252, phone_h=545, bezel=6, radius=28)
    draw_arrow(draw, (lx + 345, ly + 390), (lx + 465, ly + 390), col=(16, 185, 129), width=2, arrow_size=6)
    
    draw.text((lx + 210, ly + 685), "AI 영수증 자동 스캔 & 하단 촬영 CTA", font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mt')
    draw.text((lx + 600, ly + 685), "수령 계좌 선택 & 하단 56dp 접수 CTA", font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mt')
    
    # Right Box: OCR Process & Revival Care (W=880)
    rx = 940
    rw = 880
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 35, text="AI CLAIM ENGINE & REVIVAL CARE", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((rx + 25, ly + 65), "청구 서류 누락 0건 & 실효 계약 부활 프로세스", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    services = [
        {
            "num": "01",
            "title": "카메라 실시간 OCR 영수증 파싱",
            "desc": "카메라 뷰파인더에 병원비/약제비 영수증을 비추면 모서리를 자동 인식하여 평면 보정합니다. 병원명, 진료일자, 결제금액이 폼 필드에 자동으로 입력되어 수기 오입력을 방지합니다."
        },
        {
            "num": "02",
            "title": "3분 이내 청구 접수 & 당일 심사 지급",
            "desc": "기존 5단계의 복잡한 청구 서식 작성을 1단계로 축소했습니다. 평소 보험료를 납부하던 계좌가 수령 계좌로 자동 세팅되어 터치 2번만으로 접수가 완료되며 소액 청구는 당일 지급됩니다."
        },
        {
            "num": "03",
            "title": "실효 계약 원클릭 부활(Revival) 케어",
            "desc": "보험료 미납으로 효력이 정지된 실효 계약을 즉시 찾아내어, 밀린 보험료와 이자를 한눈에 보여주고 원터치 납부로 보장을 즉시 되살릴 수 있도록 유도합니다."
        },
        {
            "num": "04",
            "title": "실시간 진행 상태 알림톡 브릿지",
            "desc": "서류 접수, 심사 중, 보완 요청, 지급 완료의 전 과정을 카카오 알림톡으로 실시간 통보하여 고객센터 전화 문의를 근본적으로 차단했습니다."
        }
    ]
    
    sy = ly + 115
    for s in services:
        draw.rounded_rectangle([rx + 25, sy, rx + rw - 25, sy + 125], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((rx + 45, sy + 18), s["num"], font=get_num_font(20, 'black'), fill=AIA_RED)
        draw.text((rx + 85, sy + 18), s["title"], font=get_font(14.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        lines = wrap_text(s["desc"], get_font(12, 'regular'), rw - 90, draw)
        ly_p = sy + 52
        for line in lines:
            draw.text((rx + 45, ly_p), line, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            ly_p += 18
        sy += 140
        
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
    
    # Top: 4 Stat Cards matching Behance Outcomes (100%, 2x, 90%, 50%)
    outcomes = [
        ("100%", "금융위 규제 가이드라인 100% 준수", "금융감독원 및 협회 배리어프리 기준 완전 충족"),
        ("2x", "본문 & 버튼 활자 크기 200% 확대", "돋보기 없이 즉시 인지 가능한 18pt~28pt 적용"),
        ("90%", "시니어 핵심 과업 완수율 90% 달성", "기존 58.2%에서 89.4%로 31.2%p 비약적 상승"),
        ("50%", "비대면 업무 소요 시간 50% 이상 단축", "복잡 8단계에서 3-Step 단축 (1분 20초 주파)")
    ]
    card_w = 405
    card_h = 140
    start_x = 100
    start_y = 220
    
    for i, (m_val, m_title, m_desc) in enumerate(outcomes):
        cx = start_x + i * (card_w + 23)
        draw.rounded_rectangle([cx, start_y, cx + card_w, start_y + card_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw.text((cx + 20, start_y + 18), m_val, font=get_num_font(32, 'black'), fill=AIA_RED if i==0 else (15, 23, 42))
        draw.text((cx + 20, start_y + 68), m_title, font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((cx + 20, start_y + 98), m_desc, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
        
    # Bottom: Authentic STAR Retrospective (200자+ 이상 실무 서술)
    star_y = 390
    draw.rounded_rectangle([100, star_y, 1820, star_y + 560], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    # Header
    draw_pill_badge(draw, left_x=125, cy=star_y + 35, text="STAR METHOD RETROSPECTIVE", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((360, star_y + 25), "AIA생명 AIA+ Phase 2 배리어프리 금융 UX 아키텍처 구축 회고 (200자 이상)", font=get_font(17, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((1500, star_y + 25), "메인화면(일반/고령자) & 화면설계서 100% 단독 총괄", font=get_font(11.5, 'bold'), fill=AIA_RED)
    
    star_boxes = [
        {
            "tag": "SITUATION",
            "title": "초고령 사회 진입과 금융 디지털 소외의 구조적 위기",
            "sub": "레거시 모바일 앱의 8단계 뎁스와 8pt 미세 폰트로 인한 고령층 이탈률 68% 육박",
            "content": (
                "2025년 초고령 사회 진입을 앞두고 금융위원회의 '고령자 친화적 모바일 금융앱 가이드라인' 준수가 법적 의무화되었습니다. "
                "기존 AIA+ 앱은 방대한 약관, 복잡한 본인인증 뎁스, 8pt 미세 폰트 등으로 인해 6070 고령 고객의 비대면 업무 이탈률이 68.4%에 달했고, "
                "보험료 납입과 대출 상환 문의가 오프라인 영업점 및 콜센터에 집중되어 운영 비용이 급증하는 심각한 병목 현상이 발생하고 있었습니다."
            ),
            "theme": "blue"
        },
        {
            "tag": "TASK",
            "title": "원터치 고령자 모드 탑재 및 10대 비대면 코어 서비스 리뉴얼",
            "sub": "금융위 가이드라인 100% 준수와 18pt+ 대형 활자 기반 제로-뎁스 아키텍처 설계",
            "content": (
                "본 프로젝트의 목표는 금융위 규제 가이드라인을 100% 완벽 준수하면서, 고령자가 로그인 즉시 1초 만에 당월 보험료를 확인하고 납부할 수 있는 "
                "'고령자 친화 간편 모드'를 구축하는 것이었습니다. 복잡한 8단계의 레거시 보험료 납입 여정을 3-Step으로 압축하고, "
                "48px 대형 인체공학 터치 타겟과 WCAG 2.1 AAA 8.4:1 고대비 컬러 시스템을 적용하여 단 하나의 오터치도 없는 안전한 금융 환경을 구축해야 했습니다."
            ),
            "theme": "purple"
        },
        {
            "tag": "ACTION",
            "title": "Qi v3.3 기반 단일 소스 디자인 시스템 구축 및 3-Step 여정 구현",
            "sub": "150종 이상의 디자인 토큰 표준화, 1-Tap 가상계좌 발급, AI 영수증 OCR 설계",
            "content": (
                "Figma 기반의 Qi 디자인 시스템 v3.3을 전면 구축하여 컬러, 타이포그래피, 24dp/32dp 아이콘 매트릭스, 56dp 인풋 컴포넌트 150종을 단일 소스로 표준화했습니다. "
                "복잡한 공인인증서를 배제하고 48px 대형 숫자 키패드와 주거래 계좌 1-Tap 출금 방식을 도입했으며, 계좌 이체가 어려운 시니어를 위해 '가상계좌 즉시 발급 및 문자 발송' "
                "기능을 설계했습니다. 또한 영수증 자동 스캔 OCR과 실효 계약 부활 원클릭 프로세스를 설계하여 비대면 서류 접수 오류를 원천 차단했습니다."
            ),
            "theme": "amber"
        },
        {
            "tag": "RESULT",
            "title": "완수율 89.4% 달성, 소요시간 58% 단축 및 포용적 금융 표준 수립",
            "sub": "콜센터 단순 문의 44.6% 급감, 개발 생산성 62.5% 향상이라는 전사적 성과 입증",
            "content": (
                "고령자 사용자 사용성 테스트(UT) 결과, 과업 완수율이 기존 58.2%에서 89.4%로 31.2%p 비약적으로 상승했고 평균 소요 시간은 1분 20초로 58.3% 단축되었습니다. "
                "단순 납부 및 발급 문의가 44.6% 급감하여 콜센터 리소스를 대폭 절감했으며, 토큰 기반 디자인 시스템 도입으로 디자인-개발 납기가 화면당 4일에서 1.5일로 단축되었습니다. "
                "이를 통해 AIA생명은 금융감독원 및 언론으로부터 '포용적 금융을 선도하는 베스트 모바일 UX'로 선정되는 쾌거를 달성했습니다."
            ),
            "theme": "green"
        }
    ]
    
    bw = 820
    bh = 220
    for idx, b in enumerate(star_boxes):
        bx = 125 + (idx % 2) * 850
        by = star_y + 80 + (idx // 2) * 235
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        
        draw_pill_badge(draw, left_x=bx + 20, cy=by + 28, text=b["tag"], font=get_font(10.5, 'bold'), theme=b["theme"], pad_x=12, height=22)
        draw.text((bx + 120, by + 18), b["title"], font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((bx + 20, by + 46), b["sub"], font=get_font(11.5, 'medium'), fill=AIA_RED if idx==3 else (29, 78, 216))
        
        lines = wrap_text(b["content"], get_font(11.5, 'regular'), bw - 40, draw)
        py = by + 76
        for line in lines:
            draw.text((bx + 20, py), line, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
            py += 17
            
    draw_slide_footer(draw, 11, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_11.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 12: EPILOGUE & CREDITS (Inclusive UX Philosophy & Spec)
# -------------------------------------------------------------
def make_slide_12():
    img = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Warm radial glow background
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([450, 180, 1470, 920], fill=(211, 17, 69, 18))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.paste(glow, (0, 0), glow)
    
    draw = ImageDraw.Draw(img)
    
    # Top Tag
    draw_pill_badge(draw, cx=960, cy=135, text="AIA LIFE · HEALTHIER, LONGER, BETTER LIVES", font=get_font(11.5, 'bold'), theme='red', pad_x=16, height=30)
    
    # Main Vision Title
    draw.text((960, 205), "모든 세대를 포용하는 지속 가능한 디지털 금융 UX", font=get_font(38, 'black'), fill=(15, 23, 42), anchor='mt')
    draw.text((960, 270), "AIA+ Phase 2 는 배리어프리 가이드라인을 넘어, 금융의 존엄성을 설계했습니다.", font=get_font(18, 'medium'), fill=AIA_RED, anchor='mt')
    
    # Center 3 Pillars of Impact
    pillars = [
        ("INCLUSIVE UX", "포용적 금융 철학", "나이와 신체적 제약에 상관없이 누구나 자신의 자산을 스스로 통제할 수 있는 권리 보장"),
        ("QI SCALABILITY", "글로벌 확장성", "홍콩, 싱가포르 등 AIA 글로벌 시장으로 즉시 이식 가능한 모듈형 토큰 아키텍처"),
        ("BUSINESS VALUE", "검증된 비즈니스 성과", "완수율 89.4% 및 인바운드 콜 44.6% 감축으로 입증된 확실한 엔터프라이즈 ROI")
    ]
    card_w = 480
    card_h = 180
    start_x = 180
    for i, (p_tag, p_title, p_desc) in enumerate(pillars):
        cx = start_x + i * (card_w + 50)
        cy = 350
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=16, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=cx + 25, cy=cy + 35, text=p_tag, font=get_font(10.5, 'bold'), theme='red' if i==0 else ('blue' if i==1 else 'green'), pad_x=12, height=24)
        draw.text((cx + 25, cy + 68), p_title, font=get_font(20, 'bold'), fill=(15, 23, 42))
        lines = wrap_text(p_desc, get_font(12.5, 'regular'), card_w - 50, draw)
        ly = cy + 105
        for line in lines:
            draw.text((cx + 25, ly), line, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 20
            
    # Bottom Center: Designer Credit & Interactive Prototype Hub Link Box
    credit_y = 600
    cw = 1100
    cx = (W - cw) // 2
    draw.rounded_rectangle([cx, credit_y, cx + cw, credit_y + 320], radius=20, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, cx=960, cy=credit_y + 38, text="LEAD PRODUCT DESIGNER & UX ARCHITECT", font=get_font(11, 'bold'), theme='gray', pad_x=14, height=26)
    draw.text((960, credit_y + 76), "기획 · 디자인 시스템 · 프로토타이핑 100% 총괄 수행", font=get_font(22, 'bold'), fill=(15, 23, 42), anchor='mt')
    
    spec_rows = [
        ("프로젝트명", "AIA생명 AIA+ Phase 2 고령자 친화 배리어프리 금융 UX 및 10대 비대면 서비스 리뉴얼"),
        ("수행 기간", "2024.08 - 2024.11 (4개월 집중 수행)"),
        ("담당 역할", "수석 프로덕트 디자이너 (UI/UX 정보설계, Qi v3.3 디자인 시스템 구축, 사용자 UT 총괄)"),
        ("적용 표준", "금융위원회 고령자 친화적 모바일 금융앱 가이드라인 100% 준수 · WCAG 2.1 AAA 고대비")
    ]
    for idx, (label, val) in enumerate(spec_rows):
        sy = credit_y + 120 + idx * 30
        draw.text((cx + 60, sy), label, font=get_font(12.5, 'bold'), fill=AIA_RED)
        draw.text((cx + 180, sy), val, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_MAIN)
        
    draw.rounded_rectangle([cx + 60, credit_y + 255, cx + cw - 60, credit_y + 298], radius=10, fill=(255, 241, 244), outline=AIA_RED, width=1)
    draw.text((960, credit_y + 276), "🔗 하단 도크의 [허브] 버튼을 누르면 전체 포트폴리오 컬렉션으로 즉시 이동합니다.", font=get_font(12, 'bold'), fill=AIA_RED, anchor='mm')
    
    draw_slide_footer(draw, 12, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_12.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_09()
    make_slide_10()
    make_slide_11()
    make_slide_12()
