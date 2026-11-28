import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
BASE_DIR = r"d:\097.flutter_project\auto_portfolio\nexon_closers"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUT_DIR = os.path.join(BASE_DIR, "behance_slides")
os.makedirs(OUT_DIR, exist_ok=True)

# NEXON CLOSERS Brand Palette (Cyber Gold + Cyan + Blaze Orange + Obsidian)
CL_GOLD = (245, 158, 11)       # #F59E0B Accessible Gold Accent
CL_GOLD_BRIGHT = (255, 196, 0) # #FFC400 Signature Closers Yellow
CL_GOLD_DARK = (180, 83, 9)    # #B45309 Deep Amber
CL_CYAN = (0, 174, 239)        # #00AEEF Cyber Cyan
CL_ORANGE = (255, 85, 0)       # #FF5500 Blaze Orange
BG_LIGHT = (255, 255, 255)
BG_HERO = (250, 252, 255)
CARD_LIGHT = (255, 255, 255)
BORDER_LIGHT = (226, 232, 240)
TEXT_MAIN = (15, 23, 42)
TEXT_SUB = (100, 116, 139)

TOTAL_SLIDES = 8

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

def draw_pill(draw, cx=None, cy=0, text="", font=None, theme='gold', pad_x=12, height=24, left_x=None, solid=False):
    themes = {
        'gold': {
            'bg': CL_GOLD if solid else (255, 251, 235),
            'border': CL_GOLD,
            'text': (255, 255, 255) if solid else CL_GOLD_DARK
        },
        'cyan': {
            'bg': CL_CYAN if solid else (240, 249, 255),
            'border': CL_CYAN,
            'text': (255, 255, 255) if solid else (2, 132, 199)
        },
        'orange': {
            'bg': CL_ORANGE if solid else (255, 247, 237),
            'border': CL_ORANGE,
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
    th = themes.get(theme, themes['gold'])
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
    draw_pill(draw, left_x=100, cy=78, text=f"{slide_num:02d} {cat}", font=get_font(10.5, 'bold'), theme='gold', pad_x=12, height=26)
    if right_badge:
        txt, th = right_badge
        bw = draw.textlength(txt, font=get_font(10.5, 'bold')) + 28
        draw_pill(draw, left_x=1820 - bw, cy=78, text=txt, font=get_font(10.5, 'bold'), theme=th, solid=True, pad_x=14, height=28)
    f_t = get_font(32, 'bold')
    w_d = draw.textlength(title_dark, font=f_t)
    draw.text((100, 116), title_dark, font=f_t, fill=TEXT_MAIN)
    draw.text((100 + w_d, 116), title_accent, font=f_t, fill=CL_GOLD_DARK)
    draw.text((100, 166), subtitle, font=get_font(14, 'regular'), fill=TEXT_SUB)

def draw_footer(draw, slide_num):
    draw.line([(100, 995), (1820, 995)], fill=BORDER_LIGHT, width=1)
    f_b = get_font(11.5, 'bold')
    brand = "NEXON · CLOSERS OFFICIAL WEB"
    draw.text((100, 1018), brand, font=f_b, fill=CL_GOLD_DARK)
    wb = draw.textlength(brand, font=f_b)
    draw.text((100 + wb + 16, 1018), "·   넥슨코리아 클로저스 6+1 타일 그리드 반응형 공식 웹사이트", font=get_font(11, 'medium'), fill=(148, 163, 184))
    draw.text((1060, 1018), "PC / Mobile Full-Responsive Web · 6-Stage Breakpoint Engine", font=get_font(10.5, 'medium'), fill=(148, 163, 184), anchor='mt')
    draw.text((1820, 1018), f"PAGE {slide_num:02d} / {TOTAL_SLIDES:02d}", font=get_font(11.5, 'black'), fill=TEXT_SUB, anchor='rt')

# -------------------------------------------------------------
# SLIDE 01: HERO COVER
# -------------------------------------------------------------
def make_slide_01():
    base = Image.new('RGBA', (W, H), (*BG_HERO, 255))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([860, 80, 1880, 820], fill=(255, 196, 0, 26))
    gd.ellipse([1040, 220, 1780, 780], fill=(0, 198, 255, 18))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)

    draw.line([(100, 52), (1820, 52)], fill=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=100, cy=76, text="NEXON KOREA · RESPONSIVE WEB CASE STUDY", font=get_font(11, 'bold'), theme='gold', pad_x=12, height=28)
    meta = "PC / Mobile WEB  ·  2014.08 - 2015.02  ·  참여율 100% (Main/Sub)  ·  UX/UI Design (PL)"
    draw.text((1820, 76), meta, font=get_font(12.5, 'medium'), fill=TEXT_SUB, anchor='rm')

    draw.text((100, 132), "NEXON WEBSITE · PSYCHIC ACTION RPG", font=get_font(12.5, 'bold'), fill=CL_GOLD_DARK)
    draw.text((100, 162), "미래적 이능 액션의 첫 관문,", font=get_font(30, 'bold'), fill=TEXT_MAIN)
    draw.text((100, 214), "NEXON CLOSERS WEB", font=get_font(42, 'black'), fill=CL_GOLD_DARK)

    sub1 = "넥슨코리아 대표 이능 액션 RPG '클로저스'의 세계관을 PC부터 모바일까지 완벽하게 담아내기 위해,"
    sub2 = "정사각형 타일 블록 기반 6+1 컬럼 반응형 그리드와 역동적 GNB·아티클 인터랙션을 구축했습니다."
    draw.text((100, 294), sub1, font=get_font(13, 'regular'), fill=(71, 85, 105))
    draw.text((100, 320), sub2, font=get_font(13, 'semibold'), fill=(30, 41, 59))

    strengths = [
        ("01", "그리드 엔진", "6+1 Columns · Gutter 0 타일 그리드", "Horizontal & Vertical Resizing",
         "정사각형 블록 형태로 컨텐츠를 정의해 가로뿐만 아니라 세로 해상도 변화에도 비율을 유지하며 동적 리사이징됩니다."),
        ("02", "6단계 반응형", "1920px ~ 543px 6단계 브레이크포인트", "Fluid Multi-Device Flow",
         "대화면 3층 계단식 구조부터 태블릿 4·3컬럼, 모바일 2컬럼까지 블록이 하단 행으로 자연스럽게 애니메이션 정렬됩니다."),
        ("03", "인터랙션", "동적 GNB 리플로우 & 아티클 롤오버", "Engagement-First Motion",
         "GNB 개폐 시 블록 자동 재배치와 아티클 카드 호버 시 최신 소식·바로가기 설명 노출로 유저 참여율을 극대화했습니다."),
        ("04", "통합 브랜드", "세계관 몰입형 6대 서브 페이지 완성", "Cohesive Game Portal UX",
         "넥슨 로그인 연동·무비 플레이어·세계관 소개·GM노트·자유게시판·다운로드까지 일관된 다크·골드 비주얼로 설계했습니다.")
    ]
    max_bw = max(draw.textlength(t, font=get_font(10, 'bold')) + 16 for _, t, _, _, _ in strengths)
    title_x = int(round(144 + max_bw + 18))

    ky = 388
    for idx, (num, tag, tko, ten, desc) in enumerate(strengths):
        rcy = ky + 14
        draw.rounded_rectangle([100, ky + 1, 134, ky + 27], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.text((117, rcy), num, font=get_font(11, 'bold'), fill=CL_GOLD_DARK, anchor='mm')
        draw_pill(draw, left_x=144, cy=rcy, text=tag, font=get_font(10, 'bold'), theme='gold', pad_x=8, height=24)
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

    # Right Side: Real CLOSERS Hero Device
    dev_path = os.path.join(ASSETS_DIR, "closers_hero_device.png")
    if os.path.exists(dev_path):
        dev = Image.open(dev_path).convert('RGBA')
        tw = 840
        th = int(dev.height * (tw / dev.width))
        dev_res = dev.resize((tw, th), Image.Resampling.LANCZOS)
        px, py = 975, 186
        sh = Image.new('RGBA', (tw + 80, th + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([40, 48, tw + 40, th + 48], radius=28, fill=(15, 23, 42, 85))
        sh = sh.filter(ImageFilter.GaussianBlur(28))
        base.paste(sh, (px - 40, py - 32), sh)
        base.paste(dev_res, (px, py), dev_res)

        draw = ImageDraw.Draw(base)
        draw.rounded_rectangle([px + 20, py + th + 24, px + tw - 20, py + th + 78], radius=12, fill=(255, 255, 255, 240), outline=BORDER_LIGHT, width=1)
        bw_d = draw_pill(draw, left_x=px + 38, cy=py + th + 51, text="OFFICIAL PORTAL", font=get_font(9.5, 'bold'), theme='gold', solid=True, pad_x=10, height=22)
        draw.text((px + 38 + bw_d + 14, py + th + 51), "6+1 타일 그리드 · GAME START 시그니처 CTA · 실시간 아티클 메인 포털", font=get_font(11.5, 'bold'), fill=TEXT_MAIN, anchor='lm')

    draw = ImageDraw.Draw(base)
    bar_y, bar_h = 836, 118
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    col_w = 1720 // 4
    specs = [
        ("CLIENT", "넥슨코리아 (Nexon Korea)", "이능 액션 MORPG '클로저스' 공식 웹사이트 구축"),
        ("PERIOD & CONTRIBUTION", "2014.08 - 2015.02 (100% Main/Sub)", "메인·서브 반응형 포털 기획 및 디자인 전담 총괄"),
        ("PROJECT ROLE", "UX/UI Design (PL)", "반응형 그리드 설계 · 인터랙션 정의 · GUI 디자인 리드"),
        ("PLATFORM", "PC / Mobile Responsive WEB", "1920px 데스크톱~543px 모바일 6단계 풀 반응형 웹")
    ]
    for i, (cat, vb, vd) in enumerate(specs):
        cx = 100 + i * col_w
        if i > 0:
            draw.line([(cx, bar_y + 20), (cx, bar_y + bar_h - 20)], fill=BORDER_LIGHT, width=1)
        draw.text((cx + 28, bar_y + 20), cat, font=get_font(10.5, 'bold'), fill=CL_GOLD_DARK)
        draw.text((cx + 28, bar_y + 45), vb, font=get_font(13, 'bold'), fill=TEXT_MAIN)
        draw.text((cx + 28, bar_y + 76), vd, font=get_font(10.5, 'regular'), fill=TEXT_SUB)

    draw_footer(draw, 1)
    base.convert('RGB').save(os.path.join(OUT_DIR, "slide_01.png"), quality=95)
    print("Generated slide_01.png")

# -------------------------------------------------------------
# SLIDE 02: TYPOGRAPHY & COLORS (WORLDVIEW DESIGN SYSTEM)
# -------------------------------------------------------------
def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 2, "TYPOGRAPHY & COLORS",
        "Design System | ", "미래적 이능 액션 세계관을 반영한 컬러 & 타이포그래피 시스템",
        "클로저스 게임 세계관과 톤을 맞추어 미래적이면서도 이능적인(Psychic Action) 에너지가 느껴지는 비주얼 아이덴티티를 정의했습니다.",
        right_badge=("VISUAL IDENTITY", "gold")
    )

    cy, ch = 215, 745
    # LEFT CARD: 6-COLOR SYSTEM (x=100, w=840)
    lx, lw = 100, 840
    draw.rounded_rectangle([lx, cy, lx + lw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=lx + 30, cy=cy + 36, text="BRAND COLOR PALETTE", font=get_font(10, 'bold'), theme='gold', pad_x=10, height=24)
    draw.text((lx + 30, cy + 70), "미래적·이능 컨셉 6대 시맨틱 컬러", font=get_font(20, 'bold'), fill=TEXT_MAIN)
    draw.text((lx + 30, cy + 100), "다크 옵시디언 배경 위에서 시선을 즉각 사로잡는 사이버 골드·시안·블레이즈 오렌지 배색", font=get_font(12, 'regular'), fill=TEXT_SUB)

    swatches = [
        ("Primary · Cyber Gold", "#FFC400", "GAME START CTA · 핵심 롤오버 하이라이트", (255, 196, 0), TEXT_MAIN),
        ("Secondary · Cyber Cyan", "#00C6FF", "SNS 아티클 · 이능 에너지 보조 액센트", (0, 198, 255), TEXT_MAIN),
        ("Accent · Blaze Orange", "#FF5500", "이벤트 강조 · 프로모션 인터랙션 포인트", (255, 85, 0), (255, 255, 255)),
        ("Neutral 9 · Pure White", "#FFFFFF", "다크 배경 위 메인 타이틀 및 본문 텍스트", (255, 255, 255), TEXT_MAIN),
        ("Neutral 5 · Steel Gray", "#999999", "서브 메타 정보 · 비활성 내비게이션 텍스트", (153, 153, 153), (255, 255, 255)),
        ("Neutral 1 · Pitch Black", "#000000", "포털 기본 다크 캔버스 및 GNB 배경", (0, 0, 0), (255, 255, 255)),
    ]
    cw_c = (lw - 60 - 20) // 2
    ch_c = 172
    for idx, (name, hex_c, role, rgb, tc) in enumerate(swatches):
        r, c = idx // 2, idx % 2
        bx = lx + 30 + c * (cw_c + 20)
        by = cy + 144 + r * (ch_c + 18)
        draw.rounded_rectangle([bx, by, bx + cw_c, by + ch_c], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([bx + 14, by + 14, bx + cw_c - 14, by + 92], radius=10, fill=rgb, outline=(203, 213, 225) if hex_c == "#FFFFFF" else None, width=1)
        draw.text((bx + 28, by + 53), hex_c, font=get_font(16, 'black'), fill=tc, anchor='lm')
        draw.text((bx + 16, by + 108), name, font=get_font(13.5, 'bold'), fill=TEXT_MAIN)
        draw.text((bx + 16, by + 134), role, font=get_font(11, 'regular'), fill=TEXT_SUB)

    # RIGHT CARD: TYPOGRAPHY SYSTEM (x=965, w=855)
    rx, rw = 965, 855
    draw.rounded_rectangle([rx, cy, rx + rw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=rx + 30, cy=cy + 36, text="TYPOGRAPHY ARCHITECTURE", font=get_font(10, 'bold'), theme='cyan', pad_x=10, height=24)
    draw.text((rx + 30, cy + 70), "이원화 타이포그래피 시스템 (윤고딕 · 돋움체)", font=get_font(20, 'bold'), fill=TEXT_MAIN)
    draw.text((rx + 30, cy + 100), "프로모션·세계관의 시각적 임팩트와 커뮤니티·공지 게시판의 고밀도 가독성을 동시 최적화", font=get_font(12, 'regular'), fill=TEXT_SUB)

    # Font Card 1: 윤고딕
    f1_y = cy + 146
    draw.rounded_rectangle([rx + 30, f1_y, rx + rw - 30, f1_y + 225], radius=14, fill=(15, 23, 42))
    draw_pill(draw, left_x=rx + 54, cy=f1_y + 34, text="DISPLAY & HEADLINE", font=get_font(9.5, 'bold'), theme='gold', solid=True, pad_x=10, height=22)
    draw.text((rx + 54, f1_y + 66), "윤고딕 (Yoon Gothic)", font=get_font(30, 'black'), fill=(255, 255, 255))
    draw.text((rx + 54, f1_y + 120), "눈 뜨지 못한 자들이여, 그림으로 도전 할 텐가?", font=get_font(18, 'bold'), fill=CL_GOLD_BRIGHT)
    draw.text((rx + 54, f1_y + 158), "프로모션 히어로 카피 · GAME START CTA · 섹션 타이틀 · 아티클 롤오버 헤드라인", font=get_font(11.5, 'regular'), fill=(148, 163, 184))
    draw.text((rx + 54, f1_y + 184), "Whereas a common understanding of these rights and freedoms is of the greatest importance.", font=get_font(10.5, 'medium'), fill=(100, 116, 139))

    # Font Card 2: 돋움체
    f2_y = f1_y + 245
    draw.rounded_rectangle([rx + 30, f2_y, rx + rw - 30, f2_y + 215], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=rx + 54, cy=f2_y + 34, text="BODY & COMMUNITY UI", font=get_font(9.5, 'bold'), theme='cyan', pad_x=10, height=22)
    draw.text((rx + 54, f2_y + 66), "돋움체 (Dotum)", font=get_font(28, 'bold'), fill=TEXT_MAIN)
    draw.text((rx + 54, f2_y + 116), "GM노트 · 자유게시판 · 공지사항 · 권장사양 테이블 등 고밀도 정보 가독성 표준", font=get_font(13, 'medium'), fill=(51, 65, 85))
    draw.text((rx + 54, f2_y + 148), "국제연합의 모든 사람들은 그 헌장에서 기본적 인권, 인간의 존엄과 가치에 대한 신념을 재확인", font=get_font(12, 'regular'), fill=TEXT_SUB)
    draw.text((rx + 54, f2_y + 176), "Whereas a common understanding of these rights and freedoms is", font=get_font(11, 'regular'), fill=(148, 163, 184))

    # Bottom Principle Strip
    draw.rounded_rectangle([rx + 30, cy + ch - 96, rx + rw - 30, cy + ch - 26], radius=12, fill=(255, 251, 235), outline=CL_GOLD, width=1)
    draw.text((rx + rw // 2, cy + ch - 61), "다크 캔버스 위 Cyber Gold(#FFC400) CTA 단일 강조로 게임 실행(GAME START) 전환 동선 극대화", font=get_font(12, 'bold'), fill=CL_GOLD_DARK, anchor='mm')

    draw_footer(draw, 2)
    img.save(os.path.join(OUT_DIR, "slide_02.png"), quality=95)
    print("Generated slide_02.png")

# -------------------------------------------------------------
# SLIDE 03: RESPONSIVE GRID ARCHITECTURE (6+1 COLUMNS, GUTTER 0)
# -------------------------------------------------------------
def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 3, "RESPONSIVE GRID SYSTEM",
        "Responsive Design | ", "6+1 컬럼(Gutter 0) 정사각형 블록 가로·세로 동적 리사이징 그리드",
        "기본 6 Columns + 좌측 GNB 1 Column(총 7 Columns, Gutter 0)으로 구성하여 가로뿐만 아니라 세로 뷰포트 변화에도 자동 대응합니다.",
        right_badge=("7-COL TILE GRID", "gold")
    )

    cy, ch = 215, 745
    # LEFT MAIN SHOWCASE: Real 7-Col Grid Overlay (x=100, w=1120)
    lx, lw = 100, 1120
    draw.rounded_rectangle([lx, cy, lx + lw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_g = draw_pill(draw, left_x=lx + 26, cy=cy + 34, text="BASIC : 6 COLUMNS + 1 COLUMN (GNB), GUTTER 0", font=get_font(10, 'bold'), theme='gold', solid=True, pad_x=12, height=24)
    draw.text((lx + 26 + bw_g + 14, cy + 34), "실물 7컬럼 정사각형 타일 그리드 오버레이", font=get_font(13, 'bold'), fill=TEXT_MAIN, anchor='lm')

    g_src = Image.open(os.path.join(ASSETS_DIR, "03_responsive_grid.jpg")).convert('RGB')
    # Crop just the tablet + pink column overlay area (y=195..565, x=220..804)
    g_crop = g_src.crop((215, 195, 810, 565))
    inner_w, inner_h = lw - 52, ch - 104
    sc = min(inner_w / g_crop.width, inner_h / g_crop.height)
    tw, th = int(g_crop.width * sc), int(g_crop.height * sc)
    px = lx + (lw - tw) // 2
    py = cy + 72 + (inner_h - th) // 2
    img.paste(g_crop.resize((tw, th), Image.Resampling.LANCZOS), (px, py))

    # RIGHT COLUMN: 3 Grid Architecture Specs (x=1245, w=575)
    rx, rw = 1245, 575
    draw.rounded_rectangle([rx, cy, rx + rw, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=rx + 26, cy=cy + 34, text="GRID ENGINEERING", font=get_font(10, 'bold'), theme='dark', pad_x=10, height=24)
    draw.text((rx + 26, cy + 68), "가로·세로 양방향 반응형 설계 원칙", font=get_font(18, 'bold'), fill=TEXT_MAIN)

    grid_specs = [
        ("01. 6+1 컬럼 & Gutter 0 밀착 구조", "gold",
         "좌측 1컬럼은 접이식 GNB 영역으로 고정하고 우측 6컬럼을 컨텐츠 아티클 영역으로 배정했습니다. 여백(Gutter)을 0으로 설계해 일러스트·캐릭터 비주얼이 화면을 가득 채우는 몰입감을 구현했습니다."),
        ("02. 정사각형(1:1) 타일 모듈화", "cyan",
         "모든 아티클(다운로드·영상·공지·자유게시판·캐릭터)과 GAME START CTA를 1:1 정사각형 블록 단위로 표준화해 해상도가 달라져도 시각적 왜곡 없이 매끄럽게 재배열됩니다."),
        ("03. 세로 뷰포트 대응 동적 Resizing", "orange",
         "기존 가로 중심 반응형을 넘어 브라우저의 세로 높이 변화까지 감지해 블록 크기를 비율에 맞게 자동 리사이징함으로써 첫 화면(Above the Fold)에 핵심 CTA와 아티클이 항상 완벽하게 노출됩니다.")
    ]
    sy = cy + 116
    for title, th, desc in grid_specs:
        draw.rounded_rectangle([rx + 26, sy, rx + rw - 26, sy + 188], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=rx + 42, cy=sy + 28, text=title, font=get_font(11, 'bold'), theme=th, pad_x=10, height=24)
        lines = wrap_text(desc, get_font(11.5, 'regular'), rw - 84, draw)
        dy = sy + 58
        for l in lines[:5]:
            draw.text((rx + 42, dy), l, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
            dy += 22
        sy += 204

    draw_footer(draw, 3)
    img.save(os.path.join(OUT_DIR, "slide_03.png"), quality=95)
    print("Generated slide_03.png")

# -------------------------------------------------------------
# SLIDE 04: 6-STAGE BREAKPOINT SYSTEM (1920px -> 543px)
# -------------------------------------------------------------
def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 4, "6-STAGE BREAKPOINT FLOW",
        "Fluid Breakpoints | ", "1920px 데스크톱부터 543px 모바일까지 6단계 반응형 전환",
        "해상도 구간마다 6→5→4→3→2컬럼으로 블록이 하단 행으로 부드럽게 애니메이션 이동하며 최적의 게임 포털 경험을 유지합니다.",
        right_badge=("6 BREAKPOINTS", "gold")
    )

    # Main Full-Width Showcase Card (y=215..855, h=640)
    my, mh = 215, 640
    draw.rounded_rectangle([100, my, 1820, my + mh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bp_src = Image.open(os.path.join(ASSETS_DIR, "04_breakpoints_6step.png")).convert('RGBA')
    inner_w, inner_h = 1660, 596
    sc = min(inner_w / bp_src.width, inner_h / bp_src.height)
    tw, th = int(bp_src.width * sc), int(bp_src.height * sc)
    px = 100 + (1720 - tw) // 2
    py = my + (mh - th) // 2
    img.paste(bp_src.resize((tw, th), Image.Resampling.LANCZOS), (px, py), bp_src.resize((tw, th), Image.Resampling.LANCZOS))

    # Bottom 6-Stage Summary Strip (y=874..960, h=86)
    by, bh = 874, 86
    draw.rounded_rectangle([100, by, 1820, by + bh], radius=14, fill=(15, 23, 42))
    stages = [
        ("@1661-1920+", "3층 계단식 · 좌측 GNB"),
        ("@1361-1660", "상단 헤더 · 가로 6-Col"),
        ("@1089-1360", "가로 5-Col 애니메이션"),
        ("@817-1088", "가로 4-Col 태블릿 가로"),
        ("@544-816", "가로 3-Col 태블릿 세로"),
        ("@543 이하", "가로 2-Col · 키비주얼 숨김")
    ]
    sw = 1720 // 6
    for idx, (bp, desc) in enumerate(stages):
        sx = 100 + idx * sw
        if idx > 0:
            draw.line([(sx, by + 18), (sx, by + bh - 18)], fill=(51, 65, 85), width=1)
        draw.text((sx + sw // 2, by + 28), bp, font=get_font(12, 'black'), fill=CL_GOLD_BRIGHT if idx in [0, 5] else CL_CYAN, anchor='mm')
        draw.text((sx + sw // 2, by + 56), desc, font=get_font(10.5, 'medium'), fill=(226, 232, 240), anchor='mm')

    draw_footer(draw, 4)
    img.save(os.path.join(OUT_DIR, "slide_04.png"), quality=95)
    print("Generated slide_04.png")

# -------------------------------------------------------------
# SLIDE 05: DYNAMIC GNB REFLOW INTERACTION
# -------------------------------------------------------------
def make_slide_05():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 5, "INTERACTION 01 · DYNAMIC GNB",
        "GNB Reflow Interaction | ", "GNB 개폐에 연동되는 블록 자동 감산 및 하단 Row 애니메이션",
        "GNB가 표시될 때는 현재 블록 개수에서 1개 블록이 빠진 Row로 자동 정렬되며, 빠진 블록은 하단 Row로 매끄럽게 이동합니다.",
        right_badge=("LIVE GNB MOTION", "gold")
    )

    cy, ch = 215, 745
    # Main 2-Screen Visual Card (y=215..780, h=565)
    draw.rounded_rectangle([100, cy, 1820, cy + 565], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    gnb_src = Image.open(os.path.join(ASSETS_DIR, "05_gnb_interaction.jpg")).convert('RGB')
    # Crop just the 2 side-by-side monitors (y=190..480, x=50..974)
    gnb_crop = gnb_src.crop((45, 188, 978, 482))
    inner_w, inner_h = 1660, 485
    sc = min(inner_w / gnb_crop.width, inner_h / gnb_crop.height)
    tw, th = int(gnb_crop.width * sc), int(gnb_crop.height * sc)
    px = 100 + (1720 - tw) // 2
    py = cy + 28
    img.paste(gnb_crop.resize((tw, th), Image.Resampling.LANCZOS), (px, py))

    # Labels right under the 2 monitors
    draw_pill(draw, cx=530, cy=cy + 530, text="STATE A · 좌측 GNB 펼침 (메뉴 1-Col + 아티클 5-Col)", font=get_font(11, 'bold'), theme='gold', solid=True, pad_x=14, height=26)
    draw_pill(draw, cx=1390, cy=cy + 530, text="STATE B · 상단 GNB 접힘 (전체 6-Col 풀와이드 확장)", font=get_font(11, 'bold'), theme='cyan', solid=True, pad_x=14, height=26)

    # Bottom 3 Interaction Spec Cards (y=800..960, h=160)
    by, bh = 800, 160
    sw = (1720 - 48) // 3
    specs = [
        ("01. N-1 컬럼 자동 계산", "좌측 GNB가 열리면 가용 가로폭에 맞춰 아티클 열을 자동으로 1열 축소해 레이아웃 깨짐을 원천 방지합니다.", "gold"),
        ("02. 하단 Row 애니메이션 재배치", "밀려난 우측 끝 블록은 즉시 사라지지 않고 부드러운 트랜지션으로 하단 Row에 재배치되어 시각적 연속성을 유지합니다.", "cyan"),
        ("03. 게임 포털 특화 시선 유지", "GNB를 접었을 때 상단 블랙/옐로우 주의선 헤더가 나타나며 캐릭터 프로모션 배너가 최대 크기로 확장됩니다.", "orange")
    ]
    for idx, (st, sd, th_c) in enumerate(specs):
        sx = 100 + idx * (sw + 24)
        draw.rounded_rectangle([sx, by, sx + sw, by + bh], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=sx + 22, cy=by + 28, text=st, font=get_font(10.5, 'bold'), theme=th_c, pad_x=10, height=22)
        lines = wrap_text(sd, get_font(11.5, 'regular'), sw - 44, draw)
        dy = by + 56
        for l in lines[:3]:
            draw.text((sx + 22, dy), l, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
            dy += 21

    draw_footer(draw, 5)
    img.save(os.path.join(OUT_DIR, "slide_05.png"), quality=95)
    print("Generated slide_05.png")

# -------------------------------------------------------------
# SLIDE 06: CONTENTS ARTICLE & HOVER INTERACTION
# -------------------------------------------------------------
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 6, "INTERACTION 02 · CONTENTS ARTICLE",
        "Contents & Hover UX | ", "유저 참여를 유도하는 아티클 카드 기본 vs 롤오버 인터랙션",
        "평소에는 게임 일러스트와 대표 이미지로 시각적 매력을 극대화하고, 마우스 롤오버 시 최신 데이터와 바로가기 설명을 즉시 제공합니다.",
        right_badge=("HOVER ENGAGEMENT", "gold")
    )

    cy = 215
    draw.rounded_rectangle([100, cy, 1820, cy + 565], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    ct_src = Image.open(os.path.join(ASSETS_DIR, "06_contents_hover.jpg")).convert('RGB')
    # Crop the 2 side-by-side monitors (y=176..464, x=50..974)
    ct_crop = ct_src.crop((48, 176, 976, 464))
    inner_w, inner_h = 1660, 485
    sc = min(inner_w / ct_crop.width, inner_h / ct_crop.height)
    tw, th = int(ct_crop.width * sc), int(ct_crop.height * sc)
    px = 100 + (1720 - tw) // 2
    py = cy + 28
    img.paste(ct_crop.resize((tw, th), Image.Resampling.LANCZOS), (px, py))

    draw_pill(draw, cx=530, cy=cy + 530, text="DEFAULT · 메인 아티클 기본 상태 (대표 이미지 & 바로가기 제목)", font=get_font(11, 'bold'), theme='dark', solid=True, pad_x=14, height=26)
    draw_pill(draw, cx=1390, cy=cy + 530, text="HOVER · 아티클 롤오버 상태 (최신 데이터 & 골드/시안 컬러 피드백)", font=get_font(11, 'bold'), theme='gold', solid=True, pad_x=14, height=26)

    # Bottom 3 Engagement Specs (y=800..960)
    by, bh = 800, 160
    sw = (1720 - 48) // 3
    specs = [
        ("01. 시각적 몰입 우선 (Default)", "복잡한 텍스트 리스트를 숨기고 고품질 캐릭터·영상 썸네일 중심으로 배치해 게임 포털 특유의 매력을 극대화했습니다.", "dark"),
        ("02. 즉각적 정보 확장 (Rollover)", "마우스 오버 시 해당 아티클의 최신 공지·게시글 요약이나 다운로드·SNS 바로가기 설명이 선명한 컬러 카드로 전환됩니다.", "gold"),
        ("03. 컬러 기반 기능 식별", "핵심 액션(다운로드·공지)은 Cyber Gold(#FFC400), 소셜(페이스북)은 Cyber Cyan(#00C6FF)으로 직관적 구분이 가능합니다.", "cyan")
    ]
    for idx, (st, sd, th_c) in enumerate(specs):
        sx = 100 + idx * (sw + 24)
        draw.rounded_rectangle([sx, by, sx + sw, by + bh], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=sx + 22, cy=by + 28, text=st, font=get_font(10.5, 'bold'), theme=th_c, pad_x=10, height=22)
        lines = wrap_text(sd, get_font(11.5, 'regular'), sw - 44, draw)
        dy = by + 56
        for l in lines[:3]:
            draw.text((sx + 22, dy), l, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
            dy += 21

    draw_footer(draw, 6)
    img.save(os.path.join(OUT_DIR, "slide_06.png"), quality=95)
    print("Generated slide_06.png")

# -------------------------------------------------------------
# SLIDE 07: 6 CORE SUB-PAGES MULTI-SCREEN GALLERY
# -------------------------------------------------------------
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 7, "PRODUCTION SUB-PAGES GALLERY",
        "6 Core Sub-Pages | ", "로그인부터 다운로드까지 일관된 게임 세계관 6대 상용 화면",
        "넥슨 로그인 연동·무비 플레이어·세계관 게임소개·GM노트·자유게시판·클라이언트 다운로드까지 6개 핵심 서브 페이지를 완성했습니다.",
        right_badge=("6-SCREEN GALLERY", "gold")
    )

    cy, ch = 215, 745
    draw.rounded_rectangle([100, cy, 1820, cy + ch], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)

    sub_src = Image.open(os.path.join(ASSETS_DIR, "07_subpages_6screens.png")).convert('RGBA')
    inner_w, inner_h = 1640, 685
    sc = min(inner_w / sub_src.width, inner_h / sub_src.height)
    tw, th = int(sub_src.width * sc), int(sub_src.height * sc)
    px = 100 + (1720 - tw) // 2
    py = cy + (ch - th) // 2
    img.paste(sub_src.resize((tw, th), Image.Resampling.LANCZOS), (px, py), sub_src.resize((tw, th), Image.Resampling.LANCZOS))

    draw_footer(draw, 7)
    img.save(os.path.join(OUT_DIR, "slide_07.png"), quality=95)
    print("Generated slide_07.png")

# -------------------------------------------------------------
# SLIDE 08: OUTCOMES & STAR RETROSPECTIVE
# -------------------------------------------------------------
def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw, 8, "OUTCOMES & RETROSPECTIVE",
        "Outcomes & STAR | ", "게임 포털 반응형 UX 혁신 성과 및 시니어 PL 회고",
        "기존 고정폭 게임 웹사이트의 한계를 극복한 6+1 반응형 타일 그리드 아키텍처의 성과와 STAR 기법 기반 회고입니다.",
        right_badge=("PROJECT OUTCOMES", "gold")
    )

    # TIER 1: BEFORE vs AFTER (y=215..475)
    t1_y, t1_h, half_w = 215, 260, 848
    lx = 100
    draw.rounded_rectangle([lx, t1_y, lx + half_w, t1_y + t1_h], radius=16, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill(draw, left_x=lx + 26, cy=t1_y + 32, text="BEFORE · 기존 고정폭 게임 웹사이트", font=get_font(10, 'bold'), theme='gray', pad_x=10, height=22)
    draw.text((lx + 26, t1_y + 58), "PC 고정폭 레이아웃 · 단절된 모바일 · 텍스트 과밀 게시판", font=get_font(16, 'bold'), fill=TEXT_MAIN)
    for idx, (k, v) in enumerate([
        ("디바이스 대응", "PC 고정 해상도 기준으로 모바일·태블릿에서 별도 사이트 운영 비효율"),
        ("정보 노출 방식", "텍스트 공지·배너 나열로 신작 게임의 세계관 몰입감 및 클릭률 저하"),
        ("네비게이션 UX", "고정 상단 메뉴로 화면 공간 제약 및 해상도별 콘텐츠 잘림 발생")
    ]):
        by = t1_y + 94 + idx * 52
        draw.rounded_rectangle([lx + 26, by, lx + half_w - 26, by + 44], radius=8, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 42, by + 22), k, font=get_font(11.5, 'bold'), fill=TEXT_SUB, anchor='lm')
        draw.text((lx + 205, by + 22), v, font=get_font(11.5, 'regular'), fill=TEXT_MAIN, anchor='lm')

    rx = 972
    draw.rounded_rectangle([rx, t1_y, rx + half_w, t1_y + t1_h], radius=16, fill=(255, 251, 235), outline=CL_GOLD, width=1)
    draw_pill(draw, left_x=rx + 26, cy=t1_y + 32, text="AFTER · NEXON CLOSERS RESPONSIVE WEB", font=get_font(10, 'bold'), theme='gold', solid=True, pad_x=10, height=22)
    draw.text((rx + 26, t1_y + 58), "가로·세로 양방향 6+1 반응형 타일 그리드 포털 표준 확립", font=get_font(16, 'bold'), fill=TEXT_MAIN)
    for idx, (k, v) in enumerate([
        ("디바이스 대응", "1920px~543px 6단계 브레이크포인트로 PC·모바일 단일 코드베이스 완결"),
        ("정보 노출 방식", "1:1 아티클 카드 기본 비주얼 + 롤오버 최신 데이터 확장으로 참여 극대화"),
        ("네비게이션 UX", "접이식 좌측 GNB 및 N-1 블록 자동 리플로우 애니메이션으로 쾌적한 탐색")
    ]):
        ay = t1_y + 94 + idx * 52
        draw.rounded_rectangle([rx + 26, ay, rx + half_w - 26, ay + 44], radius=8, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
        draw.text((rx + 42, ay + 22), k, font=get_font(11.5, 'bold'), fill=CL_GOLD_DARK, anchor='lm')
        draw.text((rx + 205, ay + 22), v, font=get_font(11.5, 'semibold'), fill=TEXT_MAIN, anchor='lm')

    # TIER 2: 4 QUANTITATIVE KPI CARDS (y=495..620)
    t2_y, t2_h, mw = 495, 125, 412
    kpis = [
        ("RESPONSIVE ENGINE", "6-Stage", "1920px ~ 543px 풀 반응형", "가로·세로 동적 리사이징 6단계 브레이크포인트", "gold"),
        ("OWNERSHIP", "100%", "Main / Sub 단독 PL 총괄", "넥슨코리아 공식 웹 UX/UI 설계 및 디자인 리드", "gold"),
        ("TILE ARCHITECTURE", "6+1 Col", "Gutter 0 정사각형 타일 시스템", "GNB 연동 N-1 블록 자동 리플로우 애니메이션", "cyan"),
        ("PORTAL SCOPE", "6-Core", "통합 서브 페이지 일관 UX", "로그인·무비·세계관·GM노트·게시판·다운로드", "orange")
    ]
    for idx, (kb, kv, kt, kd, kth) in enumerate(kpis):
        mx = 100 + idx * (mw + 24)
        draw.rounded_rectangle([mx, t2_y, mx + mw, t2_y + t2_h], radius=14, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=mx + 22, cy=t2_y + 24, text=kb, font=get_font(9, 'bold'), theme=kth, pad_x=8, height=18)
        vc = CL_GOLD_DARK if kth == 'gold' else (CL_CYAN if kth == 'cyan' else CL_ORANGE)
        draw.text((mx + 22, t2_y + 42), kv, font=get_font(26, 'black'), fill=vc)
        draw.text((mx + 22, t2_y + 82), kt, font=get_font(12, 'bold'), fill=TEXT_MAIN)
        draw.text((mx + 22, t2_y + 102), kd, font=get_font(10, 'regular'), fill=TEXT_SUB)

    # TIER 3: STAR RETROSPECTIVE (y=640..960)
    sy, sw, sh = 640, 1720, 320
    draw.rounded_rectangle([100, sy, 100 + sw, sy + sh], radius=16, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    bw_s = draw_pill(draw, left_x=126, cy=sy + 32, text="SENIOR UX STRATEGY RETROSPECTIVE (STAR)", font=get_font(10, 'bold'), theme='gold', solid=True, pad_x=12, height=24)
    draw.text((126 + bw_s + 16, sy + 32), "이능 액션 게임 세계관과 고난도 6+1 반응형 타일 그리드를 결합한 포털 설계 회고", font=get_font(15, 'bold'), fill=TEXT_MAIN, anchor='lm')

    stars = [
        ("S · Situation (상황)", "넥슨코리아 신작 이능 액션 RPG '클로저스' 론칭을 앞두고, PC와 모바일 모든 환경에서 강렬한 세계관 몰입감과 높은 커뮤니티 참여를 이끌어낼 차세대 공식 웹사이트가 필요했습니다."),
        ("T · Task (과제)", "가로 해상도뿐 아니라 세로 비율 변화에도 GAME START CTA와 핵심 아티클이 잘리지 않고, GNB 개폐 시 자연스럽게 재정렬되는 고도화된 반응형 그리드 시스템을 설계해야 했습니다."),
        ("A · Action (실행)", "6+1 컬럼(Gutter 0) 정사각형 타일 구조와 1920px~543px 6단계 브레이크포인트를 정의하고, GNB 연동 N-1 블록 리플로우·아티클 롤오버 정보 확장·6대 서브 페이지 캐릭터 가이드를 구현했습니다."),
        ("R · Result (성과)", "단일 반응형 아키텍처로 PC·태블릿·모바일 전 기기에서 일관된 클로저스 브랜드 경험을 성공적으로 론칭하며, 게임 포털 반응형 UX의 선도적 레퍼런스를 확립했습니다.")
    ]
    sc_w = (sw - 52 - 60) // 4
    for idx, (st, sdesc) in enumerate(stars):
        sx = 126 + idx * (sc_w + 20)
        draw.rounded_rectangle([sx, sy + 66, sx + sc_w, sy + sh - 22], radius=12, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw_pill(draw, left_x=sx + 18, cy=sy + 92, text=st, font=get_font(10, 'bold'), theme='gold' if idx in [0, 3] else 'cyan', pad_x=10, height=22)
        lines = wrap_text(sdesc, get_font(11, 'regular'), sc_w - 36, draw)
        ly = sy + 120
        for l in lines:
            draw.text((sx + 18, ly), l, font=get_font(11, 'regular'), fill=TEXT_SUB)
            ly += 21

    draw_footer(draw, 8)
    img.save(os.path.join(OUT_DIR, "slide_08.png"), quality=95)
    print("Generated slide_08.png")

if __name__ == '__main__':
    for fn in [make_slide_01, make_slide_02, make_slide_03, make_slide_04, make_slide_05, make_slide_06, make_slide_07, make_slide_08]:
        fn()
    pdf_path = os.path.join(BASE_DIR, "Nexon_Closers_Responsive_Web_Portfolio.pdf")
    slides = [Image.open(os.path.join(OUT_DIR, f"slide_{i:02d}.png")).convert('RGB') for i in range(1, TOTAL_SLIDES + 1)]
    slides[0].save(pdf_path, save_all=True, append_images=slides[1:], resolution=100.0)
    print(f"Successfully compiled {len(slides)} slides -> {pdf_path}")
