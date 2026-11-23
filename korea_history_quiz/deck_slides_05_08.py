import os
from PIL import Image, ImageDraw, ImageFilter
from build_history_common import (
    W, H, MOCKUP_DIR, get_font, get_num_font, wrap_text_by_words,
    draw_pill_badge, create_base_canvas, draw_slide_header, draw_slide_footer, save_slide,
    C_TITLE_WHITE, C_RED_HERO, C_RED_MUTED, C_GOLD_ACC, C_INDIGO_ACC, C_TEXT_BODY, C_TEXT_MUTED,
    C_GREEN_ACC, C_BORDER_RED, C_BG_CARD, C_BG_CONTAINER
)

def make_shadow(im, radius=28, alpha=150):
    sh = Image.new('RGBA', (im.width + 56, im.height + 56), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([28, 28, 28 + im.width, 28 + im.height], radius=40, fill=(0, 0, 0, alpha))
    return sh.filter(ImageFilter.GaussianBlur(radius))

# -------------------------------------------------------------
# SLIDE 05: USER FLOW & INTERACTION LOGIC
# -------------------------------------------------------------
def make_slide_05():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 5, "핵심 학습 여정 및 실전 인터랙션 플로우",
                      "모의고사 응시부터 오답 분석, 1:1 사료 해설까지 단절 없는 인터랙티브 루프를 구현했습니다.")
    
    steps = [
        ("01", "시험 모드 선택", "실전 풀모의고사 / 10문항 숏폼 / 취약 시대 중 목적에 맞는 학습 선택", "red"),
        ("02", "문제 풀이 & 사료 판독", "고해상도 유물·사료 사진 핀치 줌 & 50:50 소거 찬스로 능동적 풀이", "gold"),
        ("03", "즉시 채점 & 정밀 분석", "정답/오답 실시간 판정 및 문항별 핵심 키워드 단서와 상세 해설 제시", "green"),
        ("04", "오답 볼트 자동 축적", "틀린 문제만 추출하여 취약 시대 재응시 및 오답 탈출 리워드 제공", "red")
    ]
    step_w = 370
    step_h = 360
    step_y = 230
    for idx, (num, stitle, sdesc, stheme) in enumerate(steps):
        sx = 100 + idx * (step_w + 30)
        draw.rounded_rectangle([sx, step_y, sx + step_w, step_y + step_h], radius=18, fill=C_BG_CARD, outline=C_BORDER_RED if stheme == 'red' else (245, 158, 11, 100), width=1)
        draw.text((sx + 24, step_y + 24), num, font=get_num_font(42, 'black'), fill=C_RED_HERO if stheme == 'red' else C_GOLD_ACC)
        draw.text((sx + 24, step_y + 90), stitle, font=get_font(18, 'bold'), fill=C_TITLE_WHITE)
        lines = wrap_text_by_words(sdesc, get_font(13.5, 'regular'), step_w - 48, draw)
        for l_idx, l in enumerate(lines):
            draw.text((sx + 24, step_y + 135 + l_idx * 24), l, font=get_font(13.5, 'regular'), fill=C_TEXT_BODY)
            
        # Arrow connector between cards
        if idx < 3:
            arrow_x = sx + step_w + 8
            arrow_y = step_y + step_h // 2
            draw.text((arrow_x, arrow_y - 14), "➔", font=get_font(20, 'bold'), fill=C_GOLD_ACC)

    # Bottom Interaction Principles Pod
    bot_y = 630
    bot_w = 1570
    bot_h = 350
    draw.rounded_rectangle([100, bot_y, 100 + bot_w, bot_y + bot_h], radius=20, fill=C_BG_CARD, outline=(255, 255, 255, 20), width=1)
    draw.text((130, bot_y + 28), "인체공학적 터치 & 게이미피케이션 UX 설계 원칙", font=get_font(14, 'bold'), fill=C_RED_HERO)
    
    rules = [
        ("01. 원핸드(One-Hand) 하단 터치 영역", "1080p 대화면 스마트폰에서도 엄지손가락 하나로 보기 1~5번 선택과 다음 문제 이동이 가능하도록 컨트롤 패널을 하단 35%에 집중 배치"),
        ("02. 시각 피로도를 낮춘 다크 앰비언트", "장시간 50문항 시험 시 눈의 피로를 최소화하는 조선 묵향 딥 네이비(Navy Dark)와 선명한 크림슨 레드 하이라이트"),
        ("03. 햅틱 피드백 & 오답 사운드 엔진", "정답 맞춤 시 경쾌한 징 소리와 햅틱 진동, 오답 시 즉각적인 둔탁 햅틱 피드백으로 감각적 학습 각인 효과 극대화")
    ]
    for r_idx, (rtitle, rdesc) in enumerate(rules):
        ry = bot_y + 70 + r_idx * 84
        draw.rounded_rectangle([130, ry, 130 + bot_w - 60, ry + 70], radius=12, fill=C_BG_CONTAINER, outline=(255, 255, 255, 10), width=1)
        draw.text((150, ry + 16), rtitle, font=get_font(14, 'bold'), fill=C_GOLD_ACC)
        draw.text((150, ry + 40), rdesc, font=get_font(12.5, 'regular'), fill=C_TEXT_BODY)
        
    draw_slide_footer(draw, meta_tags="USER FLOW & UX LOGIC · 05/12")
    save_slide(base, 5)

