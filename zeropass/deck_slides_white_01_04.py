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
# SLIDE 01: HERO COVER (Exact Same Composition as Smart DCA Slide 01)
# ==============================================================
def make_slide_01():
    base = Image.new('RGBA', (W, H), (250, 252, 255, 255))
    
    # 1. Subtle Ambient Radial Glow
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([800, 100, 1850, 850], fill=(0, 82, 255, 18))
    g_draw.ellipse([1050, 180, 1750, 780], fill=(6, 182, 212, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    
    draw = ImageDraw.Draw(base)
    
    # Hairline Top Boundary
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    # Top Kicker & Metadata
    draw_pill_badge(draw, left_x=100, cy=76, text="2026 CASE STUDY", font=get_font(11.5, 'bold'), theme='blue', has_dot=False, pad_x=12, height=28)
    
    meta_txt = "기획(PM) · UI/UX 디자인 · Android Live (v1.0) · Tablet Kiosk & ERP"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=(100, 116, 139))
    
    # Category Label
    draw.text((100, 146), "ZEROPASS · CHECK & PAY", font=get_font(14, 'bold'), fill=(0, 82, 255))
    
    # Big Clean Headline (Exact Same 56pt Black as Smart DCA)
    title_p1 = "1초 원터치 출결, "
    title_p2 = "완벽한 수납 자동화."
    w_p1 = draw.textlength(title_p1, font=get_font(56, 'black'))
    draw.text((100, 178), title_p1, font=get_font(56, 'black'), fill=(15, 23, 42))
    draw.text((100 + w_p1, 178), title_p2, font=get_font(56, 'black'), fill=(0, 82, 255))
    
    # Clean UX Subtitle (2 balanced lines)
    sub1 = "학원·교습소·피트니스 원장님의 매일 반복되는 출결 체크와 미수금 독촉 스트레스를,"
    sub2 = "단 한 번의 터치와 오프라인 SQLite 볼트 아키텍처로 완전 무결하게 해결하는 엔터프라이즈 모바일 솔루션"
    draw.text((100, 260), sub1, font=get_font(16.5, 'regular'), fill=(71, 85, 105))
    draw.text((100, 288), sub2, font=get_font(16.5, 'semibold'), fill=(30, 41, 59))
    
    # OPEN STORYLINE: Key Strengths (Exact Open Layout matching Smart DCA Slide 01)
    strengths = [
        ("01", "출결 마찰 제로", "1초 원터치 키오스크 UI", "Zero-Friction Kiosk Dial",
         "원생이 본인 전화번호 뒤 4자리만 터치하면 0.8초 내에 등·하원 처리 및 잔여 횟수가 즉시 차감되어 대기 줄을 원천 제거합니다."),
        ("02", "수납 누수 차단", "스마트 D-Day 수납 장부", "D-Day Ledger Architecture",
         "정기 결제일과 잔여 회차를 실시간 계산하여 만료 7일 전부터 3단계 색상(Green/Amber/Red)으로 수납 우선순위를 직관적으로 분류합니다."),
        ("03", "감정 소모 해소", "원클릭 모바일 청구서", "Frictionless Billing Share",
         "회원별 계좌번호와 청구 금액이 자동 치환된 정중한 카카오톡 청구서 템플릿을 터치 한 번으로 전송하여 불편한 대면 독촉을 없앴습니다."),
        ("04", "데이터 신뢰 보장", "Zero-Latency 로컬 보안 볼트", "On-Device SQLite Vault",
         "외부 유료 서버 의존 없이 100% 온디바이스 SQLite 암호화 보관으로 월 유지비 0원과 인터넷 끊김 없는 완전한 연속성을 실현했습니다.")
    ]
    
    max_badge_w = max(draw.textlength(tag, font=get_font(10, 'bold')) + 16 for _, tag, _, _, _ in strengths)
    title_x = int(round(144 + max_badge_w + 24))
    
    k_y = 358
    for idx, (num, tag, title_ko, sub_en, desc) in enumerate(strengths):
        draw.rounded_rectangle([100, k_y + 2, 136, k_y + 28], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.text((118, k_y + 15), num, font=get_font(11, 'bold'), fill=(0, 82, 255), anchor='mm')
        
        draw_pill_badge(draw, left_x=144, cy=k_y + 15, text=tag, font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=22)
        
        draw.text((title_x, k_y + 4), title_ko, font=get_font(15.5, 'bold'), fill=(15, 23, 42))
        w_title = draw.textlength(title_ko, font=get_font(15.5, 'bold'))
        draw.text((title_x + w_title + 12, k_y + 6), f"·  {sub_en}", font=get_font(12, 'medium'), fill=(100, 116, 139))
        
        words = desc.split(' ')
        lines = []
        cur_l = ""
        for w in words:
            test = (cur_l + ' ' + w).strip()
            if draw.textlength(test, font=get_font(12, 'regular')) <= 780:
                cur_l = test
            else:
                lines.append(cur_l)
                cur_l = w
        if cur_l:
            lines.append(cur_l)
            
        desc_y = k_y + 36
        for l in lines[:2]:
            draw.text((144, desc_y), l, font=get_font(12, 'regular'), fill=(71, 85, 105))
            desc_y += 20
            
        if idx < 3:
            draw.line([(100, k_y + 92), (900, k_y + 92)], fill=(226, 232, 240), width=1)
        k_y += 114

    # Right Side: Dual Flagship iPhone Mockups (Rotated -11 degrees, identical to Smart DCA)
    phone_pass = Image.open(f'{MOCKUP_DIR}/mockup_01_pass.png').convert('RGBA')
    phone_ledger = Image.open(f'{MOCKUP_DIR}/mockup_02_ledger.png').convert('RGBA')
    
    target_h = 670
    target_w = int(round(target_h * (phone_pass.width / phone_pass.height)))
    p_front = phone_pass.resize((target_w, target_h), Image.Resampling.LANCZOS)
    p_back = phone_ledger.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    angle = -11.0
    rot_front = p_front.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    rot_back = p_back.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    sh_back, pad_b = make_shadow(rot_back, blur=40, offset=(18, 34), alpha=65)
    sh_front, pad_f = make_shadow(rot_front, blur=48, offset=(24, 44), alpha=88)
    
    p_back_x, p_back_y = 1270, 115
    p_front_x, p_front_y = 970, 170
    
    base.paste(sh_back, (p_back_x - pad_b[0], p_back_y - pad_b[1]), sh_back)
    base.paste(rot_back, (p_back_x, p_back_y), rot_back)
    
    base.paste(sh_front, (p_front_x - pad_f[0], p_front_y - pad_f[1]), sh_front)
    base.paste(rot_front, (p_front_x, p_front_y), rot_front)
    
    draw = ImageDraw.Draw(base)
    
    # Bottom 4-Column Specification Strip
    bar_y = 840
    bar_h = 116
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    col_w = (1720) // 4
    specs = [
        ("PROJECT ROLE", "서비스 기획 100% · UI/UX 디자인 100%", "사용자 리서치 · 문제 정의 · IA 정보 설계 · 와이어프레임 · UI 디자인 총괄"),
        ("PERIOD & TIMELINE", "2025.02 - 2025.03 (6주 완성)", "실제 학원 및 피트니스 원장님 파일럿 검증 후 비공개 테스트 완료"),
        ("DESIGN SYSTEM", "Clean Trust White 토큰 · 컴포넌트", "8pt 베이스라인 · Electric Blue & Slate 가독성 팔레트 · 햅틱 피드백 규격"),
        ("DELIVERY & RELEASE", "Google Play 비공개 테스트 & 1:1 캡처", "Phone 1080x1920, 7\"/10\" Tablet 스토어 규격 실물 캡처 및 CSV 동기화")
    ]
    
    for i, (cat, val_bold, val_desc) in enumerate(specs):
        cx = 100 + i * col_w
        if i > 0:
            draw.line([(cx, bar_y + 18), (cx, bar_y + bar_h - 18)], fill=(226, 232, 240), width=1)
        
        draw.text((cx + 28, bar_y + 18), cat, font=get_font(11, 'bold'), fill=(0, 82, 255))
        draw.text((cx + 28, bar_y + 42), val_bold, font=get_font(14.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 28, bar_y + 70), val_desc, font=get_font(11, 'regular'), fill=(100, 116, 139))
        
    draw_slide_footer(draw, 1)
    save_slide(base.convert('RGB'), 1)

# ==============================================================
# SLIDE 02: MARKET RESEARCH & PROBLEM STUDY
# ==============================================================
def make_slide_02():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=2,
        category_en="USER RESEARCH | DESK RESEARCH & MARKET STUDY",
        title_black="소규모 교육·체육 시설의 고질적 운영 병목과 ",
        title_blue="아날로그 장부의 기존 문제점",
        subtitle_kr="소규모 학원 및 스튜디오 운영자(N=120) 심층 인터뷰와 SaaS 도입 비용 분석을 통해 도출한 3대 핵심 전략"
    )
    
    # 3 Top Problem Cards
    card_y = 220
    card_w = 535
    card_h = 330
    
    problems = [
        ("MARKET TREND", "고비용 SaaS의 불필요한 기능 과잉", "월 4~12만 원의 고정 구독료",
         "원생 30~50명 규모의 소규모 교습소나 1인 PT 샵에서 필요한 것은 '출결'과 '수납'뿐인데, 대형 학원용 종합 ERP의 과도한 기능과 높은 구독료로 인해 심각한 고정비 마진 누수가 발생하고 있습니다.",
         "연간 50~140만 원 고정 지출 부담", "red"),
        ("BOTTLENECK", "수기 장부 출결로 인한 수업 전 마찰", "수업 전 15~20분 골든타임 소모",
         "학생들이 등원할 때 종이 출석부에 손으로 이름을 적거나, 강사가 일일이 학부모에게 출석 문자를 수동 작성하느라 정작 가장 중요한 수업 준비와 오리엔테이션 시간이 낭비되고 있습니다.",
         "원생 인증 대기시간 평균 45초 소요", "amber"),
        ("FINANCIAL LEAK", "체계 없는 미수금 연체와 독촉 스트레스", "회비 납부일 누락으로 18% 연체",
         "정기 결제일과 회차권 소진 시점이 제각각 달라 만료일 파악이 어렵고, 원장님이 직접 원생이나 학부모에게 회비 납부를 요청하는 과정에서 극심한 감정 소모와 회비 누수가 발생합니다.",
         "월평균 미수금 회수 지연일 14일+", "red")
    ]
    
    for i, (badge_tag, title, highlight, desc, stat_txt, theme) in enumerate(problems):
        cx = 100 + i * (card_w + 57)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        # Left accent stripe
        draw.rounded_rectangle([cx, card_y + 14, cx + 5, card_y + card_h - 14], radius=3, fill=(239, 68, 68) if theme == 'red' else (245, 158, 11))
        
        draw_pill_badge(draw, left_x=cx + 24, cy=card_y + 26, text=badge_tag, font=get_font(10, 'bold'), theme=theme, pad_x=8, height=22)
        draw.text((cx + 24, card_y + 54), title, font=get_font(16.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 24, card_y + 82), f"•  {highlight}", font=get_font(13.5, 'semibold'), fill=(220, 38, 38) if theme == 'red' else (180, 83, 9))
        
        lines = wrap_text_by_words(desc, get_font(13, 'regular'), card_w - 48, draw)
        ly = card_y + 120
        for l in lines:
            draw.text((cx + 24, ly), l, font=get_font(13, 'regular'), fill=(71, 85, 105))
            ly += 22
            
        # Bottom Stat Box
        draw.rounded_rectangle([cx + 24, card_y + card_h - 58, cx + card_w - 24, card_y + card_h - 18], radius=8, fill=(254, 242, 242) if theme == 'red' else (254, 243, 199))
        draw.text((cx + 40, card_y + card_h - 38), f"⚠ {stat_txt}", font=get_font(12, 'bold'), fill=(220, 38, 38) if theme == 'red' else (180, 83, 9), anchor='lm')

    # Bottom 3 Solution Architecture Cards (y=580 to 950)
    sol_y = 580
    sol_h = 370
    solutions = [
        ("SOLUTION 01", "1초 키오스크 출결 UI", "0.8초 번호 인증",
         "별도의 전산 교육이나 카드 태그 없이, 데스크 공기계 화면에서 전화번호 뒤 4자리만 터치하면 0.8초 내에 등·하원 처리 및 잔여 횟수가 즉각 차감되는 무마찰 UX를 구현했습니다.",
         "✓ 출결 소요 시간 45초 → 0.8초 단축 (98% 개선)", "blue"),
        ("SOLUTION 02", "스마트 D-Day 수납 장부", "3단계 위험도 분류",
         "매달 말일에 몰아보던 방식에서 탈피하여 만료 7일 전(D-7)부터 당일, 연체 회원을 3단계 컬러 뱃지로 자동 정렬하여 수납 우선순위를 직관적으로 파악할 수 있도록 설계했습니다.",
         "✓ 미수금 회수 기간 14일 → 2일로 단축 (86% 개선)", "blue"),
        ("SOLUTION 03", "Zero-Latency 로컬 보안 볼트", "온디바이스 SQLite FFI",
         "외부 유료 클라우드에 의존하지 않고 기기 내부의 SQLite FFI 엔진을 통해 100% 로컬 암호화 보관하여 인터넷 장애 시에도 키오스크가 멈추지 않는 연속성을 확보했습니다.",
         "✓ 서버 유지비 월 0원 & 데이터 손실율 0.00%", "green")
    ]
    
    for i, (badge_tag, title, highlight, desc, stat_txt, theme) in enumerate(solutions):
        cx = 100 + i * (card_w + 57)
        draw.rounded_rectangle([cx, sol_y, cx + card_w, sol_y + sol_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([cx, sol_y + 14, cx + 5, sol_y + sol_h - 14], radius=3, fill=(0, 82, 255) if theme == 'blue' else (16, 185, 129))
        
        draw_pill_badge(draw, left_x=cx + 24, cy=sol_y + 26, text=badge_tag, font=get_font(10, 'bold'), theme=theme, pad_x=8, height=22)
        draw.text((cx + 24, sol_y + 54), title, font=get_font(16.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 24, sol_y + 82), f"•  {highlight}", font=get_font(13.5, 'semibold'), fill=(0, 82, 255) if theme == 'blue' else (5, 150, 105))
        
        lines = wrap_text_by_words(desc, get_font(13, 'regular'), card_w - 48, draw)
        ly = sol_y + 120
        for l in lines:
            draw.text((cx + 24, ly), l, font=get_font(13, 'regular'), fill=(71, 85, 105))
            ly += 22
            
        draw.rounded_rectangle([cx + 24, sol_y + sol_h - 58, cx + card_w - 24, sol_y + sol_h - 18], radius=8, fill=(239, 246, 255) if theme == 'blue' else (236, 253, 245))
        draw.text((cx + 40, sol_y + sol_h - 38), stat_txt, font=get_font(12, 'bold'), fill=(0, 82, 255) if theme == 'blue' else (5, 150, 105), anchor='lm')

    draw_slide_footer(draw, 2)
    save_slide(base.convert('RGB'), 2)

# ==============================================================
# SLIDE 03: TARGET & PERSONA MATRIX
# ==============================================================
def make_slide_03():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=3,
        category_en="TARGET & PERSONA | SEGMENTATION MATRIX & BENCHMARK",
        title_black="타깃 세그먼트 매트릭스와 ",
        title_blue="대표 페르소나 행동 지표",
        subtitle_kr="원장님(관리자)과 원생(키오스크 사용자)의 상반된 인터랙션 니즈와 행동 패턴을 구조화한 페르소나 매트릭스"
    )
    
    card_w = 835
    card_h = 740
    cy = 220
    
    # Left Persona Card: 원장님 (Primary Persona)
    cx1 = 100
    draw.rounded_rectangle([cx1, cy, cx1 + card_w, cy + card_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=cx1 + 30, cy=cy + 36, text="PRIMARY PERSONA · 스튜디오 원장님", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=26)
    draw.text((cx1 + 30, cy + 80), "김서연 원장님 (42세 · 음악학원 및 보컬 스튜디오 7년차 운영)", font=get_font(20, 'bold'), fill=(15, 23, 42))
    draw.text((cx1 + 30, cy + 112), "“수업 가르치기도 바쁜데 매달 미수금 확인하고 독촉 연락하는 게 가장 큰 스트레스예요.”", font=get_font(13.5, 'medium'), fill=(0, 82, 255))
    
    traits1 = [
        ("핵심 목표 (Goals)", "• 원생 60명의 월 정기 수납 및 회차 소진을 엑셀 없이 자동 집계\n• 수업 도중 끊김 없이 데스크에 비치된 공기계로 출결 완료"),
        ("주요 불편 (Pain Points)", "• 대형 프랜차이즈 전용 프로그램은 월 구독료가 너무 비싸 부담\n• 학부모에게 회비 입금해달라고 직접 전화하기 민망하고 시간 낭비"),
        ("요구 기능 (UX Needs)", "• D-Day 기반 만료 알림 뱃지 및 청구서 원클릭 공유 템플릿\n• 복잡한 로그인/클라우드 설정 없이 백업 가능한 안전한 로컬 DB"),
        ("행동 패턴 (Behavior)", "• 아침 출근 직후 태블릿 키오스크 모드 켜두기\n• 오후 6시 수업 종료 후 수납 장부 탭에서 오늘 입금 내역 정산")
    ]
    ty = cy + 155
    for t_lbl, t_desc in traits1:
        draw.rounded_rectangle([cx1 + 30, ty, cx1 + card_w - 30, ty + 120], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((cx1 + 48, ty + 18), t_lbl, font=get_font(13.5, 'bold'), fill=(0, 82, 255))
        for l_idx, l in enumerate(t_desc.split('\n')):
            draw.text((cx1 + 48, ty + 48 + l_idx * 24), l, font=get_font(12.5, 'regular'), fill=(51, 65, 85))
        ty += 135

    # Right Persona Card: 원생 / 학부모 (Secondary Persona)
    cx2 = 985
    draw.rounded_rectangle([cx2, cy, cx2 + card_w, cy + card_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=cx2 + 30, cy=cy + 36, text="SECONDARY PERSONA · 원생 & 학부모", font=get_font(11, 'bold'), theme='cyan', pad_x=12, height=26)
    draw.text((cx2 + 30, cy + 80), "이도현 학생 (15세 · 중학교 2학년, 학원 등하원)", font=get_font(20, 'bold'), fill=(15, 23, 42))
    draw.text((cx2 + 30, cy + 112), "“학원 도착해서 번호 4자리만 누르면 바로 끝나니까 줄 설 필요도 없고 편해요.”", font=get_font(13.5, 'medium'), fill=(8, 145, 178))
    
    traits2 = [
        ("핵심 목표 (Goals)", "• 가방 멘 채로 1초 만에 등원 체크하고 연습실 바로 입장\n• 본인 남은 수업 회차나 수강 기간을 직관적으로 확인"),
        ("주요 불편 (Pain Points)", "• 지문 인식이 안 되거나 카드 태그를 깜빡하고 안 가져왔을 때 혼남\n• 번호 패드가 작거나 반응이 느리면 뒤에 친구들이 줄 서서 눈치 보임"),
        ("요구 기능 (UX Needs)", "• 큼직한 다이얼 패드와 즉각적인 햅틱 및 사운드 피드백\n• 등원/하원 2개의 단순 버튼으로 선택 고민 제거"),
        ("행동 패턴 (Behavior)", "• 등원 시: 핸드폰 뒤 4자리 누르고 '등원' 탭 → 0.5초 피드백 확인\n• 하원 시: 수업 종료 후 동일하게 4자리 누르고 '하원' 탭")
    ]
    ty = cy + 155
    for t_lbl, t_desc in traits2:
        draw.rounded_rectangle([cx2 + 30, ty, cx2 + card_w - 30, ty + 120], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((cx2 + 48, ty + 18), t_lbl, font=get_font(13.5, 'bold'), fill=(8, 145, 178))
        for l_idx, l in enumerate(t_desc.split('\n')):
            draw.text((cx2 + 48, ty + 48 + l_idx * 24), l, font=get_font(12.5, 'regular'), fill=(51, 65, 85))
        ty += 135

    draw_slide_footer(draw, 3)
    save_slide(base.convert('RGB'), 3)

# ==============================================================
# SLIDE 04: INFORMATION ARCHITECTURE (IA)
# ==============================================================
def make_slide_04():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=4,
        category_en="INFORMATION ARCHITECTURE · SERVICE STRUCTURE",
        title_black="누구나 바로 이해하고 쓰는 ",
        title_blue="5대 핵심 메뉴 구조",
        subtitle_kr="원터치 출결부터 수납 장부, 원생 디렉터리, 보안 볼트까지 필요한 기능을 한눈에 찾을 수 있는 쉬운 화면 구성"
    )
    
    ia_cols = [
        ("TAB 01", "출결 키오스크 (Pass)", "대형 숫자 다이얼 패드", ["4자리 번호 즉시 검색", "등원 / 하원 원터치 토글", "오늘 출결 실시간 로그", "최근 인증 원생 토스트 피드백", "전체화면 키오스크 고정 모드"]),
        ("TAB 02", "수납 장부 (Ledger)", "매출 및 미수금 관리", ["월별 예상 매출 & 실수납 집계", "미수금 D-Day 위험 단계 필터", "청구서 생성 및 카톡 알림 템플릿", "현금/카드/계좌이체 결제 처리", "지출 및 강사료 정산 관리"]),
        ("TAB 03", "원생 관리 (Members)", "회원 프로필 및 수강권", ["원생 카드 및 수강 그룹(반) 분류", "수강권 등록 (월 정기 / 회차제)", "출결 히스토리 및 납부 이력 뷰", "결제자(학부모) 연락처 연동", "CSV 원생 일괄 업로드/다운"]),
        ("TAB 04", "프로 멤버십 (Pro Store)", "상용 라이선스 & 확장", ["Pro 평생 소장 라이선스 관리", "데이터 무제한 원생 등록 해제", "커스텀 스튜디오 로고 브랜딩", "영구 라이선스 복원 키 관리", "프리미엄 엑셀 내보내기 팩"]),
        ("TAB 05", "스튜디오 볼트 (Settings)", "로컬 환경설정 & 보안", ["스튜디오 상호 및 계좌번호 설정", "자동 출결 알림 문자 템플릿", "SQLite 로컬 백업 & 복원 볼트", "글로벌 6개 국어 다국어 전환", "다크/라이트 테마 & 보안 잠금"])
    ]
    
    card_w = 320
    card_h = 700
    cy = 230
    for idx, (tab_k, tab_name, sub_title, items) in enumerate(ia_cols):
        cx = 100 + idx * (card_w + 25)
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=cx + 20, cy=cy + 34, text=tab_k, font=get_font(10.5, 'bold'), theme='blue' if idx in [0, 1] else 'slate', pad_x=10, height=24)
        draw.text((cx + 20, cy + 74), tab_name, font=get_font(17, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 20, cy + 100), sub_title, font=get_font(12, 'medium'), fill=(0, 82, 255) if idx in [0, 1] else (100, 116, 139))
        draw.line([(cx + 20, cy + 124), (cx + card_w - 20, cy + 124)], fill=(226, 232, 240), width=1)
        
        iy = cy + 145
        for itm in items:
            draw.rounded_rectangle([cx + 15, iy, cx + card_w - 15, iy + 85], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.text((cx + 26, iy + 20), "• " + itm, font=get_font(12.5, 'bold'), fill=(15, 23, 42))
            draw.text((cx + 26, iy + 48), "Native Flutter + SQLite Sync", font=get_font(10.5, 'regular'), fill=(100, 116, 139))
            iy += 100

    draw_slide_footer(draw, 4)
    save_slide(base.convert('RGB'), 4)

print("Slides 01-04 defined successfully in clean white style!")
