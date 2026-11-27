import os
from PIL import Image, ImageDraw
from deck_common import *

def make_slide_09():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 9, "CORE FEATURE 03", "Crop & Production Simulation", "STEP 3. 재배 작물 DB 매칭 및 생산성 시뮬레이션", "딸기, 토마토, 파프리카 등 고부가가치 작물별 생육 환경, 단가, 연간 예상 수확량 자동 계산")

    # Left: Feature Details
    lx = 80
    lw = 600
    draw.rounded_rectangle([lx, 260, lx + lw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, lx + 25, 295, "CROP PRODUCTIVITY ENGINE", get_font(10.5, 'bold'), theme='green')
    draw.text((lx + 25, 335), "데이터 기반 수확량 및 매출 예측", font=get_font(22, 'bold'), fill=TEXT_LIGHT_MAIN)

    crop_cards = [
        ("농촌진흥청 공공 DB 기반 작물 사전", "작물별 적정 온도, 습도, 일조량, 배지 종류 및 계절별 수확 주기 알고리즘 탑재"),
        ("지역별 도매시장 실시간 경락가 연동", "가락시장 등 주요 공영도매시장의 3개년 평균 거래 단가를 매칭하여 신뢰할 수 있는 예상 매출액 산출"),
        ("작물별 맞춤 설비 옵션 자동 제안", "양액기, 환경제어기(복합환경), 온수보일러, LED 보광등 등 필수 설비 자동 리스트업 및 견적 산출")
    ]
    fy = 400
    for title, desc in crop_cards:
        draw.rounded_rectangle([lx + 20, fy, lx + lw - 20, fy + 150], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, fy + 35), title, font=get_font(17, 'bold'), fill=BRAND_GREEN)
        draw.text((lx + 40, fy + 75), desc, font=get_font(13.5, 'regular'), fill=TEXT_LIGHT_SUB)
        fy += 175

    # Right: High Resolution Screen View
    rx = 710
    rw = W - 80 - rx
    draw.rounded_rectangle([rx, 260, rx + rw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    s_p = os.path.join(ASSETS_DIR, "screen_04_crop_selection.png")
    if os.path.exists(s_p):
        s_img = Image.open(s_p).convert('RGBA')
        scale = min((rw - 30) / s_img.width, (950 - 260 - 30) / s_img.height)
        sw = int(s_img.width * scale)
        sh = int(s_img.height * scale)
        s_res = s_img.resize((sw, sh), Image.Resampling.LANCZOS)
        img.paste(s_res, (rx + (rw - sw) // 2, 260 + (950 - 260 - sh) // 2), s_res)

    draw_slide_footer(draw, 9, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_09.png"), quality=95)
    print("Generated slide_09.png")

def make_slide_10():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 10, "CORE FEATURE 04", "Economic Feasibility & ROI", "STEP 4. 경제성 타당성 분석 및 금융 심사 모델", "총사업비, 시설조성비, 설계감리비, 운영비(OPEX) 대비 회수기간 및 IRR을 도출하는 금융 모델링")

    # Left: Feature Details
    lx = 80
    lw = 600
    draw.rounded_rectangle([lx, 260, lx + lw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, lx + 25, 295, "FINANCIAL VALUATION MODEL", get_font(10.5, 'bold'), theme='green')
    draw.text((lx + 25, 335), "엔터프라이즈급 정량 경제성 분석", font=get_font(22, 'bold'), fill=TEXT_LIGHT_MAIN)

    fin_cards = [
        ("세부 CAPEX / OPEX 산출 명세", "토지 매입비, 토목/건축공사비, ICT 스마트팜 장비비, 연간 인건비 및 난방비 정밀 분해"),
        ("10개년 현금흐름(Cash Flow) 시뮬레이션", "감가상각, 법인세, 금융 이자율을 반영한 연차별 순수익 추정과 손익분기점(BEP) 제시"),
        ("투자 유치용 IRR / NPV 정량 지표", "투자 기관 및 정책자금 심사에 즉각 제출 가능한 내부수익률(IRR)과 순현재가치(NPV) 자동 계산")
    ]
    fy = 400
    for title, desc in fin_cards:
        draw.rounded_rectangle([lx + 20, fy, lx + lw - 20, fy + 150], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, fy + 35), title, font=get_font(17, 'bold'), fill=BRAND_GREEN)
        draw.text((lx + 40, fy + 75), desc, font=get_font(13.5, 'regular'), fill=TEXT_LIGHT_SUB)
        fy += 175

    # Right: High Resolution Screen View
    rx = 710
    rw = W - 80 - rx
    draw.rounded_rectangle([rx, 260, rx + rw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    s_p = os.path.join(ASSETS_DIR, "screen_06_economic_analysis.png")
    if os.path.exists(s_p):
        s_img = Image.open(s_p).convert('RGBA')
        scale = min((rw - 30) / s_img.width, (950 - 260 - 30) / s_img.height)
        sw = int(s_img.width * scale)
        sh = int(s_img.height * scale)
        s_res = s_img.resize((sw, sh), Image.Resampling.LANCZOS)
        img.paste(s_res, (rx + (rw - sw) // 2, 260 + (950 - 260 - sh) // 2), s_res)

    draw_slide_footer(draw, 10, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_10.png"), quality=95)
    print("Generated slide_10.png")

def make_slide_11():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 11, "REPORT & EXPERT MATCHING", "Valuation Report & Ecosystem", "토지개발 타당성 종합 보고서 및 컨설팅 매칭", "토지주와 투자사, 시공사를 원스톱으로 연결하는 표준 리포트 생성 및 B2B 생태계 허브")

    # Left: Feature Details
    lx = 80
    lw = 600
    draw.rounded_rectangle([lx, 260, lx + lw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, lx + 25, 295, "COMPREHENSIVE VALUATION REPORT", get_font(10.5, 'bold'), theme='green')
    draw.text((lx + 25, 335), "표준 타당성 보고서 & 컨설팅", font=get_font(22, 'bold'), fill=TEXT_LIGHT_MAIN)

    rep_cards = [
        ("원클릭 고해상도 PDF 보고서 출력", "토지 개요, 지적도, 시설 배치도, 10개년 재무 예측표를 집약한 20페이지 분량의 심사 보고서 자동 인쇄"),
        ("검증된 시공사 및 스마트팜 파트너 연계", "국내 50여 개 우수 시공사 풀을 기반으로 분석 결과에 따른 최적 견적 비교 입찰 시스템 지원"),
        ("금융 기관 및 정책 자금 컨설팅 연결", "농림축산식품부 스마트팜 종합자금 등 연계 가능한 저리 정책금융 가이드 및 전문 컨설팅 상담 신청")
    ]
    fy = 400
    for title, desc in rep_cards:
        draw.rounded_rectangle([lx + 20, fy, lx + lw - 20, fy + 150], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, fy + 35), title, font=get_font(17, 'bold'), fill=BRAND_GREEN)
        draw.text((lx + 40, fy + 75), desc, font=get_font(13.5, 'regular'), fill=TEXT_LIGHT_SUB)
        fy += 175

    # Right: High Resolution Screen View
    rx = 710
    rw = W - 80 - rx
    draw.rounded_rectangle([rx, 260, rx + rw, 950], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    s_p = os.path.join(ASSETS_DIR, "screen_07_report_summary.png")
    if os.path.exists(s_p):
        s_img = Image.open(s_p).convert('RGBA')
        scale = min((rw - 30) / s_img.width, (950 - 260 - 30) / s_img.height)
        sw = int(s_img.width * scale)
        sh = int(s_img.height * scale)
        s_res = s_img.resize((sw, sh), Image.Resampling.LANCZOS)
        img.paste(s_res, (rx + (rw - sw) // 2, 260 + (950 - 260 - sh) // 2), s_res)

    draw_slide_footer(draw, 11, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_11.png"), quality=95)
    print("Generated slide_11.png")

def make_slide_12():
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 12, "OUTCOMES & RETROSPECTIVE", "STAR Retrospective & Business Impact", "비즈니스 성과 지표 및 STAR 기법 회고", "토지개발 인허가 분석 기간 90% 단축과 데이터 기반 의사결정 체계 확립", dark_mode=True)

    # 4 Quantitative Impact Cards
    metrics = [
        ("90% 단축", "인허가 분석 소요 시간", "기존 2주(14일) 소요되던 규제 검토 및 현장 조사를 3초 자동 분석으로 획기적 단축"),
        ("100% 신뢰", "공공 데이터 정합성", "토지이용계획원, 지적도, 생태자연도 등 12대 공공 API 실시간 검증을 통한 무결점 달성"),
        ("350% 증가", "사업 타당성 검토 건수", "전문 지식이 없는 토지 소유주도 직관적으로 접근하여 월평균 시뮬레이션 의뢰 급증"),
        ("8주 완수", "기획/설계/디자인 완료", "B2B UX/UI 아키텍처 및 60여 개 핵심 컴포넌트 라이브러리를 단독으로 설계 완수")
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
        ("Result & Learning (성과 및 회고)", "기존 2주 이상 소요되던 토지 타당성 분석 기간을 3초로 90% 이상 단축했으며, 토지주-개발사-투자사 간 신뢰 기반의 협업 허브를 구축했습니다. 방대한 전문 도메인 지식을 프로덕트 디자이너의 직관적 UX 아키텍처로 체계화함으로써 비즈니스 가치를 극대화한 프로젝트였습니다.")
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
