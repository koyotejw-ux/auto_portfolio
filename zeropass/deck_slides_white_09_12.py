import os
from PIL import Image, ImageDraw, ImageFilter
from build_zeropass_white_common import (
    W, H, MOCKUP_DIR, get_font, get_num_font, wrap_text_by_words,
    draw_pill_badge, draw_slide_header, draw_slide_footer, save_slide,
    draw_arrow
)

def make_shadow(img, blur=44, offset=(22, 40), alpha=80):
    mask = img.split()[3]
    sh_img = Image.new('RGBA', (img.width + 120, img.height + 120), (0, 0, 0, 0))
    black = Image.new('RGBA', img.size, (15, 23, 42, alpha))
    sh_img.paste(black, (60 + offset[0], 60 + offset[1]), mask)
    return sh_img.filter(ImageFilter.GaussianBlur(blur)), (60, 60)

# ==============================================================
# SLIDE 09: CORE FEATURE DEEP DIVE 02 - D-DAY BILLING LEDGER
# ==============================================================
def make_slide_09():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    lx = 100
    lw = 540
    
    draw_pill_badge(draw, left_x=lx, cy=78, text="09 CORE FEATURE | SMART D-DAY BILLING LEDGER", font=get_font(10.5, 'bold'), theme='blue', has_dot=True, pad_x=10, height=26)
    
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
    
    desc_text = "월말에 몰아서 수기 확인하던 복잡한 장부를 3단계 실시간 D-Day 컬러 코딩으로 완전 자동화했어요. 만료 7일 전 사전 알림부터 연체 미수금 원클릭 카카오톡 청구서 발송까지 무결하게 지원합니다."
    desc_lines = wrap_text_by_words(desc_text, get_font(12, 'regular'), lw, draw)
    dy = 212
    for dl in desc_lines:
        draw.text((lx, dy), dl, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 19
        
    # Card 1: 3-Stage D-Day Architecture
    card_y = 310
    card_h = 660
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=card_y + 30, text="D-DAY AUDITING ENGINE", font=get_font(10, 'bold'), theme='blue', has_dot=True, pad_x=10, height=24)
    draw.text((lx + 225, card_y + 20), "3단계 실시간 수납 위험도 정렬 체계", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.line([(lx + 24, card_y + 50), (lx + lw - 24, card_y + 50)], fill=(241, 245, 249), width=1)
    
    stages = [
        ("STAGE 1: D-7 만료 임박 알림 (Amber)", "수강 만료 7일 전부터 주황색 뱃지로 전환되어 원장님이 사전 재등록 의사를 확인하고 미수금을 사전에 예방합니다.", (217, 119, 6), (254, 243, 199)),
        ("STAGE 2: D-Day 당일 수납 대상 (Blue)", "오늘이 회비 납부일인 회원은 파란색 뱃지와 함께 최상단 정렬되어 등원 즉시 원클릭 수납 처리를 유도합니다.", (0, 82, 255), (239, 246, 255)),
        ("STAGE 3: Overdue 미수금 연체 관리 (Red)", "납부일이 경과한 미납 회원은 빨간색 뱃지와 경과 일수가 카운트되며, 터치 1번으로 카카오톡 청구서 발송이 활성화됩니다.", (220, 38, 38), (254, 242, 242))
    ]
    
    sy = card_y + 64
    for stit, sdesc, scol, sbg in stages:
        draw.rounded_rectangle([lx + 24, sy, lx + lw - 24, sy + 128], radius=12, fill=sbg, outline=scol, width=1)
        draw.text((lx + 40, sy + 16), stit, font=get_font(13.5, 'bold'), fill=scol)
        lines = wrap_text_by_words(sdesc, get_font(12, 'regular'), lw - 80, draw)
        ly = sy + 44
        for l in lines:
            draw.text((lx + 40, ly), l, font=get_font(12, 'regular'), fill=(51, 65, 85))
            ly += 21
        sy += 140
        
    # Bottom Inversion Stat Box inside Left Card
    draw.rounded_rectangle([lx + 24, card_y + card_h - 190, lx + lw - 24, card_y + card_h - 24], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=lx + 40, cy=card_y + card_h - 162, text="1-TAP BILLING", font=get_font(9, 'bold'), theme='blue', pad_x=8, height=20)
    draw.text((lx + 150, card_y + card_h - 172), "원클릭 모바일 청구서 즉시 전송", font=get_font(14, 'bold'), fill=(0, 82, 255))
    b_desc = "원생명, 수강과목, 청구금액, 입금 계좌번호가 정중한 서식에 자동 치환되어 카카오톡/문자로 1초 만에 전송됩니다."
    b_lines = wrap_text_by_words(b_desc, get_font(11.5, 'regular'), lw - 80, draw)
    by = card_y + card_h - 138
    for bl in b_lines:
        draw.text((lx + 40, by), bl, font=get_font(11.5, 'regular'), fill=(71, 85, 105))
        by += 19

    # Center Phone Mockup (Mockup 02 Ledger)
    m2 = Image.open(f"{MOCKUP_DIR}/mockup_02_ledger.png").convert('RGBA')
    scale_h = 640
    pw = int(round(scale_h * (m2.width / m2.height)))
    phone_l = m2.resize((pw, scale_h), Image.Resampling.LANCZOS)
    px = 715
    py = 234
    
    sh_center = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    shc_draw = ImageDraw.Draw(sh_center)
    shc_draw.rounded_rectangle([px + 12, py + 16, px + pw - 12, py + scale_h + 24], radius=36, fill=(0, 0, 0, 60))
    shc_draw.ellipse([px - 20, py + scale_h - 25, px + pw + 20, py + scale_h + 35], fill=(0, 82, 255, 30))
    sh_center = sh_center.filter(ImageFilter.GaussianBlur(26))
    base = Image.alpha_composite(base, sh_center)
    base.paste(phone_l, (px, py), phone_l)
    draw = ImageDraw.Draw(base)

    # Right Column: 2-Step Verified Flow Card + Telemetry Report (x=1100, w=720)
    rx = 1100
    rw = 720
    
    step_y = 234
    step_h = 475
    draw.rounded_rectangle([rx, step_y, rx + rw, step_y + step_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=step_y + 30, text="VERIFIED WORKFLOW", font=get_font(10, 'bold'), theme='blue', has_dot=True, pad_x=10, height=24)
    draw.text((rx + 220, step_y + 20), "2단계 D-Day 수납 확인 & 카카오톡 청구 워크플로우", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, step_y + 52), (rx + rw - 28, step_y + 52)], fill=(241, 245, 249), width=1)
    
    m_pass = Image.open(f"{MOCKUP_DIR}/mockup_02_ledger.png").convert('RGBA')
    m_member = Image.open(f"{MOCKUP_DIR}/mockup_03_members.png").convert('RGBA')
    
    step_pw = 142
    step_ph = int(round(step_pw * (m_pass.height / m_pass.width)))
    sm1 = m_pass.resize((step_pw, step_ph), Image.Resampling.LANCZOS)
    sm2 = m_member.resize((step_pw, step_ph), Image.Resampling.LANCZOS)
    
    p_w = 326
    p_h = 400
    p_y = step_y + 60
    p1_x = rx + 24
    p2_x = rx + rw - 24 - p_w
    
    # LEFT POD: STEP 01
    draw.rounded_rectangle([p1_x, p_y, p1_x + p_w, p_y + p_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p1_x + 14, cy=p_y + 20, text="STEP 01", font=get_font(9, 'bold'), theme='slate', pad_x=8, height=20)
    draw.text((p1_x + 82, p_y + 20), "D-Day 장부 실시간 정렬", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(p1_x + 14, p_y + 36), (p1_x + p_w - 14, p_y + 36)], fill=(226, 232, 240), width=1)
    
    phone1_x = p1_x + 14
    phone1_y = p_y + 48
    base.paste(sm1, (phone1_x, phone1_y), sm1)
    
    d1_x = phone1_x + step_pw + 12
    d1_w = p1_x + p_w - 14 - d1_x
    
    t1_y = p_y + 48
    t_h = 76
    draw.rounded_rectangle([d1_x, t1_y, d1_x + d1_w, t1_y + t_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d1_x + 10, t1_y + 8), "D+ 연체 회원", font=get_font(9.5, 'bold'), fill=(220, 38, 38))
    draw.text((d1_x + 10, t1_y + 28), "3명 연체", font=get_font(14, 'bold'), fill=(220, 38, 38))
    draw.text((d1_x + 10, t1_y + 54), "미수금 ₩480,000", font=get_font(8.5, 'medium'), fill=(148, 163, 184))
    
    t2_y = t1_y + t_h + 10
    draw.rounded_rectangle([d1_x, t2_y, d1_x + d1_w, t2_y + t_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d1_x + 10, t2_y + 8), "D-7 만료 임박", font=get_font(9.5, 'bold'), fill=(180, 83, 9))
    draw.text((d1_x + 10, t2_y + 28), "4명 대기", font=get_font(14, 'bold'), fill=(180, 83, 9))
    draw.text((d1_x + 10, t2_y + 54), "재등록 사전 안내", font=get_font(8.5, 'medium'), fill=(148, 163, 184))
    
    t3_y = t2_y + t_h + 10
    draw.rounded_rectangle([d1_x, t3_y, d1_x + d1_w, t3_y + t_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d1_x + 10, t3_y + 8), "정상 납부 원생", font=get_font(9.5, 'bold'), fill=(0, 82, 255))
    draw.text((d1_x + 10, t3_y + 28), "28명 완료", font=get_font(14, 'bold'), fill=(0, 82, 255))
    draw.text((d1_x + 10, t3_y + 54), "회수율 92.4%", font=get_font(8.5, 'medium'), fill=(16, 185, 129))
    
    # RIGHT POD: STEP 02
    draw.rounded_rectangle([p2_x, p_y, p2_x + p_w, p_y + p_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p2_x + 14, cy=p_y + 20, text="STEP 02", font=get_font(9, 'bold'), theme='blue', pad_x=8, height=20)
    draw.text((p2_x + 82, p_y + 20), "원클릭 청구서 & 원부 관리", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(p2_x + 14, p_y + 36), (p2_x + p_w - 14, p_y + 36)], fill=(226, 232, 240), width=1)
    
    phone2_x = p2_x + 14
    phone2_y = p_y + 48
    base.paste(sm2, (phone2_x, phone2_y), sm2)
    
    d2_x = phone2_x + step_pw + 12
    d2_w = p2_x + p_w - 14 - d2_x
    
    r1_y = p_y + 48
    draw.rounded_rectangle([d2_x, r1_y, d2_x + d2_w, r1_y + t_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d2_x + 10, r1_y + 8), "카카오 알림톡", font=get_font(9.5, 'bold'), fill=(15, 23, 42))
    draw.text((d2_x + 10, r1_y + 28), "1초 발송", font=get_font(14, 'bold'), fill=(0, 82, 255))
    draw.text((d2_x + 10, r1_y + 54), "계좌번호 자동 치환", font=get_font(8.5, 'medium'), fill=(148, 163, 184))
    
    r2_y = r1_y + t_h + 10
    draw.rounded_rectangle([d2_x, r2_y, d2_x + d2_w, r2_y + t_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d2_x + 10, r2_y + 8), "원생 출결 원부", font=get_font(9.5, 'bold'), fill=(15, 23, 42))
    draw.text((d2_x + 10, r2_y + 28), "1-Tap 조회", font=get_font(14, 'bold'), fill=(5, 150, 105))
    draw.text((d2_x + 10, r2_y + 54), "잔여 횟수 및 이력", font=get_font(8.5, 'medium'), fill=(148, 163, 184))
    
    r3_y = r2_y + t_h + 10
    draw.rounded_rectangle([d2_x, r3_y, d2_x + d2_w, r3_y + t_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d2_x + 10, r3_y + 8), "스튜디오 볼트", font=get_font(9.5, 'bold'), fill=(15, 23, 42))
    draw.text((d2_x + 10, r3_y + 28), "100% 로컬", font=get_font(14, 'bold'), fill=(122, 34, 255))
    draw.text((d2_x + 10, r3_y + 54), "SQLite ACID 암호화", font=get_font(8.5, 'medium'), fill=(148, 163, 184))
    
    # 3-B. Financial Telemetry & Recovery Report Card
    rep_y = step_y + step_h + 16
    rep_h = 245
    draw.rounded_rectangle([rx, rep_y, rx + rw, rep_y + rep_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=rep_y + 28, text="FINANCIAL AUDIT", font=get_font(10, 'bold'), theme='green', has_dot=True, pad_x=10, height=24)
    draw.text((rx + 185, rep_y + 18), "실시간 수납 회수율 및 경영 텔레메트리 리포트", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, rep_y + 48), (rx + rw - 28, rep_y + 48)], fill=(241, 245, 249), width=1)
    
    sol_y = rep_y + 58
    draw.rounded_rectangle([rx + 28, sol_y, rx + rw - 28, sol_y + 68], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=rx + 48, cy=sol_y + 22, text="VERIFIED 92.4% RECOVERY", font=get_font(9.5, 'bold'), theme='green', has_dot=True, pad_x=8, height=22)
    draw.text((rx + 295, sol_y + 12), "D-Day 사전 알림 도입 후 미수금 회수 소요 14일 ➔ 2일 단축", font=get_font(14.5, 'bold'), fill=(0, 82, 255))
    draw.text((rx + 48, sol_y + 44), "100% 온디바이스 SQLite 트랜잭션 연동으로 수납 누수 및 장부 오차율 0.00% 달성", font=get_font(10.5, 'regular'), fill=(71, 85, 105))
    
    rep_chips = [
        ("월 총 예상 매출", "₩ 6,800,000", (100, 116, 139)),
        ("정상 수납 완료", "₩ 6,320,000", (0, 82, 255)),
        ("미수금 연체 잔액", "₩ 480,000", (220, 38, 38)),
        ("미수금 회수율", "92.4%", (16, 185, 129))
    ]
    rc_y = sol_y + 78
    rc_w = (rw - 56 - 36) // 4
    for idx, (label, val, c_col) in enumerate(rep_chips):
        rc_x = rx + 28 + idx * (rc_w + 12)
        draw.rounded_rectangle([rc_x, rc_y, rc_x + rc_w, rc_y + 64], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((rc_x + 14, rc_y + 12), label, font=get_font(9.5, 'bold'), fill=(100, 116, 139))
        draw.text((rc_x + 14, rc_y + 34), val, font=get_num_font(14, 'bold'), fill=c_col)

    draw_slide_footer(draw, 9)
    save_slide(base.convert('RGB'), 9)

# ==============================================================
# SLIDE 10: MOBILE SCREENS SHOWCASE
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
# SLIDE 12: LIVE INTERACTIVE PROTOTYPE
# ==============================================================
def make_slide_12():
    base = Image.new('RGBA', (W, H), (11, 15, 23, 255))
    draw = ImageDraw.Draw(base)
    
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

    rx = 780
    rw = 1040
    
    steps = [
        ("1", "출결 키오스크 번호 입력", "0.8초 번호 매칭", "다이얼 패드에서 전화번호 뒤 4자리를 터치하면 즉각 해당 원생을 특정하고 등원/하원 분기가 팝업됩니다."),
        ("2", "원터치 등·하원 차감", "실시간 잔여 횟수 갱신", "[등원] 버튼을 누르면 잔여 수업 일수(-1)가 즉시 차감되며 우측 출결 타임라인에 실시간 로그가 기록됩니다."),
        ("3", "D-Day 수납 장부 필터링", "3단계 위험도 분류", "만료 임박(주황), 당일(파랑), 연체(빨강) 탭을 전환하며 실시간 필터링 동작을 직접 테스트할 수 있습니다."),
        ("4", "원클릭 카카오톡 청구서", "정중한 서식 자동 치환", "수납 지연 원생 카드를 터치하여 회원명, 수강과목, 금액, 계좌번호가 자동 생성된 청구서를 확인합니다.")
    ]
    
    sy = 220
    for num_str, title, tag, desc in steps:
        draw.rounded_rectangle([rx, sy, rx + rw, sy + 76], radius=12, fill=(18, 24, 38, 255), outline=(30, 41, 59, 255), width=1)
        draw.rounded_rectangle([rx + 16, sy + 18, rx + 52, sy + 58], radius=8, fill=(0, 82, 255, 40), outline=(0, 82, 255, 120), width=1)
        draw.text((rx + 34, sy + 38), num_str, font=get_num_font(16, 'bold'), fill=(56, 189, 248), anchor='mm')
        
        draw.text((rx + 68, sy + 18), title, font=get_font(14, 'bold'), fill=(255, 255, 255))
        draw_pill_badge(draw, left_x=rx + rw - 170, cy=sy + 26, text=tag, font=get_font(9, 'bold'), theme='cyan', dark_mode=True, pad_x=8, height=20)
        draw.text((rx + 68, sy + 44), desc, font=get_font(11.5, 'regular'), fill=(148, 163, 184))
        sy += 90

    # Master Action Launcher Card
    launch_y = sy + 10
    launch_h = 190
    draw.rounded_rectangle([rx, launch_y, rx + rw, launch_y + launch_h], radius=16, fill=(15, 23, 42, 255), outline=(0, 82, 255, 120), width=1)
    
    draw_pill_badge(draw, left_x=rx + 28, cy=launch_y + 30, text="INTERACTIVE HUB READY", font=get_font(10, 'bold'), theme='green', dark_mode=True, has_dot=True, pad_x=10, height=24)
    draw.text((rx + 235, launch_y + 20), "실제 뷰포트에서 체크앤페이를 직접 체험해보세요.", font=get_font(16, 'bold'), fill=(255, 255, 255))
    draw.text((rx + 28, launch_y + 54), "웹 브라우저에서 실제 모바일 화면을 직접 터치하고 인터랙션을 경험할 수 있습니다.", font=get_font(12, 'regular'), fill=(148, 163, 184))
    
    # 4 Quick Mode Switch Pills
    modes = [
        ("01 키오스크 모드", "0.8s 번호 입력"),
        ("02 D-Day 장부", "3단계 위험도 정렬"),
        ("03 원생 디렉터리", "출결 타임라인"),
        ("04 카톡 청구서", "정중한 서식 공유")
    ]
    mw = (rw - 56 - 36) // 4
    my = launch_y + 88
    for idx, (m_tit, m_sub) in enumerate(modes):
        mx = rx + 28 + idx * (mw + 12)
        draw.rounded_rectangle([mx, my, mx + mw, my + 54], radius=10, fill=(24, 32, 54, 255), outline=(40, 53, 80, 255), width=1)
        draw.text((mx + 14, my + 12), m_tit, font=get_font(11, 'bold'), fill=(255, 255, 255))
        draw.text((mx + 14, my + 32), m_sub, font=get_font(9.5, 'regular'), fill=(100, 116, 139))
        
    draw.text((rx + 28, launch_y + launch_h - 24), "• 브라우저에서 index.html 또는 prototype.html을 실행하여 60fps 인터랙티브 엔진을 경험하세요.", font=get_font(10, 'regular'), fill=(100, 116, 139))

    draw_slide_footer(draw, 12, dark_mode=True)
    save_slide(base.convert('RGB'), 12)
    print("SAVED perfect Slide 09, 10, 11, 12 successfully!")
