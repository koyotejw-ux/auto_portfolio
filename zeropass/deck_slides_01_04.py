import os
from PIL import Image, ImageDraw, ImageFilter
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
# SLIDE 01: HERO COVER
# -------------------------------------------------------------
def make_slide_01():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    
    draw.line([(100, 52), (1820, 52)], fill=(0, 210, 255, 40), width=1)
    draw_pill_badge(draw, left_x=100, cy=76, text="2026 ENTERPRISE CASE STUDY", font=get_font(11.5, 'bold'), theme='cyan', pad_x=12, height=28)
    
    meta_txt = "스마트 출결 키오스크 · 학원/스튜디오 ERP · SQLite Vault · 1인 단독 기획·디자인"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=C_TEXT_BODY)
    
    draw.text((100, 146), "ZEROPASS · CHECK & PAY", font=get_font(14, 'bold'), fill=C_CYAN_HERO)
    
    title_p1 = "1초 원터치 출결, "
    title_p2 = "완벽한 수납 자동화."
    w_p1 = draw.textlength(title_p1, font=get_font(54, 'black'))
    draw.text((100, 178), title_p1, font=get_font(54, 'black'), fill=C_TITLE_WHITE)
    draw.text((100 + w_p1, 178), title_p2, font=get_font(54, 'black'), fill=C_CYAN_HERO)
    
    sub1 = "학원·교습소·피트니스·공부방 원장님의 매일 반복되는 출결 체크와 미수금 독촉 스트레스를"
    sub2 = "단 한 번의 터치와 오프라인 SQLite 볼트 아키텍처로 완전 무결하게 해결하는 엔터프라이즈 모바일 솔루션."
    draw.text((100, 256), sub1, font=get_font(15, 'regular'), fill=C_TEXT_BODY)
    draw.text((100, 282), sub2, font=get_font(15, 'regular'), fill=C_TEXT_BODY)
    
    # 4 Key Impact Metric Pods
    metrics = [
        ("0.8s", "출결 완결 속도", "키오스크 뒷번호 4자리 즉시 인증", "cyan"),
        ("100%", "로컬 데이터 영속성", "인터넷 끊김 없는 SQLite Vault", "indigo"),
        ("92%", "미수금 회수율 향상", "D-Day 실시간 자동 수납 장부", "green"),
        ("0원", "초기 서버 유지비", "Zero-Server 오프라인 클라우드 백업", "cyan")
    ]
    card_y = 350
    card_w = 195
    card_h = 135
    for idx, (m_val, m_lbl, m_desc, theme) in enumerate(metrics):
        cx = 100 + idx * (card_w + 18)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=16, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
        draw.text((cx + 18, card_y + 20), m_val, font=get_num_font(34, 'black'), fill=C_CYAN_HERO if theme == 'cyan' else (C_GREEN_ACC if theme == 'green' else C_INDIGO_ACC))
        draw.text((cx + 18, card_y + 68), m_lbl, font=get_font(13, 'bold'), fill=C_TITLE_WHITE)
        draw.text((cx + 18, card_y + 94), m_desc, font=get_font(10.5, 'medium'), fill=C_TEXT_MUTED)
        
    # Project Scope Pod
    scope_y = 515
    scope_w = 835
    scope_h = 240
    draw.rounded_rectangle([100, scope_y, 100 + scope_w, scope_y + scope_h], radius=18, fill=C_BG_CARD, outline=(0, 210, 255, 60), width=1)
    draw.text((125, scope_y + 22), "PROJECT SPECIFICATION & ARCHITECTURE OVERVIEW", font=get_font(12, 'bold'), fill=C_CYAN_HERO)
    
    spec_rows = [
        ("담당 역할", "프로덕트 기획, UX/UI 디자인 총괄, Flutter 프론트 아키텍처 (100% 1인 전담)"),
        ("핵심 과제", "원터치 출결 키오스크 인지 마찰 제거, 회비 만료·미수금 알림 장부 체계화, 로컬 보안"),
        ("기술 스택", "Flutter 3.9, SQLite Native FFI, Riverpod 3.3, CSV Import/Export, Material 3"),
        ("지원 플랫폼", "Android Phone (1080x1920), 7\" Tablet (1200x1920), 10\" Tablet (1600x2560)"),
        ("상용화 상태", "Google Play Store 비공개 테스트 완료 및 글로벌 다국어(6개 국어) 규격 대응")
    ]
    for r_idx, (k, v) in enumerate(spec_rows):
        ry = scope_y + 56 + r_idx * 34
        draw.text((125, ry), f"•  {k}", font=get_font(12, 'bold'), fill=C_TITLE_WHITE)
        draw.text((230, ry), f":  {v}", font=get_font(12, 'medium'), fill=C_TEXT_BODY)
        
    # Bottom Tag Row
    tags = ["#키오스크_UX", "#스튜디오_ERP", "#오프라인_퍼스트", "#SQLite_엔진", "#미수금_제로", "#다국어_로컬라이징"]
    tx = 100
    for t in tags:
        draw_pill_badge(draw, left_x=tx, cy=795, text=t, font=get_font(11, 'bold'), theme='slate', height=28, pad_x=12)
        tx += int(draw.textlength(t, font=get_font(11, 'bold')) + 24 + 10)
        
    # Right Hero Mockup Device Showcase (Center Pass, Right Ledger)
    m1 = Image.open(f"{MOCKUP_DIR}/mockup_01_pass.png")
    m2 = Image.open(f"{MOCKUP_DIR}/mockup_02_ledger.png")
    
    scale_h1 = 780
    scale_h2 = 690
    
    dev1 = m1.resize((int(m1.width * (scale_h1 / m1.height)), scale_h1), Image.Resampling.LANCZOS)
    dev2 = m2.resize((int(m2.width * (scale_h2 / m2.height)), scale_h2), Image.Resampling.LANCZOS)
    
    pos2 = (1420, 190)
    sh2 = make_shadow(dev2, radius=35, alpha=140)
    base.paste(sh2, (pos2[0] - 30, pos2[1] - 20), sh2)
    base.paste(dev2, pos2, dev2)
    
    pos1 = (1060, 140)
    sh1 = make_shadow(dev1, radius=45, alpha=190)
    base.paste(sh1, (pos1[0] - 30, pos1[1] - 20), sh1)
    base.paste(dev1, pos1, dev1)
    
    draw_slide_footer(draw, 1)
    save_slide(base, 1)

