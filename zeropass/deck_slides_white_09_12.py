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
    
    draw_pill_badge(draw, left_x=lx, cy=78, text="09 핵심 기능 | 스마트 D-Day 수납 장부", font=get_font(10.5, 'bold'), theme='blue', has_dot=False, pad_x=10, height=26)
    
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
    draw_pill_badge(draw, left_x=lx + 24, cy=card_y + 30, text="수납 검증 엔진", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=10, height=24)
    draw.text((lx + 150, card_y + 20), "3단계 실시간 수납 위험도 정렬 체계", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.line([(lx + 24, card_y + 50), (lx + lw - 24, card_y + 50)], fill=(241, 245, 249), width=1)
    
    stages = [
        ("1단계: D-7 만료 임박 알림 (주황)", "수강 만료 7일 전부터 주황색 뱃지로 전환되어 원장님이 사전 재등록 의사를 확인하고 미수금을 사전에 예방합니다.", (217, 119, 6), (254, 243, 199)),
        ("2단계: D-Day 당일 수납 대상 (파랑)", "오늘이 회비 납부일인 회원은 파란색 뱃지와 함께 최상단 정렬되어 등원 즉시 원클릭 수납 처리를 유도합니다.", (0, 82, 255), (239, 246, 255)),
        ("3단계: 연체 미수금 집중 관리 (빨강)", "납부일이 경과한 미납 회원은 빨간색 뱃지와 경과 일수가 카운트되며, 터치 1번으로 카카오톡 청구서 발송이 활성화됩니다.", (220, 38, 38), (254, 242, 242))
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
    draw_pill_badge(draw, left_x=lx + 40, cy=card_y + card_h - 162, text="원클릭 청구", font=get_font(9, 'bold'), theme='blue', pad_x=8, height=20)
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
    draw_pill_badge(draw, left_x=rx + 28, cy=step_y + 30, text="수납 검증 워크플로우", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=10, height=24)
    draw.text((rx + 180, step_y + 20), "2단계 D-Day 수납 확인 & 카카오톡 청구 워크플로우", font=get_font(16, 'bold'), fill=(15, 23, 42))
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
    
    # TOP POD 01: STEP 01
    draw.rounded_rectangle([p1_x, p_y, p1_x + p_w, p_y + p_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p1_x + 14, cy=p_y + 20, text="1단계", font=get_font(9, 'bold'), theme='slate', pad_x=8, height=20)
    draw.text((p1_x + 70, p_y + 20), "D-Day 장부 실시간 정렬", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # Passy mini badge
    p_cry = 'd:/097.flutter_project/auto_portfolio/zeropass/assets/mascot/mascot_profile_crying_round.png'
    if os.path.exists(p_cry):
        im_cry = Image.open(p_cry).convert('RGBA').resize((24, 24), Image.Resampling.LANCZOS)
        base.paste(im_cry, (p1_x + p_w - 38, p_y + 8), im_cry)
        draw = ImageDraw.Draw(base)

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
    draw_pill_badge(draw, left_x=p2_x + 14, cy=p_y + 20, text="2단계", font=get_font(9, 'bold'), theme='blue', pad_x=8, height=20)
    draw.text((p2_x + 70, p_y + 20), "원클릭 청구서 & 원부 관리", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')

    p_laugh = 'd:/097.flutter_project/auto_portfolio/zeropass/assets/mascot/mascot_profile_laughing_round.png'
    if os.path.exists(p_laugh):
        im_lgh = Image.open(p_laugh).convert('RGBA').resize((24, 24), Image.Resampling.LANCZOS)
        base.paste(im_lgh, (p2_x + p_w - 38, p_y + 8), im_lgh)
        draw = ImageDraw.Draw(base)

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
    draw.text((d2_x + 10, r3_y + 54), "오프라인 안심 암호화", font=get_font(8.5, 'medium'), fill=(148, 163, 184))
    
    # 3-B. Financial Telemetry & Recovery Report Card
    rep_y = step_y + step_h + 16
    rep_h = 245
    draw.rounded_rectangle([rx, rep_y, rx + rw, rep_y + rep_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=rep_y + 28, text="수납 성과 분석", font=get_font(10, 'bold'), theme='green', has_dot=False, pad_x=10, height=24)
    draw.text((rx + 160, rep_y + 18), "실시간 수납 회수율 및 경영 텔레메트리 리포트", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, rep_y + 48), (rx + rw - 28, rep_y + 48)], fill=(241, 245, 249), width=1)
    
    sol_y = rep_y + 58
    draw.rounded_rectangle([rx + 28, sol_y, rx + rw - 28, sol_y + 68], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=rx + 48, cy=sol_y + 22, text="회수율 92.4% 입증", font=get_font(9.5, 'bold'), theme='green', has_dot=False, pad_x=8, height=22)
    draw.text((rx + 295, sol_y + 12), "D-Day 사전 알림 도입 후 미수금 회수 소요 14일 ➔ 2일 단축", font=get_font(14.5, 'bold'), fill=(0, 82, 255))
    draw.text((rx + 48, sol_y + 44), "100% 로컬 안심 저장 연동으로 수납 누수 및 장부 오차율 0.00% 달성", font=get_font(10.5, 'regular'), fill=(71, 85, 105))
    
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
# SLIDE 10: MOBILE SCREENS SHOWCASE (6 Modern Flagship Screens + User Journey Bar)
# ==============================================================
def make_slide_10():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=10,
        category_en="모바일 상용 화면 · 피그마 및 플러터",
        title_black="출결 키오스크부터 수납 장부까지, ",
        title_blue="일관된 6대 핵심 상용 화면이에요.",
        subtitle_kr="원생과 원장님의 핵심 여정(User Journey)을 빈틈없이 지원하도록 피그마 토큰과 플러터 위젯 트리로 구현한 6대 상용 화면입니다."
    )
    
    screens = [
        ('mockup_01_pass.png', '01. 출결 키오스크', '4자리 번호 즉시 검색', '& 0.8초 등하원 인증'),
        ('mockup_02_ledger.png', '02. 수납 장부', 'D-Day 미수금 자동 정렬', '& 원클릭 청구서 전송'),
        ('mockup_03_members.png', '03. 원생 디렉터리', '수강권 및 이력 관리', '& 결제자(학부모) 연동'),
        ('mockup_04_pro.png', '04. 프로 멤버십', '평생 소장 라이선스', '& 무제한 원생 등록 해제'),
        ('mockup_05_vault.png', '05. 스튜디오 볼트', '로컬 안심 백업', '& 오프라인 암호화 보관'),
        ('mockup_06_en.png', '06. 글로벌 다국어', '글로벌 6개 언어 지원', '& 화폐 단위 자동 변환')
    ]
    
    # 6 Modern Flagship 19.5:9 Mobile Screens Grid
    pw = 210
    phone_y = 230
    pgap = 80
    px = 130
    
    for m_file, title, line1, line2 in screens:
        m_path = f"{MOCKUP_DIR}/{m_file}"
        if not os.path.exists(m_path):
            m_path = f"{MOCKUP_DIR}/mockup_01_pass.png"
            
        phone = Image.open(m_path).convert('RGBA')
        cur_ph = int(round(pw * (phone.height / phone.width)))
        phone = phone.resize((pw, cur_ph), Image.Resampling.LANCZOS)
        
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([px + 8, phone_y + 12, px + pw - 8, phone_y + cur_ph + 18], radius=28, fill=(0, 0, 0, 55))
        sh = sh.filter(ImageFilter.GaussianBlur(16))
        base = Image.alpha_composite(base, sh)
        base.paste(phone, (px, phone_y), phone)
        
        draw = ImageDraw.Draw(base)
        
        pill_y = phone_y + cur_ph + 16
        draw_pill_badge(draw, cx=px + pw // 2, cy=pill_y + 14, text=title, font=get_font(11, 'bold'), pad_x=12, height=26)
        
        w_l1 = draw.textlength(line1, font=get_font(10.5, 'medium'))
        draw.text((px + (pw - w_l1) / 2, pill_y + 44), line1, font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        w_l2 = draw.textlength(line2, font=get_font(10.5, 'medium'))
        draw.text((px + (pw - w_l2) / 2, pill_y + 62), line2, font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        
        px += pw + pgap
        
    # Bottom Horizontal User Journey Flow Ribbon (Spanning x=100 to 1820)
    draw.rounded_rectangle([100, 915, 1820, 975], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=124, cy=945, text="사용자 여정", font=get_font(11, 'bold'), theme='blue', has_dot=False, pad_x=12, height=26)
    
    flow_steps = [
        ("01 번호 터치 등원", 310),
        ("02 D-Day 장부 점검", 570),
        ("03 수강 이력 관리", 840),
        ("04 원클릭 카톡 청구", 1110),
        ("05 오프라인 안심 백업", 1380),
        ("06 글로벌 환경 확장", 1640)
    ]
    for step_txt, sx in flow_steps:
        draw.text((sx, 945), step_txt, font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        if sx < 1600:
            draw.text((sx + 190, 945), "→", font=get_font(18, 'bold'), fill=(0, 82, 255), anchor='lm')

    draw_slide_footer(draw, 10)
    save_slide(base.convert('RGB'), 10)

# ==============================================================
# SLIDE 11: BUSINESS IMPACT & STRATEGIC RETROSPECTIVE (3-Tier Senior Layout)
# ==============================================================
def make_slide_11():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=11,
        category_en="성과 지표 · 기획 디자인 회고",
        title_black="출결 소요 시간 0.8초와 미수금 92% 회수, ",
        title_blue="실제 학원 파일럿으로 검증된 프로덕트 가치예요.",
        subtitle_kr="현장 검증 기반 4대 정량 지표와 STAR 기법으로 서술한 시니어 프로덕트 기획·디자인 회고입니다.",
        right_badge=("현장 검증 100%", "green")
    )
    
    # ---------------------------------------------------------
    # 1. TOP DUAL COMPARISON CARDS: BEFORE vs. AFTER (y=226 to 526, h=300)
    # ---------------------------------------------------------
    card_y = 226
    card_h = 300
    card_w = 840
    
    # Left: Traditional Manual & Heavy SaaS (Before)
    cx1 = 100
    draw.rounded_rectangle([cx1, card_y, cx1 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(254, 202, 202), width=1)
    draw.rounded_rectangle([cx1, card_y + 14, cx1 + 5, card_y + card_h - 14], radius=3, fill=(239, 68, 68))
    draw_pill_badge(draw, left_x=cx1 + 24, cy=card_y + 24, text="도입 전 : 기존 아날로그 수기 및 고비용 ERP", font=get_font(9.5, 'bold'), theme='red', pad_x=10, height=22)
    draw.text((cx1 + 24, card_y + 50), "수기 출석부와 독촉 스트레스, 고정 구독료 부담", font=get_font(17, 'bold'), fill=(15, 23, 42))
    draw.text((cx1 + 24, card_y + 74), "제각각 다른 수납일과 비효율적 손글씨 출결로 인한 운영 병목", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    b_rows = [
        ("출결 관리 소요 시간", "원생 1인당 45초 소요 (수업 시작 전 15~20분 대기 병목)", (220, 38, 38)),
        ("월평균 미수금 연체율", "18.4% 누수 발생 (제각각 다른 결제일 추적 불가)", (220, 38, 38)),
        ("학부모 대면 수납 마찰", "원장 직접 독촉 통화 (감정 소모 극심 및 재등록 이탈)", (180, 83, 9)),
        ("고정 소프트웨어 비용", "월 5~15만 원 고정 SaaS 구독료 지출 (소규모 적자 요인)", (15, 23, 42))
    ]
    ry = card_y + 98
    for label, val, val_col in b_rows:
        draw.rounded_rectangle([cx1 + 24, ry, cx1 + card_w - 24, ry + 42], radius=8, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
        draw.text((cx1 + 38, ry + 21), label, font=get_font(11.5, 'bold'), fill=(100, 116, 139), anchor='lm')
        draw.text((cx1 + 210, ry + 21), val, font=get_font(12, 'bold'), fill=val_col, anchor='lm')
        ry += 48

    # Right: ZeroPass Automated Workflow (After)
    cx2 = 980
    draw.rounded_rectangle([cx2, card_y, cx2 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.rounded_rectangle([cx2, card_y + 14, cx2 + 5, card_y + card_h - 14], radius=3, fill=(0, 82, 255))
    draw_pill_badge(draw, left_x=cx2 + 24, cy=card_y + 24, text="도입 후 : 체크앤페이 원터치 자동화", font=get_font(9.5, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((cx2 + 24, card_y + 50), "1초 원터치 인증과 D-Day 수납 장부 자동화", font=get_font(17, 'bold'), fill=(15, 23, 42))
    draw.text((cx2 + 24, card_y + 74), "자연스러운 출결 및 정중한 카카오톡 청구서로 감정 마찰 제로화", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    a_rows = [
        ("키오스크 출결 속도", "0.8초 즉시 인증 완결 (소요 시간 98.2% 대폭 단축)", (0, 82, 255)),
        ("D-Day 수납 적기 회수율", "92.4% 적기 회수 달성 (회수 소요 기간 14일 ➔ 2일)", (5, 150, 105)),
        ("모바일 청구서 발송", "1-Tap 카카오톡 서식 즉시 전송 (대면 마찰 제로)", (5, 150, 105)),
        ("월 고정 유지비용", "월 0원 평생 소장 라이선스 (서버비 0원 온디바이스)", (180, 83, 9))
    ]
    ry = card_y + 98
    for label, val, val_col in a_rows:
        draw.rounded_rectangle([cx2 + 24, ry, cx2 + card_w - 24, ry + 42], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((cx2 + 38, ry + 21), label, font=get_font(11.5, 'bold'), fill=(100, 116, 139), anchor='lm')
        draw.text((cx2 + 210, ry + 21), val, font=get_font(12, 'bold'), fill=val_col, anchor='lm')
        ry += 48
        
    # ---------------------------------------------------------
    # 2. MIDDLE 4 TELEMETRY METRICS CARDS (y=544 to 684, h=140)
    # ---------------------------------------------------------
    m_y = 544
    m_h = 140
    m_w = 405
    m_gap = 33
    tx = 100
    
    telemetry_data = [
        ("0.8초", "출결 속도 혁신", "출결 소요 98.2% 단축", "4자리 번호 터치 즉시 등하원 및 잔여 세션 자동 차감", (0, 82, 255), "blue"),
        ("92.4%", "미수금 회수율", "미수금 적기 회수율", "D-Day 3단계 컬러 정렬로 연체 발생 사전 예방 완결", (16, 185, 129), "green"),
        ("0원", "서버 유지비 제로", "월 고정 유지비 0원", "외부 유료 서버 없이 온디바이스 안전 보관으로 평생 소장", (2, 132, 199), "cyan"),
        ("100%", "오프라인 가동률", "인터넷 장애 무중단 가동", "통신 장애 발생 시에도 키오스크 출결 100% 정상 작동", (245, 158, 11), "amber")
    ]
    
    for val, badge, title, desc, col, theme_key in telemetry_data:
        draw.rounded_rectangle([tx, m_y, tx + m_w, m_y + m_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=tx + 18, cy=m_y + 20, text=badge, font=get_font(9, 'bold'), theme=theme_key, has_dot=False, pad_x=8, height=20)
        draw.text((tx + 18, m_y + 44), val, font=get_num_font(30, 'black'), fill=(15, 23, 42))
        draw.text((tx + 18, m_y + 84), title, font=get_font(13, 'bold'), fill=(15, 23, 42))
        draw.text((tx + 18, m_y + 108), desc, font=get_font(10.5, 'regular'), fill=(100, 116, 139))
        tx += m_w + m_gap
        
    # ---------------------------------------------------------
    # 3. BOTTOM 3 STRATEGIC RETROSPECTIVE & ROADMAP CARDS (y=702 to 970, h=268)
    # ---------------------------------------------------------
    b_y = 702
    b_h = 268
    b_w = 548
    b_gap = 38
    bx = 100
    
    bottom_cards = [
        (
            "기획 회고 01",
            "현장 마찰 제로화의 설계 (STAR)",
            "소상공인 도메인 복잡성을 0.8초 키오스크로 정제",
            "원생 출결은 단순 확인이 아니라 수업 전 분위기를 좌우하는 의식입니다. 번호 4자리와 대형 80dp 터치 다이얼 패드로 전환하여, 60명 정원 파일럿 현장에서 출결 시간을 45초에서 0.8초로 98.2% 단축하고 대기 줄을 완전히 없앴습니다.",
            "✓ 수업 준비 효율 92% 개선 입증",
            "blue", (0, 82, 255)
        ),
        (
            "기획 회고 02",
            "심리적 감정 마찰의 해소 (STAR)",
            "대면 독촉 대신 우아한 D-Day 자동 장부 연동",
            "원장님의 가장 큰 감정 고통인 '회비 독촉'을 해결하고자 만료 7일 전부터 3단계 컬러 뱃지 시스템을 적용했습니다. 터치 1번으로 카카오톡 청구서 서식이 자동 완성되도록 설계하여 미수금 회수 소요 기간을 14일에서 2일로 단축했습니다.",
            "✓ 미수금 회수율 92.4% 달성",
            "green", (5, 150, 105)
        ),
        (
            "성장 로드맵",
            "지속 가능한 엔터프라이즈 진화",
            "스토어 출시 완료 및 로컬 생태계 확장 계획",
            "• 1단계 (완료) : 1초 키오스크 & D-Day 장부 구글 플레이 상용 출시 완료\n• 2단계 (예정) : 학부모 전용 웹 출결 알림 & 안심 등원 푸시 서비스 연동\n• 3단계 (확장) : 블루투스 영수증 프린터 및 다점포 로컬 동기화 지원",
            "스토어 상용 인증 통과 ✓",
            "cyan", (8, 145, 178)
        )
    ]
    
    for badge, title, sub, body_txt, check_txt, theme_key, col in bottom_cards:
        draw.rounded_rectangle([bx, b_y, bx + b_w, b_y + b_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=bx + 20, cy=b_y + 22, text=badge, font=get_font(9, 'bold'), theme=theme_key, has_dot=False, pad_x=8, height=20)
        draw.text((bx + 20, b_y + 50), title, font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((bx + 20, b_y + 72), sub, font=get_font(11, 'bold'), fill=col)
        draw.line([(bx + 20, b_y + 92), (bx + b_w - 20, b_y + 92)], fill=(241, 245, 249), width=1)
        
        py = b_y + 102
        for line in body_txt.split('\n'):
            words = line.split(' ')
            cur_line = ""
            for w in words:
                test_line = (cur_line + " " + w).strip()
                bbox = draw.textbbox((0, 0), test_line, font=get_font(10.5, 'regular'))
                if bbox[2] - bbox[0] <= b_w - 40:
                    cur_line = test_line
                else:
                    draw.text((bx + 20, py), cur_line, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
                    py += 18
                    cur_line = w
            if cur_line:
                draw.text((bx + 20, py), cur_line, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
                py += 18
                
        draw.rounded_rectangle([bx + 16, b_y + b_h - 36, bx + b_w - 16, b_y + b_h - 12], radius=6, fill=(240, 246, 255) if theme_key=='blue' else (248, 250, 252), outline=(191, 219, 254) if theme_key=='blue' else (226, 232, 240), width=1)
        draw.text((bx + 24, b_y + b_h - 24), check_txt, font=get_font(10, 'bold'), fill=col, anchor='lm')
        bx += b_w + b_gap

    draw_slide_footer(draw, 11)
    save_slide(base.convert('RGB'), 11)

# ==============================================================
# SLIDE 12: LIVE INTERACTIVE PROTOTYPE (Grand Finale Unified Layout)
# ==============================================================
def make_slide_12():
    import numpy as np
    import qrcode

    base = Image.new('RGBA', (W, H), (11, 15, 23, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=12,
        category_en="인터랙티브 프로토타입 · 플러터 웹",
        title_black="화면을 터치하듯, ",
        title_blue="실제 플러터 웹 프로토타입을 직접 조작해 보세요.",
        subtitle_kr="정적인 슬라이드를 넘어 스마트폰 뷰포트에서 4대 핵심 출결·수납 여정을 직접 터치하고 검증할 수 있는 인터랙티브 허브입니다.",
        right_badge=("체험 준비 완료", "green"),
        dark_mode=True
    )
    
    # Left Dual 3D Layered Mockup Showcase
    phone_pass_path = f"{MOCKUP_DIR}/mockup_01_pass.png"
    phone_ledger_path = f"{MOCKUP_DIR}/mockup_02_ledger.png"
    
    if os.path.exists(phone_pass_path) and os.path.exists(phone_ledger_path):
        im_ledger = Image.open(phone_ledger_path).convert('RGBA')
        ph_back = 570
        pw_back = int(round(ph_back * (im_ledger.width / im_ledger.height)))
        im_ledger = im_ledger.resize((pw_back, ph_back), Image.Resampling.LANCZOS)
        
        im_pass = Image.open(phone_pass_path).convert('RGBA')
        ph_front = 610
        pw_front = int(round(ph_front * (im_pass.width / im_pass.height)))
        im_pass = im_pass.resize((pw_front, ph_front), Image.Resampling.LANCZOS)
        
        # Neon ambient glow on dark slate
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([110, 230, 130 + pw_back + 40, 254 + ph_back + 30], fill=(0, 60, 180, 50))
        shd.rounded_rectangle([130 + 10, 254 + 15, 130 + pw_back - 10, 254 + ph_back + 20], radius=32, fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(24))
        base = Image.alpha_composite(base, sh)
        base.paste(im_ledger, (130, 254), im_ledger)
        
        sh2 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        shd2 = ImageDraw.Draw(sh2)
        shd2.ellipse([340 - 30, 234 + ph_front - 40, 340 + pw_front + 30, 234 + ph_front + 50], fill=(0, 180, 255, 90))
        shd2.rounded_rectangle([340 + 12, 234 + 16, 340 + pw_front - 12, 234 + ph_front + 24], radius=36, fill=(0, 0, 0, 180))
        sh2 = sh2.filter(ImageFilter.GaussianBlur(28))
        base = Image.alpha_composite(base, sh2)
        base.paste(im_pass, (340, 234), im_pass)
        
        draw = ImageDraw.Draw(base)

    # Left Bottom Spec Strip (x=100, y=856, w=660, h=124)
    draw.rounded_rectangle([100, 856, 760, 980], radius=14, fill=(17, 24, 39, 255), outline=(40, 53, 72), width=1)
    draw_pill_badge(draw, left_x=120, cy=880, text="FLUTTER WEB PRODUCTION ENGINE", font=get_font(9, 'bold'), theme='blue', dark_mode=True, pad_x=8, height=20)
    draw.text((120, 908), "• 60fps Native Web CanvasKit / SkWasm 렌더링 파이프라인 탑재", font=get_font(11, 'medium'), fill=(203, 213, 225))
    draw.text((120, 930), "• 100% 온디바이스 로컬 안심 저장 아키텍처 (외부 API 무전송 보안)", font=get_font(11, 'medium'), fill=(203, 213, 225))
    draw.text((120, 952), "• 반응형 모바일 뷰포트 시뮬레이터 & 실시간 키오스크 인터랙션 완벽 지원", font=get_font(11, 'medium'), fill=(56, 189, 248))

    # Right Column: Master Launcher + 4 Step Cards + QR Hub (x=800 to 1820, w=1020)
    rx = 800
    rw = 1020
    proto_entry_url = "https://koyotejw-ux.github.io/zeropass/portfolio/prototype.html"

    # 1. Master Radiant Blue Launcher Card (y=234 to 348, h=114)
    my = 234
    mh = 114
    m_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    m_glow_d = ImageDraw.Draw(m_glow)
    m_glow_d.rounded_rectangle([rx - 6, my - 2, rx + rw + 6, my + mh + 8], radius=24, fill=(0, 87, 255, 120))
    m_glow = m_glow.filter(ImageFilter.GaussianBlur(24))
    base = Image.alpha_composite(base, m_glow)
    
    t = np.linspace(0, 1, rw, endpoint=True, dtype=np.float32)
    r_arr = (0 * (1 - t) + 0 * t).astype(np.uint8)
    g_arr = (87 * (1 - t) + 195 * t).astype(np.uint8)
    b_arr = (255 * (1 - t) + 245 * t).astype(np.uint8)
    grad_arr = np.zeros((mh, rw, 4), dtype=np.uint8)
    grad_arr[:, :, 0] = r_arr
    grad_arr[:, :, 1] = g_arr
    grad_arr[:, :, 2] = b_arr
    grad_arr[:, :, 3] = 255
    grad_box = Image.fromarray(grad_arr, 'RGBA')
    
    grad_mask = Image.new('L', (rw, mh), 0)
    gmd = ImageDraw.Draw(grad_mask)
    gmd.rounded_rectangle([0, 0, rw - 1, mh - 1], radius=16, fill=255)
    base.paste(grad_box, (rx, my), grad_mask)
    draw = ImageDraw.Draw(base)
    
    badge_w = 145
    draw.rounded_rectangle([rx + 24, my + 14, rx + 24 + badge_w, my + 35], radius=10, fill=(0, 36, 110, 190), outline=(255, 255, 255, 180), width=1)
    draw.text((rx + 24 + badge_w // 2, my + 24), "웹 프로토타입 실행", font=get_font(9, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    draw.text((rx + 24, my + 57), "모바일 목업 디바이스에서 전체 플로우 직접 실행하기 ↗", font=get_font(18, 'extrabold'), fill=(255, 255, 255), anchor='lm')
    draw.text((rx + 24, my + 87), "0.8초 키오스크 인증부터 D-Day 수납 장부까지, 4대 핵심 여정을 실물 뷰포트에서 한 번에 체험하세요.", font=get_font(12, 'medium'), fill=(225, 242, 255), anchor='lm')
    
    btn_w = 210
    btn_h = 44
    btn_x = rx + rw - btn_w - 24
    btn_y = my + (mh - btn_h) // 2
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=12, fill=(255, 255, 255), outline=(255, 255, 255), width=1)
    draw.text((btn_x + btn_w // 2, btn_y + btn_h // 2), "인터랙티브 전체 체험 ↗", font=get_font(13.5, 'bold'), fill=(0, 82, 255), anchor='mm')

    # 2. 4 Subdued Step Cards (y=358 to 688)
    steps = [
        ("1", "출결 키오스크 번호 입력", "0.8초 번호 매칭", "다이얼 패드에서 전화번호 뒤 4자리를 터치하면 즉각 해당 원생을 특정하고 등원/하원 분기가 팝업됩니다."),
        ("2", "원터치 등·하원 차감", "실시간 잔여 횟수 갱신", "[등원] 버튼을 누르면 잔여 수업 일수(-1)가 즉시 차감되며 우측 출결 타임라인에 실시간 로그가 기록됩니다."),
        ("3", "D-Day 수납 장부 필터링", "3단계 위험도 분류", "만료 임박(주황), 당일(파랑), 연체(빨강) 탭을 전환하며 실시간 필터링 동작을 직접 테스트할 수 있습니다."),
        ("4", "원클릭 카카오톡 청구서", "정중한 서식 자동 치환", "수납 지연 원생 카드를 터치하여 회원명, 수강과목, 금액, 계좌번호가 자동 생성된 청구서를 확인합니다.")
    ]
    
    sy = 358
    sh_step = 74
    for num_str, title, tag, desc in steps:
        draw.rounded_rectangle([rx, sy, rx + rw, sy + sh_step], radius=12, fill=(18, 24, 38, 255), outline=(30, 41, 59, 255), width=1)
        draw.rounded_rectangle([rx + 16, sy + 16, rx + 52, sy + 56], radius=8, fill=(0, 82, 255, 40), outline=(0, 82, 255, 120), width=1)
        draw.text((rx + 34, sy + 36), num_str, font=get_num_font(16, 'bold'), fill=(56, 189, 248), anchor='mm')
        
        draw.text((rx + 68, sy + 17), title, font=get_font(14, 'bold'), fill=(255, 255, 255))
        draw_pill_badge(draw, left_x=rx + rw - 170, cy=sy + 25, text=tag, font=get_font(9, 'bold'), theme='cyan', dark_mode=True, pad_x=8, height=20)
        draw.text((rx + 68, sy + 43), desc, font=get_font(11.5, 'regular'), fill=(148, 163, 184))
        sy += sh_step + 10

    # 3. Bottom Guide Hint + QR Code Hub (y=716 to 980, h=264)
    qy = 716
    qh = 264
    draw.rounded_rectangle([rx, qy, rx + rw, qy + qh], radius=16, fill=(17, 24, 39, 255), outline=(30, 41, 59, 255), width=1)
    
    # Left Content inside QR plate
    draw_pill_badge(draw, left_x=rx + 24, cy=qy + 26, text="모바일 QR 즉시 실행", font=get_font(9.5, 'bold'), theme='green', dark_mode=True, has_dot=False, pad_x=10, height=22)
    draw.text((rx + 24, qy + 58), "스마트폰 카메라로 QR 코드를 스캔하세요.", font=get_font(17, 'bold'), fill=(255, 255, 255))
    draw.text((rx + 24, qy + 86), "별도 앱 설치 없이 모바일 브라우저에서 60fps 플러터 웹 프로토타입이 즉시 구동됩니다.", font=get_font(12, 'regular'), fill=(148, 163, 184))
    
    # Passy Assistant Character beside QR Code
    mascot_body_p = 'd:/097.flutter_project/auto_portfolio/zeropass/assets/mascot/passy_clean_body.png'
    if os.path.exists(mascot_body_p):
        im_pb = Image.open(mascot_body_p).convert('RGBA')
        pb_h = 75
        pb_w = int(round(pb_h * (im_pb.width / im_pb.height)))
        pb_scaled = im_pb.resize((pb_w, pb_h), Image.Resampling.LANCZOS)
        base.paste(pb_scaled, (rx + rw - 190 - pb_w - 45, qy + 140), pb_scaled)
        draw = ImageDraw.Draw(base)
    
    # 4 Quick Mode Pill Badges
    q_modes = [
        ("01 키오스크 모드", "0.8s 번호 입력"),
        ("02 D-Day 장부", "3단계 위험도 정렬"),
        ("03 원생 디렉터리", "출결 타임라인"),
        ("04 카톡 청구서", "정중한 서식 공유")
    ]
    q_mw = (rw - 280) // 2
    q_my = qy + 120
    for idx, (m_tit, m_sub) in enumerate(q_modes):
        row = idx // 2
        col = idx % 2
        q_bx = rx + 24 + col * (q_mw + 12)
        q_by = q_my + row * 60
        draw.rounded_rectangle([q_bx, q_by, q_bx + q_mw, q_by + 52], radius=10, fill=(24, 32, 54, 255), outline=(40, 53, 80, 255), width=1)
        draw.text((q_bx + 14, q_by + 12), m_tit, font=get_font(11, 'bold'), fill=(255, 255, 255))
        draw.text((q_bx + 14, q_by + 31), m_sub, font=get_font(9.5, 'regular'), fill=(100, 116, 139))
        
    draw.text((rx + 24, qy + qh - 18), "• PC 웹 브라우저에서는 좌측 목업 디바이스를 직접 클릭하여 실시간 인터랙션을 검증할 수 있습니다.", font=get_font(10, 'regular'), fill=(100, 116, 139))

    # Right Real QR Code Generation
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(proto_entry_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    qr_w, qr_h = 190, 190
    qr_resized = qr_img.resize((qr_w, qr_h), Image.Resampling.NEAREST)
    
    qr_plate_x = rx + rw - qr_w - 30
    qr_plate_y = qy + 36
    draw.rounded_rectangle([qr_plate_x - 8, qr_plate_y - 8, qr_plate_x + qr_w + 8, qr_plate_y + qr_h + 8], radius=12, fill=(255, 255, 255))
    base.paste(qr_resized, (qr_plate_x, qr_plate_y))

    draw_slide_footer(draw, 12, dark_mode=True)
    save_slide(base.convert('RGB'), 12)
    print("SAVED perfect Slide 09, 10, 11, 12 successfully!")
