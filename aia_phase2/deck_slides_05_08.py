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
# SLIDE 05: CORE USER FLOW & INTERACTION LOGIC
# -------------------------------------------------------------
def make_slide_05():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 5, "CORE USER FLOW & JOURNEY", "복잡한 8단계를 3단계로 단축한", " 초간편 보험료 납입 여정", "인증 장벽 제거 및 1-Tap 가상계좌 발급으로 완료율을 극대화한 비대면 플로우", right_badge=("3-STEP ZERO FRICTION", "green"))
    
    # 3 Big Step Cards
    steps = [
        {
            "num": "STEP 01",
            "title": "계약 선택 & 납부금 확인",
            "sub": "원터치 계약 요약 카드",
            "screen": "screen_pay_list_senior.png",
            "desc": "홈 화면에서 '보험료 바로 내기' 터치 즉시 진입. 보유 계약 중 당월 미납된 계약이 자동 선택되어 단 1초 만에 납부 금액 확인.",
            "features": [
                "당월 납입 보험료 18pt 굵은 글씨 강조",
                "복잡한 약관 번호 대신 친숙한 상품명 표시",
                "선택 해제/다건 동시 납부 체크박스 지원"
            ]
        },
        {
            "num": "STEP 02",
            "title": "납부 수단 1-Tap 선택",
            "sub": "주거래 계좌 or 가상계좌",
            "screen": "screen_pay_input_account.png",
            "desc": "기존에 등록된 주거래 은행 계좌가 즉시 로딩되어 비밀번호 입력 없이 출금 동의. 계좌 변경 또는 가상계좌 입금도 즉시 탭 가능.",
            "features": [
                "기등록 은행 계좌 번호 마스킹 안전 노출",
                "가상계좌 즉시 발급 및 카카오톡/문자 전송",
                "오입금 방지 실시간 예금주명 일치 검증"
            ]
        },
        {
            "num": "STEP 03",
            "title": "간편 전자서명 & 완료",
            "sub": "원터치 인증 & 안심 알림",
            "screen": "screen_pay_done.png",
            "desc": "공인인증서 폐지 후 도입된 6자리 PIN 또는 간편 서명으로 즉시 승인 완료. 카카오 알림톡으로 입금 확인증 즉시 발송.",
            "features": [
                "48px 대형 숫자 키패드로 오터치 제로화",
                "납부 결과 즉시 조회 및 영수증 저장",
                "매월 5일 자동이체 간편 등록 팝업 케어"
            ]
        }
    ]
    
    cw = 520
    ch = 730
    start_x = 100
    start_y = 220
    
    for i, s in enumerate(steps):
        cx = start_x + i * (cw + 30)
        draw.rounded_rectangle([cx, start_y, cx + cw, start_y + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Step Badge
        draw_pill_badge(draw, left_x=cx + 25, cy=start_y + 35, text=s["num"], font=get_font(11, 'bold'), theme='red' if i==1 else 'blue', pad_x=12, height=24)
        draw.text((cx + 105, start_y + 25), s["sub"], font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB)
        draw.text((cx + 25, start_y + 65), s["title"], font=get_font(19, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        # Phone Screen Mockup inside card
        screen_file = os.path.join(CORE_DIR, s["screen"])
        draw_phone_mockup(img, screen_file, cx=cx + cw // 2, cy=start_y + 320, phone_w=220, phone_h=440, bezel=8, radius=28)
        
        # Description
        py = start_y + 560
        lines = wrap_text(s["desc"], get_font(12, 'regular'), cw - 50, draw)
        for line in lines:
            draw.text((cx + 25, py), line, font=get_font(12, 'regular'), fill=TEXT_LIGHT_MAIN)
            py += 18
            
        # Feature bullets
        py += 10
        for feat in s["features"]:
            draw.text((cx + 25, py), "•", font=get_font(12, 'bold'), fill=AIA_RED)
            draw.text((cx + 40, py), feat, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_SUB)
            py += 22
            
    draw_slide_footer(draw, 5, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_05.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 06: SENIOR BARRIER-FREE SYSTEM & DESIGN ETHICS
# -------------------------------------------------------------
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 6, "SENIOR ACCESSIBILITY & UI SYSTEM", "고령자 친화 배리어프리 가이드라인", " 4대 핵심 설계 원칙", "WCAG 2.1 AAA 고대비율과 인체공학 터치 타겟을 적용한 시니어 전용 인터페이스", right_badge=("ACCESSIBILITY AAA 8.4:1", "red"))
    
    pillars = [
        {
            "tag": "PRINCIPLE 01",
            "title": "대형 활자 & 시인성 극대화",
            "metric": "18pt ~ 28pt",
            "metric_desc": "기본 본문 및 핵심 금액 최소 활자 크기",
            "details": [
                ("본문 18pt 이상 기본 적용", "일반 앱 대비 150% 확대된 본문 폰트 크기로 돋보기 없이 즉시 인지"),
                ("단일 위계 굵기(Bold) 구분", "라이트/씬 폰트 배제, SemiBold/Bold 중심의 명확한 자획 구현"),
                ("자간 및 행간 160% 확대", "글자 뭉침 현상을 방지하는 와이드 레터스페이싱 및 넉넉한 줄간격")
            ]
        },
        {
            "tag": "PRINCIPLE 02",
            "title": "고대비 컬러 & 안구 피로 저감",
            "metric": "8.4 : 1",
            "metric_desc": "WCAG AAA 기준(7:1)을 상회하는 명도 대비",
            "details": [
                ("순백색 배경 대비 다크 그레이 텍스트", "#0F172A 컬러로 순수 블랙의 번짐을 줄이고 선명도 극대화"),
                ("AIA Red 시그니처 엑센트", "주요 액션 버튼과 상태 뱃지에 강력한 브랜드 레드(#D31145) 적용"),
                ("미세 연회색 테두리 배제", "카드 컨테이너의 외곽선을 2px 솔리드 라인으로 뚜렷하게 분리")
            ]
        },
        {
            "tag": "PRINCIPLE 03",
            "title": "인체공학 터치 & 오조작 방지",
            "metric": "48 x 48 dp",
            "metric_desc": "최소 인터랙션 터치 타겟 규격",
            "details": [
                ("손떨림 보정 마진 16dp 확보", "인접 버튼 간 충분한 간격을 두어 의도치 않은 오터치 원천 차단"),
                ("하단 플로팅 1-Action 풀와이드 버튼", "엄지손가락 이동 동선을 고려한 높이 56dp 풀너비 고정 버튼"),
                ("터치 즉각 햅틱 진동 피드백", "버튼 클릭 시 물리적 진동 반응으로 작업 수행 완료 여부 즉각 체감")
            ]
        },
        {
            "tag": "PRINCIPLE 04",
            "title": "쉬운 금융 언어 & 인지 부하 제로",
            "metric": "Zero-Jargon",
            "metric_desc": "금융 전문 용어 100% 일상어 순화",
            "details": [
                ("난해한 보험 한자어 퇴출", "'부활신청' ➔ '효력 회복하기', '해약환급금' ➔ '해약 시 돌려받는 돈'"),
                ("단일 화면 1개 과업 원칙", "한 화면에 하나의 질문만 던져 고령층의 정보 과부하 및 혼란 방지"),
                ("진행 단계 명확한 넘버링", "'1단계: 계좌확인 ➔ 2단계: 서명'으로 잔여 여정을 항상 인지")
            ]
        }
    ]
    
    pw = 395
    ph = 730
    start_x = 100
    start_y = 220
    
    for i, p in enumerate(pillars):
        px = start_x + i * (pw + 23)
        draw.rounded_rectangle([px, start_y, px + pw, start_y + ph], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Tag
        draw_pill_badge(draw, left_x=px + 20, cy=start_y + 35, text=p["tag"], font=get_font(10.5, 'bold'), theme='red' if i in [0, 1] else 'blue', pad_x=12, height=24)
        draw.text((px + 20, start_y + 65), p["title"], font=get_font(17, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        # Metric Box
        draw.rounded_rectangle([px + 20, start_y + 105, px + pw - 20, start_y + 195], radius=12, fill=(255, 241, 244) if i in [0, 1] else (239, 246, 255))
        m_col = AIA_RED if i in [0, 1] else (0, 81, 255)
        draw.text((px + 35, start_y + 120), p["metric"], font=get_num_font(30, 'black'), fill=m_col)
        draw.text((px + 35, start_y + 165), p["metric_desc"], font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_SUB)
        
        # Details
        dy = start_y + 225
        for h_text, b_text in p["details"]:
            draw.text((px + 22, dy), "✔", font=get_font(12, 'bold'), fill=m_col)
            draw.text((px + 40, dy), h_text, font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
            lines = wrap_text(b_text, get_font(12, 'regular'), pw - 60, draw)
            ly = dy + 22
            for line in lines:
                draw.text((px + 40, ly), line, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
                ly += 18
            dy = ly + 20
            
    draw_slide_footer(draw, 6, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_06.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 07: GLOBAL DESIGN SYSTEM (Qi DS v3.3)
# -------------------------------------------------------------
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 7, "GLOBAL DESIGN SYSTEM & TOKENS", "AIA 글로벌 표준 디자인 시스템", " Qi Design System v3.3", "디자인 토큰, 아이코노그래피, 폼 필드 컴포넌트의 단일 소스 아키텍처", right_badge=("QI TOKENS V3.3", "red"))
    
    # 3 Section Cards
    # Left: Tokens & Color System (W=520)
    lx = 100
    ly = 220
    lw = 520
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=ly + 35, text="QI COLOR & TYPOGRAPHY TOKENS", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 25, ly + 65), "AIA 브랜드 시그니처 & 타이포 규격", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Color chips
    colors = [
        ("AIA Red (Primary)", "#D31145", AIA_RED, "브랜드 메인 액션 및 강조"),
        ("AIA Deep Red", "#9E002B", AIA_RED_DARK, "다크 테마 헤더 및 그라디언트"),
        ("Slate Black (Text)", "#0F172A", (15, 23, 42), "본문 고대비 시인성 텍스트"),
        ("Card Border", "#E2E8F0", (226, 232, 240), "명확한 경계선 및 컨테이너"),
        ("Success Green", "#10B981", (16, 185, 129), "정상 납부 및 승인 완료"),
        ("Alert Amber", "#F59E0B", (245, 158, 11), "미납 알림 및 주의 사항")
    ]
    cy = ly + 115
    for c_name, c_hex, c_rgb, c_sub in colors:
        draw.rounded_rectangle([lx + 25, cy, lx + 75, cy + 50], radius=8, fill=c_rgb)
        draw.text((lx + 90, cy + 6), c_name, font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((lx + 90, cy + 28), f"{c_hex}  ·  {c_sub}", font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_SUB)
        cy += 64
        
    # Typography Scale
    draw.text((lx + 25, cy + 10), "시스템 타이포그래피 스케일", font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN)
    typo_scales = [
        ("Hero Display", "32px / Bold", "메인 환영 메시지 및 총 자산"),
        ("Title Large", "24px / Bold", "각 서비스 헤더 및 핵심 금액"),
        ("Senior Body", "18px / SemiBold", "고령자 모드 기본 본문 텍스트"),
        ("General Body", "14px / Regular", "일반 모드 리스트 및 부가 안내")
    ]
    ty = cy + 40
    for t_name, t_size, t_desc in typo_scales:
        draw.text((lx + 25, ty), t_name, font=get_font(12, 'bold'), fill=AIA_RED)
        draw.text((lx + 130, ty), t_size, font=get_font(12, 'medium'), fill=TEXT_LIGHT_MAIN)
        draw.text((lx + 250, ty), t_desc, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
        ty += 32
        
    # Middle: Real Qi Icon Matrix (W=540)
    mx = 650
    mw = 540
    draw.rounded_rectangle([mx, ly, mx + mw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=mx + 25, cy=ly + 35, text="QI ICONOGRAPHY SYSTEM", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((mx + 25, ly + 65), "24dp 픽셀 퍼펙트 벡터 아이콘 세트", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Embed real extracted Qi Icon Matrix image
    qi_icon_path = os.path.join(QI_DIR, "qi_icon_matrix.png")
    if os.path.exists(qi_icon_path):
        qicon = Image.open(qi_icon_path).convert('RGBA')
        # Scale to fit ~500w x 360h
        qicon = qicon.resize((490, 360), Image.Resampling.LANCZOS)
        img.paste(qicon, (mx + 25, ly + 115), qicon)
        
    # Icon System Rules
    iry = ly + 500
    draw.text((mx + 25, iry), "Qi 아이콘 시스템 설계 원칙", font=get_font(14, 'bold'), fill=(29, 78, 216))
    irules = [
        "24x24dp 바운딩 박스 & 2dp 스트로크 두께 통일",
        "광학적 중심(Optical Center) 보정으로 시각적 균형 유지",
        "고령자 모드 전용 32dp 라지 아이콘 매핑 테이블 구축",
        "SVG 벡터 기반 Flutter / React 다형성 지원"
    ]
    iry += 30
    for r in irules:
        draw.text((mx + 25, iry), "•", font=get_font(12, 'bold'), fill=(29, 78, 216))
        draw.text((mx + 42, iry), r, font=get_font(12, 'regular'), fill=TEXT_LIGHT_MAIN)
        iry += 28
        
    # Right: Real Qi Input Component Specs (W=500)
    rx = 1220
    rw = 600
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 35, text="QI INPUT & FORM COMPONENTS", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 25, ly + 65), "입력 컴포넌트 & 인터랙션 상태 머신", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Embed real extracted Qi Input Component image
    qi_input_path = os.path.join(QI_DIR, "qi_input_component.png")
    if os.path.exists(qi_input_path):
        qinput = Image.open(qi_input_path).convert('RGBA')
        qinput = qinput.resize((550, 420), Image.Resampling.LANCZOS)
        img.paste(qinput, (rx + 25, ly + 115), qinput)
        
    # Input System Rules
    c_desc_y = ly + 560
    draw.text((rx + 25, c_desc_y), "컴포넌트 접근성 표준화 지침", font=get_font(14, 'bold'), fill=(5, 150, 105))
    c_rules = [
        "기본 56dp 높이 보장으로 터치 오류 방지",
        "에러 발생 시 텍스트 + 색상 + 햅틱 삼중 피드백",
        "포커스 시 2px 아웃라인으로 키보드 탐색 완벽 대응"
    ]
    c_desc_y += 30
    for cr in c_rules:
        draw.text((rx + 25, c_desc_y), "✔", font=get_font(12, 'bold'), fill=(5, 150, 105))
        draw.text((rx + 45, c_desc_y), cr, font=get_font(12, 'regular'), fill=TEXT_LIGHT_MAIN)
        c_desc_y += 28
        
    draw_slide_footer(draw, 7, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_07.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 08: CORE JOURNEY 01 - PREMIUM PAYMENT
# -------------------------------------------------------------
def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 8, "CORE JOURNEY 01 · PREMIUM PAYMENT", "보험료 간편 납부 & 실시간 가상계좌", " 엔드투엔드 여정", "당월/미납 보험료 조회부터 주거래 계좌 출금 및 가상계좌 즉시 입금 완료까지", right_badge=("CONVERSION 89.4%", "red"))
    
    # 4 Sequential Screen Mockups
    screens = [
        ("STEP 01", "계약 및 납부액 조회", "screen_pay_list_senior.png", "보유 계약 중 납입 대상 자동 집계 및 굵은 글씨 안내"),
        ("STEP 02", "납부 계좌 1-Tap 선택", "screen_pay_input_account.png", "기등록 주거래 계좌 즉시 선택 또는 계좌 변경"),
        ("STEP 03", "가상계좌 즉시 발급", "screen_pay_virtual.png", "입금 전용 가상계좌 발급 및 문자/카카오톡 전송"),
        ("STEP 04", "납부 완료 & 케어 안내", "screen_pay_done.png", "영수증 즉시 발급 및 매월 5일 자동이체 등록 유도")
    ]
    
    sw = 395
    sh = 730
    start_x = 100
    start_y = 220
    
    for i, (step_tag, step_title, s_file, s_desc) in enumerate(screens):
        sx = start_x + i * (sw + 23)
        draw.rounded_rectangle([sx, start_y, sx + sw, start_y + sh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Tag & Title
        draw_pill_badge(draw, left_x=sx + 20, cy=start_y + 35, text=step_tag, font=get_font(10.5, 'bold'), theme='red' if i==3 else 'blue', pad_x=12, height=24)
        draw.text((sx + 20, start_y + 65), step_title, font=get_font(16.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        # Device Mockup
        screen_path = os.path.join(CORE_DIR, s_file)
        draw_phone_mockup(img, screen_path, cx=sx + sw // 2, cy=start_y + 370, phone_w=240, phone_h=480, bezel=8, radius=30)
        
        # Desc Box
        draw.rounded_rectangle([sx + 20, start_y + sh - 95, sx + sw - 20, start_y + sh - 25], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        lines = wrap_text(s_desc, get_font(12, 'regular'), sw - 60, draw)
        dy = start_y + sh - 82
        for line in lines:
            draw.text((sx + 30, dy), line, font=get_font(12, 'medium'), fill=TEXT_LIGHT_MAIN)
            dy += 18
            
    draw_slide_footer(draw, 8, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_08.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
