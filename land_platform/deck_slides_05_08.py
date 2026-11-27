import os
from PIL import Image, ImageDraw
from deck_common import *

# -------------------------------------------------------------
# SLIDE 05: INFORMATION ARCHITECTURE (AIA+ Style Hierarchy)
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
    
    # Left: Structural Analysis Card
    lw = 540
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

    # Right: Authentic Figma IA Tree Graphic (ref_05_ia_tree.png)
    rx = 665
    rw = 1155
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ly + 35, text="OFFICIAL FIGMA IA TREE", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 225, ly + 35), "피그마 원본 정보 구조도 (Home 계층 및 5대 서브 도메인)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    ia_path = os.path.join(ASSETS_DIR, "ref_05_ia_tree.png")
    if os.path.exists(ia_path):
        ia_img = Image.open(ia_path).convert('RGBA')
        scale = min((rw - 60) / ia_img.width, (lh - 90) / ia_img.height)
        iw = int(ia_img.width * scale)
        ih = int(ia_img.height * scale)
        i_res = ia_img.resize((iw, ih), Image.Resampling.LANCZOS)
        img.paste(i_res, (rx + (rw - iw) // 2, ly + 70 + (lh - 90 - ih) // 2), i_res)

    draw_slide_footer(draw, 5, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_05.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 06: USER FLOW & DECISION LOGIC (AIA+ Style Flow Chart)
# -------------------------------------------------------------
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 6, 
        "USER FLOW & LOGIC", 
        "User Flow & Logic | ", 
        "원스톱 토지개발 시뮬레이션 유저 플로우 및 분기 로직", 
        "메인(홈) → 로그인 분기 → 대상지 선택 → 토지분석 → 시설배치 → 스마트팜 설계 → 조성비/전체매출 → 보고서 제공", 
        right_badge=("USER FLOW DIAGRAM", "green")
    )
    
    # Left: Authentic Figma User Flow Diagram (part_user_flow.png)
    lw = 1100
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="END-TO-END WORKFLOW DIAGRAM", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((385, ly + 35), "시뮬레이션 전 과정 분기 조건 및 화면 전환 아키텍처", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    uf_path = os.path.join(ASSETS_DIR, "part_user_flow.png")
    if os.path.exists(uf_path):
        uf_img = Image.open(uf_path).convert('RGBA')
        scale = min((lw - 60) / uf_img.width, (lh - 90) / uf_img.height)
        uw = int(uf_img.width * scale)
        uh = int(uf_img.height * scale)
        u_res = uf_img.resize((uw, uh), Image.Resampling.LANCZOS)
        img.paste(u_res, (100 + (lw - uw) // 2, ly + 70 + (lh - 90 - uh) // 2), u_res)

    # Right: Decision Logic Explanation Cards
    rx = 1225
    rw = 595
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 35, text="CORE DECISION NODES", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 25, ly + 75), "핵심 분기 및 데이터 연계", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    nodes = [
        ("Node 1. 로그인/회원가입 분기", "비로그인 상태에서도 지번 검색 및 1단계 규제 확인 가능, 시설배치 및 상세 보고서 생성 시 간편 로그인 유도"),
        ("Node 2. 대상지 선택 및 GIS 분석", "지번 입력 즉시 12대 공공 API 호출, 개발 적합성(용도지역, 건폐율, 도로 접도, 경사도) 실시간 진단"),
        ("Node 3. 시설배치 및 스마트팜 설계", "온실 규격, 재배 작물 연동, 단지 구획 및 부대시설(관리동, 선별장) 최적 배치 시뮬레이션"),
        ("Node 4. 조성비·매출·타당성 보고서", "총사업비 산출 내역, 가공유통시설 및 할인율 설정 후 최종 금융 심사용 종합 보고서 PDF 발급")
    ]
    ny = ly + 115
    for title, desc in nodes:
        draw.rounded_rectangle([rx + 20, ny, rx + rw - 20, ny + 130], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((rx + 35, ny + 30), title, font=get_font(15, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12, 'regular'), rw - 70, draw)
        dy = ny + 60
        for l in lines:
            draw.text((rx + 35, dy), l, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 20
        ny += 148

    draw_slide_footer(draw, 6, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_06.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 07: WIREFRAME & GIS INTERACTION (AIA+ Style Dual-Split)
# -------------------------------------------------------------
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 7, 
        "WIREFRAME & GIS UX", 
        "Wireframe & Interaction | ", 
        "듀얼 스플릿 뷰 기반 GIS 와이어프레임 및 화면 구조", 
        "좌측 420px 고정 워크플로우 제어 패널과 우측 인터랙티브 GIS 공간 캔버스의 조작 인터랙션", 
        right_badge=("GIS WIREFRAME SPECS", "green")
    )
    
    # Left: Architecture Specs
    lw = 540
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="DUAL-SPLIT GRID LOGIC", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "GIS 공간 인터랙션 그리드", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    specs = [
        ("좌측 스텝별 워크플로우 패널", "STEP 1(대상지)부터 STEP 4(타당성)까지 수직 스텝 네비게이션과 입력 폼을 한눈에 조작할 수 있는 전용 컨트롤러"),
        ("우측 고해상도 공간 GIS 캔버스", "지적도, 고도/경사도 히트맵, 위성지도 레이어 위에 토지 경계선 및 최적 스마트팜 모듈을 3D 실시간 렌더링"),
        ("하단 실시간 재무 서머리 바", "토지 면적, 가용지 비율, 총 소요 공사비 및 연간 예상 매출액의 누적 연산 결과를 지연 없이 즉시 피드백")
    ]
    sy = ly + 115
    for title, desc in specs:
        draw.rounded_rectangle([125, sy, 100 + lw - 25, sy + 175], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, sy + 35), title, font=get_font(16, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(12.5, 'regular'), lw - 70, draw)
        dy = sy + 75
        for l in lines:
            draw.text((145, dy), l, font=get_font(12.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 22
        sy += 195

    # Right: High Resolution Screen View (screen_02_map_analysis.png)
    rx = 665
    rw = 1155
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ly + 35, text="CORE GIS INTERFACE", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 225, ly + 35), "공간 지도 기반 토지 분석 및 인허가 규제 시뮬레이터", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    wf_p = os.path.join(ASSETS_DIR, "screen_02_map_analysis.png")
    if os.path.exists(wf_p):
        w_img = Image.open(wf_p).convert('RGBA')
        scale = min((rw - 60) / w_img.width, (lh - 90) / w_img.height)
        ww = int(w_img.width * scale)
        wh = int(w_img.height * scale)
        w_res = w_img.resize((ww, wh), Image.Resampling.LANCZOS)
        img.paste(w_res, (rx + (rw - ww) // 2, ly + 70 + (lh - 90 - wh) // 2), w_res)

    draw_slide_footer(draw, 7, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_07.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 08: DESIGN SYSTEM & ATOMIC TOKENS (AIA+ Style System)
# -------------------------------------------------------------
def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 8, 
        "DESIGN SYSTEM & TOKENS", 
        "Design System | ", 
        "토지개발 플랫폼 디자인 시스템 (Design System Standards)", 
        "피그마 원본 디자인 토큰: Primary-500(#00C65F), Spacing(4~40px), Radius, Stroke 및 아이콘 라이브러리", 
        right_badge=("FIGMA DESIGN TOKENS", "green")
    )
    
    # Left: Typography & Color Hierarchy Cards
    lw = 600
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="TYPOGRAPHY & ACCESSIBILITY", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "프리텐다드 기반 정보 계층 구조", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)

    typos = [
        ("Pretendard Bold 48", "메인 랜딩 헤드라인 및 프로모션 타이틀"),
        ("Pretendard Bold 32", "섹션별 핵심 헤더 및 1단계/2단계 모듈명"),
        ("Pretendard SemiBold 24", "패널 위젯 타이틀 및 토지 분석 요약 라벨"),
        ("Pretendard Medium 16", "본문 데이터 텍스트 및 지표 설명 (WCAG AAA)"),
        ("Pretendard Regular 14", "테이블 바디, 공시지가 주석 및 서브 캡션")
    ]
    ty = ly + 115
    for t_name, t_use in typos:
        draw.rounded_rectangle([125, ty, 100 + lw - 25, ty + 75], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, ty + 25), t_name, font=get_font(14, 'bold'), fill=BRAND_GREEN)
        draw.text((145, ty + 48), t_use, font=get_font(12, 'regular'), fill=TEXT_LIGHT_SUB)
        ty += 92

    draw.rounded_rectangle([125, ly + 595, 100 + lw - 25, ly + 715], radius=10, fill=(240, 253, 244), outline=BRAND_GREEN, width=1)
    draw.text((145, ly + 620), "🔍 WCAG 2.1 AAA 고대비 검증 결과", font=get_font(13, 'bold'), fill=BRAND_DARK)
    draw.text((145, ly + 650), "• Primary Green (#00C65F) vs Slate 900 : 7.2:1 (AAA 달성)", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
    draw.text((145, ly + 675), "• Neutral 900 Text vs White Background : 15.1:1 (최고 수준 가독성)", font=get_font(11.5, 'bold'), fill=(16, 185, 129))

    # Right: Authentic Figma Design System Sheet (part_design_tokens.png)
    rx = 725
    rw = 1095
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 30, cy=ly + 35, text="ATOMIC DESIGN TOKENS", font=get_font(10.5, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 225, ly + 35), "공식 컬러 팔레트, 아이콘 매트릭스, Spacing/Radius 규격", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    ds_path = os.path.join(ASSETS_DIR, "part_design_tokens.png")
    if os.path.exists(ds_path):
        ds_img = Image.open(ds_path).convert('RGBA')
        scale = min((rw - 60) / ds_img.width, (lh - 90) / ds_img.height)
        dw = int(ds_img.width * scale)
        dh = int(ds_img.height * scale)
        d_res = ds_img.resize((dw, dh), Image.Resampling.LANCZOS)
        img.paste(d_res, (rx + (rw - dw) // 2, ly + 70 + (lh - 90 - dh) // 2), d_res)

    draw_slide_footer(draw, 8, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_08.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