# -------------------------------------------------------------
# SLIDE 02: PROBLEM DEFINITION & MARKET STUDY
# -------------------------------------------------------------
def make_slide_02():
    base, draw = create_base_canvas(center_orbit=(1500, 500))
    draw_slide_header(draw, 2, "Market & Problem Study", "소규모 교육·체육 시설의 고질적 운영 병목: ", "아날로그 장부와 비싼 SaaS의 딜레마", "월 수십만 원의 구독료 부담과 인터넷 장애 공포, 미수금 관리 누수를 정밀 분석")
    
    # 3 Problem Cards
    cards = [
        ("PAIN POINT 01", "매달 고정 지출되는 고비용 SaaS 부담", 
         "소규모 교습소나 1인 PT 스튜디오의 월 고정비에서 회원관리 프로그램 구독료(월 4~12만원)는 극심한 마진 누수를 유발합니다.\n실제 필요한 기능은 출결과 수납뿐인데 불필요한 기능이 과도하게 묶여 있습니다.",
         "월 100만 원+ 연간 고정 구독료 지출", "red"),
        ("PAIN POINT 02", "수기 장부와 단체 카톡의 출결 마찰",
         "학생들이 등원할 때 종이 출석부에 손으로 적거나, 원장님이 일일이 학부모에게 수동 문자를 전송하느라 수업 시작 전 15~20분의 황금 시간이 허무하게 소모됩니다.",
         "수업 시작 전 15~20분 인지적 과부하 발생", "red"),
        ("PAIN POINT 03", "미수금 누수 및 껄끄러운 납부 독촉",
         "회원마다 다른 결제 주기(월 정기/회차제)로 인해 만료일 추적이 누락되고, 대면 독촉의 심리적 부담으로 인해 월평균 15~23%의 회비 수납 지연이 발생합니다.",
         "월 회비의 18% 이상 미수금 연체 누수", "red")
    ]
    card_w = 515
    card_h = 320
    for idx, (tag, title, body, stat, theme) in enumerate(cards):
        cx = 100 + idx * (card_w + 35)
        cy = 220
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=18, fill=C_BG_CARD, outline=(239, 68, 68, 90), width=1)
        draw_pill_badge(draw, left_x=cx + 25, cy=cy + 36, text=tag, font=get_font(11, 'bold'), theme='red', height=26, pad_x=10)
        draw.text((cx + 25, cy + 76), title, font=get_font(18, 'bold'), fill=C_TITLE_WHITE)
        lines = wrap_text_by_words(body, get_font(13.5, 'regular'), card_w - 50, draw)
        ly = cy + 120
        for l in lines:
            draw.text((cx + 25, ly), l, font=get_font(13.5, 'regular'), fill=C_TEXT_BODY)
            ly += 22
        draw.rounded_rectangle([cx + 25, cy + card_h - 60, cx + card_w - 25, cy + card_h - 20], radius=10, fill=(48, 16, 24, 255), outline=(239, 68, 68, 140), width=1)
        draw.text((cx + 40, cy + card_h - 40), f"⚠ {stat}", font=get_font(12, 'bold'), fill=C_RED_ACC, anchor='lm')

    # 3 Solution Architecture Columns Below
    sol_y = 575
    sol_h = 385
    sol_cards = [
        ("SOLUTION 01", "1초 키오스크 출결 UI", "학생/회원이 태블릿 또는 공기계 폰 화면에서 본인 전화번호 뒤 4자리만 터치하면 0.8초 내에 등·하원 처리 및 잔여 횟수 즉시 차감."),
        ("SOLUTION 02", "스마트 D-Day 수납 장부", "월 정기결제와 잔여 회차(10회/20회)를 실시간 감지하여 만료 7일 전부터 색상별(Green/Amber/Red) 위험 뱃지로 수납 우선순위 자동 분류."),
        ("SOLUTION 03", "Zero-Latency 로컬 보안 볼트", "외부 서버 의존 없이 100% 온디바이스 SQLite 암호화 보관. 인터넷 장애 시에도 키오스크가 멈추지 않으며 CSV 원클릭 백업/복원 지원.")
    ]
    for idx, (tag, title, body) in enumerate(sol_cards):
        cx = 100 + idx * (card_w + 35)
        draw.rounded_rectangle([cx, sol_y, cx + card_w, sol_y + sol_h], radius=18, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
        draw_pill_badge(draw, left_x=cx + 25, cy=sol_y + 36, text=tag, font=get_font(11, 'bold'), theme='cyan', height=26, pad_x=10)
        draw.text((cx + 25, sol_y + 76), title, font=get_font(18, 'bold'), fill=C_CYAN_HERO)
        lines = wrap_text_by_words(body, get_font(14, 'regular'), card_w - 50, draw)
        ly = sol_y + 120
        for l in lines:
            draw.text((cx + 25, ly), l, font=get_font(14, 'regular'), fill=C_TEXT_BODY)
            ly += 24
        draw.rounded_rectangle([cx + 25, sol_y + sol_h - 70, cx + card_w - 25, sol_y + sol_h - 25], radius=10, fill=(10, 36, 48, 255), outline=(0, 210, 255, 140), width=1)
        draw.text((cx + 40, sol_y + sol_h - 48), "✓ UX 성과: 운영 마찰 0건 & 출결 시간 92% 단축", font=get_font(12, 'bold'), fill=C_CYAN_HERO, anchor='lm')

    draw_slide_footer(draw, 2)
    save_slide(base, 2)

# -------------------------------------------------------------
# SLIDE 03: TARGET & PERSONA MATRIX
# -------------------------------------------------------------
def make_slide_03():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 3, "Target Persona Matrix", "현장 실무 중심의 페르소나 분석: ", "원장님과 원생의 상반된 인터랙션 니즈", "1초 안에 인증을 끝내야 하는 초등/중학생 원생과 수납 현황을 한눈에 파악해야 하는 원장님의 상호 작용 구조화")
    
    col_w = 785
    col_h = 740
    
    # Left Persona: 원장님 (관리자)
    p1_x = 100
    p1_y = 220
    draw.rounded_rectangle([p1_x, p1_y, p1_x + col_w, p1_y + col_h], radius=20, fill=C_BG_CARD, outline=C_BORDER_CYAN, width=1)
    draw_pill_badge(draw, left_x=p1_x + 30, cy=p1_y + 40, text="PRIMARY PERSONA · 원장님 (관리자)", font=get_font(12, 'bold'), theme='cyan', height=30, pad_x=14)
    draw.text((p1_x + 30, p1_y + 88), "김서연 원장님 (42세 · 음악학원 및 보컬 스튜디오 7년차 운영)", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    draw.text((p1_x + 30, p1_y + 120), "“수업 가르치기도 바쁜데 매달 미수금 확인하고 독촉 문자 보내는 게 가장 큰 스트레스예요.”", font=get_font(13.5, 'medium'), fill=C_CYAN_MUTED)
    
    # 4 Trait Boxes for Persona 1
    p1_traits = [
        ("핵심 목표 (Goals)", "• 원생 60명의 월 정기 수납 및 회차 소진을 엑셀 없이 자동 집계\n• 수업 도중 끊김 없이 데스크에 비치된 공기계로 출결 처리"),
        ("주요 불편 (Pain Points)", "• 대형 프랜차이즈 전용 프로그램은 월 구독료가 너무 비싸 부담\n• 학부모에게 회비 입금해달라고 직접 전화하기 민망하고 시간 낭비"),
        ("요구 기능 (UX Needs)", "• D-Day 기반 만료 알림 뱃지 및 청구서 원클릭 공유 템플릿\n• 복잡한 로그인/클라우드 설정 없이 백업 가능한 안전한 로컬 DB"),
        ("행동 패턴 (Behavior)", "• 아침 출근 직후 태블릿 키오스크 모드 켜두기\n• 오후 6시 수업 종료 후 수납 장부 탭에서 오늘 입금 내역 정산")
    ]
    ty = p1_y + 165
    for t_lbl, t_desc in p1_traits:
        draw.rounded_rectangle([p1_x + 30, ty, p1_x + col_w - 30, ty + 120], radius=14, fill=C_BG_CONTAINER, outline=(0, 210, 255, 40), width=1)
        draw.text((p1_x + 50, ty + 20), t_lbl, font=get_font(13.5, 'bold'), fill=C_CYAN_HERO)
        lines = t_desc.split('\n')
        for l_idx, l in enumerate(lines):
            draw.text((p1_x + 50, ty + 50 + l_idx * 24), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
        ty += 135

    # Right Persona: 원생/학부모 (키오스크 사용자)
    p2_x = 935
    p2_y = 220
    draw.rounded_rectangle([p2_x, p2_y, p2_x + col_w, p2_y + col_h], radius=20, fill=C_BG_CARD, outline=(129, 140, 248, 80), width=1)
    draw_pill_badge(draw, left_x=p2_x + 30, cy=p2_y + 40, text="SECONDARY PERSONA · 원생 & 학부모", font=get_font(12, 'bold'), theme='indigo', height=30, pad_x=14)
    draw.text((p2_x + 30, p2_y + 88), "이도현 학생 (15세 · 중학교 2학년, 학원 등하원)", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    draw.text((p2_x + 30, p2_y + 120), "“학원 도착해서 번호 4자리만 누르면 바로 끝나니까 줄 설 필요도 없고 편해요.”", font=get_font(13.5, 'medium'), fill=C_INDIGO_ACC)
    
    p2_traits = [
        ("핵심 목표 (Goals)", "• 가방 멘 채로 1초 만에 등원 체크하고 연습실 바로 입장\n• 본인 남은 수업 회차나 수강 기간을 직관적으로 확인"),
        ("주요 불편 (Pain Points)", "• 지문 인식이 안 되거나 카드 태그를 깜빡하고 안 가져왔을 때 혼남\n• 번호 패드가 작거나 반응이 느리면 뒤에 친구들이 줄 서서 눈치 보임"),
        ("요구 기능 (UX Needs)", "• 큼직한 다이얼 패드와 즉각적인 햅틱 및 사운드 피드백\n• 등원/하원 2개의 단순 버튼으로 선택 고민 제거"),
        ("행동 패턴 (Behavior)", "• 등원 시: 핸드폰 뒤 4자리 누르고 '등원' 탭 → 0.5초 피드백 확인\n• 하원 시: 수업 종료 후 동일하게 4자리 누르고 '하원' 탭")
    ]
    ty = p2_y + 165
    for t_lbl, t_desc in p2_traits:
        draw.rounded_rectangle([p2_x + 30, ty, p2_x + col_w - 30, ty + 120], radius=14, fill=C_BG_CONTAINER, outline=(129, 140, 248, 40), width=1)
        draw.text((p2_x + 50, ty + 20), t_lbl, font=get_font(13.5, 'bold'), fill=C_INDIGO_ACC)
        lines = t_desc.split('\n')
        for l_idx, l in enumerate(lines):
            draw.text((p2_x + 50, ty + 50 + l_idx * 24), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
        ty += 135

    draw_slide_footer(draw, 3)
    save_slide(base, 3)

# -------------------------------------------------------------
# SLIDE 04: INFORMATION ARCHITECTURE (IA)
# -------------------------------------------------------------
def make_slide_04():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 4, "Information Architecture", "직관적 탐색을 위한 5대 코어 내비게이션: ", "역할 기반 모듈 아키텍처", "원터치 출결 키오스크부터 수납 장부, 원생 디렉터리, 스튜디오 설정 볼트까지 계층적 트리 구조 설계")
    
    ia_cols = [
        ("TAB 01", "출결 키오스크 (Pass)", "대형 숫자 다이얼 패드", ["4자리 번호 즉시 검색", "등원 / 하원 원터치 토글", "실시간 오늘 출결 로그 리스트", "최근 인증 원생 토스트 피드백", "전체화면 키오스크 고정 모드"]),
        ("TAB 02", "수납 장부 (Ledger)", "매출 및 미수금 종합 관리", ["월별 예상 매출 & 실수납 집계", "미수금 D-Day 위험 단계 필터", "청구서 생성 및 카톡 알림 템플릿", "현금/카드/계좌이체 결제 처리", "지출 및 강사료 정산 관리"]),
        ("TAB 03", "원생 관리 (Members)", "회원 프로필 및 수강권", ["원생 카드 및 수강 그룹(반) 분류", "수강권 등록 (월 정기 / 회차제)", "출결 히스토리 및 납부 이력 뷰", "결제자(학부모) 연락처 연동", "CSV 원생 일괄 업로드/다운"]),
        ("TAB 04", "프로 멤버십 (Pro Store)", "상용 라이선스 & 기능 확장", ["Pro 평생 소장 라이선스 관리", "데이터 무제한 원생 등록 해제", "커스텀 스튜디오 로고 브랜딩", "영구 라이선스 복원 키 관리", "프리미엄 엑셀 내보내기 팩"]),
        ("TAB 05", "스튜디오 볼트 (Settings)", "로컬 환경설정 & 보안 DB", ["스튜디오 상호 및 계좌번호 설정", "자동 출결 알림 문자 템플릿", "SQLite 로컬 백업 & 복원 볼트", "글로벌 6개 국어 다국어 전환", "다크/라이트 테마 & 보안 잠금"])
    ]
    card_w = 320
    card_h = 700
    for idx, (tab_k, tab_name, sub_title, items) in enumerate(ia_cols):
        cx = 100 + idx * (card_w + 25)
        cy = 230
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=18, fill=C_BG_CARD, outline=C_BORDER_CYAN if idx in [0, 1] else (99, 102, 241, 60), width=1)
        draw_pill_badge(draw, left_x=cx + 20, cy=cy + 34, text=tab_k, font=get_font(11, 'bold'), theme='cyan' if idx in [0, 1] else 'indigo', height=26, pad_x=10)
        draw.text((cx + 20, cy + 76), tab_name, font=get_font(18, 'bold'), fill=C_TITLE_WHITE)
        draw.text((cx + 20, cy + 104), sub_title, font=get_font(12.5, 'medium'), fill=C_CYAN_MUTED)
        draw.line([(cx + 20, cy + 130), (cx + card_w - 20, cy + 130)], fill=(0, 210, 255, 30), width=1)
        
        iy = cy + 155
        for itm in items:
            draw.rounded_rectangle([cx + 15, iy, cx + card_w - 15, iy + 85], radius=12, fill=C_BG_CONTAINER, outline=(0, 210, 255, 30), width=1)
            draw.text((cx + 28, iy + 20), "• " + itm, font=get_font(13, 'bold'), fill=C_TITLE_WHITE)
            draw.text((cx + 28, iy + 48), "Native Flutter + SQLite Sync", font=get_font(10.5, 'regular'), fill=C_TEXT_MUTED)
            iy += 100

    draw_slide_footer(draw, 4)
    save_slide(base, 4)

print("Slides 01-04 defined successfully!")