# -------------------------------------------------------------
# SLIDE 06: CORE SCREEN 1 - HOME DASHBOARD
# -------------------------------------------------------------
def make_slide_06():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 6, "CORE SCREEN 01 · 스마트 학습 홈 대시보드",
                      "출석 스트릭, 일일 미션, 6대 시대별 마스터리 레이더를 한눈에 파악하는 중앙 관제 센터입니다.")
    
    # Left Content Pod
    lx = 100
    ly = 240
    lw = 840
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=20, fill=C_BG_CARD, outline=C_BORDER_RED, width=1)
    draw_pill_badge(draw, left_x=lx + 28, cy=ly + 38, text="UI/UX DEEP DIVE", font=get_font(11.5, 'bold'), theme='red', pad_x=12, height=26)
    draw.text((lx + 28, ly + 76), "학습 동기부여와 성취감을 극대화한 대시보드", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    
    features = [
        ("연속 출석 스트릭 (Streak Engine)", "매일 앱에 접속하여 퀴즈 1회 이상 풀이 시 불꽃 아이콘 스트릭이 유지되어 학습 습관을 자연스럽게 형성합니다."),
        ("6대 시대별 마스터리 게이지", "선사부터 현대까지 각 시대별 누적 정답률을 원형/바 프로그레스로 직관화하여 취약 파트를 즉시 판별합니다."),
        ("스마트 이어풀기 (Resume Engine)", "풀다가 중단한 회차의 잔여 문항과 타이머를 SQLite 로컬에 보존하여 원터치로 시험을 이어갑니다."),
        ("일일 엽전 리워드 & 찬스 충전", "매일 주어지는 퀘스트 완료 시 엽전 포인트를 획득하여 50:50 힌트 찬스를 잠금 해제할 수 있습니다.")
    ]
    fy = ly + 130
    for ftitle, fdesc in features:
        draw.rounded_rectangle([lx + 28, fy, lx + lw - 28, fy + 120], radius=14, fill=C_BG_CONTAINER, outline=(255, 255, 255, 12), width=1)
        draw.text((lx + 46, fy + 18), f"• {ftitle}", font=get_font(14, 'bold'), fill=C_GOLD_ACC)
        lines = wrap_text_by_words(fdesc, get_font(13, 'regular'), lw - 90, draw)
        for l_idx, l in enumerate(lines):
            draw.text((lx + 46, fy + 48 + l_idx * 22), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
        fy += 140

    # Right Phone Mockup
    phone_path = os.path.join(MOCKUP_DIR, 'mockup_01_home.png')
    if os.path.exists(phone_path):
        p = Image.open(phone_path).convert('RGBA')
        scale = 0.54
        pw, ph = int(p.width * scale), int(p.height * scale)
        p_scaled = p.resize((pw, ph), Image.Resampling.LANCZOS)
        sh = make_shadow(p_scaled, radius=36, alpha=190)
        px = 1200
        py = 140
        base.paste(sh, (px - 28, py - 28), sh)
        base.paste(p_scaled, (px, py), p_scaled)
        
    draw_slide_footer(draw, meta_tags="HOME DASHBOARD ENGINE · 06/12")
    save_slide(base, 6)

# -------------------------------------------------------------
# SLIDE 07: CORE SCREEN 2 - EXAM CENTER & QUESTION SOLVING
# -------------------------------------------------------------
def make_slide_07():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 7, "CORE SCREEN 02 · 한능검 실전 기출 시험 센터",
                      "실제 시험과 100% 동일한 50문항 80분 타이머와 고해상도 사료 이미지 분석 엔진을 제공합니다.")
    
    # Left Content Pod
    lx = 100
    ly = 240
    lw = 840
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=20, fill=C_BG_CARD, outline=C_BORDER_RED, width=1)
    draw_pill_badge(draw, left_x=lx + 28, cy=ly + 38, text="EXAM ENGINE", font=get_font(11.5, 'bold'), theme='gold', pad_x=12, height=26)
    draw.text((lx + 28, ly + 76), "실전 몰입도를 높이는 시험장 맞춤형 UI", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    
    features = [
        ("회차별 실전 모의고사 (50문항/80분)", "최신 77회 한능검 심화 기출을 실제 시험지 배열과 동일하게 재현하여 실전 감각을 극대화합니다."),
        ("10문항 랜덤 숏폼 테스트", "시간이 부족한 직장인 및 통학생을 위해 핵심 기출 10문항을 무작위 추출하여 15분 만에 집중 풀이합니다."),
        ("사료 핀치 줌 & 풀스크린 뷰어", "복잡한 비문, 지도, 금동대향로 등 유물 디테일을 고화질로 줌인하여 문제 해결 단서를 직관적으로 포착합니다."),
        ("50:50 소거 찬스 & 오답 탈락 연출", "헷갈리는 오답 보기 2개를 즉시 지워주는 게이미피케이션 찬스로 시험 불안감을 완화합니다.")
    ]
    fy = ly + 130
    for ftitle, fdesc in features:
        draw.rounded_rectangle([lx + 28, fy, lx + lw - 28, fy + 120], radius=14, fill=C_BG_CONTAINER, outline=(255, 255, 255, 12), width=1)
        draw.text((lx + 46, fy + 18), f"• {ftitle}", font=get_font(14, 'bold'), fill=C_RED_HERO)
        lines = wrap_text_by_words(fdesc, get_font(13, 'regular'), lw - 90, draw)
        for l_idx, l in enumerate(lines):
            draw.text((lx + 46, fy + 48 + l_idx * 22), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
        fy += 140

    # Right Phone Mockup (Exam Center)
    phone_path = os.path.join(MOCKUP_DIR, 'mockup_02_exam.png')
    if os.path.exists(phone_path):
        p = Image.open(phone_path).convert('RGBA')
        scale = 0.54
        pw, ph = int(p.width * scale), int(p.height * scale)
        p_scaled = p.resize((pw, ph), Image.Resampling.LANCZOS)
        sh = make_shadow(p_scaled, radius=36, alpha=190)
        px = 1200
        py = 140
        base.paste(sh, (px - 28, py - 28), sh)
        base.paste(p_scaled, (px, py), p_scaled)
        
    draw_slide_footer(draw, meta_tags="EXAM CENTER ARCHITECTURE · 07/12")
    save_slide(base, 7)

# -------------------------------------------------------------
# SLIDE 08: CORE SCREEN 3 - QUIZ COMMENTARY & CLUE REVEAL
# -------------------------------------------------------------
def make_slide_08():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 8, "CORE SCREEN 03 · 정답 해설 및 사료 단서 식별 엔진",
                      "정답 유무 표시를 넘어 사료 속 핵심 키워드 형광펜 하이라이트와 보기별 상세 해설을 제공합니다.")
    
    # Left Content Pod
    lx = 100
    ly = 240
    lw = 840
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=20, fill=C_BG_CARD, outline=C_BORDER_RED, width=1)
    draw_pill_badge(draw, left_x=lx + 28, cy=ly + 38, text="COMMENTARY ENGINE", font=get_font(11.5, 'bold'), theme='green', pad_x=12, height=26)
    draw.text((lx + 28, ly + 76), "단순 암기를 입체적 이해로 바꾸는 해설 UX", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    
    features = [
        ("사료 키워드 옐로우 하이라이트", "문제 지문 중 정답을 도출하는 결정적 역사적 단서(왕명, 관직, 사건명)를 자동으로 하이라이팅하여 제시합니다."),
        ("오답 선지 1~5번 완전 분석", "정답 해설뿐만 아니라 왜 다른 보기가 틀렸는지 오답의 이유와 해당 시대적 배경을 상세히 주석 처리합니다."),
        ("동일 시대 연계 문항 추천", "틀린 문제와 동일한 역사적 주제(예: 삼국통일 과정)를 다룬 타 회차 기출 문항으로 즉시 연계 학습을 유도합니다."),
        ("원터치 오답 노트 북마크", "터치 한 번으로 즐겨찾기 또는 취약 볼트에 저장하여 언제든 나만의 맞춤 시험지로 재생성합니다.")
    ]
    fy = ly + 130
    for ftitle, fdesc in features:
        draw.rounded_rectangle([lx + 28, fy, lx + lw - 28, fy + 120], radius=14, fill=C_BG_CONTAINER, outline=(255, 255, 255, 12), width=1)
        draw.text((lx + 46, fy + 18), f"• {ftitle}", font=get_font(14, 'bold'), fill=C_GREEN_ACC)
        lines = wrap_text_by_words(fdesc, get_font(13, 'regular'), lw - 90, draw)
        for l_idx, l in enumerate(lines):
            draw.text((lx + 46, fy + 48 + l_idx * 22), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
        fy += 140

    # Right Phone Mockup (Quiz Screen)
    phone_path = os.path.join(MOCKUP_DIR, 'mockup_03_quiz.png')
    if os.path.exists(phone_path):
        p = Image.open(phone_path).convert('RGBA')
        scale = 0.54
        pw, ph = int(p.width * scale), int(p.height * scale)
        p_scaled = p.resize((pw, ph), Image.Resampling.LANCZOS)
        sh = make_shadow(p_scaled, radius=36, alpha=190)
        px = 1200
        py = 140
        base.paste(sh, (px - 28, py - 28), sh)
        base.paste(p_scaled, (px, py), p_scaled)
        
    draw_slide_footer(draw, meta_tags="COMMENTARY & CLUE SYSTEM · 08/12")
    save_slide(base, 8)

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
