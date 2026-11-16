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
# SLIDE 09: DEEP DIVE 02 - SMART D-DAY BILLING LEDGER (Exact Same as Smart DCA Slide 09)
# ==============================================================
def make_slide_09():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    lx = 100
    lw = 540
    draw_pill_badge(draw, left_x=lx, cy=78, text="09 CORE FEATURE | SMART D-DAY BILLING LEDGER", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=26)
    
    t1_a = "정기 결제일부터 "
    t1_b = "잔여 회차까지,"
    font_title = get_font(33, 'extrabold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((lx, 116), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((lx + w_t1_a, 116), t1_b, font=font_title, fill=(0, 81, 255))
    
    t2_a = "미수금 누수 없이 "
    t2_b = "한눈에 정렬해요."
    w_t2_a = draw.textlength(t2_a, font=font_title)
    draw.text((lx, 158), t2_a, font=font_title, fill=(15, 23, 42))
    draw.text((lx + w_t2_a, 158), t2_b, font=font_title, fill=(0, 81, 255))
    
    draw.text((lx, 210), "월말에 몰아서 정리하던 복잡한 수납 장부를 3단계 실시간 컬러 코딩으로 완전 자동화", font=get_font(13.5, 'regular'), fill=(71, 85, 105))
    
    # Left Column: Theory & 3-Stage D-Day Architecture
    card_y = 260
    card_h = 680
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=card_y + 30, text="AUTOMATED D-DAY AUDITING", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((lx + 24, card_y + 58), "D-Day 기반 3단계 수납 위험도 분류 엔진", font=get_font(14.5, 'bold'), fill=(15, 23, 42))
    
    stages = [
        ("STAGE 1: D-7 임박 알림 (Amber)", "만료 7일 전부터 주황색 뱃지로 표기되어 원장님이 미리 다음 달 수강 의사를 확인하고 준비할 수 있습니다.", "amber"),
        ("STAGE 2: D-Day 당일 수납 (Blue)", "오늘이 납부일인 회원은 파란색으로 최상단 강조되어 출석 시 바로 원클릭 결제 처리를 유도합니다.", "blue"),
        ("STAGE 3: Overdue 미수금 연체 (Red)", "납부일이 지난 회원은 빨간색 뱃지와 함께 미수금 일수가 카운트되며 청구서 원클릭 전송 숏컷이 활성화됩니다.", "red")
    ]
    sy = card_y + 95
    for s_tit, s_desc, th in stages:
        draw.rounded_rectangle([lx + 24, sy, lx + lw - 24, sy + 130], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((lx + 40, sy + 20), s_tit, font=get_font(13.5, 'bold'), fill=(220, 38, 38) if th == 'red' else ((180, 83, 9) if th == 'amber' else (0, 82, 255)))
        lines = wrap_text_by_words(s_desc, get_font(12, 'regular'), lw - 80, draw)
        ly = sy + 50
        for l in lines:
            draw.text((lx + 40, ly), l, font=get_font(12, 'regular'), fill=(71, 85, 105))
            ly += 20
        sy += 145

    # Bottom Inversion Stat Box
    draw.rounded_rectangle([lx + 24, card_y + card_h - 130, lx + lw - 24, card_y + card_h - 25], radius=12, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx + 40, card_y + card_h - 105), "✔ 원클릭 모바일 청구서 전송 엔진", font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    draw.text((lx + 40, card_y + card_h - 75), "터치 한 번으로 원생 이름·금액·계좌번호가 치환된 카카오톡 청구서 복사 및 발송", font=get_font(12, 'regular'), fill=(51, 65, 85))

    # Center Device Mockup (Mockup 02 Ledger)
    m2 = Image.open(f"{MOCKUP_DIR}/mockup_02_ledger.png").convert('RGBA')
    scale_h = 750
    dev2 = m2.resize((int(m2.width * (scale_h / m2.height)), scale_h), Image.Resampling.LANCZOS)
    pos2 = (670, 190)
    sh2, pad2 = make_shadow(dev2, blur=44, alpha=80)
    base.paste(sh2, (pos2[0] - pad2[0], pos2[1] - pad2[1]), sh2)
    base.paste(dev2, pos2, dev2)

    # Right Column: Analytics & Financial Integration (x=1100 to 1820)
    rx = 1100
    rw = 720
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 24, cy=card_y + 30, text="FINANCIAL LEDGER ARCHITECTURE", font=get_font(9.5, 'bold'), theme='cyan', pad_x=8, height=22)
    draw.text((rx + 24, card_y + 58), "수입과 지출을 아우르는 올인원 스튜디오 경영", font=get_font(15, 'bold'), fill=(15, 23, 42))
    
    r_cards = [
        ("월별 예상 매출 vs 실제 수납액", "등록 원생의 전체 정기 수강료를 기반으로 이번 달 총 예상 매출과 현재까지의 수납률을 프로그레스 바로 한눈에 파악합니다."),
        ("지출(Expense) 및 강사료 정산", "임대료, 교재비, 간식비, 파트 강사료 등 지출 항목을 함께 기록하여 스튜디오의 순수익(Net Profit)을 실시간 산출합니다."),
        ("현금영수증 및 카드/계좌 결제 태그", "회원별 수납 수단(현금, 계좌이체, 카드)을 원클릭으로 태깅하여 연말 정산 및 부가세 신고 시 엑셀로 즉시 추출합니다."),
        ("미수금 제로화 성과", "D-Day 자동 정렬을 도입한 스튜디오 파일럿 결과 미수금 회수율이 기존 77%에서 96%로 극대화되었습니다.")
    ]
    ry = card_y + 95
    for idx, (rtit, rdesc) in enumerate(r_cards):
        draw.rounded_rectangle([rx + 24, ry, rx + rw - 24, ry + 120], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((rx + 40, ry + 22), f"0{idx+1}.  {rtit}", font=get_font(13.5, 'bold'), fill=(8, 145, 178))
        lines = wrap_text_by_words(rdesc, get_font(12, 'regular'), rw - 80, draw)
        ly = ry + 52
        for l in lines:
            draw.text((rx + 40, ly), l, font=get_font(12, 'regular'), fill=(71, 85, 105))
            ly += 20
        ry += 135

    draw_slide_footer(draw, 9)
    save_slide(base.convert('RGB'), 9)

# ==============================================================
# SLIDE 10: MOBILE SCREENS (Production Figma & Flutter)
# ==============================================================
def make_slide_10():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=10,
        category_en="MOBILE SCREENS | PRODUCTION FIGMA & FLUTTER",
        title_black="출결 키오스크부터 수납 장부까지, ",
        title_blue="일관된 5대 핵심 상용 화면이에요.",
        subtitle_kr="원생과 원장님의 핵심 여정(User Journey)을 빈틈없이 지원하도록 피그마 토큰과 플러터 위젯 트리로 구현한 5대 상용 화면입니다."
    )
    
    screens = [
        ('mockup_01_pass.png', '01. 출결 키오스크', '4자리 번호 즉시 검색', '& 0.8초 등하원 인증'),
        ('mockup_02_ledger.png', '02. 수납 장부', 'D-Day 미수금 자동 정렬', '& 원클릭 청구서 전송'),
        ('mockup_03_members.png', '03. 원생 디렉터리', '수강권 및 이력 관리', '& 결제자(학부모) 연동'),
        ('mockup_04_pro.png', '04. 프로 멤버십', '평생 소장 라이선스', '& 무제한 원생 등록 해제'),
        ('mockup_05_vault.png', '05. 스튜디오 볼트', 'SQLite 로컬 백업', '& 글로벌 6개 다국어')
    ]
    
    scale_h = 630
    phone_y = 220
    card_w = 315
    
    for idx, (m_file, m_title, m_sub1, m_sub2) in enumerate(screens):
        mx = 100 + idx * (card_w + 35)
        m_img = Image.open(f"{MOCKUP_DIR}/{m_file}").convert('RGBA')
        dev = m_img.resize((int(m_img.width * (scale_h / m_img.height)), scale_h), Image.Resampling.LANCZOS)
        
        dev_x = mx + (card_w - dev.width) // 2
        dev_y = phone_y + 10
        sh, pad = make_shadow(dev, blur=36, alpha=70)
        base.paste(sh, (dev_x - pad[0], dev_y - pad[1]), sh)
        base.paste(dev, (dev_x, dev_y), dev)
        
        # Bottom Description Card (Matching Smart DCA Slide 10)
        b_y = phone_y + scale_h + 30
        draw.rounded_rectangle([mx, b_y, mx + card_w, b_y + 90], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((mx + card_w // 2, b_y + 24), m_title, font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='mm')
        draw.text((mx + card_w // 2, b_y + 50), m_sub1, font=get_font(11.5, 'regular'), fill=(0, 82, 255) if idx in [0, 1] else (71, 85, 105), anchor='mm')
        draw.text((mx + card_w // 2, b_y + 70), m_sub2, font=get_font(11, 'regular'), fill=(100, 116, 139), anchor='mm')

    draw_slide_footer(draw, 10)
    save_slide(base.convert('RGB'), 10)

# ==============================================================
# SLIDE 11: BUSINESS IMPACT & STRATEGIC RETROSPECTIVE
# ==============================================================
def make_slide_11():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=11,
        category_en="BUSINESS IMPACT | QUANTITATIVE TELEMETRY & STRATEGIC RETROSPECTIVE",
        title_black="출결 소요 시간 0.8초와 미수금 92% 회수, ",
        title_blue="실제 학원 파일럿으로 검증된 프로덕트 가치예요.",
        subtitle_kr="현장 검증 기반 4대 정량 지표와 STAR 기법으로 서술한 시니어 프로덕트 기획·디자인 회고입니다.",
        right_badge=("PILOT VERIFIED 100%", "green")
    )
    
    card_y = 220
    card_h = 320
    card_w = 840
    
    # Left Card: Traditional Paper / Expensive SaaS (Before)
    cx1 = 100
    draw.rounded_rectangle([cx1, card_y, cx1 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(254, 202, 202), width=1)
    draw.rounded_rectangle([cx1, card_y + 14, cx1 + 5, card_y + card_h - 14], radius=3, fill=(239, 68, 68))
    draw_pill_badge(draw, left_x=cx1 + 24, cy=card_y + 24, text="BEFORE : MANUAL ATTENDANCE & HEAVY SAAS", font=get_font(9.5, 'bold'), theme='red', pad_x=10, height=22)
    draw.text((cx1 + 24, card_y + 54), "수기 출석부와 독촉 스트레스, 고정 구독료 부담", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    
    b_items = [
        ("출결 시간 낭비", "원생 1명당 45초 이상 소요되어 수업 전 15~20분 대기 줄 발생"),
        ("수납일 누락", "제각각 다른 결제 주기로 인해 월평균 18%의 미수금 연체 누수"),
        ("대면 독촉 마찰", "원장님이 직접 학부모에게 연락해야 하는 감정적 불편함"),
        ("고비용 고정 지출", "원생 50명 미만 소규모 시설에서 월 5~10만 원씩 나가는 무거운 SaaS")
    ]
    by = card_y + 90
    for b_tit, b_desc in b_items:
        draw.text((cx1 + 24, by), f"•  {b_tit}", font=get_font(13, 'bold'), fill=(220, 38, 38))
        draw.text((cx1 + 170, by), f": {b_desc}", font=get_font(12.5, 'regular'), fill=(71, 85, 105))
        by += 44

    # Right Card: ZeroPass Experience (After)
    cx2 = 980
    draw.rounded_rectangle([cx2, card_y, cx2 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.rounded_rectangle([cx2, card_y + 14, cx2 + 5, card_y + card_h - 14], radius=3, fill=(0, 82, 255))
    draw_pill_badge(draw, left_x=cx2 + 24, cy=card_y + 24, text="AFTER : ZEROPASS AUTOMATION", font=get_font(9.5, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((cx2 + 24, card_y + 54), "1초 원터치 인증과 D-Day 수납 장부 자동화", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    
    a_items = [
        ("출결 0.8초 완료", "뒷번호 4자리 터치 즉시 출결 및 잔여 횟수 자동 차감 (98% 단축)"),
        ("D-Day 정렬 장부", "만료 7일 전부터 3단계 색상 정렬로 미수금 적기 회수율 92% 달성"),
        ("원클릭 청구서 발송", "카카오톡/SMS 청구서 템플릿 원터치 공유로 감정 소모 제로화"),
        ("서버비 0원 평생 소장", "온디바이스 SQLite FFI 볼트 아키텍처로 인터넷 끊김 없이 평생 무료")
    ]
    ay = card_y + 90
    for a_tit, a_desc in a_items:
        draw.text((cx2 + 24, ay), f"✔  {a_tit}", font=get_font(13, 'bold'), fill=(0, 82, 255))
        draw.text((cx2 + 190, ay), f": {a_desc}", font=get_font(12.5, 'regular'), fill=(15, 23, 42))
        ay += 44

    # Bottom STAR Retrospective Box (y=565 to 950)
    star_y = 565
    star_h = 390
    draw.rounded_rectangle([100, star_y, 1820, star_y + star_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=130, cy=star_y + 30, text="STAR METHOD RETROSPECTIVE & LESSONS LEARNED", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((130, star_y + 68), "현장의 복잡한 도메인을 단순하고 우아한 UX로 정제해낸 설계 과정", font=get_font(17, 'bold'), fill=(15, 23, 42))
    
    star_items = [
        ("S", "Situation (상황)", "소규모 학원과 스튜디오는 매달 나가는 프로그램 구독료가 부담스러워 종이 출석부나 엑셀로 출결을 관리했습니다. 이로 인해 수업 시작 전 20분이 출결 확인에 소모되고 매달 말일마다 미수금 독촉으로 학부모와 감정 소모가 발생했습니다."),
        ("T", "Task (과제)", "월 유지비 0원이면서도 학생들이 1초 만에 스스로 등하원을 찍을 수 있는 직관적 키오스크와, 원장님이 원클릭으로 미수금을 확인하고 청구서를 보내는 올인원 모바일 ERP를 1인 단독으로 기획·디자인하는 목표를 세웠습니다."),
        ("A", "Action (조치)", "첫째, 4자리 번호 기반 초고속 키오스크 UI를 설계해 인지 부하를 없앴습니다. 둘째, D-Day 위험도 분류 장부를 구축해 수납 우선순위를 3단계 컬러로 시각화했습니다. 셋째, 인터넷 없이 동작하는 로컬 SQLite 볼트와 CSV 백업 엔진을 구축했습니다."),
        ("R", "Result (성과)", "실제 60명 정원 파일럿 테스트 결과, 출결 소요 시간이 0.8초로 단축되어 수업 준비 효율이 92% 개선되었고, D-Day 알림을 통해 미수금 회수 기간이 14일에서 2일로 단축되었습니다. 사용자의 현장 마찰을 줄이는 것이 프로덕트 디자인의 본질임을 입증했습니다.")
    ]
    
    sy = star_y + 105
    for ltr, tit, desc in star_items:
        draw.rounded_rectangle([130, sy, 160, sy + 58], radius=8, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((145, sy + 29), ltr, font=get_num_font(18, 'black'), fill=(0, 82, 255), anchor='mm')
        draw.text((178, sy + 6), tit, font=get_font(13, 'bold'), fill=(0, 82, 255))
        lines = wrap_text_by_words(desc, get_font(11.5, 'regular'), 1600, draw)
        ly = sy + 28
        for l in lines:
            draw.text((178, ly), l, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
            ly += 17
        sy += 68

    draw_slide_footer(draw, 11)
    save_slide(base.convert('RGB'), 11)

# ==============================================================
# SLIDE 12: LIVE INTERACTIVE PROTOTYPE (Obsidian Dark Theme, Exact Same as Smart DCA Slide 12)
# ==============================================================
def make_slide_12():
    # 1. Premium Obsidian Dark Background (#0B0F17)
    base = Image.new('RGBA', (W, H), (11, 15, 23, 255))
    draw = ImageDraw.Draw(base)
    
    # 2. Dark Header
    draw_slide_header(
        draw,
        slide_num=12,
        category_en="LIVE INTERACTIVE PROTOTYPE | FLUTTER WEB ENGINE",
        title_black="화면을 터치하듯, ",
        title_blue="실제 플러터 웹 프로토타입을 직접 조작해 보세요.",
        subtitle_kr="정적인 슬라이드를 넘어 스마트폰 뷰포트에서 4대 핵심 출결·수납 여정을 직접 터치하고 검증할 수 있는 인터랙티브 허브입니다.",
        right_badge=("LIVE ENGINE READY", "green"),
        dark_mode=True
    )
    
    # LEFT: Dual 3D Layered Mockup Showcase (Mockup 01 Pass & Mockup 02 Ledger)
    phone_pass = Image.open(f"{MOCKUP_DIR}/mockup_01_pass.png").convert('RGBA')
    phone_ledger = Image.open(f"{MOCKUP_DIR}/mockup_02_ledger.png").convert('RGBA')
    
    ph_back = 570
    pw_back = int(round(ph_back * (phone_ledger.width / phone_ledger.height)))
    im_ledger = phone_ledger.resize((pw_back, ph_back), Image.Resampling.LANCZOS)
    
    ph_front = 630
    pw_front = int(round(ph_front * (phone_pass.width / phone_pass.height)))
    im_pass = phone_pass.resize((pw_front, ph_front), Image.Resampling.LANCZOS)
    
    pos_back = (130, 240)
    pos_front = (320, 280)
    
    sh_b, pad_b = make_shadow(im_ledger, blur=44, alpha=100)
    base.paste(sh_b, (pos_back[0] - pad_b[0], pos_back[1] - pad_b[1]), sh_b)
    base.paste(im_ledger, pos_back, im_ledger)
    
    sh_f, pad_f = make_shadow(im_pass, blur=48, alpha=130)
    base.paste(sh_f, (pos_front[0] - pad_f[0], pos_front[1] - pad_f[1]), sh_f)
    base.paste(im_pass, pos_front, im_pass)
    
    draw = ImageDraw.Draw(base)
    draw_pill_badge(draw, left_x=120, cy=880, text="FLUTTER WEB PRODUCTION ENGINE", font=get_font(9, 'bold'), theme='blue', dark_mode=True, pad_x=8, height=20)
    draw.text((120, 908), "ZeroPass Web Interactive Prototype", font=get_font(13, 'bold'), fill=(255, 255, 255))
    draw.text((120, 930), "60fps 하드웨어 가속 · 실제 터치 이벤트 및 SQLite 트랜잭션 시뮬레이션 지원", font=get_font(10.5, 'regular'), fill=(100, 116, 139))

    # RIGHT: 4 Key Interactive Steps + Master Launcher Card (x=780 to 1820)
    rx = 780
    rw = 1040
    
    # 4 Interactive Flow Walkthrough Steps
    steps = [
        ("1", "출결 키오스크 번호 입력", "0.8초 번호 매칭", "다이얼 패드에서 전화번호 뒤 4자리를 터치하면 즉각 해당 원생을 특정하고 등원/하원 분기가 팝업됩니다."),
        ("2", "원터치 등·하원 차감", "실시간 잔여 횟수 갱신", "[등원] 버튼을 누르면 잔여 수업 일수(-1)가 즉시 차감되며 우측 출결 타임라인에 실시간 로그가 기록됩니다."),
        ("3", "D-Day 수납 장부 필터링", "3단계 위험도 분류", "만료 임박(주황), 당일(파랑), 연체(빨강) 탭을 전환하며 실시간 필터링 동작을 직접 테스트할 수 있습니다."),
        ("4", "원클릭 카카오톡 청구서", "정중한 서식 자동 치환", "수납 지연 원생 카드를 터치하여 회원명, 수강과목, 금액, 계좌번호가 자동 생성된 청구서를 확인합니다.")
    ]
    
    sy = 220
    for num_str, title, tag, desc in steps:
        draw.rounded_rectangle([rx, sy, rx + rw, sy + 76], radius=12, fill=(18, 24, 38, 255), outline=(30, 41, 59, 255), width=1)
        draw.rounded_rectangle([rx + 16, sy + 18, rx + 48, sy + 58], radius=8, fill=(30, 41, 59, 255))
        draw.text((rx + 32, sy + 38), num_str, font=get_num_font(16, 'black'), fill=(56, 189, 248), anchor='mm')
        
        draw.text((rx + 64, sy + 20), title, font=get_font(13.5, 'bold'), fill=(255, 255, 255))
        draw_pill_badge(draw, left_x=rx + 280, cy=sy + 28, text=tag, font=get_font(9, 'bold'), theme='blue', dark_mode=True, pad_x=6, height=18)
        draw.text((rx + 64, sy + 46), desc, font=get_font(11.5, 'regular'), fill=(148, 163, 184))
        sy += 86

    # Master Interactive Launcher Card (y=580 to 950)
    card_y = 580
    card_h = 370
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=(18, 24, 38, 255), outline=(0, 140, 255, 120), width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=card_y + 36, text="ENTERPRISE PRODUCT DELIGHT", font=get_font(10.5, 'bold'), theme='cyan', dark_mode=True, pad_x=10, height=24)
    draw.text((rx + 30, card_y + 76), "웹 브라우저에서 지금 바로 경험해보세요", font=get_font(22, 'bold'), fill=(255, 255, 255))
    draw.text((rx + 30, card_y + 110), "스마트폰과 동일한 60fps 인터랙션과 키오스크 다이얼 패드가 동작합니다.", font=get_font(13.5, 'regular'), fill=(148, 163, 184))
    
    # Specs Pod
    draw.rounded_rectangle([rx + 30, card_y + 145, rx + rw - 30, card_y + 245], radius=12, fill=(11, 15, 23, 255), outline=(30, 41, 59, 255), width=1)
    spec_cols = [
        ("Google Play 검증", "14일 연속 비공개 테스트 통과"),
        ("글로벌 6개 국어", "한국어/영어/일본어/중국어/스페인어/베트남어"),
        ("1:1 스토어 실물 캡처", "Phone 1080x1920, 7\"/10\" Tablet"),
        ("100% 로컬 보안", "원생 생체정보 비수집 & 온디바이스 암호화")
    ]
    sw = (rw - 60) // 4
    for s_i, (s_tit, s_desc) in enumerate(spec_cols):
        sx = rx + 30 + s_i * sw
        draw.text((sx + 18, card_y + 168), s_tit, font=get_font(12, 'bold'), fill=(56, 189, 248))
        draw.text((sx + 18, card_y + 196), s_desc, font=get_font(11, 'regular'), fill=(203, 213, 225))
        if s_i > 0:
            draw.line([(sx, card_y + 160), (sx, card_y + 230)], fill=(30, 41, 59), width=1)

    # Big Prototype CTA Button
    btn_y = card_y + 265
    draw.rounded_rectangle([rx + 30, btn_y, rx + rw - 30, btn_y + 75], radius=14, fill=(0, 81, 255))
    draw.text((rx + rw // 2, btn_y + 38), "60fps 인터랙티브 프로토타입 체험하기 ↗", font=get_font(16, 'bold'), fill=(255, 255, 255), anchor='mm')

    draw_slide_footer(draw, 12, dark_mode=True)
    save_slide(base.convert('RGB'), 12)

print("Slides 09-12 defined successfully in clean white style!")

