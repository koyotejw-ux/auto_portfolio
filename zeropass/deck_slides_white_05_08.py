import os
from PIL import Image, ImageDraw, ImageFilter
from build_zeropass_white_common import (
    W, H, MOCKUP_DIR, get_font, get_num_font, wrap_text_by_words,
    draw_pill_badge, draw_slide_header, draw_slide_footer, save_slide,
    C_TITLE_BLACK, C_BLUE_HERO, C_CYAN_ACCENT, C_TEXT_BODY, C_TEXT_MUTED,
    C_BORDER_LINE, C_BG_CARD, C_BG_CONTAINER
)

def make_shadow(img, blur=44, offset=(22, 40), alpha=80):
    mask = img.split()[3]
    sh_img = Image.new('RGBA', (img.width + 120, img.height + 120), (0, 0, 0, 0))
    black = Image.new('RGBA', img.size, (0, 0, 0, alpha))
    sh_img.paste(black, (60 + offset[0], 60 + offset[1]), mask)
    return sh_img.filter(ImageFilter.GaussianBlur(blur)), (60, 60)

# ==============================================================
# SLIDE 05: USER FLOW & EXPERIENCE LOGIC
# ==============================================================
def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=5,
        category_en="USER FLOW | SERVICE INTERACTION FLOWCHART",
        title_black="사용자 행동과 판단을 이끄는 ",
        title_blue="4단계 서비스 UX 플로우차트",
        subtitle_kr="원생의 등원 인증부터 로컬 트랜잭션 차감, 수납 장부 D-Day 정렬, 원클릭 청구서 발송까지 이어지는 핵심 여정"
    )
    
    steps = [
        ("STEP 01", "키오스크 등·하원 인증", "원생이 태블릿 화면에서 전화번호 뒤 4자리를 누르고 '등원' 탭.", "입력 마찰 최소화\n큰 터치 타깃 (80dp)", "0.8초 완료", "blue"),
        ("STEP 02", "로컬 DB 트랜잭션 & 차감", "SQLite Vault에 출결 시각 기록 및 잔여 회차(-1) 또는 일수 자동 차감.", "네트워크 독립 처리\n실시간 무결성 보장", "즉시 반영", "cyan"),
        ("STEP 03", "수납 장부 D-Day 상태 갱신", "만료 7일 전 회원은 Amber(주의), 당일/초과는 Red(미수금)로 자동 정렬.", "시각적 우선순위\n미수금 누수 원천 차단", "자동 집계", "amber"),
        ("STEP 04", "원클릭 청구서 공유/알림", "원장님이 해당 회원 카드에서 터치 한 번으로 카카오톡/문자 청구서 전송.", "개인 계좌번호 자동 삽입\n정중한 알림 템플릿", "1초 전송", "green")
    ]
    
    step_w = 385
    step_h = 420
    sy = 230
    for idx, (st_num, st_title, st_desc, ux_point, badge_txt, theme) in enumerate(steps):
        sx = 100 + idx * (step_w + 50)
        draw.rounded_rectangle([sx, sy, sx + step_w, sy + step_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=sx + 24, cy=sy + 34, text=st_num, font=get_font(10.5, 'bold'), theme=theme, pad_x=10, height=24)
        draw_pill_badge(draw, cx=sx + step_w - 65, cy=sy + 34, text=badge_txt, font=get_font(10, 'bold'), theme='slate', pad_x=8, height=22)
        draw.text((sx + 24, sy + 76), st_title, font=get_font(17, 'bold'), fill=(15, 23, 42))
        
        lines = wrap_text_by_words(st_desc, get_font(13, 'regular'), step_w - 48, draw)
        ly = sy + 115
        for l in lines:
            draw.text((sx + 24, ly), l, font=get_font(13, 'regular'), fill=(71, 85, 105))
            ly += 22
            
        draw.rounded_rectangle([sx + 20, sy + step_h - 130, sx + step_w - 20, sy + step_h - 20], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((sx + 35, sy + step_h - 105), "Key UX Architecture:", font=get_font(11, 'bold'), fill=(0, 82, 255))
        u_lines = ux_point.split('\n')
        for u_idx, u in enumerate(u_lines):
            draw.text((sx + 35, sy + step_h - 80 + u_idx * 22), "• " + u, font=get_font(12, 'medium'), fill=(15, 23, 42))
            
        if idx < 3:
            arrow_x = sx + step_w + 12
            arrow_y = sy + step_h // 2
            draw.line([(arrow_x, arrow_y), (arrow_x + 24, arrow_y)], fill=(0, 82, 255), width=2)
            draw.polygon([(arrow_x + 24, arrow_y - 6), (arrow_x + 34, arrow_y), (arrow_x + 24, arrow_y + 6)], fill=(0, 82, 255))

    # Bottom Edge Case Guard Box (y=690 to 950)
    vbox_y = 690
    vbox_w = 1720
    vbox_h = 260
    draw.rounded_rectangle([100, vbox_y, 100 + vbox_w, vbox_y + vbox_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=130, cy=vbox_y + 34, text="ERROR PREVENTION & EDGE CASE HANDLING", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=26)
    draw.text((130, vbox_y + 76), "현장 실무에서 빈번한 3대 돌발 상황 대응 로직 (Edge-Case Guard)", font=get_font(18, 'bold'), fill=(15, 23, 42))
    
    edge_cases = [
        ("동일 번호 뒷자리 중복", "동일한 전화번호 뒤 4자리를 가진 원생이 2명 이상일 경우, 즉시 모달 다이얼로그로 원생 이름과 소속 반을 제시하여 오출결을 원천 차단합니다."),
        ("수강권 만료 시 출결 시도", "잔여 회차가 0회이거나 기간이 만료된 원생이 출결할 경우, 키오스크에 '원장님께 문의해주세요' 안내 및 관리자 장부에 즉시 미수금 뱃지 표기."),
        ("갑작스런 태블릿 전원 꺼짐", "모든 데이터는 SharedPreferences 캐시가 아닌 트랜잭션 단위 SQLite FFI로 커밋되므로, 비정상 종료 시에도 마지막 출결 1건까지 100% 보존됩니다.")
    ]
    ec_w = 515
    for ec_idx, (ec_tit, ec_desc) in enumerate(edge_cases):
        ec_x = 130 + ec_idx * (ec_w + 40)
        ec_y = vbox_y + 115
        draw.rounded_rectangle([ec_x, ec_y, ec_x + ec_w, ec_y + 115], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((ec_x + 18, ec_y + 18), "✔ " + ec_tit, font=get_font(13.5, 'bold'), fill=(0, 82, 255))
        ec_lines = wrap_text_by_words(ec_desc, get_font(12, 'regular'), ec_w - 36, draw)
        ey = ec_y + 46
        for l in ec_lines:
            draw.text((ec_x + 18, ey), l, font=get_font(12, 'regular'), fill=(71, 85, 105))
            ey += 18

    draw_slide_footer(draw, 5)
    save_slide(base.convert('RGB'), 5)

# ==============================================================
# SLIDE 06: WIREFRAME & ERGONOMICS
# ==============================================================
def make_slide_06():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=6,
        category_en="WIREFRAME | MOBILE UX & ERGONOMIC ARCHITECTURE",
        title_black="실제 앱 구조를 그대로 반영한 ",
        title_blue="모바일·태블릿 와이어프레임과 인체공학적 설계",
        subtitle_kr="다이얼 패드의 최소 터치 타깃 80dp 확보와 한 손 조작을 위한 엄지 조작 반경(Thumb-Zone) 최적화"
    )
    
    col_w = 540
    col_h = 740
    cy = 220
    
    ergo_cards = [
        ("ERGONOMICS 01", "키오스크 데스크 배치 앵글", "태블릿 거치대 평균 각도(45°~60°)에서 서 있는 원생의 시선과 손가락 접근 궤적을 분석하여 번호 패드를 화면 하단 55% 영역에 집중 배치.", [
            "터치 유효 타깃: 84 x 84 dp (WCAG AAA 준수)",
            "시선 고정 위치: 상단 20% 실시간 시계 & 상태 안내",
            "입력 완료 즉시 햅틱 진동 피드백 (50ms 연동)"
        ], "blue"),
        ("ERGONOMICS 02", "원장님 모바일 한 손 조작 동선", "강의 중이거나 이동 중에도 한 손 엄지손가락(Thumb-Zone)으로 모든 탭 전환 및 장부 조회가 가능하도록 하단 고정 내비게이션 바 적용.", [
            "주요 인터랙션 엄지 반경(Natural Zone) 배치",
            "상단 햄버거 메뉴 배제, 직관적 5탭 내비게이션",
            "가장 중요한 '수납 확인'을 중앙 2번 탭에 배치"
        ], "cyan"),
        ("ERGONOMICS 03", "고대비 클린 테마 시각 피로 완화", "장시간 켜두는 데스크 키오스크 특성을 고려하여 눈부심 없는 Slate Background 테마와 시인성 높은 타이포그래피 표준 수립.", [
            "글자 명도 대비비: 12.8:1 (극상의 가독성)",
            "상태별 컬러 코딩: Blue(정상), Amber(임박), Red(미수)",
            "야간 수업 중에도 눈부심 없는 정돈된 카드 UI"
        ], "slate")
    ]
    
    for idx, (pill, title, desc, bullets, theme) in enumerate(ergo_cards):
        cx = 100 + idx * (col_w + 50)
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + col_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=cx + 30, cy=cy + 36, text=pill, font=get_font(11, 'bold'), theme=theme, pad_x=12, height=26)
        draw.text((cx + 30, cy + 80), title, font=get_font(19, 'bold'), fill=(15, 23, 42))
        
        lines = wrap_text_by_words(desc, get_font(13.5, 'regular'), col_w - 60, draw)
        ly = cy + 120
        for l in lines:
            draw.text((cx + 30, ly), l, font=get_font(13.5, 'regular'), fill=(71, 85, 105))
            ly += 22
            
        draw.line([(cx + 30, cy + 220), (cx + col_w - 30, cy + 220)], fill=(226, 232, 240), width=1)
        
        draw.text((cx + 30, cy + 245), "Design Guidelines & Specs:", font=get_font(13, 'bold'), fill=(0, 82, 255))
        by = cy + 280
        for b in bullets:
            draw.rounded_rectangle([cx + 25, by, cx + col_w - 25, by + 95], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.text((cx + 40, by + 18), "✔ " + b.split(':')[0], font=get_font(13, 'bold'), fill=(15, 23, 42))
            sub_t = b.split(':')[1] if ':' in b else ""
            draw.text((cx + 40, by + 48), sub_t.strip(), font=get_font(12, 'regular'), fill=(71, 85, 105))
            by += 115

    draw_slide_footer(draw, 6)
    save_slide(base.convert('RGB'), 6)

# ==============================================================
# SLIDE 07: VISUAL DESIGN SYSTEM
# ==============================================================
def make_slide_07():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=7,
        category_en="DESIGN SYSTEM | BRAND IDENTITY & COMPONENT ARCHITECTURE",
        title_black="브랜드 정체성과 신뢰를 규정하는 ",
        title_blue="비주얼 아이덴티티 & 디자인 시스템",
        subtitle_kr="체크앤페이 핵심 디자인 컨셉, 24dp 아이코노그라피, 파운데이션 토큰 규칙(Radius·Spacing·Color)"
    )
    
    left_w = 835
    left_h = 740
    lx = 100
    ly = 220
    draw.rounded_rectangle([lx, ly, lx + left_w, ly + left_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 30, cy=ly + 36, text="FOUNDATION 01 · COLOR TOKENS", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=26)
    
    color_swatches = [
        ("Brand Blue", "#0052FF", (0, 82, 255), "메인 액션, 키오스크 등원 버튼, 활성 탭"),
        ("Cyber Cyan", "#0891B2", (8, 145, 178), "보조 기능, 프로 멤버십, 정보 하이라이트"),
        ("Success Emerald", "#10B981", (16, 185, 129), "수납 완료, 등원 완료 피드백, 정상 상태"),
        ("Warning Amber", "#F59E0B", (245, 158, 11), "만료 7일 전 임박 알림, 하원 대기"),
        ("Error Red", "#EF4444", (239, 68, 68), "회비 미수금 연체, 만료 회원 출결 차단"),
        ("Clean Slate", "#0F172A", (15, 23, 42), "메인 타이틀 텍스트, 고대비 가독성")
    ]
    sw_y = ly + 80
    for name, hex_code, rgb_val, purpose in color_swatches:
        draw.rounded_rectangle([lx + 30, sw_y, lx + 130, sw_y + 65], radius=10, fill=rgb_val, outline=(226, 232, 240), width=1)
        draw.text((lx + 150, sw_y + 14), name, font=get_font(15, 'bold'), fill=(15, 23, 42))
        draw.text((lx + 330, sw_y + 16), hex_code, font=get_num_font(13, 'bold'), fill=(0, 82, 255))
        draw.text((lx + 150, sw_y + 40), purpose, font=get_font(12, 'regular'), fill=(71, 85, 105))
        sw_y += 80

    draw.line([(lx + 30, ly + 580), (lx + left_w - 30, ly + 580)], fill=(226, 232, 240), width=1)
    draw.text((lx + 30, ly + 602), "TYPOGRAPHY HIERARCHY (Pretendard Variable)", font=get_font(13, 'bold'), fill=(0, 82, 255))
    draw.text((lx + 30, ly + 634), "Display Bold 54pt · Screen Head 24pt · Card Title 18pt · Body Medium 14pt · Caption 11pt", font=get_font(12.5, 'medium'), fill=(15, 23, 42))
    draw.text((lx + 30, ly + 668), "다국어 6개 국어(한국어, 영어, 일본어, 중국어, 스페인어, 베트남어) 완벽 렌더링 검증 완료", font=get_font(12, 'regular'), fill=(100, 116, 139))

    rx = 985
    ry = 220
    draw.rounded_rectangle([rx, ry, rx + left_w, ry + left_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ry + 36, text="FOUNDATION 02 · CORE UI COMPONENTS", font=get_font(11, 'bold'), theme='cyan', pad_x=12, height=26)
    
    # 3 Spec Boxes
    specs = [
        ("컴포넌트 1: 대형 키오스크 다이얼 & 등하원 액션 버튼", "• 번호 패드: 3x4 그리드, 최소 76dp 이상의 터치 영역으로 오터치율 0.2% 미만 달성\n• 등원 버튼: Brand Blue Filled (#0052FF), 하원 버튼: Outlined Border 스타일로 직관적 대비\n• 피드백: 터치 시 Scale(0.96) 애니메이션 및 50ms 햅틱 진동 연동"),
        ("컴포넌트 2: 원생 수강권 & 출결 상태 인포 카드", "• 상태 뱃지: [정기 32일 남음 / 초록], [회차 1회 남음 / 주황], [회비 미납 2일 / 빨강]\n• 수납 방법: 계좌이체/카드/현금 결제 방식을 아이콘과 함께 원클릭 스위칭\n• 청구서 공유: 터치 시 사전 작성된 카카오톡/SMS 청구서 템플릿 복사 및 실행"),
        ("컴포넌트 3: 매출 & 미수금 통계 대시보드 위젯", "• 이번 달 총 예상 매출 vs 실제 수납액 프로그레스 바 시각화\n• 미수금 총액과 연체 인원을 상단 메인 KPI 카드로 즉시 노출하여 긴급도 부여\n• 월별 매출 추이 비교 및 회비 납부율 통계를 1초 만에 확인 가능")
    ]
    py = ry + 80
    for s_tit, s_desc in specs:
        draw.rounded_rectangle([rx + 30, py, rx + left_w - 30, py + 195], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((rx + 48, py + 20), s_tit, font=get_font(14, 'bold'), fill=(0, 82, 255))
        for l_idx, l in enumerate(s_desc.split('\n')):
            draw.text((rx + 48, py + 52 + l_idx * 24), l, font=get_font(12.5, 'regular'), fill=(51, 65, 85))
        py += 215

    draw_slide_footer(draw, 7)
    save_slide(base.convert('RGB'), 7)

# ==============================================================
# SLIDE 08: DEEP DIVE 01 - KIOSK ATTENDANCE ENGINE (Exact Same as Smart DCA Slide 08)
# ==============================================================
def make_slide_08():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    lx = 100
    lw = 490
    draw_pill_badge(draw, left_x=lx, cy=78, text="08 CORE FEATURE | 0.8s KIOSK ATTENDANCE DOCK", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=26)
    
    t1_a = "복잡한 카드 태그 없이 "
    t1_b = "번호 4자리로,"
    font_title = get_font(33, 'extrabold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((lx, 116), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((lx + w_t1_a, 116), t1_b, font=font_title, fill=(0, 81, 255))
    
    t2_a = "0.8초 만에 "
    t2_b = "출결과 차감을 완성해요."
    w_t2_a = draw.textlength(t2_a, font=font_title)
    draw.text((lx, 158), t2_a, font=font_title, fill=(0, 81, 255))
    draw.text((lx + w_t2_a, 158), t2_b, font=font_title, fill=(15, 23, 42))
    
    draw.text((lx, 210), "바코드 리더기나 지문 인식기 고장 없이, 원생이 직접 전화번호 뒤 4자리만 터치하면 즉각 인증 완결", font=get_font(13.5, 'regular'), fill=(71, 85, 105))
    
    # Left Comparison Card (Traditional vs ZeroPass)
    comp_y = 260
    comp_h = 680
    draw.rounded_rectangle([lx, comp_y, lx + lw, comp_y + comp_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=comp_y + 30, text="PARADIGM COMPARISON", font=get_font(9.5, 'bold'), theme='slate', pad_x=8, height=22)
    draw.text((lx + 24, comp_y + 58), "기존 아날로그 출결 vs 체크앤페이 원터치 키오스크", font=get_font(14.5, 'bold'), fill=(15, 23, 42))
    
    # Traditional
    draw.rounded_rectangle([lx + 24, comp_y + 95, lx + lw - 24, comp_y + 280], radius=12, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((lx + 40, comp_y + 115), "기존 종이 장부 & 바코드 카드 출결", font=get_font(13.5, 'bold'), fill=(220, 38, 38))
    t_bullets = [
        "• 종이 출석부에 손으로 이름을 적느라 원생 대기 줄 발생",
        "• 실물 카드 분실 시 재발급 비용 및 출결 누락",
        "• 수업 시작 전 15~20분 동안 강사가 출결 확인에 매달림"
    ]
    for b_idx, b in enumerate(t_bullets):
        draw.text((lx + 40, comp_y + 150 + b_idx * 38), b, font=get_font(12, 'regular'), fill=(127, 29, 29))
        
    # ZeroPass
    draw.rounded_rectangle([lx + 24, comp_y + 305, lx + lw - 24, comp_y + 645], radius=12, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx + 40, comp_y + 325), "체크앤페이 1초 원터치 키오스크 혁신", font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    z_bullets = [
        ("4자리 번호 인덱스 매칭", "SQLite 번호 역색인으로 입력 즉시 10ms 내 원생 자동 감지"),
        ("등원 / 하원 원터치 분기", "오늘 이미 등원한 원생은 하원 버튼으로 자동 스위칭"),
        ("오늘 출결 타임라인", "우측 화면에 실시간 등원 로그가 순차 렌더링되어 교차 검증"),
        ("학부모 알림 연동", "출결 즉시 등록된 연락처로 안전 도착 확인 메시지 전송")
    ]
    zy = comp_y + 365
    for z_tit, z_desc in z_bullets:
        draw.text((lx + 40, zy), "✔ " + z_tit, font=get_font(13, 'bold'), fill=(0, 82, 255))
        draw.text((lx + 40, zy + 24), z_desc, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
        zy += 65

    # Center Mockup Device (Mockup 01 Pass)
    m1 = Image.open(f"{MOCKUP_DIR}/mockup_01_pass.png").convert('RGBA')
    scale_h = 750
    dev1 = m1.resize((int(m1.width * (scale_h / m1.height)), scale_h), Image.Resampling.LANCZOS)
    pos1 = (620, 190)
    sh1, pad1 = make_shadow(dev1, blur=44, alpha=80)
    base.paste(sh1, (pos1[0] - pad1[0], pos1[1] - pad1[1]), sh1)
    base.paste(dev1, pos1, dev1)
    
    # Right Column: Flow Architecture & Metrics (x=1050 to 1820)
    rx = 1050
    rw = 770
    draw.rounded_rectangle([rx, comp_y, rx + rw, comp_y + comp_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 24, cy=comp_y + 30, text="INTERACTIVE FLOW & TELEMETRY", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((rx + 24, comp_y + 58), "초고속 출결 엔진의 기술적 무결성 지표", font=get_font(15, 'bold'), fill=(15, 23, 42))
    
    flow_cards = [
        ("0.8s 초고속 인증 속도", "터치 입력부터 SQLite 커밋 완료 및 화면 피드백까지 전 과정 0.8초 완료"),
        ("오인증 방지 2차 확인 모달", "동일한 뒷번호 4자리 보유 원생 감지 시 즉시 이름 선택 모달 팝업"),
        ("하원 잔여 수업 회차 자동 차감", "수강권 종류(월정기/회차)에 맞춘 실시간 자동 차감 트랜잭션"),
        ("100% 오프라인 동작 보증", "학원 인터넷 장애 시에도 멈춤 없이 SQLite 로컬 볼트에 무손실 커밋")
    ]
    fy = comp_y + 95
    for f_idx, (f_tit, f_desc) in enumerate(flow_cards):
        draw.rounded_rectangle([rx + 24, fy, rx + rw - 24, fy + 120], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((rx + 42, fy + 22), f"0{f_idx+1}.  {f_tit}", font=get_font(14, 'bold'), fill=(0, 82, 255))
        draw.text((rx + 42, fy + 56), f_desc, font=get_font(12.5, 'regular'), fill=(71, 85, 105))
        fy += 135

    draw_slide_footer(draw, 8)
    save_slide(base.convert('RGB'), 8)

print("Slides 05-08 defined successfully in clean white style!")
