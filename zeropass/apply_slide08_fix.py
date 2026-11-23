import os

script_path = r'd:\097.flutter_project\auto_portfolio\zeropass\deck_slides_white_05_08.py'
with open(script_path, 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('    card_y = 244\n    card_w = 548\n    card_h = 584')
idx2 = text.find('    tel_y = 832\n    tel_h = 142\n    draw.rounded_rectangle([lx, tel_y, lx + 1720, tel_y + tel_h]')

if idx1 == -1 or idx2 == -1:
    print('Failed to find indices:', idx1, idx2)
    exit(1)

new_block = '''    card_y = 236
    card_w = 548
    card_h = 604
    card_gap = 38
    start_x = 100

    kiosk_stages = [
        {
            "step": "STEP 01",
            "title": "대기 및 진입 (Standby Engine)",
            "sub": "원생 진입 감지 & 실시간 디지털 클록 연동",
            "img_path": "zeropass/assets/kiosk_mockups/real_tablet_kiosk_standby.png",
            "badge": "무인 대기 모드",
            "badge_theme": "slate",
            "chips": [
                ("옵시디언 다크 테마", "시인성 100% 최적화"),
                ("스튜디오 브랜드 연동", "실시간 시계 동기화"),
                ("10인치 태블릿 반응형", "가로/세로 오토 레이아웃")
            ],
            "interaction": "진입 대기: 4자리 입력 박스가 Clear 상태로 원생 터치 대기 (CPU 점유율 < 1%)"
        },
        {
            "step": "STEP 02",
            "title": "인체공학 터치 다이얼 (Dialing & Indexing)",
            "sub": "116dp 대형 텐키패드 & 10ms 고속 트리거",
            "img_path": "zeropass/assets/kiosk_mockups/real_tablet_kiosk_dial.png",
            "badge": "고속 햅틱 입력",
            "badge_theme": "blue",
            "chips": [
                ("116dp 대형 터치 그리드", "유아 오터치 원천 차단"),
                ("네온 글로우 햅틱 피드백", "입력 즉시 시각 반응"),
                ("인메모리 인덱스 매칭", "4자리 입력 시 즉각 검색")
            ],
            "interaction": "입력 파이프라인: 4자리 터치 완료 시 10ms 내 로컬 DB 원생 식별 트리거 가동"
        },
        {
            "step": "STEP 03",
            "title": "0.8초 완결 & 메인 동기화 (Sync Celebration)",
            "sub": "원생 식별 · 잔여 회차 즉시 차감 · 모바일 실시간 반영",
            "img_path": "zeropass/assets/kiosk_mockups/real_tablet_kiosk_success.png",
            "badge": "출결 및 차감 완결",
            "badge_theme": "emerald",
            "chips": [
                ("강지훈 원생 식별 및 차감", "잔여 1회 / 총 12회 차감"),
                ("학부모 알림톡 큐 자동 적립", "백그라운드 즉각 발송"),
                ("원장님 모바일 실시간 갱신", "헤더 출결 카운터 즉시 반영")
            ],
            "interaction": "상태 인터랙션: 태블릿 성공 완료 즉시 모바일 '출결 체크' 헤더 카운터 자동 갱신"
        }
    ]

    for idx, stage in enumerate(kiosk_stages):
        cx = start_x + idx * (card_w + card_gap)

        # Outer Card Container
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

        # Step Header Pill & Badge
        draw_pill_badge(draw, left_x=cx + 20, cy=card_y + 24, text=stage["step"], font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22)
        # Removed redundant top-right badge per user UX request

        draw.text((cx + 20, card_y + 44), stage["title"], font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 20, card_y + 65), stage["sub"], font=get_font(10, 'regular'), fill=(100, 116, 139))

        # Tablet Device Mockup Placement
        img_p = stage["img_path"]
        if os.path.exists(img_p):
            raw_screen = Image.open(img_p).convert('RGBA')

            if idx < 2:
                # Steps 1 & 2: Large Expanded Tablet Mockup (target_h=340)
                framed_tab = make_tablet_kiosk_frame(raw_screen, target_h=340)
                tab_x = cx + (card_w - framed_tab.width) // 2
                tab_y = card_y + 80

                sh_tab, pad_tab = make_shadow(framed_tab, blur=24, offset=(10, 16), alpha=70)
                base.paste(sh_tab, (tab_x - pad_tab[0], tab_y - pad_tab[1]), sh_tab)
                base.paste(framed_tab, (tab_x, tab_y), framed_tab)

            else:
                # STEP 03: Dual Mockup (Tablet Kiosk Success + Real-Time Mobile "출결 체크" Sync Phone)
                framed_tab = make_tablet_kiosk_frame(raw_screen, target_h=340)
                tab_x = cx + 22
                tab_y = card_y + 80

                sh_tab, pad_tab = make_shadow(framed_tab, blur=22, offset=(8, 14), alpha=65)
                base.paste(sh_tab, (tab_x - pad_tab[0], tab_y - pad_tab[1]), sh_tab)
                base.paste(framed_tab, (tab_x, tab_y), framed_tab)

                # Mobile Phone Showing Real-Time Synced "출결 체크" Main Screen
                phone_p = 'zeropass/assets/iphone_mockups/clean_android_upright_mockup.png'
                if os.path.exists(phone_p):
                    phone_img = Image.open(phone_p).convert('RGBA')
                    p_scale = 300 / phone_img.height
                    pw_scaled = int(phone_img.width * p_scale)
                    phone_scaled = phone_img.resize((pw_scaled, 300), Image.Resampling.LANCZOS)

                    px_pos = cx + card_w - pw_scaled - 20
                    py_pos = card_y + 138

                    sh_phone, pad_ph = make_shadow(phone_scaled, blur=20, offset=(10, 16), alpha=85)
                    base.paste(sh_phone, (px_pos - pad_ph[0], py_pos - pad_ph[1]), sh_phone)
                    base.paste(phone_scaled, (px_pos, py_pos), phone_scaled)

                    # Floating Real-Time Sync Indicator Pill on Phone
                    pill_w = 142
                    pill_h = 24
                    pill_x = px_pos + (pw_scaled - pill_w) // 2
                    pill_y = py_pos - 12
                    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=12, fill=(0, 82, 255), outline=(255, 255, 255), width=2)
                    draw.text((pill_x + pill_w // 2, pill_y + 12), "⚡ 메인 즉시 동기화", font=get_font(8.5, 'bold'), fill=(255, 255, 255), anchor='mm')

        # 3 Structured Micro Feature Chips
        chip_y = card_y + 452
        chip_h = 26
        for c_idx, (c_label, c_sub) in enumerate(stage["chips"]):
            cy_pos = chip_y + c_idx * 32
            draw.rounded_rectangle([cx + 16, cy_pos, cx + card_w - 16, cy_pos + chip_h], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.ellipse([cx + 26, cy_pos + 10, cx + 32, cy_pos + 16], fill=(0, 81, 255))
            draw.text((cx + 38, cy_pos + 13), c_label, font=get_font(9.5, 'bold'), fill=(30, 41, 59), anchor='lm')
            draw.text((cx + card_w - 26, cy_pos + 13), c_sub, font=get_font(8.5, 'medium'), fill=(0, 82, 255), anchor='rm')

        # Interactive Relationship Box
        rel_y = card_y + card_h - 44
        draw.rounded_rectangle([cx + 16, rel_y, cx + card_w - 16, rel_y + 32], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((cx + card_w // 2, rel_y + 16), stage["interaction"], font=get_font(8.5, 'bold'), fill=(0, 82, 255), anchor='mm')

    # Draw Inter-Stage Flow Arrows Between Step 1 -> Step 2 and Step 2 -> Step 3
    for a_idx in range(2):
        ax1 = start_x + (a_idx + 1) * card_w + a_idx * card_gap - 6
        ax2 = ax1 + 48
        ay = card_y + 250
        draw_arrow(draw, (ax1, ay), (ax2, ay), col=(0, 82, 255), width=2, arrow_size=6)
        draw.rounded_rectangle([ax1 + 8, ay - 14, ax2 - 8, ay + 14], radius=10, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
        draw.text((ax1 + 20, ay), "0.4s", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')

    # -------------------------------------------------------------
    # Bottom Horizontal KPI & Telemetry Performance Strip
    # -------------------------------------------------------------
'''

new_text = text[:idx1] + new_block + text[idx2:]
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Updated deck_slides_white_05_08.py successfully!')

