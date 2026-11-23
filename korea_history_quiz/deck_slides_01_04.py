import os
from PIL import Image, ImageDraw, ImageFilter
from build_history_common import (
    W, H, MOCKUP_DIR, get_font, get_num_font, wrap_text_by_words,
    draw_pill_badge, create_base_canvas, draw_slide_header, draw_slide_footer, save_slide,
    C_TITLE_WHITE, C_RED_HERO, C_RED_MUTED, C_GOLD_ACC, C_INDIGO_ACC, C_TEXT_BODY, C_TEXT_MUTED,
    C_GREEN_ACC, C_BORDER_RED, C_BG_CARD, C_BG_CONTAINER
)

ASSETS_DIR = 'd:/097.flutter_project/korea_history_quiz/assets'

def make_shadow(im, radius=32, alpha=170):
    sh = Image.new('RGBA', (im.width + 64, im.height + 64), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([32, 32, 32 + im.width, 32 + im.height], radius=44, fill=(0, 0, 0, alpha))
    return sh.filter(ImageFilter.GaussianBlur(radius))

# -------------------------------------------------------------
# SLIDE 01: HERO COVER (ULTRA-POLISHED)
# -------------------------------------------------------------
def make_slide_01():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    
    # Header Rule & Pills
    draw.line([(100, 52), (1820, 52)], fill=(239, 68, 68, 60), width=1)
    w_pill = draw_pill_badge(draw, left_x=100, cy=76, text="2026 EDUTECH ARCHITECTURE CASE STUDY", font=get_font(11.5, 'bold'), theme='red', pad_x=14, height=28)
    
    meta_txt = "한능검 심화 100% 실전 기출 · 6대 시대별 요약집 · 스마트 오답 볼트 · 1인 단독 기획·디자인"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 68), meta_txt, font=get_font(13.5, 'medium'), fill=C_TEXT_BODY)
    
    draw.text((100, 142), "KOREA HISTORY QUIZ · 대한한국사", font=get_font(14, 'bold'), fill=C_RED_HERO)
    
    title_p1 = "방대한 5,000년 역사 흐름을 "
    title_p2 = "한 손으로 압축 정복하다"
    w_p1 = draw.textlength(title_p1, font=get_font(52, 'black'))
    draw.text((100, 174), title_p1, font=get_font(52, 'black'), fill=C_TITLE_WHITE)
    draw.text((100 + w_p1, 174), title_p2, font=get_font(52, 'black'), fill=C_RED_HERO)
    
    sub1 = "공무원·공기업 취업 및 수능·한능검 1급 합격을 위한 최신 80문항 모의고사 엔진과"
    sub2 = "오답률 88% 취약 시대 자동 인덱싱, 6대 시대별 마스터 노트로 수험 기간을 1/3로 단축하는 에듀테크 플랫폼"
    draw.text((100, 252), sub1, font=get_font(15, 'regular'), fill=C_TEXT_BODY)
    draw.text((100, 278), sub2, font=get_font(15, 'regular'), fill=C_TEXT_BODY)
    
    # 4 Key Impact Metric Pods
    metrics = [
        ("1,500+", "실전 기출 문항 풀", "최신 77회 한능검 심화 전문 수록", "red"),
        ("100%", "오프라인 영속성", "통신 장애 없는 SQLite 로컬 캐싱", "gold"),
        ("88%", "취약 파트 적중 보완", "틀린 문제 자동 인덱싱 & 오답 노트", "green"),
        ("6대 시대", "선사부터 현대까지", "키워드 연표 & 오디오 청각 학습", "red")
    ]
    card_y = 345
    card_w = 195
    card_h = 135
    for idx, (m_val, m_lbl, m_desc, theme) in enumerate(metrics):
        cx = 100 + idx * (card_w + 18)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=16, fill=C_BG_CARD, outline=C_BORDER_RED if theme == 'red' else (245, 158, 11, 120), width=1)
        draw.text((cx + 18, card_y + 20), m_val, font=get_num_font(32, 'black'), fill=C_RED_HERO if theme == 'red' else (C_GOLD_ACC if theme == 'gold' else C_GREEN_ACC))
        draw.text((cx + 18, card_y + 68), m_lbl, font=get_font(13, 'bold'), fill=C_TITLE_WHITE)
        draw.text((cx + 18, card_y + 94), m_desc, font=get_font(10.5, 'medium'), fill=C_TEXT_MUTED)
        
    # Project Scope Pod
    scope_y = 510
    scope_w = 835
    scope_h = 240
    draw.rounded_rectangle([100, scope_y, 100 + scope_w, scope_y + scope_h], radius=18, fill=C_BG_CARD, outline=(239, 68, 68, 70), width=1)
    draw.text((125, scope_y + 22), "PROJECT SPECIFICATION & ARCHITECTURE OVERVIEW", font=get_font(12, 'bold'), fill=C_RED_HERO)
    
    spec_rows = [
        ("담당 역할", "프로덕트 기획, UX/UI 디자인 총괄, Flutter 프론트 아키텍처 (100% 1인 전담)"),
        ("핵심 과제", "방대한 시험 범위 압축, 사료 이미지 고해상도 판독성 확보, 게이미피케이션 동기부여"),
        ("기술 스택", "Flutter 3.9, SQLite Local Cache, Provider, Custom Audio Player, Material 3"),
        ("지원 플랫폼", "Android Phone (1080x1920), 7\" Tablet (1200x1920), 10\" Tablet (1600x2560)"),
        ("적용 상태", "Google Play Store 출시 라이브 & 수험생 1만+ 누적 기출 풀이 검증 완료")
    ]
    for r_idx, (k, v) in enumerate(spec_rows):
        ry = scope_y + 54 + r_idx * 34
        draw.text((125, ry), f"• {k}", font=get_font(12, 'bold'), fill=C_GOLD_ACC)
        draw.text((225, ry), f":  {v}", font=get_font(12, 'medium'), fill=C_TEXT_BODY)
        
    # Bottom Tags
    tags = ["#한능검_1급", "#에듀테크_UX", "#오답_볼트", "#SQLite_캐싱", "#사료_핀치줌", "#게이미피케이션"]
    tx = 100
    for t in tags:
        draw_pill_badge(draw, left_x=tx, cy=795, text=t, font=get_font(11, 'bold'), theme='slate', height=28, pad_x=12)
        tx += int(draw.textlength(t, font=get_font(11, 'bold')) + 24 + 10)

    # Hero Phone Mockup Devices Showcase on Right
    m1 = Image.open(f"{MOCKUP_DIR}/mockup_01_home.png")
    m2 = Image.open(f"{MOCKUP_DIR}/mockup_02_exam.png")
    
    scale_h1 = 780
    scale_h2 = 690
    
    dev1 = m1.resize((int(m1.width * (scale_h1 / m1.height)), scale_h1), Image.Resampling.LANCZOS)
    dev2 = m2.resize((int(m2.width * (scale_h2 / m2.height)), scale_h2), Image.Resampling.LANCZOS)
    
    pos2 = (1420, 175)
    sh2 = make_shadow(dev2, radius=35, alpha=150)
    base.paste(sh2, (pos2[0] - 32, pos2[1] - 24), sh2)
    base.paste(dev2, pos2, dev2)
    
    pos1 = (1050, 130)
    sh1 = make_shadow(dev1, radius=45, alpha=200)
    base.paste(sh1, (pos1[0] - 32, pos1[1] - 24), sh1)
    base.paste(dev1, pos1, dev1)
    
    # Floating Korean History Relic Badge (Comb Pattern Pottery)
    relic_path = os.path.join(ASSETS_DIR, 'comb_pattern_pottery.png')
    if os.path.exists(relic_path):
        relic = Image.open(relic_path).convert('RGBA')
        r_w = 110
        r_sc = relic.resize((r_w, int(relic.height * (r_w / relic.width))), Image.Resampling.LANCZOS)
        badge_im = Image.new('RGBA', (130, 130), (0, 0, 0, 0))
        bd = ImageDraw.Draw(badge_im)
        bd.rounded_rectangle([0, 0, 130, 130], radius=24, fill=(15, 23, 42, 230), outline=(245, 158, 11, 160), width=2)
        badge_im.paste(r_sc, ((130 - r_sc.width)//2, (130 - r_sc.height)//2), r_sc)
        sh_b = make_shadow(badge_im, radius=20, alpha=140)
        base.paste(sh_b, (980 - 24, 690 - 20), sh_b)
        base.paste(badge_im, (980, 690), badge_im)
    
    draw_slide_footer(draw, meta_tags="HERO COVER · 01/12")
    save_slide(base, 1)

# -------------------------------------------------------------
# SLIDE 02: PROBLEM DEFINITION & MARKET STUDY
# -------------------------------------------------------------
def make_slide_02():
    base, draw = create_base_canvas(center_orbit=(1500, 500))
    draw_slide_header(draw, 2, "수험생 87%가 호소하는 한능검 학습의 3대 장벽과 시장 기회",
                      "방대한 시대별 암기 부담과 두꺼운 기출 문제집의 이동성 한계를 디지털 솔루션으로 해결합니다.")
    
    # 3 Problem Cards
    cards = [
        ("PAIN POINT 01", "방대한 5,000년 역사 범위와 망각 곡선", 
         "구석기부터 현대사까지 6대 시대를 거치며 앞부분을 외우면 뒷부분을 잊어버리는 치명적인 망각 주기 발생.\n학습 진도율과 시대별 정답률을 한눈에 체감할 수 있는 실시간 인덱싱 대시보드 부재.",
         "평균 3.2회 반복 후 포기", "red"),
        ("PAIN POINT 02", "기출 문제집의 휴대성 한계 및 사료 판독 난이도", 
         "500페이지가 넘는 두꺼운 기출 문제집은 이동 중 학습이 불가능하며, 흑백 인쇄된 유물·사료 사진은 시험장에서 작은 디테일을 식별하기 어려움.\n고해상도 컬러 핀치 줌 뷰어 필수.",
         "무게 1.2kg 종이 교재 한계", "gold"),
        ("PAIN POINT 03", "반복되는 취약 시대와 비효율적 오답 정리", 
         "수험생마다 조선 붕당정치, 근현대사 독립운동단체 등 특정 시대의 오답이 집중되나 오답노트를 수기로 오려 붙이는 데 학습 시간의 40% 이상을 소모하는 비효율성.",
         "오답 정리 1회당 45분 소요", "red")
    ]
    card_w = 490
    card_h = 330
    card_y = 225
    for idx, (tag, t_txt, desc, stat_txt, theme) in enumerate(cards):
        cx = 100 + idx * (card_w + 25)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=20, fill=C_BG_CARD, outline=C_BORDER_RED if theme == 'red' else (245, 158, 11, 100), width=1)
        draw_pill_badge(draw, left_x=cx + 24, cy=card_y + 36, text=tag, font=get_font(11.5, 'bold'), theme=theme, pad_x=12, height=26)
        draw.text((cx + 24, card_y + 70), t_txt, font=get_font(18, 'bold'), fill=C_TITLE_WHITE)
        lines = wrap_text_by_words(desc, get_font(13.5, 'regular'), card_w - 48, draw)
        for l_idx, l in enumerate(lines):
            draw.text((cx + 24, card_y + 115 + l_idx * 24), l, font=get_font(13.5, 'regular'), fill=C_TEXT_BODY)
            
        # Stat footer inside card
        draw.rounded_rectangle([cx + 20, card_y + card_h - 52, cx + card_w - 20, card_y + card_h - 18], radius=10, fill=C_BG_CONTAINER)
        draw.text((cx + 34, card_y + card_h - 44), f"실측 지표: {stat_txt}", font=get_font(12, 'bold'), fill=C_GOLD_ACC if theme == 'gold' else C_RED_HERO)
            
    # Bottom Solution Strategy Architecture Pod
    strat_y = 585
    strat_w = 1520
    strat_h = 400
    draw.rounded_rectangle([100, strat_y, 100 + strat_w, strat_y + strat_h], radius=20, fill=C_BG_CARD, outline=(255, 255, 255, 18), width=1)
    draw.text((130, strat_y + 26), "대한한국사 핵심 가치 제안 (CORE VALUE PROPOSITION)", font=get_font(14, 'bold'), fill=C_RED_HERO)
    
    strat_items = [
        ("01. 마이크로 러닝 모의고사", "출퇴근/통학 10분 동안 5문항씩 가볍게 푸는 숏폼 모드와 50문항 80분 풀타임 실전 모드 듀얼 지원", "gold"),
        ("02. 자동 오답 인덱싱 볼트", "틀린 문제는 클릭 한 번 없이 오답 노트에 자동 저장되며, 정답을 맞힐 때까지 스마트 재출제 알고리즘 작동", "red"),
        ("03. 6대 시대별 요약집 내장", "유물 사진, 지도, 사료 원문이 포함된 시대별 고해상도 요약집을 앱 내에 탑재하여 교재 없이 완벽 대비", "green")
    ]
    for s_idx, (stitle, sdesc, stheme) in enumerate(strat_items):
        sx = 130 + s_idx * (480 + 20)
        sy = strat_y + 68
        draw.rounded_rectangle([sx, sy, sx + 480, sy + 295], radius=16, fill=C_BG_CONTAINER, outline=(239, 68, 68, 40), width=1)
        draw_pill_badge(draw, left_x=sx + 20, cy=sy + 32, text=f"STRATEGY 0{s_idx+1}", font=get_font(11, 'bold'), theme=stheme, pad_x=10, height=24)
        draw.text((sx + 20, sy + 65), stitle, font=get_font(17, 'bold'), fill=C_TITLE_WHITE)
        slines = wrap_text_by_words(sdesc, get_font(13, 'regular'), 440, draw)
        for sl_idx, sl in enumerate(slines):
            draw.text((sx + 20, sy + 110 + sl_idx * 22), sl, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
            
    draw_slide_footer(draw, meta_tags="PROBLEM & VALUE PROPOSITION · 02/12")
    save_slide(base, 2)

# -------------------------------------------------------------
# SLIDE 03: TARGET PERSONA MATRIX
# -------------------------------------------------------------
def make_slide_03():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 3, "목표 수험생 페르소나 및 학습 시나리오 매트릭스",
                      "단기 고득점이 필요한 공기업 준비생부터 틈새 시간 학습을 원하는 대학생까지 맞춤형 여정을 설계했습니다.")
    
    personas = [
        {
            "badge": "PRIMARY PERSONA", "theme": "red",
            "name": "김민준 (27세) · 공기업/공무원 채용 준비생",
            "tag": "목표: 한능검 심화 1급 80점 이상 단기 취득",
            "pain": "가산점 제출 마감까지 남은 기간은 4주. 전공 시험과 NCS 준비로 한국사에 하루 2시간 이상 투자하기 어려움.",
            "journey": "① 퇴근길 10분 모의고사 풀기 → ② 자동 기록된 오답 노트 복습 → ③ 주말 실전 50문항 풀모의고사 응시",
            "gain": "암기 취약 시대(근현대사)만 집중 공략하여 3주 만에 안정적인 88점 확보"
        },
        {
            "badge": "SECONDARY PERSONA", "theme": "gold",
            "name": "이수아 (22세) · 수능 및 학점 대비 대학생",
            "tag": "목표: 한국사 필수 등급 확보 및 교양 시험 대비",
            "pain": "사료 지문이 길고 헷갈리는 유물 문제가 많아 교재를 정독할 시간이 부족하고 집중력이 금방 저하됨.",
            "journey": "① 6대 시대별 요약집 정독 → ② 사료 핀치 줌으로 유물 디테일 확인 → ③ 50:50 찬스 활용 퀴즈 격파",
            "gain": "시각적 유물 카드와 게이미피케이션 스트릭 유지로 지루함 없이 1등급 달성"
        }
    ]
    card_w = 790
    card_h = 740
    card_y = 230
    for idx, p in enumerate(personas):
        cx = 100 + idx * (card_w + 40)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=22, fill=C_BG_CARD, outline=C_BORDER_RED if p['theme'] == 'red' else (245, 158, 11, 100), width=1)
        
        draw_pill_badge(draw, left_x=cx + 32, cy=card_y + 40, text=p['badge'], font=get_font(12, 'bold'), theme=p['theme'], pad_x=14, height=28)
        draw.text((cx + 32, card_y + 80), p['name'], font=get_font(21, 'bold'), fill=C_TITLE_WHITE)
        draw.text((cx + 32, card_y + 115), p['tag'], font=get_font(14, 'semibold'), fill=C_RED_HERO if p['theme'] == 'red' else C_GOLD_ACC)
        
        # Sections
        sec_y = card_y + 160
        sections = [
            ("주요 페인포인트 (Core Pain Points)", p['pain'], C_RED_MUTED),
            ("수험생 프로덕트 유저 여정 (User Journey)", p['journey'], C_TEXT_BODY),
            ("기대 성과 & 가치 달성 (Expected Gains)", p['gain'], C_GREEN_ACC)
        ]
        for stitle, scontent, sc_col in sections:
            draw.rounded_rectangle([cx + 32, sec_y, cx + card_w - 32, sec_y + 160], radius=14, fill=C_BG_CONTAINER, outline=(255, 255, 255, 12), width=1)
            draw.text((cx + 50, sec_y + 18), stitle, font=get_font(13.5, 'bold'), fill=C_GOLD_ACC)
            lines = wrap_text_by_words(scontent, get_font(13.5, 'regular'), card_w - 100, draw)
            for l_idx, l in enumerate(lines):
                draw.text((cx + 50, sec_y + 52 + l_idx * 24), l, font=get_font(13.5, 'regular'), fill=sc_col)
            sec_y += 180
            
    draw_slide_footer(draw, meta_tags="TARGET PERSONA & JOURNEY · 03/12")
    save_slide(base, 3)

