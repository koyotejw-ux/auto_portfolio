import os
import math
from PIL import Image, ImageDraw, ImageFilter
from build_zeropass_white_common import (
    W, H, MOCKUP_DIR, get_font, get_num_font, wrap_text_by_words,
    draw_pill_badge, draw_slide_header, draw_slide_footer, save_slide,
    draw_donut_chart_on_base, draw_diamond, draw_arrow, draw_dashed_line, draw_dashed_arrow,
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
# SLIDE 01: HERO COVER
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
    draw_pill_badge(draw, left_x=100, cy=76, text="프로덕션 케이스 스터디", font=get_font(11.5, 'bold'), theme='blue', has_dot=False, pad_x=12, height=28)
    
    meta_txt = "기획(PM) · UI/UX 디자인 · Android 출시 (v1.0) · 웹 프로토타입"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=(100, 116, 139))
    
    # Category Label
    draw.text((100, 146), "체크앤페이 · CHECK & PAY", font=get_font(14, 'bold'), fill=(0, 82, 255))
    
    # Big Clean Headline
    title_p1 = "1초 원터치 출결, "
    title_p2 = "완벽한 수납 자동화."
    w_p1 = draw.textlength(title_p1, font=get_font(56, 'black'))
    draw.text((100, 178), title_p1, font=get_font(56, 'black'), fill=(15, 23, 42))
    draw.text((100 + w_p1, 178), title_p2, font=get_font(56, 'black'), fill=(0, 82, 255))
    
    # Clean UX Subtitle (2 balanced lines)
    sub1 = "학원·교습소·스튜디오 원장님의 매일 반복되는 출결 체크와 미수금 독촉 스트레스를,"
    sub2 = "단 한 번의 터치와 오프라인 안심 저장 구조로 완전 무결하게 해결하는 엔터프라이즈 모바일 솔루션"
    draw.text((100, 260), sub1, font=get_font(16.5, 'regular'), fill=(71, 85, 105))
    draw.text((100, 288), sub2, font=get_font(16.5, 'semibold'), fill=(30, 41, 59))
    
    # OPEN STORYLINE: Key Strengths
    strengths = [
        ("01", "출결 마찰 제로", "1초 원터치 키오스크 UI", "0.8초 고속 출결 다이얼",
         "원생이 본인 전화번호 뒤 4자리만 터치하면 0.8초 내에 등·하원 처리 및 잔여 횟수가 즉시 차감되어 대기 줄을 원천 제거합니다."),
        ("02", "수납 누수 차단", "스마트 D-Day 수납 장부", "3단계 위험도 정렬 체계",
         "정기 결제일과 잔여 회차를 실시간 계산하여 만료 7일 전부터 3단계 색상(초록/주황/빨강)으로 수납 우선순위를 직관적으로 분류합니다."),
        ("03", "감정 소모 해소", "원클릭 모바일 청구서", "정중한 알림톡 템플릿",
         "회원별 계좌번호와 청구 금액이 자동 치환된 정중한 카카오톡 청구서 템플릿을 터치 한 번으로 전송하여 불편한 대면 독촉을 없앴습니다."),
        ("04", "안심 프라이버시", "100% 로컬 오프라인 볼트", "기기 내부 로컬 안심 저장",
         "외부 유료 서버 없이 기기 내부 로컬 안심 저장소에 암호화 보관하여 월 유지비 0원과 인터넷 끊김 없는 완전한 연속성을 실현했습니다.")
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

    # Right Side: Dual Flagship iPhone Mockups (-11 deg Angled & Ultra-Natural Shadow)
    phone_pass = Image.open(f"{MOCKUP_DIR}/mockup_01_pass.png").convert('RGBA')
    phone_ledger = Image.open(f"{MOCKUP_DIR}/mockup_02_ledger.png").convert('RGBA')
    
    target_h = 670
    target_w = int(round(target_h * (phone_pass.width / phone_pass.height)))
    p_front = phone_pass.resize((target_w, target_h), Image.Resampling.LANCZOS)
    p_back = phone_ledger.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    angle = -11.0
    rot_front = p_front.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    rot_back = p_back.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    def make_shadow_angled(img, blur=44, offset=(22, 40), alpha=80):
        mask = img.split()[3]
        sh_img = Image.new('RGBA', (img.width + 120, img.height + 120), (0, 0, 0, 0))
        black = Image.new('RGBA', img.size, (15, 23, 42, alpha))
        sh_img.paste(black, (60 + offset[0], 60 + offset[1]), mask)
        return sh_img.filter(ImageFilter.GaussianBlur(blur)), (60, 60)
        
    sh_back, pad_b = make_shadow_angled(rot_back, blur=40, offset=(18, 34), alpha=65)
    sh_front, pad_f = make_shadow_angled(rot_front, blur=48, offset=(24, 44), alpha=88)
    
    p_back_x, p_back_y = 1270, 115
    p_front_x, p_front_y = 970, 170
    
    base.paste(sh_back, (p_back_x - pad_b[0], p_back_y - pad_b[1]), sh_back)
    base.paste(rot_back, (p_back_x, p_back_y), rot_back)
    
    base.paste(sh_front, (p_front_x - pad_f[0], p_front_y - pad_f[1]), sh_front)
    base.paste(rot_front, (p_front_x, p_front_y), rot_front)
    
    # 🌟 Mascot "Passy" (패시) Cute Greeting Placement
    mascot_p = 'd:/097.flutter_project/auto_portfolio/zeropass/assets/mascot/passy_clean_body.png'
    if os.path.exists(mascot_p):
        im_m = Image.open(mascot_p).convert('RGBA')
        mh = 240
        mw = int(round(mh * (im_m.width / im_m.height)))
        m_scaled = im_m.resize((mw, mh), Image.Resampling.LANCZOS)
        
        # Ground Shadow for Mascot
        m_sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        m_sh_d = ImageDraw.Draw(m_sh)
        mx_pos = 1530
        my_pos = 580
        m_sh_d.ellipse([mx_pos + 25, my_pos + mh - 25, mx_pos + mw - 15, my_pos + mh + 15], fill=(0, 50, 150, 70))
        m_sh = m_sh.filter(ImageFilter.GaussianBlur(14))
        base = Image.alpha_composite(base, m_sh)
        base.paste(m_scaled, (mx_pos, my_pos), m_scaled)
        
        # Mascot Speech Bubble (Cute Welcoming Message)
        draw = ImageDraw.Draw(base)
        sb_x = mx_pos - 80
        sb_y = my_pos - 45
        sb_w = 260
        sb_h = 42
        draw.rounded_rectangle([sb_x, sb_y, sb_x + sb_w, sb_y + sb_h], radius=12, fill=(255, 255, 255), outline=(0, 82, 255), width=2)
        # Tail
        draw.polygon([(sb_x + 130, sb_y + sb_h), (sb_x + 150, sb_y + sb_h), (sb_x + 145, sb_y + sb_h + 10)], fill=(0, 82, 255))
        draw.polygon([(sb_x + 132, sb_y + sb_h - 1), (sb_x + 148, sb_y + sb_h - 1), (sb_x + 145, sb_y + sb_h + 8)], fill=(255, 255, 255))
        draw.text((sb_x + sb_w // 2, sb_y + sb_h // 2 - 1), "안녕! 난 체크앤페이 마스코트 패시야 🐧", font=get_font(10.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    draw = ImageDraw.Draw(base)
    
    # Bottom 4-Column Specification Strip (Spanning x=100 to 1820, y=840 to 956)
    bar_y = 840
    bar_h = 116
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    col_w = 1720 // 4
    specs = [
        ("담당 역할", "서비스 기획 100% · UI/UX 디자인 100%", "소상공인 리서치 · 문제 정의 · IA 정보 설계 · 와이어프레임 · UI 디자인 총괄"),
        ("진행 기간", "2026.08 - 현재 (v1.0 상용 운영)", "1인 학원·스튜디오 현장 인터뷰 기반 설계 및 실기기 검증 후 지속 고도화"),
        ("디자인 시스템", "신뢰 기반 토큰 및 컴포넌트 규격", "8pt 베이스라인 · 브랜드 일렉트릭 블루(#0052FF) · 라이트 테마 고대비 12.8:1"),
        ("출시 및 배포", "Android 상용 출시 & 60fps 웹 프로토타입", "안심 로컬 보관 아키텍처 탑재 · 실제 뷰포트 인터랙티브 허브 완성")
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
# SLIDE 02: USER RESEARCH | DESK RESEARCH & MARKET STUDY
# ==============================================================
def make_slide_02():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=2,
        category_en="시장 리서치 · 문제 정의",
        title_black="소규모 교육·체육 시설의 고질적 운영 병목과 ",
        title_blue="아날로그 장부의 기존 문제점",
        subtitle_kr="소규모 학원 및 스튜디오 운영자(N=120) 심층 인터뷰와 SaaS 도입 비용 분석을 통해 도출한 3대 핵심 전략"
    )
    
    card_w = 546
    card_h = 224
    gap = 40
    sy = 234
    
    # CARD 1: MARKET TREND (Donut Chart - 84.2%)
    c1_x = 100
    draw.rounded_rectangle([c1_x, sy, c1_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c1_x, sy + 18, c1_x + 5, sy + card_h - 18], radius=2, fill=(220, 38, 38))
    
    draw_pill_badge(draw, left_x=c1_x + 24, cy=sy + 26, text="비용 부담 리서치", font=get_font(10, 'bold'), theme='red', pad_x=8, height=22)
    draw.text((c1_x + 24, sy + 58), "고비용 ERP와 기능 과잉 부담", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c1_x + 24, sy + 88), "원생 30~50명 규모 원장님의 84%가 월 5~15만원의\n과도한 ERP 구독료 부담으로 도입을 포기합니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    draw.text((c1_x + 24, sy + 144), "84.2%", font=get_num_font(38, 'black'), fill=(220, 38, 38))
    draw.text((c1_x + 24, sy + 188), "비용 부담 응답률 (소상공인 실태 N=120)", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    cx_donut = c1_x + card_w - 95
    cy_donut = sy + 116
    draw_donut_chart_on_base(base, cx_donut, cy_donut, r_outer=56, r_inner=38, percentage=84.2, col_fill=(220, 38, 38), col_track=(254, 226, 226))
    draw = ImageDraw.Draw(base)
    draw_pill_badge(draw, cx=cx_donut, cy=sy + 32, text="N=120 설문", font=get_font(9, 'bold'), theme='red', pad_x=8, height=20)
    draw.text((cx_donut, cy_donut - 8), "84%", font=get_num_font(18, 'black'), fill=(220, 38, 38), anchor='mm')
    draw.text((cx_donut, cy_donut + 14), "포기율", font=get_font(9.5, 'bold'), fill=(100, 116, 139), anchor='mm')
    
    # CARD 2: BEHAVIOR TREND (Horizontal Bar - 45s -> 0.8s)
    c2_x = c1_x + card_w + gap
    draw.rounded_rectangle([c2_x, sy, c2_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c2_x, sy + 18, c2_x + 5, sy + card_h - 18], radius=2, fill=(217, 119, 6))
    
    draw_pill_badge(draw, left_x=c2_x + 24, cy=sy + 26, text="출결 병목 분석", font=get_font(10, 'bold'), theme='amber', pad_x=8, height=22)
    draw.text((c2_x + 24, sy + 58), "수기 출석부의 대기 병목 시간", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c2_x + 24, sy + 88), "원생들이 이름을 손으로 적거나 카드를 찾는 동안\n수업 시작 전 15~20분의 골든타임이 소모됩니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    draw.text((c2_x + 24, sy + 144), "45초 → 0.8초", font=get_num_font(28, 'black'), fill=(217, 119, 6))
    draw.text((c2_x + 24, sy + 188), "출결 소요 시간 98% 단축 (원터치 키오스크)", font=get_font(11, 'bold'), fill=(16, 185, 129))
    
    bx = c2_x + card_w - 170
    b_w = 145
    draw_pill_badge(draw, cx=bx + b_w // 2, cy=sy + 32, text="인증 소요 시간", font=get_font(9, 'bold'), theme='amber', pad_x=8, height=20)
    draw.text((bx, sy + 57), "기존 수기/카드", font=get_font(10, 'bold'), fill=(148, 163, 184))
    draw.text((bx + b_w, sy + 57), "45.0초", font=get_font(11.5, 'bold'), fill=(220, 38, 38), anchor='ra')
    draw.rounded_rectangle([bx, sy + 75, bx + b_w, sy + 91], radius=8, fill=(248, 113, 113))
    
    draw.text((bx, sy + 101), "체크앤페이", font=get_font(10, 'bold'), fill=(0, 82, 255))
    draw.text((bx + b_w, sy + 101), "0.8초", font=get_font(11.5, 'bold'), fill=(16, 185, 129), anchor='ra')
    draw.rounded_rectangle([bx, sy + 119, bx + b_w, sy + 135], radius=8, fill=(241, 245, 249))
    draw.rounded_rectangle([bx, sy + 119, bx + 18, sy + 135], radius=8, fill=(16, 185, 129))
    draw_pill_badge(draw, cx=bx + b_w // 2, cy=sy + 166, text="56배 고속 · 98% 단축", font=get_font(9.5, 'bold'), theme='green', pad_x=10, height=24, solid=True)
    
    # CARD 3: INDUSTRY GAP (Vertical Column - 100% On-Device vs 0%)
    c3_x = c2_x + card_w + gap
    draw.rounded_rectangle([c3_x, sy, c3_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c3_x, sy + 18, c3_x + 5, sy + card_h - 18], radius=2, fill=(0, 82, 255))
    
    draw_pill_badge(draw, left_x=c3_x + 24, cy=sy + 26, text="데이터 안심 보관", font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((c3_x + 24, sy + 58), "온디바이스 로컬 독립 보안 부재", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c3_x + 24, sy + 88), "기존 모든 학원 관리 프로그램은 외부 클라우드 의존으로\n인터넷 장애 시 출결 중단 및 개인정보 유출 위험 노출.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    draw.text((c3_x + 24, sy + 144), "100%", font=get_num_font(38, 'black'), fill=(0, 82, 255))
    draw.text((c3_x + 24, sy + 188), "오프라인 연속 가동률 (로컬 안심 볼트)", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    draw_pill_badge(draw, cx=c3_x + card_w - 90, cy=sy + 32, text="서버 독립성", font=get_font(9, 'bold'), theme='blue', pad_x=8, height=20)
    base_v_y = sy + 160
    col_h = 74
    draw.line([(c3_x + card_w - 165, base_v_y), (c3_x + card_w - 20, base_v_y)], fill=(226, 232, 240), width=1)
    
    col1_x = c3_x + card_w - 124
    draw.rounded_rectangle([col1_x - 22, base_v_y - col_h, col1_x + 22, base_v_y], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([col1_x - 22, base_v_y - 8, col1_x + 22, base_v_y], radius=3, fill=(254, 202, 202), outline=(239, 68, 68), width=1)
    draw.text((col1_x, base_v_y - col_h - 10), "0%", font=get_num_font(13.5, 'bold'), fill=(220, 38, 38), anchor='mm')
    draw.text((col1_x, base_v_y + 16), "일반 SaaS", font=get_font(10.5, 'bold'), fill=(148, 163, 184), anchor='mm')
    
    col2_x = c3_x + card_w - 56
    draw.rounded_rectangle([col2_x - 22, base_v_y - col_h, col2_x + 22, base_v_y], radius=6, fill=(0, 82, 255))
    draw.text((col2_x, base_v_y - col_h - 10), "100%", font=get_num_font(13.5, 'black'), fill=(0, 82, 255), anchor='mm')
    draw.text((col2_x, base_v_y + 16), "체크앤페이", font=get_font(10.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 2. MIDDLE: INSIGHT BANNER
    ins_y = 465
    draw.rounded_rectangle([100, ins_y, 1820, ins_y + 54], radius=12, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=120, cy=ins_y + 27, text="핵심 발견점", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=30)
    ins_text = "소규모 사업장에는 복잡한 대형 ERP가 아닌, '1초 출결 키오스크'와 'D-Day 미수금 자동 정렬'에 특화된 온디바이스 볼트가 정답이다."
    draw.text((260, ins_y + 17), ins_text, font=get_font(14.5, 'bold'), fill=(0, 82, 255))
    draw.polygon([(960, ins_y + 54), (952, ins_y + 64), (968, ins_y + 64)], fill=(0, 82, 255))
    
    # 3. BOTTOM: 2x2 SWOT MATRIX (Left) + 3 STRATEGIC PILLARS (Right)
    b_y = 550
    swot_w = 830
    swot_h = 415
    draw.rounded_rectangle([100, b_y, 100 + swot_w, b_y + swot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((125, b_y + 20), "SWOT 포지셔닝 분석 : 체크앤페이의 전략적 기회 요인", font=get_font(15, 'bold'), fill=(15, 23, 42))
    draw.line([(125, b_y + 48), (100 + swot_w - 25, b_y + 48)], fill=(241, 245, 249), width=1)
    
    qw = (swot_w - 60) // 2
    qh = 158
    
    # S
    s_x = 125
    s_y = b_y + 65
    draw.rounded_rectangle([s_x, s_y, s_x + qw, s_y + qh], radius=10, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw_pill_badge(draw, left_x=s_x + 14, cy=s_y + 22, text="강점 (Strength)", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24, solid=True)
    s_points = ["• 0.8초 키오스크 번호 매칭 & 등하원", "• 서버 유지비 0원 & 완전한 오프라인", "• D-Day 3단계 시각적 미수금 장부"]
    for idx, p in enumerate(s_points):
        draw.text((s_x + 14, s_y + 56 + idx * 24), p, font=get_font(11.5, 'medium'), fill=(6, 95, 70))
        
    # W
    w_x = s_x + qw + 10
    w_y = s_y
    draw.rounded_rectangle([w_x, w_y, w_x + qw, w_y + qh], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=w_x + 14, cy=w_y + 22, text="약점 (Weakness)", font=get_font(10, 'bold'), theme='red', pad_x=10, height=24, solid=True)
    w_points = ["• 온디바이스 특성상 초기 기기 세팅 필요", "• 대형 프랜차이즈 다점포 중앙통제 부재", "• 신규 브랜드 인지도 확보 필요"]
    for idx, p in enumerate(w_points):
        draw.text((w_x + 14, w_y + 56 + idx * 24), p, font=get_font(11.5, 'medium'), fill=(153, 27, 27))
        
    # O
    o_x = s_x
    o_y = s_y + qh + 12
    draw.rounded_rectangle([o_x, o_y, o_x + qw, o_y + qh], radius=10, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=o_x + 14, cy=o_y + 22, text="기회 (Opportunity)", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24, solid=True)
    o_points = ["• 1인 교습소·피트니스 급증 (고정비 절감)", "• 개인정보 보호 강화 (로컬 볼트 선호)", "• 글로벌 6개 국어 스토어 확장성"]
    for idx, p in enumerate(o_points):
        draw.text((o_x + 14, o_y + 56 + idx * 24), p, font=get_font(11.5, 'medium'), fill=(30, 64, 175))
        
    # T
    t_x = w_x
    t_y = o_y
    draw.rounded_rectangle([t_x, t_y, t_x + qw, t_y + qh], radius=10, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw_pill_badge(draw, left_x=t_x + 14, cy=t_y + 22, text="위협 (Threat)", font=get_font(10, 'bold'), theme='amber', pad_x=10, height=24, solid=True)
    t_points = ["• 대형 ERP 업체의 저가 번들링 공세", "• 공기계 태블릿 고장 및 분실 리스크", "• 플랫폼 종속적 모바일 정책 변경"]
    for idx, p in enumerate(t_points):
        draw.text((t_x + 14, t_y + 56 + idx * 24), p, font=get_font(11.5, 'medium'), fill=(146, 64, 14))

    # Right: 3 Strategic Pillars
    sp_x = 970
    sp_w = 850
    draw.rounded_rectangle([sp_x, b_y, sp_x + sp_w, b_y + swot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((sp_x + 25, b_y + 20), "3대 핵심 프로덕트 전략 (Strategic Pillars)", font=get_font(15, 'bold'), fill=(15, 23, 42))
    draw.line([(sp_x + 25, b_y + 48), (sp_x + sp_w - 25, b_y + 48)], fill=(241, 245, 249), width=1)
    
    pillars = [
        ("전략 01", "1초 원터치 키오스크 UI", "대기 시간 98% 단축 (무마찰 출결)",
         "공기계 스마트폰·태블릿에 띄워두면 원생이 본인 전화번호 뒤 4자리만 터치하여 0.8초 내에 등·하원 처리 및 잔여 횟수 즉시 차감."),
        ("전략 02", "스마트 D-Day 수납 장부", "미수금 누수 원천 차단 (적기 회수)",
         "매달 말일에 몰아보던 수동 장부 대신, 만료 7일 전(주황)부터 당일/연체(빨강)를 3단계 색상으로 자동 정렬하여 수납 우선순위 실시간 파악."),
        ("전략 03", "로컬 보안 안심 볼트", "월 서버비 0원 & 100% 로컬 암호화",
         "외부 유료 서버 의존 없이 기기 내부 로컬 안전 저장소에 암호화 보관하여 인터넷 장애 시에도 키오스크가 멈추지 않는 연속성과 개인정보 완벽 보호 실현.")
    ]
    py = b_y + 65
    for p_tag, p_tit, p_sub, p_desc in pillars:
        draw.rounded_rectangle([sp_x + 25, py, sp_x + sp_w - 25, py + 98], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=sp_x + 40, cy=py + 24, text=p_tag, font=get_font(10, 'bold'), theme='blue', pad_x=8, height=22)
        draw.text((sp_x + 155, py + 14), p_tit, font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((sp_x + 350, py + 16), "• " + p_sub, font=get_font(12, 'bold'), fill=(0, 82, 255))
        draw.text((sp_x + 40, py + 48), p_desc, font=get_font(12, 'regular'), fill=(71, 85, 105))
        py += 108

    draw_slide_footer(draw, 2)
    save_slide(base.convert('RGB'), 2)

# ==============================================================
# SLIDE 03: TARGET & PERSONA | SEGMENTATION MATRIX & BENCHMARK
# ==============================================================
def make_slide_03():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=3,
        category_en="타깃 세그먼트 · 페르소나 분석",
        title_black="타깃 세그먼트 매트릭스와 ",
        title_blue="경쟁사 벤치마킹 분석",
        subtitle_kr="2x2 타깃 포지셔닝 매트릭스와 4대 플랫폼 벤치마크, 그리고 대표 페르소나 행동 지표"
    )
    
    # 1. 2x2 Target Segmentation Matrix (Top-Left)
    t_x = 100
    t_y = 234
    t_w = 780
    t_h = 378
    draw.rounded_rectangle([t_x, t_y, t_x + t_w, t_y + t_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((t_x + 24, t_y + 18), "타깃 세그먼트 분석 매트릭스", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((t_x + 24, t_y + 38), "원생 규모와 디지털 숙련도에 따른 4대 학원·교습소 유형 분류", font=get_font(11.5, 'medium'), fill=(100, 116, 139))
    
    grid_w = 540
    grid_h = 260
    grid_x = t_x + (t_w - grid_w) // 2
    grid_y = t_y + 76
    qw = (grid_w - 16) // 2
    qh = (grid_h - 16) // 2
    
    axis_x = grid_x + qw + 8
    axis_y = grid_y + qh + 8
    draw.line([(axis_x, grid_y), (axis_x, grid_y + grid_h)], fill=(203, 213, 225), width=2)
    draw.line([(grid_x, axis_y), (grid_x + grid_w, axis_y)], fill=(203, 213, 225), width=2)
    
    draw.text((axis_x, grid_y - 12), "▲ 소규모 1인 (10~60명)", font=get_font(10, 'bold'), fill=(0, 82, 255), anchor='ms')
    draw.text((axis_x, grid_y + grid_h + 16), "▼ 대형 기업형 (100명+)", font=get_font(10, 'bold'), fill=(100, 116, 139), anchor='ma')
    draw.text((grid_x - 12, axis_y), "◀ 종이/아날로그", font=get_font(10, 'bold'), fill=(100, 116, 139), anchor='rm')
    draw.text((grid_x + grid_w + 12, axis_y), "모바일/간편화 ▶", font=get_font(10, 'bold'), fill=(0, 82, 255), anchor='lm')
    
    # Q1: CORE TARGET (1인 교습소/공부방)
    q1_x = grid_x + qw + 16
    q1_y = grid_y
    draw.rounded_rectangle([q1_x, q1_y, q1_x + qw, q1_y + qh], radius=8, fill=(239, 246, 255), outline=(147, 197, 253), width=1)
    draw_pill_badge(draw, left_x=q1_x + 12, cy=q1_y + 22, text="핵심 타깃", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22, solid=True)
    draw.text((q1_x + 12, q1_y + 44), "1인 교습소 · 스튜디오", font=get_font(13, 'bold'), fill=(0, 82, 255))
    draw.text((q1_x + 12, q1_y + 68), "• 수업과 행정을 1인이 전담하여 출결 여력 부족\n• 월 유지비 0원 & 키오스크 즉각 도입 선호", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    # Q2: PRIMARY TARGET (소규모 학원)
    q2_x = q1_x
    q2_y = axis_y + 8
    draw.rounded_rectangle([q2_x, q2_y, q2_x + qw, q2_y + qh], radius=8, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=q2_x + 12, cy=q2_y + 22, text="주요 타깃", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=22, solid=True)
    draw.text((q2_x + 12, q2_y + 44), "소형 예체능 · 보습학원", font=get_font(13, 'bold'), fill=(16, 185, 129))
    draw.text((q2_x + 12, q2_y + 68), "• 미수금 회수 지연으로 현금 흐름 악화\n• 원클릭 카톡 청구서로 감정소모 해소", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    # Q3: 아날로그 유지층
    q3_x = grid_x
    q3_y = grid_y
    draw.rounded_rectangle([q3_x, q3_y, q3_x + qw, q3_y + qh], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=q3_x + 12, cy=q3_y + 22, text="잠재 고객", font=get_font(9.5, 'bold'), theme='slate', pad_x=8, height=22)
    draw.text((q3_x + 12, q3_y + 44), "전통 아날로그 교습소", font=get_font(13, 'bold'), fill=(100, 116, 139))
    draw.text((q3_x + 12, q3_y + 68), "• 수기 출석부와 종이 영수증 고수\n• 복잡한 IT 도구 기피, 4자리 번호 전환 가능", font=get_font(11, 'regular'), fill=(100, 116, 139), spacing=3)
    
    # Q4: 대형 ERP 종속층
    q4_x = grid_x
    q4_y = q2_y
    draw.rounded_rectangle([q4_x, q4_y, q4_x + qw, q4_y + qh], radius=8, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=q4_x + 12, cy=q4_y + 22, text="후순위 타깃", font=get_font(9.5, 'bold'), theme='red', pad_x=8, height=22)
    draw.text((q4_x + 12, q4_y + 44), "대형 입시 종합학원", font=get_font(13, 'bold'), fill=(153, 27, 27))
    draw.text((q4_x + 12, q4_y + 68), "• 수백만원 대형 ERP 및 지문인식기 사용\n• 전담 행정직원 상주로 키오스크 단독 비선호", font=get_font(11, 'regular'), fill=(153, 27, 27), spacing=3)

    # 2. Competitive Benchmark Table (Top-Right)
    b_x = 920
    b_y = 234
    b_w = 900
    b_h = 378
    draw.rounded_rectangle([b_x, b_y, b_x + b_w, b_y + b_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((b_x + 24, b_y + 18), "경쟁 솔루션 비교 분석표", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((b_x + 24, b_y + 38), "기존 대형 학원 ERP 및 출결 서비스 대비 체크앤페이의 핵심 차별화 요소", font=get_font(11.5, 'medium'), fill=(100, 116, 139))
    
    table_y = b_y + 68
    th_h = 36
    draw.rounded_rectangle([b_x + 20, table_y, b_x + b_w - 20, table_y + th_h], radius=8, fill=(241, 245, 249))
    cols = [("비교 항목", 180), ("대형 ERP (T사)", 160), ("출결 전용 (C사)", 160), ("수기 장부", 160), ("체크앤페이", 200)]
    tx = b_x + 20
    for c_tit, c_w in cols:
        draw.text((tx + c_w // 2, table_y + th_h // 2), c_tit, font=get_font(11, 'bold'), fill=(15, 23, 42) if c_tit != "체크앤페이" else (0, 82, 255), anchor='mm')
        tx += c_w
        
    bench_rows = [
        ("월 이용 요금", "월 5~15만 원", "월 3~6만 원", "월 0원", "완전 무료 / Pro 소장"),
        ("키오스크 하드웨어", "고가 전용 단말기 필수", "전용 태블릿 렌탈", "종이/바인더", "남는 공기계 스마트폰/태블릿"),
        ("출결 인증 속도", "평균 15초 (카드/지문)", "평균 5초 (앱 태그)", "평균 45초 (손글씨)", "0.8초 (전화번호 4자리)"),
        ("수납 및 미수금", "복잡한 복식회계", "단순 결제 링크", "매월 말 수동 대조", "D-Day 3단계 컬러 자동분류"),
        ("데이터 보안", "외부 서버 전송", "외부 서버 전송", "분실/훼손 위험", "100% 온디바이스 암호화")
    ]
    ry = table_y + th_h + 8
    for r_idx, r_data in enumerate(bench_rows):
        row_bg = (239, 246, 255) if r_idx % 2 == 1 else (255, 255, 255)
        draw.rounded_rectangle([b_x + 20, ry, b_x + b_w - 20, ry + 42], radius=6, fill=row_bg)
        tx = b_x + 20
        for val_idx, val in enumerate(r_data):
            c_w = cols[val_idx][1]
            val_col = (0, 82, 255) if val_idx == 4 else ((15, 23, 42) if val_idx == 0 else (71, 85, 105))
            val_font = get_font(11.5, 'bold') if val_idx in [0, 4] else get_font(11, 'regular')
            draw.text((tx + c_w // 2, ry + 21), val, font=val_font, fill=val_col, anchor='mm')
            tx += c_w
        ry += 48

    # 3. Bottom Persona Profiles (Primary & Secondary with Persona Behavioral Spectrums)
    p_y = 625
    pw = 840
    ph = 345
    
    # Persona 1: 이지은 원장 (1인 음악학원)
    draw.rounded_rectangle([100, p_y, 100 + pw, p_y + ph], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=125, cy=p_y + 24, text="핵심 페르소나 01", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((125, p_y + 52), "이지은 (34세 · 피아노 교습소 1인 원장)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.text((125, p_y + 76), "• 운영 환경: 원생 38명 · 강사 없이 1인 운영 · 주 5일 수업", font=get_font(12, 'medium'), fill=(71, 85, 105))
    
    p1_cols = [
        ("주요 불편 사항", "• 레슨 도중 원생 올 때마다 출석체크로 수업 단절\n• 회비 납부일이 제각각이라 카톡 독촉 민망함\n• 대형 ERP는 월 8만원이나 해서 소규모에 비효율"),
        ("해결 목표 및 니즈", "• 아이들이 들어와 스스로 0.8초 만에 찍는 키오스크\n• 만료 임박 회원 정중한 청구서 템플릿 원클릭 전송\n• 복잡한 교육 없이 공기계에 깔아 쓰는 단순함")
    ]
    p_cx = 125
    for c_tit, c_desc in p1_cols:
        draw.rounded_rectangle([p_cx, p_y + 102, p_cx + 380, p_y + 234], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((p_cx + 14, p_y + 116), c_tit, font=get_font(12, 'bold'), fill=(0, 82, 255))
        d_y = p_y + 140
        for dl in c_desc.split('\n'):
            draw.text((p_cx + 14, d_y), dl, font=get_font(11, 'regular'), fill=(71, 85, 105))
            d_y += 20
        p_cx += 405
        
    draw.line([(125, p_y + 248), (100 + pw - 25, p_y + 248)], fill=(241, 245, 249), width=1)
    draw.text((125, p_y + 258), "운영 성향 지표 분석", font=get_font(10, 'bold'), fill=(100, 116, 139))
    from build_zeropass_white_common import draw_behavior_slider
    draw_behavior_slider(draw, 125, p_y + 282, 380, "운영 형태", "1인 단독", "전담 직원", 0.15, theme='blue')
    draw_behavior_slider(draw, 530, p_y + 282, 380, "출결 방식", "0.8초 키오스크", "수기 장부", 0.10, theme='blue')
    draw_behavior_slider(draw, 125, p_y + 316, 380, "수납 관리", "D-Day 자동", "월말 정산", 0.20, theme='blue')
    draw_behavior_slider(draw, 530, p_y + 316, 380, "서버 의존", "오프라인 안심", "클라우드", 0.10, theme='blue')

    # Persona 2: 박진우 대표 (1인 PT/필라테스 스튜디오)
    p2_x = 980
    draw.rounded_rectangle([p2_x, p_y, p2_x + pw, p_y + ph], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p2_x + 25, cy=p_y + 24, text="보조 페르소나 02", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24)
    draw.text((p2_x + 25, p_y + 52), "박진우 (39세 · 1인 기구필라테스 스튜디오 운영)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.text((p2_x + 25, p_y + 76), "• 운영 환경: 회원 55명 · 10회/20회/30회 세션제 · 예약제 운영", font=get_font(12, 'medium'), fill=(71, 85, 105))
    
    p2_cols = [
        ("주요 불편 사항", "• 회원별 잔여 횟수 차감 누락되어 정산 시 분쟁 발생\n• 운동 후 지친 회원에게 재등록 요청하기 어색함\n• 인터넷 장애 시 헬스장 전산 먹통으로 출결 중단"),
        ("해결 목표 및 니즈", "• 입장 시 4자리 터치 즉시 잔여 횟수(-1) 자동 차감\n• 잔여 3회 이하 회원 자동 분류 및 알림톡 전송\n• 100% 로컬 작동으로 통신 장애에도 멈추지 않는 연속성")
    ]
    p_cx2 = p2_x + 25
    for c_tit, c_desc in p2_cols:
        draw.rounded_rectangle([p_cx2, p_y + 102, p_cx2 + 380, p_y + 234], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((p_cx2 + 14, p_y + 116), c_tit, font=get_font(12, 'bold'), fill=(16, 185, 129))
        d_y = p_y + 140
        for dl in c_desc.split('\n'):
            draw.text((p_cx2 + 14, d_y), dl, font=get_font(11, 'regular'), fill=(71, 85, 105))
            d_y += 20
        p_cx2 += 405
        
    draw.line([(p2_x + 25, p_y + 248), (p2_x + pw - 25, p_y + 248)], fill=(241, 245, 249), width=1)
    draw.text((p2_x + 25, p_y + 258), "운영 성향 지표 분석", font=get_font(10, 'bold'), fill=(100, 116, 139))
    draw_behavior_slider(draw, p2_x + 25, p_y + 282, 380, "세션 차감", "원터치 자동", "수동 체크", 0.10, theme='green')
    draw_behavior_slider(draw, p2_x + 430, p_y + 282, 380, "회수 주기", "D-3 사전예방", "연체 후 독촉", 0.25, theme='green')
    draw_behavior_slider(draw, p2_x + 25, p_y + 316, 380, "기기 활용", "공기계 태블릿", "고가 키오스크", 0.20, theme='green')
    draw_behavior_slider(draw, p2_x + 430, p_y + 316, 380, "프라이버시", "온디바이스", "외부 서버", 0.15, theme='green')

    draw_slide_footer(draw, 3)
    save_slide(base.convert('RGB'), 3)

# ==============================================================
# SLIDE 04: INFORMATION ARCHITECTURE (IA) - CLEAN HIERARCHY TREE
# ==============================================================
def make_slide_04():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw,
        slide_num=4,
        category_en="정보 구조도 (IA) · 서비스 설계",
        title_black="누구나 바로 이해하고 쓰는 ",
        title_blue="5대 핵심 메뉴 구조 (IA)",
        subtitle_kr="원터치 출결부터 수납 장부, 원생 디렉터리, 보안 볼트까지 필요한 기능을 한눈에 찾을 수 있는 쉬운 계층 구조"
    )
    
    top_badge_x = 1450
    top_badge_y = 65
    draw.rounded_rectangle([top_badge_x, top_badge_y, top_badge_x + 370, top_badge_y + 60], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    mascot_p = 'd:/097.flutter_project/auto_portfolio/zeropass/assets/mascot/passy_clean_body.png'
    if os.path.exists(mascot_p):
        im_m = Image.open(mascot_p).convert('RGBA')
        mh = 50
        mw = int(round(mh * (im_m.width / im_m.height)))
        m_scaled = im_m.resize((mw, mh), Image.Resampling.LANCZOS)
        base.paste(m_scaled, (top_badge_x + 12, top_badge_y + 5), m_scaled)
        draw = ImageDraw.Draw(base)
        text_x = top_badge_x + mw + 20
    else:
        draw_pill_badge(draw, left_x=top_badge_x + 16, cy=top_badge_y + 30, text="서비스 구성", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=24)
        text_x = top_badge_x + 110
        
    draw.text((text_x, top_badge_y + 18), "5대 메인 탭 구조 (IA)", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    draw.text((text_x, top_badge_y + 38), "총 25개 직관적 화면 · 패시 안내 탑재", font=get_font(10.5, 'medium'), fill=(0, 82, 255))
    
    # Root Node
    root_x1, root_y1, root_x2, root_y2 = 730, 226, 1190, 286
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=12, fill=(255, 255, 255), outline=(0, 82, 255), width=2)
    b_root = draw_pill_badge(draw, left_x=root_x1 + 18, cy=root_y1 + 30, text="시작 화면", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=26)
    draw.text((b_root[2] + 16, root_y1 + 19), "체크앤페이 전체 메뉴 구조 (IA)", font=get_font(14.5, 'bold'), fill=(15, 23, 42))
    draw.text((b_root[2] + 16, root_y1 + 41), "원생 키오스크와 원장님 ERP를 통합한 5대 핵심 도메인", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    col_centers = [cx + cw // 2 for cx in cols_x]
    
    draw.line([(960, root_y2), (960, 308)], fill=(0, 82, 255), width=2)
    draw.ellipse([956, 304, 964, 312], fill=(0, 82, 255))
    draw.line([(col_centers[0], 308), (col_centers[-1], 308)], fill=(0, 82, 255, 180), width=2)
    for cx in col_centers:
        draw.ellipse([cx - 4, 308 - 4, cx + 4, 308 + 4], fill=(0, 82, 255))
        draw_arrow(draw, (cx, 308), (cx, 330), col=(0, 82, 255), width=2, arrow_size=4)
        
    ia_domains = [
        ("01. 출결 키오스크", "1초 원터치 인증", "번호 4자리 즉시 매칭", [
            ("인증 화면", "다이얼 패드", "대형 80dp 터치 숫자 키패드", False),
            ("분기 팝업", "등원/하원 선택", "당일 상태에 따른 원터치 액션", False),
            ("피드백", "잔여 횟수 토스트", "차감 결과 및 학부모 알림 연동", True),
            ("로그 화면", "오늘 출결 타임라인", "실시간 등하원 기록 교차 확인", False)
        ]),
        ("02. 수납 장부", "D-Day 위험도 분류", "월말 미수금 누수 원천 차단", [
            ("대시보드", "월별 수납 현황", "총 예상 수납액 vs 미수금 집계", False),
            ("정렬 탭", "D-Day 3단계 필터", "만료 7일전(주의) / 당일 / 연체", True),
            ("청구서", "원클릭 카톡 청구", "회원명·금액·계좌 자동 템플릿", True),
            ("정산 모달", "결제 수단 처리", "현금/카드/계좌이체 즉시 반영", False)
        ]),
        ("03. 원생 관리", "회원 프로필 & 수강권", "수강권 회차 및 만료일 관리", [
            ("회원 목록", "전체 원생 디렉터리", "이름·전화번호 실시간 고속 검색", False),
            ("프로필", "수강권 등록/수정", "정기 기간권 및 회차제 수강권", False),
            ("이력 조회", "출결 & 수납 히스토리", "과거 출석 일자 및 납부 내역", False),
            ("데이터 연동", "CSV 대량 등록/내보내기", "엑셀 호환 데이터 백업/복원", True)
        ]),
        ("04. 프로 멤버십", "상용 라이선스 & 확장", "무제한 원생 등록 평생 소장", [
            ("라이선스", "Pro 영구 소장권", "월 구독료 없는 1회 구매 라이선스", False),
            ("기능 해금", "무제한 회원 등록", "무료 30명 제한 해제 및 로고", True),
            ("복원 센터", "구글 계정 원클릭 복원", "기기 변경 시에도 라이선스 유지", False),
            ("혜택 관리", "VIP 무광고 세션", "보상형 광고 시청 시 무료 체험", True)
        ]),
        ("05. 보안 볼트", "로컬 설정 & 프라이버시", "100% 온디바이스 암호화 관리", [
            ("상점 설정", "스튜디오 상호 & 계좌", "청구서에 자동 입력될 계좌 지정", False),
            ("알림 템플릿", "문자/카톡 문구 커스텀", "출결 완료 및 회비 안내 문구", False),
            ("다국어 전환", "글로벌 6개 국어 지원", "한국어/영어/일어/중국어/베트남어/스페인어", True),
            ("보안 볼트", "로컬 안심 백업/복구", "외부 서버 전송 없는 암호화 파일", True)
        ])
    ]
    
    card_y = 330
    for idx, (tab_code, tab_name, tab_sub, sub_screens) in enumerate(ia_domains):
        cx = cols_x[idx]
        draw.rounded_rectangle([cx, card_y, cx + cw, card_y + 60], radius=10, fill=(255, 255, 255), outline=(0, 82, 255) if idx in [0, 1] else (203, 213, 225), width=2 if idx in [0, 1] else 1)
        draw_pill_badge(draw, left_x=cx + 12, cy=card_y + 20, text=tab_code.split('.')[0], font=get_font(9.5, 'bold'), theme='blue' if idx in [0, 1] else 'slate', pad_x=6, height=18)
        draw.text((cx + 56, card_y + 11), tab_code.split('.')[1].strip(), font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 12, card_y + 38), tab_sub, font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        
        draw.line([(cx + cw // 2, card_y + 60), (cx + cw // 2, card_y + 80)], fill=(0, 82, 255), width=2)
        
        sy = card_y + 80
        for s_type, s_name, s_desc, is_key in sub_screens:
            bg_col = (239, 246, 255) if is_key else (255, 255, 255)
            border_col = (147, 197, 253) if is_key else (226, 232, 240)
            draw.rounded_rectangle([cx, sy, cx + cw, sy + 115], radius=10, fill=bg_col, outline=border_col, width=1)
            
            draw_pill_badge(draw, left_x=cx + 12, cy=sy + 20, text=s_type, font=get_font(8.5, 'bold'), theme='blue' if is_key else 'slate', pad_x=6, height=18)
            draw.text((cx + 80, sy + 11), s_name, font=get_font(13, 'bold'), fill=(15, 23, 42))
            draw.text((cx + 12, sy + 42), s_desc, font=get_font(11, 'regular'), fill=(71, 85, 105))
            draw.line([(cx + 12, sy + 74), (cx + cw - 12, sy + 74)], fill=(226, 232, 240), width=1)
            draw.text((cx + 12, sy + 88), "로컬 즉시 동기화", font=get_font(9.5, 'medium'), fill=(0, 82, 255) if is_key else (148, 163, 184))
            sy += 128

    draw_slide_footer(draw, 4)
    save_slide(base.convert('RGB'), 4)
