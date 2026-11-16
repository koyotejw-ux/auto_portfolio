import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from build_zeropass_common import (
    W, H, MOCKUP_DIR, get_font, get_num_font, wrap_text_by_words,
    draw_pill_badge, create_base_canvas, draw_slide_header, draw_slide_footer, save_slide,
    C_TITLE_WHITE, C_CYAN_HERO, C_CYAN_MUTED, C_INDIGO_ACC, C_TEXT_BODY, C_TEXT_MUTED,
    C_GREEN_ACC, C_RED_ACC, C_BORDER_CYAN, C_BG_CARD, C_BG_CONTAINER
)

def make_shadow(im, radius=30, alpha=160):
    sh = Image.new('RGBA', (im.width + 60, im.height + 60), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([30, 30, 30 + im.width, 30 + im.height], radius=40, fill=(0, 0, 0, alpha))
    return sh.filter(ImageFilter.GaussianBlur(radius))

# -------------------------------------------------------------
# SLIDE 05: USER FLOW & EXPERIENCE LOGIC
# -------------------------------------------------------------
def make_slide_05():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 5, "User Flow & Experience Logic", "과업 완결 시간을 최소화하는 사용자 동선: ", "인지 부하 제로의 4-Step 워크플로우", "원생의 등원 인증부터 원장님의 수납 장부 확인, 자동 청구서 발송까지의 상호 연계 동선 분석")
    
    steps = [
        ("STEP 01", "키오스크 등·하원 인증", "원생이 태블릿 화면에서 전화번호 뒤 4자리를 누르고 '등원' 탭.", "입력 마찰 최소화\n큰 터치 타깃 (80dp)", "0.8초 완료"),
        ("STEP 02", "로컬 DB 트랜잭션 & 차감", "SQLite Vault에 출결 시각 기록 및 잔여 회차(-1) 또는 일수 자동 차감.", "네트워크 독립 처리\n실시간 무결성 보장", "즉시 반영"),
        ("STEP 03", "수납 장부 D-Day 상태 갱신", "만료 7일 전 회원은 Amber(주의), 당일/초과는 Red(미수금)로 자동 정렬.", "시각적 우선순위\n미수금 누수 원천 차단", "자동 집계"),
        ("STEP 04", "원클릭 청구서 공유/알림", "원장님이 해당 회원 카드에서 터치 한 번으로 카카오톡/문자 청구서 전송.", "개인 계좌번호 자동 삽입\n정중한 알림 템플릿", "1초 전송")
    ]
    step_w = 385
    step_h = 420
    sy = 240
    for idx, (st_num, st_title, st_desc, ux_point, badge_txt) in enumerate(steps):
        sx = 100 + idx * (step_w + 50)
        draw.rounded_rectangle([sx, sy, sx + step_w, sy + step_h], radius=18, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
        draw_pill_badge(draw, left_x=sx + 25, cy=sy + 36, text=st_num, font=get_font(11, 'bold'), theme='cyan', height=26, pad_x=10)
        draw_pill_badge(draw, cx=sx + step_w - 65, cy=sy + 36, text=badge_txt, font=get_font(10.5, 'bold'), theme='green' if idx in [0, 3] else 'indigo', height=24, pad_x=8)
        draw.text((sx + 25, sy + 82), st_title, font=get_font(18, 'bold'), fill=C_TITLE_WHITE)
        
        lines = wrap_text_by_words(st_desc, get_font(13.5, 'regular'), step_w - 50, draw)
        ly = sy + 125
        for l in lines:
            draw.text((sx + 25, ly), l, font=get_font(13.5, 'regular'), fill=C_TEXT_BODY)
            ly += 22
            
        draw.rounded_rectangle([sx + 20, sy + step_h - 130, sx + step_w - 20, sy + step_h - 20], radius=12, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
        draw.text((sx + 35, sy + step_h - 105), "Key UX Architecture:", font=get_font(11, 'bold'), fill=C_CYAN_HERO)
        u_lines = ux_point.split('\n')
        for u_idx, u in enumerate(u_lines):
            draw.text((sx + 35, sy + step_h - 80 + u_idx * 22), "• " + u, font=get_font(12, 'medium'), fill=C_TITLE_WHITE)
            
        # Arrow between steps
        if idx < 3:
            arrow_x = sx + step_w + 12
            arrow_y = sy + step_h // 2
            draw.line([(arrow_x, arrow_y), (arrow_x + 24, arrow_y)], fill=C_CYAN_HERO, width=2)
            draw.polygon([(arrow_x + 24, arrow_y - 6), (arrow_x + 34, arrow_y), (arrow_x + 24, arrow_y + 6)], fill=C_CYAN_HERO)

    # Bottom Logic Verification Box
    vbox_y = 700
    vbox_w = 1720
    vbox_h = 240
    draw.rounded_rectangle([100, vbox_y, 100 + vbox_w, vbox_y + vbox_h], radius=18, fill=C_BG_CARD, outline=(99, 102, 241, 60), width=1)
    draw_pill_badge(draw, left_x=130, cy=vbox_y + 36, text="ERROR PREVENTION & EDGE CASE HANDLING", font=get_font(11.5, 'bold'), theme='indigo', height=28, pad_x=12)
    draw.text((130, vbox_y + 80), "현장 실무에서 빈번한 3대 돌발 상황 대응 로직 (Edge-Case Guard)", font=get_font(18, 'bold'), fill=C_TITLE_WHITE)
    
    edge_cases = [
        ("동일 번호 뒷자리 중복", "동일한 전화번호 뒤 4자리를 가진 원생이 2명 이상일 경우, 즉시 모달 다이얼로그로 원생 이름과 소속 반을 제시하여 오출결을 원천 차단합니다."),
        ("수강권 만료 시 출결 시도", "잔여 회차가 0회이거나 기간이 만료된 원생이 출결할 경우, 키오스크에 '원장님께 문의해주세요' 안내 및 관리자 장부에 즉시 미수금 뱃지 표기."),
        ("갑작스런 태블릿 전원 꺼짐", "모든 데이터는 SharedPreferences 캐시가 아닌 트랜잭션 단위 SQLite FFI로 커밋되므로, 비정상 종료 시에도 마지막 출결 1건까지 100% 보존됩니다.")
    ]
    ec_w = 515
    for ec_idx, (ec_tit, ec_desc) in enumerate(edge_cases):
        ec_x = 130 + ec_idx * (ec_w + 40)
        ec_y = vbox_y + 115
        draw.rounded_rectangle([ec_x, ec_y, ec_x + ec_w, ec_y + 105], radius=12, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
        draw.text((ec_x + 18, ec_y + 16), "✔ " + ec_tit, font=get_font(13.5, 'bold'), fill=C_CYAN_HERO)
        ec_lines = wrap_text_by_words(ec_desc, get_font(12, 'regular'), ec_w - 36, draw)
        ey = ec_y + 44
        for l in ec_lines:
            draw.text((ec_x + 18, ey), l, font=get_font(12, 'regular'), fill=C_TEXT_BODY)
            ey += 18

    draw_slide_footer(draw, 5)
    save_slide(base, 5)

# -------------------------------------------------------------
# SLIDE 06: WIREFRAME & ERGONOMICS
# -------------------------------------------------------------
def make_slide_06():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 6, "Wireframe & Ergonomics", "한 손 조작(Thumb-Zone) 및 데스크 키오스크 인체공학: ", "시인성과 조작 편의 극대화", "다이얼 패드의 최소 터치 타깃 80dp 확보와 시선 흐름(F-Pattern)에 맞춘 계층적 시각 가이드")
    
    col_w = 540
    col_h = 740
    
    # 3 Ergonomic Pillars
    ergo_cards = [
        ("ERGONOMICS 01", "키오스크 데스크 배치 앵글", "태블릿 거치대 평균 각도(45°~60°)에서 서 있는 원생의 시선과 손가락 접근 궤적을 분석하여 번호 패드를 화면 하단 55% 영역에 집중 배치.", [
            "터치 유효 타깃: 84 x 84 dp (WCAG AAA 준수)",
            "시선 고정 위치: 상단 20% 실시간 시계 & 상태 안내",
            "입력 완료 즉시 햅틱 진동 피드백 (50ms)"
        ]),
        ("ERGONOMICS 02", "원장님 모바일 한 손 조작 동선", "강의 중이거나 이동 중에도 한 손 엄지손가락(Thumb-Zone)으로 모든 탭 전환 및 장부 조회가 가능하도록 하단 고정 내비게이션 바 적용.", [
            "주요 인터랙션 엄지 반경(Natural Zone) 배치",
            "상단 햄버거 메뉴 배제, 직관적 5탭 내비게이션",
            "가장 중요한 '수납 확인'을 중앙 2번 탭에 배치"
        ]),
        ("ERGONOMICS 03", "고대비 다크모드 시각 피로 완화", "장시간 켜두는 데스크 키오스크 특성을 고려하여 OLED 번인 방지 및 눈부심 없는 Slate Dark(#0B0F19) 테마를 기본 채택.", [
            "글자 명도 대비비: 12.8:1 (극상의 가독성)",
            "상태별 컬러 코딩: Cyan(정상), Amber(임박), Red(미수)",
            "야간 수업 중에도 눈부심 없는 은은한 글래스모피즘"
        ])
    ]
    for idx, (pill, title, desc, bullets) in enumerate(ergo_cards):
        cx = 100 + idx * (col_w + 50)
        cy = 220
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + col_h], radius=20, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
        draw_pill_badge(draw, left_x=cx + 30, cy=cy + 40, text=pill, font=get_font(11.5, 'bold'), theme='cyan', height=28, pad_x=12)
        draw.text((cx + 30, cy + 90), title, font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
        
        lines = wrap_text_by_words(desc, get_font(14, 'regular'), col_w - 60, draw)
        ly = cy + 135
        for l in lines:
            draw.text((cx + 30, ly), l, font=get_font(14, 'regular'), fill=C_TEXT_BODY)
            ly += 24
            
        draw.line([(cx + 30, cy + 240), (cx + col_w - 30, cy + 240)], fill=(0, 210, 255, 30), width=1)
        
        draw.text((cx + 30, cy + 265), "Design Guidelines & Specs:", font=get_font(13, 'bold'), fill=C_CYAN_HERO)
        by = cy + 305
        for b in bullets:
            draw.rounded_rectangle([cx + 25, by, cx + col_w - 25, by + 95], radius=12, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
            draw.text((cx + 40, by + 20), "✔ " + b.split(':')[0], font=get_font(13.5, 'bold'), fill=C_TITLE_WHITE)
            sub_t = b.split(':')[1] if ':' in b else ""
            draw.text((cx + 40, by + 50), sub_t.strip(), font=get_font(12, 'regular'), fill=C_CYAN_MUTED)
            by += 115

    draw_slide_footer(draw, 6)
    save_slide(base, 6)

# -------------------------------------------------------------
# SLIDE 07: VISUAL DESIGN SYSTEM
# -------------------------------------------------------------
def make_slide_07():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 7, "Visual Design System", "엔터프라이즈 신뢰성과 키오스크 가독성을 위한 디자인 토큰: ", "Cyber Slate & Electric Cyan", "일관된 UI 컴포넌트, 시맨틱 컬러 팔레트, Pretendard 가변 타이포그래피 표준 수립")
    
    # Left Half: Color Palette & Typography
    left_w = 835
    left_h = 740
    lx = 100
    ly = 220
    draw.rounded_rectangle([lx, ly, lx + left_w, ly + left_h], radius=20, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
    draw_pill_badge(draw, left_x=lx + 30, cy=ly + 40, text="SEMANTIC COLOR PALETTE & TOKENS", font=get_font(11.5, 'bold'), theme='cyan', height=28, pad_x=12)
    
    color_swatches = [
        ("Primary Cyan", "#00D2FF", (0, 210, 255), "메인 액션, 키오스크 등원 버튼, 활성 탭"),
        ("Accent Indigo", "#818CF8", (129, 140, 248), "보조 기능, 프로 멤버십, 설정 헤더"),
        ("Success Emerald", "#34D399", (52, 211, 153), "수납 완료, 등원 완료 피드백, 정상 상태"),
        ("Warning Amber", "#FBBF24", (251, 191, 36), "만료 7일 전 임박 알림, 하원 대기"),
        ("Error Red", "#F87171", (248, 113, 113), "회비 미수금 연체, 만료 회원 출결 차단"),
        ("Background Navy", "#0B0F19", (11, 15, 25), "OLED 다크 테마 배경, 시각 피로 제로")
    ]
    sw_y = ly + 80
    for name, hex_code, rgb_val, purpose in color_swatches:
        draw.rounded_rectangle([lx + 30, sw_y, lx + 130, sw_y + 65], radius=12, fill=rgb_val, outline=(255, 255, 255, 60), width=1)
        draw.text((lx + 150, sw_y + 14), name, font=get_font(15, 'bold'), fill=C_TITLE_WHITE)
        draw.text((lx + 330, sw_y + 16), hex_code, font=get_num_font(13, 'bold'), fill=C_CYAN_HERO)
        draw.text((lx + 150, sw_y + 40), purpose, font=get_font(12, 'regular'), fill=C_TEXT_BODY)
        sw_y += 80

    draw.line([(lx + 30, ly + 580), (lx + left_w - 30, ly + 580)], fill=(0, 210, 255, 30), width=1)
    draw.text((lx + 30, ly + 605), "TYPOGRAPHY HIERARCHY (Pretendard Variable)", font=get_font(13, 'bold'), fill=C_CYAN_HERO)
    draw.text((lx + 30, ly + 638), "Display Bold 54pt · Screen Head 24pt · Card Title 18pt · Body Medium 14pt · Caption 11pt", font=get_font(12.5, 'medium'), fill=C_TEXT_BODY)
    draw.text((lx + 30, ly + 672), "다국어 6개 국어(한국어, 영어, 일본어, 중국어, 스페인어, 베트남어) 완벽 렌더링 검증 완료", font=get_font(12, 'regular'), fill=C_CYAN_MUTED)

    # Right Half: UI Components Preview (Buttons, Cards, Badges)
    rx = 985
    ry = 220
    draw.rounded_rectangle([rx, ry, rx + left_w, ry + left_h], radius=20, fill=C_BG_CARD, outline=(99, 102, 241, 60), width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ry + 40, text="CORE UI COMPONENT SPECIFICATIONS", font=get_font(11.5, 'bold'), theme='indigo', height=28, pad_x=12)
    
    # 1. Kiosk Dial Pad Spec Box
    draw.rounded_rectangle([rx + 30, ry + 80, rx + left_w - 30, ry + 270], radius=16, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
    draw.text((rx + 50, ry + 102), "컴포넌트 1: 대형 키오스크 다이얼 & 등하원 액션 버튼", font=get_font(14, 'bold'), fill=C_CYAN_HERO)
    draw.text((rx + 50, ry + 130), "• 번호 패드: 3x4 그리드, 최소 76dp 이상의 터치 영역으로 오터치율 0.2% 미만 달성\n• 등원 버튼: Cyan Filled (#00D2FF), 하원 버튼: Outlined Border 스타일로 직관적 대비 부여\n• 시각/청각 피드백: 터치 시 Scale(0.96) 애니메이션 및 50ms 햅틱 진동 연동", font=get_font(12.5, 'regular'), fill=C_TEXT_BODY)
    
    # 2. Member Card Spec Box
    draw.rounded_rectangle([rx + 30, ry + 295, rx + left_w - 30, ry + 495], radius=16, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
    draw.text((rx + 50, ry + 317), "컴포넌트 2: 원생 수강권 & 출결 상태 인포 카드", font=get_font(14, 'bold'), fill=C_INDIGO_ACC)
    draw.text((rx + 50, ry + 345), "• 상태 뱃지: [정기 32일 남음 / 초록], [회차 1회 남음 / 주황], [회비 미납 2일 / 빨강]\n• 수납 방법: 계좌이체/카드/현금 결제 방식을 아이콘과 함께 원클릭 스위칭\n• 청구서 공유: 터치 시 사전 작성된 카카오톡/SMS 청구서 템플릿 복사 및 실행", font=get_font(12.5, 'regular'), fill=C_TEXT_BODY)
    
    # 3. Ledger Analytics Spec Box
    draw.rounded_rectangle([rx + 30, ry + 520, rx + left_w - 30, ry + 705], radius=16, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
    draw.text((rx + 50, ry + 542), "컴포넌트 3: 매출 & 미수금 통계 대시보드 위젯", font=get_font(14, 'bold'), fill=C_GREEN_ACC)
    draw.text((rx + 50, ry + 570), "• 이번 달 총 예상 매출 vs 실제 수납액 프로그레스 바 시각화\n• 미수금 총액과 연체 인원을 상단 메인 KPI 카드로 즉시 노출하여 긴급도 부여\n• 월별 매출 추이 비교 및 회비 납부율 통계를 1초 만에 확인 가능", font=get_font(12.5, 'regular'), fill=C_TEXT_BODY)

    draw_slide_footer(draw, 7)
    save_slide(base, 7)

# -------------------------------------------------------------
# SLIDE 08: DEEP DIVE 01 - KIOSK ATTENDANCE ENGINE
# -------------------------------------------------------------
def make_slide_08():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 8, "Deep Dive · Kiosk Attendance Engine", "0.8초 즉각 인증을 완성한 1초 원터치 키오스크: ", "초고속 출결 엔진", "원생의 핸드폰 번호 뒤 4자리 매칭 알고리즘과 100% 로컬 SQLite 트랜잭션 동기화 설계")
    
    # Left Explanation Pods
    left_w = 980
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + left_w, ly + 740], radius=20, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 40, text="CORE FEATURE DEEP DIVE 01", font=get_font(11.5, 'bold'), theme='cyan', height=28, pad_x=12)
    draw.text((130, ly + 90), "단 한 번의 터치로 끝나는 초간편 출결 UX", font=get_font(22, 'bold'), fill=C_TITLE_WHITE)
    draw.text((130, ly + 125), "복잡한 바코드 스캐너나 지문 인식기 없이, 데스크에 놓인 태블릿 화면에서 즉시 완결", font=get_font(13.5, 'medium'), fill=C_CYAN_MUTED)
    
    deep_items = [
        ("4자리 번호 인덱스 즉시 검색", "SQLite 'substr(phone, -4)' 인덱스를 구축하여 번호 입력과 동시에 10ms 이내에 해당 원생을 특정. 학생이 대기할 틈 없이 즉각 화면에 이름과 잔여 수업 일수가 팝업됩니다."),
        ("등원 / 하원 원터치 자동 분기", "오늘 이미 등원 처리된 원생인 경우 버튼이 '하원'으로 자동 전환되어, 실수로 등원을 두 번 누르거나 횟수가 중복 차감되는 문제를 원천 예방합니다."),
        ("실시간 오늘 출결 현황 타임라인", "키오스크 화면 우측에 실시간으로 출결한 학생들의 리스트(도현 등원 16:32, 민지 등원 16:30)가 스크롤되어, 뒤에 서 있는 학생과 원장님이 한눈에 출결 여부를 교차 검증합니다."),
        ("원클릭 학부모 등하원 알림 연동", "출결 즉시 등록된 학부모 연락처로 '[체크앤페이] 이도현 학생이 학원에 안전하게 도착했습니다' 메시지를 카카오톡/SMS로 전송할 수 있는 원터치 숏컷을 제공합니다.")
    ]
    dy = ly + 175
    for idx, (title, desc) in enumerate(deep_items):
        draw.rounded_rectangle([130, dy, 100 + left_w - 30, dy + 115], radius=14, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
        draw.text((150, dy + 20), f"0{idx+1}.  {title}", font=get_font(14.5, 'bold'), fill=C_CYAN_HERO)
        lines = wrap_text_by_words(desc, get_font(12.5, 'regular'), left_w - 80, draw)
        ey = dy + 50
        for l in lines:
            draw.text((150, ey), l, font=get_font(12.5, 'regular'), fill=C_TEXT_BODY)
            ey += 20
        dy += 132

    # Right Showcase: Device Mockup of Screen 1 (Pass Screen)
    m1 = Image.open(f"{MOCKUP_DIR}/mockup_01_pass.png")
    scale_h = 750
    dev1 = m1.resize((int(m1.width * (scale_h / m1.height)), scale_h), Image.Resampling.LANCZOS)
    pos1 = (1240, 205)
    sh1 = make_shadow(dev1, radius=40, alpha=180)
    base.paste(sh1, (pos1[0] - 30, pos1[1] - 20), sh1)
    base.paste(dev1, pos1, dev1)
    
    draw_slide_footer(draw, 8)
    save_slide(base, 8)

print("Slides 05-08 defined successfully!")
