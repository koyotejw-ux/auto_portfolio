import os
from PIL import Image, ImageDraw
from deck_common import *

def make_slide_09():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 9, "DESIGN SYSTEM & TOKENS", "Color, Typography & Components", "토지개발 플랫폼 디자인 시스템 & 아토믹 토큰", "Primary-500(#00C65F), Spacing(4~40px), Corner Radius(4~999px), Stroke 시스템 명세")

    rx = 80
    rw = W - 160
    ry = 260
    rh = 690
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    ds_path = os.path.join(ASSETS_DIR, "part_design_tokens.png")
    if os.path.exists(ds_path):
        ds_img = Image.open(ds_path).convert('RGBA')
        scale = min((rw - 60) / ds_img.width, (rh - 60) / ds_img.height)
        nw = int(ds_img.width * scale)
        nh = int(ds_img.height * scale)
        d_res = ds_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(d_res, (rx + (rw - nw) // 2, ry + (rh - nh) // 2), d_res)

    draw_slide_footer(draw, 9, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_09.png"), quality=95)
    print("Generated slide_09.png")

def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 10, "CORE UI & RESPONSIVE PROTOTYPE", "Responsive Multi-Device Views", "반응형 멀티 디바이스 프로토타입 (Desktop & Mobile)", "데스크톱 듀얼 스플릿 대화면과 모바일 현장 터치 최적화 뷰포트 설계")

    # Left: Mobile Map & Analysis View
    lx = 80
    lw = 540
    draw.rounded_rectangle([lx, 260, lx + lw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, lx + 25, 295, "MOBILE ONSITE VIEW", get_font(10.5, 'bold'), theme='green')
    draw.text((lx + 25, 335), "현장 실사 모바일 최적화", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    m_p = os.path.join(FIG_DIR, "18e703c31b8c3ee8a45a40b94efab8fd98786b70.png")
    if not os.path.exists(m_p):
        m_p = os.path.join(ASSETS_DIR, "screen_02_map_analysis.png")
    if os.path.exists(m_p):
        m_img = Image.open(m_p).convert('RGBA')
        scale = min((lw - 60) / m_img.width, (950 - 380 - 40) / m_img.height)
        mw = int(m_img.width * scale)
        mh = int(m_img.height * scale)
        m_res = m_img.resize((mw, mh), Image.Resampling.LANCZOS)
        img.paste(m_res, (lx + (lw - mw) // 2, 380 + (950 - 380 - mh) // 2), m_res)

    # Right: Desktop Web GIS View
    rx = 650
    rw = W - 80 - rx
    draw.rounded_rectangle([rx, 260, rx + rw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, rx + 25, 295, "DESKTOP GIS CONSOLE", get_font(10.5, 'bold'), theme='green')
    draw.text((rx + 25, 335), "대화면 공간 GIS 분석 콘솔", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    d_p = os.path.join(ASSETS_DIR, "screen_03_facility_layout.png")
    if os.path.exists(d_p):
        d_img = Image.open(d_p).convert('RGBA')
        scale = min((rw - 60) / d_img.width, (950 - 380 - 40) / d_img.height)
        dw = int(d_img.width * scale)
        dh = int(d_img.height * scale)
        d_res = d_img.resize((dw, dh), Image.Resampling.LANCZOS)
        img.paste(d_res, (rx + (rw - dw) // 2, 380 + (950 - 380 - dh) // 2), d_res)

    draw_slide_footer(draw, 10, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_10.png"), quality=95)
    print("Generated slide_10.png")

def make_slide_11():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 11, "UI SCREENS SHOWCASE", "Isometric 3D Screen Showcase", "전체 UI 화면 설계 및 파노라마 쇼케이스", "토지 탐색, 시설 배치, 작물 선택, 상세 설계, 종합 타당성 분석 보고서 엔드투엔드 화면 구성")

    # High-impact Isometric Showcase Frame
    rx = 80
    rw = W - 160
    ry = 260
    rh = 690
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)

    iso_p = os.path.join(FIG_DIR, "718485fcee490c2d75e225ff483c610efb054a00.png")
    if not os.path.exists(iso_p):
        iso_p = os.path.join(ASSETS_DIR, "screen_07_report_summary.png")
    if os.path.exists(iso_p):
        iso_img = Image.open(iso_p).convert('RGBA')
        scale = min((rw - 40) / iso_img.width, (rh - 40) / iso_img.height)
        iw = int(iso_img.width * scale)
        ih = int(iso_img.height * scale)
        i_res = iso_img.resize((iw, ih), Image.Resampling.LANCZOS)
        img.paste(i_res, (rx + (rw - iw) // 2, ry + (rh - ih) // 2), i_res)

    draw_slide_footer(draw, 11, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_11.png"), quality=95)
    print("Generated slide_11.png")

def make_slide_12():
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 12, "PROJECT RETROSPECTIVE & OUTCOMES", "Business Outcomes & STAR Retrospective", "프로젝트 성과 지표 및 STAR 기법 회고", "인허가 분석 시간 90% 단축과 토지주-개발사-투자사 간 신뢰 기반 협업 체계 확립", dark_mode=True)

    # 4 Quantitative Impact Cards (Exact from User Figma)
    metrics = [
        ("100+", "분석 가능 토지 규제", "국토계획법, 산지관리법, 농지법 등 100여 개 공공 인허가 조건 자동 매칭"),
        ("90%", "분석 소요 시간 단축", "기존 2주 이상 걸리던 전문가 현장/서류 검토를 3~5초 내 실시간 진단"),
        ("3~5s", "원터치 시뮬레이션", "지번 입력 즉시 최적 단지 구획 및 시설 조성비 산출 자동화"),
        ("40%", "의사결정 정확도 향상", "데이터 기반의 정량적 타당성 검토를 통해 사업 리스크 사전 방지")
    ]
    mx = 80
    for num, title, desc in metrics:
        draw.rounded_rectangle([mx, 250, mx + 415, 450], radius=16, fill=CARD_DARK, outline=BORDER_DARK, width=1)
        draw.text((mx + 25, 280), num, font=get_font(32, 'black'), fill=BRAND_LIGHT)
        draw.text((mx + 25, 335), title, font=get_font(18, 'bold'), fill=(255, 255, 255))
        draw.text((mx + 25, 375), desc, font=get_font(13, 'regular'), fill=TEXT_DARK_SUB)
        mx += 440

    # STAR Retrospective Card (200자 이상 시니어급 기술 회고)
    draw.rounded_rectangle([80, 480, W - 80, 950], radius=16, fill=CARD_DARK, outline=BORDER_DARK, width=1)
    draw_pill_badge(draw, 110, 515, "SENIOR UX STRATEGY RETROSPECTIVE (STAR)", get_font(11, 'bold'), theme='dark_green')
    draw.text((110, 555), "공간 GIS와 금융 데이터가 융합된 복잡계를 단순하고 명쾌한 UX로 전환한 여정", font=get_font(22, 'bold'), fill=(255, 255, 255))

    star_items = [
        ("Situation (상황 및 배경)", "토지개발은 공간 지적도, 수많은 건축 조례, 복잡한 인허가 법률, 거액의 자금 조달이 얽혀 있어 정보 비대칭이 극심하고, 비전문가인 토지 소유주가 사업성을 검토하기에는 진입 장벽이 매우 높은 시장이었습니다."),
        ("Task (해결 과제 및 목표)", "복잡한 법률·규제 데이터를 사용자가 학습하지 않고도 직관적으로 이해할 수 있는 단일 인터랙션 플로우를 구축하고, 대상지 선택부터 시설 배치, 수확량 예측, 경제성 타당성 보고서 출력까지 원스톱으로 지원하는 B2B 플랫폼 아키텍처를 완성해야 했습니다."),
        ("Action (실행 전략 및 디자인 결정)", "좌측 420px 워크플로우 패널과 우측 인터랙티브 GIS 캔버스의 듀얼 스플릿 뷰를 설계하여 조작 편의성을 극대화했습니다. 12대 공공 데이터를 3단계 계층 구조로 정제하고, 개발 불가 구역을 붉은색 히트맵으로 시각화하여 리스크 인지율을 100% 확보했습니다. 또한 고대비 에머랄드 그린 디자인 시스템을 구축하여 복잡한 재무 지표를 한눈에 파악하도록 최적화했습니다."),
        ("Result & Learning (성과 및 회고)", "기존 2주 이상 소요되던 토지 타당성 분석 기간을 3~5초로 90% 이상 단축했으며, 토지주-개발사-투자사 간 신뢰 기반의 협업 허브를 구축했습니다. 방대한 전문 도메인 지식을 프로덕트 디자이너의 직관적 UX 아키텍처로 체계화함으로써 비즈니스 가치를 극대화한 프로젝트였습니다.")
    ]
    sy = 605
    for tag, text in star_items:
        draw.text((110, sy), tag, font=get_font(14, 'bold'), fill=BRAND_LIGHT)
        draw.text((110, sy + 25), text, font=get_font(13, 'regular'), fill=TEXT_DARK_MAIN)
        sy += 78

    draw_slide_footer(draw, 12, 12, dark_mode=True)
    img.save(os.path.join(OUT_DIR, "slide_12.png"), quality=95)
    print("Generated slide_12.png")

if __name__ == '__main__':
    make_slide_09()
    make_slide_10()
    make_slide_11()
    make_slide_12()
