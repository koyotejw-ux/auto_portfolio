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
        "홈 중심의 회원체계, 코어 시뮬레이터, 사용자 통계, 마이 프로젝트, 관리자 콘솔 구조", 
        right_badge=("PLATFORM IA TREE", "green")
    )
    
    lw = 480
    lh = 740
    ly = 220
    draw.rounded_rectangle([100, ly, 100 + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=130, cy=ly + 35, text="5-DOMAIN IA PRINCIPLES", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((130, ly + 75), "5대 핵심 도메인 아키텍처", font=get_font(20, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    principles = [
        ("01. 회원/인증 체계", "일반 농가부터 전문 개발사까지 유형별 맞춤 권한 관리 및 온보딩"),
        ("02. 코어 시뮬레이터", "대상지 탐색부터 시설배치, 적산, 매출설계 5단계 파이프라인"),
        ("03. 사용자 통계 센터", "지역별 인기 개발 유형 및 평균 투자수익률 실시간 집계 대시보드"),
        ("04. 마이 프로젝트", "저장된 시뮬레이션 프로젝트 즉시 재호출 및 금융 보고서 발급"),
        ("05. 관리자 콘솔", "공공 API 연동 모니터링 및 전국 토지 규제 조례 DB 실시간 동기화")
    ]
    py = ly + 115
    for title, desc in principles:
        draw.rounded_rectangle([125, py, 100 + lw - 25, py + 105], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((145, py + 24), title, font=get_font(14.5, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(desc, get_font(11.5, 'regular'), lw - 70, draw)
        dy = py + 52
        for l in lines:
            draw.text((145, dy), l, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        py += 120

    rx = 605
    rw = 1215
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_ia = draw_pill_badge(draw, left_x=rx + 30, cy=ly + 35, text="DIRECT VECTOR HIERARCHY TREE", font=get_font(10, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 30 + bw_ia + 14, ly + 35), "피그마 원본 정보 구조도 (Home 중심 4대 도메인 및 16개 서브 노드)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    root_x, root_y, root_w, root_h = rx + rw//2 - 90, ly + 82, 180, 52
    draw.rounded_rectangle([root_x, root_y, root_x + root_w, root_y + root_h], radius=26, fill=BRAND_GREEN)
    draw.text((root_x + root_w//2, root_y + root_h//2), "Home (앱 메인)", font=get_font(16, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    categories = [
        ("01. 회원가입/로그인", ["로그인", "회원가입", "비밀번호 찾기", "서비스 이용약관"]),
        ("02. 시뮬레이션 (Core)", ["시뮬레이션 시작", "시뮬레이션 통계", "진행 이력 관리", "보고서 뷰어"]),
        ("03. 사용자 통계 & 마이", ["지역별 개발 통계", "비용/수익률 집계", "내 프로젝트 보관", "결제 및 영수증"]),
        ("04. 관리자 콘솔", ["메인 위젯 관리", "공공 API 연동", "토지 규제 DB", "회원 권한 관리"])
    ]
    
    cat_w = 265
    cat_gap = 25
    cat_start_x = rx + (rw - (4 * cat_w + 3 * cat_gap)) // 2
    cat_y = ly + 200
    
    stem_y = ly + 162
    draw.line([(root_x + root_w//2, root_y + root_h), (root_x + root_w//2, stem_y)], fill=(148, 163, 184), width=2)
    draw.line([(cat_start_x + cat_w//2, stem_y), (cat_start_x + 3 * (cat_w + cat_gap) + cat_w//2, stem_y)], fill=(148, 163, 184), width=2)
    
    for c_idx, (cat_title, sub_nodes) in enumerate(categories):
        cx = cat_start_x + c_idx * (cat_w + cat_gap)
        draw.line([(cx + cat_w//2, stem_y), (cx + cat_w//2, cat_y)], fill=(148, 163, 184), width=2)
        
        col_hdr = BRAND_DARK if c_idx == 1 else (30, 41, 59)
        draw.rounded_rectangle([cx, cat_y, cx + cat_w, cat_y + 44], radius=10, fill=col_hdr)
        draw.text((cx + cat_w//2, cat_y + 22), cat_title, font=get_font(13.5, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        node_start_y = cat_y + 66
        for n_idx, node_text in enumerate(sub_nodes):
            ny = node_start_y + n_idx * 68
            draw.line([(cx + cat_w//2, ny - 22), (cx + cat_w//2, ny + 22)], fill=(203, 213, 225), width=2)
            box_bg = (240, 253, 244) if c_idx == 1 else (248, 250, 252)
            box_bd = (167, 243, 208) if c_idx == 1 else BORDER_LIGHT
            draw.rounded_rectangle([cx + 10, ny, cx + cat_w - 10, ny + 48], radius=8, fill=box_bg, outline=box_bd, width=1)
            draw.ellipse([cx + 26, ny + 21, cx + 32, ny + 27], fill=BRAND_GREEN)
            draw.text((cx + 42, ny + 24), node_text, font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')

    draw.rounded_rectangle([rx + 30, ly + lh - 66, rx + rw - 30, ly + lh - 20], radius=10, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    bw_kp = draw_pill_badge(draw, left_x=rx + 46, cy=ly + lh - 43, text="IA KEY VALUE", font=get_font(9.5, 'bold'), theme='green', solid=True, pad_x=10, height=20)
    draw.text((rx + 46 + bw_kp + 14, ly + lh - 43), "복잡한 GIS 및 금융 분석 단계를 '홈 → 시뮬레이션 → 통계 → 보고서'의 4단 직관 흐름으로 표준화", font=get_font(12, 'bold'), fill=BRAND_DARK, anchor='lm')

    draw_slide_footer(draw, 5, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_05.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 06: RESPONSIVE WIREFRAME SYSTEM (Native Vector Wireframes)
# -------------------------------------------------------------
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 6, 
        "RESPONSIVE WIREFRAME SYSTEM", 
        "Wireframe Architecture | ", 
        "반응형 랜딩페이지 및 코어 GIS 시뮬레이터 와이어프레임 설계", 
        "프로덕트 2대 핵심 경험: [1] 고객 유입용 패럴랙스 랜딩페이지  |  [2] B2B 듀얼 스플릿 GIS 시뮬레이터 워크스페이스 구조", 
        right_badge=("PREDICTIVE WIREFRAME", "green")
    )
    
    card_y = 215
    card_h = 745
    
    c1_x, c1_w = 100, 830
    draw.rounded_rectangle([c1_x, card_y, c1_x + c1_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_wf1 = draw_pill_badge(draw, left_x=c1_x + 25, cy=card_y + 35, text="WIREFRAME 01 · LANDING PAGE", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24)
    draw.text((c1_x + 25 + bw_wf1 + 14, card_y + 35), "반응형 랜딩페이지 와이어프레임 (1920px)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    wf1_y = card_y + 70
    draw.rounded_rectangle([c1_x + 25, wf1_y, c1_x + c1_w - 25, wf1_y + 45], radius=6, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((c1_x + 45, wf1_y + 22), "FARMINGSYS", font=get_font(13, 'bold'), fill=BRAND_GREEN, anchor='lm')
    navs = ["시뮬레이터", "사용자통계", "마이페이지", "관리자"]
    for idx, nv in enumerate(navs):
        draw.text((c1_x + 220 + idx * 110, wf1_y + 22), nv, font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='lm')
    draw.rounded_rectangle([c1_x + c1_w - 125, wf1_y + 10, c1_x + c1_w - 40, wf1_y + 35], radius=12, fill=BRAND_GREEN)
    draw.text((c1_x + c1_w - 82, wf1_y + 22), "새로시작", font=get_font(10.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    hero_y = wf1_y + 55
    hero_h = 240
    draw.rounded_rectangle([c1_x + 25, hero_y, c1_x + c1_w - 25, hero_y + hero_h], radius=10, fill=(30, 41, 59))
    draw.text((c1_x + 50, hero_y + 48), "고객의", font=get_font(18, 'bold'), fill=BRAND_GREEN)
    draw.text((c1_x + 50, hero_y + 80), "토지개발 사업에 동행하다", font=get_font(22, 'bold'), fill=(255, 255, 255))
    draw.text((c1_x + 50, hero_y + 122), "빅데이터 기반 토지 분석과 지능형 스마트팜 시뮬레이션", font=get_font(12, 'regular'), fill=(203, 213, 225))
    draw.rounded_rectangle([c1_x + 50, hero_y + 158, c1_x + 216, hero_y + 196], radius=19, fill=BRAND_GREEN)
    draw.text((c1_x + 133, hero_y + 177), "시뮬레이터 시작하기 →", font=get_font(11.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    desk_x = c1_x + c1_w - 375
    desk_y = hero_y + 25
    desk_w, desk_h = 325, 190
    draw.rounded_rectangle([desk_x, desk_y, desk_x + desk_w, desk_y + desk_h], radius=8, fill=(15, 23, 42), outline=(71, 85, 105), width=2)
    draw.rectangle([desk_x + 10, desk_y + 10, desk_x + desk_w - 10, desk_y + desk_h - 10], fill=(51, 65, 85))
    draw.text((desk_x + desk_w//2, desk_y + desk_h//2), "Interactive 3D Preview", font=get_font(12, 'bold'), fill=BRAND_GREEN, anchor='mm')

    sec2_y = hero_y + hero_h + 22
    draw.text((c1_x + c1_w//2, sec2_y + 24), "고객의 비즈니스 파트너 · 토지개발 솔루션", font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((c1_x + c1_w//2, sec2_y + 48), "원하는 토지의 분석과 개발을 위한 솔루션을 제공하고 새로운 가치를 창출합니다.", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
    
    pillars = [
        ("토지소유주", "놀고 있는 땅의 가치를\n최대화하는 최적 시뮬레이션"),
        ("개발자/운영사", "토목·건축 표준 적산과\n인허가 리스크 사전 차단"),
        ("투자자/금융사", "정량 데이터 기반 연차별\nIRR/NPV 타당성 검증")
    ]
    pil_w = 236
    pil_gap = 26
    pil_sx = c1_x + (c1_w - (3 * pil_w + 2 * pil_gap)) // 2
    for idx, (p_title, p_desc) in enumerate(pillars):
        px = pil_sx + idx * (pil_w + pil_gap)
        py = sec2_y + 78
        draw.rounded_rectangle([px, py, px + pil_w, py + 175], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.ellipse([px + pil_w//2 - 22, py + 22, px + pil_w//2 + 22, py + 66], fill=BRAND_GREEN if idx==1 else (226, 232, 240))
        draw.text((px + pil_w//2, py + 44), str(idx+1), font=get_font(14, 'bold'), fill=(255, 255, 255) if idx==1 else (100, 116, 139), anchor='mm')
        draw.text((px + pil_w//2, py + 92), p_title, font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
        lines = p_desc.split('\n')
        draw.text((px + pil_w//2, py + 122), lines[0], font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')
        draw.text((px + pil_w//2, py + 142), lines[1], font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB, anchor='mm')

    # Right Wireframe: GIS Simulator
    c2_x, c2_w = 990, 830
    draw.rounded_rectangle([c2_x, card_y, c2_x + c2_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_wf2 = draw_pill_badge(draw, left_x=c2_x + 25, cy=card_y + 35, text="WIREFRAME 02 · GIS SIMULATOR", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((c2_x + 25 + bw_wf2 + 14, card_y + 35), "듀얼 스플릿 인터랙티브 시뮬레이터 (B2B 워크스페이스)", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    sim_y = card_y + 70
    draw.rounded_rectangle([c2_x + 25, sim_y, c2_x + c2_w - 25, sim_y + 40], radius=6, fill=(30, 41, 59))
    draw.text((c2_x + 45, sim_y + 20), "토지개발 분석 플랫폼  |  시뮬레이터 워크스페이스", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='lm')
    draw.text((c2_x + c2_w - 45, sim_y + 20), "STEP 1/5 : 대상지 분석", font=get_font(11, 'bold'), fill=BRAND_GREEN, anchor='rm')

    split_y = sim_y + 50
    split_h = card_h - 145
    
    panel_w = 270
    draw.rounded_rectangle([c2_x + 25, split_y, c2_x + 25 + panel_w, split_y + split_h], radius=8, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((c2_x + 40, split_y + 20), "STEP 1. 대상지 선택", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.rounded_rectangle([c2_x + 40, split_y + 48, c2_x + 15 + panel_w, split_y + 82], radius=6, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    # Vector magnifying glass icon
    draw.ellipse([c2_x + 50, split_y + 59, c2_x + 60, split_y + 69], outline=(148, 163, 184), width=2)
    draw.line([(c2_x + 59, split_y + 68), (c2_x + 63, split_y + 72)], fill=(148, 163, 184), width=2)
    draw.text((c2_x + 70, split_y + 65), "지번 검색 (고양시 덕양구...)", font=get_font(10.5, 'regular'), fill=(148, 163, 184), anchor='lm')
    
    panel_items = [
        ("토지 기본 정보", "지번, 총면적(750㎡), 지목(전)"),
        ("토지이용 규제 판정", "제2종일반주거지역, 건폐율 60%"),
        ("자연환경 분석", "표고 10미만, 경사도 5미만 (적합)"),
        ("공사비 사전 견적", "기본 토목공사비 표준값 자동 산정"),
        ("예상 사업 타당성", "초기 투자비 회수 예상 3년")
    ]
    p_item_y = split_y + 94
    for p_t, p_d in panel_items:
        draw.rounded_rectangle([c2_x + 40, p_item_y, c2_x + 15 + panel_w, p_item_y + 58], radius=6, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        draw.text((c2_x + 50, p_item_y + 14), p_t, font=get_font(11, 'bold'), fill=BRAND_GREEN)
        draw.text((c2_x + 50, p_item_y + 34), p_d, font=get_font(9.5, 'regular'), fill=TEXT_LIGHT_SUB)
        p_item_y += 66

    draw.rounded_rectangle([c2_x + 40, split_y + split_h - 56, c2_x + 15 + panel_w, split_y + split_h - 16], radius=8, fill=BRAND_GREEN)
    draw.text((c2_x + 25 + panel_w//2, split_y + split_h - 36), "다음 단계: 시설 배치 →", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')

    gis_x = c2_x + 25 + panel_w + 15
    gis_w = c2_w - panel_w - 65
    draw.rounded_rectangle([gis_x, split_y, gis_x + gis_w, split_y + split_h], radius=8, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    
    for gx in range(gis_x + 30, gis_x + gis_w, 40):
        draw.line([(gx, split_y), (gx, split_y + split_h)], fill=(226, 232, 240), width=1)
    for gy in range(split_y + 30, split_y + split_h, 40):
        draw.line([(gis_x, gy), (gis_x + gis_w, gy)], fill=(226, 232, 240), width=1)
        
    poly_pts = [
        (gis_x + 100, split_y + 120),
        (gis_x + 320, split_y + 90),
        (gis_x + 380, split_y + 260),
        (gis_x + 220, split_y + 380),
        (gis_x + 80, split_y + 300)
    ]
    draw.polygon(poly_pts, fill=(22, 198, 102, 50), outline=BRAND_GREEN, width=3)
    draw.text((gis_x + 210, split_y + 220), "선택 대상지 경계선\n총 면적: 750㎡\n(개발 적합도 100%)", font=get_font(12, 'bold'), fill=BRAND_DARK, anchor='mm')
    
    ctrl_x = gis_x + gis_w - 95
    ctrl_y = split_y + 20
    draw.rounded_rectangle([ctrl_x, ctrl_y, ctrl_x + 80, ctrl_y + 120], radius=8, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
    ctrl_labels = ["지적도", "일반지도", "위성스카이"]
    for idx, cl in enumerate(ctrl_labels):
        cy_b = ctrl_y + 10 + idx * 36
        draw.rounded_rectangle([ctrl_x + 8, cy_b, ctrl_x + 72, cy_b + 28], radius=4, fill=(236, 253, 245) if idx==2 else (248, 250, 252))
        draw.text((ctrl_x + 40, cy_b + 14), cl, font=get_font(9.5, 'bold' if idx==2 else 'regular'), fill=BRAND_GREEN if idx==2 else TEXT_LIGHT_SUB, anchor='mm')

    draw_slide_footer(draw, 6, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_06.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 07: DESIGN SYSTEM · ATOMIC TOKENS (Water Calculator Slide 07 Inspired)
# -------------------------------------------------------------
def _draw_vector_icon(draw, cx, cy, kind, col):
    if kind == 'map':
        draw.polygon([(cx-11, cy-7), (cx-3, cy-10), (cx+4, cy-6), (cx+11, cy-9), (cx+11, cy+7), (cx+4, cy+10), (cx-3, cy+6), (cx-11, cy+9)], outline=col, width=2)
        draw.line([(cx-3, cy-10), (cx-3, cy+6)], fill=col, width=1)
        draw.line([(cx+4, cy-6), (cx+4, cy+10)], fill=col, width=1)
    elif kind == 'layer':
        draw.polygon([(cx, cy-10), (cx+11, cy-4), (cx, cy+2), (cx-11, cy-4)], outline=col, width=2)
        draw.line([(cx-11, cy+2), (cx, cy+8), (cx+11, cy+2)], fill=col, width=2)
    elif kind == 'grid':
        for r in range(2):
            for c in range(2):
                x0 = cx - 9 + c * 10
                y0 = cy - 9 + r * 10
                draw.rounded_rectangle([x0, y0, x0+8, y0+8], radius=2, outline=col, width=2)
    elif kind == 'chart':
        draw.line([(cx-10, cy+9), (cx+10, cy+9)], fill=col, width=2)
        draw.rectangle([cx-8, cy+1, cx-4, cy+9], fill=col)
        draw.rectangle([cx-2, cy-4, cx+2, cy+9], fill=col)
        draw.rectangle([cx+4, cy-9, cx+8, cy+9], fill=col)
    elif kind == 'search':
        draw.ellipse([cx-9, cy-9, cx+4, cy+4], outline=col, width=2)
        draw.line([(cx+3, cy+3), (cx+10, cy+10)], fill=col, width=2)
    elif kind == 'doc':
        draw.rounded_rectangle([cx-8, cy-10, cx+8, cy+10], radius=2, outline=col, width=2)
        draw.line([(cx-4, cy-4), (cx+4, cy-4)], fill=col, width=2)
        draw.line([(cx-4, cy+1), (cx+4, cy+1)], fill=col, width=2)
        draw.line([(cx-4, cy+6), (cx+1, cy+6)], fill=col, width=2)
    elif kind == 'shield':
        draw.polygon([(cx, cy-10), (cx+9, cy-6), (cx+8, cy+3), (cx, cy+10), (cx-8, cy+3), (cx-9, cy-6)], outline=col, width=2)
        draw.line([(cx-4, cy), (cx-1, cy+3), (cx+5, cy-3)], fill=col, width=2)
    elif kind == 'download':
        draw.line([(cx, cy-9), (cx, cy+4)], fill=col, width=2)
        draw.line([(cx-5, cy-1), (cx, cy+4), (cx+5, cy-1)], fill=col, width=2)
        draw.line([(cx-9, cy+9), (cx+9, cy+9)], fill=col, width=2)

def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 7, 
        "DESIGN SYSTEM · ATOMIC TOKENS", 
        "Design System | ", 
        "Agri-Tech 브랜드 정체성을 규정하는 디자인 시스템 & 토큰 규격", 
        "Figma 1:1 규격화: Pretendard 6단계 타이포그래피, 10색 시맨틱 컬러, 24px 벡터 아이코노그래피 및 인터랙티브 컴포넌트 키트", 
        right_badge=("OFFICIAL FIGMA DESIGN SYSTEM", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # COLUMN 1: TYPOGRAPHY SYSTEM (w=520, x=100)
    c1_x, c1_w = 100, 520
    draw.rounded_rectangle([c1_x, card_y, c1_x + c1_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c1_x + 25, cy=card_y + 35, text="FOUNDATION 01 · TYPOGRAPHY", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24)
    draw.text((c1_x + 25, card_y + 66), "Pretendard 타이포그래피 스케일", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c1_x + 25, card_y + 92), "6대 핵심 텍스트 위계 · Tabular 고정폭 숫자 시스템 적용", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    typo_specs = [
        ("Headline 48", "48px / Bold", "Pretendard Bold", "메인 대시보드 타이틀 및 핵심 통계 지표 대형 숫자", 20, BRAND_GREEN),
        ("Headline 32", "32px / Bold", "Pretendard Bold", "카드 섹션 타이틀 및 시뮬레이션 단계별 명칭", 17, BRAND_DARK),
        ("Subhead 20", "20px / Bold", "Pretendard Bold", "테이블 헤더, 탭 메뉴 및 위젯 그룹 타이틀", 14.5, TEXT_LIGHT_MAIN),
        ("Body 16", "16px / Medium", "Pretendard Medium", "기본 입력 폼 필드, 셀렉트박스 및 메인 리스트 텍스트", 13, TEXT_LIGHT_MAIN),
        ("Body 14", "14px / Regular", "Pretendard Regular", "테이블 데이터 행, 세부 규제 설명 및 조례 가이드", 12, TEXT_LIGHT_SUB),
        ("Caption 12", "12px / Regular", "Pretendard Regular", "배지 라벨, 메타데이터 타임스탬프 및 툴팁 출처 표기", 11, (148, 163, 184))
    ]
    
    ty_start = card_y + 124
    row_h = 98
    for i, (t_name, t_size, t_family, t_usage, font_sz, bar_col) in enumerate(typo_specs):
        r_y = ty_start + i * row_h
        bg_col = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rounded_rectangle([c1_x + 20, r_y, c1_x + c1_w - 20, r_y + 88], radius=10, fill=bg_col, outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([c1_x + 28, r_y + 14, c1_x + 32, r_y + 74], radius=2, fill=bar_col)
        draw.text((c1_x + 42, r_y + 15), t_name, font=get_font(font_sz, 'bold' if 'Bold' in t_family else 'medium'), fill=TEXT_LIGHT_MAIN)
        draw_pill_badge(draw, left_x=c1_x + c1_w - 134, cy=r_y + 24, text=t_size, font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
        draw.text((c1_x + 42, r_y + 45), f"Font: {t_family}", font=get_font(10.5, 'medium'), fill=BRAND_TEAL)
        draw.text((c1_x + 42, r_y + 64), t_usage, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)

    # COLUMN 2: COLOR PALETTE & CRISP VECTOR ICONOGRAPHY (w=600, x=640)
    c2_x, c2_w = 640, 600
    draw.rounded_rectangle([c2_x, card_y, c2_x + c2_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c2_x + 25, cy=card_y + 35, text="FOUNDATION 02 · COLOR & ICONS", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((c2_x + 25, card_y + 66), "컬러 팔레트 및 24px 벡터 아이코노그래피", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c2_x + 25, card_y + 92), "Agri-Tech Trust 시맨틱 컬러 및 24×24px 광학 그리드 아이콘", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    color_tokens = [
        {"name": "Primary-500", "code": "#16C666", "rgb": (22, 198, 102)},
        {"name": "Primary-300", "code": "#38E085", "rgb": (56, 224, 133)},
        {"name": "Secondary", "code": "#14B8A6", "rgb": (20, 184, 166)},
        {"name": "Neutral-900", "code": "#1E293B", "rgb": (30, 41, 59)},
        {"name": "Neutral-700", "code": "#334155", "rgb": (51, 65, 85)},
        {"name": "Neutral-400", "code": "#94A3B8", "rgb": (148, 163, 184)},
        {"name": "Neutral-100", "code": "#F1F5F9", "rgb": (241, 245, 249)},
        {"name": "White", "code": "#FFFFFF", "rgb": (255, 255, 255)},
        {"name": "Error-500", "code": "#EF4444", "rgb": (239, 68, 68)},
        {"name": "Warning-500", "code": "#F59E0B", "rgb": (245, 158, 11)}
    ]
    
    pal_y = card_y + 124
    sw_w, sw_h = 104, 86
    gap_x, gap_y = 10, 10
    for idx, c in enumerate(color_tokens):
        row, col = idx // 5, idx % 5
        bx = c2_x + 20 + col * (sw_w + gap_x)
        by = pal_y + row * (sw_h + gap_y)
        draw.rounded_rectangle([bx, by, bx + sw_w, by + sw_h], radius=10, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        c_outline = (203, 213, 225) if c["name"] == "White" else None
        draw.rounded_rectangle([bx + 8, by + 8, bx + sw_w - 8, by + 38], radius=6, fill=c["rgb"], outline=c_outline, width=1)
        draw.text((bx + 8, by + 46), c["name"], font=get_font(10, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((bx + 8, by + 63), c["code"], font=get_font(9.5, 'medium'), fill=TEXT_LIGHT_SUB)
        
    mid_div_y = pal_y + 2 * (sw_h + gap_y) + 16
    draw.line([(c2_x + 20, mid_div_y), (c2_x + c2_w - 20, mid_div_y)], fill=BORDER_LIGHT, width=1)
    
    icon_hdr_y = mid_div_y + 16
    bw_ic = draw_pill_badge(draw, left_x=c2_x + 20, cy=icon_hdr_y + 10, text="24px VECTOR ICONOGRAPHY", font=get_font(9.5, 'bold'), theme='green', pad_x=10, height=20)
    draw.text((c2_x + 20 + bw_ic + 12, icon_hdr_y + 10), "핵심 GIS · 분석 · 리포트 시스템 아이콘", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    icon_specs = [
        ("지적도·경계", "ic_cadastral_map", "map", BRAND_GREEN),
        ("레이어 전환", "ic_gis_layers", "layer", BRAND_TEAL),
        ("온실 모듈", "ic_facility_grid", "grid", BRAND_GREEN),
        ("수익성 차트", "ic_roi_chart", "chart", (37, 99, 235)),
        ("지번 검색", "ic_parcel_search", "search", (51, 65, 85)),
        ("타당성 보고서", "ic_report_pdf", "doc", BRAND_DARK),
        ("인허가 검증", "ic_legal_pass", "shield", BRAND_GREEN),
        ("리포트 저장", "ic_export_file", "download", (37, 99, 235)),
    ]
    ic_y0 = icon_hdr_y + 34
    ic_w, ic_h = 132, 134
    ic_gx, ic_gy = 10, 12
    for idx, (label, tok, kind, col) in enumerate(icon_specs):
        r, c = idx // 4, idx % 4
        ix = c2_x + 20 + c * (ic_w + ic_gx)
        iy = ic_y0 + r * (ic_h + ic_gy)
        draw.rounded_rectangle([ix, iy, ix + ic_w, iy + ic_h], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([ix + ic_w//2 - 22, iy + 18, ix + ic_w//2 + 22, iy + 62], radius=12, fill=(255, 255, 255), outline=BORDER_LIGHT, width=1)
        _draw_vector_icon(draw, ix + ic_w//2, iy + 40, kind, col)
        draw.text((ix + ic_w//2, iy + 82), label, font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
        draw.text((ix + ic_w//2, iy + 102), tok, font=get_font(8.5, 'medium'), fill=col, anchor='mm')
        draw.text((ix + ic_w//2, iy + 118), "24×24px · 2px", font=get_font(8.5, 'regular'), fill=(148, 163, 184), anchor='mm')

    # COLUMN 3: SPACING, RADIUS & COMPONENT STATES (w=560, x=1260)
    c3_x, c3_w = 1260, 560
    draw.rounded_rectangle([c3_x, card_y, c3_x + c3_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c3_x + 25, cy=card_y + 35, text="FOUNDATION 03 · ATOMIC KIT", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24)
    draw.text((c3_x + 25, card_y + 66), "규격 단위 및 인터랙티브 컴포넌트", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c3_x + 25, card_y + 92), "8-pt 그리드 Spacing, Radius 및 실전 UI 상태 규격", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    t_y = card_y + 124
    sp_x, sp_w = c3_x + 20, 252
    draw.rounded_rectangle([sp_x, t_y, sp_x + sp_w, t_y + 270], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=sp_x + 14, cy=t_y + 20, text="SPACING SCALE (8-PT)", font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
    
    spacings = [
        ("Spacing / 4", "4px", "초밀착 인라인 여백"),
        ("Spacing / 8", "8px", "컴포넌트 내부 패딩 (S)"),
        ("Spacing / 16", "16px", "기본 카드/모듈 패딩 (M)"),
        ("Spacing / 24", "24px", "카드 간격 / 컴포넌트 갭"),
        ("Spacing / 32", "32px", "섹션 그룹 간격 (L)"),
        ("Spacing / 48", "48px", "대형 모듈 외부 여백 (XL)")
    ]
    sy_cur = t_y + 42
    for s_label, s_val, s_desc in spacings:
        draw.text((sp_x + 14, sy_cur + 5), s_label, font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw_pill_badge(draw, left_x=sp_x + sp_w - 56, cy=sy_cur + 11, text=s_val, font=get_font(9.5, 'bold'), theme='blue', pad_x=6, height=16)
        draw.text((sp_x + 14, sy_cur + 21), s_desc, font=get_font(9.5, 'regular'), fill=TEXT_LIGHT_SUB)
        draw.line([(sp_x + 14, sy_cur + 34), (sp_x + sp_w - 14, sy_cur + 34)], fill=(226, 232, 240), width=1)
        sy_cur += 36
        
    rad_x, rad_w = c3_x + 286, 254
    draw.rounded_rectangle([rad_x, t_y, rad_x + rad_w, t_y + 270], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rad_x + 14, cy=t_y + 20, text="RADIUS & STROKE TOKENS", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    
    geom_tokens = [
        ("Radius / Small", "4px", "태그/체크박스/뱃지"),
        ("Radius / Medium", "8px", "버튼/인풋/셀렉트박스"),
        ("Radius / Large", "16px", "카드 컨테이너/모달"),
        ("Radius / Circle", "999px", "원형 아바타/알약형"),
        ("Stroke / Default", "1.0px", "기본 카드 테두리"),
        ("Stroke / Strong", "2.0px", "포커스/활성 테두리")
    ]
    gy_cur = t_y + 42
    for g_label, g_val, g_desc in geom_tokens:
        draw.text((rad_x + 14, gy_cur + 5), g_label, font=get_font(11, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw_pill_badge(draw, left_x=rad_x + rad_w - 60, cy=gy_cur + 11, text=g_val, font=get_font(9.5, 'bold'), theme='green', pad_x=6, height=16)
        draw.text((rad_x + 14, gy_cur + 21), g_desc, font=get_font(9.5, 'regular'), fill=TEXT_LIGHT_SUB)
        draw.line([(rad_x + 14, gy_cur + 34), (rad_x + rad_w - 14, gy_cur + 34)], fill=(226, 232, 240), width=1)
        gy_cur += 36

    comp_y = t_y + 290
    comp_h = card_y + card_h - comp_y - 20
    draw.rounded_rectangle([c3_x + 20, comp_y, c3_x + c3_w - 20, comp_y + comp_h], radius=14, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    bw_cs = draw_pill_badge(draw, left_x=c3_x + 36, cy=comp_y + 26, text="UI COMPONENT KIT", font=get_font(9.5, 'bold'), theme='green', solid=True, pad_x=10, height=22)
    draw.text((c3_x + 36 + bw_cs + 12, comp_y + 26), "실제 앱 적용 인터랙티브 상태 규격", font=get_font(12, 'bold'), fill=BRAND_DARK, anchor='lm')
    
    ex1_y = comp_y + 58
    draw.text((c3_x + 36, ex1_y + 16), "CTA 버튼", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    draw.rounded_rectangle([c3_x + 118, ex1_y, c3_x + 240, ex1_y + 34], radius=8, fill=BRAND_GREEN)
    draw.text((c3_x + 179, ex1_y + 17), "분석 시작 (Default)", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.rounded_rectangle([c3_x + 252, ex1_y, c3_x + 374, ex1_y + 34], radius=8, fill=BRAND_DARK)
    draw.text((c3_x + 313, ex1_y + 17), "분석 시작 (Hover)", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.rounded_rectangle([c3_x + 386, ex1_y, c3_x + 516, ex1_y + 34], radius=8, fill=(226, 232, 240))
    draw.text((c3_x + 451, ex1_y + 17), "선택 대기 (Disabled)", font=get_font(10, 'bold'), fill=(148, 163, 184), anchor='mm')

    ex2_y = ex1_y + 52
    draw.text((c3_x + 36, ex2_y + 16), "규제 뱃지", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    bw_b1 = draw_pill_badge(draw, left_x=c3_x + 118, cy=ex2_y + 16, text="적합 · 개발가능", font=get_font(10, 'bold'), theme='green', pad_x=11, height=28)
    bw_b2 = draw_pill_badge(draw, left_x=c3_x + 118 + bw_b1 + 10, cy=ex2_y + 16, text="조건부 · 심의필요", font=get_font(10, 'bold'), theme='blue', pad_x=11, height=28)
    draw_pill_badge(draw, left_x=c3_x + 118 + bw_b1 + 10 + bw_b2 + 10, cy=ex2_y + 16, text="불가 · 보전지역", font=get_font(10, 'bold'), theme='red', pad_x=11, height=28)

    # Elevation summary strip inside bottom of Component Kit
    ex3_y = ex2_y + 54
    draw.rounded_rectangle([c3_x + 36, ex3_y, c3_x + c3_w - 36, comp_y + comp_h - 18], radius=10, fill=(255, 255, 255), outline=(187, 247, 208), width=1)
    draw.text((c3_x + 50, ex3_y + 20), "4-Tier Elevation & Responsive Grid", font=get_font(11.5, 'bold'), fill=BRAND_DARK)
    draw.text((c3_x + 50, ex3_y + 42), "Desktop 12-Col (1920px) · Mobile 4-Col (390px) · WCAG 2.1 AA 고대비 준수", font=get_font(10, 'regular'), fill=TEXT_LIGHT_SUB)
    draw.text((c3_x + 50, ex3_y + 62), "Elevation-01(Y:2 B:4) · Elevation-02(Y:4 B:12) · Elevation-03(Y:10 B:24)", font=get_font(10, 'medium'), fill=(100, 116, 139))

    draw_slide_footer(draw, 7, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_07.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 08: CORE FEATURE 01 · MULTI-SCREEN LAND ANALYSIS & REPORT
# (Water Calculator Slide 08/09 Multi-Screen Section Structure)
# -------------------------------------------------------------
def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 8, 
        "CORE FEATURE 01 · LAND ANALYSIS", 
        "Simulation Step 1~2 | ", 
        "지번 입력 3초 만에 규제 판정부터 토지 분석 보고서까지 완성", 
        "멀티스크린 실물 연동: [1] GIS 듀얼 스플릿 규제 탐색  |  [2] 원페이지 토지 분석 보고서  |  [3] 모바일 현장 조회 UI", 
        right_badge=("3-SCREEN LIVE FLOW", "green")
    )
    
    card_y = 215
    card_h = 745
    
    # LEFT ZONE: STEP 1 GIS MAP DESKTOP + KEY METRIC (x=100, w=580)
    lx, lw = 100, 580
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_l = draw_pill_badge(draw, left_x=lx + 24, cy=card_y + 34, text="STEP 01 · GIS PARCEL MAP", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24)
    draw.text((lx + 24 + bw_l + 12, card_y + 34), "대상지 규제 탐색 & 지적도 듀얼 뷰", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    step2_desk = os.path.join(ASSETS_DIR, "figma_step2_land_analysis_desktop.png")
    desk_h_used = draw_browser_mockup(img, step2_desk, x=lx + 24, y=card_y + 66, w=lw - 48, h=360, title="STEP 1 · GIS MAP", url="https://farmingsys.io/app/land-map")
    
    # Annotations under Step 1 Desktop
    info_y = card_y + 66 + desk_h_used + 22
    specs_l = [
        ("01. 4대 공적 규제 실시간 파싱", "기본정보·자연환경·토지건물·도시계획 4대 탭으로 100여 개 법령을 3초 만에 판정"),
        ("02. 용도지역 제외면적 자동 필터링", "개발 불가 및 조건부 구역을 체크박스와 컬러 배지로 즉시 분리해 인허가 리스크 차단")
    ]
    for st, sd in specs_l:
        draw.rounded_rectangle([lx + 24, info_y, lx + lw - 24, info_y + 92], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.text((lx + 40, info_y + 18), st, font=get_font(13, 'bold'), fill=BRAND_GREEN)
        lines = wrap_text(sd, get_font(11, 'regular'), lw - 80, draw)
        dy = info_y + 44
        for l in lines[:2]:
            draw.text((lx + 40, dy), l, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 18
        info_y += 104

    # Bottom Metric Strip in Left Zone
    draw.rounded_rectangle([lx + 24, card_y + card_h - 86, lx + lw - 24, card_y + card_h - 22], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    bw_m = draw_pill_badge(draw, left_x=lx + 40, cy=card_y + card_h - 54, text="LEAD TIME -90%", font=get_font(10, 'bold'), theme='green', solid=True, pad_x=10, height=22)
    draw.text((lx + 40 + bw_m + 12, card_y + card_h - 54), "지자체 열람 14일 → 지번 입력 3초 원클릭 분석", font=get_font(12, 'bold'), fill=BRAND_DARK, anchor='lm')

    # CENTER ZONE: HERO LAND ANALYSIS REPORT DESKTOP (x=700, w=530)
    mx, mw = 700, 530
    draw.rounded_rectangle([mx, card_y, mx + mw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_c = draw_pill_badge(draw, left_x=mx + 24, cy=card_y + 34, text="STEP 02 · LAND REPORT", font=get_font(10, 'bold'), theme='blue', pad_x=10, height=24)
    draw.text((mx + 24 + bw_c + 12, card_y + 34), "원페이지 토지 분석 보고서 실물", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    rep_desk = os.path.join(ASSETS_DIR, "figma_step2_land_analysis_report_desktop.jpg")
    rep_im = Image.open(rep_desk)
    target_rep_h = 640
    rep_vp_h = target_rep_h - 34 - 4
    rep_vp_w = int(rep_vp_h * (rep_im.width / rep_im.height))
    tot_rep_w = min(mw - 48, rep_vp_w + 4)
    rep_x = mx + (mw - tot_rep_w) // 2
    draw_browser_mockup(img, rep_desk, x=rep_x, y=card_y + 70, w=tot_rep_w, h=target_rep_h, title="", url="https://farmingsys.io/report/land")

    # RIGHT ZONE: MOBILE FIELD VIEW + ANNOTATED CALLOUTS (x=1250, w=570)
    rx, rw = 1250, 570
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    bw_r = draw_pill_badge(draw, left_x=rx + 24, cy=card_y + 34, text="MOBILE RESPONSIVE", font=get_font(10, 'bold'), theme='green', pad_x=10, height=24)
    draw.text((rx + 24 + bw_r + 12, card_y + 34), "모바일 현장 조회 & 바텀시트 UI", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    
    mob_asset = os.path.join(ASSETS_DIR, "figma_step2_land_analysis_mobile.png")
    draw_phone_mockup(img, mob_asset, cx=rx + 155, cy=card_y + 398, target_h=620, bezel=7, radius=28)
    
    # Right-side callout cards next to Mobile Phone
    ax, aw = rx + 305, rw - 328
    callouts = [
        ("GIS OVERLAY", "위치·면적 지적도", "위성영상과 연속지적도를 오버레이해 총면적(750㎡)과 경계선을 직관 확인"),
        ("6-AXIS AUDIT", "6대 공적장부 종합", "용도지역·지목·경사도·표고·접도조건을 단일 요약 테이블로 자동 정제"),
        ("NET USABLE", "가용 부지 자동 선별", "법적 제한 구역을 제외한 순수 시공 가능 면적을 100% 정밀 분리")
    ]
    ay = card_y + 84
    for badge_t, c_title, c_desc in callouts:
        draw.rounded_rectangle([ax, ay, ax + aw, ay + 186], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw_pill_badge(draw, left_x=ax + 16, cy=ay + 26, text=badge_t, font=get_font(9, 'bold'), theme='green', pad_x=8, height=20)
        draw.text((ax + 16, ay + 52), c_title, font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        lines = wrap_text(c_desc, get_font(10.5, 'regular'), aw - 32, draw)
        dy = ay + 82
        for l in lines[:4]:
            draw.text((ax + 16, dy), l, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)
            dy += 19
        ay += 204

    draw_slide_footer(draw, 8, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_08.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