# -------------------------------------------------------------
# SLIDE 04: INFORMATION ARCHITECTURE (IA)
# -------------------------------------------------------------
def make_slide_04():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 4, "정보 구조 설계 (IA) & 데이터 계층 체계",
                      "학습 상태, 실전 시험, 오답 복습, 시대별 서고를 유기적으로 연결한 4단 탭 아키텍처입니다.")
    
    tabs = [
        {
            "name": "01. 홈 대시보드 (Home Hub)", "theme": "red",
            "desc": "일일 학습 목표 및 누적 통계",
            "nodes": ["• 연속 출석 스트릭 & 일일 미션", "• 6대 시대별 마스터리 레이더 차트", "• 최근 풀던 시험 이어풀기 진입", "• 취약 시대 즉각 추천 배너"]
        },
        {
            "name": "02. 기출 시험 센터 (Exam Center)", "theme": "gold",
            "desc": "최신 한능검 실전 모의고사",
            "nodes": ["• 회차별 실전 모의고사 (50문항/80분)", "• 10문항 랜덤 숏폼 테스트", "• 타이머 일시정지 & OMR 마킹", "• 사료 이미지 풀스크린 확대경"]
        },
        {
            "name": "03. 시대별 서고 (Study Hall)", "theme": "green",
            "desc": "선사부터 현대까지 6대 테마",
            "nodes": ["• 핵심 연표 타임라인 네비게이션", "• 고해상도 유물·사료 카드 인덱스", "• 오디오 요약 청취 플레이어", "• 키워드 검색 & 시대 필터링"]
        },
        {
            "name": "04. 스마트 오답 볼트 (Vault)", "theme": "indigo",
            "desc": "취약 파트 정밀 타격 복습",
            "nodes": ["• 오답 자동 분류 (시대별/유형별)", "• 1:1 맞춤 정밀 해설 및 사료 단서", "• 맞힐 때까지 무한 재도전 모드", "• 즐겨찾기 문항 PDF 내보내기"]
        }
    ]
    card_w = 390
    card_h = 720
    card_y = 240
    for idx, t in enumerate(tabs):
        cx = 100 + idx * (card_w + 20)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=20, fill=C_BG_CARD, outline=C_BORDER_RED if t['theme'] == 'red' else (255, 255, 255, 25), width=1)
        draw_pill_badge(draw, left_x=cx + 24, cy=card_y + 36, text=f"TAB {idx+1}", font=get_font(11, 'bold'), theme=t['theme'], pad_x=12, height=26)
        draw.text((cx + 24, card_y + 75), t['name'], font=get_font(17, 'bold'), fill=C_TITLE_WHITE)
        draw.text((cx + 24, card_y + 105), t['desc'], font=get_font(13, 'medium'), fill=C_GOLD_ACC)
        
        draw.line([(cx + 24, card_y + 140), (cx + card_w - 24, card_y + 140)], fill=(255, 255, 255, 15), width=1)
        
        # Nodes list
        ny = card_y + 170
        for n in t['nodes']:
            draw.rounded_rectangle([cx + 20, ny, cx + card_w - 20, ny + 95], radius=12, fill=C_BG_CONTAINER, outline=(255, 255, 255, 10), width=1)
            lines = wrap_text_by_words(n, get_font(13, 'regular'), card_w - 60, draw)
            for l_idx, l in enumerate(lines):
                draw.text((cx + 34, ny + 20 + l_idx * 22), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
            ny += 115
            
    draw_slide_footer(draw, meta_tags="INFORMATION ARCHITECTURE · 04/12")
    save_slide(base, 4)

if __name__ == '__main__':
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
