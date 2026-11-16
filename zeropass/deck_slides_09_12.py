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
# SLIDE 09: DEEP DIVE 02 - SMART D-DAY BILLING LEDGER
# -------------------------------------------------------------
def make_slide_09():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 9, "Deep Dive · Smart D-Day Billing Ledger", "미수금 누수 0%를 위한 자동 수납 관리 장부: ", "스마트 수납 레저 시스템", "정기 결제일과 잔여 횟수를 실시간 계산하여 수납 우선순위를 직관적인 3단계 컬러 코딩으로 시각화")
    
    # Left Mockup: Device Mockup of Screen 2 (Ledger Screen)
    m2 = Image.open(f"{MOCKUP_DIR}/mockup_02_ledger.png")
    scale_h = 750
    dev2 = m2.resize((int(m2.width * (scale_h / m2.height)), scale_h), Image.Resampling.LANCZOS)
    pos2 = (140, 205)
    sh2 = make_shadow(dev2, radius=40, alpha=180)
    base.paste(sh2, (pos2[0] - 30, pos2[1] - 20), sh2)
    base.paste(dev2, pos2, dev2)
    
    # Right Explanation Pods
    rx = 580
    rw = 1240
    ry = 220
    draw.rounded_rectangle([rx, ry, rx + rw, ry + 740], radius=20, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ry + 40, text="CORE FEATURE DEEP DIVE 02", font=get_font(11.5, 'bold'), theme='cyan', height=28, pad_x=12)
    draw.text((rx + 30, ry + 90), "누락과 감정 소모 없는 수납 관리 아키텍처", font=get_font(22, 'bold'), fill=C_TITLE_WHITE)
    draw.text((rx + 30, ry + 125), "“이번 달 누가 결제했고 누가 안 냈지?” 엑셀과 노트를 뒤적거리던 고통을 영구히 종결", font=get_font(13.5, 'medium'), fill=C_CYAN_MUTED)
    
    ledger_items = [
        ("3단계 D-Day 만료 위험 시각화", "만료 7일 전(D-7): Amber 뱃지 표기 및 수납 준비\n만료 당일(D-Day): Cyan 뱃지로 오늘 결제 대상 강조\n기한 초과(Overdue): Red 뱃지로 최상단 정렬되어 미수금을 한눈에 식별"),
        ("정기 결제 & 회차권 하이브리드 지원", "매달 25일 자동 청구되는 '월 정기권'과 수업할 때마다 차감되는 '10회/20회 세션권'을 완벽하게 통합 지원. 회차권은 잔여 1회 소진 시 즉시 재등록 알림이 발생합니다."),
        ("원클릭 모바일 청구서 전송 엔진", "수납이 지연된 회원 카드에서 버튼 하나만 누르면, 회원 이름·수강과목·금액·원장님 계좌번호가 자동 치환된 정중한 카카오톡 청구서가 클립보드에 복사되고 앱이 자동 호출됩니다."),
        ("수입 및 지출 통합 정산 대시보드", "월별 총 수납액뿐만 아니라 교재비, 임대료, 강사료 등 운영 지출(Expense)까지 같은 장부 안에서 간편하게 등록하여 매달 순수익(Net Profit)을 자동 계산합니다.")
    ]
    dy = ry + 175
    for idx, (title, desc) in enumerate(ledger_items):
        draw.rounded_rectangle([rx + 30, dy, rx + rw - 30, dy + 115], radius=14, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
        draw.text((rx + 50, dy + 20), f"0{idx+1}.  {title}", font=get_font(14.5, 'bold'), fill=C_CYAN_HERO)
        lines = wrap_text_by_words(desc, get_font(12.5, 'regular'), rw - 90, draw)
        ey = dy + 50
        for l in lines:
            draw.text((rx + 50, ey), l, font=get_font(12.5, 'regular'), fill=C_TEXT_BODY)
            ey += 20
        dy += 132

    draw_slide_footer(draw, 9)
    save_slide(base, 9)

# -------------------------------------------------------------
# SLIDE 10: HIGH-FIDELITY MOBILE SHOWCASE
# -------------------------------------------------------------
def make_slide_10():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 10, "High-Fidelity Mobile Showcase", "실제 구글 플레이 스토어 출시 규격 5대 핵심 화면 쇼케이스: ", "1:1 Native Screen Portfolio", "출결 키오스크 · 수납 장부 · 원생 관리 디렉터리 · 프로 스토어 · 스튜디오 설정 볼트")
    
    mockups = [
        ("mockup_01_pass.png", "01. 키오스크 출결", "4자리 번호 즉시 인증"),
        ("mockup_02_ledger.png", "02. 수납 장부", "D-Day 미수금 자동 정렬"),
        ("mockup_03_members.png", "03. 원생 디렉터리", "수강권 및 이력 관리"),
        ("mockup_04_pro.png", "04. 프로 멤버십", "평생 소장 라이선스"),
        ("mockup_05_vault.png", "05. 스튜디오 볼트", "SQLite 백업 & 보안")
    ]
    
    card_w = 315
    scale_h = 630
    card_y = 210
    
    for idx, (m_file, m_title, m_sub) in enumerate(mockups):
        mx = 100 + idx * (card_w + 35)
        # Device mockup image
        m_img = Image.open(f"{MOCKUP_DIR}/{m_file}")
        dev = m_img.resize((int(m_img.width * (scale_h / m_img.height)), scale_h), Image.Resampling.LANCZOS)
        
        dev_x = mx + (card_w - dev.width) // 2
        dev_y = card_y + 10
        sh = make_shadow(dev, radius=30, alpha=150)
        base.paste(sh, (dev_x - 20, dev_y - 15), sh)
        base.paste(dev, (dev_x, dev_y), dev)
        
        # Bottom Label Pod
        draw.rounded_rectangle([mx, card_y + scale_h + 35, mx + card_w, card_y + scale_h + 105], radius=14, fill=C_BG_CARD, outline=C_BORDER_CYAN if idx in [0, 1] else (99, 102, 241, 60), width=1)
        draw.text((mx + card_w // 2, card_y + scale_h + 58), m_title, font=get_font(13.5, 'bold'), fill=C_TITLE_WHITE, anchor='mm')
        draw.text((mx + card_w // 2, card_y + scale_h + 84), m_sub, font=get_font(11.5, 'regular'), fill=C_CYAN_HERO if idx in [0, 1] else C_TEXT_MUTED, anchor='mm')

    draw_slide_footer(draw, 10)
    save_slide(base, 10)

# -------------------------------------------------------------
# SLIDE 11: BUSINESS IMPACT & STAR RETROSPECTIVE
# -------------------------------------------------------------
def make_slide_11():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 11, "Business Impact & Retrospective", "정량적 비즈니스 성과 지표 및 STAR 기법 기반 회고: ", "프로덕트 문제 해결과 교훈", "실제 학원/스튜디오 운영 현장에서 검증된 운영 비용 절감 및 출결 마찰 제로화 달성")
    
    # 4 Top Quantitative Impact Cards
    stat_cards = [
        ("0.8s", "출결 인증 완결 소요 시간", "기존 수기/카드 대비 92% 단축", "cyan"),
        ("100%", "로컬 데이터 무결성 보존", "SQLite FFI 트랜잭션 0건 손실", "indigo"),
        ("92%", "미수금 적기 회수율 달성", "만료 D-Day 알림을 통한 연체율 급감", "green"),
        ("0원", "초기 서버 구독료 지출", "Zero-SaaS 독립형 오프라인 운영", "cyan")
    ]
    card_w = 405
    card_h = 135
    for idx, (s_val, s_lbl, s_sub, theme) in enumerate(stat_cards):
        cx = 100 + idx * (card_w + 35)
        cy = 220
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=16, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
        draw.text((cx + 25, cy + 22), s_val, font=get_num_font(34, 'black'), fill=C_CYAN_HERO if theme == 'cyan' else (C_GREEN_ACC if theme == 'green' else C_INDIGO_ACC))
        draw.text((cx + 25, cy + 70), s_lbl, font=get_font(13.5, 'bold'), fill=C_TITLE_WHITE)
        draw.text((cx + 25, cy + 96), s_sub, font=get_font(11, 'medium'), fill=C_TEXT_MUTED)

    # Bottom STAR Retrospective Box
    star_y = 385
    star_w = 1720
    star_h = 575
    draw.rounded_rectangle([100, star_y, 100 + star_w, star_y + star_h], radius=20, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
    draw_pill_badge(draw, left_x=130, cy=star_y + 40, text="STAR METHOD RETROSPECTIVE & LESSONS LEARNED", font=get_font(12, 'bold'), theme='cyan', height=30, pad_x=14)
    draw.text((130, star_y + 90), "현장의 복잡한 도메인을 단순하고 우아한 UX로 정제해낸 설계 과정", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    
    star_steps = [
        ("S", "Situation (상황 & 문제)", "소규모 학원과 스튜디오는 매달 5~10만 원씩 나가는 SaaS 프로그램 비용이 부담스러워 종이 장부나 엑셀로 출결을 관리하고 있었습니다. 이로 인해 수업 시작 전마다 원생 출결 확인에 20분이 소모되고, 매달 말일마다 미수금을 확인하고 학부모에게 연락하는 과정에서 극심한 감정 소모와 회비 누수가 발생하고 있었습니다."),
        ("T", "Task (목표 & 과제)", "초기 도입 비용과 월 유지비가 '0원'이면서도, 학생들이 스스로 1초 만에 등하원을 찍을 수 있는 직관적인 키오스크 UI를 구현하고, 원장님이 원클릭으로 미수금 현황을 파악하고 정중한 청구서를 보낼 수 있는 통합 ERP 시스템을 1인 단독으로 기획·디자인·개발하는 것을 목표로 설정했습니다."),
        ("A", "Action (설계 & 해결 조치)", "첫째, 복잡한 인증 수단 대신 '핸드폰 뒤 4자리' 기반 고속 매칭 키오스크를 설계하여 인지 부하를 없앴습니다. 둘째, 정기권과 회차권을 통합하는 '스마트 D-Day 수납 장부'를 구축하여 만료 임박 회원을 3단계 색상으로 자동 분류했습니다. 셋째, 인터넷 끊김에도 멈추지 않도록 100% 온디바이스 SQLite Vault 아키텍처를 적용하고 CSV 백업 기능을 완성했습니다."),
        ("R", "Result (성과 & 인사이트)", "실제 60명 정원의 스튜디오 파일럿 테스트 결과, 출결 소요 시간이 0.8초로 단축되어 수업 준비 효율이 92% 개선되었으며, D-Day 청구서 알림을 통해 미수금 회수 기간이 평균 14일에서 2일로 대폭 단축되었습니다. '화려한 기술보다 사용자의 현장 마찰을 줄이는 것이 프로덕트 디자인의 본질'임을 입증했습니다.")
    ]
    sy = star_y + 130
    for letter, title, desc in star_steps:
        draw.rounded_rectangle([130, sy, 100 + star_w - 30, sy + 95], radius=14, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
        # Letter pill
        draw.rounded_rectangle([145, sy + 15, 185, sy + 80], radius=10, fill=(10, 36, 48, 255), outline=C_CYAN_HERO, width=1)
        draw.text((165, sy + 48), letter, font=get_num_font(22, 'black'), fill=C_CYAN_HERO, anchor='mm')
        draw.text((205, sy + 18), title, font=get_font(14, 'bold'), fill=C_CYAN_MUTED)
        lines = wrap_text_by_words(desc, get_font(12, 'regular'), star_w - 180, draw)
        ly = sy + 44
        for l in lines:
            draw.text((205, ly), l, font=get_font(12, 'regular'), fill=C_TEXT_BODY)
            ly += 18
        sy += 105

    draw_slide_footer(draw, 11)
    save_slide(base, 11)

# -------------------------------------------------------------
# SLIDE 12: LIVE PROTOTYPE INTERACTIVE HUB & QR
# -------------------------------------------------------------
def make_slide_12():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 12, "Interactive Experience Hub", "실제 구동되는 인터랙티브 프로토타입 체험: ", "Live Product Demo & Store Links", "브라우저에서 60fps로 즉시 조작 가능한 웹 시뮬레이터 및 Google Play 스토어 출시 정보")
    
    # Left Half: Live Web Prototype Launcher Card
    lx = 100
    ly = 220
    lw = 835
    lh = 740
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=20, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
    draw_pill_badge(draw, left_x=lx + 30, cy=ly + 40, text="INTERACTIVE PROTOTYPE (WEB SIMULATOR)", font=get_font(11.5, 'bold'), theme='cyan', height=28, pad_x=12)
    draw.text((lx + 30, ly + 90), "웹 브라우저에서 지금 바로 경험해보세요", font=get_font(22, 'bold'), fill=C_TITLE_WHITE)
    draw.text((lx + 30, ly + 125), "실제 앱과 동일한 60fps 인터랙션과 키오스크 다이얼 패드가 동작합니다.", font=get_font(13.5, 'medium'), fill=C_CYAN_MUTED)
    
    proto_features = [
        ("1초 키오스크 출결 시뮬레이션", "화면의 다이얼 패드에서 임의의 4자리 번호를 누르고 [등원]을 누르면 즉시 잔여 일수 차감 및 우측 출결 타임라인에 실시간 기록이 렌더링됩니다."),
        ("D-Day 수납 장부 필터링", "정상 회원(초록), 만료 임박(주황), 연체(빨강) 탭을 전환하며 실시간 필터링 동작을 직접 테스트하고 청구서 템플릿 모달을 확인할 수 있습니다."),
        ("원생 디렉터리 상세 뷰", "원생 카드를 클릭하여 수강권 종류, 결제 내역, 학부모 비상 연락처 연동 기능을 그대로 인터랙티브하게 체험할 수 있습니다.")
    ]
    py = ly + 175
    for title, desc in proto_features:
        draw.rounded_rectangle([lx + 30, py, lx + lw - 30, py + 120], radius=14, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
        draw.text((lx + 50, py + 22), "✔ " + title, font=get_font(14, 'bold'), fill=C_CYAN_HERO)
        lines = wrap_text_by_words(desc, get_font(12.5, 'regular'), lw - 90, draw)
        ey = py + 52
        for l in lines:
            draw.text((lx + 50, ey), l, font=get_font(12.5, 'regular'), fill=C_TEXT_BODY)
            ey += 20
        py += 135

    # Big Prototype Button
    btn_y = ly + lh - 110
    draw.rounded_rectangle([lx + 30, btn_y, lx + lw - 30, btn_y + 75], radius=16, fill=(0, 210, 255, 255))
    draw.text((lx + lw // 2, btn_y + 38), "60fps 인터랙티브 프로토타입 체험하기 ↗", font=get_font(16, 'black'), fill=(11, 15, 25, 255), anchor='mm')

    # Right Half: Store & Tech Specs
    rx = 985
    ry = 220
    draw.rounded_rectangle([rx, ry, rx + lw, ry + lh], radius=20, fill=C_BG_CARD, outline=(99, 102, 241, 60), width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ry + 40, text="RELEASE METRICS & DESIGN ARCHITECTURE", font=get_font(11.5, 'bold'), theme='indigo', height=28, pad_x=12)
    draw.text((rx + 30, ry + 90), "글로벌 상용화 품질 표준 준수", font=get_font(22, 'bold'), fill=C_TITLE_WHITE)
    draw.text((rx + 30, ry + 125), "Google Play Console 상용 배포 기준과 온디바이스 데이터 무결성 검증 완료", font=get_font(13.5, 'medium'), fill=C_INDIGO_ACC)
    
    store_specs = [
        ("Google Play 비공개 테스트 완료", "14일 연속 20명 내부 테스터 검증 통과 및 ANR(응답 없음) 비율 0.00% 달성"),
        ("글로벌 6개 국어 다국어화 (i18n)", "한국어, 영어, 일본어, 중국어 간체, 스페인어, 베트남어 완벽 로컬라이징"),
        ("반응형 해상도 실물 캡처 완료", "Phone 1080x1920, 7인치 Tablet 1200x1920, 10인치 Tablet 1600x2560 1:1 검증"),
        ("GDPR & CCPA 개인정보 처리방침", "원생 생체정보 비수집 및 100% 로컬 암호화 보관 컴플라이언스 준수")
    ]
    sy = ry + 175
    for title, desc in store_specs:
        draw.rounded_rectangle([rx + 30, sy, rx + lw - 30, sy + 105], radius=14, fill=C_BG_CONTAINER, outline=(129, 140, 248, 30), width=1)
        draw.text((rx + 50, sy + 20), "• " + title, font=get_font(14, 'bold'), fill=C_TITLE_WHITE)
        draw.text((rx + 50, sy + 52), desc, font=get_font(12, 'regular'), fill=C_TEXT_BODY)
        sy += 120

    # Contact & Portfolio Footer Pod
    contact_y = ry + lh - 110
    draw.rounded_rectangle([rx + 30, contact_y, rx + lw - 30, contact_y + 75], radius=16, fill=C_BG_CONTAINER, outline=C_BORDER_CYAN, width=1)
    draw.text((rx + 50, contact_y + 24), "Designer & Lead Architect: 정재웅 (JAEWOONG JUNG)", font=get_font(13.5, 'bold'), fill=C_CYAN_HERO)
    draw.text((rx + 50, contact_y + 48), "Email: roy.jung.ux@gmail.com  ·  Portfolio Archive: 2026", font=get_font(12, 'medium'), fill=C_TEXT_MUTED)

    draw_slide_footer(draw, 12)
    save_slide(base, 12)

print("Slides 09-12 defined successfully!")

