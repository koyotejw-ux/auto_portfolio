import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from deck_common import (
    W, H, BASE_DIR, CORE_DIR, QI_DIR, OUT_DIR,
    AIA_RED, AIA_RED_DARK, AIA_RED_LIGHT, AIA_RED_BORDER,
    BG_DARK, CARD_DARK, BORDER_DARK, TEXT_DARK_MAIN, TEXT_DARK_SUB,
    BG_LIGHT, CARD_LIGHT, BORDER_LIGHT, BORDER_LIGHT_ACCENT,
    TEXT_LIGHT_MAIN, TEXT_LIGHT_SUB,
    get_font, get_num_font, wrap_text, draw_pill_badge, draw_arrow,
    draw_slide_header, draw_slide_footer, draw_phone_mockup
)

# -------------------------------------------------------------
# SLIDE 01: HERO COVER (AIA+ SENIOR MODE - REAL HERO SCREEN)
# -------------------------------------------------------------
def make_slide_01():
    img = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([800, 100, 1800, 1000], fill=(211, 17, 69, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    img.paste(glow, (0, 0), glow)
    
    draw = ImageDraw.Draw(img)
    
    draw_pill_badge(draw, left_x=120, cy=105, text="AIA LIFE · SENIOR ACCESSIBILITY INNOVATION", font=get_font(11, 'bold'), theme='red', pad_x=14, height=28)
    draw_pill_badge(draw, left_x=440, cy=105, text="Qi DESIGN SYSTEM v3.3", font=get_font(11, 'bold'), theme='gray', pad_x=12, height=28)
    
    draw.text((120, 155), "AIA+", font=get_font(60, 'black'), fill=(15, 23, 42))
    draw.text((275, 155), "SENIOR MODE", font=get_font(60, 'black'), fill=AIA_RED)
    draw.text((120, 235), "고령자 친화 배리어프리 금융 UX & 10대 비대면 서비스 리뉴얼", font=get_font(26, 'bold'), fill=(51, 65, 85))
    
    desc_kr = (
        "금융위원회 '고령자 친화적 모바일 금융앱 가이드라인' 100% 완벽 준수\n"
        "6070 액티브 시니어를 위한 제로-뎁스(Zero-Depth) 직관 탐색 아키텍처와\n"
        "Qi 글로벌 디자인 시스템 v3.3 기반의 단일 소스 멀티 테마 프로덕트 디자인"
    )
    draw.text((120, 295), desc_kr, font=get_font(15.5, 'regular'), fill=(100, 116, 139), spacing=8)
    
    draw.text((120, 400), "AIA+ 고령자 모드 5대 핵심 서비스 (Overview)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    spheres = [
        ("조회", "계약/납입액 확인", (59, 130, 246)),
        ("납입", "보험료 바로 내기", AIA_RED),
        ("청구", "병원비 서류 접수", (168, 85, 247)),
        ("대출", "환급금 계약대출", (16, 185, 129)),
        ("상담", "큰글씨 고객센터", (71, 85, 105))
    ]
    for idx, (s_name, s_sub, s_col) in enumerate(spheres):
        sx = 120 + idx * 125
        sy = 450
        draw.ellipse([sx, sy, sx + 95, sy + 95], fill=s_col)
        draw.text((sx + 47, sy + 38), s_name, font=get_font(18, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((sx + 47, sy + 62), s_sub, font=get_font(9.5, 'medium'), fill=(255, 255, 255), anchor='mm')
        
    stats = [
        ("100%", "금융위 규제 가이드라인 준수"),
        ("2x", "본문 및 버튼 폰트 크기 확대"),
        ("90%", "시니어 코어 과업 완수율 달성"),
        ("50%", "비대면 업무 소요 시간 단축")
    ]
    card_y = 610
    for idx, (val, label) in enumerate(stats):
        cx = 120 + (idx % 2) * 280
        cy = card_y + (idx // 2) * 110
        cw, ch = 265, 95
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((cx + 20, cy + 20), val, font=get_num_font(32, 'black'), fill=AIA_RED if idx==0 else (15, 23, 42))
        lines = wrap_text(label, get_font(11.5, 'medium'), cw - 40, draw)
        ly = cy + 56
        for line in lines:
            draw.text((cx + 20, ly), line, font=get_font(11.5, 'medium'), fill=TEXT_LIGHT_SUB)
            ly += 16
            
    spec_y = 855
    draw.rounded_rectangle([120, spec_y, 680, spec_y + 115], radius=14, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    specs = [
        ("프로젝트", "AIA생명 AIA+ Phase 2 고령자 모드 & 비대면 서비스 리뉴얼"),
        ("수행 역할", "메인화면(일반/고령자) & 전체 서비스 아키텍처/화면설계 100% 단독 총괄"),
        ("핵심 혁신", "일반모드 ↔ 고령자모드 원클릭 스위칭 & 금융위 가이드라인 완전 준수")
    ]
    for idx, (label, val) in enumerate(specs):
        sy = spec_y + 15 + idx * 31
        draw.text((140, sy), label, font=get_font(12, 'bold'), fill=AIA_RED)
        draw.text((225, sy), val, font=get_font(12, 'bold' if idx==1 else 'medium'), fill=(15, 23, 42))
        
    gen_screen = os.path.join(CORE_DIR, "screen_general_main_clean.png")
    if not os.path.exists(gen_screen):
        gen_screen = os.path.join(CORE_DIR, "screen_general_main.png")
    sen_screen = os.path.join(CORE_DIR, "screen_senior_main_hero.png")
    if not os.path.exists(sen_screen):
        sen_screen = os.path.join(CORE_DIR, "screen_senior_main_home.png")
    pay_screen = os.path.join(CORE_DIR, "screen_pay_list_senior.png")
    
    draw_phone_mockup(img, gen_screen, cx=930, cy=565, phone_w=280, phone_h=605, bezel=6, radius=32, show_toggle_badge="[일반모드] 메인화면")
    draw_phone_mockup(img, sen_screen, cx=1260, cy=530, phone_w=335, phone_h=715, bezel=7, radius=36, show_toggle_badge="[고령자모드] 원터치 홈 (총괄설계)")
    draw_phone_mockup(img, pay_screen, cx=1590, cy=565, phone_w=280, phone_h=605, bezel=6, radius=32, show_toggle_badge="[간편납부] 56dp CTA")
    
    draw_arrow(draw, (1075, 565), (1095, 565), col=AIA_RED, width=3, arrow_size=8)
    draw_pill_badge(draw, cx=1085, cy=535, text="1-Tap 전환", font=get_font(10, 'bold'), theme='red', solid=True, pad_x=8, height=20)
    
    draw_pill_badge(draw, cx=1260, cy=145, text="고령자 친화 제로-뎁스 원터치 홈 · 직접 기획 및 화면설계", font=get_font(12, 'bold'), theme='red', solid=True, pad_x=16, height=32)
    
    draw_slide_footer(draw, 1, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_01.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 02: PROBLEMS & RESEARCH (Full 3-Tier Research Sheet)
# -------------------------------------------------------------
def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 2, 
        "PROBLEMS & RESEARCH", 
        "Problems & Research | ", 
        "보험앱 고령자 사용 실태 조사 및 데이터 분석", 
        "4대 핵심 문제점, 금융당국 지침 및 AIA 휴리스틱 평가, UX 논문 불편사항 파이차트, 클릭 로그 바 차트", 
        right_badge=("EMPIRICAL RESEARCH", "red")
    )
    
    problems = [
        {
            "num": "1",
            "title": "고령자 배려 부족",
            "desc": "각 보험사 및 금융사들이 '고령자 모드' 또는 '간편 모드'를 도입했지만, 글씨 크기와 화면 배치 차이가 미미하고 모드 전환 기능도 찾기 어려워 개선 필요."
        },
        {
            "num": "2",
            "title": "명칭/UI 혼란 초래",
            "desc": "금융사마다 서로 다른 명칭(KB·하나 '간편홈', 신한·우리 '쉬운홈')을 사용해 소비자가 쉽게 인식하지 못함. 직관적 통일성 확보 필요."
        },
        {
            "num": "3",
            "title": "접근성 낮은 UI 설계",
            "desc": "모드 전환 버튼이 앱 하단에 위치하거나 글씨가 작아 고령층이 사용하기 어려움. 엄지 터치 영역(Thumb Zone) 고려 가독성/접근성 개선 절실."
        },
        {
            "num": "4",
            "title": "지침 및 휴리스틱 고려",
            "desc": "금융감독원 권장 고령자 간편모드 지침(글자크기, 명도대비, 대체수단) 반영 및 AIA 글로벌 표준 휴리스틱 평가 체계 엄격 적용 필요."
        }
    ]
    
    t1_y = 215
    t1_w = 412
    t1_h = 220
    for i, p in enumerate(problems):
        px = 100 + i * (t1_w + 24)
        draw.rounded_rectangle([px, t1_y, px + t1_w, t1_y + t1_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([px + 20, t1_y + 18, px + 50, t1_y + 48], radius=6, fill=AIA_RED)
        draw.text((px + 35, t1_y + 33), p["num"], font=get_font(15, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((px + 62, t1_y + 33), p["title"], font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw.line([(px + 20, t1_y + 60), (px + t1_w - 20, t1_y + 60)], fill=BORDER_LIGHT, width=1)
        
        lines = wrap_text(p["desc"], get_font(12, 'regular'), t1_w - 40, draw)
        ly = t1_y + 75
        for line in lines:
            draw.text((px + 20, ly), line, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 20
            
    t2_y = 455
    t2_w = 848
    t2_h = 210
    
    lx = 100
    draw.rounded_rectangle([lx, t2_y, lx + t2_w, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=t2_y + 25, text="REGULATORY GUIDELINES", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=20)
    draw.text((lx + 25, t2_y + 58), "보험업권 모바일 금융앱 간편모드 지침 (금융감독원)", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    guideline_points = [
        ("화면 구성 단순화", "자주 쓰는 4대 핵심 업무(계약조회, 청구, 납입, 대출) 첫 화면 전면 배치"),
        ("가독성 및 대비 강화", "기본 본문 18pt 이상, 명도비 4.5:1 이상(AAA권장) 고대비 색상 설계"),
        ("쉬운 접근성 보장", "메인 화면 상단에서 1-Tap으로 즉시 전환 가능한 토글 스위치 배치"),
        ("대체 수단 제공", "비밀번호 분실 등 비상 시 가상계좌 대체 발급 및 전담 상담사 연결")
    ]
    gy = t2_y + 92
    for g_title, g_desc in guideline_points:
        draw.text((lx + 25, gy), "•", font=get_font(11, 'bold'), fill=(59, 130, 246))
        draw.text((lx + 40, gy), g_title + " :", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((lx + 185, gy), g_desc, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
        gy += 27
        
    rx = 972
    draw.rounded_rectangle([rx, t2_y, rx + t2_w, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=t2_y + 25, text="AIA HEURISTICS AUDIT", font=get_font(10, 'bold'), theme='red', pad_x=10, height=20)
    draw.text((rx + 25, t2_y + 58), "AIA 글로벌 표준 휴리스틱 평가 항목 (Qi v3.3)", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    heuristic_points = [
        ("인지 마찰 최소화 (Zero-Depth)", "화면당 1개 과업만 제시하여 고령층의 정보 과부하 방지"),
        ("인체공학 터치 (Thumb Zone)", "하단 56dp 풀와이드 CTA 버튼 및 최소 48dp 터치 타깃 보장"),
        ("시각/촉각 완료 피드백", "성공 완료 시 굵은 녹색 체크마크, 햅틱 진동 및 카카오 알림톡 전송"),
        ("안심 에러 케어 (Error Recovery)", "오입력 시 붉은색 안내문구 대신 쉬운 설명 및 되돌리기 제공")
    ]
    hy = t2_y + 92
    for h_title, h_desc in heuristic_points:
        draw.text((rx + 25, hy), "•", font=get_font(11, 'bold'), fill=AIA_RED)
        draw.text((rx + 40, hy), h_title + " :", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((rx + 245, hy), h_desc, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
        hy += 27
        
    t3_y = 685
    t3_w = 848
    t3_h = 265
    
    draw.rounded_rectangle([lx, t3_y, lx + t3_w, t3_y + t3_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw.text((lx + 25, t3_y + 20), "보험 앱 사용 불편사항", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + t3_w - 25, t3_y + 24), "(출처 : UX 논문 고령자 앱 사용 조사)", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='ra')
    
    pie_cx, pie_cy, pie_r = lx + 160, t3_y + 145, 95
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=0, end=115, fill=(239, 68, 68))
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=115, end=216, fill=(59, 130, 246))
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=216, end=295, fill=(14, 165, 233))
    draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r], start=295, end=360, fill=(71, 85, 105))
    draw.ellipse([pie_cx - 40, pie_cy - 40, pie_cx + 40, pie_cy + 40], fill=CARD_LIGHT)
    draw.text((pie_cx, pie_cy), "불편요인", font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    legends = [
        ("글자가 작아 잘 안 보임", "32%", (239, 68, 68)),
        ("보험금 청구 경로 어려움", "28%", (59, 130, 246)),
        ("버튼 터치 실수 많음 (오터치)", "22%", (14, 165, 233)),
        ("메뉴가 너무 복잡함 (뎁스)", "18%", (71, 85, 105))
    ]
    leg_y = t3_y + 68
    for l_title, l_pct, l_col in legends:
        draw.rounded_rectangle([lx + 320, leg_y + 3, lx + 336, leg_y + 19], radius=3, fill=l_col)
        draw.text((lx + 350, leg_y + 2), l_title, font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((lx + t3_w - 40, leg_y + 2), l_pct, font=get_num_font(14, 'bold'), fill=l_col, anchor='ra')
        leg_y += 42
        
    draw.rounded_rectangle([rx, t3_y, rx + t3_w, t3_y + t3_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw.text((rx + 25, t3_y + 20), "클릭 로그 기반 주요 기능별 클릭 비율(%)", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((rx + t3_w - 25, t3_y + 24), "(출처 : AIA 생명 로그 분석)", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='ra')
    
    click_data = [
        ("계약조회", 37.8, (99, 102, 241)),
        ("보험금 청구", 26.8, (99, 102, 241)),
        ("보험계약대출", 12.2, (129, 140, 248)),
        ("보험료 납입", 12.2, (129, 140, 248)),
        ("납입관리", 6.8, (165, 180, 252)),
        ("개인정보변경", 4.2, (199, 210, 254))
    ]
    
    bar_start_y = t3_y + 65
    max_w = 480
    for b_label, b_pct, b_col in click_data:
        draw.text((rx + 30, bar_start_y + 2), b_label, font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN)
        bar_len = int(max_w * (b_pct / 40.0))
        draw.rounded_rectangle([rx + 140, bar_start_y + 4, rx + 140 + bar_len, bar_start_y + 18], radius=6, fill=b_col)
        draw.text((rx + 155 + bar_len, bar_start_y), f"{b_pct}%", font=get_num_font(12, 'bold'), fill=(79, 70, 229) if b_pct > 20 else TEXT_LIGHT_SUB)
        bar_start_y += 31
        
    draw_slide_footer(draw, 2, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_02.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 03: COMPETITOR BENCHMARK (Focused Core Matrix & Strategic Insights)
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 3, 
        "COMPETITOR BENCHMARK ANALYSIS", 
        "Competitor Analysis | ", 
        "7대 생·손보사 고령자 모드 핵심 벤치마크 및 전략적 차별화", 
        "업계 실태 비교 매트릭스(명칭/레이아웃/색상대비/UX라이팅)와 AIA+ Phase 2의 4대 차별화 핵심 전략", 
        right_badge=("KEY BENCHMARK", "red")
    )
    
    card_y = 220
    card_h = 730
    
    lx = 100
    lw = 1040
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="7대 보험사 고령자 모드 지원 현황 핵심 매트릭스", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 68), "주요 보험사 간편모드 기능별 지원 수준 비교", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    cols = ["비교 항목", "A 생명", "B 생명", "C 화재", "D 손보", "E 손보", "F 화재", "G 라이프", "AIA+ (TO-BE)"]
    col_w = [170, 95, 95, 95, 95, 95, 95, 95, 145]
    col_x = [lx + 25]
    for w in col_w[:-1]:
        col_x.append(col_x[-1] + w)
        
    th_y = card_y + 115
    draw.rounded_rectangle([col_x[0], th_y, col_x[-1] + col_w[-1], th_y + 44], radius=8, fill=(30, 41, 59))
    for i, col in enumerate(cols):
        draw.text((col_x[i] + col_w[i]//2, th_y + 22), col, font=get_font(11.5, 'bold'), fill=(255, 255, 255) if i<8 else (255, 220, 230), anchor='mm')
        
    t1_rows = [
        ("고령자 모드 명칭", "간편홈", "간편모드", "큰글씨", "편한", "간편", "쉬운", "간편홈", "간편홈 (표준화)"),
        ("메인 전용 간편 구성", "O", "O", "O", "O", "O", "O", "O", "O (원터치 게이트)"),
        ("전용 레이아웃 분기", "O", "O", "O", "O", "O", "O", "O", "O (독립 화면 분기)"),
        ("전용 텍스트 크기 확대", "O", "△", "O", "O", "O", "O", "O", "O (18~28pt 2배)"),
        ("전용 터치 버튼 확대", "O", "O", "O", "O", "O", "O", "O", "O (56dp 풀와이드)"),
        ("전용 색상대비 (AAA)", "X", "X", "X", "X", "X", "X", "X", "O (WCAG 7:1)"),
        ("전용 버튼 UX라이팅", "X", "X", "X", "X", "X", "X", "X", "O (쉬운 명확 용어)"),
        ("전용 아이콘 메뉴 레이블", "O", "X", "X", "X", "X", "X", "X", "O (아이콘+텍스트)")
    ]
    
    r_y = th_y + 48
    for r_idx, row in enumerate(t1_rows):
        is_highlight = "색상대비" in row[0] or "UX라이팅" in row[0]
        bg_col = (255, 241, 244) if is_highlight else ((255, 255, 255) if r_idx % 2 == 0 else (248, 250, 252))
        draw.rectangle([col_x[0], r_y, col_x[-1] + col_w[-1], r_y + 48], fill=bg_col)
        draw.line([(col_x[0], r_y + 48), (col_x[-1] + col_w[-1], r_y + 48)], fill=BORDER_LIGHT, width=1)
        
        for c_idx, val in enumerate(row):
            txt_col = TEXT_LIGHT_MAIN
            if val == "O" or "O (" in val:
                txt_col = (5, 150, 105)
            elif val == "X":
                txt_col = (220, 38, 38)
            elif val == "△":
                txt_col = (217, 119, 6)
            if c_idx == 8:
                txt_col = AIA_RED
            draw.text((col_x[c_idx] + col_w[c_idx]//2, r_y + 24), val, font=get_font(11.5, 'bold' if c_idx==8 or is_highlight else 'medium'), fill=txt_col, anchor='mm')
        r_y += 50
        
    draw.rounded_rectangle([col_x[0], card_y + card_h - 110, col_x[-1] + col_w[-1], card_y + card_h - 25], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((col_x[0] + 20, card_y + card_h - 90), "🔍 벤치마크 진단 결론", font=get_font(12, 'bold'), fill=AIA_RED)
    draw.text((col_x[0] + 20, card_y + card_h - 65), "타 보험사는 명칭 난립 및 단순 크기 확대에 머물러 실질적 배리어프리(색상대비 AAA, UX라이팅)가 전무함.", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
    draw.text((col_x[0] + 20, card_y + card_h - 43), "AIA+는 '단일 앱 내 완전 분기 + WCAG AAA 인증 + 쉬운 우리말 라이팅'으로 업계 최고 수준 사용성을 확립.", font=get_font(11.5, 'bold'), fill=(5, 150, 105))
    
    rx = 1180
    rw = 640
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=card_y + 35, text="CORE DIFFERENTIATORS", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 25, card_y + 68), "AIA+만의 4대 핵심 차별화 전략", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    strategies = [
        {
            "tag": "STRATEGY 01",
            "title": "명칭 표준화 & 직관적 모드 전환",
            "desc": "난립하던 '쉬운홈/편한모드' 대신 직관적인 [간편홈] 명칭을 정립하고, 메인 상단 1-Tap 토글 스위치로 진입 장벽을 완전히 허물었습니다."
        },
        {
            "tag": "STRATEGY 02",
            "title": "업계 최초 WCAG AAA 명도대비 준수",
            "desc": "타사 전원이 미흡했던 색상 대비를 7:1 이상의 고대비 팔레트(AIA Red & Deep Navy)로 전면 개편하여 시각 저하 고령자의 식별성을 극대화했습니다."
        },
        {
            "tag": "STRATEGY 03",
            "title": "고령층 친화 쉬운 UX라이팅",
            "desc": "어려운 한자어 보험 용어 대신 '보험료 바로 내기', '병원비 서류 접수' 등 일상 언어로 100% 전환하여 읽는 즉시 이해하도록 설계했습니다."
        },
        {
            "tag": "STRATEGY 04",
            "title": "실명 클릭 로그 기반 5대 핵심 메뉴 배치",
            "desc": "단순 나열이 아닌 실제 클릭 로그 1·2위인 계약조회(37.8%)와 청구(26.8%)를 첫 화면에 즉시 노출하는 제로-뎁스 아키텍처를 완성했습니다."
        }
    ]
    
    sy = card_y + 115
    for s in strategies:
        draw.rounded_rectangle([rx + 20, sy, rx + rw - 20, sy + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=rx + 35, cy=sy + 22, text=s["tag"], font=get_font(10, 'bold'), theme='red' if '02' in s["tag"] or '04' in s["tag"] else 'blue', pad_x=8, height=20)
        draw.text((rx + 130, sy + 22), s["title"], font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        lines = wrap_text(s["desc"], get_font(11.5, 'regular'), rw - 70, draw)
        ly = sy + 48
        for line in lines:
            draw.text((rx + 35, ly), line, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 18
        sy += 144
        
    draw_slide_footer(draw, 3, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_03.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 04: INFORMATION ARCHITECTURE & USER FLOW (Refactored Core Layout)
# -------------------------------------------------------------
def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 4, 
        "INFORMATION ARCHITECTURE & USER FLOW", 
        "Information Architecture | ", 
        "제로-뎁스(Zero-Depth) 정보 구조도 및 사용자 여정", 
        "클릭 로그 분석 기반 원터치 5대 핵심 비대면 과업 구조와 제로-뎁스 설계 원칙", 
        right_badge=("CORE ARCHITECTURE", "red")
    )
    
    card_y = 220
    card_h = 730
    
    # Left Column: Information Architecture Tree (W=1040)
    lx = 100
    lw = 1040
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="DUAL-MODE INFORMATION ARCHITECTURE", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 68), "단일 앱 내 이원화 모드 구조 및 5대 핵심 과업", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Root Node
    root_x, root_y, root_w, root_h = lx + (lw - 340)//2, card_y + 115, 340, 60
    draw.rounded_rectangle([root_x, root_y, root_x + root_w, root_y + root_h], radius=12, fill=AIA_RED, outline=AIA_RED_BORDER, width=2)
    draw.text((root_x + root_w//2, root_y + 20), "AIA+ 모바일 통합 플랫폼", font=get_font(15, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((root_x + root_w//2, root_y + 42), "단일 소스 멀티 테마 (Single Codebase)", font=get_font(11, 'medium'), fill=AIA_RED_LIGHT, anchor='mm')
    
    # Branch lines
    draw.line([(root_x + root_w//2, root_y + root_h), (root_x + root_w//2, card_y + 215)], fill=BORDER_LIGHT, width=2)
    draw.line([(lx + 150, card_y + 215), (lx + lw - 150, card_y + 215)], fill=BORDER_LIGHT, width=2)
    
    # Mode 1: General Mode (Left)
    g_x, g_y, g_w, g_h = lx + 40, card_y + 240, 280, 75
    draw.rounded_rectangle([g_x, g_y, g_x + g_w, g_y + g_h], radius=12, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.line([(lx + 150, card_y + 215), (lx + 150, g_y)], fill=BORDER_LIGHT, width=2)
    draw_pill_badge(draw, cx=g_x + g_w//2, cy=g_y + 22, text="DEFAULT MODE", font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
    draw.text((g_x + g_w//2, g_y + 50), "일반 사용자 모드 (종합 메뉴)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    # Mode 2: Senior Mode (Right - Focus)
    s_x, s_y, s_w, s_h = lx + 360, card_y + 240, 640, 75
    draw.rounded_rectangle([s_x, s_y, s_x + s_w, s_y + s_h], radius=12, fill=(255, 241, 244), outline=AIA_RED, width=2)
    draw.line([(lx + lw - 150, card_y + 215), (lx + lw - 150, s_y)], fill=AIA_RED, width=2)
    draw_pill_badge(draw, cx=s_x + s_w//2, cy=s_y + 22, text="SENIOR MODE (PHASE 2 RENEWAL)", font=get_font(10, 'bold'), theme='red', pad_x=12, height=20)
    draw.text((s_x + s_w//2, s_y + 50), "고령자 친화 모드 (제로-뎁스 5대 핵심 업무 집중)", font=get_font(14, 'bold'), fill=AIA_RED, anchor='mm')
    
    # 1-Tap Toggle Indicator between modes
    draw_arrow(draw, (g_x + g_w, g_y + g_h//2), (s_x, s_y + s_h//2), col=AIA_RED, width=2, arrow_size=6)
    draw_pill_badge(draw, cx=(g_x + g_w + s_x)//2, cy=g_y + g_h//2 - 14, text="1-Tap 토글", font=get_font(9, 'bold'), theme='red', solid=True, pad_x=6, height=18)
    
    # 5 Sub-Nodes under Senior Mode
    draw.line([(s_x + s_w//2, s_y + s_h), (s_x + s_w//2, card_y + 365)], fill=AIA_RED, width=2)
    draw.line([(lx + 40, card_y + 365), (lx + lw - 40, card_y + 365)], fill=AIA_RED, width=2)
    
    senior_tasks = [
        ("01. 계약 조회", "보유 계약 목록\n수익률 큰글씨\n로그 37.8% (1위)", (59, 130, 246)),
        ("02. 보험금 청구", "영수증 OCR 촬영\n수기입력 0건\n로그 26.8% (2위)", (168, 85, 247)),
        ("03. 보험료 납입", "당월 미납금 원터치\n주거래 계좌 연동\n로그 12.2% (3위)", AIA_RED),
        ("04. 계약 대출", "대출 가능 한도조회\n즉시 이체 신청\n로그 12.2% (공동3위)", (16, 185, 129)),
        ("05. 고객 상담", "전담 상담사 원클릭\n고객센터 전화연결\n자주묻는질문 지원", (71, 85, 105))
    ]
    
    tw = 180
    th = 190
    for idx, (ttitle, titems, tcol) in enumerate(senior_tasks):
        tx = lx + 40 + idx * 195
        ty = card_y + 395
        draw.line([(tx + tw//2, card_y + 365), (tx + tw//2, ty)], fill=AIA_RED, width=2)
        draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=12, fill=(255, 255, 255), outline=tcol, width=2 if idx==2 else 1)
        draw.rounded_rectangle([tx + 8, ty + 10, tx + tw - 8, ty + 36], radius=6, fill=tcol)
        draw.text((tx + tw//2, ty + 23), ttitle, font=get_font(11.5, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        ilines = titems.split('\n')
        iy = ty + 52
        for line in ilines:
            is_stat = "로그" in line
            draw.text((tx + 12, iy), "•" if not is_stat else "★", font=get_font(10, 'bold'), fill=tcol if not is_stat else AIA_RED)
            draw.text((tx + 24, iy), line, font=get_font(10.5, 'bold' if is_stat else 'regular'), fill=AIA_RED if is_stat else TEXT_LIGHT_MAIN)
            iy += 40
            
    # Bottom Architecture Summary Note
    draw.rounded_rectangle([lx + 40, card_y + card_h - 105, lx + lw - 40, card_y + card_h - 25], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((lx + 60, card_y + card_h - 85), "💡 제로-뎁스(Zero-Depth) 아키텍처 구축 논리", font=get_font(12, 'bold'), fill=AIA_RED)
    draw.text((lx + 60, card_y + card_h - 60), "실제 고령 고객의 전체 모바일 트래픽 89%를 차지하는 4대 업무를 메인 첫 화면에 전면 배치하여,", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 60, card_y + card_h - 40), "메뉴를 찾아 헤매는 인지 피로도를 원천 차단하고 1-Tap 즉시 과업 완수를 달성했습니다.", font=get_font(11.5, 'bold'), fill=(5, 150, 105))
    
    # Right Column: 4 Core Design Principles (W=640)
    rx = 1180
    rw = 640
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=card_y + 35, text="ZERO-DEPTH PRINCIPLES", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 25, card_y + 68), "정보 구조 설계 4대 핵심 원칙", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    principles = [
        {
            "tag": "PRINCIPLE 01",
            "title": "단일 화면 1개 과업 (Single Task Focus)",
            "desc": "여러 단계의 복잡한 뎁스를 완전히 제거하고, 화면 전환 시마다 오직 1개의 명확한 질문과 액션만 제시하여 고령층 인지 과부하를 방지합니다."
        },
        {
            "tag": "PRINCIPLE 02",
            "title": "엄지 터치 영역 최적화 (Thumb Zone)",
            "desc": "모든 핵심 의사결정 CTA 버튼은 하단 56dp 풀와이드로 고정하여, 스마트폰을 한 손 또는 양손으로 쥐었을 때 가장 누르기 편한 영역에 배치했습니다."
        },
        {
            "tag": "PRINCIPLE 03",
            "title": "오입력 최소화 자동 채움 (Smart Prefill)",
            "desc": "증권번호 수기 입력을 완전히 배제하고, 기등록 주거래 계좌와 환급금 계좌를 자동 불러와 터치 1번으로 서식을 완료하도록 설계했습니다."
        },
        {
            "tag": "PRINCIPLE 04",
            "title": "안심 브릿지 연동 (Multi-Channel Care)",
            "desc": "모바일 조작 중 어려움이 발생하면 즉시 1-Tap 전담 상담사 전화로 연결되며, 처리 완료 시 카카오 알림톡으로 실시간 안심 영수증을 발송합니다."
        }
    ]
    
    py = card_y + 115
    for p in principles:
        draw.rounded_rectangle([rx + 20, py, rx + rw - 20, py + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=rx + 35, cy=py + 22, text=p["tag"], font=get_font(10, 'bold'), theme='red' if '01' in p["tag"] or '03' in p["tag"] else 'blue', pad_x=8, height=20)
        draw.text((rx + 135, py + 22), p["title"], font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        lines = wrap_text(p["desc"], get_font(11.5, 'regular'), rw - 70, draw)
        ly = py + 48
        for line in lines:
            draw.text((rx + 35, ly), line, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly += 18
        py += 144
        
    draw_slide_footer(draw, 4, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_04.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
