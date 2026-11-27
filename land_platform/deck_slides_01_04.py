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
        # Desktop frame wrapper
        fx = 780
        fy = 160
        draw.rounded_rectangle([fx - 10, fy - 10, fx + mw + 10, fy + 720], radius=16, fill=(10, 15, 25), outline=BORDER_DARK, width=2)
        # paste cropped view
        crop_view = m_res.crop((0, 0, mw, min(700, mh)))
        img.paste(crop_view, (fx, fy), crop_view)

    draw_slide_footer(draw, 1, 12, dark_mode=True)
    img.save(os.path.join(OUT_DIR, "slide_01.png"), quality=95)
    print("Generated slide_01.png")

def make_slide_02():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 2, "PROJECT OVERVIEW", "Background & Market Problem", "토지개발 시장의 고질적 비효율과 정보 비대칭 해결", "공간 빅데이터와 인허가 규제 시뮬레이션을 통한 디지털 전환(DX) 가치 창출")
    
    # 3 Problem Cards
    problems = [
        ("01", "정보의 극심한 파편화", "토지이용계획원, 지적도, 도시계획조례 등 인허가 확인을 위해 5개 이상의 공공기관 사이트를 개별 방문해야 하는 비효율 발생"),
        ("02", "비전문가의 타당성 검토 한계", "토지 소유주가 자신의 토지에 어떤 시설(스마트팜, 창고, 주거)이 최적인지 경제성 및 인허가 타당성을 판단할 객관적 도구 부재"),
        ("03", "이해관계자 간 신뢰 단절", "토지주-개발사-투자사 간 검증되지 않은 기획서와 정성적 추정에 의존하여 사업 지연 및 자금 조달 리스크 급증")
    ]
    cx = 80
    for num, title, desc in problems:
        draw.rounded_rectangle([cx, 260, cx + 380, 520], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw.text((cx + 25, 290), num, font=get_font(28, 'black'), fill=BRAND_GREEN)
        draw.text((cx + 25, 345), title, font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((cx + 25, 385), desc, font=get_font(13.5, 'regular'), fill=TEXT_LIGHT_SUB)
        cx += 405

    # Bottom Solution Architecture
    draw.rounded_rectangle([80, 550, W - 80, 960], radius=16, fill=(240, 253, 244), outline=BRAND_GREEN, width=1)
    draw_pill_badge(draw, 110, 585, "CORE SOLUTION ARCHITECTURE", get_font(11, 'bold'), theme='green')
    draw.text((110, 620), "3단계 원스톱 토지개발 타당성 분석 플랫폼", font=get_font(22, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    steps = [
        ("STEP 1. 공간 GIS 토지 분석", "지번 입력 즉시 용도지역, 공시지가, 접도조건, 고도/경사도, 생태자연도 등 법적 규제 3초 내 자동 진단"),
        ("STEP 2. 시설 배치 & 단지 설계", "선택 토지 내 최적 스마트팜, 태양광, 복합시설 자동 배치 및 재배 작물 연동 생산량 시뮬레이션"),
        ("STEP 3. 경제성 타당성 보고서", "총 투자비용, 건축공사비, 연간 예상 매출액, 회수기간, IRR을 반영한 전문가급 표준 보고서 자동 생성")
    ]
    sx = 110
    for s_title, s_desc in steps:
        draw.rounded_rectangle([sx, 670, sx + 540, 920], radius=12, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw.text((sx + 20, 700), s_title, font=get_font(16, 'bold'), fill=BRAND_GREEN)
        draw.text((sx + 20, 740), s_desc, font=get_font(13, 'regular'), fill=TEXT_LIGHT_SUB)
        sx += 570

    draw_slide_footer(draw, 2, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_02.png"), quality=95)
    print("Generated slide_02.png")

def make_slide_03():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 3, "USER PERSONA & ECOSYSTEM", "Stakeholder Ecosystem", "토지개발 생태계 3대 핵심 이해관계자 분석", "토지 소유주, 전문 개발사, 투자 기관의 요구사항을 통합하여 신뢰 기반의 협업 허브 구축")

    personas = [
        ("토지 소유주 (Land Owner)", "보유 토지의 개발 가능성과 최적 활용 방안을 알고 싶으나 법적 규제 분석에 어려움을 겪는 5070 자산가", ["간편한 지번 검색 및 원터치 규제 진단", "복잡한 법률 용어 대신 시각화된 시설 추천", "예상 수익률과 초기 투자비용 직관적 확인"]),
        ("전문 개발사 (Developer)", "사업성 있는 토지를 발굴하고 빠른 기획 설계와 인허가 검토를 완료해야 하는 토지 개발 및 시공 파트너", ["GIS 기반 다필지 통합 필터링 및 조건 검색", "단지 배치 및 시설 규격 커스텀 시뮬레이션", "금융 심사용 표준 사업계획서 PDF 추출"]),
        ("투자 기관 (Investor / Fund)", "토지개발 프로젝트의 리스크를 검증하고 자금 투입 타당성을 객관적으로 평가해야 하는 금융·투자사", ["공공 데이터 기반 법적 인허가 클리어런스", "비용·수익 구조의 정량적 IRR/NPV 데이터", "리스크 평가 항목 및 회수 기간 투명성 확보"])
    ]
    px = 80
    for title, role_desc, reqs in personas:
        draw.rounded_rectangle([px, 250, px + 560, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, px + 25, 285, "KEY USER SEGMENT", get_font(10.5, 'bold'), theme='green')
        draw.text((px + 25, 325), title, font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((px + 25, 365), role_desc, font=get_font(13, 'regular'), fill=TEXT_LIGHT_SUB)
        draw.line([(px + 25, 430), (px + 535, 430)], fill=BORDER_LIGHT, width=1)
        
        draw.text((px + 25, 455), "CORE REQUIREMENTS & VALUE", font=get_font(12, 'bold'), fill=BRAND_GREEN)
        ry = 495
        for req in reqs:
            draw.text((px + 25, ry), "•", font=get_font(14, 'bold'), fill=BRAND_GREEN)
            draw.text((px + 45, ry), req, font=get_font(13.5, 'medium'), fill=TEXT_LIGHT_MAIN)
            ry += 48
        px += 590

    draw_slide_footer(draw, 3, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_03.png"), quality=95)
    print("Generated slide_03.png")

def make_slide_04():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 4, "INFORMATION ARCHITECTURE", "Platform Sitemap & User Journey", "GIS 공간 데이터 기반 4대 정보 설계 계층 구조", "대상지 탐색부터 시설 배치, 사업성 시뮬레이션, 보고서 연계로 이어지는 무결점 사용자 여정")

    ia_groups = [
        ("01. GIS 토지 탐색 엔진", ["지번 / 주소 통합 검색", "지적도 / 위성지도 레이어", "토지이용계획 3초 진단", "용도지역 및 행위제한"]),
        ("02. 시설 배치 시뮬레이터", ["스마트팜 / 온실 모듈", "단지 구획 및 도로 설계", "재배 작물 DB 매칭", "면적별 설비 자동 연동"]),
        ("03. 타당성 & 경제성 분석", ["총사업비 산출 내역서", "연간 예상 매출 및 비용", "회수기간 / IRR 추정", "수익률 민감도 분석"]),
        ("04. 보고서 & 전문가 매칭", ["공식 분석 보고서 생성", "PDF 다운로드 및 공유", "시공사 / 개발사 견적", "투자 유치 컨설팅 연계"])
    ]
    ix = 80
    for group_title, items in ia_groups:
        draw.rounded_rectangle([ix, 260, ix + 415, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([ix, 260, ix + 415, 330], radius=16, fill=(240, 253, 244), outline=BRAND_GREEN, width=1)
        draw.text((ix + 25, 295), group_title, font=get_font(17, 'bold'), fill=BRAND_GREEN, anchor='lm')
        
        iy = 370
        for item in items:
            draw.rounded_rectangle([ix + 20, iy, ix + 395, iy + 105], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
            draw.text((ix + 40, iy + 35), item, font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN)
            draw.text((ix + 40, iy + 65), "데이터 무결성 검증 및 API 연동", font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            iy += 135
        ix += 440

    draw_slide_footer(draw, 4, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_04.png"), quality=95)
    print("Generated slide_04.png")

if __name__ == '__main__':
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
