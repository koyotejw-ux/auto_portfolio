import os

target_path = r'd:\097.flutter_project\auto_portfolio\zeropass\deck_slides_white_01_04.py'
with open(target_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_slide_01 = '''def make_slide_01():
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
    draw_pill_badge(draw, left_x=100, cy=76, text="2026 CASE STUDY", font=get_font(11.5, 'bold'), theme='blue', has_dot=True, pad_x=12, height=28)
    
    meta_txt = "기획(PM) · UI/UX 디자인 · Android Live (v1.0) · Web Prototype"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=(100, 116, 139))
    
    # Category Label
    draw.text((100, 146), "CHECK & PAY · ZEROPASS", font=get_font(14, 'bold'), fill=(0, 82, 255))
    
    # Big Clean Headline
    title_p1 = "1초 원터치 출결, "
    title_p2 = "완벽한 수납 자동화."
    w_p1 = draw.textlength(title_p1, font=get_font(56, 'black'))
    draw.text((100, 178), title_p1, font=get_font(56, 'black'), fill=(15, 23, 42))
    draw.text((100 + w_p1, 178), title_p2, font=get_font(56, 'black'), fill=(0, 82, 255))
    
    # Clean UX Subtitle (2 balanced lines)
    sub1 = "학원·교습소·스튜디오 원장님의 매일 반복되는 출결 체크와 미수금 독촉 스트레스를,"
    sub2 = "단 한 번의 터치와 오프라인 SQLite 볼트 아키텍처로 완전 무결하게 해결하는 엔터프라이즈 모바일 솔루션"
    draw.text((100, 260), sub1, font=get_font(16.5, 'regular'), fill=(71, 85, 105))
    draw.text((100, 288), sub2, font=get_font(16.5, 'semibold'), fill=(30, 41, 59))
    
    # OPEN STORYLINE: Key Strengths
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
    
    draw = ImageDraw.Draw(base)
    
    # Bottom 4-Column Specification Strip (Spanning x=100 to 1820, y=840 to 956)
    bar_y = 840
    bar_h = 116
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    col_w = 1720 // 4
    specs = [
        ("PROJECT ROLE", "서비스 기획 100% · UI/UX 디자인 100%", "소상공인 리서치 · 문제 정의 · IA 정보 설계 · 와이어프레임 · UI 디자인 총괄"),
        ("PERIOD & TIMELINE", "2026.08 - 현재 (v1.0 프로덕션 운영)", "1인 학원·스튜디오 현장 인터뷰 기반 설계 및 실기기 검증 후 지속 고도화"),
        ("DESIGN SYSTEM", "Enterprise Trust 토큰 · 컴포넌트 규격", "8pt 베이스라인 · 브랜드 일렉트릭 블루(#0052FF) · 라이트 테마 고대비 12.8:1"),
        ("DELIVERY & RELEASE", "Android 상용 출시 & 60fps 웹 프로토타입", "SQLite ACID 온디바이스 볼트 탑재 · 실제 뷰포트 인터랙티브 허브 완성")
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
'''

p_start = text.find('def make_slide_01():')
p_end = text.find('# ==============================================================\n# SLIDE 02:', p_start)
updated = text[:p_start] + new_slide_01 + '\n\n' + text[p_end:]

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(updated)

print('Updated deck_slides_white_01_04.py successfully!')
