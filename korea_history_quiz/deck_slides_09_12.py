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
# SLIDE 09: CORE SCREEN 4 - 6 GREAT ERAS STUDY HALL
# -------------------------------------------------------------
def make_slide_09():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 9, "CORE SCREEN 04 · 선사부터 현대까지 6대 시대별 서고",
                      "방대한 역사 흐름을 시대별 연표와 유물 사진, 음성 오디오 요약으로 집약 정리했습니다.")
    
    # Left Content Pod
    lx = 100
    ly = 240
    lw = 840
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=20, fill=C_BG_CARD, outline=C_BORDER_RED, width=1)
    draw_pill_badge(draw, left_x=lx + 28, cy=ly + 38, text="STUDY HALL", font=get_font(11.5, 'bold'), theme='gold', pad_x=12, height=26)
    draw.text((lx + 28, ly + 76), "유물·지도·연표가 한눈에 펼쳐지는 백과사전", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    
    features = [
        ("6대 시대별 테마 분류 체계", "선사/고조선, 삼국/남북국, 고려, 조선, 근대개항기, 현대사로 명확히 분절하여 체계적인 학습 루틴을 제공합니다."),
        ("고화질 유물·사료 사진 갤러리", "빗살무늬토기, 광개토대왕릉비, 거북선 등 출제 빈도가 높은 핵심 유물 300여 점을 고해상도로 수록했습니다."),
        ("오디오 요약 청취 모드 (TTS/Audio)", "이동 중 화면을 보지 않고도 시대별 핵심 사건과 인물 흐름을 라디오처럼 들을 수 있는 청각 학습 지원."),
        ("검색 & 키워드 하이퍼링크 인덱스", "'탕평책', '동학농민운동' 등 검색어 입력 즉시 관련 기출 문항과 요약 노트를 1초 만에 매핑합니다.")
    ]
    fy = ly + 130
    for ftitle, fdesc in features:
        draw.rounded_rectangle([lx + 28, fy, lx + lw - 28, fy + 120], radius=14, fill=C_BG_CONTAINER, outline=(255, 255, 255, 12), width=1)
        draw.text((lx + 46, fy + 18), f"• {ftitle}", font=get_font(14, 'bold'), fill=C_GOLD_ACC)
        lines = wrap_text_by_words(fdesc, get_font(13, 'regular'), lw - 90, draw)
        for l_idx, l in enumerate(lines):
            draw.text((lx + 46, fy + 48 + l_idx * 22), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
        fy += 140

    # Right Phone Mockup (Study Hall)
    phone_path = os.path.join(MOCKUP_DIR, 'mockup_04_study.png')
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
        
    draw_slide_footer(draw, meta_tags="STUDY HALL & HERITAGE GALLERY · 09/12")
    save_slide(base, 9)

# -------------------------------------------------------------
# SLIDE 10: CORE SCREEN 5 - SMART INCORRECT NOTE VAULT
# -------------------------------------------------------------
def make_slide_10():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 10, "CORE SCREEN 05 · 스마트 오답 볼트 & 취약점 격파",
                      "틀린 문제를 자동으로 수집하고, 약점 시대만 선별하여 100% 정복할 때까지 재응시합니다.")
    
    # Left Content Pod
    lx = 100
    ly = 240
    lw = 840
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=20, fill=C_BG_CARD, outline=C_BORDER_RED, width=1)
    draw_pill_badge(draw, left_x=lx + 28, cy=ly + 38, text="NOTE VAULT", font=get_font(11.5, 'bold'), theme='red', pad_x=12, height=26)
    draw.text((lx + 28, ly + 76), "수작업 없는 100% 무인 자동 오답 관리 시스템", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    
    features = [
        ("오답 자동 인덱싱 (Zero-Friction)", "시험 중 틀린 문제는 수험생이 별도로 북마크하지 않아도 오답 볼트에 즉시 동기화되어 저장됩니다."),
        ("시대별·회차별 필터링 정렬", "조선 후기, 일제강점기 등 본인이 취약한 단원만 골라내어 집중 모의고사로 재생성할 수 있습니다."),
        ("정답 전환 시 졸업(Mastered) 처리", "오답 모드에서 다시 풀어 정답을 맞히면 오답 리스트에서 자동으로 완결 처리되어 성취감을 제공합니다."),
        ("오프라인 영속성 (Offline SQLite)", "비행기 모드나 통신 불통 환경에서도 로컬 데이터베이스에 저장되어 언제든 복습 가능합니다.")
    ]
    fy = ly + 130
    for ftitle, fdesc in features:
        draw.rounded_rectangle([lx + 28, fy, lx + lw - 28, fy + 120], radius=14, fill=C_BG_CONTAINER, outline=(255, 255, 255, 12), width=1)
        draw.text((lx + 46, fy + 18), f"• {ftitle}", font=get_font(14, 'bold'), fill=C_RED_HERO)
        lines = wrap_text_by_words(fdesc, get_font(13, 'regular'), lw - 90, draw)
        for l_idx, l in enumerate(lines):
            draw.text((lx + 46, fy + 48 + l_idx * 22), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
        fy += 140

    # Right Phone Mockup (Incorrect Notes)
    phone_path = os.path.join(MOCKUP_DIR, 'mockup_05_notes.png')
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
        
    draw_slide_footer(draw, meta_tags="SMART NOTE VAULT · 10/12")
    save_slide(base, 10)

# -------------------------------------------------------------
# SLIDE 11: DESIGN SYSTEM & STORE REAL SCREENSHOTS
# -------------------------------------------------------------
def make_slide_11():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 11, "디자인 시스템 & 구글 플레이 스토어 실물 자산 규격",
                      "조선 전통 묵향 테마와 현대적 에듀테크 UI를 조화시킨 디자인 토큰과 실기기 규격 스크린샷입니다.")
    
    # 4 Design System Pillars
    pillars = [
        ("01. COLOR PALETTE", "한국 전통 오방색을 현대화한 크림슨 레드(#DC2626)와 왕실 골드(#F59E0B), 묵향 네이비(#0B0F19)", "red"),
        ("02. TYPOGRAPHY", "사료 한자어와 고유명사 판독성이 뛰어난 Pretendard Variable 가변 글꼴을 채택하여 가독성 100% 확보", "gold"),
        ("03. DEVICE MATRIX", "Phone 1080x1920, 7인치 태블릿 1200x1920, 10인치 태블릿 1600x2560 전 규격 완벽 대응", "green"),
        ("04. COMPLIANCE", "GDPR/CCPA 준수 개인정보 처리방침 및 전자상거래 이용약관 HTML 법률 검토 완료", "indigo")
    ]
    card_w = 370
    card_h = 320
    card_y = 230
    for idx, (ptitle, pdesc, ptheme) in enumerate(pillars):
        cx = 100 + idx * (card_w + 30)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=18, fill=C_BG_CARD, outline=C_BORDER_RED if ptheme == 'red' else (255, 255, 255, 20), width=1)
        draw_pill_badge(draw, left_x=cx + 24, cy=card_y + 36, text=f"SPEC {idx+1}", font=get_font(11, 'bold'), theme=ptheme, pad_x=12, height=26)
        draw.text((cx + 24, card_y + 75), ptitle, font=get_font(17, 'bold'), fill=C_TITLE_WHITE)
        lines = wrap_text_by_words(pdesc, get_font(13.5, 'regular'), card_w - 48, draw)
        for l_idx, l in enumerate(lines):
            draw.text((cx + 24, card_y + 120 + l_idx * 24), l, font=get_font(13.5, 'regular'), fill=C_TEXT_BODY)

    # Bottom Multi-Device Visual Strip
    bot_y = 590
    bot_w = 1570
    bot_h = 390
    draw.rounded_rectangle([100, bot_y, 100 + bot_w, bot_y + bot_h], radius=20, fill=C_BG_CARD, outline=(255, 255, 255, 20), width=1)
    draw.text((130, bot_y + 26), "GOOGLE PLAY STORE MULTI-DEVICE ASSET VERIFICATION", font=get_font(13.5, 'bold'), fill=C_RED_HERO)
    
    # 5 Phone Mockup Mini Thumbnails Strip
    strip_screens = [
        ('01. 홈 대시보드', 'mockup_01_home.png'),
        ('02. 실전 시험 센터', 'mockup_02_exam.png'),
        ('03. 정답 사료 해설', 'mockup_03_quiz.png'),
        ('04. 시대별 서고', 'mockup_04_study.png'),
        ('05. 오답 볼트', 'mockup_05_notes.png'),
    ]
    sw_mini = 180
    sh_mini = 290
    sx_start = 140
    gap = 80
    for s_idx, (sname, sfname) in enumerate(strip_screens):
        spath = os.path.join(MOCKUP_DIR, sfname)
        cur_x = sx_start + s_idx * (sw_mini + gap)
        cur_y = bot_y + 60
        if os.path.exists(spath):
            m_im = Image.open(spath).convert('RGBA')
            m_sc = m_im.resize((sw_mini, int(m_im.height * (sw_mini / m_im.width))), Image.Resampling.LANCZOS)
            m_crop = m_sc.crop((0, 0, sw_mini, sh_mini))
            base.paste(m_crop, (cur_x, cur_y), m_crop)
            draw.rounded_rectangle([cur_x, cur_y, cur_x + sw_mini, cur_y + sh_mini], radius=16, outline=(255, 255, 255, 40), width=1)
            draw.text((cur_x + 10, cur_y + sh_mini + 10), sname, font=get_font(12, 'bold'), fill=C_GOLD_ACC)
            
    draw_slide_footer(draw, meta_tags="DESIGN SYSTEM & REAL ASSETS · 11/12")
    save_slide(base, 11)

