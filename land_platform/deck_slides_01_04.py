import os
from PIL import Image, ImageDraw
from deck_common import *

def make_slide_01():
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Hero Title & Metadata
    draw_pill_badge(draw, 100, 160, "PROPTECH & GIS B2B CLOUD", get_font(12, 'bold'), theme='dark_green')
    draw.text((100, 240), "토지개발사업 분석 플랫폼", font=get_font(46, 'black'), fill=(255, 255, 255))
    draw.text((100, 310), "FARMINGSYS · B2B LAND DEVELOPMENT PLATFORM", font=get_font(18, 'bold'), fill=BRAND_LIGHT)
    
    desc = [
        "복잡한 토지 규제와 인허가, 공간 GIS 빅데이터를 3단계 계층 구조로 시각화하여",
        "토지 소유자, 지자체, 전문 개발사, 금융 투자자를 원스톱으로 연결하는",
        "국내 유일의 엔터프라이즈급 토지개발 사업 타당성 및 경제성 자동 시뮬레이션 SaaS"
    ]
    dy = 370
    for line in desc:
        draw.text((100, dy), line, font=get_font(16, 'regular'), fill=TEXT_DARK_SUB)
        dy += 32
        
    # Project Specs Card
    specs = [
        ("PROJECT", "토지개발사업 분석 플랫폼 구축"),
        ("ROLE", "B2B UX/UI 아키텍처 및 디자인 총괄 (100%)"),
        ("PERIOD", "2024.12 - 2025.01 (8주)"),
        ("PLATFORM", "Responsive Web & Cloud SaaS (Desktop Focused)")
    ]
    sy = 520
    draw.rounded_rectangle([100, sy, 720, sy + 280], radius=16, fill=CARD_DARK, outline=BORDER_DARK, width=1)
    spy = sy + 30
    for label, val in specs:
        draw.text((130, spy), label, font=get_font(11, 'bold'), fill=BRAND_LIGHT)
        draw.text((130, spy + 22), val, font=get_font(15, 'bold'), fill=(255, 255, 255))
        spy += 60

    # Right Hero Mockup Frame
    mock_p = os.path.join(ASSETS_DIR, "screen_01_landing.png")
    if os.path.exists(mock_p):
        m_img = Image.open(mock_p).convert('RGBA')
        mw = 1040
        mh = int(m_img.height * (mw / m_img.width))
        m_res = m_img.resize((mw, mh), Image.Resampling.LANCZOS)
        fx = 780
        fy = 160
        draw.rounded_rectangle([fx - 10, fy - 10, fx + mw + 10, fy + 720], radius=16, fill=(10, 15, 25), outline=BORDER_DARK, width=2)
        crop_view = m_res.crop((0, 0, mw, min(700, mh)))
        img.paste(crop_view, (fx, fy), crop_view)

    draw_slide_footer(draw, 1, 12, dark_mode=True)
    img.save(os.path.join(OUT_DIR, "slide_01.png"), quality=95)
    print("Generated slide_01.png")

def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 2, "PROBLEMS & RESEARCH 01", "4 Core Market Problems", "토지개발 시장의 4대 핵심 문제점 분석", "정보의 파편화 및 비표준화, 비전문가의 접근 장벽, 디지털화의 부재, 사용자 경험의 단절")
    
    # Pure Figma Card Graphic (ref_01_problems.png)
    rx = 80
    rw = W - 160
    ry = 260
    rh = 690
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    p_img_path = os.path.join(ASSETS_DIR, "ref_01_problems.png")
    if os.path.exists(p_img_path):
        p_img = Image.open(p_img_path).convert('RGBA')
        scale = min((rw - 60) / p_img.width, (rh - 60) / p_img.height)
        nw = int(p_img.width * scale)
        nh = int(p_img.height * scale)
        p_res = p_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(p_res, (rx + (rw - nw) // 2, ry + (rh - nh) // 2), p_res)

    draw_slide_footer(draw, 2, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_02.png"), quality=95)
    print("Generated slide_02.png")

def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 3, "PROBLEMS & RESEARCH 02", "Empirical Research & Data", "정량적 사용자 리서치 및 데이터 통계 검증", "사용자가 가장 어려워하는 과정(수익성 계산 4.5점) 및 정보 파편화 통합 필요성 데이터 분석")

    rx = 80
    rw = W - 160
    ry = 260
    rh = 690
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    r_img_path = os.path.join(ASSETS_DIR, "ref_02_research_charts.png")
    if os.path.exists(r_img_path):
        r_img = Image.open(r_img_path).convert('RGBA')
        scale = min((rw - 60) / r_img.width, (rh - 60) / r_img.height)
        nw = int(r_img.width * scale)
        nh = int(r_img.height * scale)
        r_res = r_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(r_res, (rx + (rw - nw) // 2, ry + (rh - nh) // 2), r_res)

    draw_slide_footer(draw, 3, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_03.png"), quality=95)
    print("Generated slide_03.png")

def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 4, "USER PERSONAS", "Target Audience Personas", "토지개발 플랫폼 2대 타깃 페르소나 정의", "귀촌 준비 직장인 김도현(35)과 농장 배치를 직접 기획하는 청년 창업가 박예진(28)의 Pain Points & Needs")

    rx = 80
    rw = W - 160
    ry = 260
    rh = 690
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    pers_path = os.path.join(ASSETS_DIR, "part_user_personas.png")
    if os.path.exists(pers_path):
        pers_img = Image.open(pers_path).convert('RGBA')
        scale = min((rw - 80) / pers_img.width, (rh - 80) / pers_img.height)
        nw = int(pers_img.width * scale)
        nh = int(pers_img.height * scale)
        p_res = pers_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(p_res, (rx + (rw - nw) // 2, ry + (rh - nh) // 2), p_res)

    draw_slide_footer(draw, 4, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_04.png"), quality=95)
    print("Generated slide_04.png")

if __name__ == '__main__':
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
