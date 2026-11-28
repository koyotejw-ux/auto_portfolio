import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
BASE_DIR = r"d:\097.flutter_project\auto_portfolio\nexon_promotion"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUT_DIR = os.path.join(BASE_DIR, "behance_slides")
os.makedirs(OUT_DIR, exist_ok=True)

# NEXON Signature Promotion Palette (Sky Cyan + Lime Green + Deep Slate)
NX_BLUE = (0, 157, 220)        # #009DDC Nexon Cyan-Blue
NX_BLUE_DARK = (3, 105, 161)   # #0369A1 Deep Sky
NX_LIME = (132, 204, 22)       # #84CC16 Nexon Lime
NX_LIME_DARK = (77, 124, 15)   # #4D7C0F Deep Lime
NX_ORANGE = (249, 115, 22)     # #F97316 Event Accent
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

def draw_pill(draw, cx=None, cy=0, text="", font=None, theme='blue', pad_x=12, height=24, left_x=None, solid=False):
    themes = {
        'blue': {
            'bg': NX_BLUE if solid else (240, 249, 255),
            'border': NX_BLUE,
            'text': (255, 255, 255) if solid else NX_BLUE_DARK
        },
        'lime': {
            'bg': NX_LIME if solid else (247, 254, 231),
            'border': NX_LIME,
            'text': (255, 255, 255) if solid else NX_LIME_DARK
        },
        'orange': {
            'bg': NX_ORANGE if solid else (255, 247, 237),
            'border': NX_ORANGE,
            'text': (255, 255, 255) if solid else (194, 65, 12)
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
    th = themes.get(theme, themes['blue'])
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
    draw_pill(draw, left_x=100, cy=78, text=f"{slide_num:02d} {cat}", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=26)
    if right_badge:
        txt, th = right_badge
        bw = draw.textlength(txt, font=get_font(10.5, 'bold')) + 28
        draw_pill(draw, left_x=1820 - bw, cy=78, text=txt, font=get_font(10.5, 'bold'), theme=th, solid=True, pad_x=14, height=28)
    f_t = get_font(32, 'bold')
    w_d = draw.textlength(title_dark, font=f_t)
    draw.text((100, 116), title_dark, font=f_t, fill=TEXT_MAIN)
    draw.text((100 + w_d, 116), title_accent, font=f_t, fill=NX_BLUE)
    draw.text((100, 166), subtitle, font=get_font(14, 'regular'), fill=TEXT_SUB)

def draw_footer(draw, slide_num):
    draw.line([(100, 995), (1820, 995)], fill=BORDER_LIGHT, width=1)
    f_b = get_font(11.5, 'bold')
    brand = "NEXON · PROMOTION DESIGN ARCHIVE"
    draw.text((100, 1018), brand, font=f_b, fill=NX_BLUE)
    wb = draw.textlength(brand, font=f_b)
    draw.text((100 + wb + 16, 1018), "·   넥슨 대표 8대 게임 대형 프로모션 & 이벤트 아트 디렉션", font=get_font(11, 'medium'), fill=(148, 163, 184))
    draw.text((1080, 1018), "영웅시대 · 클로저스 · 엘소드 · 크아 · 카트라이더 · 바람의나라 · 테일즈위버 · 피파온라인3", font=get_font(10, 'medium'), fill=(148, 163, 184), anchor='mt')
    draw.text((1820, 1018), f"PAGE {slide_num:02d} / {TOTAL_SLIDES:02d}", font=get_font(11.5, 'black'), fill=TEXT_SUB, anchor='rt')

# -------------------------------------------------------------
# SLIDE 01: HERO COVER
# -------------------------------------------------------------
def make_slide_01():
    base = Image.new('RGBA', (W, H), (*BG_HERO, 255))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([860, 80, 1880, 820], fill=(0, 157, 220, 26))
    gd.ellipse([1040, 220, 1780, 780], fill=(132, 204, 22, 22))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)

    draw.line([(100, 52), (1820, 52)], fill=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=100, cy=76, text="NEXON KOREA · PROMOTION & EVENT ARCHIVE", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=28)
    meta = "Web Promotion & Event  ·  8 Flagship Titles  ·  참여율 100%  ·  Art Direction · UI · Promotion Design"
    draw.text((1820, 76), meta, font=get_font(12, 'medium'), fill=TEXT_SUB, anchor='rm')

    draw.text((100, 132), "NEXON FLAGSHIP TITLES · MULTI-GENRE CAMPAIGNS", font=get_font(12.5, 'bold'), fill=NX_BLUE)
    draw.text((100, 162), "유저의 시선과 참여를 이끌다,", font=get_font(30, 'bold'), fill=TEXT_MAIN)
    draw.text((100, 214), "PROMOTION DESIGN", font=get_font(44, 'black'), fill=NX_BLUE)

    sub1 = "무협·이능 액션·캐주얼·클래식 RPG·스포츠까지 넥슨코리아 대표 8대 게임 타이틀의"
    sub2 = "대형 업데이트 프로모션, 참여형 이벤트, 인터랙션 배너 및 포털 비주얼 아카이브입니다."
    draw.text((100, 294), sub1, font=get_font(13, 'regular'), fill=(71, 85, 105))
    draw.text((100, 320), sub2, font=get_font(13, 'semibold'), fill=(30, 41, 59))

    strengths = [
        ("01", "멀티 장르", "8대 넥슨 대표 타이틀 맞춤형 톤앤매너", "All-Genre Art Direction",
         "영웅시대·클로저스·엘소드·크아·카트·바람의나라·테일즈위버·피파온라인3 각 IP 세계관에 최적화된 비주얼을 구축했습니다."),
        ("02", "참여형 UX", "퀴즈·퍼즐·룰렛·오락실 게이미피케이션", "Gamified Event Flows",
         "단순 정보 나열을 넘어 룰렛·틀린그림찾기·능력시험·퍼즐 등 유저가 직접 클릭하고 즐기는 인터랙티브 이벤트를 설계했습니다."),
        ("03", "임팩트 키비주얼", "레이어 분해 합성 & 커스텀 타이포그래피", "High-Impact Key Visuals",
         "배경·파티클·캐릭터 레이어 분리 연출과 장르별 붓글씨·네온·3D 메탈릭 타이틀 디자인으로 클릭 전환율을 극대화했습니다."),
        ("04", "전 채널 확장", "메인 개편부터 점검·충전 UI·배너까지 통합", "Full-Funnel Asset System",
         "대형 프로모션 랜딩, 서버 점검 카운트다운, 넥슨캐시 충전 완료 UI, 시즌 핫타임 배너까지 일관된 브랜드 경험을 완성했습니다.")
    ]
    max_bw = max(draw.textlength(t, font=get_font(10, 'bold')) + 16 for _, t, _, _, _ in strengths)
    title_x = int(round(144 + max_bw + 18))

    ky = 388
    for idx, (num, tag, tko, ten, desc) in enumerate(strengths):
        rcy = ky + 14
        draw.rounded_rectangle([100, ky + 1, 134, ky + 27], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.text((117, rcy), num, font=get_font(11, 'bold'), fill=NX_BLUE, anchor='mm')
        draw_pill(draw, left_x=144, cy=rcy, text=tag, font=get_font(10, 'bold'), theme='blue' if idx % 2 == 0 else 'lime', pad_x=8, height=24)
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

    # Right Side: 4-Game Dynamic Visual Collage
    col_path = os.path.join(ASSETS_DIR, "promo_collage_hero.png")
    if os.path.exists(col_path):
        col_im = Image.open(col_path).convert('RGBA')
        tw = 840
        th = int(col_im.height * (tw / col_im.width))
        col_res = col_im.resize((tw, th), Image.Resampling.LANCZOS)
        px, py = 975, 198
        sh = Image.new('RGBA', (tw + 80, th + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([40, 48, tw + 40, th + 48], radius=24, fill=(15, 23, 42, 85))
        sh = sh.filter(ImageFilter.GaussianBlur(28))
        base.paste(sh, (px - 40, py - 32), sh)
        mask = Image.new('L', (tw, th), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=20, fill=255)
        base.paste(col_res, (px, py), mask)

        draw = ImageDraw.Draw(base)
        draw.rounded_rectangle([px + 20, py + th + 24, px + tw - 20, py + th + 78], radius=12, fill=(255, 255, 255, 240), outline=BORDER_LIGHT, width=1)
        bw_d = draw_pill(draw, left_x=px + 38, cy=py + th + 51, text="8 FLAGSHIP TITLES", font=get_font(9.5, 'bold'), theme='blue', solid=True, pad_x=10, height=22)
        draw.text((px + 38 + bw_d + 14, py + th + 51), "FIFA Online 3 · 엘소드 · 카트라이더 · 크레이지아케이드 외 4종 실물", font=get_font(11.5, 'bold'), fill=TEXT_MAIN, anchor='lm')

    draw = ImageDraw.Draw(base)
    bar_y, bar_h = 836, 118
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    col_w = 1720 // 4
    specs = [
        ("CLIENT", "넥슨코리아 (Nexon Korea)", "국내 대표 8대 라이브 게임 타이틀 프로모션 총괄"),
        ("ARCHIVE SCOPE", "40+ 대형 업데이트 & 이벤트", "메인 개편 · 티저 · 참여형 이벤트 · 배너 · 시스템 UI"),
        ("CORE CAPABILITY", "Art Direction · Promotion UI", "장르별 커스텀 타이포 · 레이어 합성 · 인터랙션 기획"),
        ("GENRE SPECTRUM", "RPG · Action · Casual · Sports", "무협·이능·캐주얼·클래식 RPG·실사 스포츠 전 장르")
    ]
    for i, (cat, vb, vd) in enumerate(specs):
        cx = 100 + i * col_w
        if i > 0:
            draw.line([(cx, bar_y + 20), (cx, bar_y + bar_h - 20)], fill=BORDER_LIGHT, width=1)
        draw.text((cx + 28, bar_y + 20), cat, font=get_font(10.5, 'bold'), fill=NX_BLUE)
        draw.text((cx + 28, bar_y + 45), vb, font=get_font(13, 'bold'), fill=TEXT_MAIN)
        draw.text((cx + 28, bar_y + 76), vd, font=get_font(10.5, 'regular'), fill=TEXT_SUB)

    draw_footer(draw, 1)
    base.convert('RGB').save(os.path.join(OUT_DIR, "slide_01.png"), quality=95)
    print("Generated slide_01.png")

# -------------------------------------------------------------
# SLIDE 02: HERO AGE (영웅시대) — MAIN LAYER ART + 4 EVENTS
# -------------------------------------------------------------
def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 2, "TITLE 01 · HERO AGE (영웅시대)",
        "영웅시대 | ", "오픈기념 BIG 이벤트 레이어 아트 디렉션 & 4대 대형 캠페인",
        "동양 무협 판타지 세계관을 극대화한 메인 프로모션 패럴랙스 레이어 설계 및 용호문·레벨워프·영웅의 봄 룰렛 이벤트",
        right_badge=("MARTIAL ARTS RPG", "blue")
    )

    cy, ch = 215, 745
    # Left Card: 02_hero_age_main.png (x=100, w=840)
    lx, lw = 100, 840
    draw.rounded_rectangle([lx, cy, lx + lw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_l = draw_pill(draw, left_x=lx + 24, cy=cy + 34, text="MAIN PROMOTION & LAYER DECOMPOSITION", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((lx + 24 + bw_l + 12, cy + 34), "오픈기념 BIG 이벤트 & 패럴랙스 레이어 분해", font=get_font(12.5, 'bold'), fill=TEXT_MAIN, anchor='lm')

    m_im = Image.open(os.path.join(ASSETS_DIR, "02_hero_age_main.png")).convert('RGBA')
    m_crop = m_im.crop((0, 78, m_im.width, m_im.height))
    iw, ih = lw - 48, 495
    sc = min(iw / m_crop.width, ih / m_crop.height)
    tw, th = int(m_crop.width * sc), int(m_crop.height * sc)
    img.paste(m_crop.resize((tw, th), Image.Resampling.LANCZOS), (lx + (lw - tw) // 2, cy + 72), m_crop.resize((tw, th), Image.Resampling.LANCZOS))

    draw.rounded_rectangle([lx + 24, cy + ch - 140, lx + lw - 24, cy + ch - 24], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((lx + 42, cy + ch - 118), "다중 레이어 합성 & 3단 배너 스위처 설계", font=get_font(13.5, 'bold'), fill=NX_BLUE_DARK)
    d1 = "배경(신비로운 숲) · 광원 파티클 · 캐릭터(전경)를 3개 레이어로 분리 설계해 역동적인 깊이감을 구현하고, 하단 3분할 슬라이더(검성회·빅3이벤트·지목문)로 주요 캠페인 탐색을 직관화했습니다."
    lines = wrap_text(d1, get_font(11.5, 'regular'), lw - 84, draw)
    dy = cy + ch - 88
    for l in lines[:3]:
        draw.text((lx + 42, dy), l, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
        dy += 20

    # Right Card: 03_hero_age_events.png (x=965, w=855)
    rx, rw = 965, 855
    draw.rounded_rectangle([rx, cy, rx + rw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_r = draw_pill(draw, left_x=rx + 24, cy=cy + 34, text="4 MAJOR CAMPAIGNS", font=get_font(10, 'bold'), theme='lime', pad_x=10, height=24)
    draw.text((rx + 24 + bw_r + 12, cy + 34), "Episode II 용호문 · 레벨워프 프로젝트 · 영웅의 봄 룰렛", font=get_font(12.5, 'bold'), fill=TEXT_MAIN, anchor='lm')

    e_im = Image.open(os.path.join(ASSETS_DIR, "03_hero_age_events.png")).convert('RGBA')
    e_crop = e_im.crop((0, 88, e_im.width, e_im.height))
    iw2, ih2 = rw - 48, 520
    sc2 = min(iw2 / e_crop.width, ih2 / e_crop.height)
    tw2, th2 = int(e_crop.width * sc2), int(e_crop.height * sc2)
    img.paste(e_crop.resize((tw2, th2), Image.Resampling.LANCZOS), (rx + (rw - tw2) // 2, cy + 68), e_crop.resize((tw2, th2), Image.Resampling.LANCZOS))

    draw.rounded_rectangle([rx + 24, cy + ch - 122, rx + rw - 24, cy + ch - 24], radius=12, fill=(247, 254, 231), outline=NX_LIME, width=1)
    draw.text((rx + 42, cy + ch - 98), "테마별 톤앤매너 변주 (수묵·사이버·스프링 룰렛)", font=get_font(13.5, 'bold'), fill=NX_LIME_DARK)
    d2 = "용호문(수묵·금박 캘리그래피), 만렙해제 레벨워프(메탈릭 사이버 타이포), 영웅의 봄(참여형 룰렛 보드) 등 이벤트 목적에 맞춘 극명한 시각적 차별화를 구현했습니다."
    lines2 = wrap_text(d2, get_font(11.5, 'regular'), rw - 84, draw)
    dy = cy + ch - 68
    for l in lines2[:2]:
        draw.text((rx + 42, dy), l, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
        dy += 20

    draw_footer(draw, 2)
    img.save(os.path.join(OUT_DIR, "slide_02.png"), quality=95)
    print("Generated slide_02.png")

# -------------------------------------------------------------
# SLIDE 03: CLOSERS PROMOTION & EVENTS
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 3, "TITLE 02 · CLOSERS (클로저스)",
        "클로저스 | ", "CBT 론칭 · 넥슨플레이 공식친구 · 신규 던전 프로모션",
        "이능 액션 RPG '클로저스'의 론칭 CBT 테스터 모집부터 라이브 업데이트 훈련 프로그램, 코믹스·설맞이 배너까지 통합 제작했습니다.",
        right_badge=("PSYCHIC ACTION", "orange")
    )

    cy = 215
    draw.rounded_rectangle([100, cy, 1820, cy + 560], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    cl_im = Image.open(os.path.join(ASSETS_DIR, "04_closers_promo.png")).convert('RGBA')
    cl_crop = cl_im.crop((0, 48, cl_im.width, cl_im.height))
    iw, ih = 1660, 516
    sc = min(iw / cl_crop.width, ih / cl_crop.height)
    tw, th = int(cl_crop.width * sc), int(cl_crop.height * sc)
    img.paste(cl_crop.resize((tw, th), Image.Resampling.LANCZOS), (100 + (1720 - tw) // 2, cy + (560 - th) // 2), cl_crop.resize((tw, th), Image.Resampling.LANCZOS))

    by, bh = 795, 165
    sw = (1720 - 48) // 3
    cards = [
        ("01. CBT 테스터 모집 & 넥슨플레이", "육각형 헥사곤 UI와 강렬한 화염·캐릭터 일러스트를 결합해 CBT 신청 및 '선물이 땅땅땅 빵!' 공식친구 전환율을 극대화했습니다.", "orange"),
        ("02. 신규 지역 던전 훈련 프로그램", "딥 퍼플 네온 톤과 명확한 단계별 미션 테이블을 적용해 복잡한 던전 입장 조건과 보상 구조를 한눈에 이해할 수 있도록 설계했습니다.", "blue"),
        ("03. 위상한 밥상 & 시즌 배너 4종", "공식 코믹스 참여형 퀴즈 이벤트와 설맞이 핫타임·아이디 철통보안 등 시의성 높은 크로스 프로모션 배너 세트를 제작했습니다.", "lime")
    ]
    for idx, (st, sd, th_c) in enumerate(cards):
        sx = 100 + idx * (sw + 24)
        draw.rounded_rectangle([sx, by, sx + sw, by + bh], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=sx + 22, cy=by + 28, text=st, font=get_font(10.5, 'bold'), theme=th_c, pad_x=10, height=22)
        lines = wrap_text(sd, get_font(11.5, 'regular'), sw - 44, draw)
        dy = by + 56
        for l in lines[:3]:
            draw.text((sx + 22, dy), l, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
            dy += 21

    draw_footer(draw, 3)
    img.save(os.path.join(OUT_DIR, "slide_03.png"), quality=95)
    print("Generated slide_03.png")

# -------------------------------------------------------------
# HELPER FOR DARK GALLERY SHOWCASE SLIDES (04 ~ 09)
# -------------------------------------------------------------
def make_gallery_slide(slide_num, cat, title_dark, title_accent, subtitle, right_badge, img_fn, highlights):
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(draw, slide_num, cat, title_dark, title_accent, subtitle, right_badge=right_badge)

    cy, ch = 215, 565
    # Sleek Dark Museum Frame matching the black background of the authentic promo boards!
    draw.rounded_rectangle([100, cy, 1820, cy + ch], radius=18, fill=(0, 0, 0), outline=(51, 65, 85), width=1)
    src = Image.open(os.path.join(ASSETS_DIR, img_fn)).convert('RGB')
    # Crop out the top black title bar (y=96..535, x=45..978) to showcase the visuals huge & crisp!
    crop = src.crop((42, 96, 982, 536))
    iw, ih = 1660, 520
    sc = min(iw / crop.width, ih / crop.height)
    tw, th = int(crop.width * sc), int(crop.height * sc)
    img.paste(crop.resize((tw, th), Image.Resampling.LANCZOS), (100 + (1720 - tw) // 2, cy + (ch - th) // 2))

    # Bottom 3 Highlights Strip (y=798..960)
    by, bh = 798, 162
    sw = (1720 - 48) // 3
    for idx, (st, sd, th_c) in enumerate(highlights):
        sx = 100 + idx * (sw + 24)
        draw.rounded_rectangle([sx, by, sx + sw, by + bh], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=sx + 22, cy=by + 28, text=st, font=get_font(10.5, 'bold'), theme=th_c, pad_x=10, height=22)
        lines = wrap_text(sd, get_font(11.5, 'regular'), sw - 44, draw)
        dy = by + 56
        for l in lines[:3]:
            draw.text((sx + 22, dy), l, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
            dy += 21

    draw_footer(draw, slide_num)
    img.save(os.path.join(OUT_DIR, f"slide_{slide_num:02d}.png"), quality=95)
    print(f"Generated slide_{slide_num:02d}.png")

# -------------------------------------------------------------
# SLIDE 10: OUTCOMES & STAR RETROSPECTIVE
# -------------------------------------------------------------
def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 10, "OUTCOMES & RETROSPECTIVE",
        "Outcomes & STAR | ", "넥슨 8대 대표 IP 멀티 장르 프로모션 아카이브 성과 및 회고",
        "각기 다른 장르와 유저층을 가진 넥슨 핵심 타이틀의 브랜드 가치를 극대화한 프로모션 아트 디렉션 전략과 STAR 회고",
        right_badge=("ARCHIVE SUMMARY", "blue")
    )

    # TIER 1: 4-GENRE ART DIRECTION MATRIX (y=215..475)
    t1_y, t1_h = 215, 260
    gw = 412
    genres = [
        ("ACTION & MARTIAL RPG", "영웅시대 · 클로저스 · 엘소드", "blue",
         "패럴랙스 레이어 합성, 강렬한 화염·네온 이펙트, 헥사곤·수묵 커스텀 타이포그래피로 신규 업데이트 몰입감 극대화"),
        ("CASUAL & ARCADE", "크레이지아케이드 · 카트라이더", "lime",
         "오락실 캐비닛·칠판 능력시험·퍼즐 보드 등 위트 있는 게이미피케이션 인터랙션으로 10~20대 유저 참여 유도"),
        ("CLASSIC FANTASY RPG", "바람의나라 · 테일즈위버", "orange",
         "장수 IP 특유의 서사적 감성(붓글씨·동양화·수채화 감성 일러스트)을 현대적 이벤트 정보 구조로 재해석"),
        ("REALISTIC SPORTS", "EA SPORTS FIFA ONLINE 3", "dark",
         "스타디움 3D 공간감, 실시간 점검 카운트다운, 직관적 GP 경품·넥슨캐시 충전 UX로 신뢰감과 기대감 동시 확보")
    ]
    for idx, (gb, gt, gth, gd) in enumerate(genres):
        gx = 100 + idx * (gw + 24)
        draw.rounded_rectangle([gx, t1_y, gx + gw, t1_y + t1_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=gx + 24, cy=t1_y + 34, text=gb, font=get_font(9.5, 'bold'), theme=gth, solid=(idx == 0), pad_x=10, height=22)
        draw.text((gx + 24, t1_y + 66), gt, font=get_font(15, 'bold'), fill=TEXT_MAIN)
        draw.line([(gx + 24, t1_y + 100), (gx + gw - 24, t1_y + 100)], fill=BORDER_LIGHT, width=1)
        lines = wrap_text(gd, get_font(11.5, 'regular'), gw - 48, draw)
        dy = t1_y + 118
        for l in lines[:5]:
            draw.text((gx + 24, dy), l, font=get_font(11.5, 'regular'), fill=TEXT_SUB)
            dy += 22

    # TIER 2: 4 QUANTITATIVE KPI CARDS (y=495..620)
    t2_y, t2_h, mw = 495, 125, 412
    kpis = [
        ("FLAGSHIP IP", "8 Titles", "넥슨코리아 대표 8대 게임", "무협·이능·캐주얼·클래식 RPG·스포츠 전 장르", "blue"),
        ("DELIVERABLES", "40+ Live", "대형 업데이트 & 이벤트 완수", "메인 개편 · 티저 · 참여형 이벤트 · 배너 · UI", "lime"),
        ("CONTRIBUTION", "100%", "아트 디렉션 & 디자인 전담", "컨셉 도출부터 키비주얼·타이포·UI 마무리 총괄", "blue"),
        ("GAMIFICATION", "Multi-UX", "참여형 이벤트 구조 설계", "룰렛 · 오락실 · 능력시험 · 퍼즐 · 코믹스 퀴즈", "orange")
    ]
    for idx, (kb, kv, kt, kd, kth) in enumerate(kpis):
        mx = 100 + idx * (mw + 24)
        draw.rounded_rectangle([mx, t2_y, mx + mw, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=mx + 22, cy=t2_y + 24, text=kb, font=get_font(9, 'bold'), theme=kth, pad_x=8, height=18)
        vc = NX_BLUE if kth == 'blue' else (NX_LIME_DARK if kth == 'lime' else NX_ORANGE)
        draw.text((mx + 22, t2_y + 42), kv, font=get_font(26, 'black'), fill=vc)
        draw.text((mx + 22, t2_y + 82), kt, font=get_font(12, 'bold'), fill=TEXT_MAIN)
        draw.text((mx + 22, t2_y + 102), kd, font=get_font(10, 'regular'), fill=TEXT_SUB)

    # TIER 3: STAR RETROSPECTIVE (y=640..960)
    sy, sw, sh = 640, 1720, 320
    draw.rounded_rectangle([100, sy, 100 + sw, sy + sh], radius=16, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    bw_s = draw_pill(draw, left_x=126, cy=sy + 32, text="SENIOR ART DIRECTION RETROSPECTIVE (STAR)", font=get_font(10, 'bold'), theme='blue', solid=True, pad_x=12, height=24)
    draw.text((126 + bw_s + 16, sy + 32), "장르별 브랜드 톤앤매너와 유저 참여 UX를 결합한 넥슨 프로모션 디자인 회고", font=get_font(15, 'bold'), fill=TEXT_MAIN, anchor='lm')

    stars = [
        ("S · Situation (상황)", "넥슨코리아의 다양한 라이브 게임(RPG·캐주얼·스포츠)들은 매 시즌 대규모 업데이트와 이벤트마다 유저의 시선을 즉각 사로잡고 실제 게임 접속과 참여로 이어지는 차별화된 비주얼이 필요했습니다."),
        ("T · Task (과제)", "빠른 라이브 서비스 일정 속에서도 각 게임 IP 고유의 세계관을 해치지 않으면서, 복잡한 보상·참여 조건을 직관적으로 전달하고 클릭·참여를 유도하는 프로모션 UX/UI를 제작해야 했습니다."),
        ("A · Action (실행)", "장르별 맞춤 키비주얼(레이어 합성·커스텀 타이포)과 게이미피케이션 UI(룰렛·오락실·퍼즐·능력시험)를 결합하고, 메인·점검·충전·배너까지 일관된 비주얼 시스템을 구축했습니다."),
        ("R · Result (성과)", "영웅시대·클로저스·피파온라인3 등 8대 핵심 타이틀의 40건 이상 대형 프로모션을 성공적으로 론칭하며, 멀티 장르를 아우르는 프로모션 아트 디렉션 및 UX 설계 역량을 입증했습니다.")
    ]
    sc_w = (sw - 52 - 60) // 4
    for idx, (st, sdesc) in enumerate(stars):
        sx = 126 + idx * (sc_w + 20)
        draw.rounded_rectangle([sx, sy + 66, sx + sc_w, sy + sh - 22], radius=12, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=sx + 18, cy=sy + 92, text=st, font=get_font(10, 'bold'), theme='blue' if idx in [0, 3] else 'lime', pad_x=10, height=22)
        lines = wrap_text(sdesc, get_font(11, 'regular'), sc_w - 36, draw)
        ly = sy + 120
        for l in lines:
            draw.text((sx + 18, ly), l, font=get_font(11, 'regular'), fill=TEXT_SUB)
            ly += 21

    draw_footer(draw, 10)
    img.save(os.path.join(OUT_DIR, "slide_10.png"), quality=95)
    print("Generated slide_10.png")

if __name__ == '__main__':
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_gallery_slide(
        4, "TITLE 03 · ELSWORD (엘소드)", "엘소드 | ", "전문직업 업데이트 · 대전 시즌 III & 한정 아바타 프로모션",
        "스타일리시 액션 RPG 엘소드의 핵심 업데이트(전문직업·대전 시즌 III)와 시즌 한정 아바타·황금연휴 프로모션 아카이브",
        ("ACTION RPG", "blue"), "05_elsword_promo.jpg", [
            ("01. 전문직업 & 대전 시즌 III", "네온 퍼플·화염 대비와 캐릭터 9인 라인업 구도를 활용해 대규모 PVP 시즌 개막의 긴장감과 기대감을 극대화했습니다.", "blue"),
            ("02. 한정 아바타 특화 배너", "빨간두건·엘리시스 그레이스 페어리·테디베어 등 아바타 컨셉에 맞춘 라운드 프레임과 직관적 카피로 구매 전환을 유도했습니다.", "orange"),
            ("03. 시즌 이벤트 통합 구성", "깜짝 퀴즈·매일 넥슨캐시 지급·황금연휴 최대 50% 할인 등 다중 혜택을 명확한 정보 위계로 정리했습니다.", "lime")
        ]
    )
    make_gallery_slide(
        5, "TITLE 04 · CRAZY ARCADE (크레이지아케이드)", "크레이지아케이드 | ", "12주년 오락실 전야제 · 능력시험 & 주말할인 이벤트",
        "전 국민 캐주얼 게임 크레이지아케이드의 유쾌한 감성을 살린 오락실 캐비닛·칠판 퀴즈·할인 프로모션 아카이브",
        ("CASUAL ARCADE", "lime"), "06_crazy_arcade_promo.jpg", [
            ("01. 크아 12주년 오락실 전야제", "레트로 아케이드 게임기 프레임 안에 실제 틀린그림찾기 미니게임을 배치해 유저가 머물며 즐기는 체험형 프로모션을 완성했습니다.", "blue"),
            ("02. 완전 쉬운 크아 능력시험", "학교 칠판과 OMR 시험지 모티브를 차용해 누구나 부담 없이 참여하고 공유할 수 있는 위트 있는 퀴즈 UI를 설계했습니다.", "lime"),
            ("03. 모두의 주말할인 50% & 배너", "경쾌한 블루·오렌지 대비와 50% 빅 타이포그래피, CP캡틴배찌 등 캐릭터 중심 배너로 높은 클릭률을 달성했습니다.", "orange")
        ]
    )
    make_gallery_slide(
        6, "TITLE 05 · KARTRIDER (카트라이더)", "카트라이더 | ", "여름 퍼즐 · 팬더 레인저 · 티끌모아 카트라이더 캠페인",
        "스피드와 밝은 에너지가 돋보이는 카트라이더의 계절별 대형 이벤트(퀴즈·여름 퍼즐·팬더 레인저·GM 소통) 아카이브",
        ("RACING CASUAL", "blue"), "07_kartrider_promo.jpg", [
            ("01. QUIZ 아이스크림 & 2013 여름 퍼즐", "청량한 여름 비치 톤과 직관적인 4단계 퍼즐 완성 트래커를 결합해 일일 출석 및 미션 참여 동기를 부여했습니다.", "blue"),
            ("02. 팬더 레인저 & 티끌모아 카트라이더", "히어로 컨셉의 네온 엠블럼과 다오·배찌 캐릭터 일러스트를 중심으로 단계별 보상 구조를 알기 쉽게 시각화했습니다.", "orange"),
            ("03. 리뷰 & 공식친구 배너 시리즈", "2014 최고의 리뷰·넥슨플레이 공식친구 맺기 등 멀티 채널 유입을 위한 고시인성 배너 시스템을 제작했습니다.", "lime")
        ]
    )
    make_gallery_slide(
        7, "TITLE 06 · KINGDOM OF THE WINDS (바람의나라)", "바람의나라 | ", "서버통합 · 영웅의힘 업데이트 & 개천절 대격돌 이벤트",
        "대한민국 최장수 클래식 MMORPG 바람의나라의 전통적 정체성을 붓글씨 캘리그래피와 강렬한 대비로 재해석한 아카이브",
        ("CLASSIC MMORPG", "orange"), "08_baram_promo.jpg", [
            ("01. 서버통합 & 도전한방 메인", "황금 용 일러스트와 전통 문양 패턴을 조화시켜 서버통합의 웅장함과 신규 도전 이벤트의 활력을 균형 있게 담아냈습니다.", "orange"),
            ("02. 영웅의힘 업데이트 & 대격돌", "바위 균열 텍스처와 레드/블루 양진영 대결 구도(호랑이 vs 곰)로 개천절 대격돌의 서사적 몰입감을 극대화했습니다.", "blue"),
            ("03. 시즌 업데이트 배너 패키지", "문파부문주 업데이트·강시대소동·눈싸움 이벤트 등 계절·콘텐츠 성격에 맞춘 캘리그래피 배너를 제작했습니다.", "lime")
        ]
    )
    make_gallery_slide(
        8, "TITLE 07 · TALESWEAVER (테일즈위버)", "테일즈위버 | ", "혹한(酷寒) · Ep.3 Benya & 10주년 감성 프로모션",
        "서정적 일러스트와 깊은 스토리가 강점인 테일즈위버의 메인 개편, 에피소드 업데이트 및 10주년 감성 이벤트 아카이브",
        ("STORY RPG", "blue"), "09_talesweaver_promo.jpg", [
            ("01. 혹한(酷寒) & Ep.3 공명 Benya 메인", "겨울 빙결 이펙트와 몽환적 퍼플 톤으로 에피소드별 분위기를 극대화하면서도 로그인·Game Start 동선을 선명하게 유지했습니다.", "blue"),
            ("02. 앤의 화분 & 새로운 시작 10주년", "따뜻한 파스텔 수채화 톤과 도트 캐릭터 아이콘, 깔끔한 보상 테이블을 결합해 10주년 기념 이벤트의 감동을 극대화했습니다.", "lime"),
            ("03. 클린 캠페인 & 커뮤니티 배너", "불법 프로그램 방지 클린 캠페인과 테일즈위버 만들기 등 유저 친화적 커뮤니케이션 배너를 일관되게 디자인했습니다.", "orange")
        ]
    )
    make_gallery_slide(
        9, "TITLE 08 · EA SPORTS FIFA ONLINE 3", "피파온라인3 | ", "스타디움 키비주얼 · GP 경품 · 점검 카운트다운 & 결제 UI",
        "실사 스포츠 게임 피파온라인3의 역동적인 스타디움 공간감과 메인 개편·서비스 점검·넥슨캐시 충전 UX 아카이브",
        ("REALISTIC SPORTS", "lime"), "10_fifa_online3_promo.jpg", [
            ("01. GP 경품 교환 & 51% 아이템예보", "잔디 구장과 3D 스포트라이트 포디움 연출로 실제 경품의 가치를 높이고, 직관적 게이지 UI로 이벤트 참여율을 강화했습니다.", "lime"),
            ("02. 메인 개편 & 서비스 점검 카운트다운", "메시·박지성 키비주얼 중심의 깔끔한 화이트/블루 포털과 플립 시계 모티브의 점검 카운트다운으로 대기 경험을 개선했습니다.", "blue"),
            ("03. 넥슨캐시 충전 & 조르기 시스템 UI", "다크 신뢰감 톤의 충전 완료·조르기 확인 UI를 정교하게 설계해 결제 흐름의 명확성과 안심감을 높였습니다.", "dark")
        ]
    )
    make_slide_10()

    pdf_path = os.path.join(BASE_DIR, "Nexon_Promotion_Design_Archive_Portfolio.pdf")
    slides = [Image.open(os.path.join(OUT_DIR, f"slide_{i:02d}.png")).convert('RGB') for i in range(1, TOTAL_SLIDES + 1)]
    slides[0].save(pdf_path, save_all=True, append_images=slides[1:], resolution=100.0)
    print(f"Successfully compiled {len(slides)} slides -> {pdf_path}")
