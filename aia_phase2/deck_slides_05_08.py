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
# SLIDE 05: FLOW CHART (Service Decision Logic & Journey)
# -------------------------------------------------------------
def make_slide_05():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 5, 
        "FLOW CHART & DECISION LOGIC", 
        "Flow Chart | ", 
        "고령자 모드 서비스 흐름도 및 분기 로직", 
        "로그인 감지부터 납부 수단(계좌/가상계좌) 선택 및 실시간 피드백까지의 엔드투엔드 의사결정 트리", 
        right_badge=("SERVICE LOGIC", "green")
    )
    
    # Large Canvas for Visual Flow Chart
    card_x, card_y, card_w, card_h = 100, 220, 1720, 730
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    # Step 1: User Entry Node
    n1_x, n1_y, n1_w, n1_h = 160, 320, 220, 90
    draw.rounded_rectangle([n1_x, n1_y, n1_x + n1_w, n1_y + n1_h], radius=12, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, cx=n1_x + n1_w//2, cy=n1_y + 24, text="START", font=get_font(10, 'bold'), theme='gray', pad_x=10, height=20)
    draw.text((n1_x + n1_w//2, n1_y + 58), "AIA+ 앱 실행", font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    # Arrow to Mode Check
    draw_arrow(draw, (n1_x + n1_w, n1_y + n1_h//2), (n1_x + n1_w + 50, n1_y + n1_h//2), col=(100, 116, 139), width=2)
    
    # Step 2: Decision Node (연령 및 설정 확인)
    d1_x, d1_y, d1_w, d1_h = 430, 305, 260, 120
    # Diamond shape or highlighted decision box
    draw.rounded_rectangle([d1_x, d1_y, d1_x + d1_w, d1_y + d1_h], radius=16, fill=(255, 241, 244), outline=AIA_RED, width=2)
    draw_pill_badge(draw, cx=d1_x + d1_w//2, cy=d1_y + 25, text="MODE CHECK", font=get_font(10, 'bold'), theme='red', pad_x=10, height=22)
    draw.text((d1_x + d1_w//2, d1_y + 60), "65세 이상 or 간편모드 설정?", font=get_font(13.5, 'bold'), fill=AIA_RED, anchor='mm')
    draw.text((d1_x + d1_w//2, d1_y + 88), "회원 DB 연령 및 세션 분석", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    # Branches from Decision Node:
    # 1. NO -> General Mode (Upwards)
    draw_arrow(draw, (d1_x + d1_w//2, d1_y), (d1_x + d1_w//2, d1_y - 45), col=(100, 116, 139), width=2)
    draw.text((d1_x + d1_w//2 + 15, d1_y - 25), "NO", font=get_font(11, 'bold'), fill=(100, 116, 139))
    draw.rounded_rectangle([d1_x - 20, d1_y - 75, d1_x + d1_w + 20, d1_y - 45], radius=8, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((d1_x + d1_w//2, d1_y - 60), "일반 통합 모드 메인 화면 이동", font=get_font(12, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    # 2. YES -> Senior Home (Right)
    draw_arrow(draw, (d1_x + d1_w, d1_y + d1_h//2), (d1_x + d1_w + 60, d1_y + d1_h//2), col=AIA_RED, width=2)
    draw.text((d1_x + d1_w + 20, d1_y + d1_h//2 - 14), "YES", font=get_font(11, 'bold'), fill=AIA_RED)
    
    # Step 3: Senior Mode Home Dashboard
    n2_x, n2_y, n2_w, n2_h = 750, 310, 260, 110
    draw.rounded_rectangle([n2_x, n2_y, n2_x + n2_w, n2_y + n2_h], radius=14, fill=CARD_LIGHT, outline=AIA_RED, width=2)
    draw_pill_badge(draw, cx=n2_x + n2_w//2, cy=n2_y + 24, text="SENIOR DASHBOARD", font=get_font(10.5, 'bold'), theme='red', pad_x=12, height=22)
    draw.text((n2_x + n2_w//2, n2_y + 60), "고령자 전용 원터치 홈", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((n2_x + n2_w//2, n2_y + 86), "당월 미납금 및 4대 과업 즉시 노출", font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    # Arrow to Action Selection
    draw_arrow(draw, (n2_x + n2_w, n2_y + n2_h//2), (n2_x + n2_w + 60, n2_y + n2_h//2), col=AIA_RED, width=2)
    
    # Step 4: Core Payment Action Node
    n3_x, n3_y, n3_w, n3_h = 1070, 310, 260, 110
    draw.rounded_rectangle([n3_x, n3_y, n3_x + n3_w, n3_y + n3_h], radius=14, fill=(255, 241, 244), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, cx=n3_x + n3_w//2, cy=n3_y + 24, text="ACTION: 납입", font=get_font(10.5, 'bold'), theme='red', pad_x=12, height=22)
    draw.text((n3_x + n3_w//2, n3_y + 60), "보험료 바로 내기 탭", font=get_font(16, 'bold'), fill=AIA_RED, anchor='mm')
    draw.text((n3_x + n3_w//2, n3_y + 86), "하단 56dp 풀와이드 [다음] CTA", font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    # Decision Node 2: Payment Method (계좌이체 vs 가상계좌)
    draw_arrow(draw, (n3_x + n3_w, n3_y + n3_h//2), (n3_x + n3_w + 50, n3_y + n3_h//2), col=AIA_RED, width=2)
    
    d2_x, d2_y, d2_w, d2_h = 1380, 305, 260, 120
    draw.rounded_rectangle([d2_x, d2_y, d2_x + d2_w, d2_y + d2_h], radius=16, fill=(240, 246, 255), outline=(59, 130, 246), width=2)
    draw_pill_badge(draw, cx=d2_x + d2_w//2, cy=d2_y + 25, text="PAYMENT METHOD", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((d2_x + d2_w//2, d2_y + 60), "납부 수단 1-Tap 선택", font=get_font(14, 'bold'), fill=(29, 78, 216), anchor='mm')
    draw.text((d2_x + d2_w//2, d2_y + 88), "기등록 계좌 vs 가상계좌 발급", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    # Bottom Branches from Payment Method to Completion:
    # Path A: Registered Bank Account (Down-Left)
    draw.line([(d2_x + 70, d2_y + d2_h), (d2_x + 70, 520)], fill=(59, 130, 246), width=2)
    draw_arrow(draw, (d2_x + 70, 520), (1200, 520), col=(59, 130, 246), width=2)
    
    p1_x, p1_y, p1_w, p1_h = 920, 480, 260, 80
    draw.rounded_rectangle([p1_x, p1_y, p1_x + p1_w, p1_y + p1_h], radius=12, fill=(239, 246, 255), outline=BORDER_LIGHT, width=1)
    draw.text((p1_x + p1_w//2, p1_y + 28), "A. 주거래 계좌 즉시 출금", font=get_font(13.5, 'bold'), fill=(29, 78, 216), anchor='mm')
    draw.text((p1_x + p1_w//2, p1_y + 54), "48px 대형 간편 PIN 비밀번호 인증", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    # Path B: Virtual Account (Down-Right)
    draw.line([(d2_x + 190, d2_y + d2_h), (d2_x + 190, 520)], fill=AIA_RED, width=2)
    draw_arrow(draw, (d2_x + 190, 520), (1400, 520), col=AIA_RED, width=2)
    
    p2_x, p2_y, p2_w, p2_h = 1400, 480, 260, 80
    draw.rounded_rectangle([p2_x, p2_y, p2_x + p2_w, p2_y + p2_h], radius=12, fill=(255, 241, 244), outline=BORDER_LIGHT, width=1)
    draw.text((p2_x + p2_w//2, p2_y + 28), "B. 입금 전용 가상계좌 발급", font=get_font(13.5, 'bold'), fill=AIA_RED, anchor='mm')
    draw.text((p2_x + p2_w//2, p2_y + 54), "계좌번호 카카오톡/문자 즉시 전송", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    # Merge both paths down to Final Completion
    draw.line([(p1_x + p1_w//2, p1_y + p1_h), (p1_x + p1_w//2, 640)], fill=(16, 185, 129), width=2)
    draw.line([(p2_x + p2_w//2, p2_y + p2_h), (p2_x + p2_w//2, 640)], fill=(16, 185, 129), width=2)
    draw.line([(p1_x + p1_w//2, 640), (p2_x + p2_w//2, 640)], fill=(16, 185, 129), width=2)
    draw_arrow(draw, ((p1_x + p1_w//2 + p2_x + p2_w//2)//2, 640), ((p1_x + p1_w//2 + p2_x + p2_w//2)//2, 680), col=(16, 185, 129), width=2)
    
    # Final Completion Node
    fin_x, fin_y, fin_w, fin_h = 1050, 680, 480, 110
    draw.rounded_rectangle([fin_x, fin_y, fin_x + fin_w, fin_y + fin_h], radius=16, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw_pill_badge(draw, cx=fin_x + fin_w//2, cy=fin_y + 25, text="COMPLETE & REASSURANCE", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=22)
    draw.text((fin_x + fin_w//2, fin_y + 60), "납부 완료 안내 & 안심 알림톡 발송", font=get_font(16, 'bold'), fill=(5, 150, 105), anchor='mm')
    draw.text((fin_x + fin_w//2, fin_y + 88), "영수증 즉시 저장 + 매월 5일 자동이체 간편 신청 팝업 케어", font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    # Left Callout Box: 3-Step Zero Friction UX Principles
    draw.rounded_rectangle([160, 480, 780, 790], radius=16, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=185, cy=510, text="ZERO-FRICTION PRINCIPLES", font=get_font(10.5, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((185, 545), "고령자 배리어프리 플로우차트 설계 원칙", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    flow_rules = [
        ("단일 화면 1개 과업 (Single Task)", "화면 전환 시마다 오직 1개의 핵심 질문과 액션만 제시하여 인지 과부하 방지"),
        ("불필요한 입력 요소 제거", "기등록 계좌를 자동 불러오고 계좌번호 마스킹으로 보안과 편의성 동시 충족"),
        ("가상계좌 대체 경로 보장", "계좌 이체 비밀번호를 잊어버린 고령자를 위해 문자 입금 가상계좌 1-Tap 발급"),
        ("시각/촉각 완료 피드백", "성공 완료 시 굵은 녹색 체크마크, 햅틱 진동, 즉시 알림톡 전송으로 안심 보장")
    ]
    fry = 585
    for rtitle, rdesc in flow_rules:
        draw.text((185, fry), "•", font=get_font(12, 'bold'), fill=AIA_RED)
        draw.text((205, fry), rtitle, font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        lines = wrap_text(rdesc, get_font(11.5, 'regular'), 550, draw)
        l_ry = fry + 20
        for line in lines:
            draw.text((205, l_ry), line, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            l_ry += 16
        fry = l_ry + 14
        
    draw_slide_footer(draw, 5, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_05.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 06: WIREFRAMES (Low-Fi Architecture & UX Annotations)
# -------------------------------------------------------------
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 6, 
        "WIREFRAMES & ANNOTATIONS", 
        "Wireframes | ", 
        "고령자 배리어프리 화면설계서 & 상세 명세", 
        "18pt 대형 활자 규격, 48dp 터치 영역, 56dp 하단 고정 CTA 버튼의 와이어프레임 구조 분석", 
        right_badge=("DETAILED SPECIFICATION", "red")
    )
    
    # 4 Sequential Wireframes with UX Callout Lines matching Behance and PLSCMV002
    wireframes = [
        {
            "tag": "WF 01 (PLSCMV002)",
            "title": "간편홈 메인 게이트 (Gate)",
            "screen": "screen_wf_plscmv002.png",
            "annotations": [
                "① 헤더: [일반용 | 간편용] 토글 스위치 (4pt+)",
                "② 개인화 알림: 최대 3건 미납/실효/만기 노출",
                "③ 내보험 카드: 스와이프 다건 조회 (최대 99개)",
                "④ 퀵액션 & 청구/대출: 5대 코어 업무 1-Tap 분기"
            ]
        },
        {
            "tag": "WF 02 (PLSDPV201)",
            "title": "계약 및 납부액 확인",
            "screen": "screen_pay_list_senior.png",
            "annotations": [
                "① 복잡한 증권번호 배제, 한글 상품명",
                "② 납입 대상 계약 체크박스 (32dp)",
                "③ 총 결제 예정 금액 28pt Bold",
                "④ 하단 [다음 (계좌선택)] 고정 버튼"
            ]
        },
        {
            "tag": "WF 03 (PLSDPV211)",
            "title": "납부 수단 선택",
            "screen": "screen_pay_input_account.png",
            "annotations": [
                "① 기등록 주거래 은행 계좌 자동 노출",
                "② 가상계좌 신청 탭 분기 옵션",
                "③ 보안 키패드 연동 안내문구",
                "④ 하단 [출금 동의 및 결제] 풀와이드"
            ]
        },
        {
            "tag": "WF 04 (PLSDPV202)",
            "title": "납부 완료 & 케어 안내",
            "screen": "screen_pay_done.png",
            "annotations": [
                "① 완료 체크 아이콘 & 안심 메시지",
                "② 결제 일시 및 승인번호 영수증",
                "③ 카카오 알림톡 발송 완료 뱃지",
                "④ 하단 [확인 (홈으로)] 원클릭 완료"
            ]
        }
    ]
    
    sw = 395
    sh = 730
    start_x = 100
    start_y = 220
    
    for i, wf in enumerate(wireframes):
        sx = start_x + i * (sw + 23)
        draw.rounded_rectangle([sx, start_y, sx + sw, start_y + sh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Tag & Title (Clean top positioning with generous 25px breathing margin)
        draw_pill_badge(draw, left_x=sx + 20, cy=start_y + 32, text=wf["tag"], font=get_font(10.5, 'bold'), theme='red' if i in [0, 3] else 'blue', pad_x=12, height=22)
        draw.text((sx + 20, start_y + 58), wf["title"], font=get_font(16.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        # Device Mockup (phone_w=208, phone_h=440, cy=start_y + 325 => top=105, strictly below title at y=58..80)
        screen_path = os.path.join(CORE_DIR, wf["screen"])
        draw_phone_mockup(img, screen_path, cx=sx + sw // 2, cy=start_y + 330, phone_w=212, phone_h=445, bezel=6, radius=24)
        
        # Wireframe Annotation Callout Box at bottom
        draw.rounded_rectangle([sx + 15, start_y + sh - 150, sx + sw - 15, start_y + sh - 15], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((sx + 25, start_y + sh - 136), "📐 화면 설계 상세 명세 (Specs)", font=get_font(11.5, 'bold'), fill=AIA_RED)
        
        ay = start_y + sh - 112
        for annot in wf["annotations"]:
            draw.text((sx + 25, ay), annot, font=get_font(11, 'medium'), fill=TEXT_LIGHT_MAIN)
            ay += 23
            
    draw_slide_footer(draw, 6, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_06.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 07: DESIGN SYSTEM (Tokens Table, Swatches & Components)
# -------------------------------------------------------------
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 7, 
        "DESIGN SYSTEM & TOKENS", 
        "Design System | ", 
        "AIA 글로벌 표준 Qi 디자인 시스템 v3.3", 
        "디자인 토큰 규격 테이블, 브랜드 컬러 팔레트, 56dp 고령자 입력 컴포넌트 표준", 
        right_badge=("QI DESIGN TOKENS", "red")
    )
    
    # 3 Section Grid matching Behance Design System section
    # Left: Design Tokens Specification Table (W=540)
    lx = 100
    ly = 220
    lw = 540
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=ly + 35, text="QI TOKEN SPECIFICATION TABLE", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 25, ly + 65), "디자인 토큰 분류 & 플랫폼 표준", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Tokens Mini Table
    th_y = ly + 110
    draw.rounded_rectangle([lx + 20, th_y, lx + lw - 20, th_y + 36], radius=6, fill=(241, 245, 249))
    draw.text((lx + 35, th_y + 18), "토큰 분류", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    draw.text((lx + 155, th_y + 18), "고령자 규격", font=get_font(11.5, 'bold'), fill=AIA_RED, anchor='lm')
    draw.text((lx + 285, th_y + 18), "일반 규격", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_SUB, anchor='lm')
    draw.text((lx + 405, th_y + 18), "WCAG 준수", font=get_font(11.5, 'bold'), fill=(16, 185, 129), anchor='lm')
    
    token_rows = [
        ("Display 폰트", "28pt Bold", "24pt Bold", "AAA (9.2:1)"),
        ("본문 Title", "20pt Bold", "16pt SemiBold", "AAA (8.6:1)"),
        ("기본 본문 Body", "18pt SemiBold", "14pt Regular", "AAA (8.4:1)"),
        ("보조 캡션", "15pt Medium", "12pt Regular", "AA (6.8:1)"),
        ("최소 터치 영역", "48 x 48 dp", "36 x 36 dp", "규제 100%"),
        ("하단 고정 CTA", "56dp 풀와이드", "48dp 기본", "Thumb Zone"),
        ("버튼 코너 라운딩", "Radius 8dp", "Radius 6dp", "인체공학"),
        ("컨테이너 보더", "2px 솔리드 라인", "1px 라인", "선명 분리")
    ]
    
    try_pos = th_y + 44
    for t_cat, t_sen, t_gen, t_wcag in token_rows:
        draw.rectangle([lx + 20, try_pos, lx + lw - 20, try_pos + 42], fill=(255, 248, 250) if "Body" in t_cat or "CTA" in t_cat else (255, 255, 255))
        draw.line([(lx + 20, try_pos + 42), (lx + lw - 20, try_pos + 42)], fill=BORDER_LIGHT, width=1)
        draw.text((lx + 35, try_pos + 21), t_cat, font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw.text((lx + 155, try_pos + 21), t_sen, font=get_font(12, 'bold'), fill=AIA_RED, anchor='lm')
        draw.text((lx + 285, try_pos + 21), t_gen, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB, anchor='lm')
        draw.text((lx + 405, try_pos + 21), t_wcag, font=get_font(11.5, 'bold'), fill=(5, 150, 105), anchor='lm')
        try_pos += 44
        
    # Bottom guideline note
    draw.rounded_rectangle([lx + 20, ly + lh - 110, lx + lw - 20, ly + lh - 25], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((lx + 35, ly + lh - 95), "💡 디자인 토큰 개발 연동 표준", font=get_font(12, 'bold'), fill=AIA_RED)
    draw.text((lx + 35, ly + lh - 70), "Figma Tokens -> JSON Schema -> Flutter AppTheme 자동 동기화", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 35, ly + lh - 48), "단일 소스 기반으로 다크/라이트 테마 및 시니어 스케일 100% 매핑", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
    
    # Middle: Real Qi Color Palette Swatches (W=520)
    mx = 670
    mw = 520
    draw.rounded_rectangle([mx, ly, mx + mw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=mx + 25, cy=ly + 35, text="BRAND COLOR PALETTE SWATCHES", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((mx + 25, ly + 65), "AIA 브랜드 시그니처 컬러 시스템", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Swatch Grid matching Behance (Rows of color boxes)
    swatches = [
        ("AIA Red (Primary)", "#D31145", AIA_RED),
        ("AIA Deep Red", "#9E002B", AIA_RED_DARK),
        ("Slate Black (Text)", "#0F172A", (15, 23, 42)),
        ("Container Slate", "#F8FAFC", (248, 250, 252)),
        ("Card Border", "#E2E8F0", (226, 232, 240)),
        ("Success Green", "#10B981", (16, 185, 129)),
        ("Alert Amber", "#F59E0B", (245, 158, 11)),
        ("Info Cerulean", "#0284C7", (2, 132, 199))
    ]
    
    sw_y = ly + 115
    for c_title, c_hex, c_rgb in swatches:
        draw.rounded_rectangle([mx + 25, sw_y, mx + 85, sw_y + 45], radius=8, fill=c_rgb, outline=BORDER_LIGHT, width=1)
        draw.text((mx + 105, sw_y + 8), c_title, font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((mx + 105, sw_y + 28), c_hex, font=get_num_font(12, 'bold'), fill=TEXT_LIGHT_SUB)
        sw_y += 58
        
    # Vector Icon Matrix Integration
    draw.text((mx + 25, sw_y + 15), "Qi 24dp/32dp 벡터 아이콘 시스템", font=get_font(14, 'bold'), fill=(29, 78, 216))
    qi_icon_path = os.path.join(QI_DIR, "qi_icon_matrix.png")
    if os.path.exists(qi_icon_path):
        qicon = Image.open(qi_icon_path).convert('RGBA')
        qicon = qicon.resize((470, 120), Image.Resampling.LANCZOS)
        img.paste(qicon, (mx + 25, sw_y + 45), qicon)
        
    # Right: Components & Form Fields (W=570)
    rx = 1220
    rw = 600
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 35, text="INPUT & BUTTON COMPONENTS", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 25, ly + 65), "고령자 인체공학 56dp 폼 컴포넌트", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    qi_input_path = os.path.join(QI_DIR, "qi_input_component.png")
    if os.path.exists(qi_input_path):
        qinput = Image.open(qi_input_path).convert('RGBA')
        qinput = qinput.resize((550, 420), Image.Resampling.LANCZOS)
        img.paste(qinput, (rx + 25, ly + 115), qinput)
        
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
# SLIDE 08: UI SCREENS PART 1 (4 Core Journey Screens)
# -------------------------------------------------------------
def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 8, 
        "UI SCREENS · CORE JOURNEY", 
        "UI Screens | ", 
        "고령자 모드 핵심 여정 4개 화면 (Row 1)", 
        "홈 대시보드, 계약 조회, 계좌 선택, 납부 완료 등 비대면 코어 서비스 화면 설계", 
        right_badge=("PRODUCTION UI", "red")
    )
    
    screens = [
        ("01. 원터치 홈", "screen_senior_main_home.png", "보유 계약 건수 및 당월 미납 보험료 한눈에 확인"),
        ("02. 계약 조회", "screen_pay_list_senior.png", "납입 대상 계약 선택 및 18pt 굵은 글씨 납부액 확인"),
        ("03. 계좌 선택", "screen_pay_input_account.png", "기등록 주거래 계좌 1-Tap 또는 가상계좌 선택"),
        ("04. 납부 완료", "screen_pay_done.png", "영수증 즉시 발급 및 카카오 알림톡 전송 완료")
    ]
    
    sw = 395
    sh = 730
    start_x = 100
    start_y = 220
    
    for i, (stitle, s_file, s_desc) in enumerate(screens):
        sx = start_x + i * (sw + 23)
        draw.rounded_rectangle([sx, start_y, sx + sw, start_y + sh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        # Tag & Title (Clean top positioning with generous 25px breathing margin)
        draw_pill_badge(draw, left_x=sx + 20, cy=start_y + 32, text=f"SCREEN 0{i+1}", font=get_font(10.5, 'bold'), theme='red' if i==3 else 'blue', pad_x=12, height=22)
        draw.text((sx + 20, start_y + 58), stitle, font=get_font(16.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        screen_path = os.path.join(CORE_DIR, s_file)
        draw_phone_mockup(img, screen_path, cx=sx + sw // 2, cy=start_y + 348, phone_w=225, phone_h=485, bezel=6, radius=26)
        
        if i < 3:
            arrow_x = sx + sw + 4
            draw_arrow(draw, (arrow_x, start_y + 348), (arrow_x + 15, start_y + 348), col=AIA_RED, width=2, arrow_size=6)
        
        draw.rounded_rectangle([sx + 20, start_y + sh - 85, sx + sw - 20, start_y + sh - 20], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        lines = wrap_text(s_desc, get_font(11.5, 'regular'), sw - 56, draw)
        dy = start_y + sh - 74
        for line in lines:
            draw.text((sx + 28, dy), line, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_MAIN)
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
