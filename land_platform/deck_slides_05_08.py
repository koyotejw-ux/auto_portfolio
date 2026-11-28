import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 05: INFORMATION ARCHITECTURE (Native Vector Tree)
# -------------------------------------------------------------
def make_slide_05():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 5, 
        "INFORMATION ARCHITECTURE", 
        "Information Architecture | ", 
        "토지개발 플랫폼 인포메이션 아키텍처 (IA) 및 5대 핵심 모듈", 
        "홈 중심의 로그인/회원가입, 시뮬레이터(시작/통계), 사용자 통계, 마이페이지, 관리자(위젯/데이터) 계층 설계", 
        right_badge=("PLATFORM IA TREE", "green")
    )
    
    lw = 480
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="5-DOMAIN IA PRINCIPLES", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "5대 핵심 도메인 아키텍처", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    principles = [
        ("01. 회원 및 인증 체계", "일반 토지주, 소농, 전문 개발사, 투자사 유형별 맞춤 권한 부여 및 비밀번호 찾기, 서비스 정책 연결"),
        ("02. 코어 시뮬레이터 엔진", "시뮬레이션 시작(대상지-토지분석-시설배치-설계-매출)과 시뮬레이션 이력 및 통계 대시보드"),
        ("03. 사용자 통계 센터", "지역별 인기 토지 개발 유형, 최근 시뮬레이션 추이 및 평균 소요 비용/수익률 실시간 집계"),
        ("04. 마이페이지 & 결제 관리", "회원 프로필 설정, 저장된 시뮬레이션 프로젝트 관리 및 심층 타당성 보고서 결제/영수증 관리"),
        ("05. 엔터프라이즈 관리자 콘솔", "위젯 설정, 공공 API 데이터 싱크 관리, 토지 규제 조례 DB 업데이트 및 회원 관리")
    ]
    py = ly + 115
    for title, desc in principles:
        draw.rounded_rectangle([125, py, 100 + lw - 25, py + 105], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, py + 25), title, font=get_font(15, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12, 'regular'), lw - 70, draw)
        dy = py + 52
        for l in lines:
            draw.text((145, dy), l, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        py += 120

    rx = 605
    rw = 1215
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ly + 35, text="DIRECT VECTOR HIERARCHY TREE", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 265, ly + 35), "피그마 원본 정보 구조도 (Home 중심 4대 도메인 및 16대 서브 노드 완전 구현)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    root_x, root_y, root_w, root_h = rx + rw//2 - 90, ly + 80, 180, 52
    draw.rounded_rectangle([root_x, root_y, root_x + root_w, root_y + root_h], radius=26, fill=BRAND_GREEN)
    draw.text((root_x + root_w//2, root_y + root_h//2), "Home (홈 메인)", font=get_font(16, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    categories = [
        ("01. 회원가입/로그인", ["로그인", "회원가입", "비밀번호 찾기", "서비스 이용약관"]),
        ("02. 시뮬레이터 (Core)", ["시뮬레이션 시작", "시뮬레이션 통계", "진행 이력 관리", "보고서 뷰어"]),
        ("03. 사용자 통계 & 마이", ["지역별 개발 통계", "비용/수익률 집계", "내 프로젝트 보관", "결제 및 영수증"]),
        ("04. 관리자 콘솔", ["메인 위젯 관리", "공공 API 연동", "토지 규제 DB", "회원 권한 관리"])
    ]
    
    cat_w = 265
    cat_gap = 25
    cat_start_x = rx + (rw - (4 * cat_w + 3 * cat_gap)) // 2
    cat_y = ly + 200
    
    stem_y = ly + 160
    draw.line([(root_x + root_w//2, root_y + root_h), (root_x + root_w//2, stem_y)], fill=(148, 163, 184), width=2)
    draw.line([(cat_start_x + cat_w//2, stem_y), (cat_start_x + 3 * (cat_w + cat_gap) + cat_w//2, stem_y)], fill=(148, 163, 184), width=2)
    
    for idx, (cat_name, sub_items) in enumerate(categories):
        cx = cat_start_x + idx * (cat_w + cat_gap)
        draw.line([(cx + cat_w//2, stem_y), (cx + cat_w//2, cat_y)], fill=(148, 163, 184), width=2)
        
        cat_col = BRAND_DARK if idx==1 else (BRAND_TEAL if idx==2 else (51, 65, 85))
        draw.rounded_rectangle([cx, cat_y, cx + cat_w, cat_y + 48], radius=10, fill=cat_col)
        draw.text((cx + cat_w//2, cat_y + 24), cat_name, font=get_font(13.5, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        sub_stem_x = cx + cat_w//2
        sub_y_start = cat_y + 48
        draw.line([(sub_stem_x, sub_y_start), (sub_stem_x, sub_y_start + 420)], fill=(203, 213, 225), width=2)
        
        for s_idx, s_text in enumerate(sub_items):
            s_box_y = cat_y + 75 + s_idx * 95
            s_box_w = cat_w - 20
            s_box_h = 68
            s_box_x = cx + 10
            
            draw.line([(sub_stem_x, s_box_y + s_box_h//2), (s_box_x, s_box_y + s_box_h//2)], fill=(148, 163, 184), width=2)
            
            box_fill = (236, 253, 245) if idx==1 else (248, 250, 252)
            box_border = BRAND_GREEN if idx==1 else BORDER_LIGHT
            draw.rounded_rectangle([s_box_x, s_box_y, s_box_x + s_box_w, s_box_y + s_box_h], radius=8, fill=box_fill, outline=box_border, width=2 if idx==1 else 1)
            
            draw.rounded_rectangle([s_box_x + 12, s_box_y + 12, s_box_x + 36, s_box_y + 32], radius=4, fill=BRAND_GREEN if idx==1 else (100, 116, 139))
            draw.text((s_box_x + 24, s_box_y + 22), f"{s_idx+1}", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
            draw.text((s_box_x + 44, s_box_y + 22), s_text, font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
            
            sub_descs = {
                "로그인": "소셜/이메일 간편인증",
                "회원가입": "토지주/전문사 유형선택",
                "비밀번호 찾기": "SMS/이메일 본인인증",
                "서비스 이용약관": "개인정보/위치기반 동의",
                "시뮬레이션 시작": "지번검색 → 분석 → 배치",
                "시뮬레이션 통계": "프로젝트별 수치 대시보드",
                "진행 이력 관리": "임시저장 및 버전 비교",
                "보고서 뷰어": "웹 인터랙티브/PDF 출력",
                "지역별 개발 통계": "시군구별 개발 트렌드",
                "비용/수익률 집계": "평균 CAPEX/IRR 지표",
                "내 프로젝트 보관": "즐겨찾기 및 폴더링",
                "결제 및 영수증": "정기구독 / 건별 리포트",
                "메인 위젯 관리": "배너/추천토지 컴포넌트",
                "공공 API 연동": "토지이음/지적도 상태",
                "토지 규제 DB": "지자체별 조례 룰셋",
                "회원 권한 관리": "승인/차단/엔터프라이즈"
            }
            draw.text((s_box_x + 14, s_box_y + 48), sub_descs.get(s_text, ""), font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)

    draw_slide_footer(draw, 5, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_05.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 06: USER FLOW & DECISION LOGIC (Flawless Native Vector Flow Chart)
# -------------------------------------------------------------
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 6, 
        "USER FLOW & DECISION LOGIC", 
        "User Flow & Logic | ", 
        "원스톱 토지개발 시뮬레이션 유저 플로우 및 의사결정 분기 로직", 
        "메인(홈) → 지번 검색 → 12대 공공 API 분석 → 개발 적합 판별 분기 → 시설 배치 → 재무 평가 → 리포트 생성", 
        right_badge=("SERVICE FLOW CHART", "green")
    )
    
    card_x, card_y, card_w, card_h = 100, 210, 1720, 750
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=card_x + 30, cy=card_y + 32, text="END-TO-END DECISION TREE & FLOW CHART", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((card_x + 30, card_y + 60), "토지개발 플랫폼 핵심 사용자 흐름 및 시스템 조건 분기 로직 (완전판)", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    n1_x, n1_y, n1_w, n1_h = card_x + 30, card_y + 110, 140, 60
    draw.rounded_rectangle([n1_x, n1_y, n1_x + n1_w, n1_y + n1_h], radius=30, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((n1_x + n1_w//2, n1_y + n1_h//2), "메인(홈)", font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw_arrow(draw, (n1_x + n1_w, n1_y + n1_h//2), (n1_x + n1_w + 35, n1_y + n1_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    
    n2_x, n2_y, n2_w, n2_h = n1_x + n1_w + 35, card_y + 100, 170, 80
    draw.rounded_rectangle([n2_x, n2_y, n2_x + n2_w, n2_y + n2_h], radius=12, fill=(255, 255, 255), outline=BRAND_GREEN, width=2)
    draw_pill_badge(draw, cx=n2_x + n2_w//2, cy=n2_y + 16, text="INPUT ACTION", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    draw.text((n2_x + n2_w//2, n2_y + 42), "대상지 지번 검색", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((n2_x + n2_w//2, n2_y + 62), "또는 지도 클릭 선택", font=get_font(11.5, 'medium'), fill=BRAND_DARK, anchor='mm')
    
    draw_arrow(draw, (n2_x + n2_w, n2_y + n2_h//2), (n2_x + n2_w + 35, n2_y + n2_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    
    d1_x, d1_y, d1_w, d1_h = n2_x + n2_w + 35, card_y + 95, 175, 90
    draw.rounded_rectangle([d1_x, d1_y, d1_x + d1_w, d1_y + d1_h], radius=14, fill=(240, 246, 255), outline=(59, 130, 246), width=2)
    draw_pill_badge(draw, cx=d1_x + d1_w//2, cy=d1_y + 18, text="CHECK 01 · GIS API", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=18)
    draw.text((d1_x + d1_w//2, d1_y + 42), "공공 데이터", font=get_font(13, 'bold'), fill=(29, 78, 216), anchor='mm')
    draw.text((d1_x + d1_w//2, d1_y + 64), "파싱 성공?", font=get_font(13, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    draw.line([(d1_x + d1_w//2, d1_y + d1_h), (d1_x + d1_w//2, card_y + 245)], fill=(225, 29, 72), width=2)
    draw_arrow(draw, (d1_x + d1_w//2, card_y + 245), (d1_x + d1_w//2, card_y + 260), col=(225, 29, 72), width=2, arrow_size=6)
    draw_pill_badge(draw, cx=d1_x + d1_w//2 + 18, cy=d1_y + d1_h + 15, text="N", font=get_font(9.5, 'bold'), theme='red', pad_x=6, height=16)
    
    fb1_x, fb1_y, fb1_w, fb1_h = d1_x - 15, card_y + 260, 205, 60
    draw.rounded_rectangle([fb1_x, fb1_y, fb1_x + fb1_w, fb1_y + fb1_h], radius=12, fill=(255, 241, 242), outline=(254, 205, 211), width=2)
    draw.text((fb1_x + fb1_w//2, fb1_y + 20), "지적도 캐시 데이터 전환", font=get_font(12, 'bold'), fill=(225, 29, 72), anchor='mm')
    draw.text((fb1_x + fb1_w//2, fb1_y + 40), "수동 지번/면적 입력 팝업", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    draw_arrow(draw, (d1_x + d1_w, d1_y + d1_h//2), (d1_x + d1_w + 40, d1_y + d1_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    draw.text((d1_x + d1_w + 16, d1_y + d1_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    d2_x, d2_y, d2_w, d2_h = d1_x + d1_w + 40, card_y + 95, 180, 90
    draw.rounded_rectangle([d2_x, d2_y, d2_x + d2_w, d2_y + d2_h], radius=14, fill=(236, 253, 245), outline=BRAND_GREEN, width=2)
    draw_pill_badge(draw, cx=d2_x + d2_w//2, cy=d2_y + 18, text="CHECK 02 · 규제 적합", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    draw.text((d2_x + d2_w//2, d2_y + 42), "개발 적합 토지?", font=get_font(13.5, 'bold'), fill=BRAND_DARK, anchor='mm')
    draw.text((d2_x + d2_w//2, d2_y + 64), "(용도지역/접도/경사)", font=get_font(11, 'medium'), fill=BRAND_GREEN, anchor='mm')
    
    draw.line([(d2_x + d2_w//2, d2_y + d2_h), (d2_x + d2_w//2, card_y + 245)], fill=(225, 29, 72), width=2)
    draw_arrow(draw, (d2_x + d2_w//2, card_y + 245), (d2_x + d2_w//2, card_y + 260), col=(225, 29, 72), width=2, arrow_size=6)
    draw_pill_badge(draw, cx=d2_x + d2_w//2 + 18, cy=d2_y + d2_h + 15, text="N", font=get_font(9.5, 'bold'), theme='red', pad_x=6, height=16)
    
    fb2_x, fb2_y, fb2_w, fb2_h = d2_x - 15, card_y + 260, 210, 60
    draw.rounded_rectangle([fb2_x, fb2_y, fb2_x + fb2_w, fb2_y + fb2_h], radius=12, fill=(255, 241, 242), outline=(254, 205, 211), width=2)
    draw.text((fb2_x + fb2_w//2, fb2_y + 20), "인허가 저촉 사유 안내", font=get_font(12, 'bold'), fill=(225, 29, 72), anchor='mm')
    draw.text((fb2_x + fb2_w//2, fb2_y + 40), "대체 작물/완충 솔루션 제시", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    draw_arrow(draw, (d2_x + d2_w, d2_y + d2_h//2), (d2_x + d2_w + 40, d2_y + d2_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    draw.text((d2_x + d2_w + 16, d2_y + d2_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    n4_x, n4_y, n4_w, n4_h = d2_x + d2_w + 40, card_y + 100, 190, 80
    draw.rounded_rectangle([n4_x, n4_y, n4_x + n4_w, n4_y + n4_h], radius=12, fill=(255, 255, 255), outline=BRAND_TEAL, width=2)
    draw_pill_badge(draw, cx=n4_x + n4_w//2, cy=n4_y + 16, text="SIMULATOR", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=18)
    draw.text((n4_x + n4_w//2, n4_y + 42), "스마트팜 단지 배치", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((n4_x + n4_w//2, n4_y + 62), "온실/부대시설/작물 연동", font=get_font(11, 'medium'), fill=BRAND_TEAL, anchor='mm')
    
    draw_arrow(draw, (n4_x + n4_w, n4_y + n4_h//2), (n4_x + n4_w + 40, n4_y + n4_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    
    d3_x, d3_y, d3_w, d3_h = n4_x + n4_w + 40, card_y + 95, 180, 90
    draw.rounded_rectangle([d3_x, d3_y, d3_x + d3_w, d3_y + d3_h], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=2)
    draw_pill_badge(draw, cx=d3_x + d3_w//2, cy=d3_y + 18, text="CHECK 03 · 리포트", font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
    draw.text((d3_x + d3_w//2, d3_y + 42), "상세 금융 리포트", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((d3_x + d3_w//2, d3_y + 64), "발급 요청?", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw.line([(d3_x + d3_w//2, d3_y + d3_h), (d3_x + d3_w//2, card_y + 245)], fill=(100, 116, 139), width=2)
    draw_arrow(draw, (d3_x + d3_w//2, card_y + 245), (d3_x + d3_w//2, card_y + 260), col=(100, 116, 139), width=2, arrow_size=6)
    draw.text((d3_x + d3_w//2 + 10, d3_y + d3_h + 12), "N", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    out1_x, out1_y, out1_w, out1_h = d3_x - 15, card_y + 260, 210, 60
    draw.rounded_rectangle([out1_x, out1_y, out1_x + out1_w, out1_y + out1_h], radius=28, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((out1_x + out1_w//2, out1_y + out1_h//2), "기본 요약 웹 대시보드 열람", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw_arrow(draw, (d3_x + d3_w, d3_y + d3_h//2), (d3_x + d3_w + 40, d3_y + d3_h//2), col=BRAND_GREEN, width=2, arrow_size=7)
    draw.text((d3_x + d3_w + 16, d3_y + d3_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=BRAND_GREEN)
    
    goal_x, goal_y, goal_w, goal_h = d3_x + d3_w + 40, card_y + 100, 240, 80
    draw.rounded_rectangle([goal_x, goal_y, goal_x + goal_w, goal_y + goal_h], radius=16, fill=(236, 253, 245), outline=BRAND_GREEN, width=2)
    draw_pill_badge(draw, cx=goal_x + goal_w//2, cy=goal_y + 18, text="FINAL GOAL", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    draw.text((goal_x + goal_w//2, goal_y + 44), "종합 타당성 리포트 발급", font=get_font(14, 'bold'), fill=BRAND_DARK, anchor='mm')
    draw.text((goal_x + goal_w//2, goal_y + 64), "20p PDF 및 금융기관 제출용", font=get_font(11.5, 'medium'), fill=BRAND_GREEN, anchor='mm')

    bot_y = card_y + 360
    draw.line([(card_x + 30, bot_y - 20), (card_x + card_w - 30, bot_y - 20)], fill=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=card_x + 30, cy=bot_y + 5, text="CORE DECISION NODES SPECIFICATION", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((card_x + 320, bot_y + 5), "개발/시스템 연동을 위한 4대 의사결정 노드 상세 정의 및 예외 처리 정책", font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    nodes_detail = [
        {
            "num": "1",
            "title": "공공 GIS API 실시간 연동 및 Fallback",
            "tag": "API & 캐싱",
            "desc": "토지이음, 국토교통부 지적도, 수치표고모델(DEM) 12대 공공 API를 비동기 병렬 호출합니다. 3초 이상 응답 지연 시 최근 30일 이내 동기화된 지적 캐시 데이터로 자동 전환하여 서비스 중단 방지."
        },
        {
            "num": "2",
            "title": "3초 법적 인허가 및 조례 룰셋 자동 진단",
            "tag": "규제 엔진",
            "desc": "선택 필지의 용도지역(농림/관리/도시), 건폐율/용적률, 개발행위허가 기준(경사도 15도 이하, 도로 접도 4m 이상)을 지자체 조례 엔진과 대조하여 적합(녹색)/조건부(황색)/불가(적색) 3색 뱃지로 즉시 판정."
        },
        {
            "num": "3",
            "title": "스마트팜 모듈 최적 배치 & 작물 연동",
            "tag": "공간 시뮬레이션",
            "desc": "비전문가를 위해 연동형 온실 규격을 토지 경계선 내에 자동 최적 정렬합니다. 딸기, 토마토 등 선택 작물별 표준 생산 주기와 단가 DB를 연계하여 유효 재배 면적 및 예상 생산량을 오차 5% 이내로 시뮬레이션."
        },
        {
            "num": "4",
            "title": "CAPEX/OPEX 경제성 산출 & 금융 표준 리포트",
            "tag": "금융 모델링",
            "desc": "토지 매입비, 온실 시공비, 시설비(CAPEX)와 운영비/인건비(OPEX)를 10개년 현금흐름으로 분석합니다. 순현재가치(NPV) 및 내부수익률(IRR)을 자동 도출하여 농협 등 금융기관 대출 심사용 20p 표준 PDF를 원클릭 발급."
        }
    ]
    
    card_cols = 4
    col_w = (card_w - 60 - (card_cols - 1) * 20) // card_cols
    cy_p = bot_y + 35
    for i, nd in enumerate(nodes_detail):
        cx_p = card_x + 30 + i * (col_w + 20)
        draw.rounded_rectangle([cx_p, cy_p, cx_p + col_w, cy_p + 310], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([cx_p + 16, cy_p + 16, cx_p + 42, cy_p + 42], radius=6, fill=BRAND_GREEN)
        draw.text((cx_p + 29, cy_p + 29), nd["num"], font=get_font(13, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw_pill_badge(draw, left_x=cx_p + col_w - 95, cy=cy_p + 29, text=nd["tag"], font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=20)
        draw.text((cx_p + 16, cy_p + 58), nd["title"], font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.line([(cx_p + 16, cy_p + 82), (cx_p + col_w - 16, cy_p + 82)], fill=BORDER_LIGHT, width=1)
        
        lines = wrap_text(nd["desc"], get_font(11.5, 'regular'), col_w - 32, draw)
        ly_p = cy_p + 95
        for l in lines:
            draw.text((cx_p + 16, ly_p), l, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly_p += 18

    draw_slide_footer(draw, 6, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_06.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 07: PROTOTYPING SCREENS (Exact Figma 3-Phone Layer States + Flow)
# -------------------------------------------------------------
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 7, 
        "PROTOTYPING SCREENS", 
        "Prototyping Screens | ", 
        "시뮬레이션 시작 전 대상지 선택 및 3단계 지도 레이어 상태 전환 흐름", 
        "피그마 공식 UI 원본: 지적도 적용 상태 → 일반지도 적용 상태 → 스카이뷰(위성) 적용 상태 인터랙션", 
        right_badge=("OFFICIAL FIGMA PROTOTYPE", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # Left Card: Core Description & State Change Specs (w=480)
    lx = 100
    lw = 480
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="GIS LAYER SWITCHING LOGIC", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 68), "대상지 선택 & 레이어 전환", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 25, card_y + 94), "사용자 관점의 3단계 지도 모드 인터랙션", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    step_descriptions = [
        ("01. 지적도 적용 상태", "토지이용계획과 공적 지번 경계선을 파악하는 기본 뷰. 필지 번호와 경계 구분이 가장 명확하여 대상지 위치 특정에 최적화."),
        ("02. 일반지도 적용 상태", "주변 도로망, 인접 건물, 아파트 단지 등 도심 인프라와의 접근성 및 진입 도로 여건을 직관적으로 확인하는 로드맵 뷰."),
        ("03. 스카이뷰(위성) 적용 상태", "고해상도 항공 위성 사진을 통해 실제 농지 현황, 임목 상태, 고도 및 주변 녹지 완충 구역을 사실적으로 검증.")
    ]
    
    s_y = card_y + 125
    for s_title, s_desc in step_descriptions:
        draw.rounded_rectangle([lx + 25, s_y, lx + lw - 25, s_y + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, s_y + 24), s_title, font=get_font(14.5, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(s_desc, get_font(11.5, 'regular'), lw - 70, draw)
        d_y = s_y + 50
        for l in lines:
            draw.text((lx + 40, d_y), l, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            d_y += 18
        s_y += 145
        
    # Bottom Key Insight Box in Left Card
    draw.rounded_rectangle([lx + 25, card_y + 580, lx + lw - 25, card_y + 715], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((lx + 40, card_y + 602), "💡 UI/UX 인터랙션 설계 핵심", font=get_font(13, 'bold'), fill=BRAND_DARK)
    insight_desc = "우측 상단 플로팅 메뉴에서 [지적도 / 일반지도 / 스카이뷰]를 원클릭 탭 시, 맵 캔버스가 부드럽게 크로스페이드되며 하단 바텀시트의 [선택된 대상지] 정보는 그대로 유지되도록 설계하여 탐색 피로도를 0%로 줄였습니다."
    lines_ins = wrap_text(insight_desc, get_font(11, 'regular'), lw - 70, draw)
    iy = card_y + 626
    for l in lines_ins:
        draw.text((lx + 40, iy), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_MAIN)
        iy += 17

    # Right Card: The Exact 3-Phone UI Flow Asset from Figma (w=1210)
    rx = 610
    rw = 1210
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=card_y + 35, text="AUTHENTIC FIGMA PROTOTYPE UI", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 285, card_y + 35), "피그마 원본 인터랙티브 프로토타입 캔버스 (지적도 → 일반지도 → 스카이뷰)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    three_phones_asset = os.path.join(ASSETS_DIR, "figma_3phones_layer_states.png")
    if os.path.exists(three_phones_asset):
        p_img = Image.open(three_phones_asset).convert('RGBA')
        scale = min((rw - 60) / p_img.width, (card_h - 100) / p_img.height)
        nw = int(p_img.width * scale)
        nh = int(p_img.height * scale)
        p_res = p_img.resize((nw, nh), Image.Resampling.LANCZOS)
        
        # Center in right card
        px = rx + (rw - nw) // 2
        py = card_y + 75 + (card_h - 90 - nh) // 2
        img.paste(p_res, (px, py), p_res)

    draw_slide_footer(draw, 7, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_07.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 08: DESIGN SYSTEM (Figma Typography Scale + Tokens Matrix 1:1 Matching)
# -------------------------------------------------------------
def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 8, 
        "DESIGN SYSTEM & ATOMIC TOKENS", 
        "Design System | ", 
        "피그마 공식 디자인 시스템: 타이포그래피 계층 & 아토믹 토큰 매트릭스", 
        "Figma 토큰 1:1 규격화: Pretendard 12단계 텍스트 스케일, 15색 아토믹 컬러 팔레트, 32종 아이콘 그리드, Spacing/Radius/Elevation 시스템", 
        right_badge=("OFFICIAL FIGMA DESIGN SYSTEM", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # 3-Column Balanced High-Density Architecture
    # Col 1: Typography Scale & Text Styles (w=520, x=100)
    # Col 2: Color Palette Matrix (15 Swatches) + Iconography System (32 Icons) (w=600, x=640)
    # Col 3: Spacing, Radius, Elevation & Component State Tokens (w=560, x=1260)
    
    # =========================================================================
    # COLUMN 1: TYPOGRAPHY HIERARCHY (w=520, x=100)
    # =========================================================================
    c1_x, c1_w = 100, 520
    draw.rounded_rectangle([c1_x, card_y, c1_x + c1_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c1_x + 25, cy=card_y + 35, text="TYPOGRAPHY SYSTEM", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((c1_x + 25, card_y + 68), "Pretendard 폰트 시스템", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c1_x + 25, card_y + 92), "피그마 원본 12단계 계층 규격 (Bold / Medium / Regular)", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    typo_specs = [
        ("Pretendard Bold 헤드라인 48", "48px / Bold", "메인 대시보드 및 핵심 통계 지표 대형 타이틀", 17),
        ("Pretendard Bold 서브헤드 40", "40px / Bold", "주요 섹션 헤더 및 화면 전환 모듈 대표 명칭", 15.5),
        ("Pretendard Bold 헤드라인 32", "32px / Bold", "카드 타이틀 및 단계별 워크플로우 명칭", 14.5),
        ("Pretendard Bold 서브헤드 28", "28px / Bold", "모달 팝업 헤더 및 주요 분석 단계 라벨", 13.5),
        ("Pretendard Bold 서브헤드 20", "20px / Bold", "테이블 헤더, 탭 메뉴 및 위젯 그룹 타이틀", 13),
        ("Pretendard Medium 본문 18", "18px / Medium", "강조 본문 문장 및 주요 필지 안내 가이드", 12.5),
        ("Pretendard Medium 본문 16", "16px / Medium", "기본 입력 폼 필드, 셀렉트박스 및 리스트 텍스트", 12),
        ("Pretendard Medium 본문 14", "14px / Medium", "테이블 데이터 행 및 부가 설명 인라인 텍스트", 11.5),
        ("Pretendard Medium 본문 12", "12px / Medium", "배지 라벨, 버튼 보조 설명 및 차트 축 텍스트", 11),
        ("Pretendard Regular 본문 14", "14px / Regular", "상세 법적 가이드, 조례 해석 설명문", 11.5),
        ("Pretendard Regular 본문 12", "12px / Regular", "주석, 참고 데이터 및 툴팁 텍스트", 11),
        ("Pretendard Regular 캡션 11", "11px / Regular", "타임스탬프, 저작권, 출처 표기 (KCI/공공포털)", 10.5)
    ]
    
    ty_start = card_y + 118
    row_h = 49
    for i, (t_name, t_size, t_usage, font_sz) in enumerate(typo_specs):
        r_y = ty_start + i * row_h
        bg_col = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rounded_rectangle([c1_x + 20, r_y, c1_x + c1_w - 20, r_y + 44], radius=8, fill=bg_col, outline=BORDER_LIGHT, width=1)
        
        # Sample indicator bar
        bar_col = BRAND_GREEN if "Bold" in t_name else (BRAND_TEAL if "Medium" in t_name else (148, 163, 184))
        draw.rounded_rectangle([c1_x + 24, r_y + 8, c1_x + 28, r_y + 36], radius=2, fill=bar_col)
        
        draw.text((c1_x + 36, r_y + 14), t_name, font=get_font(font_sz, 'bold' if 'Bold' in t_name else ('medium' if 'Medium' in t_name else 'regular')), fill=TEXT_LIGHT_MAIN)
        draw_pill_badge(draw, left_x=c1_x + c1_w - 125, cy=r_y + 22, text=t_size, font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
        draw.text((c1_x + 36, r_y + 29), t_usage, font=get_font(10, 'regular'), fill=TEXT_LIGHT_SUB)

    # =========================================================================
    # COLUMN 2: COLOR MATRIX + ICONOGRAPHY SYSTEM (w=600, x=640)
    # =========================================================================
    c2_x, c2_w = 640, 600
    draw.rounded_rectangle([c2_x, card_y, c2_x + c2_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c2_x + 25, cy=card_y + 35, text="COLOR & ICONOGRAPHY TOKENS", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((c2_x + 25, card_y + 68), "컬러 팔레트 & 24px 아이콘 세트", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c2_x + 25, card_y + 92), "Agri-Tech 브랜드 아이덴티티 및 직관적 시각 언어 규격", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    # 1. Color Palette (15 Swatches in 3 rows x 5 cols)
    color_tokens = [
        # Row 1: Brand & Dark
        {"name": "Primary-500", "code": "#16C666", "rgb": (22, 198, 102), "role": "메인 브랜드 컬러"},
        {"name": "Primary-300", "code": "#38E085", "rgb": (56, 224, 133), "role": "포커스/인터랙션"},
        {"name": "Secondary", "code": "#14B8A6", "rgb": (20, 184, 166), "role": "GIS/시뮬레이션"},
        {"name": "Black", "code": "#000000", "rgb": (0, 0, 0), "role": "순수 블랙"},
        {"name": "Neutral-900", "code": "#1E293B", "rgb": (30, 41, 59), "role": "헤드라인/대비 텍스트"},
        
        # Row 2: Grayscale Neutrals
        {"name": "Neutral-700", "code": "#334155", "rgb": (51, 65, 85), "role": "서브헤드/아이콘"},
        {"name": "Neutral-600", "code": "#475569", "rgb": (71, 85, 105), "role": "본문 메인 텍스트"},
        {"name": "Neutral-500", "code": "#64748B", "rgb": (100, 116, 139), "role": "캡션/플레이스홀더"},
        {"name": "Neutral-400", "code": "#94A3B8", "rgb": (148, 163, 184), "role": "비활성/보조 테두리"},
        {"name": "Neutral-300", "code": "#CBD5E1", "rgb": (203, 213, 225), "role": "디바이더/카드 테두리"},
        
        # Row 3: Light Backgrounds & Semantics
        {"name": "Neutral-200", "code": "#E2E8F0", "rgb": (226, 232, 240), "role": "인풋/버튼 배경"},
        {"name": "Neutral-100", "code": "#F1F5F9", "rgb": (241, 245, 249), "role": "컨테이너 배경"},
        {"name": "White", "code": "#FFFFFF", "rgb": (255, 255, 255), "role": "기본 캔버스 카드"},
        {"name": "Error-500", "code": "#EF4444", "rgb": (239, 68, 68), "role": "인허가 불가/경고"},
        {"name": "Warning-500", "code": "#F59E0B", "rgb": (245, 158, 11), "role": "조건부 허가/유의"}
    ]
    
    pal_y = card_y + 120
    sw_w = 104
    sw_h = 76
    gap_x = 10
    gap_y = 12
    
    for idx, c in enumerate(color_tokens):
        row = idx // 5
        col = idx % 5
        bx = c2_x + 20 + col * (sw_w + gap_x)
        by = pal_y + row * (sw_h + gap_y)
        
        # Swatch Box
        draw.rounded_rectangle([bx, by, bx + sw_w, by + sw_h], radius=10, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        # Color bar
        c_outline = (203, 213, 225) if c["name"] == "White" else None
        draw.rounded_rectangle([bx + 6, by + 6, bx + sw_w - 6, by + 34], radius=6, fill=c["rgb"], outline=c_outline, width=1)
        # Token Name & Hex Code
        draw.text((bx + 8, by + 42), c["name"], font=get_font(10.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((bx + 8, by + 58), c["code"], font=get_font(9.5, 'medium'), fill=TEXT_LIGHT_SUB)
        
    # Divider between Colors and Icons
    mid_div_y = pal_y + 3 * (sw_h + gap_y) + 12
    draw.line([(c2_x + 20, mid_div_y), (c2_x + c2_w - 20, mid_div_y)], fill=BORDER_LIGHT, width=1)
    
    # 2. System Iconography Section
    icon_hdr_y = mid_div_y + 16
    draw_pill_badge(draw, left_x=c2_x + 20, cy=icon_hdr_y + 10, text="FIGMA 24px SYSTEM ICONOGRAPHY", font=get_font(10, 'bold'), theme='gray', pad_x=10, height=20)
    draw.text((c2_x + 215, icon_hdr_y + 10), "32종 피그마 벡터 심볼 (지도 탐색 · 분석 · 필터 · 제어)", font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    # 32 System Icons representation (4 rows x 8 cols)
    icon_list = [
        "새로고침", "더보기", "상향이동", "필터정렬", "닫기/삭제", "빌딩/건축", "토지경계", "레이어설정",
        "인허가지표", "지적도추출", "일반지도", "위성스카이", "홈대시보드", "내보내기", "다운로드", "데이터분석",
        "보안인증", "검색/조회", "고객지원", "접기/펼치기", "승인/체크", "경고안내", "위치마커", "시간기록",
        "구글로그인", "카카오연동", "드롭다운", "선택체크", "화면보기", "숨김처리", "줌인(확대)", "줌아웃(축소)"
    ]
    
    ic_start_y = icon_hdr_y + 30
    ic_box_w = 64
    ic_box_h = 50
    ic_gap_x = 7
    ic_gap_y = 8
    
    for idx, ic_name in enumerate(icon_list):
        i_row = idx // 8
        i_col = idx % 8
        ix = c2_x + 20 + i_col * (ic_box_w + ic_gap_x)
        iy = ic_start_y + i_row * (ic_box_h + ic_gap_y)
        
        draw.rounded_rectangle([ix, iy, ix + ic_box_w, iy + ic_box_h], radius=8, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        # Small icon symbol circle
        sym_col = BRAND_GREEN if idx in [0, 6, 7, 10, 11, 20] else (BRAND_TEAL if idx in [5, 12, 15, 22] else (100, 116, 139))
        draw.ellipse([ix + ic_box_w//2 - 9, iy + 8, ix + ic_box_w//2 + 9, iy + 26], fill=(255, 255, 255), outline=sym_col, width=1)
        # Dot inside
        draw.ellipse([ix + ic_box_w//2 - 2, iy + 15, ix + ic_box_w//2 + 2, iy + 19], fill=sym_col)
        # Label
        draw.text((ix + ic_box_w//2, iy + 36), ic_name, font=get_font(9, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')

    # =========================================================================
    # COLUMN 3: SPACING, RADIUS, ELEVATION & COMPONENT STATES (w=560, x=1260)
    # =========================================================================
    c3_x, c3_w = 1260, 560
    draw.rounded_rectangle([c3_x, card_y, c3_x + c3_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c3_x + 25, cy=card_y + 35, text="ATOMIC METRICS & COMPONENTS", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((c3_x + 25, card_y + 68), "규격 단위 & 컴포넌트 토큰", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c3_x + 25, card_y + 92), "8-pt 그리드 Spacing, Radius, Stroke 및 컴포넌트 상태", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    # 1. Spacing & Radius Table (Dual Column Grid)
    t_y = card_y + 120
    
    # Left Sub-table: Spacing Tokens (w=245)
    sp_x, sp_w = c3_x + 20, 245
    draw.rounded_rectangle([sp_x, t_y, sp_x + sp_w, t_y + 265], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=sp_x + 14, cy=t_y + 18, text="SPACING SCALE (8-PT)", font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
    
    spacings = [
        ("Spacing / 4", "4px", "초밀착 인라인 여백"),
        ("Spacing / 8", "8px", "컴포넌트 내부 패딩 (S)"),
        ("Spacing / 12", "12px", "폼 요소 내부 여백"),
        ("Spacing / 16", "16px", "기본 카드/모듈 패딩 (M)"),
        ("Spacing / 24", "24px", "카드 간격 / 컴포넌트 갭"),
        ("Spacing / 32", "32px", "섹션 그룹 간격 (L)"),
        ("Spacing / 40", "40px", "대형 모듈 외부 여백 (XL)")
    ]
    sy_cur = t_y + 38
    for s_label, s_val, s_desc in spacings:
        draw.text((sp_x + 14, sy_cur + 8), s_label, font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw_pill_badge(draw, left_x=sp_x + sp_w - 55, cy=sy_cur + 13, text=s_val, font=get_font(9.5, 'bold'), theme='blue', pad_x=6, height=16)
        draw.text((sp_x + 14, sy_cur + 21), s_desc, font=get_font(9.5, 'regular'), fill=TEXT_LIGHT_SUB)
        draw.line([(sp_x + 14, sy_cur + 32), (sp_x + sp_w - 14, sy_cur + 32)], fill=(226, 232, 240), width=1)
        sy_cur += 32
        
    # Right Sub-table: Radius & Stroke Tokens (w=255)
    rad_x, rad_w = c3_x + 285, 255
    draw.rounded_rectangle([rad_x, t_y, rad_x + rad_w, t_y + 265], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rad_x + 14, cy=t_y + 18, text="RADIUS & STROKE TOKENS", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    
    geom_tokens = [
        ("Radius / Small", "4px", "태그/체크박스/뱃지 모서리"),
        ("Radius / Medium", "8px", "버튼/인풋 필드/셀렉트박스"),
        ("Radius / Large", "16px", "카드 컨테이너/모달 팝업"),
        ("Radius / Circle", "999px", "원형 아바타/알약형 뱃지"),
        ("Stroke / Light", "0.5px", "보조 디바이더/차트 그리드"),
        ("Stroke / Default", "1.0px", "기본 카드 테두리/인풋 아웃라인"),
        ("Stroke / Strong", "2.0px", "포커스/활성 선택 상태 테두리")
    ]
    gy_cur = t_y + 38
    for g_label, g_val, g_desc in geom_tokens:
        draw.text((rad_x + 14, gy_cur + 8), g_label, font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw_pill_badge(draw, left_x=rad_x + rad_w - 60, cy=gy_cur + 13, text=g_val, font=get_font(9.5, 'bold'), theme='green', pad_x=6, height=16)
        draw.text((rad_x + 14, gy_cur + 21), g_desc, font=get_font(9.5, 'regular'), fill=TEXT_LIGHT_SUB)
        draw.line([(rad_x + 14, gy_cur + 32), (rad_x + rad_w - 14, gy_cur + 32)], fill=(226, 232, 240), width=1)
        gy_cur += 32

    # 2. Interactive Component States Showcase (Bottom Panel of Col 3)
    comp_y = t_y + 280
    draw.rounded_rectangle([c3_x + 20, comp_y, c3_x + c3_w - 20, card_y + card_h - 25], radius=14, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c3_x + 35, cy=comp_y + 22, text="UI COMPONENT STATES SPEC", font=get_font(10, 'bold'), theme='green', pad_x=10, height=20)
    draw.text((c3_x + 215, comp_y + 22), "실제 앱 화면 적용 인터랙티브 상태 규격", font=get_font(12, 'bold'), fill=BRAND_DARK, anchor='lm')
    
    # 4 Interactive Examples: Primary Button, Input Field, Badge State, Selection Card
    # Example 1: Button States
    ex1_y = comp_y + 44
    draw.text((c3_x + 35, ex1_y + 12), "1. 버튼 인터랙션", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_MAIN)
    # Default State
    draw.rounded_rectangle([c3_x + 145, ex1_y, c3_x + 260, ex1_y + 28], radius=8, fill=BRAND_GREEN)
    draw.text((c3_x + 202, ex1_y + 14), "분석 시작하기", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((c3_x + 202, ex1_y + 34), "Default", font=get_font(9, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')
    # Hover State
    draw.rounded_rectangle([c3_x + 275, ex1_y, c3_x + 390, ex1_y + 28], radius=8, fill=BRAND_DARK)
    draw.text((c3_x + 332, ex1_y + 14), "분석 시작하기", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((c3_x + 332, ex1_y + 34), "Hover/Active", font=get_font(9, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')
    # Disabled State
    draw.rounded_rectangle([c3_x + 405, ex1_y, c3_x + 520, ex1_y + 28], radius=8, fill=(226, 232, 240))
    draw.text((c3_x + 462, ex1_y + 14), "선택 대기중", font=get_font(11, 'bold'), fill=(148, 163, 184), anchor='mm')
    draw.text((c3_x + 462, ex1_y + 34), "Disabled", font=get_font(9, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    # Example 2: Input Field & Badges
    ex2_y = ex1_y + 52
    draw.text((c3_x + 35, ex2_y + 12), "2. 필지 진단 뱃지", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_MAIN)
    # Pass Badge
    draw_pill_badge(draw, left_x=c3_x + 145, cy=ex2_y + 14, text="적합 · 개발가능", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=26)
    # Warning Badge
    draw_pill_badge(draw, left_x=c3_x + 275, cy=ex2_y + 14, text="조건부 · 심의필요", font=get_font(10.5, 'bold'), theme='yellow', pad_x=12, height=26)
    # Error Badge
    draw_pill_badge(draw, left_x=c3_x + 405, cy=ex2_y + 14, text="불가 · 보전관리지역", font=get_font(10.5, 'bold'), theme='red', pad_x=12, height=26)
    
    # Example 3: Elevation & Shadow System Summary
    ex3_y = ex2_y + 48
    draw.rounded_rectangle([c3_x + 35, ex3_y, c3_x + c3_w - 35, ex3_y + 52], radius=10, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    draw.text((c3_x + 50, ex3_y + 16), "💡 4-Tier Elevation System (그림자 계층 규격)", font=get_font(11.5, 'bold'), fill=BRAND_DARK)
    elev_desc = "Elevation-01(카드 Y:2 B:4), Elevation-02(드롭다운 Y:4 B:12), Elevation-03(모달 Y:10 B:24), Elevation-04(플로팅 FAB Y:16 B:32 15% Green Blur)"
    draw.text((c3_x + 50, ex3_y + 34), elev_desc, font=get_font(10, 'regular'), fill=TEXT_LIGHT_SUB)

    draw_slide_footer(draw, 8, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_08.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