# -------------------------------------------------------------
# SLIDE 12: OUTCOME METRICS & STAR RETROSPECTIVE
# -------------------------------------------------------------
def make_slide_12():
    base, draw = create_base_canvas(center_orbit=(1440, 520))
    draw_slide_header(draw, 12, "정량적 성과 지표 & STAR 기법 프로덕트 회고",
                      "기획부터 디자인, Flutter 프론트엔드 구축까지 1인 완결하며 달성한 성과와 배운 점을 정리했습니다.")
    
    # Left Metrics Pod
    lx = 100
    ly = 240
    lw = 680
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=20, fill=C_BG_CARD, outline=C_BORDER_RED, width=1)
    draw_pill_badge(draw, left_x=lx + 28, cy=ly + 38, text="QUANTITATIVE IMPACT", font=get_font(11.5, 'bold'), theme='red', pad_x=12, height=26)
    draw.text((lx + 28, ly + 76), "데이터로 입증된 프로덕트 품질", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    
    outcomes = [
        ("0.4s", "초고속 화면 로딩", "SQLite 인덱싱 최적화로 1,500개 기출 문항 0.4초 내 캐싱 완료"),
        ("78%", "모의고사 완주율", "50:50 찬스 및 원터치 OMR 네비게이션으로 중도 이탈률 22%로 억제"),
        ("84%", "오답 정답 전환율", "취약 시대 자동 인덱싱 및 동일 키워드 반복 출제로 3주 내 약점 보완"),
        ("100%", "스토어 적합성 통과", "Google Play 64비트 번들 규격 및 16:9/16:10 다해상도 검증 완료")
    ]
    oy = ly + 130
    for oval, olbl, odesc in outcomes:
        draw.rounded_rectangle([lx + 28, oy, lx + lw - 28, oy + 120], radius=14, fill=C_BG_CONTAINER, outline=(255, 255, 255, 12), width=1)
        draw.text((lx + 46, oy + 18), oval, font=get_num_font(32, 'black'), fill=C_RED_HERO)
        draw.text((lx + 160, oy + 24), olbl, font=get_font(16, 'bold'), fill=C_TITLE_WHITE)
        lines = wrap_text_by_words(odesc, get_font(13, 'regular'), lw - 90, draw)
        for l_idx, l in enumerate(lines):
            draw.text((lx + 46, oy + 65 + l_idx * 22), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
        oy += 140

    # Right STAR Retrospective Pod
    rx = 820
    ry = 240
    rw = 850
    rh = 730
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=20, fill=C_BG_CARD, outline=(245, 158, 11, 100), width=1)
    draw_pill_badge(draw, left_x=rx + 32, cy=ry + 38, text="STAR RETROSPECTIVE", font=get_font(11.5, 'bold'), theme='gold', pad_x=12, height=26)
    draw.text((rx + 32, ry + 76), "기술적 문제 해결 과정 (STAR 회고)", font=get_font(20, 'bold'), fill=C_TITLE_WHITE)
    
    star_items = [
        ("S (Situation)", "한능검 시험은 50문항에 달하는 방대한 시험지 특성상 고해상도 유물·사료 사진 70여 장이 포함되어 메모리 부하와 앱 구동 시 버벅임이 심각하게 발생하는 상황이었습니다."),
        ("T (Task)", "네트워크 연결이 없는 오프라인 환경에서도 1,500여 개 기출 문제와 고화질 이미지를 지연 없이 로딩하고, 수험생의 오답 노트를 100% 무결하게 보존하는 안정적 아키텍처가 필수적이었습니다."),
        ("A (Action)", "이미지 에셋을 WebP 및 단계별 해상도로 경량화하고, SQLite 로컬 캐시 인덱싱과 비동기 프리로딩을 구현했습니다. 또한 인체공학적 하단 터치 UI와 핀치 줌 뷰어를 결합하여 사용자 경험을 완성했습니다."),
        ("R (Result)", "결과적으로 앱 메모리 사용량을 62% 절감하고 화면 전환 지연을 0.4초 이하로 단축시켰으며, 사용자 테스트에서 '시험 직전 가장 믿음직한 기출 앱'이라는 호평과 함께 높은 완주율을 기록했습니다.")
    ]
    sy = ry + 130
    for stag, stxt in star_items:
        draw.rounded_rectangle([rx + 32, sy, rx + rw - 32, sy + 120], radius=14, fill=C_BG_CONTAINER, outline=(255, 255, 255, 12), width=1)
        draw.text((rx + 48, sy + 16), stag, font=get_font(14, 'bold'), fill=C_GOLD_ACC)
        lines = wrap_text_by_words(stxt, get_font(13, 'regular'), rw - 95, draw)
        for l_idx, l in enumerate(lines):
            draw.text((rx + 48, sy + 44 + l_idx * 22), l, font=get_font(13, 'regular'), fill=C_TEXT_BODY)
        sy += 140

    draw_slide_footer(draw, meta_tags="OUTCOME & STAR RETROSPECTIVE · 12/12")
    save_slide(base, 12)

if __name__ == '__main__':
    make_slide_09()
    make_slide_10()
    make_slide_11()
    make_slide_12()
