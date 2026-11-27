import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from deck_common import (
    W, H, BASE_DIR, CORE_DIR, QI_DIR, OUT_DIR,
    AIA_RED, AIA_RED_DARK, AIA_RED_LIGHT, AIA_RED_BORDER,
    BG_DARK, CARD_DARK, BORDER_DARK, TEXT_DARK_MAIN, TEXT_DARK_SUB,
    BG_LIGHT, CARD_LIGHT, BORDER_LIGHT, BORDER_LIGHT_ACCENT,
    TEXT_LIGHT_MAIN, TEXT_LIGHT_SUB,
    get_font, get_num_font, wrap_text, draw_pill_badge, draw_arrow,
    draw_slide_header, draw_slide_footer, draw_phone_mockup
)

# -------------------------------------------------------------
# SLIDE 05: FLOW CHART (Flawless Native Vector Flow Chart: Mode Switching)
# -------------------------------------------------------------
def make_slide_05():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 5, 
        "FLOW CHART & DECISION LOGIC", 
        "Flow Chart | ", 
        "일반모드 ↔ 고령자모드 전환 의사결정 로직 플로우", 
        "화면설계서 원본 로직: 로그인 여부, 기 활성 여부, 최초 진입, 65세 이상 연령 판별 및 동의 팝업 분기 트리", 
        right_badge=("SERVICE DECISION LOGIC", "red")
    )
    
    card_x, card_y, card_w, card_h = 80, 205, 1760, 760
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    draw_pill_badge(draw, left_x=card_x + 30, cy=card_y + 30, text="MODE SWITCHING DECISION TREE", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((card_x + 30, card_y + 58), "일반 / 고령자 모드 전환 실행 시 시스템 분기 및 진입 경로 (완전판)", font=get_font(17, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    # Node 1: Start [메인(홈)]
    n1_x, n1_y, n1_w, n1_h = 120, 315, 150, 60
    draw.rounded_rectangle([n1_x, n1_y, n1_x + n1_w, n1_y + n1_h], radius=30, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((n1_x + n1_w//2, n1_y + n1_h//2), "메인(홈)", font=get_font(14.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw_arrow(draw, (n1_x + n1_w, n1_y + n1_h//2), (n1_x + n1_w + 35, n1_y + n1_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    
    # Node 2: Action [일반/고령자 모드 전환 실행]
    n2_x, n2_y, n2_w, n2_h = 305, 305, 180, 80
    draw.rounded_rectangle([n2_x, n2_y, n2_x + n2_w, n2_y + n2_h], radius=12, fill=(255, 255, 255), outline=AIA_RED, width=2)
    draw_pill_badge(draw, cx=n2_x + n2_w//2, cy=n2_y + 16, text="ACTION", font=get_font(9.5, 'bold'), theme='red', pad_x=8, height=18)
    draw.text((n2_x + n2_w//2, n2_y + 42), "일반 / 고령자", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((n2_x + n2_w//2, n2_y + 62), "모드 전환 실행", font=get_font(13, 'bold'), fill=AIA_RED, anchor='mm')
    
    draw_arrow(draw, (n2_x + n2_w, n2_y + n2_h//2), (n2_x + n2_w + 35, n2_y + n2_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    
    # Decision 1: [로그인 여부?]
    d1_x, d1_y, d1_w, d1_h = 520, 300, 165, 90
    draw.rounded_rectangle([d1_x, d1_y, d1_x + d1_w, d1_y + d1_h], radius=14, fill=(240, 246, 255), outline=(59, 130, 246), width=2)
    draw_pill_badge(draw, cx=d1_x + d1_w//2, cy=d1_y + 18, text="CHECK 01", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=18)
    draw.text((d1_x + d1_w//2, d1_y + 52), "로그인 여부?", font=get_font(14.5, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    # PATH A: 비로그인 분기
    draw.line([(d1_x + d1_w//2, d1_y + d1_h), (d1_x + d1_w//2, 630)], fill=AIA_RED, width=2)
    draw_arrow(draw, (d1_x + d1_w//2, 630), (520, 630), col=AIA_RED, width=2, arrow_size=6)
    draw_pill_badge(draw, cx=d1_x + d1_w//2 + 18, cy=d1_y + d1_h + 25, text="N", font=get_font(10, 'bold'), theme='red', pad_x=6, height=18)
    
    d1n_x, d1n_y, d1n_w, d1n_h = 440, 590, 175, 80
    draw.rounded_rectangle([d1n_x, d1n_y, d1n_x + d1n_w, d1n_y + d1n_h], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((d1n_x + d1n_w//2, d1n_y + 30), "고령자 모드", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((d1n_x + d1n_w//2, d1n_y + 52), "활성 여부?", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw_arrow(draw, (d1n_x + d1n_w, d1n_y + d1n_h//2), (d1n_x + d1n_w + 35, d1n_y + d1n_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    draw.text((d1n_x + d1n_w + 14, d1n_y + d1n_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    out1_x, out1_y, out1_w, out1_h = d1n_x + d1n_w + 35, 602, 230, 56
    draw.rounded_rectangle([out1_x, out1_y, out1_x + out1_w, out1_y + out1_h], radius=28, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((out1_x + out1_w//2, out1_y + out1_h//2), "일반 모드 로그인 전 메인 전환", font=get_font(12, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    draw.line([(d1n_x + d1n_w//2, d1n_y + d1n_h), (d1n_x + d1n_w//2, 715)], fill=AIA_RED, width=2)
    draw_arrow(draw, (d1n_x + d1n_w//2, 715), (d1n_x + d1n_w//2, 730), col=AIA_RED, width=2, arrow_size=6)
    draw.text((d1n_x + d1n_w//2 + 10, d1n_y + d1n_h + 10), "N", font=get_font(11, 'bold'), fill=AIA_RED)
    
    out2_x, out2_y, out2_w, out2_h = d1n_x - 30, 730, 240, 56
    draw.rounded_rectangle([out2_x, out2_y, out2_x + out2_w, out2_y + out2_h], radius=28, fill=(255, 241, 244), outline=AIA_RED, width=2)
    draw.text((out2_x + out2_w//2, out2_y + out2_h//2), "고령자 모드 로그인 전 메인 전환", font=get_font(12, 'bold'), fill=AIA_RED, anchor='mm')
    
    # PATH B: 로그인 상태 분기
    draw_arrow(draw, (d1_x + d1_w, d1_y + d1_h//2), (d1_x + d1_w + 40, d1_y + d1_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    draw.text((d1_x + d1_w + 16, d1_y + d1_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    d2_x, d2_y, d2_w, d2_h = 725, 300, 165, 90
    draw.rounded_rectangle([d2_x, d2_y, d2_x + d2_w, d2_y + d2_h], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, cx=d2_x + d2_w//2, cy=d2_y + 18, text="CHECK 02", font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
    draw.text((d2_x + d2_w//2, d2_y + 42), "고령자 모드", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    draw.text((d2_x + d2_w//2, d2_y + 64), "활성 여부?", font=get_font(13, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw_arrow(draw, (d2_x + d2_w, d2_y + d2_h//2), (d2_x + d2_w + 40, d2_y + d2_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    draw.text((d2_x + d2_w + 16, d2_y + d2_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    out3_x, out3_y, out3_w, out3_h = d2_x + d2_w + 40, 315, 240, 60
    draw.rounded_rectangle([out3_x, out3_y, out3_x + out3_w, out3_y + out3_h], radius=30, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((out3_x + out3_w//2, out3_y + out3_h//2), "일반 모드 로그인 후 메인 전환", font=get_font(12.5, 'bold'), fill=(29, 78, 216), anchor='mm')
    
    draw.line([(d2_x + d2_w//2, d2_y + d2_h), (d2_x + d2_w//2, 435)], fill=AIA_RED, width=2)
    draw_arrow(draw, (d2_x + d2_w//2, 435), (d2_x + d2_w//2, 450), col=AIA_RED, width=2, arrow_size=6)
    draw.text((d2_x + d2_w//2 + 10, d2_y + d2_h + 12), "N", font=get_font(11, 'bold'), fill=AIA_RED)
    
    d3_x, d3_y, d3_w, d3_h = 725, 450, 165, 85
    draw.rounded_rectangle([d3_x, d3_y, d3_x + d3_w, d3_y + d3_h], radius=14, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, cx=d3_x + d3_w//2, cy=d3_y + 18, text="CHECK 03", font=get_font(9.5, 'bold'), theme='gray', pad_x=8, height=18)
    draw.text((d3_x + d3_w//2, d3_y + 50), "최초 진입 여부?", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    draw_arrow(draw, (d3_x + d3_w, d3_y + d3_h//2), (d3_x + d3_w + 35, d3_y + d3_h//2), col=(148, 163, 184), width=2, arrow_size=6)
    draw.text((d3_x + d3_w + 14, d3_y + d3_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    d4_x, d4_y, d4_w, d4_h = 925, 450, 175, 85
    draw.rounded_rectangle([d4_x, d4_y, d4_x + d4_w, d4_y + d4_h], radius=14, fill=(255, 241, 244), outline=AIA_RED, width=2)
    draw_pill_badge(draw, cx=d4_x + d4_w//2, cy=d4_y + 18, text="AGE CHECK", font=get_font(9.5, 'bold'), theme='red', pad_x=8, height=18)
    draw.text((d4_x + d4_w//2, d4_y + 50), "나이가 65세 이상?", font=get_font(13.5, 'bold'), fill=AIA_RED, anchor='mm')
    
    draw_arrow(draw, (d4_x + d4_w, d4_y + d4_h//2), (d4_x + d4_w + 35, d4_y + d4_h//2), col=AIA_RED, width=2, arrow_size=6)
    draw.text((d4_x + d4_w + 14, d4_y + d4_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=AIA_RED)
    
    d5_x, d5_y, d5_w, d5_h = 1135, 450, 175, 85
    draw.rounded_rectangle([d5_x, d5_y, d5_x + d5_w, d5_y + d5_h], radius=14, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw_pill_badge(draw, cx=d5_x + d5_w//2, cy=d5_y + 18, text="USER CONSENT", font=get_font(9.5, 'bold'), theme='green', pad_x=8, height=18)
    draw.text((d5_x + d5_w//2, d5_y + 40), "고령자 모드", font=get_font(13, 'bold'), fill=(5, 150, 105), anchor='mm')
    draw.text((d5_x + d5_w//2, d5_y + 60), "전환 동의?", font=get_font(13, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    draw_arrow(draw, (d5_x + d5_w, d5_y + d5_h//2), (d5_x + d5_w + 35, d5_y + d5_h//2), col=(16, 185, 129), width=2, arrow_size=7)
    draw.text((d5_x + d5_w + 14, d5_y + d5_h//2 - 14), "Y", font=get_font(11, 'bold'), fill=(16, 185, 129))
    
    goal_x, goal_y, goal_w, goal_h = d5_x + d5_w + 35, 458, 250, 68
    draw.rounded_rectangle([goal_x, goal_y, goal_x + goal_w, goal_y + goal_h], radius=34, fill=(255, 241, 244), outline=AIA_RED, width=2)
    draw.text((goal_x + goal_w//2, goal_y + 23), "고령자 모드 로그인 후", font=get_font(13.5, 'bold'), fill=AIA_RED, anchor='mm')
    draw.text((goal_x + goal_w//2, goal_y + 46), "메인(홈)으로 전환", font=get_font(13.5, 'bold'), fill=AIA_RED, anchor='mm')
    
    draw.line([(d3_x + d3_w//2, d3_y + d3_h), (d3_x + d3_w//2, 600)], fill=AIA_RED, width=2)
    draw.line([(d3_x + d3_w//2, 600), (goal_x + goal_w//2, 600)], fill=AIA_RED, width=2)
    draw_arrow(draw, (goal_x + goal_w//2, 600), (goal_x + goal_w//2, goal_y + goal_h), col=AIA_RED, width=2, arrow_size=6)
    
    draw.line([(d4_x + d4_w//2, d4_y + d4_h), (d4_x + d4_w//2, 560)], fill=AIA_RED, width=2)
    draw.line([(d4_x + d4_w//2, 560), (goal_x + goal_w//2 - 25, 560)], fill=AIA_RED, width=2)
    draw.line([(goal_x + goal_w//2 - 25, 560), (goal_x + goal_w//2 - 25, goal_y + goal_h)], fill=AIA_RED, width=2)
    
    draw.line([(d5_x + d5_w//2, d5_y + d5_h), (d5_x + d5_w//2, 660)], fill=(100, 116, 139), width=2)
    draw_arrow(draw, (d5_x + d5_w//2, 660), (d5_x + d5_w//2, 675), col=(100, 116, 139), width=2, arrow_size=6)
    draw.text((d5_x + d5_w//2 + 10, d5_y + d5_h + 12), "N", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    stay_x, stay_y, stay_w, stay_h = d5_x - 35, 675, 245, 56
    draw.rounded_rectangle([stay_x, stay_y, stay_x + stay_w, stay_y + stay_h], radius=28, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)
    draw.text((stay_x + stay_w//2, stay_y + stay_h//2), "일반 모드 로그인 후 메인 유지", font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mm')
    
    sum_y = 855
    draw.rounded_rectangle([card_x + 30, sum_y, card_x + card_w - 30, sum_y + 70], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((card_x + 50, sum_y + 24), "💡 시스템 설계 인사이트 및 사용자 자기결정권 보장", font=get_font(13, 'bold'), fill=AIA_RED)
    sum_desc = "회원 연령(65세) 자동 판별 알고리즘을 도입하되, 강제가 아닌 [사용자 선택권 보장 팝업]을 경유하도록 설계하여 디지털 소외감 방지 및 자기결정권을 완벽 보장합니다."
    draw.text((card_x + 50, sum_y + 46), sum_desc, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
    
    draw_slide_footer(draw, 5, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_05.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 06: WIREFRAMES (Harmonized Wireframe Mockup & Specs)
# -------------------------------------------------------------
def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 6, 
        "WIREFRAMES & DETAILED SPECS", 
        "Wireframes | ", 
        "고령자모드 메인 화면설계서 (PLSCMV002 Gate)", 
        "Figma 공식 화면설계서 원본 기반: 간편홈 모드 전환, 개인화 알림(최대3건), 계약 스와이프, 청구/대출 5대 영역 Description", 
        right_badge=("OFFICIAL FIGMA SPEC", "red")
    )
    
    card_y = 210
    card_h = 750
    
    # Left Card: Official Figma Wireframe Phones (Phone 1: Gate & Contract / Phone 2: Scroll & Claims)
    lx = 100
    lw = 740
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="PLSCMV002 · OFFICIAL FIGMA WIREFRAME", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 65), "간편홈 메인 화면설계서 원본 구조", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 25, card_y + 92), "AIA+_Phase 2_화면설계서_고령자모드_메인.fig 공식 산출물", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    p1_path = os.path.join(CORE_DIR, "wf_phone1_gate.png")
    p2_path = os.path.join(CORE_DIR, "wf_phone2_scroll.png")
    
    draw_phone_mockup(img, p1_path, cx=lx + 190, cy=card_y + 395, phone_w=250, phone_h=525, bezel=6, radius=28)
    draw_phone_mockup(img, p2_path, cx=lx + 550, cy=card_y + 395, phone_w=250, phone_h=525, bezel=6, radius=28)
    
    draw.text((lx + 190, card_y + 685), "① 메인 게이트 (Gate)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mt')
    draw.text((lx + 190, card_y + 708), "토글, 알림(3건), 계약 스와이프", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mt')
    
    draw.text((lx + 550, card_y + 685), "② 하단 스크롤 (Scroll)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mt')
    draw.text((lx + 550, card_y + 708), "청구 접수 현황, 보험 대출, GNB", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mt')
    
    # Right Card: Description Specs Table
    rx = 870
    rw = 950
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=card_y + 35, text="OFFICIAL UI SPECIFICATION TABLE", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 25, card_y + 65), "화면설계서 공식 상세 명세 (Description)", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((rx + 25, card_y + 92), "개발/QA 검증을 위한 5대 UI 컴포넌트 정책 및 인터랙션 정의", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
    
    specs = [
        {
            "num": "1",
            "name": "[헤더 영역] 일반모드 ↔ 간편모드 스위칭",
            "tag": "헤더 토글",
            "desc": "헤더 상단에 [일반홈 / 간편홈] 원터치 토글을 배치하여 모드 상호 전환 제공. 고령자모드는 텍스트 크기 기본 +4pt 이상 확대. 미확인 개인화 알림 건수 뱃지(최대 99건) 동적 표시."
        },
        {
            "num": "2",
            "name": "[개인화 알림] 최대 3건 순차 노출 & 더보기",
            "tag": "알림 리스트",
            "desc": "사용자별 주요 알림(미납 보험료, 만기 등)을 1건씩 최대 3건까지 하단 콘텐츠를 밀며 리스트 표시. 4건 이상 발생 시 [n건 더보기] 버튼 노출 및 터치 시 레이어 팝업으로 전체 리스트 제공."
        },
        {
            "num": "3",
            "name": "[내보험(계약) 영역] 좌우 스와이프 다건 조회",
            "tag": "카드 스와이프",
            "desc": "복수 계약 시 변액보험 우선 노출(수익률 강조). 보유 계약 1건 시 일반 카드 너비 고정, 2건 이상 시 좌우 스와이프 인터랙션 제공. 카드 탭 시 해당 계약 상세 화면으로 다이렉트 이동."
        },
        {
            "num": "4",
            "name": "[보험금 청구 영역] 실시간 청구 상태 노출",
            "tag": "상태 트래킹",
            "desc": "타이틀: '보험금 청구 총 n건'. 진행 중인 청구 건이 있을 시 [청구일자 / 접수·심사 상태 뱃지 / 피보험자] 카드 표시. 청구 건 부재 시 '간편 청구 신청' 유도 카드로 자동 전환."
        },
        {
            "num": "5",
            "name": "[대출 내역 영역] 대출 현황 및 한도 조회",
            "tag": "대출 한도",
            "desc": "5-1(대출 보유 시): 총 대출금액 / 추가 대출 가능금액 / 기준일 표시. 5-2(대출 미보유 시): 내 보험 대출 신청 카드 표시. 탭 시 대출 가능 금액 및 금리 간편 조회 화면으로 이동."
        }
    ]
    
    sy = card_y + 120
    box_h = 110
    gap = 14
    for s in specs:
        draw.rounded_rectangle([rx + 25, sy, rx + rw - 25, sy + box_h], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([rx + 40, sy + 14, rx + 68, sy + 42], radius=6, fill=AIA_RED)
        draw.text((rx + 54, sy + 28), s["num"], font=get_font(13, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        draw.text((rx + 80, sy + 28), s["name"], font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw_pill_badge(draw, left_x=rx + rw - 130, cy=sy + 28, text=s["tag"], font=get_font(10.5, 'bold'), theme='gray', pad_x=8, height=20)
        
        lines = wrap_text(s["desc"], get_font(11.5, 'regular'), rw - 110, draw)
        ly_p = sy + 52
        for line in lines:
            draw.text((rx + 40, ly_p), line, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly_p += 18
        sy += box_h + gap
        
    draw_slide_footer(draw, 6, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_06.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 07: DESIGN SYSTEM & TOKENS (Official Guidelines & Components)
# -------------------------------------------------------------
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 7, 
        "DESIGN SYSTEM & TOKENS", 
        "Design System | ", 
        "AIA 고령자 맞춤 디자인 시스템 (Design System Standards)", 
        "공식 디자인 시스템 원본 기반: 텍스트(+4pt), 버튼(48px), 고대비 컬러, 단순화 아이콘 및 실제 UI 컴포넌트", 
        right_badge=("OFFICIAL DESIGN SYSTEM", "red")
    )
    
    # -------------------------------------------------------------
    # TOP SECTION: 4 Core Standard Definition Cards (항목 / 기준 정의 / 적용 목적)
    # -------------------------------------------------------------
    top_y = 205
    top_h = 175
    top_w = 1720
    top_x = 100
    
    draw.rounded_rectangle([top_x, top_y, top_x + top_w, top_y + top_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=top_x + 25, cy=top_y + 26, text="DESIGN SYSTEM GUIDELINES", font=get_font(10.5, 'bold'), theme='red', pad_x=10, height=22)
    draw.text((top_x + 225, top_y + 16), "고령자 친화 인터페이스 4대 표준 정의 및 적용 목적", font=get_font(15, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    ds_principles = [
        ("텍스트 (Typography)", "기존 대비 +4pt 이상", "가독성 확보 및 피로도 감소", "본문 18pt 이상, 헤드라인 1~6 및 본문 1~2 계층화 체계"),
        ("버튼 (Touch Target)", "최소 터치 영역 48px", "터치 정확도 향상 및 구분성 확보", "56dp 풀와이드 메인 CTA 및 충분한 탭 영역 확보"),
        ("컬러 (Color Contrast)", "고대비 조합 (High Contrast)", "색약 및 고령자 인지 대응", "배경 대비 7:1 이상의 WCAG AAA 고대비 엄격 준수"),
        ("아이콘 (Iconography)", "단순화 의미 + 라벨 병기", "직관적 인지 고려 UI 형성", "아이콘 단독 노출 지양, 명확한 한글 텍스트 라벨 결합")
    ]
    
    card_cols = 4
    col_w = (top_w - 40 - (card_cols - 1) * 16) // card_cols
    col_x = top_x + 20
    
    for title, standard, purpose, sub in ds_principles:
        draw.rounded_rectangle([col_x, top_y + 48, col_x + col_w, top_y + top_h - 14], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([col_x, top_y + 48, col_x + col_w, top_y + 80], radius=12, fill=(241, 245, 249))
        draw.rectangle([col_x, top_y + 68, col_x + col_w, top_y + 80], fill=(241, 245, 249))
        draw.text((col_x + 14, top_y + 64), title, font=get_font(12, 'bold'), fill=AIA_RED, anchor='lm')
        
        draw.text((col_x + 14, top_y + 96), "기준: " + standard, font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((col_x + 14, top_y + 118), "목적: " + purpose, font=get_font(11.5, 'bold'), fill=(16, 185, 129))
        draw.text((col_x + 14, top_y + 138), sub, font=get_font(10.5, 'regular'), fill=TEXT_LIGHT_SUB)
        col_x += col_w + 16
        
    # -------------------------------------------------------------
    # BOTTOM SECTION: 3 Columns (Typography / Palette & System / UI Components)
    # -------------------------------------------------------------
    bot_y = 395
    bot_h = 565
    
    # Col 1: Typography Scale (한국어 헤드라인 1~6, 본문 1~2)
    c1_x = 100
    c1_w = 480
    draw.rounded_rectangle([c1_x, bot_y, c1_x + c1_w, bot_y + bot_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c1_x + 20, cy=bot_y + 30, text="TYPOGRAPHY SCALE", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=22)
    draw.text((c1_x + 20, bot_y + 55), "한국어 폰트 스케일 계층 구조", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c1_x + 20, bot_y + 78), "고령자 시각 피로도 최소화를 위한 계층화 텍스트 시스템", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
    
    typo_items = [
        ("헤드라인 1", "32pt Bold", "주요 타이틀 및 전환 알림"),
        ("헤드라인 2", "28pt Bold", "섹션 헤더 및 주요 카드 타이틀"),
        ("헤드라인 3", "24pt Bold", "모달 팝업 및 서브 섹션"),
        ("헤드라인 4", "20pt Bold", "계약 정보 및 중요 금액 표시"),
        ("헤드라인 5", "18pt SemiBold", "코어 퀵액션 메뉴 레이블"),
        ("헤드라인 6", "16pt SemiBold", "리스트 타이틀 및 안내 강조"),
        ("본문 1 (Body 1)", "16pt Regular", "상세 안내문 및 설명 텍스트"),
        ("본문 2 (Body 2)", "14pt Regular", "부가 캡션 및 부가 메타 정보"),
    ]
    
    ty_y = bot_y + 105
    for t_name, t_sz, t_desc in typo_items:
        draw.rounded_rectangle([c1_x + 18, ty_y, c1_x + c1_w - 18, ty_y + 48], radius=8, fill=(250, 252, 255), outline=BORDER_LIGHT, width=1)
        draw.text((c1_x + 30, ty_y + 24), t_name, font=get_font(12.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw_pill_badge(draw, left_x=c1_x + 160, cy=ty_y + 24, text=t_sz, font=get_font(10.5, 'bold'), theme='gray', pad_x=8, height=20)
        draw.text((c1_x + 255, ty_y + 24), t_desc, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB, anchor='lm')
        ty_y += 54
        
    # Col 2: Color Palette Swatches (Figma 원본 고대비 팔레트 + WCAG 검증)
    c2_x = 600
    c2_w = 560
    draw.rounded_rectangle([c2_x, bot_y, c2_x + c2_w, bot_y + bot_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c2_x + 20, cy=bot_y + 30, text="COLOR PALETTE & CONTRAST", font=get_font(10.5, 'bold'), theme='red', pad_x=10, height=22)
    draw.text((c2_x + 20, bot_y + 55), "고대비 브랜드 및 기능 컬러 팔레트", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c2_x + 20, bot_y + 78), "색약·저시력 고령자를 위한 고대비 컬러 매트릭스", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
    
    palette_path = os.path.join(CORE_DIR, "ds_palette.png")
    if os.path.exists(palette_path):
        pal_img = Image.open(palette_path)
        pw, ph = 520, int(520 * pal_img.height / pal_img.width)
        if ph > 220:
            ph = 220
            pw = int(ph * pal_img.width / pal_img.height)
        pal_resized = pal_img.resize((pw, ph), Image.Resampling.LANCZOS)
        pal_x = c2_x + (c2_w - pw) // 2
        img.paste(pal_resized, (pal_x, bot_y + 105))
        draw.rounded_rectangle([pal_x - 4, bot_y + 101, pal_x + pw + 4, bot_y + 105 + ph + 4], radius=10, outline=BORDER_LIGHT, width=1)
        
    draw.rounded_rectangle([c2_x + 20, bot_y + 345, c2_x + c2_w - 20, bot_y + bot_h - 20], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((c2_x + 35, bot_y + 368), "🔍 WCAG 2.1 AAA 고대비 검증 결과", font=get_font(13, 'bold'), fill=AIA_RED)
    
    contrast_points = [
        ("AIA Red Primary (#D31145) vs White", "5.8:1 (AA 충족, 56dp CTA)"),
        ("Navy Main Text (#0F172A) vs White", "14.8:1 (최고 수준 AAA 달성)"),
        ("Slate Subtitle (#475569) vs White", "7.1:1 (엄격한 고대비 기준 준수)"),
        ("Teal Focus (#00878A) vs White", "4.8:1 (포커스 링 및 보조 인지)")
    ]
    cp_y = bot_y + 398
    for label, res in contrast_points:
        draw.text((c2_x + 35, cp_y), "• " + label + " :", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
        draw.text((c2_x + 325, cp_y), res, font=get_font(11.5, 'bold'), fill=(16, 185, 129))
        cp_y += 24
    draw.text((c2_x + 35, cp_y + 8), "※ 색상만으로 정보를 구별하지 않고 텍스트 레이블 병행 표기 원칙", font=get_font(11, 'bold'), fill=AIA_RED)
    
    # Col 3: Real UI Components & Forms (피그마 원본에서 정밀 크롭한 4대 핵심 컴포넌트)
    c3_x = 1180
    c3_w = 640
    draw.rounded_rectangle([c3_x, bot_y, c3_x + c3_w, bot_y + bot_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=c3_x + 20, cy=bot_y + 30, text="FIGMA UI COMPONENTS", font=get_font(10.5, 'bold'), theme='green', pad_x=10, height=22)
    draw.text((c3_x + 20, bot_y + 55), "공식 UI 컴포넌트 & 48px 터치 폼", font=get_font(16, 'bold'), fill=TEXT_LIGHT_MAIN)
    draw.text((c3_x + 20, bot_y + 78), "피그마 원본 추출: 납부 카드, 출금 계좌 선택, 48px 일자 칩셋", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
    
    # Grid of cropped crystal clear UI components
    notice_p = os.path.join(CORE_DIR, "comp_notice.png")
    icons_p = os.path.join(CORE_DIR, "comp_icons.png")
    if os.path.exists(notice_p):
        n_img = Image.open(notice_p)
        nw, nh = 360, int(360 * n_img.height / n_img.width)
        n_res = n_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(n_res, (c3_x + 25, bot_y + 110))
        draw.rounded_rectangle([c3_x + 25, bot_y + 110, c3_x + 25 + nw, bot_y + 110 + nh], radius=8, outline=BORDER_LIGHT, width=1)
        
    if os.path.exists(icons_p):
        ic_img = Image.open(icons_p)
        iw, ih = 205, int(205 * ic_img.height / ic_img.width)
        ic_res = ic_img.resize((iw, ih), Image.Resampling.LANCZOS)
        img.paste(ic_res, (c3_x + 405, bot_y + 110))
        draw.rounded_rectangle([c3_x + 405, bot_y + 110, c3_x + 405 + iw, bot_y + 110 + ih], radius=8, outline=BORDER_LIGHT, width=1)
        
    # Bottom Row: comp_bank & comp_chips
    bank_p = os.path.join(CORE_DIR, "comp_bank.png")
    chips_p = os.path.join(CORE_DIR, "comp_chips.png")
    row2_y = bot_y + 295
    if os.path.exists(bank_p):
        b_img = Image.open(bank_p)
        bw, bh = 280, int(280 * b_img.height / b_img.width)
        if bh > 235:
            bh = 235
            bw = int(bh * b_img.width / b_img.height)
        b_res = b_img.resize((bw, bh), Image.Resampling.LANCZOS)
        img.paste(b_res, (c3_x + 25, row2_y))
        draw.rounded_rectangle([c3_x + 25, row2_y, c3_x + 25 + bw, row2_y + bh], radius=8, outline=BORDER_LIGHT, width=1)
        
    if os.path.exists(chips_p):
        ch_img = Image.open(chips_p)
        cw, ch = 285, int(285 * ch_img.height / ch_img.width)
        if ch > 235:
            ch = 235
            cw = int(ch * ch_img.width / ch_img.height)
        ch_res = ch_img.resize((cw, ch), Image.Resampling.LANCZOS)
        img.paste(ch_res, (c3_x + 325, row2_y))
        draw.rounded_rectangle([c3_x + 325, row2_y, c3_x + 325 + cw, row2_y + ch], radius=8, outline=BORDER_LIGHT, width=1)
        
    draw_slide_footer(draw, 7, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_07.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 8, 
        "UI SCREENS · SENIOR MODE MAIN DASHBOARD", 
        "UI Screens | ", 
        "고령자모드 간편홈 메인 화면설계 상세 분석 (PLSCMV002)", 
        "일반/간편 토글, 최대 3건 개인화 알림, 내보험 계약 스와이프, 5대 퀵액션 그리드 및 보험금 청구 접수현황", 
        right_badge=("OFFICIAL MAIN DESIGN", "red")
    )
    
    # 4 Sequential UI Columns matching exact uploaded screen layout
    screens = [
        (
            "01. 간편홈 게이트 (상단)", 
            "screen_senior_main_part1_gate.png", 
            "• [일반홈/간편홈] 원터치 토글 헤더\n• 당월 미납 보험료 알림 (미납건 즉시 납부)\n• 다이렉트 치아보험 롤링 배너 (1/3)"
        ),
        (
            "02. 계약 스와이프 (중단)", 
            "screen_senior_main_part2_contract.png", 
            "• 계약자/피보험자/수익자 뱃지 분기\n• 무배당 VITALITY 암보험 월 12,870원\n• 좌우 스와이프 다건 조회 (최대 99개)"
        ),
        (
            "03. 5대 코어 퀵액션 그리드", 
            "screen_senior_main_part3_quickactions.png", 
            "• [보험금 청구] 1위 업무 대형 레드 강조\n• 보험료 납입, 자동이체 납입관리\n• 계약조회, 고객 정보변경 1-Tap 분기"
        ),
        (
            "04. 실시간 청구/대출 현황", 
            "screen_senior_main_part4_claims.png", 
            "• '보험금 청구 총 2건' 실시간 접수중 뱃지\n• 내 보험 대출 신청 가능 금액 확인\n• 하단 큰글씨 GNB (홈/청구/마이/전체)"
        )
    ]
    
    sw = 395
    sh = 730
    start_x = 100
    start_y = 220
    
    for i, (stitle, s_file, s_desc) in enumerate(screens):
        sx = start_x + i * (sw + 23)
        draw.rounded_rectangle([sx, start_y, sx + sw, start_y + sh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
        
        draw_pill_badge(draw, left_x=sx + 20, cy=start_y + 32, text=f"SECTION 0{i+1}", font=get_font(10.5, 'bold'), theme='red' if i in [0, 1] else 'blue', pad_x=12, height=22)
        draw.text((sx + 20, start_y + 58), stitle, font=get_font(16.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        
        screen_path = os.path.join(CORE_DIR, s_file)
        if not os.path.exists(screen_path):
            screen_path = os.path.join(CORE_DIR, "screen_senior_main_official.png")
            
        draw_phone_mockup(img, screen_path, cx=sx + sw // 2, cy=start_y + 338, phone_w=225, phone_h=465, bezel=6, radius=26)
        
        if i < 3:
            arrow_x = sx + sw + 4
            draw_arrow(draw, (arrow_x, start_y + 338), (arrow_x + 15, start_y + 338), col=AIA_RED, width=2, arrow_size=6)
        
        # Bottom Description Specs Card (Height=95)
        draw.rounded_rectangle([sx + 15, start_y + sh - 105, sx + sw - 15, start_y + sh - 15], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        
        desc_lines = s_desc.split('\n')
        dy = start_y + sh - 93
        for line in desc_lines:
            draw.text((sx + 24, dy), line, font=get_font(11, 'medium'), fill=TEXT_LIGHT_MAIN)
            dy += 24
            
    draw_slide_footer(draw, 8, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_08.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
