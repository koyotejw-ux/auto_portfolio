import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
BASE_DIR = r"d:\097.flutter_project\auto_portfolio\ht_wallpad"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUT_DIR = os.path.join(BASE_DIR, "behance_slides")
os.makedirs(OUT_DIR, exist_ok=True)

# HT Brand Identity Palette (Signature Crimson + Smart Home Slate)
HT_RED = (244, 0, 68)          # #F40044 HT Signature Magenta-Red
HT_DARK = (190, 18, 60)        # #BE123C Deep Crimson
HT_BLUE = (37, 99, 235)        # #2563EB Smart Control Blue
HT_TEAL = (13, 148, 136)       # #0D9488 IoT Info Teal
BG_LIGHT = (255, 255, 255)
BG_HERO = (250, 252, 255)
CARD_LIGHT = (255, 255, 255)
BORDER_LIGHT = (226, 232, 240)
TEXT_MAIN = (15, 23, 42)
TEXT_SUB = (100, 116, 139)

TOTAL_SLIDES = 10

def get_font(size, weight='bold'):
    candidates = {
        'black': ["Pretendard-Black.otf", "Pretendard-Black.ttf", "malgunbd.ttf", "arialbd.ttf"],
        'bold': ["Pretendard-Bold.otf", "Pretendard-Bold.ttf", "malgunbd.ttf", "arialbd.ttf"],
        'semibold': ["Pretendard-SemiBold.otf", "Pretendard-Bold.otf", "malgunbd.ttf", "arialbd.ttf"],
        'medium': ["Pretendard-Medium.otf", "Pretendard-Medium.ttf", "malgun.ttf", "arial.ttf"],
        'regular': ["Pretendard-Regular.otf", "Pretendard-Regular.ttf", "malgun.ttf", "arial.ttf"],
    }
    font_paths = [
        r"C:\Windows\Fonts",
        r"C:\Users\coyot\AppData\Local\Microsoft\Windows\Fonts",
        os.path.join(r"d:\097.flutter_project\auto_portfolio", "assets", "fonts"),
    ]
    for fn in candidates.get(weight, candidates['regular']):
        for d in font_paths:
            fp = os.path.join(d, fn)
            if os.path.exists(fp):
                try:
                    return ImageFont.truetype(fp, int(size * 1.33))
                except Exception:
                    pass
    return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append("")
            continue
        words = para.split(' ')
        cur = ""
        for w in words:
            test = f"{cur} {w}".strip()
            if draw.textlength(test, font=font) <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def draw_pill(draw, cx=None, cy=0, text="", font=None, theme='red', pad_x=12, height=24, left_x=None, solid=False):
    themes = {
        'red': {
            'bg': HT_RED if solid else (255, 241, 244),
            'border': HT_RED,
            'text': (255, 255, 255) if solid else HT_RED
        },
        'blue': {
            'bg': HT_BLUE if solid else (239, 246, 255),
            'border': HT_BLUE,
            'text': (255, 255, 255) if solid else HT_BLUE
        },
        'teal': {
            'bg': HT_TEAL if solid else (240, 253, 250),
            'border': HT_TEAL,
            'text': (255, 255, 255) if solid else HT_TEAL
        },
        'dark': {
            'bg': TEXT_MAIN if solid else (241, 245, 249),
            'border': TEXT_MAIN if solid else (203, 213, 225),
            'text': (255, 255, 255) if solid else TEXT_MAIN
        },
        'gray': {
            'bg': (241, 245, 249),
            'border': (203, 213, 225),
            'text': (100, 116, 139)
        }
    }
    th = themes.get(theme, themes['red'])
    tw = draw.textlength(text, font=font)
    bw = tw + pad_x * 2
    if left_x is not None:
        x1, x2 = left_x, left_x + bw
    else:
        x1, x2 = cx - bw // 2, cx + bw // 2
    y1, y2 = cy - height // 2, cy + height // 2
    draw.rounded_rectangle([x1, y1, x2, y2], radius=height // 2, fill=th['bg'], outline=th['border'], width=1)
    draw.text(((x1 + x2) // 2, cy), text, font=font, fill=th['text'], anchor='mm')
    return bw

def draw_header(draw, slide_num, cat, title_dark, title_accent, subtitle, right_badge=None):
    draw.line([(100, 48), (1820, 48)], fill=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=100, cy=78, text=f"{slide_num:02d} {cat}", font=get_font(10.5, 'bold'), theme='red', pad_x=12, height=26)
    if right_badge:
        txt, th = right_badge
        bw = draw.textlength(txt, font=get_font(10.5, 'bold')) + 28
        draw_pill(draw, left_x=1820 - bw, cy=78, text=txt, font=get_font(10.5, 'bold'), theme=th, solid=True, pad_x=14, height=28)
    f_t = get_font(32, 'bold')
    w_d = draw.textlength(title_dark, font=f_t)
    draw.text((100, 116), title_dark, font=f_t, fill=TEXT_MAIN)
    draw.text((100 + w_d, 116), title_accent, font=f_t, fill=HT_RED)
    draw.text((100, 166), subtitle, font=get_font(14, 'regular'), fill=TEXT_SUB)

def draw_footer(draw, slide_num):
    draw.line([(100, 995), (1820, 995)], fill=BORDER_LIGHT, width=1)
    f_b = get_font(11.5, 'bold')
    brand = "HT · ANDROID CUSTOM WALLPAD"
    draw.text((100, 1018), brand, font=f_b, fill=HT_RED)
    wb = draw.textlength(brand, font=f_b)
    draw.text((100 + wb + 16, 1018), "·   현대HT 차세대 스마트홈 Android Custom OS UX/UI", font=get_font(11, 'medium'), fill=(148, 163, 184))
    draw.text((1060, 1018), "현대건설 · 현대엔지니어링 · 대우건설 1군 건설사 적용 플래그십 라인업", font=get_font(10.5, 'medium'), fill=(148, 163, 184), anchor='mt')
    draw.text((1820, 1018), f"PAGE {slide_num:02d} / {TOTAL_SLIDES:02d}", font=get_font(11.5, 'black'), fill=TEXT_SUB, anchor='rt')

# -------------------------------------------------------------
# SLIDE 01: HERO COVER (Clean Editorial + Real Wallpad Device)
# -------------------------------------------------------------
def make_slide_01():
    base = Image.new('RGBA', (W, H), (*BG_HERO, 255))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([860, 80, 1880, 820], fill=(244, 0, 68, 22))
    gd.ellipse([1040, 200, 1780, 760], fill=(37, 99, 235, 16))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)

    draw.line([(100, 52), (1820, 52)], fill=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=100, cy=76, text="FLAGSHIP SMART HOME OS CASE STUDY", font=get_font(11, 'bold'), theme='red', pad_x=12, height=28)
    meta = "Android Custom OS  ·  2018.05 - 2024.02  ·  참여율 100% (Main/Sub)  ·  PL · UX · UI · GUI"
    draw.text((1820, 76), meta, font=get_font(12.5, 'medium'), fill=TEXT_SUB, anchor='rm')

    draw.text((100, 132), "HYUNDAI HT · ANDROID CUSTOM WALLPAD", font=get_font(12.5, 'bold'), fill=HT_RED)
    draw.text((100, 162), "온 가족의 일상을 잇다,", font=get_font(30, 'bold'), fill=TEXT_MAIN)
    draw.text((100, 214), "HT Android Custom WALLPAD", font=get_font(38, 'black'), fill=HT_RED)

    sub1 = "기존 리눅스(Linux) 월패드 라인업을 고객사 니즈와 확장성에 맞춰 안드로이드 OS로 전면 전환하고,"
    sub2 = "부팅부터 홈 런처·앱 서랍·IoT 제어까지 3세대 가족 모두가 편안한 스마트홈 UX를 완성했습니다."
    draw.text((100, 294), sub1, font=get_font(13, 'regular'), fill=(71, 85, 105))
    draw.text((100, 320), sub2, font=get_font(13, 'semibold'), fill=(30, 41, 59))

    strengths = [
        ("01", "OS 전면 전환", "Linux → Android Custom OS 아키텍처", "Full-Stack Boot to Launcher",
         "부팅 애니메이션, 초기 데이터 동기화, 홈 런처, 시스템 네비게이션바까지 커스텀 OS 전 단계를 일관 설계했습니다."),
        ("02", "경쟁 우위 UX", "업계 최초 앱 서랍 & 통합 알림 센터", "App Drawer & Notification Hub",
         "K·C·S·L사 등 주요 경쟁사에 부재한 앱 서랍, 공통 네비게이션바, 실시간 통합 알림 시스템을 선도적으로 도입했습니다."),
        ("03", "유니버설 디자인", "20대부터 70대 시니어까지 전 세대 접근성", "3-Generation Barrier-Free",
         "원거리에서도 한눈에 인지되는 고대비 타이포그래피와 대형 터치 타깃으로 시니어·가족 모두의 오작동을 차단했습니다."),
        ("04", "멀티 디바이스", "도어폰·로비폰·이마주2.0 앱 실시간 연동", "Cross-Device Ecosystem",
         "공동현관 호출부터 화상 통화, 문열기, 세대현관 모니터링까지 4대 스마트홈 기기 간 끊김 없는 시나리오를 구현했습니다.")
    ]
    max_bw = max(draw.textlength(t, font=get_font(10, 'bold')) + 16 for _, t, _, _, _ in strengths)
    title_x = int(round(144 + max_bw + 18))

    ky = 392
    for idx, (num, tag, tko, ten, desc) in enumerate(strengths):
        rcy = ky + 14
        draw.rounded_rectangle([100, ky + 1, 134, ky + 27], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.text((117, rcy), num, font=get_font(11, 'bold'), fill=HT_RED, anchor='mm')
        draw_pill(draw, left_x=144, cy=rcy, text=tag, font=get_font(10, 'bold'), theme='red', pad_x=8, height=24)
        f_tk = get_font(14, 'bold')
        draw.text((title_x, rcy), tko, font=f_tk, fill=TEXT_MAIN, anchor='lm')
        wtk = draw.textlength(tko, font=f_tk)
        draw.text((title_x + wtk + 10, rcy), f"·  {ten}", font=get_font(11, 'medium'), fill=TEXT_SUB, anchor='lm')
        lines = wrap_text(desc, get_font(11.5, 'regular'), 736, draw)
        dy = ky + 40
        for l in lines[:2]:
            draw.text((144, dy), l, font=get_font(11.5, 'regular'), fill=(71, 85, 105))
            dy += 19
        if idx < 3:
            draw.line([(100, ky + 78), (880, ky + 78)], fill=BORDER_LIGHT, width=1)
        ky += 96

    # Right Side: Real HT Wallpad Hero Device + Ambient Standby Preview
    dev_path = os.path.join(ASSETS_DIR, "wallpad_hero_device.png")
    if os.path.exists(dev_path):
        dev = Image.open(dev_path).convert('RGBA')
        tw = 850
        th = int(dev.height * (tw / dev.width))
        dev_res = dev.resize((tw, th), Image.Resampling.LANCZOS)
        px, py = 965, 255
        # Soft shadow
        sh = Image.new('RGBA', (tw + 80, th + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([40, 48, tw + 40, th + 48], radius=30, fill=(15, 23, 42, 75))
        sh = sh.filter(ImageFilter.GaussianBlur(28))
        base.paste(sh, (px - 40, py - 32), sh)
        base.paste(dev_res, (px, py), dev_res)

        # Clean label strip below wallpad device
        draw = ImageDraw.Draw(base)
        draw.rounded_rectangle([px + 20, py + th + 32, px + tw - 20, py + th + 88], radius=12, fill=(255, 255, 255, 240), outline=BORDER_LIGHT, width=1)
        bw_d = draw_pill(draw, left_x=px + 38, cy=py + th + 60, text="LIVE LAUNCHER UI", font=get_font(9.5, 'bold'), theme='red', solid=True, pad_x=10, height=22)
        draw.text((px + 38 + bw_d + 14, py + th + 60), "날씨·미세먼지 · HEMS 에너지(가스/전기) · 6대 핵심 제어 퀵 런처 통합 화면", font=get_font(11.5, 'bold'), fill=TEXT_MAIN, anchor='lm')

    draw = ImageDraw.Draw(base)
    bar_y, bar_h = 836, 118
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    col_w = 1720 // 4
    specs = [
        ("CLIENTS", "HT · 현대건설 · 현대엔지니어링 · 대우건설", "국내 1군 주요 건설사 스마트홈 프리미엄 단지 적용"),
        ("PERIOD & CONTRIBUTION", "2018.05 - 2024.02 (100% Main/Sub)", "6년 장기 라인업 전환 프로젝트 메인/서브 전담 총괄"),
        ("PROJECT ROLE", "PL · UX 리서치 · UI 설계 · GUI 디자인", "경쟁사 분석·페르소나·여정맵·IA·와이어프레임·GUI 완결"),
        ("PLATFORM", "Android Custom OS (Embedded)", "부팅·초기동기화·런처·앱서랍·다기기 연동 커스텀 OS")
    ]
    for i, (cat, vb, vd) in enumerate(specs):
        cx = 100 + i * col_w
        if i > 0:
            draw.line([(cx, bar_y + 20), (cx, bar_y + bar_h - 20)], fill=BORDER_LIGHT, width=1)
        draw.text((cx + 28, bar_y + 20), cat, font=get_font(10.5, 'bold'), fill=HT_RED)
        draw.text((cx + 28, bar_y + 45), vb, font=get_font(13, 'bold'), fill=TEXT_MAIN)
        draw.text((cx + 28, bar_y + 76), vd, font=get_font(10.5, 'regular'), fill=TEXT_SUB)

    draw_footer(draw, 1)
    base.convert('RGB').save(os.path.join(OUT_DIR, "slide_01.png"), quality=95)
    print("Generated slide_01.png")

# -------------------------------------------------------------
# SLIDE 02: OVERVIEW & DESIGN PROCESS
# -------------------------------------------------------------
def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 2, "OVERVIEW & PROCESS",
        "Overview & Design Process | ", "리눅스에서 안드로이드 커스텀 OS로의 패러다임 전환",
        "고객사 요구사항과 스마트홈 비즈니스 확장을 수용하는 차세대 월패드 플랫폼 전환 전략 및 4단계 설계 프로세스",
        right_badge=("OS TRANSFORMATION", "red")
    )

    # Top Section: Overview Narrative + Real Standby 09:01 Visual Banner (y=215..555)
    t1_y, t1_h = 215, 330
    draw.rounded_rectangle([100, t1_y, 1820, t1_y + t1_h], radius=16, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    
    # Left Narrative (x=130..920)
    draw_pill(draw, left_x=130, cy=t1_y + 36, text="PROJECT BACKGROUND & GOAL", font=get_font(10, 'bold'), theme='red', pad_x=10, height=24)
    draw.text((130, t1_y + 68), "온 가족이 매일 마주하는 가장 편안한 스마트홈 허브", font=get_font(22, 'bold'), fill=TEXT_MAIN)
    
    ov_txt = (
        "현대에이치티(HT)는 기존 주력 리눅스(Linux) 월패드 라인업의 확장성 한계를 극복하고, "
        "주요 건설사 고객 요구사항과 IoT 비즈니스 확장을 수용하기 위해 Android Custom OS 기반 라인업 전면 교체를 추진했습니다.\n"
        "리눅스와 완전히 다른 안드로이드 환경에 맞춰 OS 부팅(Booting)부터 홈 런처(Launcher), 앱 서랍(App Drawer), "
        "다기기 연동까지 전 단계를 정밀 분석하여 전 세대가 직관적으로 사용할 수 있는 디자인을 완성했습니다."
    )
    lines = wrap_text(ov_txt, get_font(13, 'regular'), 780, draw)
    ly = t1_y + 114
    for l in lines:
        draw.text((130, ly), l, font=get_font(13, 'regular'), fill=(51, 65, 85))
        ly += 25

    # Right Real Standby 09:01 Hardware Photo Banner (x=960..1785)
    sb_path = os.path.join(ASSETS_DIR, "wallpad_standby_banner.png")
    if os.path.exists(sb_path):
        sb = Image.open(sb_path).convert('RGBA')
        bw_s, bh_s = 820, 230
        sb_res = sb.resize((bw_s, bh_s), Image.Resampling.LANCZOS)
        mask = Image.new('L', (bw_s, bh_s), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw_s, bh_s], radius=14, fill=255)
        img.paste(sb_res, (965, t1_y + 30), mask)
        draw.rounded_rectangle([965, t1_y + 30, 965 + bw_s, t1_y + 30 + bh_s], radius=14, outline=BORDER_LIGHT, width=1)
        draw.text((965 + bw_s // 2, t1_y + 286), "HT Android Custom Wallpad · 미니멀 대기화면(Ambient Clock 09:01) 실물 적용", font=get_font(11.5, 'medium'), fill=TEXT_SUB, anchor='mm')

    # Bottom Section: 4-Stage Design Process (y=575..955)
    p_y = 575
    draw_pill(draw, left_x=100, cy=p_y + 14, text="4-STAGE DESIGN PROCESS", font=get_font(10, 'bold'), theme='dark', pad_x=10, height=24)
    draw.text((100, p_y + 42), "사용자에게 친화적이고 유용한 제품을 제공하기 위한 4단계 체계적 리서치 & 설계", font=get_font(16, 'bold'), fill=TEXT_MAIN)

    stages = [
        ("01", "Define", "Understanding Product & Goals",
         "Linux→Android 전환 목표 수립, 건설사 고객 요구사항 정의 및 커스텀 OS 핵심 과업 도출", False),
        ("02", "Discovery", "Analysis, Research & User Flow",
         "K·C·S·L 경쟁사 비교 분석, 3세대 페르소나 심층 인터뷰, 5단계 여정맵 및 멀티디바이스 유스케이스 수립", True),
        ("03", "Design", "Wireframes, Prototyping & Testing",
         "홈 런처·앱 서랍·통화·제어 와이어프레임 설계, 시니어 가독성 및 터치 타깃 사용성 검증", False),
        ("04", "Deliver", "UI Design, System & Animation",
         "HT Android Custom OS 디자인 시스템 규격화, 부팅·로딩 모션 가이드 및 양산 GUI 최종 납품", False)
    ]
    cw = 412
    ch = 268
    cy0 = p_y + 82
    for idx, (num, title, sub, desc, active) in enumerate(stages):
        cx = 100 + idx * (cw + 24)
        fill_c = HT_RED if active else (248, 250, 252)
        out_c = HT_RED if active else BORDER_LIGHT
        t_main = (255, 255, 255) if active else TEXT_MAIN
        t_sub = (255, 228, 234) if active else HT_RED
        t_desc = (255, 241, 244) if active else TEXT_SUB
        num_c = (255, 255, 255) if active else (203, 213, 225)

        draw.rounded_rectangle([cx, cy0, cx + cw, cy0 + ch], radius=16, fill=fill_c, outline=out_c, width=1)
        draw.text((cx + 28, cy0 + 28), title, font=get_font(22, 'black'), fill=t_main)
        draw.text((cx + 28, cy0 + 62), sub, font=get_font(11.5, 'bold'), fill=t_sub)
        draw.line([(cx + 28, cy0 + 90), (cx + cw - 28, cy0 + 90)], fill=(255, 130, 160) if active else BORDER_LIGHT, width=1)
        dlines = wrap_text(desc, get_font(12, 'regular'), cw - 56, draw)
        dy = cy0 + 108
        for l in dlines[:3]:
            draw.text((cx + 28, dy), l, font=get_font(12, 'regular'), fill=t_desc)
            dy += 21
        draw.text((cx + cw - 28, cy0 + ch - 26), num, font=get_font(38, 'black'), fill=num_c, anchor='rb')

    draw_footer(draw, 2)
    img.save(os.path.join(OUT_DIR, "slide_02.png"), quality=95)
    print("Generated slide_02.png")

# -------------------------------------------------------------
# SLIDE 03: COMPETITOR ANALYSIS
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 3, "COMPETITOR ANALYSIS",
        "Competitor Analysis | ", "주요 경쟁 4사(K·C·S·L사) 기능 비교 및 HT 차별화 전략",
        "안드로이드 OS를 도입한 경쟁 월패드 4사의 UX 공백을 진단하고, HT만의 3대 핵심 OS 차별화 기능을 정의했습니다.",
        right_badge=("BENCHMARK MATRIX", "red")
    )

    # Top Matrix Card (y=215..670)
    my, mh = 215, 455
    draw.rounded_rectangle([100, my, 1820, my + mh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_m = draw_pill(draw, left_x=130, cy=my + 36, text="4-COMPANY BENCHMARK MATRIX", font=get_font(10, 'bold'), theme='dark', pad_x=10, height=24)
    draw.text((130 + bw_m + 14, my + 36), "경쟁사(K·C·S·L사) 대비 HT Android Custom OS 핵심 기능 비교", font=get_font(13.5, 'bold'), fill=TEXT_MAIN, anchor='lm')

    cols = ["Company / Function", "K사", "C사", "S사", "L사", "HT Android Custom (Ours)"]
    col_ws = [340, 210, 210, 210, 210, 420]
    gap = 12
    gx = 130
    gy = my + 72

    cur_x = gx
    for idx, (cname, cw) in enumerate(zip(cols, col_ws)):
        is_ht = (idx == 5)
        bg = HT_RED if is_ht else ((30, 41, 59) if idx == 0 else (241, 245, 249))
        tc = (255, 255, 255) if (is_ht or idx == 0) else TEXT_MAIN
        draw.rounded_rectangle([cur_x, gy, cur_x + cw, gy + 54], radius=10, fill=bg)
        draw.text((cur_x + cw // 2, gy + 27), cname, font=get_font(13.5, 'bold'), fill=tc, anchor='mm')
        cur_x += cw + gap

    rows = [
        ("Apply Android OS", "O", "O", "O", "O", "O  ·  Full Custom OS (부팅~런처)"),
        ("APP Drawer (앱 서랍)", "X", "X", "X", "X", "O  ·  3대 카테고리 앱 서랍 최초 도입"),
        ("Common Navigation Bar", "X", "△", "X", "X", "O  ·  전 화면 일관 하단 시스템바"),
        ("Notification System", "△", "△", "△", "△", "O  ·  택배·방문 실시간 통합 알림")
    ]
    ry = gy + 66
    rh = 68
    for r_label, k_v, c_v, s_v, l_v, ht_v in rows:
        vals = [r_label, k_v, c_v, s_v, l_v, ht_v]
        cur_x = gx
        for idx, (val, cw) in enumerate(zip(vals, col_ws)):
            is_ht = (idx == 5)
            if idx == 0:
                bg, bd, tc, fw = (248, 250, 252), BORDER_LIGHT, TEXT_MAIN, 'bold'
            elif is_ht:
                bg, bd, tc, fw = (255, 241, 244), HT_RED, HT_DARK, 'bold'
            else:
                bg = (248, 250, 252)
                bd = BORDER_LIGHT
                tc = (225, 29, 72) if val == "X" else ((217, 119, 6) if val == "△" else (16, 185, 129))
                fw = 'black'
            draw.rounded_rectangle([cur_x, ry, cur_x + cw, ry + rh], radius=10, fill=bg, outline=bd, width=2 if is_ht else 1)
            f_sz = 13 if idx in [0, 5] else 18
            draw.text((cur_x + cw // 2, ry + rh // 2), val, font=get_font(f_sz, fw), fill=tc, anchor='mm')
            cur_x += cw + gap
        ry += rh + 12

    # Bottom 3 Strategic Differentiation Cards (y=695..955)
    sy, sh = 695, 260
    sw = (1720 - 48) // 3
    diffs = [
        ("DIFFERENTIATION 01", "직관적 앱 서랍(App Drawer) 최초 도입",
         "경쟁 4사 모두 복잡한 뎁스 메뉴에 흩어져 있던 전체 기능을 '소통·제어·정보' 3대 카테고리 앱 서랍으로 집약해 1초 만에 탐색 가능하도록 혁신했습니다.", "red"),
        ("DIFFERENTIATION 02", "전 화면 공통 네비게이션바 표준화",
         "앱 전환·홈 복귀·뒤로가기 조작이 제각각이던 기존 월패드 한계를 깨고, 안드로이드 표준 공통 시스템바를 적용해 학습 비용을 제로화했습니다.", "blue"),
        ("DIFFERENTIATION 03", "실시간 통합 알림 센터(Notification)",
         "택배 도착, 부재중 방문자, 에너지 이상 등 생활 핵심 이벤트를 누락 없이 배지(N)와 알림 드로어로 즉각 피드백하도록 고도화했습니다.", "teal")
    ]
    for idx, (bg_t, title, desc, th) in enumerate(diffs):
        sx = 100 + idx * (sw + 24)
        draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=sx + 26, cy=sy + 34, text=bg_t, font=get_font(10, 'bold'), theme=th, pad_x=10, height=22)
        draw.text((sx + 26, sy + 68), title, font=get_font(16, 'bold'), fill=TEXT_MAIN)
        draw.line([(sx + 26, sy + 102), (sx + sw - 26, sy + 102)], fill=BORDER_LIGHT, width=1)
        lines = wrap_text(desc, get_font(12, 'regular'), sw - 52, draw)
        dy = sy + 122
        for l in lines:
            draw.text((sx + 26, dy), l, font=get_font(12, 'regular'), fill=TEXT_SUB)
            dy += 22

    draw_footer(draw, 3)
    img.save(os.path.join(OUT_DIR, "slide_03.png"), quality=95)
    print("Generated slide_03.png")

# -------------------------------------------------------------
# SLIDE 04: USER PERSONAS (3 GENERATIONS)
# -------------------------------------------------------------
def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 4, "USER PERSONAS",
        "User Personas | ", "전 세대(20대~70대) 실사용자 인터뷰 기반 3대 페르소나",
        "실무진·비즈니스 그룹 요구사항과 실제 가정 내 다양한 연령대 사용자 인터뷰를 통해 핵심 Pain Points를 도출했습니다.",
        right_badge=("3-GENERATION UX", "red")
    )

    personas = [
        ("PERSONA 01 · 40대 가장", "김선도", "43세 · IT Planner", '"분석하는게 좋아"', "persona_01.png", "blue",
         "잦은 야근으로 피곤한 몸을 이끌고 집에 돌아와 월패드에서 조명을 제어하려 했으나 메뉴가 보이지 않아 이것저것 눌러보며 불편함을 겪음.",
         ["메뉴 찾기가 어렵고 직관적이지 않음", "메인에서 전체 앱/기능 위치를 한눈에 파악 불가"],
         "홈 위젯 대시보드 + 3대 카테고리 앱 서랍(App Drawer)"),
        ("PERSONA 02 · 20대 대학생", "정지은", "23세 · Student", '"불편한건 못참아"', "persona_02.png", "red",
         "택배기사 공동현관 호출 시 빠르게 버튼을 눌렀으나 터치 인식이 불량해 여러 번 시도. 다른 택배가 도착했음에도 알림이 전혀 뜨지 않음.",
         ["버튼 터치 반응성 및 인식률 저하", "택배 도착 여부 확인 불가 · 통합 알림 부재"],
         "고반응 대형 터치 타깃 + 실시간 배지(N) 통합 알림 시스템"),
        ("PERSONA 03 · 70대 시니어", "조한석", "72세 · Senior", '"새로운건 어려워"', "persona_03.png", "teal",
         "아들 내외가 공동현관에서 호출했을 때 색상이 흐릿하고 글자가 작아 메뉴와 문열기 버튼을 인지하지 못해 결국 직접 문을 열러 나감.",
         ["흐릿한 색상과 작은 텍스트로 가독성 저하", "복잡한 메뉴 구조로 버튼 기능 직관 인지 불가"],
         "WCAG 고대비 컬러 · 원거리 대형 폰트 · 직관 문열기 CTA")
    ]

    cw = 556
    ch = 740
    cy = 215
    for idx, (badge, name, job, quote, av_fn, th, story, pains, sol) in enumerate(personas):
        cx = 100 + idx * (cw + 26)
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=cx + 28, cy=cy + 34, text=badge, font=get_font(10, 'bold'), theme=th, pad_x=10, height=24)

        # Circular Avatar
        av_p = os.path.join(ASSETS_DIR, av_fn)
        if os.path.exists(av_p):
            av = Image.open(av_p).convert('RGBA').resize((88, 88), Image.Resampling.LANCZOS)
            mask = Image.new('L', (88, 88), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, 88, 88], fill=255)
            img.paste(av, (cx + 28, cy + 68), mask)
            draw.ellipse([cx + 28, cy + 68, cx + 116, cy + 156], outline=BORDER_LIGHT, width=2)

        draw.text((cx + 136, cy + 72), name, font=get_font(24, 'bold'), fill=TEXT_MAIN)
        draw.text((cx + 136, cy + 108), job, font=get_font(13, 'medium'), fill=TEXT_SUB)
        accent_c = HT_RED if th == 'red' else (HT_BLUE if th == 'blue' else HT_TEAL)
        draw.text((cx + 136, cy + 134), quote, font=get_font(13, 'bold'), fill=accent_c)

        draw.line([(cx + 28, cy + 178), (cx + cw - 28, cy + 178)], fill=BORDER_LIGHT, width=1)

        # Scenario
        draw.text((cx + 28, cy + 196), "USER SCENARIO", font=get_font(10, 'bold'), fill=TEXT_SUB)
        slines = wrap_text(story, get_font(12, 'regular'), cw - 56, draw)
        sy = cy + 220
        for l in slines[:4]:
            draw.text((cx + 28, sy), l, font=get_font(12, 'regular'), fill=(51, 65, 85))
            sy += 21

        # Pain Points Box
        py = cy + 332
        draw.rounded_rectangle([cx + 28, py, cx + cw - 28, py + 174], radius=12, fill=(255, 241, 244), outline=(254, 205, 211), width=1)
        draw.text((cx + 46, py + 20), "CORE PAIN POINTS", font=get_font(10.5, 'bold'), fill=HT_RED)
        ppy = py + 52
        for p in pains:
            draw.ellipse([cx + 46, ppy + 5, cx + 53, ppy + 12], fill=HT_RED)
            plines = wrap_text(p, get_font(12, 'medium'), cw - 110, draw)
            for pl in plines[:2]:
                draw.text((cx + 62, ppy), pl, font=get_font(12, 'medium'), fill=TEXT_MAIN)
                ppy += 20
            ppy += 14

        # Solution Direction Box
        sol_y = cy + 530
        draw.rounded_rectangle([cx + 28, sol_y, cx + cw - 28, cy + ch - 28], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=cx + 44, cy=sol_y + 28, text="UX SOLUTION", font=get_font(9.5, 'bold'), theme=th, solid=True, pad_x=10, height=22)
        sol_lines = wrap_text(sol, get_font(13, 'bold'), cw - 88, draw)
        sly = sol_y + 58
        for l in sol_lines[:3]:
            draw.text((cx + 44, sly), l, font=get_font(13, 'bold'), fill=TEXT_MAIN)
            sly += 22

    draw_footer(draw, 4)
    img.save(os.path.join(OUT_DIR, "slide_04.png"), quality=95)
    print("Generated slide_04.png")

# -------------------------------------------------------------
# SLIDE 05: USER JOURNEY MAP (5 STEPS - VISITOR CALL TO ENTRY)
# -------------------------------------------------------------
def make_slide_05():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 5, "USER JOURNEY MAP",
        "User Journey Map | ", "방문자 공동현관 호출부터 세대 방문까지 5단계 여정 분석",
        "사용자가 직면하는 약점과 병목 구간을 5단계로 분해하여 감정 곡선과 핵심 UX 전환 기회(Opportunity)를 도출했습니다.",
        right_badge=("5-STEP JOURNEY", "red")
    )

    ly, lh = 215, 745
    draw.rounded_rectangle([100, ly, 1820, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)

    col_ws = [166, 290, 290, 290, 290, 290]
    gap = 10
    gx = 128
    gy = ly + 28

    steps = ["Step", "01. 방문자 호출", "02. 세대주 호출 인지", "03. 세대주 방문자 확인", "04. 세대주 기능 실행", "05. 방문자 세대 방문"]
    cur_x = gx
    for idx, (st, cw) in enumerate(zip(steps, col_ws)):
        bg = HT_RED if idx > 0 else (30, 41, 59)
        draw.rounded_rectangle([cur_x, gy, cur_x + cw, gy + 46], radius=10, fill=bg)
        draw.text((cur_x + cw // 2, gy + 23), st, font=get_font(13, 'bold'), fill=(255, 255, 255), anchor='mm')
        cur_x += cw + gap

    rows = [
        ("Actions\n(행동)", (255, 255, 255), TEXT_MAIN, [
            "방문자가 공동현관에 도착하여 세대 동·호를 호출",
            "세대 월패드에서 초인종이 울려 확인을 위해 이동",
            "화면 식별이 어려워 통화 연결 후 우체국 직원임을 인지",
            "월패드에서 문열기 기능을 실행해 공동현관 개방",
            "공동현관 개방 후 우체국 직원이 세대 현관에 방문"
        ]),
        ("Emotion\n(감정 상태)", (248, 250, 252), TEXT_MAIN, [
            ("보통 · 기대", "teal"),
            ("불편 · 당황", "blue"),
            ("답답 · 혼란", "red"),
            ("불만 · 스트레스", "red"),
            ("안도 · 완료", "teal")
        ]),
        ("Pain Point\n(불편 사항)", (255, 241, 244), HT_DARK, [
            "동·호 오입력 시 전체 취소 후 다시 입력해야 하는 번거로움",
            "화면이 작아 월패드 가까이 다가가야 방문자 식별 가능",
            "스피커 및 마이크 볼륨 조절이 어려워 통화 음질 저하",
            "문열기 버튼이 작고 눈에 띄지 않아 터치 실행에 애로",
            "방문자가 세대현관에 오는 과정을 실시간 확인 불가"
        ]),
        ("Needs\n(사용자 요구)", (239, 246, 255), HT_BLUE, [
            "동·호 오입력 시 이전 숫자만 간편하게 수정할 수 있기를 원함",
            "멀리서도 방문자를 즉시 식별할 수 있는 대화면 표시",
            "통화 중 스피커·마이크 음량을 직관적으로 조절 가능",
            "살짝만 눌러도 잘 열리고 한눈에 보이는 문열기 버튼",
            "초인종을 누르기 전에도 세대현관 사전 모니터링 지원"
        ]),
        ("Opportunity\n(전환 기회)", (240, 253, 244), (4, 120, 87), [
            "백스페이스 개별 수정 키패드 및 오입력 방지 피드백",
            "현관보기 전체 화면(Full-Screen) 자동 확대 모드 제공",
            "스피커·마이크 분리형 직관 볼륨 슬라이더 컨트롤 제공",
            "대형 터치 영역 확장 및 고대비 문열기 CTA 컬러 적용",
            "세대 현관 실시간 CCTV 모니터링 위젯 및 자동 연동"
        ])
    ]

    row_hs = [122, 74, 140, 140, 140]
    ry = gy + 56
    for r_idx, ((rlbl, rbg, rcol, rvals), rh) in enumerate(zip(rows, row_hs)):
        draw.rounded_rectangle([gx, ry, gx + col_ws[0], ry + rh], radius=10, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
        l_parts = rlbl.split('\n')
        draw.text((gx + col_ws[0] // 2, ry + rh // 2 - 11), l_parts[0], font=get_font(12.5, 'bold'), fill=rcol, anchor='mm')
        draw.text((gx + col_ws[0] // 2, ry + rh // 2 + 12), l_parts[1], font=get_font(10.5, 'medium'), fill=TEXT_SUB, anchor='mm')

        cur_x = gx + col_ws[0] + gap
        for v_idx, val in enumerate(rvals):
            cw = col_ws[v_idx + 1]
            draw.rounded_rectangle([cur_x, ry, cur_x + cw, ry + rh], radius=10, fill=rbg, outline=BORDER_LIGHT, width=1)
            if r_idx == 1:
                em_txt, em_th = val
                draw_pill(draw, cx=cur_x + cw // 2, cy=ry + rh // 2, text=em_txt, font=get_font(11.5, 'bold'), theme=em_th, solid=(em_th == 'red'), pad_x=16, height=32)
            else:
                lines = wrap_text(val, get_font(11.5, 'medium' if r_idx == 4 else 'regular'), cw - 28, draw)
                vy = ry + (rh - len(lines) * 20) // 2 + 10
                for l in lines:
                    draw.text((cur_x + cw // 2, vy), l, font=get_font(11.5, 'medium' if r_idx == 4 else 'regular'), fill=TEXT_MAIN, anchor='mm')
                    vy += 20
            cur_x += cw + gap
        ry += rh + 10

    draw_footer(draw, 5)
    img.save(os.path.join(OUT_DIR, "slide_05.png"), quality=95)
    print("Generated slide_05.png")

# -------------------------------------------------------------
# SLIDE 06: MULTI-DEVICE USE CASE MATRIX
# -------------------------------------------------------------
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 6, "MULTI-DEVICE USE CASE",
        "System Use Case | ", "도어폰 · 로비폰 · 이마주 2.0 앱 · 월패드 4대 기기 연동 시나리오",
        "사용자 행위에 맞춰 스마트홈 생태계 내 4대 디바이스가 실시간으로 상호작용하는 시스템 역할 매트릭스를 정립했습니다.",
        right_badge=("CROSS-DEVICE SYNC", "red")
    )

    my, mh = 215, 745
    draw.rounded_rectangle([100, my, 1820, my + mh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_u = draw_pill(draw, left_x=130, cy=my + 34, text="END-TO-END SYSTEM INTERACTION MATRIX", font=get_font(10, 'bold'), theme='red', pad_x=10, height=24)
    draw.text((130 + bw_u + 14, my + 34), "OS 부팅(Booting)부터 공동현관 호출·방문자 확인·문열기까지 4대 시스템 역할 정의", font=get_font(13, 'bold'), fill=TEXT_MAIN, anchor='lm')

    cols = ["No.", "구분 / 항목", "사용자", "핵심 시나리오", "도어폰 · 로비폰", "모바일 앱 (이마주 2.0)", "HT Android 월패드 (Core)"]
    col_ws = [56, 174, 86, 320, 260, 340, 380]
    gap = 8
    gx = 130
    gy = my + 66

    cur_x = gx
    for idx, (cname, cw) in enumerate(zip(cols, col_ws)):
        bg = HT_RED if idx == 6 else (30, 41, 59)
        draw.rounded_rectangle([cur_x, gy, cur_x + cw, gy + 44], radius=8, fill=bg)
        draw.text((cur_x + cw // 2, gy + 22), cname, font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
        cur_x += cw + gap

    use_cases = [
        ("01", "월패드 시작\nBooting", "입주민",
         "월패드 전원을 켜면 화면에서 HT 브랜드 로고 애니메이션이 표시됨",
         "대기 상태 (연동 없음)", "대기 상태 (연동 없음)",
         "안드로이드 커스텀 OS 커널 및 시스템 서비스 부팅 로딩"),
        ("02", "월패드 시작\nInitialData", "입주민",
         "UI 로딩 인디케이터가 표시되며 초기 환경 데이터를 수신",
         "대기 상태 (연동 없음)", "대기 상태 (연동 없음)",
         "홈 런처 시작에 필요한 UI 위젯 및 초기 데이터 서버 동기화"),
        ("03", "월패드 시작\nHome Launcher", "입주민",
         "모든 정보가 로드된 홈 런처를 확인하고 원하는 스마트홈 기능 실행",
         "네트워크 연동 대기", "세대 기기 상태 동기화",
         "모든 위젯·제어 모듈 로드 완료 · 전체 스마트홈 기능 활성"),
        ("04", "세대 방문\n공동현관 호출", "방문자",
         "방문자가 아파트 공동현관 로비폰에서 방문할 세대 동·호를 호출",
         "로비폰: 동/호 입력 후 해당 세대로 실시간 화상 호출 발신",
         "푸시 알림 및 모바일 화상 호출 수신 대기",
         "초인종 사운드 출력 및 공동현관 호출 팝업 자동 전환"),
        ("05", "세대 방문\n방문자 확인", "입주민",
         "월패드 또는 이마주 2.0 앱에서 방문자 영상을 확인하고 문열기 실행",
         "로비폰: 입주민 통화 수락 시 양방향 스피커 통화 및 문열림",
         "로비폰 카메라 영상 수신 · 통화 수락 · 원격 문열기 실행 후 복귀",
         "고화질 방문자 영상 수신 · 대형 문열기 CTA 실행 · 초기화면 자동 복귀")
    ]

    ry = gy + 54
    rh = 108
    for row in use_cases:
        cur_x = gx
        for idx, (val, cw) in enumerate(zip(row, col_ws)):
            is_wp = (idx == 6)
            bg = (255, 241, 244) if is_wp else ((248, 250, 252) if idx in [0, 1, 2] else (255, 255, 255))
            bd = HT_RED if is_wp else BORDER_LIGHT
            draw.rounded_rectangle([cur_x, ry, cur_x + cw, ry + rh], radius=8, fill=bg, outline=bd, width=2 if is_wp else 1)
            if idx == 0:
                draw.text((cur_x + cw // 2, ry + rh // 2), val, font=get_font(13, 'black'), fill=HT_RED, anchor='mm')
            elif idx == 1:
                pts = val.split('\n')
                draw.text((cur_x + cw // 2, ry + rh // 2 - 11), pts[0], font=get_font(10.5, 'medium'), fill=TEXT_SUB, anchor='mm')
                draw.text((cur_x + cw // 2, ry + rh // 2 + 11), pts[1], font=get_font(12, 'bold'), fill=TEXT_MAIN, anchor='mm')
            elif idx == 2:
                draw_pill(draw, cx=cur_x + cw // 2, cy=ry + rh // 2, text=val, font=get_font(10, 'bold'), theme='blue' if val == '방문자' else 'dark', pad_x=8, height=22)
            else:
                lines = wrap_text(val, get_font(11, 'bold' if is_wp else 'regular'), cw - 24, draw)
                vy = ry + (rh - len(lines) * 18) // 2 + 9
                for l in lines[:4]:
                    draw.text((cur_x + 12, vy), l, font=get_font(11, 'bold' if is_wp else 'regular'), fill=HT_DARK if is_wp else TEXT_MAIN, anchor='lm')
                    vy += 18
            cur_x += cw + gap
        ry += rh + 10

    draw_footer(draw, 6)
    img.save(os.path.join(OUT_DIR, "slide_06.png"), quality=95)
    print("Generated slide_06.png")

# -------------------------------------------------------------
# SLIDE 07: INFORMATION ARCHITECTURE & USER FLOW
# -------------------------------------------------------------
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 7, "IA & USER FLOW",
        "Information Architecture & User Flow | ", "3대 생활 도메인 15개 모듈 IA 및 방문자 응대 플로우",
        "최소한의 인지 부하로 원하는 기능에 접근하는 '홈(런처)-앱스(서랍)' 계층 구조와 공동현관~세대현관 엔드투엔드 플로우",
        right_badge=("ARCHITECTURE & FLOW", "red")
    )

    cy, ch = 215, 745
    # LEFT: IA TREE (x=100, w=880)
    lx, lw = 100, 880
    draw.rounded_rectangle([lx, cy, lx + lw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_ia = draw_pill(draw, left_x=lx + 26, cy=cy + 34, text="INFORMATION ARCHITECTURE", font=get_font(10, 'bold'), theme='red', pad_x=10, height=24)
    draw.text((lx + 26 + bw_ia + 12, cy + 34), "홈(런처) ↔ 앱스(서랍) 기반 3대 도메인 15개 핵심 기능", font=get_font(13, 'bold'), fill=TEXT_MAIN, anchor='lm')

    # Root Nodes on left of IA card
    rx0 = lx + 34
    draw.rounded_rectangle([rx0, cy + 160, rx0 + 130, cy + 216], radius=10, fill=(248, 250, 252), outline=TEXT_MAIN, width=2)
    draw.text((rx0 + 65, cy + 188), "앱스 (서랍)", font=get_font(13, 'bold'), fill=TEXT_MAIN, anchor='mm')

    draw.rounded_rectangle([rx0, cy + 320, rx0 + 130, cy + 380], radius=30, fill=TEXT_MAIN)
    draw.text((rx0 + 65, cy + 350), "홈 (런처)", font=get_font(13.5, 'bold'), fill=(255, 255, 255), anchor='mm')

    draw.line([(rx0 + 65, cy + 216), (rx0 + 65, cy + 320)], fill=(148, 163, 184), width=2)
    spine_x = rx0 + 166
    draw.line([(rx0 + 130, cy + 188), (spine_x, cy + 188)], fill=(148, 163, 184), width=2)
    draw.line([(rx0 + 130, cy + 350), (spine_x, cy + 350)], fill=(148, 163, 184), width=2)
    draw.line([(spine_x, cy + 150), (spine_x, cy + 560)], fill=(148, 163, 184), width=2)

    domains = [
        ("소통", (224, 231, 255), HT_BLUE, ["현관보기", "세대통화", "일반전화", "경비실", "메모"]),
        ("제어", (255, 237, 213), (234, 88, 12), ["가스", "조명", "난방", "방범", "엘리베이터"]),
        ("정보", (204, 251, 241), HT_TEAL, ["택배", "방문", "차량", "에너지", "CCTV"])
    ]
    dom_ys = [cy + 150, cy + 355, cy + 560]
    for (d_name, d_bg, d_col, items), dy in zip(domains, dom_ys):
        draw.line([(spine_x, dy), (spine_x + 32, dy)], fill=(148, 163, 184), width=2)
        bx = spine_x + 32
        draw.rounded_rectangle([bx, dy - 26, bx + 110, dy + 26], radius=26, fill=d_bg, outline=d_col, width=2)
        draw.text((bx + 55, dy), d_name, font=get_font(14, 'bold'), fill=d_col, anchor='mm')

        # 5 sub-item chips in a clean horizontal row
        sub_x0 = bx + 132
        draw.line([(bx + 110, dy), (sub_x0, dy)], fill=(203, 213, 225), width=2)
        iw = 96
        igap = 8
        for s_idx, it in enumerate(items):
            ix = sub_x0 + s_idx * (iw + igap)
            draw.rounded_rectangle([ix, dy - 30, ix + iw, dy + 30], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
            draw.text((ix + iw // 2, dy), it, font=get_font(12, 'bold'), fill=TEXT_MAIN, anchor='mm')

    # Bottom IA Summary
    draw.rounded_rectangle([lx + 26, cy + ch - 72, lx + lw - 26, cy + ch - 22], radius=10, fill=(255, 241, 244), outline=(254, 205, 211), width=1)
    draw.text((lx + lw // 2, cy + ch - 47), "홈 런처(위젯+자주 쓰는 기능)와 3대 카테고리 앱 서랍을 분리해 메뉴 탐색 깊이(Depth)를 2단계 이내로 단축", font=get_font(11.5, 'bold'), fill=HT_DARK, anchor='mm')

    # RIGHT: USER FLOW DIAGRAM (x=1000, w=820)
    rx, rw = 1000, 820
    draw.rounded_rectangle([rx, cy, rx + rw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_uf = draw_pill(draw, left_x=rx + 26, cy=cy + 34, text="USER FLOW · VISITOR ACCESS", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((rx + 26 + bw_uf + 12, cy + 34), "공동현관 호출 → 세대현관 개방 의사결정 플로우", font=get_font(13, 'bold'), fill=TEXT_MAIN, anchor='lm')

    def draw_node(x, y, w, h, txt, fill=(248, 250, 252), bd=TEXT_MAIN, tc=TEXT_MAIN, rad=10):
        draw.rounded_rectangle([x, y, x + w, y + h], radius=rad, fill=fill, outline=bd, width=2)
        lines = txt.split('\n')
        ny = y + (h - len(lines) * 18) // 2 + 9
        for l in lines:
            draw.text((x + w // 2, ny), l, font=get_font(11.5, 'bold'), fill=tc, anchor='mm')
            ny += 18

    def draw_diamond(cx_d, cy_d, hw, hh, txt):
        pts = [(cx_d, cy_d - hh), (cx_d + hw, cy_d), (cx_d, cy_d + hh), (cx_d - hw, cy_d)]
        draw.polygon(pts, fill=(255, 241, 244), outline=HT_RED, width=2)
        lines = txt.split('\n')
        ny = cy_d - (len(lines) - 1) * 9
        for l in lines:
            draw.text((cx_d, ny), l, font=get_font(10.5, 'bold'), fill=HT_DARK, anchor='mm')
            ny += 18

    def draw_arr(p1, p2, col=(100, 116, 139)):
        draw.line([p1, p2], fill=col, width=2)
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2:
            if y2 > y1:
                draw.polygon([(x2 - 5, y2 - 8), (x2 + 5, y2 - 8), (x2, y2)], fill=col)
            else:
                draw.polygon([(x2 - 5, y2 + 8), (x2 + 5, y2 + 8), (x2, y2)], fill=col)
        else:
            if x2 > x1:
                draw.polygon([(x2 - 8, y2 - 5), (x2 - 8, y2 + 5), (x2, y2)], fill=col)

    # Row 1: Start -> Lobby Call -> Screen Check -> Lobby Open
    fy1 = cy + 105
    draw_node(rx + 36, fy1, 130, 56, "세대방문 시작", fill=TEXT_MAIN, bd=TEXT_MAIN, tc=(255, 255, 255), rad=28)
    draw_arr((rx + 166, fy1 + 28), (rx + 206, fy1 + 28))
    draw_node(rx + 206, fy1, 155, 56, "방문자 공동현관\n세대 호 호출")
    draw_arr((rx + 361, fy1 + 28), (rx + 404, fy1 + 28))
    draw_diamond(rx + 474, fy1 + 28, 70, 44, "월패드\n화면 확인?")
    draw_arr((rx + 544, fy1 + 28), (rx + 602, fy1 + 28), col=HT_RED)
    draw.text((rx + 572, fy1 + 14), "YES", font=get_font(9.5, 'bold'), fill=HT_RED, anchor='mm')
    draw_node(rx + 602, fy1, 182, 56, "세대주 월패드\n공동현관 열림", fill=(239, 246, 255), bd=HT_BLUE, tc=HT_BLUE)

    # Branch N -> Voice Check -> Lobby Open
    fy2 = cy + 245
    draw_arr((rx + 474, fy1 + 72), (rx + 474, fy2 - 44))
    draw.text((rx + 492, fy1 + 88), "NO", font=get_font(9.5, 'bold'), fill=TEXT_SUB, anchor='mm')
    draw_diamond(rx + 474, fy2, 70, 44, "월패드\n통화 확인?")
    draw.line([(rx + 544, fy2), (rx + 693, fy2)], fill=HT_BLUE, width=2)
    draw_arr((rx + 693, fy2), (rx + 693, fy1 + 56), col=HT_BLUE)
    draw.text((rx + 615, fy2 - 14), "YES (통화 승인)", font=get_font(9.5, 'bold'), fill=HT_BLUE, anchor='mm')

    # Row 3: Door Call -> Door Screen Check -> Door Open
    fy3 = cy + 375
    draw_arr((rx + 693, fy1 + 56), (rx + 693, fy3 - 30))  # visual flow continuation
    draw_node(rx + 602, fy3 - 28, 182, 56, "방문자 세대현관\n초인종 호출", fill=(248, 250, 252), bd=TEXT_MAIN)

    fy4 = cy + 495
    draw_arr((rx + 693, fy3 + 28), (rx + 693, fy4 - 44))
    draw_diamond(rx + 693, fy4, 72, 44, "세대현관\n화면/통화?")

    draw_arr((rx + 621, fy4), (rx + 556, fy4), col=HT_TEAL)
    draw.text((rx + 588, fy4 - 14), "YES", font=get_font(9.5, 'bold'), fill=HT_TEAL, anchor='mm')
    draw_node(rx + 360, fy4 - 28, 196, 56, "세대현관 열림 및\n방문자 안전 대면", fill=(240, 253, 250), bd=HT_TEAL, tc=HT_TEAL)

    # Reject branch (routed cleanly to the left without crossing any box!)
    fy5 = cy + 610
    draw.line([(rx + 404, fy2), (rx + 235, fy2)], fill=(148, 163, 184), width=2)
    draw.text((rx + 320, fy2 - 14), "NO (미응답)", font=get_font(9.5, 'bold'), fill=TEXT_SUB, anchor='mm')
    draw_arr((rx + 235, fy2), (rx + 235, fy5), col=(148, 163, 184))
    draw_node(rx + 150, fy5, 170, 52, "호출 거절 / 미응답", fill=(241, 245, 249), bd=(148, 163, 184), tc=TEXT_SUB)
    draw.line([(rx + 458, fy4 + 28), (rx + 458, fy5 + 26)], fill=HT_TEAL, width=2)
    draw_arr((rx + 458, fy5 + 26), (rx + 580, fy5 + 26), col=HT_TEAL)
    draw_node(rx + 580, fy5, 180, 52, "세대방문 종료", fill=TEXT_MAIN, bd=TEXT_MAIN, tc=(255, 255, 255), rad=26)
    draw_arr((rx + 693, fy4 + 44), (rx + 693, fy5), col=(148, 163, 184))
    draw.text((rx + 716, fy4 + 58), "NO", font=get_font(9.5, 'bold'), fill=TEXT_SUB, anchor='mm')

    draw_footer(draw, 7)
    img.save(os.path.join(OUT_DIR, "slide_07.png"), quality=95)
    print("Generated slide_07.png")

# -------------------------------------------------------------
# SLIDE 08: WIREFRAMES & MULTI-SCREEN ARCHITECTURE
# -------------------------------------------------------------
def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 8, "WIREFRAMES & MULTI-SCREEN",
        "Wireframe Architecture | ", "홈 런처 · 앱 서랍 · 통화 · 메모 · 제어 멀티스크린 와이어프레임",
        "사업담당자·PM·개발자·디자이너 간 원활한 소통과 개발 완성도를 높이기 위해 6대 핵심 화면의 상세 와이어프레임을 구축했습니다.",
        right_badge=("6-SCREEN WIREFRAMES", "red")
    )

    cy, ch = 215, 745
    # Left Main Showcase: Authentic Uploaded 6-Screen Wireframe Board (x=100, w=1160)
    lx, lw = 100, 1160
    draw.rounded_rectangle([lx, cy, lx + lw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_w = draw_pill(draw, left_x=lx + 26, cy=cy + 34, text="AUTHENTIC MULTI-SCREEN WIREFRAMES", font=get_font(10, 'bold'), theme='dark', pad_x=10, height=24)
    draw.text((lx + 26 + bw_w + 14, cy + 34), "홈 대시보드 · 오류 예외처리 · 3대 카테고리 앱 서랍 · 통화 · 메모 · 기기 제어 실물", font=get_font(13, 'bold'), fill=TEXT_MAIN, anchor='lm')

    wf_path = os.path.join(ASSETS_DIR, "07_wireframes.png")
    if os.path.exists(wf_path):
        wf = Image.open(wf_path).convert('RGBA')
        # Crop out the top "Wireframes" title area from 07_wireframes.png (y=170..576) to show the 6 wireframe screens crisp & large!
        wf_crop = wf.crop((0, 165, wf.width, wf.height))
        inner_w, inner_h = lw - 48, ch - 104
        scale = min(inner_w / wf_crop.width, inner_h / wf_crop.height)
        tw, th = int(wf_crop.width * scale), int(wf_crop.height * scale)
        wf_res = wf_crop.resize((tw, th), Image.Resampling.LANCZOS)
        px = lx + (lw - tw) // 2
        py = cy + 72 + (inner_h - th) // 2
        img.paste(wf_res, (px, py), wf_res)
        draw.rounded_rectangle([px - 4, py - 4, px + tw + 4, py + th + 4], radius=10, outline=BORDER_LIGHT, width=1)

    # Right Column: 3 Core Wireframe Architecture Specs (x=1285, w=535)
    rx, rw = 1285, 535
    draw.rounded_rectangle([rx, cy, rx + rw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=rx + 26, cy=cy + 34, text="KEY UX ARCHITECTURE", font=get_font(10, 'bold'), theme='red', pad_x=10, height=24)
    draw.text((rx + 26, cy + 66), "멀티스크린 와이어프레임 설계 핵심", font=get_font(18, 'bold'), fill=TEXT_MAIN)

    wf_specs = [
        ("01. 위젯 기반 홈 런처 & 예외처리", "red",
         "좌측 날씨·EMS(전기·수도·가스) 실시간 게이지와 우측 6대 퀵 아이콘(N 배지 알림)을 한 화면에 배치하고, 서버 통신 오류 시 대체 안내 UI까지 완벽 설계했습니다."),
        ("02. 3대 카테고리 앱 서랍(App Drawer)", "blue",
         "소통(현관·통화·경비실·메모), 제어(조명·가스·난방·방범·엘리베이터), 정보(택배·방문·차량·에너지)를 3행 그리드로 정렬해 탐색 시간을 최소화했습니다."),
        ("03. 고시인성 통화·메모·제어 서브 뷰", "teal",
         "세대현관·공동현관·경비실 탭 전환 통화 UI, 우측 볼륨 컨트롤바, 직관적인 메모 목록 및 기기별 대형 온/오프 버튼을 일관된 하단 시스템바로 통합했습니다.")
    ]
    sy = cy + 114
    for title, th, desc in wf_specs:
        draw.rounded_rectangle([rx + 24, sy, rx + rw - 24, sy + 188], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=rx + 40, cy=sy + 28, text=title, font=get_font(11, 'bold'), theme=th, pad_x=10, height=24)
        lines = wrap_text(desc, get_font(12, 'regular'), rw - 80, draw)
        dy = sy + 60
        for l in lines[:5]:
            draw.text((rx + 40, dy), l, font=get_font(12, 'regular'), fill=(51, 65, 85))
            dy += 22
        sy += 204

    draw_footer(draw, 8)
    img.save(os.path.join(OUT_DIR, "slide_08.png"), quality=95)
    print("Generated slide_08.png")

# -------------------------------------------------------------
# SLIDE 09: DESIGN SYSTEM & UNIVERSAL UX TOKENS
# -------------------------------------------------------------
def _draw_smarthome_icon(draw, cx, cy, kind, col):
    if kind == 'door':
        draw.rounded_rectangle([cx - 8, cy - 11, cx + 8, cy + 11], radius=2, outline=col, width=2)
        draw.ellipse([cx + 2, cy - 1, cx + 5, cy + 2], fill=col)
    elif kind == 'guard':
        draw.ellipse([cx - 6, cy - 10, cx + 6, cy + 2], outline=col, width=2)
        draw.arc([cx - 10, cy + 2, cx + 10, cy + 16], start=180, end=360, fill=col, width=2)
    elif kind == 'lock':
        draw.rounded_rectangle([cx - 9, cy - 2, cx + 9, cy + 10], radius=3, outline=col, width=2)
        draw.arc([cx - 6, cy - 10, cx + 6, cy + 2], start=180, end=360, fill=col, width=2)
    elif kind == 'elev':
        draw.rounded_rectangle([cx - 9, cy - 10, cx + 9, cy + 10], radius=2, outline=col, width=2)
        draw.polygon([(cx - 4, cy - 2), (cx, cy - 6), (cx + 4, cy - 2)], fill=col)
        draw.polygon([(cx - 4, cy + 2), (cx, cy + 6), (cx + 4, cy + 2)], fill=col)
    elif kind == 'bulb':
        draw.ellipse([cx - 7, cy - 10, cx + 7, cy + 4], outline=col, width=2)
        draw.line([(cx - 4, cy + 7), (cx + 4, cy + 7)], fill=col, width=2)
        draw.line([(cx - 3, cy + 10), (cx + 3, cy + 10)], fill=col, width=2)
    elif kind == 'energy':
        draw.polygon([(cx + 1, cy - 11), (cx - 7, cy + 1), (cx, cy + 1), (cx - 1, cy + 11), (cx + 7, cy - 1), (cx, cy - 1)], outline=col, width=2)
    elif kind == 'box':
        draw.rounded_rectangle([cx - 9, cy - 8, cx + 9, cy + 9], radius=2, outline=col, width=2)
        draw.line([(cx - 9, cy - 2), (cx + 9, cy - 2)], fill=col, width=2)
        draw.line([(cx, cy - 8), (cx, cy - 2)], fill=col, width=2)
    elif kind == 'cctv':
        draw.rounded_rectangle([cx - 10, cy - 6, cx + 6, cy + 5], radius=2, outline=col, width=2)
        draw.polygon([(cx + 6, cy - 3), (cx + 11, cy - 6), (cx + 11, cy + 4), (cx + 6, cy + 1)], outline=col, width=2)

def make_slide_09():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 9, "DESIGN SYSTEM · UNIVERSAL UX",
        "Design System | ", "3세대 가족의 원거리 가독성을 보장하는 월패드 디자인 시스템",
        "어두운 거실·밝은 낮 환경 모두에서 시니어부터 청년까지 오작동 없이 제어하는 고대비 다크 서피스 및 아토믹 UI 토큰",
        right_badge=("HT CUSTOM UI KIT", "red")
    )

    cy, ch = 215, 745
    # COL 1: TYPOGRAPHY & READABILITY (x=100, w=520)
    c1_x, c1_w = 100, 520
    draw.rounded_rectangle([c1_x, cy, c1_x + c1_w, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=c1_x + 24, cy=cy + 34, text="FOUNDATION 01 · TYPOGRAPHY", font=get_font(10, 'bold'), theme='red', pad_x=10, height=24)
    draw.text((c1_x + 24, cy + 66), "원거리 시인성 타이포그래피 스케일", font=get_font(18, 'bold'), fill=TEXT_MAIN)
    draw.text((c1_x + 24, cy + 92), "벽면 부착 1.5m 시거리 기준 시니어 가독성 최적화", font=get_font(11.5, 'regular'), fill=TEXT_SUB)

    typos = [
        ("Clock 64", "64sp / Light", "대기화면 시계(09:01) & 온도(25°)", 20, HT_RED),
        ("Widget 36", "36sp / Bold", "HEMS 에너지 사용량(20,654) 핵심 수치", 17, HT_BLUE),
        ("Title 24", "24sp / Bold", "서브 앱 헤더 및 통화 대상지 명칭", 15, TEXT_MAIN),
        ("Action 18", "18sp / Bold", "문열기·통화 등 핵심 CTA 버튼 라벨", 13.5, HT_RED),
        ("Body 16", "16sp / Medium", "앱 서랍 아이콘 명칭 및 제어 상태 텍스트", 12.5, TEXT_SUB),
        ("Caption 13", "13sp / Regular", "날짜·미세먼지·시스템바 보조 메타 정보", 11, (148, 163, 184))
    ]
    ty = cy + 126
    for i, (tn, ts, tu, fsz, col) in enumerate(typos):
        bg = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rounded_rectangle([c1_x + 20, ty, c1_x + c1_w - 20, ty + 88], radius=10, fill=bg, outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([c1_x + 28, ty + 14, c1_x + 32, ty + 74], radius=2, fill=col)
        draw.text((c1_x + 42, ty + 16), tn, font=get_font(fsz, 'bold'), fill=TEXT_MAIN)
        draw_pill(draw, left_x=c1_x + c1_w - 134, cy=ty + 26, text=ts, font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
        draw.text((c1_x + 42, ty + 54), tu, font=get_font(11, 'regular'), fill=TEXT_SUB)
        ty += 98

    # COL 2: COLOR SYSTEM & 8 SMART HOME ICONS (x=640, w=600)
    c2_x, c2_w = 640, 600
    draw.rounded_rectangle([c2_x, cy, c2_x + c2_w, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=c2_x + 24, cy=cy + 34, text="FOUNDATION 02 · COLOR & ICONS", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((c2_x + 24, cy + 66), "고대비 다크 서피스 & 스마트홈 아이콘", font=get_font(18, 'bold'), fill=TEXT_MAIN)
    draw.text((c2_x + 24, cy + 92), "HT 시그니처 크림슨 및 8대 핵심 IoT 기능별 컬러 코딩", font=get_font(11.5, 'regular'), fill=TEXT_SUB)

    colors = [
        ("HT Crimson", "#F40044", (244, 0, 68)),
        ("Wallpad Dark", "#0F172A", (15, 23, 42)),
        ("Card Glass", "#1E293B", (30, 41, 59)),
        ("IoT Blue", "#3B82F6", (59, 130, 246)),
        ("Security Org", "#F97316", (249, 115, 22)),
        ("Info Teal", "#14B8A6", (20, 184, 166)),
        ("Success Grn", "#10B981", (16, 185, 129)),
        ("Alert Amber", "#F59E0B", (245, 158, 11)),
        ("Text Light", "#F8FAFC", (248, 250, 252)),
        ("Divider", "#CBD5E1", (203, 213, 225)),
    ]
    sw_w, sw_h = 104, 86
    for idx, (cn, chx, rgb) in enumerate(colors):
        r, c = idx // 5, idx % 5
        bx = c2_x + 20 + c * (sw_w + 10)
        by = cy + 124 + r * (sw_h + 10)
        draw.rounded_rectangle([bx, by, bx + sw_w, by + sw_h], radius=10, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([bx + 8, by + 8, bx + sw_w - 8, by + 38], radius=6, fill=rgb, outline=(203, 213, 225) if cn == "Text Light" else None, width=1)
        draw.text((bx + 8, by + 46), cn, font=get_font(9.5, 'bold'), fill=TEXT_MAIN)
        draw.text((bx + 8, by + 63), chx, font=get_font(9, 'medium'), fill=TEXT_SUB)

    div_y = cy + 322
    draw.line([(c2_x + 20, div_y), (c2_x + c2_w - 20, div_y)], fill=BORDER_LIGHT, width=1)
    bw_ic = draw_pill(draw, left_x=c2_x + 20, cy=div_y + 24, text="SMART HOME 24dp ICONS", font=get_font(9.5, 'bold'), theme='red', pad_x=10, height=20)
    draw.text((c2_x + 20 + bw_ic + 12, div_y + 24), "카테고리별 컬러 코딩 8대 핵심 아이콘", font=get_font(11.5, 'bold'), fill=TEXT_MAIN, anchor='lm')

    icons = [
        ("현관보기", "ic_front_door", "door", (99, 102, 241)),
        ("경비실", "ic_security_call", "guard", (59, 130, 246)),
        ("방범·보안", "ic_home_lock", "lock", (249, 115, 22)),
        ("엘리베이터", "ic_elevator", "elev", (234, 88, 12)),
        ("조명 제어", "ic_light_ctrl", "bulb", (245, 158, 11)),
        ("HEMS 에너지", "ic_hems_power", "energy", HT_RED),
        ("택배 알림", "ic_parcel_box", "box", HT_TEAL),
        ("세대 CCTV", "ic_cctv_live", "cctv", (16, 185, 129))
    ]
    ic_w, ic_h = 132, 134
    for idx, (lbl, tok, knd, col) in enumerate(icons):
        r, c = idx // 4, idx % 4
        ix = c2_x + 20 + c * (ic_w + 10)
        iy = div_y + 48 + r * (ic_h + 12)
        draw.rounded_rectangle([ix, iy, ix + ic_w, iy + ic_h], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([ix + ic_w // 2 - 22, iy + 18, ix + ic_w // 2 + 22, iy + 62], radius=12, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        _draw_smarthome_icon(draw, ix + ic_w // 2, iy + 40, knd, col)
        draw.text((ix + ic_w // 2, iy + 82), lbl, font=get_font(11.5, 'bold'), fill=TEXT_MAIN, anchor='mm')
        draw.text((ix + ic_w // 2, iy + 102), tok, font=get_font(8.5, 'medium'), fill=col, anchor='mm')
        draw.text((ix + ic_w // 2, iy + 118), "48dp Touch · 24dp", font=get_font(8, 'regular'), fill=(148, 163, 184), anchor='mm')

    # COL 3: TOUCH ERGONOMICS & COMPONENT KIT (x=1260, w=560)
    c3_x, c3_w = 1260, 560
    draw.rounded_rectangle([c3_x, cy, c3_x + c3_w, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=c3_x + 24, cy=cy + 34, text="FOUNDATION 03 · ERGONOMICS", font=get_font(10, 'bold'), theme='teal', pad_x=10, height=24)
    draw.text((c3_x + 24, cy + 66), "월패드 터치 인체공학 & 컴포넌트 규격", font=get_font(18, 'bold'), fill=TEXT_MAIN)
    draw.text((c3_x + 24, cy + 92), "오터치 방지 56dp+ 대형 타깃 및 공통 시스템바 규격", font=get_font(11.5, 'regular'), fill=TEXT_SUB)

    # Dark Wallpad Preview Card inside Col 3
    dk_y = cy + 126
    draw.rounded_rectangle([c3_x + 24, dk_y, c3_x + c3_w - 24, dk_y + 276], radius=14, fill=(15, 23, 42))
    draw_pill(draw, left_x=c3_x + 42, cy=dk_y + 28, text="DARK SURFACE COMPONENT KIT", font=get_font(9.5, 'bold'), theme='red', solid=True, pad_x=10, height=22)

    # Primary CTA Row
    draw.rounded_rectangle([c3_x + 42, dk_y + 58, c3_x + 266, dk_y + 110], radius=12, fill=HT_RED)
    draw.text((c3_x + 154, dk_y + 84), "공동현관 문열기 (Primary)", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.rounded_rectangle([c3_x + 282, dk_y + 58, c3_x + c3_w - 42, dk_y + 110], radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    draw.text((c3_x + 400, dk_y + 84), "통화 연결 / 종료", font=get_font(12, 'bold'), fill=(248, 250, 252), anchor='mm')

    # Notification Badge Row
    draw.rounded_rectangle([c3_x + 42, dk_y + 128, c3_x + c3_w - 42, dk_y + 186], radius=12, fill=(30, 41, 59))
    draw.ellipse([c3_x + 60, dk_y + 145, c3_x + 84, dk_y + 169], fill=HT_RED)
    draw.text((c3_x + 72, dk_y + 157), "N", font=get_font(11, 'black'), fill=(255, 255, 255), anchor='mm')
    draw.text((c3_x + 98, dk_y + 147), "실시간 통합 알림 배지 (택배·방문자)", font=get_font(12, 'bold'), fill=(248, 250, 252))
    draw.text((c3_x + 98, dk_y + 167), "미확인 이벤트 발생 시 런처 아이콘 우상단 즉시 표시", font=get_font(10, 'regular'), fill=(148, 163, 184))

    # Common System Navigation Bar Demo
    draw.rounded_rectangle([c3_x + 42, dk_y + 206, c3_x + c3_w - 42, dk_y + 256], radius=10, fill=(8, 12, 22), outline=(51, 65, 85), width=1)
    nav_labels = ["← 뒤로가기", "● 홈 (런처)", "≡ 앱 서랍", "알림 센터"]
    nw = (c3_w - 84) // 4
    for ni, nl in enumerate(nav_labels):
        draw.text((c3_x + 42 + ni * nw + nw // 2, dk_y + 231), nl, font=get_font(11, 'bold'), fill=HT_RED if ni == 1 else (203, 213, 225), anchor='mm')

    # Bottom Ergonomic Spec Cards
    erg_y = dk_y + 298
    erg_specs = [
        ("MINIMUM TOUCH TARGET", "56 × 56 dp 이상 대형 터치 영역", "20대 빠른 터치와 70대 시니어 오터치를 동시 방지하는 물리 버튼급 타깃 규격"),
        ("CONTRAST RATIO", "WCAG 2.1 AAA (8.5:1) 초고대비", "거실 직사광선 및 야간 소등 환경 모두에서 즉각 판독되는 다크 글래스 대비"),
        ("OS CONSISTENCY", "전 화면 공통 하단 시스템바 고정", "어떤 앱에 진입해도 1-Tap으로 홈·이전·앱서랍으로 복귀하는 제로 미아 구조")
    ]
    for et, ev, ed in erg_specs:
        draw.rounded_rectangle([c3_x + 24, erg_y, c3_x + c3_w - 24, erg_y + 92], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((c3_x + 40, erg_y + 16), et, font=get_font(9.5, 'bold'), fill=HT_RED)
        draw.text((c3_x + 40, erg_y + 36), ev, font=get_font(13, 'bold'), fill=TEXT_MAIN)
        draw.text((c3_x + 40, erg_y + 62), ed, font=get_font(10.5, 'regular'), fill=TEXT_SUB)
        erg_y += 104

    draw_footer(draw, 9)
    img.save(os.path.join(OUT_DIR, "slide_09.png"), quality=95)
    print("Generated slide_09.png")

# -------------------------------------------------------------
# SLIDE 10: BUSINESS IMPACT & STAR RETROSPECTIVE
# -------------------------------------------------------------
def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 10, "OUTCOMES & RETROSPECTIVE",
        "Outcomes & STAR | ", "차세대 Android 월패드 라인업 안착 및 시니어 UX 회고",
        "기존 리눅스 월패드 대비 UX 혁신 성과(Before/After), 1군 건설사 적용 성과 지표 및 STAR 기법 기술 회고",
        right_badge=("PROJECT OUTCOMES", "red")
    )

    # TIER 1: BEFORE vs AFTER (y=215..475)
    t1_y, t1_h, half_w = 215, 260, 848
    lx = 100
    draw.rounded_rectangle([lx, t1_y, lx + half_w, t1_y + t1_h], radius=16, fill=(255, 250, 250), outline=(254, 202, 202), width=1)
    draw_pill(draw, left_x=lx + 26, cy=t1_y + 32, text="BEFORE · 기존 Linux 월패드 라인업", font=get_font(10, 'bold'), theme='gray', pad_x=10, height=22)
    draw.text((lx + 26, t1_y + 58), "확장성 한계 · 복잡한 메뉴 구조 · 시니어 접근성 미흡", font=get_font(16, 'bold'), fill=TEXT_MAIN)
    for idx, (k, v) in enumerate([
        ("OS 및 확장성", "폐쇄형 리눅스 기반으로 신규 IoT 서비스·고객사 커스텀 대응 지연"),
        ("메뉴 탐색 및 알림", "앱 서랍·공통 네비게이션바·통합 알림 부재로 기능 탐색 혼란"),
        ("시니어 사용성", "작은 글씨·흐린 대비·좁은 터치 영역으로 문열기 등 핵심 과업 실패")
    ]):
        by = t1_y + 94 + idx * 52
        draw.rounded_rectangle([lx + 26, by, lx + half_w - 26, by + 44], radius=8, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 42, by + 22), k, font=get_font(11.5, 'bold'), fill=TEXT_SUB, anchor='lm')
        draw.text((lx + 205, by + 22), v, font=get_font(11.5, 'regular'), fill=TEXT_MAIN, anchor='lm')

    rx = 972
    draw.rounded_rectangle([rx, t1_y, rx + half_w, t1_y + t1_h], radius=16, fill=(255, 246, 248), outline=(253, 164, 175), width=1)
    draw_pill(draw, left_x=rx + 26, cy=t1_y + 32, text="AFTER · HT Android Custom WALLPAD", font=get_font(10, 'bold'), theme='red', solid=True, pad_x=10, height=22)
    draw.text((rx + 26, t1_y + 58), "전 세대가 편안하게 쓰는 차세대 스마트홈 커스텀 OS 표준", font=get_font(16, 'bold'), fill=TEXT_MAIN)
    for idx, (k, v) in enumerate([
        ("OS 및 확장성", "Android Custom OS 전면 전환으로 1군 건설사 맞춤형 확장성 확보"),
        ("메뉴 탐색 및 알림", "업계 최초 앱 서랍·공통 네비게이션바·실시간 통합 알림 센터 구축"),
        ("시니어 사용성", "원거리 고대비 타이포·56dp 대형 터치 타깃으로 전 세대 오작동 제로화")
    ]):
        ay = t1_y + 94 + idx * 52
        draw.rounded_rectangle([rx + 26, ay, rx + half_w - 26, ay + 44], radius=8, fill=(255, 241, 244), outline=(254, 205, 211), width=1)
        draw.text((rx + 42, ay + 22), k, font=get_font(11.5, 'bold'), fill=HT_DARK, anchor='lm')
        draw.text((rx + 205, ay + 22), v, font=get_font(11.5, 'semibold'), fill=TEXT_MAIN, anchor='lm')

    # TIER 2: 4 QUANTITATIVE KPI CARDS (y=495..620)
    t2_y, t2_h, mw = 495, 125, 412
    kpis = [
        ("LONG-TERM LINEUP", "6 Years", "2018.05 ~ 2024.02 장기 총괄", "안드로이드 커스텀 OS 플래그십 라인업 전환 완수", "red"),
        ("OWNERSHIP", "100%", "Main / Sub 전담 기여도", "PL·UX 리서치·UI 설계·GUI 디자인 전 과정 총괄", "red"),
        ("TOP CLIENTS", "4+ Tier-1", "1군 대형 건설사 납품 적용", "HT·현대건설·현대엔지니어링·대우건설 등 단지 공급", "blue"),
        ("ECOSYSTEM", "4-Device", "크로스 디바이스 실시간 연동", "월패드·도어폰·로비폰·이마주 2.0 앱 통합 UX 완성", "teal")
    ]
    for idx, (kb, kv, kt, kd, kth) in enumerate(kpis):
        mx = 100 + idx * (mw + 24)
        draw.rounded_rectangle([mx, t2_y, mx + mw, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=mx + 22, cy=t2_y + 24, text=kb, font=get_font(9, 'bold'), theme=kth, pad_x=8, height=18)
        vc = HT_RED if kth == 'red' else (HT_BLUE if kth == 'blue' else HT_TEAL)
        draw.text((mx + 22, t2_y + 42), kv, font=get_font(26, 'black'), fill=vc)
        draw.text((mx + 22, t2_y + 82), kt, font=get_font(12, 'bold'), fill=TEXT_MAIN)
        draw.text((mx + 22, t2_y + 102), kd, font=get_font(10, 'regular'), fill=TEXT_SUB)

    # TIER 3: STAR RETROSPECTIVE (y=640..960)
    sy, sw, sh = 640, 1720, 320
    draw.rounded_rectangle([100, sy, 100 + sw, sy + sh], radius=16, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    bw_s = draw_pill(draw, left_x=126, cy=sy + 32, text="SENIOR UX STRATEGY RETROSPECTIVE (STAR)", font=get_font(10, 'bold'), theme='red', solid=True, pad_x=12, height=24)
    draw.text((126 + bw_s + 16, sy + 32), "임베디드 리눅스에서 차세대 Android 커스텀 OS 스마트홈 표준을 구축한 6년의 여정", font=get_font(15, 'bold'), fill=TEXT_MAIN, anchor='lm')

    stars = [
        ("S · Situation (상황)", "기존 주력 리눅스 월패드는 건설사별 커스텀 요구와 신규 IoT 서비스 확장에 한계가 있었으며, 복잡한 메뉴와 낮은 시인성으로 전 세대 사용자의 불편이 누적되고 있었습니다."),
        ("T · Task (과제)", "부팅·초기동기화·런처·앱서랍까지 완전히 새로운 Android Custom OS 아키텍처를 설계하고, 20대부터 70대 시니어까지 학습 없이 쓰는 스마트홈 UX를 구축해야 했습니다."),
        ("A · Action (실행)", "경쟁 4사 벤치마킹과 3세대 페르소나·5단계 여정맵을 통해 업계 최초로 3대 카테고리 앱 서랍, 공통 시스템바, 실시간 통합 알림 및 도어폰·로비폰·이마주 2.0 연동 시나리오를 설계했습니다."),
        ("R · Result (성과)", "현대건설·현대엔지니어링·대우건설 등 국내 1군 건설사 단지에 차세대 안드로이드 월패드 라인업을 성공적으로 안착시키며 HT의 핵심 플래그십 OS 표준을 확립했습니다.")
    ]
    sc_w = (sw - 52 - 60) // 4
    for idx, (st, sdesc) in enumerate(stars):
        sx = 126 + idx * (sc_w + 20)
        draw.rounded_rectangle([sx, sy + 66, sx + sc_w, sy + sh - 22], radius=12, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=sx + 18, cy=sy + 92, text=st, font=get_font(10, 'bold'), theme='red' if idx in [0, 3] else 'blue', pad_x=10, height=22)
        lines = wrap_text(sdesc, get_font(11, 'regular'), sc_w - 36, draw)
        ly = sy + 120
        for l in lines:
            draw.text((sx + 18, ly), l, font=get_font(11, 'regular'), fill=TEXT_SUB)
            ly += 21

    draw_footer(draw, 10)
    img.save(os.path.join(OUT_DIR, "slide_10.png"), quality=95)
    print("Generated slide_10.png")

if __name__ == '__main__':
    for fn in [
        make_slide_01, make_slide_02, make_slide_03, make_slide_04, make_slide_05,
        make_slide_06, make_slide_07, make_slide_08, make_slide_09, make_slide_10
    ]:
        fn()
    pdf_path = os.path.join(BASE_DIR, "HT_Android_Custom_Wallpad_Portfolio.pdf")
    slides = [Image.open(os.path.join(OUT_DIR, f"slide_{i:02d}.png")).convert('RGB') for i in range(1, TOTAL_SLIDES + 1)]
    slides[0].save(pdf_path, save_all=True, append_images=slides[1:], resolution=100.0)
    print(f"Successfully compiled {len(slides)} slides -> {pdf_path}")
