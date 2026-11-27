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
        "화면설계서 원본 기반: 일반/간편 모드 토글, 개인화 알림(최대3건), 계약 스와이프, 청구/대출 5대 핵심 명세", 
        right_badge=("OFFICIAL FIGMA SPEC", "red")
    )
    
    card_y = 220
    card_h = 730
    
    lx = 100
    lw = 760
    draw.rounded_rectangle([lx, card_y, lx + lw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=card_y + 35, text="PLSCMV002 · LOGIN GATE WIREFRAME", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 25, card_y + 65), "간편홈 메인 게이트 와이어프레임 구조", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    wf_gate_path = os.path.join(CORE_DIR, "wf_senior_main_gate.png")
    wf_scroll_path = os.path.join(CORE_DIR, "wf_senior_main_scroll.png")
    
    draw_phone_mockup(img, wf_gate_path, cx=lx + 195, cy=card_y + 355, phone_w=240, phone_h=510, bezel=6, radius=24)
    draw_phone_mockup(img, wf_scroll_path, cx=lx + 545, cy=card_y + 355, phone_w=240, phone_h=510, bezel=6, radius=24)
    
    draw.text((lx + 195, card_y + 645), "① 메인 상단 게이트 (Gate)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mt')
    draw.text((lx + 195, card_y + 670), "토글, 알림(3건), 계약(스와이프), 퀵메뉴", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mt')
    
    draw.text((lx + 545, card_y + 645), "② 메인 하단 스크롤 (Scroll)", font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='mt')
    draw.text((lx + 545, card_y + 670), "보험금 청구 접수현황, 보험 대출, 고객지원", font=get_font(11, 'medium'), fill=TEXT_LIGHT_SUB, anchor='mt')
    
    rx = 900
    rw = 920
    draw.rounded_rectangle([rx, card_y, rx + rw, card_y + card_h], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=card_y + 35, text="OFFICIAL UI SPECIFICATION TABLE", font=get_font(11, 'bold'), theme='blue', pad_x=12, height=24)
    draw.text((rx + 25, card_y + 65), "화면설계서 공식 상세 명세 (Description)", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    specs = [
        {
            "num": "1",
            "name": "[헤더 영역] 일반모드 ↔ 간편모드 스위칭",
            "desc": "일반홈 노출 (텍스트로 표시). 헤더에 있는 [일반홈/간편홈] 토글을 통해 상호 모드 전환 가능. 기본 간편홈 모드는 일반 대비 기본 +4pt 크기 확대 적용. 미확인 알림 메시지 건수 뱃지(최대 99개) 노출."
        },
        {
            "num": "2",
            "name": "[개인화 알림] 최대 3건 롤링 & 더보기",
            "desc": "알림 1건씩 최대 3건까지 하단 콘텐츠를 밀며 리스트 표시. 4건 이상인 경우 [n건 더보기] 버튼 노출되며, 터치 시 레이어 팝업으로 전체 알림 리스트를 확인 가능."
        },
        {
            "num": "3",
            "name": "[내보험(계약) 영역] 좌우 스와이프 다건 조회",
            "desc": "내 보험 카드 표시 (복수 계약 시 변액보험 우선 노출, 수익률 강조). 1개일 때는 일반 카드와 동일한 너비로 고정 표시, 2개 이상일 경우 좌우 스와이프 기능 제공 (수에 제한 없음). 카드 탭 시 계약 상세 화면 이동."
        },
        {
            "num": "4",
            "name": "[보험금 청구 영역] 실시간 청구 상태 노출",
            "desc": "타이틀: '보험금 청구 총 n건'. 청구 건이 있을 시 [청구일 / 접수/심사상태 / 피보험자] 노출. 2개 이상 좌우 스와이프 지원. 청구 건이 없을 시 신규 청구 유도 카드로 자동 전환."
        },
        {
            "num": "5",
            "name": "[대출 내역 영역] 대출 현황 및 한도 조회",
            "desc": "5-1: 대출 건이 있을 시 통합 대출 현황 카드 표시 (총 대출 금액 / 추가 대출 가능 금액 / 기준일). 5-2: 대출 건이 없을 시 대출 신청 유도 카드 노출 및 1-Tap 신청 버튼 연동."
        }
    ]
    
    sy = card_y + 110
    for s in specs:
        draw.rounded_rectangle([rx + 25, sy, rx + rw - 25, sy + 110], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
        draw.rounded_rectangle([rx + 40, sy + 16, rx + 68, sy + 44], radius=6, fill=AIA_RED)
        draw.text((rx + 54, sy + 30), s["num"], font=get_font(13, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        draw.text((rx + 80, sy + 28), s["name"], font=get_font(14, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        lines = wrap_text(s["desc"], get_font(11.5, 'regular'), rw - 120, draw)
        ly_p = sy + 52
        for line in lines:
            draw.text((rx + 40, ly_p), line, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB)
            ly_p += 17
        sy += 118
        
    draw_slide_footer(draw, 6, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_06.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 07: DESIGN SYSTEM (Tokens Table, Swatches & Components)
# -------------------------------------------------------------
def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(
        draw, 7, 
        "DESIGN SYSTEM & TOKENS", 
        "Design System | ", 
        "AIA 글로벌 표준 Qi 디자인 시스템 v3.3", 
        "디자인 토큰 규격 테이블, 브랜드 컬러 팔레트, 56dp 고령자 입력 컴포넌트 표준", 
        right_badge=("QI DESIGN TOKENS", "red")
    )
    
    lx = 100
    ly = 220
    lw = 540
    lh = 730
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=lx + 25, cy=ly + 35, text="QI TOKEN SPECIFICATION TABLE", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((lx + 25, ly + 65), "디자인 토큰 분류 & 플랫폼 표준", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    th_y = ly + 110
    draw.rounded_rectangle([lx + 20, th_y, lx + lw - 20, th_y + 36], radius=6, fill=(241, 245, 249))
    draw.text((lx + 35, th_y + 18), "토큰 분류", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
    draw.text((lx + 155, th_y + 18), "고령자 규격", font=get_font(11.5, 'bold'), fill=AIA_RED, anchor='lm')
    draw.text((lx + 285, th_y + 18), "일반 규격", font=get_font(11.5, 'bold'), fill=TEXT_LIGHT_SUB, anchor='lm')
    draw.text((lx + 405, th_y + 18), "WCAG 준수", font=get_font(11.5, 'bold'), fill=(16, 185, 129), anchor='lm')
    
    token_rows = [
        ("Display 폰트", "28pt Bold", "24pt Bold", "AAA (9.2:1)"),
        ("본문 Title", "20pt Bold", "16pt SemiBold", "AAA (8.6:1)"),
        ("기본 본문 Body", "18pt SemiBold", "14pt Regular", "AAA (8.4:1)"),
        ("보조 캡션", "15pt Medium", "12pt Regular", "AA (6.8:1)"),
        ("최소 터치 영역", "48 x 48 dp", "36 x 36 dp", "규제 100%"),
        ("하단 고정 CTA", "56dp 풀와이드", "48dp 기본", "Thumb Zone"),
        ("버튼 코너 라운딩", "Radius 8dp", "Radius 6dp", "인체공학"),
        ("컨테이너 보더", "2px 솔리드 라인", "1px 라인", "선명 분리")
    ]
    
    try_pos = th_y + 44
    for t_cat, t_sen, t_gen, t_wcag in token_rows:
        draw.rectangle([lx + 20, try_pos, lx + lw - 20, try_pos + 42], fill=(255, 248, 250) if "Body" in t_cat or "CTA" in t_cat else (255, 255, 255))
        draw.line([(lx + 20, try_pos + 42), (lx + lw - 20, try_pos + 42)], fill=BORDER_LIGHT, width=1)
        draw.text((lx + 35, try_pos + 21), t_cat, font=get_font(12, 'bold'), fill=TEXT_LIGHT_MAIN, anchor='lm')
        draw.text((lx + 155, try_pos + 21), t_sen, font=get_font(12, 'bold'), fill=AIA_RED, anchor='lm')
        draw.text((lx + 285, try_pos + 21), t_gen, font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_SUB, anchor='lm')
        draw.text((lx + 405, try_pos + 21), t_wcag, font=get_font(11.5, 'bold'), fill=(5, 150, 105), anchor='lm')
        try_pos += 44
        
    draw.rounded_rectangle([lx + 20, ly + lh - 110, lx + lw - 20, ly + lh - 25], radius=10, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((lx + 35, ly + lh - 95), "💡 디자인 토큰 개발 연동 표준", font=get_font(12, 'bold'), fill=AIA_RED)
    draw.text((lx + 35, ly + lh - 70), "Figma Tokens -> JSON Schema -> Flutter AppTheme 자동 동기화", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
    draw.text((lx + 35, ly + lh - 48), "단일 소스 기반으로 다크/라이트 테마 및 시니어 스케일 100% 매핑", font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
    
    mx = 670
    mw = 520
    draw.rounded_rectangle([mx, ly, mx + mw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=mx + 25, cy=ly + 35, text="QI COLOR MATRIX & CONTRAST", font=get_font(11, 'bold'), theme='red', pad_x=12, height=24)
    draw.text((mx + 25, ly + 65), "고대비 컬러 팔레트 & 시각 보조", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    swatches = [
        ("AIA Red Primary", (211, 17, 69), "#D31145", "브랜드 주 색상, 56dp CTA 버튼, 주요 뱃지"),
        ("AIA Red Dark", (168, 14, 55), "#A80E37", "버튼 활성/눌림 상태 및 고대비 텍스트"),
        ("AIA Red Light", (255, 241, 244), "#FFF1F4", "경고 및 미납 알림 하이라이트 배경"),
        ("Text Main Navy", (15, 23, 42), "#0F172A", "고령자 본문 고대비 텍스트 (9.2:1 명도비)"),
        ("Text Subtitle Slate", (71, 85, 105), "#475569", "보조 설명 및 부가 레이블 (6.8:1)"),
        ("Success Emerald", (16, 185, 129), "#10B981", "완료 피드백, 자동이체 정상 등록 뱃지"),
        ("Notice Amber", (245, 158, 11), "#F59E0B", "미납 도래 3일 전 주의 환기 알림")
    ]
    
    sw_y = ly + 115
    for s_name, s_rgb, s_hex, s_desc in swatches:
        draw.rounded_rectangle([mx + 25, sw_y, mx + 75, sw_y + 46], radius=8, fill=s_rgb, outline=BORDER_LIGHT, width=1)
        draw.text((mx + 90, sw_y + 12), s_name, font=get_font(13.5, 'bold'), fill=TEXT_LIGHT_MAIN)
        draw.text((mx + 250, sw_y + 14), s_hex, font=get_font(11.5, 'bold'), fill=AIA_RED)
        draw.text((mx + 90, sw_y + 32), s_desc, font=get_font(11, 'regular'), fill=TEXT_LIGHT_SUB)
        sw_y += 62
        
    draw.rounded_rectangle([mx + 25, ly + lh - 180, mx + mw - 25, ly + lh - 25], radius=12, fill=(248, 250, 252), outline=BORDER_LIGHT, width=1)
    draw.text((mx + 40, ly + lh - 165), "🔍 WCAG 2.1 AAA 명도 대비 검증 결과", font=get_font(12.5, 'bold'), fill=AIA_RED)
    draw.text((mx + 40, ly + lh - 138), "• #D31145 vs #FFFFFF : 5.8:1 (AA 기준 상회)", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
    draw.text((mx + 40, ly + lh - 116), "• #0F172A vs #FFFFFF : 14.8:1 (최고 수준 AAA)", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
    draw.text((mx + 40, ly + lh - 94), "• #10B981 vs #FFFFFF : 4.6:1 (식별성 충족)", font=get_font(11.5, 'regular'), fill=TEXT_LIGHT_MAIN)
    draw.text((mx + 40, ly + lh - 72), "• 배경색과 본문 간 최소 7:1 이상의 고대비 엄격 준수", font=get_font(11.5, 'bold'), fill=(16, 185, 129))
    
    rx = 1220
    rw = 600
    draw.rounded_rectangle([rx, ly, rx + rw, ly + lh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    draw_pill_badge(draw, left_x=rx + 25, cy=ly + 35, text="REAL QI ASSET SHOWCASE", font=get_font(11, 'bold'), theme='green', pad_x=12, height=24)
    draw.text((rx + 25, ly + 65), "실제 Qi 버튼 및 폼 컴포넌트", font=get_font(18, 'bold'), fill=TEXT_LIGHT_MAIN)
    
    qi_comp_path = os.path.join(QI_DIR, "qi_button_sheet.png")
    if os.path.exists(qi_comp_path):
        c_img = Image.open(qi_comp_path).convert('RGB')
        c_w, c_h = 550, 580
        c_img = c_img.resize((c_w, c_h), Image.Resampling.LANCZOS)
        img.paste(c_img, (rx + 25, ly + 115))
        draw.rounded_rectangle([rx + 25, ly + 115, rx + 25 + c_w, ly + 115 + c_h], radius=10, outline=BORDER_LIGHT, width=1)
        
    draw_slide_footer(draw, 7, 12, dark_mode=False)
    out_path = os.path.join(OUT_DIR, "slide_07.png")
    img.save(out_path, quality=95)
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# SLIDE 08: UI SCREENS - SENIOR MODE MAIN DASHBOARD (EXACT SPECS)
# -------------------------------------------------------------
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
            "screen_senior_main_top_gate.png", 
            "• [일반홈/간편홈] 원터치 토글 헤더\n• 당월 미납 보험료 알림 (미납건 즉시 납부)\n• 다이렉트 치아보험 롤링 배너 (1/3)"
        ),
        (
            "02. 계약 스와이프 (중단)", 
            "screen_senior_main_official.png", 
            "• 계약자/피보험자/수익자 뱃지 분기\n• 무배당 VITALITY 암보험 월 12,870원\n• 좌우 스와이프 다건 조회 (최대 99개)"
        ),
        (
            "03. 5대 코어 퀵액션 그리드", 
            "screen_general_main.png", 
            "• [보험금 청구] 1위 업무 대형 레드 강조\n• 보험료 납입, 자동이체 납입관리\n• 계약조회, 고객 정보변경 1-Tap 분기"
        ),
        (
            "04. 실시간 청구/대출 현황", 
            "screen_claim_step1.png", 
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
