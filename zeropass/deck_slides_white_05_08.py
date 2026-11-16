"""
ZeroPass Behance Deck Slides 05 - 08 (White Minimal Clean Enterprise Aesthetic)
Senior PRD Architecture Standard:
- Slide 05: 5-Stage Interactive User Flowchart with Decision Diamonds, Recovery Loops, and Guard Containers
- Slide 06: 4 Expanded 19.5:9 Smartphone Wireframes with Dynamic Island, Thumb-Zone Arc & PRD Callout Anchor Pins
- Slide 07: Visual Identity & Design System (Foundations, App Icon Keyline Drafting Blueprint, 24dp Iconography, Tokens & Component Kit)
- Slide 08: Core Feature Deep Dive 01 - 0.8s One-Touch Kiosk Attendance Engine
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from build_zeropass_white_common import (
    W, H, FONT_DIR, MOCKUP_DIR, OUT_DIRS,
    C_BLUE_HERO, C_CYAN_ACCENT, C_TITLE_BLACK, C_TEXT_BODY, C_TEXT_MUTED,
    C_BG_CARD, C_BORDER_LINE, C_BG_CONTAINER,
    get_font, get_num_font, draw_pill_badge, draw_slide_header, draw_slide_footer,
    wrap_text_by_words, save_slide,
    draw_diamond, draw_arrow, draw_dashed_line, draw_dashed_arrow
)

FLUTTER_MATERIAL_FONT = r"C:\flutter\bin\cache\artifacts\material_fonts\MaterialIcons-Regular.otf"

def get_material_icon_font(size):
    if os.path.exists(FLUTTER_MATERIAL_FONT):
        try:
            return ImageFont.truetype(FLUTTER_MATERIAL_FONT, int(round(size)))
        except:
            pass
    return get_font(size, 'bold')

def make_shadow(img, blur=44, offset=(22, 40), alpha=80):
    sh = Image.new('RGBA', (img.width + blur * 4, img.height + blur * 4), (0, 0, 0, 0))
    shd = ImageDraw.Draw(sh)
    pad = (blur * 2, blur * 2)
    shd.rounded_rectangle(
        [pad[0] + offset[0], pad[1] + offset[1],
         pad[0] + offset[0] + img.width, pad[1] + offset[1] + img.height],
        radius=28, fill=(15, 23, 42, alpha)
    )
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    return sh, pad


# ==============================================================
# SLIDE 05: 5-STAGE USER FLOWCHART (PRD ENTERPRISE STANDARD)
# ==============================================================
def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=5, 
        category_en="USER FLOW | SERVICE INTERACTION FLOWCHART", 
        title_black="사용자 행동과 판단을 이끄는 ", 
        title_blue="5단계 서비스 UX 플로우차트", 
        subtitle_kr="원생 등원 인증부터 로컬 트랜잭션 차감, D-Day 수납 정렬, 카카오톡 청구서 발송 및 데이터 동기화까지의 핵심 여정"
    )
    
    # Top-Right Legend: Diagram Notation (w=540, h=78)
    leg_x = 1280
    leg_y = 65
    leg_w = 540
    leg_h = 78
    draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=leg_x + 16, cy=leg_y + 20, text="NOTATION", font=get_font(8, 'bold'), theme='blue', has_dot=True, pad_x=6, height=18)
    draw.text((leg_x + 105, leg_y + 20), "플로우차트 기호 범례", font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # 4 compact legend items
    draw.rounded_rectangle([leg_x + 16, leg_y + 44, leg_x + 70, leg_y + 68], radius=10, fill=(0, 82, 255))
    draw.text((leg_x + 43, leg_y + 56), "Start/End", font=get_font(7, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((leg_x + 76, leg_y + 56), "시작/종료", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 142, leg_y + 44, leg_x + 192, leg_y + 68], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 167, leg_y + 56), "Screen", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((leg_x + 198, leg_y + 56), "화면/접점", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 268, leg_y + 44, leg_x + 318, leg_y + 68], radius=4, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw.text((leg_x + 293, leg_y + 56), "Action", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    draw.text((leg_x + 325, leg_y + 56), "사용자 행동", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw_diamond(draw, cx=leg_x + 410, cy=leg_y + 56, w=34, h=22, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw.text((leg_x + 410, leg_y + 56), "Decide", font=get_font(6.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((leg_x + 434, leg_y + 56), "판단 분기", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    # 5 STAGE COLUMNS
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    col_centers = [cx + cw // 2 for cx in cols_x]
    
    stages_info = [
        ("STAGE 01", "키오스크 등원 인증", "0.8s Quick Attendance"),
        ("STAGE 02", "로컬 DB 트랜잭션", "SQLite Atomic Commit"),
        ("STAGE 03", "수납 장부 D-Day", "Ledger Auto Sorting"),
        ("STAGE 04", "원클릭 청구서 발송", "Kakao Notification"),
        ("STAGE 05", "보안 볼트 & 백업", "Local Vault & Sync")
    ]
    
    # Stage Headers
    for i, (st_code, st_name, st_en) in enumerate(stages_info):
        cx = cols_x[i]
        draw.rounded_rectangle([cx, 234, cx + cw, 284], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw_pill_badge(draw, left_x=cx + 16, cy=249, text=st_code, font=get_font(7.5, 'bold'), theme='blue', pad_x=5, height=16)
        draw.text((cx + 86, 249), st_name, font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((cx + 16, 269), st_en, font=get_font(8.5, 'medium'), fill=(100, 116, 139), anchor='lm')
        
        if i < 4:
            arrow_start_x = cx + cw
            arrow_end_x = cols_x[i + 1]
            draw_arrow(draw, (arrow_start_x + 2, 259), (arrow_end_x - 2, 259), col=(0, 82, 255), width=2, arrow_size=4)
            
    nw = 260
    
    # =============================================================
    # DIAGRAM TRACK 1: STAGE 01 (Center: 264)
    # =============================================================
    c0 = col_centers[0]
    
    # 1. Start Capsule
    draw.rounded_rectangle([c0 - 75, 300, c0 + 75, 328], radius=14, fill=(0, 82, 255))
    draw.text((c0, 314), "Start : 등원 키오스크", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw_arrow(draw, (c0, 328), (c0, 344), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Screen: 번호 다이얼 화면
    draw.rounded_rectangle([c0 - nw // 2, 344, c0 + nw // 2, 388], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=358, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c0 - 54, 358), "출결 다이얼 & 대기 화면", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c0, 375), "80dp 대형 텐키패드 및 실시간 시계 표시", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c0, 388), (c0, 406), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 3. Decision Diamond: 전화번호 뒷 4자리 일치?
    draw_diamond(draw, cx=c0, cy=432, w=176, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c0, 432), "원생 번호 매칭 여부?", font=get_font(9.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    
    # Branch No (Right -> Unmatched loop)
    draw_dashed_line(draw, (c0 + 88, 432), (cols_x[0] + cw - 16, 432), col=(244, 63, 94), width=1)
    draw.text(((c0 + 88 + cols_x[0] + cw - 16) // 2, 422), "No (미등록)", font=get_font(7.5, 'bold'), fill=(220, 38, 38), anchor='mm')
    draw_dashed_arrow(draw, (cols_x[0] + cw - 16, 432), (cols_x[0] + cw - 16, 464), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[0] + cw - 88, 464, cols_x[0] + cw - 6, 496], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[0] + cw - 47, 475), "미등록 안내 팝업", font=get_font(7.5, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw.text((cols_x[0] + cw - 47, 486), "데스크 문의 유도", font=get_font(7, 'medium'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[0] + cw - 47, 496), (cols_x[0] + cw - 47, 524), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[0] + cw - 47, 524), (c0 + nw // 2, 524), col=(244, 63, 94), width=1, arrow_size=3)
    
    # Branch Yes (Straight down -> Member Select)
    draw_arrow(draw, (c0, 458), (c0, 502), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c0 - 30, 480), "Yes (매칭)", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 4. Screen: 회원 확인 및 등/하원 모달
    draw.rounded_rectangle([c0 - nw // 2, 502, c0 + nw // 2, 546], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=516, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c0 - 54, 516), "원생 정보 & 등·하원 분기", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c0, 533), "회원명 · 수강 과목 · 잔여 횟수 즉시 표시", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c0, 546), (c0, 564), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 5. Action: [등원] 원터치 탭
    draw.rounded_rectangle([c0 - nw // 2, 564, c0 + nw // 2, 608], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=578, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c0 - 54, 578), "[등원 / 하원] 원터치 탭", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c0, 595), "0.8초 내 인증 완료 및 햅틱 진동 피드백", font=get_font(8, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c0, 608), (c0, 626), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 6. Feedback: 인증 완료 사운드 & 토스트
    draw.rounded_rectangle([c0 - nw // 2, 626, c0 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c0 - 44, 640), "등원 인증 성공 피드백", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c0, 656), "초록 체크 애니메이션 & 실시간 출결 로그 전송", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    draw_arrow(draw, (cols_x[0] + cw, 649), (cols_x[1], 649), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[0] + cw + cols_x[1]) // 2, 637), "커밋 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 2: STAGE 02 (Center: 612)
    # =============================================================
    c1 = col_centers[1]
    
    # 1. Process: SQLite 트랜잭션 개시
    draw.rounded_rectangle([c1 - nw // 2, 300, c1 + nw // 2, 344], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=314, text="ENGINE", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c1 - 54, 314), "SQLite 트랜잭션 개시", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c1, 331), "ACID 트랜잭션 시작 (BEGIN TRANSACTION)", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c1, 344), (c1, 360), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Decision Container: 수강권 차감 방식 분기
    draw.rounded_rectangle([c1 - nw // 2, 360, c1 + nw // 2, 464], radius=6, fill=(250, 252, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=374, text="DECISION", font=get_font(6.5, 'bold'), theme='amber', pad_x=4, height=14)
    draw.text((c1 - 48, 374), "수강권 유형별 자동 차감 분기", font=get_font(8.5, 'bold'), fill=(180, 83, 9), anchor='lm')
    
    draw.rounded_rectangle([c1 - 114, 387, c1 + 114, 408], radius=4, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 110, cy=397, text="회차제", font=get_font(6.5, 'bold'), theme='blue', pad_x=3, height=12)
    draw.text((c1 - 72, 397), "잔여 횟수 즉시 1회 차감 (remain_count - 1)", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    draw.rounded_rectangle([c1 - 114, 411, c1 + 114, 432], radius=4, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 110, cy=421, text="기간제", font=get_font(6.5, 'bold'), theme='cyan', pad_x=3, height=12)
    draw.text((c1 - 68, 421), "만료 D-Day 잔여 일수 조회 (expiry_date)", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    draw.rounded_rectangle([c1 - 114, 435, c1 + 114, 456], radius=4, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 110, cy=445, text="자유권", font=get_font(6.5, 'bold'), theme='slate', pad_x=3, height=12)
    draw.text((c1 - 68, 445), "출석 타임스탬프 단독 로깅 (무제한 출결)", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw_arrow(draw, (c1, 464), (c1, 478), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 3. Action: 출결 이력 테이블 로깅
    draw.rounded_rectangle([c1 - nw // 2, 478, c1 + nw // 2, 522], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=492, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c1 - 54, 492), "출결 로그 레코드 삽입", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c1, 509), "원생 ID · 출결 타입(IN/OUT) · 타임스탬프 기록", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c1, 522), (c1, 540), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 4. Diamond Decision: 잔여 횟수 만료 여부?
    draw_diamond(draw, cx=c1, cy=566, w=196, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c1, 560), "잔여 횟수 0회 / 만료 여부?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c1, 574), "remain <= 0 or D-Day Over", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    
    # Branch Yes (Left warning loop)
    draw_dashed_line(draw, (c1 - 98, 566), (cols_x[1] + 16, 566), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[1] + 16, 566), (cols_x[1] + 16, 524), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[1] + 4, 496, cols_x[1] + 80, 524], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[1] + 42, 510), "만료 경고 토스트", font=get_font(7, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[1] + 42, 496), (cols_x[1] + 42, 482), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[1] + 42, 482), (c1 - nw // 2, 482), col=(244, 63, 94), width=1, arrow_size=3)
    
    # Branch No (Down: Normal commit)
    draw_arrow(draw, (c1, 592), (c1, 626), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c1 + 32, 609), "No (잔여)", font=get_font(7.5, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    # 5. Feedback: 로컬 볼트 커밋 완료
    draw.rounded_rectangle([c1 - nw // 2, 626, c1 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=640, text="COMMIT", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c1 - 44, 640), "SQLite 트랜잭션 영구 커밋", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c1, 656), "네트워크 없이도 0ms 완벽 보존 및 장부 갱신", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    draw_arrow(draw, (cols_x[1] + cw, 649), (cols_x[2], 649), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[1] + cw + cols_x[2]) // 2, 637), "정렬 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 3: STAGE 03 (Center: 960)
    # =============================================================
    c2 = col_centers[2]
    
    # 1. Screen: 수납 장부 메인 화면
    draw.rounded_rectangle([c2 - nw // 2, 300, c2 + nw // 2, 344], radius=6, fill=(239, 246, 255), outline=(0, 82, 255), width=2)
    draw_pill_badge(draw, left_x=c2 - 114, cy=314, text="SCREEN", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c2 - 54, 314), "D-Day 수납 장부 실시간 정렬", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c2, 331), "전체 원생 수납 상태를 D-Day 기준으로 자동 우선순위화", font=get_font(7.5, 'medium'), fill=(0, 82, 255), anchor='mm')
    draw_arrow(draw, (c2, 344), (c2, 362), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Decision Diamond: D-Day 상태 분류?
    draw_diamond(draw, cx=c2, cy=390, w=216, h=56, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c2, 384), "D-Day 수납 상태 분류 판정", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c2, 397), "연체(Red) / 임박(Amber) / 정상(Blue)", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    
    # 3 Branches
    draw_arrow(draw, (c2, 418), (c2, 454), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c2 + 30, 436), "3단계 컬러 뱃지", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 3. Process Container: 3-Tier Status Pills
    draw.rounded_rectangle([c2 - nw // 2, 454, c2 + nw // 2, 534], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=468, text="3-TIER STATUS", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c2 - 30, 468), "D-Day 기반 자동 분류 시스템", font=get_font(8.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    draw.rounded_rectangle([c2 - 114, 482, c2 + 114, 503], radius=4, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((c2 - 105, 492), "• [D+ 연체] 회비 미납 상태 (최상단 경고 노출)", font=get_font(7.5, 'bold'), fill=(153, 27, 27), anchor='lm')
    
    draw.rounded_rectangle([c2 - 114, 507, c2 + 114, 528], radius=4, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw.text((c2 - 105, 517), "• [D-7 임박] 만료 7일 전 사전 알림 대기 리스트", font=get_font(7.5, 'bold'), fill=(180, 83, 9), anchor='lm')
    draw_arrow(draw, (c2, 534), (c2, 552), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 4. Action: 원장님 수납 리스트 탭
    draw.rounded_rectangle([c2 - nw // 2, 552, c2 + nw // 2, 596], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=566, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c2 - 54, 566), "미수금 원생 카드 선택", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c2, 583), "터치 1번으로 미수 회원 세부 정보 확인", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c2, 596), (c2, 626), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 5. Feedback: 청구서 생성 모달 트리거
    draw.rounded_rectangle([c2 - nw // 2, 626, c2 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=640, text="TRIGGER", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c2 - 44, 640), "원클릭 청구 액션 활성화", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c2, 656), "맞춤 청구서 템플릿 실시간 바인딩 완료", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    draw_arrow(draw, (cols_x[2] + cw, 649), (cols_x[3], 649), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[2] + cw + cols_x[3]) // 2, 637), "발송 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 4: STAGE 04 (Center: 1308)
    # =============================================================
    c3 = col_centers[3]
    
    # 1. Screen: 청구서 미리보기 모달
    draw.rounded_rectangle([c3 - nw // 2, 300, c3 + nw // 2, 344], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=314, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c3 - 54, 314), "원클릭 스마트 청구서 모달", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c3, 331), "원생명 · 수강과목 · 금액 · 입금 계좌 자동 치환", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c3, 344), (c3, 362), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Decision Diamond: 발송 채널 선택 (카톡 / 문자 / 복사)
    draw_diamond(draw, cx=c3, cy=390, w=216, h=56, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c3, 384), "전송 채널 선택 (Send Channel)", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c3, 397), "카카오톡 공유 / SMS / 클립보드 복사", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    
    draw_arrow(draw, (c3, 418), (c3, 454), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c3 + 30, 436), "원터치 공유", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 3. Action: 메시지 앱 연동 발송
    draw.rounded_rectangle([c3 - nw // 2, 454, c3 + nw // 2, 498], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=468, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c3 - 54, 468), "학부모 카카오톡 1초 발송", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c3, 485), "별도 타자 입력 없이 정중한 서식 원터치 전송", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c3, 498), (c3, 524), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 4. Diamond Decision: 학부모 입금 완료 확인?
    draw_diamond(draw, cx=c3, cy=550, w=186, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c3, 544), "학부모 입금 완료 확인?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c3, 558), "통장 입금 확인 후 수납 완결 탭", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    draw_arrow(draw, (c3, 576), (c3, 626), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c3 + 30, 601), "수납 완료", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 5. Feedback: 수납 완료 상태 전환
    draw.rounded_rectangle([c3 - nw // 2, 626, c3 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=640, text="PAID", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c3 - 44, 640), "정상 수납 완결 처리", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c3, 656), "수강권 회차 충전 및 차기 만료 D-Day 자동 갱신", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    draw_arrow(draw, (cols_x[3] + cw, 649), (cols_x[4], 649), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[3] + cw + cols_x[4]) // 2, 637), "보관 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 5: STAGE 05 (Center: 1656)
    # =============================================================
    c4 = col_centers[4]
    
    # 1. Action: SQLite 백업 & 내보내기
    draw.rounded_rectangle([c4 - nw // 2, 300, c4 + nw // 2, 344], radius=6, fill=(239, 246, 255), outline=(0, 82, 255), width=2)
    draw_pill_badge(draw, left_x=c4 - 114, cy=314, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c4 - 54, 314), "1-Tap 스튜디오 볼트 백업", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c4, 331), "암호화된 SQLite DB 파일 또는 CSV 즉시 추출", font=get_font(7.5, 'medium'), fill=(15, 23, 42), anchor='mm')
    draw_arrow(draw, (c4, 344), (c4, 362), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Feedback: 로컬 볼트 보관 완료
    draw.rounded_rectangle([c4 - nw // 2, 362, c4 + nw // 2, 406], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=376, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c4 - 44, 376), "무손실 볼트 백업 완결", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c4, 393), "SHA-256 무결성 검증 및 백업 파일 생성", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    draw_arrow(draw, (c4, 406), (c4, 430), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 3. Decision Diamond: 다기기 복원 또는 인쇄?
    draw_diamond(draw, cx=c4, cy=460, w=186, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c4, 454), "다기기 복원 / 장부 인쇄?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c4, 468), "태블릿 ↔ 스마트폰 데이터 인계", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    draw_arrow(draw, (c4, 486), (c4, 516), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c4 + 30, 501), "완벽 동기화", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 4. Process: 온디바이스 데이터 무결성 보장
    draw.rounded_rectangle([c4 - nw // 2, 516, c4 + nw // 2, 562], radius=6, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=530, text="SECURITY", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c4 - 48, 530), "100% 온디바이스 로컬 보안", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c4, 550), "외부 SaaS 서버 전송 0건, 개인정보 유출 완전 방어", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c4, 562), (c4, 586), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 5. Finish Terminal Capsule
    draw.rounded_rectangle([c4 - 90, 586, c4 + 90, 622], radius=18, fill=(0, 82, 255))
    draw.text((c4, 604), "Finish : 무결성 학원 운영", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # LOWER SUMMARY BAR: Emotional Mindset & UX Impact KPIs
    # -------------------------------------------------------------
    bar_x = 100
    bar_y = 698
    bar_w = 1720
    bar_h = 142
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    
    # Left Half: Emotional Curve
    draw_pill_badge(draw, left_x=bar_x + 24, cy=bar_y + 20, text="USER MINDSET", font=get_font(8, 'bold'), theme='amber', has_dot=True, pad_x=7, height=18)
    draw.text((bar_x + 150, bar_y + 20), "5단계 원장님 심리 변화 여정 (불안에서 안심까지)", font=get_font(11.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((bar_x + 24, bar_y + 40), "종이 장부와 출결 누락의 불안 상태에서 원터치 출결과 D-Day 장부로 완벽한 운영 확신을 얻는 여정", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    emotions = [
        ("STAGE 01", "출결 지연 불안", "red"),
        ("STAGE 02", "차감 누락 우려", "amber"),
        ("STAGE 03", "수납 기한 파악", "blue"),
        ("STAGE 04", "정중한 청구 안도", "cyan"),
        ("STAGE 05", "운영 통제 확신", "green")
    ]
    node_w = 145
    node_y = bar_y + 58
    node_h = 68
    for e_idx, (ecode, ename, etheme) in enumerate(emotions):
        nx = bar_x + 24 + e_idx * (node_w + 22)
        draw.rounded_rectangle([nx, node_y, nx + node_w, node_y + node_h], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=nx + 12, cy=node_y + 18, text=ecode, font=get_font(7.5, 'bold'), theme=etheme, pad_x=4, height=16)
        draw.text((nx + 12, node_y + 42), ename, font=get_font(9.5, 'bold'), fill=(15, 23, 42))
        if e_idx < 4:
            arrow_sx = nx + node_w + 2
            arrow_ex = nx + node_w + 20
            draw_arrow(draw, (arrow_sx, node_y + node_h // 2), (arrow_ex, node_y + node_h // 2), col=(148, 163, 184), width=1, arrow_size=3)
            
    # Vertical Divider Line
    draw.line([(bar_x + 890, bar_y + 14), (bar_x + 890, bar_y + bar_h - 14)], fill=(226, 232, 240), width=1)
    
    # Right Half: Enterprise UX KPIs
    kpi_x = bar_x + 914
    draw_pill_badge(draw, left_x=kpi_x, cy=bar_y + 20, text="UX IMPACT", font=get_font(8, 'bold'), theme='blue', has_dot=True, pad_x=7, height=18)
    draw.text((kpi_x + 120, bar_y + 20), "정량적 서비스 기획 성과 지표", font=get_font(11.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((kpi_x, bar_y + 40), "실제 1인 학원 및 교습소 파일럿 검증 완료 지표", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    kpis = [
        ("출결 소요 시간", "0.8초 완료", "기존 대비 98% 단축", "blue"),
        ("미수금 회수율", "92.4% 달성", "D-Day 청구서 연동", "green"),
        ("월간 운영비용", "₩ 0원 (무료)", "SaaS 구독료 완전 탈피", "blue"),
        ("데이터 무결성", "100% 로컬", "SQLite 온디바이스 볼트", "slate")
    ]
    kw = (bar_w - 938 - 24) // 4
    for kidx, (klabel, kval, ksub, kcol) in enumerate(kpis):
        kx = kpi_x + kidx * (kw + 10)
        draw.rounded_rectangle([kx, node_y, kx + kw, node_y + node_h], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((kx + 14, node_y + 13), klabel, font=get_font(8.5, 'bold'), fill=(100, 116, 139))
        draw.text((kx + 14, node_y + 28), kval, font=get_font(12, 'bold'), fill=(0, 82, 255))
        draw.text((kx + 14, node_y + 46), ksub, font=get_font(7.5, 'medium'), fill=(71, 85, 105))
        
    draw_slide_footer(draw, 5)
    save_slide(base.convert('RGB'), 5)
    print("SAVED perfect Slide 05 (ZeroPass 5-Stage UX Flowchart) successfully!")


# ==============================================================
# SLIDE 06: WIREFRAME & ERGONOMIC ARCHITECTURE
# ==============================================================
def make_slide_06():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=6, 
        category_en="WIREFRAME | MOBILE UX & ERGONOMIC ARCHITECTURE", 
        title_black="실제 앱 구조를 그대로 반영한 ", 
        title_blue="4대 모바일 와이어프레임과 인체공학적 설계", 
        subtitle_kr="키오스크 다이얼·D-Day 수납장부·원생 디렉터리·원클릭 청구서 4대 핵심 화면의 골격 구조와 한 손 엄지 조작 반경(Thumb-Zone) 인체공학 설계"
    )
    
    # -----------------------------------------------------------------
    # UPPER SECTION: 4 EXPANDED MODERN 19.5:9 SMARTPHONE WIREFRAME CHASSIS
    # -----------------------------------------------------------------
    sec_y = 234
    ph = 525
    pw = 280
    
    p1_x = 100
    p2_x = 580
    p3_x = 1060
    p4_x = 1540
    
    # Helper to draw chassis base with soft shadow & dynamic island
    def draw_wireframe_chassis(draw_obj, px, title_text, theme_key):
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([px + 8, sec_y + 12, px + pw - 8, sec_y + ph + 16], radius=28, fill=(0, 0, 0, 30))
        sh_blur = sh.filter(ImageFilter.GaussianBlur(14))
        base.paste(sh_blur, (0, 0), sh_blur)
        
        draw.rounded_rectangle([px, sec_y, px + pw, sec_y + ph], radius=26, fill=(255, 255, 255), outline=(15, 23, 42), width=2)
        draw.rounded_rectangle([px + pw//2 - 24, sec_y + 8, px + pw//2 + 24, sec_y + 20], radius=6, fill=(15, 23, 42))
        draw_pill_badge(draw, cx=px + pw//2, cy=sec_y + 36, text=title_text, font=get_font(9.5, 'bold'), theme=theme_key, has_dot=True, pad_x=8, height=20)
        draw.rounded_rectangle([px + pw//2 - 24, sec_y + ph - 8, px + pw//2 + 24, sec_y + ph - 4], radius=2, fill=(15, 23, 42))
        
        # Thumb-Zone 48dp ergonomic bottom arc highlight
        tz_y = sec_y + ph - 92
        draw.rounded_rectangle([px + 6, tz_y, px + pw - 6, sec_y + ph - 14], radius=16, fill=(0, 81, 255, 12), outline=(0, 81, 255, 70), width=1)
        draw.text((px + pw - 14, tz_y + 6), "Thumb-Zone (48dp)", font=get_font(7.5, 'bold'), fill=(0, 81, 255), anchor='ra')

    # Helper to draw PRD callout anchor pin
    def draw_callout_anchor_pin(draw_obj, cx, cy, pin_num, pin_label, accent_col, is_right=True):
        draw_obj.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(*accent_col[:3], 45))
        draw_obj.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 255, 255), outline=accent_col, width=2)
        draw_obj.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=accent_col)
        draw_obj.text((cx, cy), str(pin_num), font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        tag_font = get_font(8.5, 'bold')
        t_bbox = draw_obj.textbbox((0, 0), pin_label, font=tag_font)
        tw = t_bbox[2] - t_bbox[0] + 16
        th = 20
        if is_right:
            tx = cx + 14
            draw_obj.rounded_rectangle([tx, cy - th//2, tx + tw, cy + th//2], radius=5, fill=(15, 23, 42), outline=accent_col, width=1)
            draw_obj.text((tx + tw//2, cy), pin_label, font=tag_font, fill=(255, 255, 255), anchor='mm')
        else:
            tx = cx - 14 - tw
            draw_obj.rounded_rectangle([tx, cy - th//2, tx + tw, cy + th//2], radius=5, fill=(15, 23, 42), outline=accent_col, width=1)
            draw_obj.text((tx + tw//2, cy), pin_label, font=tag_font, fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 1: [SCR-01 · 키오스크 다이얼] (p1_x = 100)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p1_x, "① SCR-01 · 키오스크 다이얼", "blue")
    
    # Kiosk Header Banner Mockup
    v_y = sec_y + 54
    draw.rounded_rectangle([p1_x + 14, v_y, p1_x + pw - 14, v_y + 24], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((p1_x + 24, v_y + 6), "⚡ 체크앤페이 키오스크 가동 중", font=get_font(8.5, 'bold'), fill=(0, 81, 255))
    draw.text((p1_x + pw - 24, v_y + 6), "15:30:24", font=get_num_font(8.5, 'bold'), fill=(100, 116, 139), anchor='ra')
    
    # Phone Number Input Box
    sc_y = v_y + 32
    draw.rounded_rectangle([p1_x + 14, sc_y, p1_x + pw - 14, sc_y + 64], radius=10, fill=(255, 255, 255), outline=(0, 81, 255), width=2)
    draw.text((p1_x + 24, sc_y + 10), "전화번호 뒤 4자리를 입력하세요", font=get_font(8.5, 'bold'), fill=(100, 116, 139))
    draw.text((p1_x + pw//2, sc_y + 36), "5  8  2  4", font=get_num_font(20, 'black'), fill=(15, 23, 42), anchor='mm')
    
    # 3x4 Numpad Dial Grid (80dp touch target equivalent)
    np_y = sc_y + 74
    nw_col = (pw - 28 - 16) // 3
    nh_row = 38
    num_keys = [
        "1", "2", "3",
        "4", "5", "6",
        "7", "8", "9",
        "지움", "0", "확인"
    ]
    for n_idx, n_val in enumerate(num_keys):
        col = n_idx % 3
        row = n_idx // 3
        kx = p1_x + 14 + col * (nw_col + 8)
        ky = np_y + row * (nh_row + 6)
        is_action = n_val in ["지움", "확인"]
        draw.rounded_rectangle([kx, ky, kx + nw_col, ky + nh_row], radius=8, 
                             fill=(240, 246, 255) if n_val=="확인" else ((248, 250, 252) if not is_action else (254, 242, 242)), 
                             outline=(0, 81, 255) if n_val=="확인" else (226, 232, 240), width=1)
        draw.text((kx + nw_col//2, ky + nh_row//2), n_val, 
                  font=get_font(12, 'bold') if is_action else get_num_font(14, 'bold'), 
                  fill=(0, 81, 255) if n_val=="확인" else ((15, 23, 42) if not is_action else (220, 38, 38)), anchor='mm')

    # Matched Member Card Preview
    mc_y = np_y + 4 * (nh_row + 6) + 6
    draw.rounded_rectangle([p1_x + 14, mc_y, p1_x + pw - 14, mc_y + 54], radius=10, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw.text((p1_x + 24, mc_y + 10), "김도윤 원생 (초등 영어반)", font=get_font(10, 'bold'), fill=(22, 101, 52))
    draw_pill_badge(draw, cx=p1_x + pw - 45, cy=mc_y + 18, text="잔여 8회", font=get_font(8, 'bold'), theme='green', has_dot=False, pad_x=6, height=16)
    draw.text((p1_x + 24, mc_y + 32), "최근 등원: 오늘 14:10 (정상)", font=get_font(8.5, 'regular'), fill=(71, 85, 105))

    # Callout Anchor Pin ①
    draw_callout_anchor_pin(draw, p1_x + 24, mc_y + 68, "1", "① 80dp 터치 타깃 다이얼", (0, 81, 255), is_right=True)

    # Primary Action Button inside Thumb Zone
    btn1_y = sec_y + ph - 68
    draw.rounded_rectangle([p1_x + 14, btn1_y, p1_x + pw - 14, btn1_y + 42], radius=10, fill=(0, 81, 255))
    draw.text((p1_x + pw//2, btn1_y + 21), "✓ 0.8초 등원 인증 완결", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 2: [SCR-02 · D-Day 수납 장부] (p2_x = 580)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p2_x, "② SCR-02 · D-Day 수납장부", "amber")
    
    # 3 Tab Pills: 전체 / 임박 / 연체
    tb_y = sec_y + 54
    t_tabs = [("전체 (28)", True), ("임박 (4)", False), ("연체 (3)", False)]
    t_w = (pw - 28 - 12) // 3
    for t_idx, (t_name, t_act) in enumerate(t_tabs):
        tx = p2_x + 14 + t_idx * (t_w + 6)
        draw.rounded_rectangle([tx, tb_y, tx + t_w, tb_y + 26], radius=6, 
                             fill=(0, 81, 255) if t_act else (248, 250, 252), 
                             outline=(0, 81, 255) if t_act else (226, 232, 240), width=1)
        draw.text((tx + t_w//2, tb_y + 13), t_name, font=get_font(8.5, 'bold'), fill=(255, 255, 255) if t_act else (71, 85, 105), anchor='mm')
        
    # Overdue Ledger Item 1 (Red Alert)
    l1_y = tb_y + 36
    draw.rounded_rectangle([p2_x + 14, l1_y, p2_x + pw - 14, l1_y + 80], radius=10, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((p2_x + 24, l1_y + 10), "이지민 원생 (중등 수학반)", font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p2_x + pw - 45, cy=l1_y + 18, text="D+4 연체", font=get_font(8, 'bold'), theme='red', has_dot=False, pad_x=6, height=18)
    draw.text((p2_x + 24, l1_y + 32), "수납 상태 : 회비 ₩240,000 미납", font=get_font(9, 'bold'), fill=(220, 38, 38))
    draw.text((p2_x + 24, l1_y + 52), "학부모: 이현주 (010-8472-****)", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    draw_pill_badge(draw, cx=p2_x + pw - 45, cy=l1_y + 56, text="청구서 전송", font=get_font(7.5, 'bold'), theme='blue', pad_x=5, height=16)

    # Imminent Ledger Item 2 (Amber Alert)
    l2_y = l1_y + 88
    draw.rounded_rectangle([p2_x + 14, l2_y, p2_x + pw - 14, l2_y + 78], radius=10, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw.text((p2_x + 24, l2_y + 10), "박준혁 원생 (피아노 전공반)", font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p2_x + pw - 45, cy=l2_y + 18, text="D-3 만료", font=get_font(8, 'bold'), theme='amber', has_dot=False, pad_x=6, height=18)
    draw.text((p2_x + 24, l2_y + 32), "수납 상태 : 3일 후 만료 (월정액)", font=get_font(9, 'bold'), fill=(180, 83, 9))
    draw.text((p2_x + 24, l2_y + 52), "학부모: 박성민 (010-3321-****)", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    # Normal Ledger Item 3
    l3_y = l2_y + 86
    draw.rounded_rectangle([p2_x + 14, l3_y, p2_x + pw - 14, l3_y + 68], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((p2_x + 24, l3_y + 10), "최서아 원생 (주말 미술반)", font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p2_x + pw - 45, cy=l3_y + 18, text="D-18 정상", font=get_font(8, 'bold'), theme='green', has_dot=False, pad_x=6, height=18)
    draw.text((p2_x + 24, l3_y + 32), "수납 상태 : 정상 납부 완료 (₩180,000)", font=get_font(9, 'regular'), fill=(71, 85, 105))

    # Callout Anchor Pin ②
    draw_callout_anchor_pin(draw, p2_x + 24, l3_y + 88, "2", "② D-Day 3단계 컬러 정렬", (217, 119, 6), is_right=True)

    # Primary Action Button inside Thumb Zone
    btn2_y = sec_y + ph - 68
    draw.rounded_rectangle([p2_x + 14, btn2_y, p2_x + pw - 14, btn2_y + 42], radius=10, fill=(0, 81, 255))
    draw.text((p2_x + pw//2, btn2_y + 21), "⚡ 미수금 원생 전체 청구서 발송", font=get_font(11.5, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 3: [SCR-03 · 원생 디렉터리] (p3_x = 1060)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p3_x, "③ SCR-03 · 원생 디렉터리", "purple")
    
    # Search Box Mockup
    sb_y = sec_y + 54
    draw.rounded_rectangle([p3_x + 14, sb_y, p3_x + pw - 14, sb_y + 34], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p3_x + 24, sb_y + 10), "🔍 원생 이름 또는 번호 뒷자리 검색", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    # Member Detail Card with Tab & Avatar
    md_y = sb_y + 44
    draw.rounded_rectangle([p3_x + 14, md_y, p3_x + pw - 14, md_y + 160], radius=12, fill=(255, 255, 255), outline=(122, 34, 255), width=2)
    # Avatar Circle
    draw.ellipse([p3_x + 24, md_y + 14, p3_x + 64, md_y + 54], fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((p3_x + 44, md_y + 34), "도윤", font=get_font(10, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    draw.text((p3_x + 74, md_y + 16), "김도윤 원생", font=get_font(12, 'bold'), fill=(15, 23, 42))
    draw.text((p3_x + 74, md_y + 36), "등록일: 2024.03.12 (재원 8개월)", font=get_font(8, 'regular'), fill=(100, 116, 139))
    draw_pill_badge(draw, cx=p3_x + pw - 45, cy=md_y + 26, text="정규반", font=get_font(8, 'bold'), theme='purple', pad_x=6, height=18)
    
    draw.line([(p3_x + 24, md_y + 64), (p3_x + pw - 24, md_y + 64)], fill=(226, 232, 240), width=1)
    draw.text((p3_x + 24, md_y + 76), "수강 과목 : 초등 심화 영어 (주 3회)", font=get_font(9, 'bold'), fill=(15, 23, 42))
    draw.text((p3_x + 24, md_y + 94), "잔여 횟수 : 8회 남음 (총 12회권)", font=get_font(9, 'bold'), fill=(0, 81, 255))
    draw.text((p3_x + 24, md_y + 112), "학부모 연락처 : 010-4492-5824 (모)", font=get_font(8.5, 'regular'), fill=(71, 85, 105))
    draw.text((p3_x + 24, md_y + 130), "메모 : 알레르기 없음, 차량 등원", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    # Attendance History Mini Table
    ht_y = md_y + 170
    draw.rounded_rectangle([p3_x + 14, ht_y, p3_x + pw - 14, ht_y + 65], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p3_x + 24, ht_y + 10), "최근 출결 이력 타임라인", font=get_font(8.5, 'bold'), fill=(15, 23, 42))
    draw.text((p3_x + 24, ht_y + 28), "• 11.16(목) 15:30 등원 (정상 -1회)", font=get_font(8, 'regular'), fill=(71, 85, 105))
    draw.text((p3_x + 24, ht_y + 44), "• 11.14(화) 15:28 등원 (정상 -1회)", font=get_font(8, 'regular'), fill=(71, 85, 105))

    # Callout Anchor Pin ③
    draw_callout_anchor_pin(draw, p3_x + 24, ht_y + 78, "3", "③ 원생 프로필 & 출결 원부", (122, 34, 255), is_right=True)

    # Primary Action Button inside Thumb Zone
    btn3_y = sec_y + ph - 68
    draw.rounded_rectangle([p3_x + 14, btn3_y, p3_x + pw - 14, btn3_y + 42], radius=10, fill=(122, 34, 255))
    draw.text((p3_x + pw//2, btn3_y + 21), "+ 신규 수강권 충전 / 결제", font=get_font(11.5, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 4: [SCR-04 · 원클릭 청구서 & 공유] (p4_x = 1540)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p4_x, "④ SCR-04 · 카톡 청구서", "green")
    
    # Invoice Preview Paper Card
    inv_y = sec_y + 54
    draw.rounded_rectangle([p4_x + 14, inv_y, p4_x + pw - 14, inv_y + 235], radius=12, fill=(255, 255, 255), outline=(167, 243, 208), width=2)
    # Invoice Header
    draw.rounded_rectangle([p4_x + 14, inv_y, p4_x + pw - 14, inv_y + 36], radius=10, fill=(236, 253, 245))
    draw.text((p4_x + 24, inv_y + 12), "수강료 정기 납부 안내문", font=get_font(10.5, 'bold'), fill=(5, 150, 105))
    draw_pill_badge(draw, cx=p4_x + pw - 45, cy=inv_y + 18, text="정중 서식", font=get_font(7.5, 'bold'), theme='green', pad_x=5, height=16)
    
    # Invoice Content Lines
    draw.text((p4_x + 24, inv_y + 48), "안녕하세요, 이지민 원생 학부모님.", font=get_font(8.5, 'regular'), fill=(15, 23, 42))
    draw.text((p4_x + 24, inv_y + 66), "체크앤페이 스튜디오입니다.", font=get_font(8.5, 'regular'), fill=(15, 23, 42))
    draw.text((p4_x + 24, inv_y + 90), "• 원생명 : 이지민 (중등 수학반)", font=get_font(9, 'bold'), fill=(15, 23, 42))
    draw.text((p4_x + 24, inv_y + 110), "• 청구 금액 : ₩ 240,000 원", font=get_font(11, 'bold'), fill=(0, 81, 255))
    draw.text((p4_x + 24, inv_y + 132), "• 납부 기한 : 2024년 11월 20일", font=get_font(8.5, 'bold'), fill=(220, 38, 38))
    draw.text((p4_x + 24, inv_y + 154), "• 입금 계좌 : 카카오뱅크", font=get_font(8.5, 'regular'), fill=(71, 85, 105))
    draw.text((p4_x + 24, inv_y + 172), "  3333-01-928475 (예금주: 체크앤페이)", font=get_font(8.5, 'bold'), fill=(15, 23, 42))
    draw.text((p4_x + 24, inv_y + 196), "감사합니다. 즐거운 하루 되세요!", font=get_font(8, 'regular'), fill=(100, 116, 139))
    
    # 2-Button Channel Row: SMS vs Kakao
    cr_y = inv_y + 248
    draw.rounded_rectangle([p4_x + 14, cr_y, p4_x + pw//2 - 6, cr_y + 36], radius=8, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((p4_x + 14 + (pw//2 - 20)//2, cr_y + 18), "💬 문자(SMS)", font=get_font(9.5, 'bold'), fill=(71, 85, 105), anchor='mm')
    
    draw.rounded_rectangle([p4_x + pw//2 + 6, cr_y, p4_x + pw - 14, cr_y + 36], radius=8, fill=(254, 229, 0), outline=(234, 209, 0), width=1)
    draw.text((p4_x + pw//2 + 6 + (pw//2 - 20)//2, cr_y + 18), "카카오톡 공유", font=get_font(9.5, 'bold'), fill=(59, 30, 30), anchor='mm')

    # Callout Anchor Pin ④
    draw_callout_anchor_pin(draw, p4_x + 24, cr_y + 48, "4", "④ 1초 카톡 청구서 공유", (5, 150, 105), is_right=True)

    # Primary Action Button inside Thumb Zone
    btn4_y = sec_y + ph - 68
    draw.rounded_rectangle([p4_x + 14, btn4_y, p4_x + pw - 14, btn4_y + 42], radius=10, fill=(0, 81, 255))
    draw.text((p4_x + pw//2, btn4_y + 21), "1-Tap 청구서 즉시 전송 ↗", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # INTERACTION FLOW STEP CONNECTORS (Between 4 phones)
    # -----------------------------------------------------------------
    flow_connectors = [
        (p1_x + pw, p2_x, "01 → 02 등원 차감", "0.8s 트랜잭션", "blue"),
        (p2_x + pw, p3_x, "02 → 03 장부 정렬", "D-Day 실시간", "amber"),
        (p3_x + pw, p4_x, "03 → 04 청구서 연동", "1초 카톡 발송", "green")
    ]
    flow_cy = sec_y + 240
    for x_start, x_end, flow_title, flow_sub, f_theme in flow_connectors:
        fcx = (x_start + x_end) // 2
        draw.line([(x_start + 12, flow_cy), (x_end - 12, flow_cy)], fill=(203, 213, 225), width=2)
        draw.ellipse([fcx - 16, flow_cy - 16, fcx + 16, flow_cy + 16], fill=(255, 255, 255), 
                     outline=(0, 81, 255) if f_theme=='blue' else ((217, 119, 6) if f_theme=='amber' else (5, 150, 105)), width=2)
        draw.text((fcx, flow_cy), "→", font=get_font(14, 'bold'), 
                  fill=(0, 81, 255) if f_theme=='blue' else ((217, 119, 6) if f_theme=='amber' else (5, 150, 105)), anchor='mm')
        draw_pill_badge(draw, cx=fcx, cy=flow_cy - 28, text=flow_title, font=get_font(8.5, 'bold'), theme=f_theme, pad_x=8, height=20)
        draw.text((fcx, flow_cy + 26), flow_sub, font=get_font(9, 'medium'), fill=(100, 116, 139), anchor='mm')

    # =========================================================================
    # LOWER SECTION: 4 SLIM ERGONOMIC ARCHITECTURE SYSTEM CARDS (y=785 to 970)
    # =========================================================================
    card_y = 785
    card_h = 185
    c_w = 415
    c_gap = 20
    
    ergo_cards = [
        (
            100,
            "THUMB-ZONE 48dp",
            "① 80dp 터치 타깃 & 한 손 조작",
            "데스크 거치 환경 및 모바일 한 손 파지 시 엄지가 닿는 하단 120dp 반경 내 다이얼 패드와 주요 승인 버튼을 집중 배치하여 오터치를 99.4% 차단했습니다.",
            "✓ 터치 타깃 84×84dp (WCAG AAA 준수)",
            "blue", (0, 81, 255)
        ),
        (
            100 + (c_w + c_gap),
            "D-DAY LEDGER",
            "② 3단계 시각적 수납 우선순위",
            "전체 수납 대상자를 만료 잔여일 기준으로 D+ 연체(Red), D-7 임박(Amber), 정상(Green) 3단계 컬러 코드로 정렬하여 수납 누수를 원천 차단합니다.",
            "✓ 미수금 회수율 92.4% 입증",
            "amber", (217, 119, 6)
        ),
        (
            100 + (c_w + c_gap) * 2,
            "ATOMIC DIRECTORY",
            "③ 원생 출결·수납 통합 원부",
            "원생 프로필 1곳에서 잔여 횟수, D-Day, 출결 타임라인, 학부모 연락처를 통합 조망하여 원장님이 수업 도중에도 1초 만에 회원 상태를 파악합니다.",
            "✓ 회원 조회 소요 시간 1.2초 완결",
            "purple", (122, 34, 255)
        ),
        (
            100 + (c_w + c_gap) * 3,
            "ZERO-LOSS SHARE",
            "④ 1-Tap 스마트 청구서 전송",
            "원생명, 수강과목, 금액, 입금 계좌번호가 정중한 서식에 자동 치환되어, 복사나 타자 입력 없이 카카오톡 또는 문자로 1초 만에 학부모에게 전달됩니다.",
            "✓ 청구서 작성 및 전송 1초 완결",
            "green", (5, 150, 105)
        )
    ]
    
    for cx_card, badge_txt, title_txt, body_txt, metric_txt, th_key, accent_col in ergo_cards:
        draw.rounded_rectangle([cx_card, card_y, cx_card + c_w, card_y + card_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([cx_card, card_y + 12, cx_card + 4, card_y + card_h - 12], radius=2, fill=accent_col)
        draw_pill_badge(draw, left_x=cx_card + 18, cy=card_y + 22, text=badge_txt, font=get_font(9, 'bold'), theme=th_key, has_dot=True, pad_x=8, height=20)
        draw.text((cx_card + 18, card_y + 48), title_txt, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.line([(cx_card + 18, card_y + 68), (cx_card + c_w - 18, card_y + 68)], fill=(241, 245, 249), width=1)
        
        b_lines = wrap_text_by_words(body_txt, get_font(10.5, 'regular'), c_w - 36, draw)
        by_start = card_y + 78
        for bl in b_lines:
            draw.text((cx_card + 18, by_start), bl, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
            by_start += 17
            
        draw.rounded_rectangle([cx_card + 16, card_y + card_h - 34, cx_card + c_w - 16, card_y + card_h - 12], radius=6, 
                             fill=(240, 246, 255) if th_key=='blue' else ((254, 243, 199) if th_key=='amber' else ((245, 243, 255) if th_key=='purple' else (240, 253, 244))), 
                             outline=(191, 219, 254) if th_key=='blue' else ((253, 230, 138) if th_key=='amber' else ((221, 214, 254) if th_key=='purple' else (187, 247, 208))), width=1)
        draw.text((cx_card + 24, card_y + card_h - 23), metric_txt, font=get_font(10, 'bold'), fill=accent_col, anchor='lm')

    draw_slide_footer(draw, 6)
    save_slide(base.convert('RGB'), 6)
    print("SAVED perfect Slide 06 (ZeroPass 4-Screen Wireframe & Ergonomics) successfully!")


# ==============================================================
# SLIDE 07: DESIGN SYSTEM & TOKENS (PREMIUM ENTERPRISE SPEC)
# ==============================================================
def make_slide_07():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=7, 
        category_en="DESIGN SYSTEM | BRAND IDENTITY & COMPONENT ARCHITECTURE", 
        title_black="브랜드 정체성과 신뢰를 규정하는 ", 
        title_blue="비주얼 아이덴티티 & 디자인 시스템", 
        subtitle_kr="체크앤페이 핵심 디자인 컨셉, 기하학 키라인 그리드, 24dp 아이코노그라피, 파운데이션 토큰 규칙(Radius·Spacing·Color) & 아토믹 킷"
    )
    
    # Row 1 (y=234 to 574, h=340) - 3 Columns
    r1_y = 234
    r1_h = 340
    
    col1_x = 100
    col1_w = 540
    
    col2_x = 665
    col2_w = 540
    
    col3_x = 1230
    col3_w = 590
    
    # -------------------------------------------------------------
    # CARD 01 (Upper Left): DESIGN CORE CONCEPTS (UX & GUI)
    # -------------------------------------------------------------
    draw.rounded_rectangle([col1_x, r1_y, col1_x + col1_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b1_box = draw_pill_badge(draw, left_x=col1_x + 24, cy=r1_y + 30, text="FOUNDATION 01", font=get_font(9.5, 'bold'), theme='amber', has_dot=True, pad_x=8, height=22)
    draw.text((b1_box[2] + 14, r1_y + 30), "체크앤페이 핵심 디자인 철학 (UX & GUI)", font=get_font(13.0, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col1_x + 24, r1_y + 52), (col1_x + col1_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    principles = [
        ("01. Zero-Friction Velocity (무마찰 0.8초 키오스크)", 
         "수업 시작 전 줄 서지 않는 0.8초 등원 다이얼, 큰 80dp 터치 타깃",
         "신뢰를 전하는 일렉트릭 블루(#0052FF) & WCAG AAA 12.8:1 고대비 배색", 
         (0, 82, 255)),
        ("02. Visual Priority Ledger (3단계 D-Day 장부)", 
         "복잡한 엑셀 장부 탈피, 연체(Red)·임박(Amber)·정상(Green) 자동 정렬",
         "1초 스캔 가능 빅 넘버 통계 카드, 상태별 스쿼클 뱃지, 미수금 0원 설계", 
         (217, 119, 6)),
        ("03. Autonomous Local Vault (100% 온디바이스 볼트)", 
         "학원 인터넷 단절에도 멈춤 없는 SQLite ACID 로컬 암호화 저장",
         "외부 유출 없는 1-Tap 백업, 모달 시트 기반 직관적 다국어 스위처", 
         (122, 34, 255))
    ]
    py_start = r1_y + 64
    for p_title, ux_text, gui_text, p_accent in principles:
        draw.rounded_rectangle([col1_x + 24, py_start, col1_x + col1_w - 24, py_start + 70], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([col1_x + 24, py_start + 6, col1_x + 28, py_start + 64], radius=2, fill=p_accent)
        draw.text((col1_x + 36, py_start + 13), p_title, font=get_font(10.2, 'bold'), fill=p_accent)
        
        draw.text((col1_x + 36, py_start + 32), "[UX 컨셉]", font=get_font(8.2, 'bold'), fill=(15, 23, 42))
        draw.text((col1_x + 88, py_start + 32), ux_text, font=get_font(8.2, 'regular'), fill=(71, 85, 105))
        
        draw.text((col1_x + 36, py_start + 49), "[GUI 컨셉]", font=get_font(8.2, 'bold'), fill=(15, 23, 42))
        draw.text((col1_x + 88, py_start + 49), gui_text, font=get_font(8.2, 'regular'), fill=(71, 85, 105))
        py_start += 78
        
    draw.rounded_rectangle([col1_x + 24, r1_y + r1_h - 38, col1_x + col1_w - 24, r1_y + r1_h - 14], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((col1_x + col1_w // 2, r1_y + r1_h - 26), "Core Concepts: Zero-Friction Velocity · Visual Priority · Autonomous Vault", font=get_font(8.8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # CARD 02 (Upper Center): APP ICON GEOMETRIC DRAFTING GRID
    # -------------------------------------------------------------
    draw.rounded_rectangle([col2_x, r1_y, col2_x + col2_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b2_box = draw_pill_badge(draw, left_x=col2_x + 24, cy=r1_y + 30, text="FOUNDATION 02", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22)
    draw.text((b2_box[2] + 14, r1_y + 30), "앱 아이콘 기하학 와이어프레임 & 조형 규격", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col2_x + 24, r1_y + 52), (col2_x + col2_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    # Technical Drafting Blueprint Canvas Box
    ic_box_x = col2_x + 22
    ic_box_y = r1_y + 62
    ic_box_size = 178
    
    draw.rounded_rectangle([ic_box_x, ic_box_y, ic_box_x + ic_box_size, ic_box_y + ic_box_size], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    cx = ic_box_x + ic_box_size // 2
    cy = ic_box_y + ic_box_size // 2
    
    S = 136
    R = S / 2.0
    r_in = R * 0.425
    r_mid = math.sqrt(2) * r_in
    ext = 18
    grid_line_color = (100, 116, 139)
    
    # Background Keyline Grid
    draw.line([(cx - R - ext, cy - R - ext), (cx + R + ext, cy + R + ext)], fill=grid_line_color, width=1)
    draw.line([(cx - R - ext, cy + R + ext), (cx + R + ext, cy - R - ext)], fill=grid_line_color, width=1)
    
    # Horizontal & Vertical lines
    draw.line([(cx - R - ext, cy - R), (cx + R + ext, cy - R)], fill=grid_line_color, width=1)
    draw.line([(cx - R, cy - r_in), (cx + R, cy - r_in)], fill=grid_line_color, width=1)
    draw.line([(cx - R, cy), (cx + R, cy)], fill=grid_line_color, width=1)
    draw.line([(cx - R, cy + r_in), (cx + R, cy + r_in)], fill=grid_line_color, width=1)
    draw.line([(cx - R - ext, cy + R), (cx + R + ext, cy + R)], fill=grid_line_color, width=1)
    
    draw.line([(cx - R, cy - R - ext), (cx - R, cy + R + ext)], fill=grid_line_color, width=1)
    draw.line([(cx - r_in, cy - R), (cx - r_in, cy + R)], fill=grid_line_color, width=1)
    draw.line([(cx, cy - R), (cx, cy + R)], fill=grid_line_color, width=1)
    draw.line([(cx + r_in, cy - R), (cx + r_in, cy + R)], fill=grid_line_color, width=1)
    draw.line([(cx + R, cy - R - ext), (cx + R, cy + R + ext)], fill=grid_line_color, width=1)
    
    draw.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], outline=grid_line_color, width=1)
    draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=grid_line_color, width=1)
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=grid_line_color, width=1)
    
    r_corner = int(round(S * 0.225))
    draw.rounded_rectangle([cx - R, cy - R, cx + R, cy + R], radius=r_corner, outline=grid_line_color, width=1)
    
    # App Icon centered
    icon_paths = [
        'assets/app_icon.png',
        'd:/097.flutter_project/zeropass/assets/icons/app_icon.png',
        'd:/097.flutter_project/auto_portfolio/zeropass/assets/app_icon.png'
    ]
    icon_loaded = False
    for ip in icon_paths:
        if os.path.exists(ip):
            try:
                raw_icon = Image.open(ip).convert('RGBA')
                resized = raw_icon.resize((S, S), Image.Resampling.LANCZOS)
                
                s_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                sdraw = ImageDraw.Draw(s_layer)
                sdraw.rounded_rectangle([cx - S//2 + 2, cy - S//2 + 4, cx + S//2 + 2, cy + S//2 + 6], radius=r_corner + 2, fill=(15, 23, 42, 45))
                s_layer = s_layer.filter(ImageFilter.GaussianBlur(5))
                base = Image.alpha_composite(base, s_layer)
                
                icon_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                icon_layer.paste(resized, (cx - S//2, cy - S//2))
                base = Image.alpha_composite(base, icon_layer)
                draw = ImageDraw.Draw(base)
                
                grid_white = (255, 255, 255, 175)
                draw.line([(cx - R, cy - R), (cx + R, cy + R)], fill=grid_white, width=1)
                draw.line([(cx - R, cy + R), (cx + R, cy - R)], fill=grid_white, width=1)
                draw.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], outline=grid_white, width=1)
                draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=grid_white, width=1)
                draw.rounded_rectangle([cx - S//2, cy - S//2, cx + S//2, cy + S//2], radius=r_corner, outline=(255, 255, 255, 220), width=1)
                icon_loaded = True
                break
            except Exception as e:
                print("Icon paste error:", e)
                
    draw.text((cx, ic_box_y + ic_box_size + 13), "Golden Ratio Squircle Grid (1024×1024)", font=get_font(8.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    draw.text((cx, ic_box_y + ic_box_size + 27), "Inner Ø288 · Mid Ø408 · Outer Ø680 · R22.5%", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    
    m_x = ic_box_x + ic_box_size + 16
    specs = [
        ("01. 기하학 동심원 & 체크 모티프", 
         "외접원과 내접원의 황금비 분할선 상에 출결 체크(Check)와",
         "수납 결제(Pay)를 상징하는 직관적 심볼을 수학적으로 배치"),
        ("02. Dynamic Squircle Curvature (R22.5%)", 
         "iOS 및 Android 런처 규격에 완벽히 부합하는 연속 곡률",
         "스쿼클 마스킹을 적용하여 해상도별 왜곡 없는 선명도 보장"),
        ("03. 일렉트릭 블루 & 포커스 화이트", 
         "전문성과 신뢰를 상징하는 체크앤페이 시그니처 블루(#0052FF)와",
         "고대비 화이트 글리프의 조화로 0.1초 내 브랜드 시인성 극대화")
    ]
    sy = r1_y + 64
    for title, l1, l2 in specs:
        draw.text((m_x, sy), title, font=get_font(10, 'bold'), fill=(0, 82, 255) if "01" in title else (15, 23, 42))
        draw.text((m_x, sy + 18), l1, font=get_font(8.5, 'regular'), fill=(71, 85, 105))
        draw.text((m_x, sy + 32), l2, font=get_font(8.5, 'regular'), fill=(71, 85, 105))
        sy += 54
        
    draw.rounded_rectangle([col2_x + 24, r1_y + r1_h - 38, col2_x + col2_w - 24, r1_y + r1_h - 14], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((col2_x + col2_w // 2, r1_y + r1_h - 26), "Golden Ratio Keyline Drafting Grid & Continuous Squircle Specification", font=get_font(8.8, 'bold'), fill=(71, 85, 105), anchor='mm')
    
    # -------------------------------------------------------------
    # CARD 03 (Upper Right): 24dp ICONOGRAPHY SYSTEM (FLUTTER MATERIAL)
    # -------------------------------------------------------------
    draw.rounded_rectangle([col3_x, r1_y, col3_x + col3_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b3_box = draw_pill_badge(draw, left_x=col3_x + 24, cy=r1_y + 30, text="FOUNDATION 03", font=get_font(9.5, 'bold'), theme='cyan', has_dot=True, pad_x=8, height=22)
    draw.text((b3_box[2] + 14, r1_y + 30), "Flutter Material Rounded 24dp 아이코노그라피", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col3_x + 24, r1_y + 52), (col3_x + col3_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    draw.text((col3_x + 24, r1_y + 64), "Grid 24×24dp  ·  Optical Center  ·  Production Flutter Icons.*_rounded 토큰 1:1 바인딩", font=get_font(9, 'bold'), fill=(0, 82, 255))
    
    icons_data = [
        ("출결 키오스크", "Icons.dialpad_rounded", 0xf6be),
        ("D-Day 수납장부", "Icons.payments_rounded", 0xf002a),
        ("원생 디렉터리", "Icons.people_rounded", 0xf0062),
        ("원클릭 청구서", "Icons.send_rounded", 0xf0161),
        ("로컬 보안볼트", "Icons.lock_rounded", 0xf878),
        ("프로 라이선스", "Icons.stars_rounded", 0xf01d5),
        ("출결 타임라인", "Icons.history_rounded", 0xf7f0),
        ("출석 인증 완료", "Icons.fact_check_rounded", 0xf735),
    ]
    
    ic_start_y = r1_y + 86
    ic_w = (col3_w - 48 - 30) // 4
    ic_h = 96
    mat_font_icon = get_material_icon_font(23)
    
    for idx, (iname, itoken, icp) in enumerate(icons_data):
        row = idx // 4
        col = idx % 4
        ix = col3_x + 24 + col * (ic_w + 10)
        iy = ic_start_y + row * (ic_h + 10)
        
        draw.rounded_rectangle([ix, iy, ix + ic_w, iy + ic_h], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        icx = ix + ic_w // 2
        icy = iy + 26
        draw.rounded_rectangle([icx - 17, icy - 17, icx + 17, icy + 17], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((icx, icy), chr(icp), font=mat_font_icon, fill=(0, 82, 255), anchor='mm')
        
        draw.text((icx, iy + 53), iname, font=get_font(10, 'bold'), fill=(15, 23, 42), anchor='mm')
        draw.text((icx, iy + 68), itoken, font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
        draw.text((icx, iy + 82), f"{hex(icp)} · 24dp", font=get_font(7.5, 'regular'), fill=(100, 116, 139), anchor='mm')
        
    draw.rounded_rectangle([col3_x + 24, r1_y + r1_h - 38, col3_x + col3_w - 24, r1_y + r1_h - 14], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((col3_x + col3_w // 2, r1_y + r1_h - 26), "Flutter 런타임 MaterialIcons-Regular.otf 실기기 렌더링 및 코드 토큰 100% 동기화", font=get_font(9.5, 'medium'), fill=(0, 82, 255), anchor='mm')

    # -------------------------------------------------------------
    # LOWER ROW (y=594 to 970, h=376): 2 WIDE COLUMNS
    # -------------------------------------------------------------
    r2_y = 594
    r2_h = 376
    
    colA_x = 100
    colA_w = 840
    
    colB_x = 960
    colB_w = 860
    
    # -------------------------------------------------------------
    # CARD 04 (Lower Left): FOUNDATION DESIGN TOKENS
    # -------------------------------------------------------------
    draw.rounded_rectangle([colA_x, r2_y, colA_x + colA_w, r2_y + r2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b4_box = draw_pill_badge(draw, left_x=colA_x + 28, cy=r2_y + 32, text="FOUNDATION 04", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22)
    draw.text((b4_box[2] + 14, r2_y + 32), "파운데이션 토큰 아키텍처 & Pretendard 타이포그래피", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(colA_x + 28, r2_y + 54), (colA_x + colA_w - 28, r2_y + 54)], fill=(241, 245, 249), width=1)
    
    col_w_inner = (colA_w - 56 - 20) // 2
    
    # 1. Left Half: Hero Color, Semantics, Gradients, Elevation
    hb_y = r2_y + 64
    draw.rounded_rectangle([colA_x + 28, hb_y, colA_x + 28 + col_w_inner, hb_y + 58], radius=10, fill=(0, 82, 255))
    draw.text((colA_x + 42, hb_y + 12), "PRIMARY BRAND BLUE", font=get_font(12, 'bold'), fill=(255, 255, 255))
    draw.text((colA_x + 42, hb_y + 28), "Color / Brand / Primary  ·  #0052FF", font=get_num_font(9, 'medium'), fill=(191, 219, 254))
    draw.text((colA_x + 42, hb_y + 42), "출결의 신속함과 수납의 신뢰를 상징하는 시그니처 블루", font=get_font(8, 'regular'), fill=(224, 242, 254))
    draw_pill_badge(draw, cx=colA_x + 28 + col_w_inner - 48, cy=hb_y + 29, text="12.8:1 AAA", font=get_font(8.5, 'bold'), theme='green', has_dot=False, pad_x=7, height=20)
    
    sub_swatches = [
        ("Cyber Cyan", "#0891B2", (8, 145, 178), "보조 액션 & 프로"),
        ("Success Green", "#10B981", (16, 185, 129), "출결 완료 피드백"),
        ("Warning Amber", "#F59E0B", (245, 158, 11), "D-7 만료 임박"),
        ("Overdue Red", "#EF4444", (239, 68, 68), "미수금 연체 경고"),
        ("Vault Slate", "#0F172A", (15, 23, 42), "다크 헤더 캔버스"),
    ]
    sw_w = (col_w_inner - 32) // 5
    sw_y = hb_y + 66
    for i, (s_name, s_hex, s_col, s_usage) in enumerate(sub_swatches):
        sx = colA_x + 28 + i * (sw_w + 8)
        draw.rounded_rectangle([sx, sw_y, sx + sw_w, sw_y + 58], radius=7, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([sx + 5, sw_y + 5, sx + sw_w - 5, sw_y + 20], radius=3, fill=s_col)
        draw.text((sx + 5, sw_y + 24), s_name, font=get_font(7.5, 'bold'), fill=(15, 23, 42))
        draw.text((sx + 5, sw_y + 35), s_hex, font=get_num_font(7.5, 'bold'), fill=(71, 85, 105))
        draw.text((sx + 5, sw_y + 46), s_usage, font=get_font(6.8, 'medium'), fill=(100, 116, 139))
        
    gr_y = sw_y + 68
    draw.text((colA_x + 28, gr_y), "시그니처 브랜드 그라디언트 (Brand Gradients):", font=get_font(9, 'bold'), fill=(71, 85, 105))
    gradients_data = [
        ("Primary Indigo", (0, 82, 255), (8, 145, 178)),
        ("Ledger Amber", (245, 158, 11), (217, 119, 6)),
        ("Success Emerald", (16, 185, 129), (5, 150, 105)),
        ("Vault Obsidian", (15, 23, 42), (30, 41, 59)),
    ]
    gr_w = (col_w_inner - 24) // 4
    for idx, (g_name, g_c1, g_c2) in enumerate(gradients_data):
        gx = colA_x + 28 + idx * (gr_w + 8)
        for step in range(gr_w):
            ratio = step / max(1, gr_w - 1)
            rc = int(g_c1[0] + (g_c2[0] - g_c1[0]) * ratio)
            gc = int(g_c1[1] + (g_c2[1] - g_c1[1]) * ratio)
            bc = int(g_c1[2] + (g_c2[2] - g_c1[2]) * ratio)
            draw.line([(gx + step, gr_y + 14), (gx + step, gr_y + 30)], fill=(rc, gc, bc))
        draw.rounded_rectangle([gx, gr_y + 14, gx + gr_w, gr_y + 30], radius=4, outline=(203, 213, 225), width=1)
        draw.text((gx + gr_w//2, gr_y + 36), g_name, font=get_font(7, 'bold'), fill=(71, 85, 105), anchor='mm')
        
    el_y = gr_y + 48
    draw.text((colA_x + 28, el_y), "엘레베이션 & 뎁스 토큰 (Elevation Hierarchy):", font=get_font(9, 'bold'), fill=(71, 85, 105))
    elevations = [
        ("Elevation 1 (2dp)", "Y:2 Blur:4", "장부 카드 서피스"),
        ("Elevation 2 (8dp)", "Y:8 Blur:16", "청구서 팝오버 모달"),
        ("Elevation 3 (16dp)", "Y:16 Blur:24", "키오스크 다이얼 패드"),
    ]
    el_w = (col_w_inner - 16) // 3
    for idx, (el_title, el_spec, el_use) in enumerate(elevations):
        ex = colA_x + 28 + idx * (el_w + 8)
        ey = el_y + 14
        draw.rounded_rectangle([ex, ey, ex + el_w, ey + 42], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((ex + 8, ey + 6), el_title, font=get_font(7.5, 'bold'), fill=(15, 23, 42))
        draw.text((ex + 8, ey + 18), el_spec, font=get_num_font(7, 'medium'), fill=(0, 82, 255))
        draw.text((ex + 8, ey + 29), el_use, font=get_font(6.8, 'regular'), fill=(100, 116, 139))
        
    # 2. Right Half: Typography Scale & Spatial Rules
    ty_x = colA_x + 28 + col_w_inner + 20
    ty_w = col_w_inner
    
    t_rows = [
        ("Display 28", "ExtraBold", "체크앤페이 0.8s 키오스크", False),
        ("Title 20", "Bold", "김도윤 원생 출결 완료", False),
        ("Subhead 16", "SemiBold", "수납 잔여 8회 · 만료 D-3", False),
        ("Body 14", "Regular", "학부모 카카오톡 청구서 발송", False),
        ("Caption 11", "Medium", "SQLite 로컬 볼트 ACID 커밋 완료", False),
    ]
    ty_start = r2_y + 64
    for i, (t_role, t_weight, t_sample, is_mono) in enumerate(t_rows):
        ry = ty_start + i * 25
        draw.rounded_rectangle([ty_x, ry, ty_x + ty_w, ry + 21], radius=5, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((ty_x + 8, ry + 4), t_role, font=get_font(8.5, 'bold'), fill=(0, 82, 255))
        draw.text((ty_x + 85, ry + 4), t_weight, font=get_font(8, 'medium'), fill=(100, 116, 139))
        draw.text((ty_x + ty_w - 8, ry + 4), t_sample, font=get_num_font(9, 'bold') if is_mono else get_font(8, 'semibold'), fill=(15, 23, 42), anchor='ra')
        
    sp_box_y = ty_start + len(t_rows) * 25 + 6
    sp_box_h = (r2_y + r2_h - 26) - sp_box_y
    draw.rounded_rectangle([ty_x, sp_box_y, ty_x + ty_w, sp_box_y + sp_box_h], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    
    draw.text((ty_x + 12, sp_box_y + 9), "코너 라운드 & 스페이싱 토큰 규칙 (Foundation Rules)", font=get_font(9.5, 'bold'), fill=(0, 82, 255))
    draw_pill_badge(draw, cx=ty_x + ty_w - 44, cy=sp_box_y + 16, text="8pt Grid", font=get_font(7.5, 'bold'), theme='blue', has_dot=False, pad_x=5, height=16)
    
    r_swatches = [
        ("radius.sm", "8px", 8, "다이얼 · 태그"),
        ("radius.md", "12px", 12, "버튼 · 인풋창"),
        ("radius.lg", "16px", 16, "장부 카드 · 모달"),
        ("radius.full", "999px", 19, "키오스크 뱃지"),
    ]
    rw_item = (ty_w - 24 - 18) // 4
    r_y = sp_box_y + 28
    for idx, (r_token, r_val, r_px, r_usage) in enumerate(r_swatches):
        rx = ty_x + 12 + idx * (rw_item + 6)
        draw.rounded_rectangle([rx, r_y, rx + rw_item, r_y + 46], radius=r_px, fill=(255, 255, 255), outline=(0, 82, 255), width=1)
        draw.rounded_rectangle([rx + 4, r_y + 4, rx + rw_item - 4, r_y + 18], radius=max(2, r_px - 3), fill=(240, 246, 255))
        draw.text((rx + rw_item // 2, r_y + 11), f"R {r_val}", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
        draw.text((rx + rw_item // 2, r_y + 25), r_token, font=get_num_font(6.8, 'bold'), fill=(15, 23, 42), anchor='mm')
        draw.text((rx + rw_item // 2, r_y + 36), r_usage, font=get_font(6.5, 'regular'), fill=(100, 116, 139), anchor='mm')
        
    sy_line = r_y + 52
    draw.text((ty_x + 12, sy_line), "• 스페이싱 토큰 (Spatial Scale): 4·8·12·16·24·32pt 기반 베이스라인 그리드", font=get_font(8, 'regular'), fill=(71, 85, 105))
    draw.text((ty_x + 12, sy_line + 14), "• 고정폭 숫자 (Tabular Figures): 실시간 출결 카운트/D-Day 계산 시 글자 흔들림 차단", font=get_font(8, 'regular'), fill=(71, 85, 105))
    draw.text((ty_x + 12, sy_line + 28), "• 3-Tier 토큰 파이프라인: Global(Primitive) → Semantic(Context) → Component 1:1 바인딩", font=get_font(8, 'bold'), fill=(0, 82, 255))
    
    draw.text((colA_x + 28, r2_y + r2_h - 17), "• WCAG 2.1 AAA 12.8:1 초고대비율 준수 · 디자인 시스템 시맨틱 토큰 100% 동기화 아키텍처", font=get_font(9, 'regular'), fill=(100, 116, 139))
    
    # -------------------------------------------------------------
    # CARD 05 (Lower Right): ATOMIC UI COMPONENT KIT
    # -------------------------------------------------------------
    draw.rounded_rectangle([colB_x, r2_y, colB_x + colB_w, r2_y + r2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b5_box = draw_pill_badge(draw, left_x=colB_x + 28, cy=r2_y + 32, text="FOUNDATION 05", font=get_font(9.5, 'bold'), theme='cyan', has_dot=True, pad_x=8, height=22)
    draw.text((b5_box[2] + 14, r2_y + 32), "프로덕션 아토믹 UI 컴포넌트 킷", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(colB_x + 28, r2_y + 54), (colB_x + colB_w - 28, r2_y + 54)], fill=(241, 245, 249), width=1)
    
    k1_y = r2_y + 68
    k1_w = (colB_w - 56 - 20) // 2
    
    # 1. Kiosk Dial Input Box
    draw.rounded_rectangle([colB_x + 28, k1_y, colB_x + 28 + k1_w, k1_y + 80], radius=10, fill=(248, 250, 252), outline=(0, 82, 255), width=2)
    draw.text((colB_x + 40, k1_y + 10), "키오스크 전화번호 4자리 인풋", font=get_font(9.5, 'bold'), fill=(0, 82, 255))
    draw.text((colB_x + 40, k1_y + 30), "5  8  2  4", font=get_num_font(15, 'black'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=colB_x + 28 + k1_w - 40, cy=k1_y + 26, text="0.8s MATCH", font=get_font(8, 'bold'), theme='blue', has_dot=False, pad_x=5, height=18)
    
    draw.rounded_rectangle([colB_x + 40, k1_y + 50, colB_x + 28 + k1_w - 12, k1_y + 72], radius=5, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    mat_font_btn = get_material_icon_font(15)
    draw.text((colB_x + 58, k1_y + 61), chr(0xf6be), font=mat_font_btn, fill=(0, 82, 255), anchor='mm')
    draw.text((colB_x + 28 + k1_w // 2, k1_y + 61), "김도윤 원생 (매칭 완료)", font=get_font(9.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((colB_x + 28 + k1_w - 28, k1_y + 61), chr(0xe156), font=mat_font_btn, fill=(16, 185, 129), anchor='mm')
    
    # 2. Ledger D-Day Card Box
    k2_x = colB_x + 28 + k1_w + 20
    draw.rounded_rectangle([k2_x, k1_y, k2_x + k1_w, k1_y + 80], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((k2_x + 14, k1_y + 10), "수납 상태 요약 & D-Day 뱃지", font=get_font(9.5, 'bold'), fill=(0, 82, 255))
    draw.text((k2_x + 14, k1_y + 30), "이번 달 총 수납액 ₩ 6,800,000", font=get_font(13, 'bold'), fill=(15, 23, 42))
    draw.text((k2_x + 14, k1_y + 54), "미수금 ₩ 480,000 (2명 연체 관리)", font=get_font(9.5, 'bold'), fill=(239, 68, 68))
    
    tog_x = k2_x + k1_w - 110
    draw.rounded_rectangle([tog_x, k1_y + 10, tog_x + 95, k1_y + 32], radius=11, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.rounded_rectangle([tog_x + 2, k1_y + 12, tog_x + 48, k1_y + 30], radius=9, fill=(0, 82, 255))
    draw.text((tog_x + 25, k1_y + 21), "월간", font=get_font(8, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((tog_x + 72, k1_y + 21), "회차", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    
    # 3. Preset Chips Row
    ch_y = k1_y + 92
    draw.text((colB_x + 28, ch_y + 6), "수강권/출결 프리셋 칩:", font=get_font(10, 'bold'), fill=(100, 116, 139))
    presets = [
        ("등원 인증", (0, 82, 255), (239, 246, 255)),
        ("하원 체크", (8, 145, 178), (236, 254, 255)),
        ("D+ 연체", (239, 68, 68), (254, 242, 242)),
        ("D-7 임박", (245, 158, 11), (254, 243, 199)),
        ("+10회 충전", (0, 82, 255), (239, 246, 255)),
        ("카톡 청구서", (59, 30, 30), (254, 229, 0)),
        ("로컬 백업", (16, 185, 129), (236, 253, 245)),
    ]
    cur_ch_x = colB_x + 185
    for p_txt, p_col, p_bg in presets:
        draw.rounded_rectangle([cur_ch_x, ch_y, cur_ch_x + 82, ch_y + 26], radius=13, fill=p_bg, outline=p_col, width=1)
        draw.text((cur_ch_x + 41, ch_y + 13), p_txt, font=get_font(9.5, 'bold'), fill=p_col, anchor='mm')
        cur_ch_x += 89
        
    # 4. CTAs Button Row
    cta_y = ch_y + 38
    mat_font_cta = get_material_icon_font(15)
    
    draw.rounded_rectangle([colB_x + 28, cta_y, colB_x + 230, cta_y + 40], radius=10, fill=(0, 82, 255))
    draw.text((colB_x + 50, cta_y + 20), chr(0xe156), font=mat_font_cta, fill=(255, 255, 255), anchor='mm')
    draw.text((colB_x + 138, cta_y + 20), "0.8초 등원 인증", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    draw.rounded_rectangle([colB_x + 242, cta_y, colB_x + 432, cta_y + 40], radius=10, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw.text((colB_x + 264, cta_y + 20), chr(0xf0161), font=mat_font_cta, fill=(0, 82, 255), anchor='mm')
    draw.text((colB_x + 347, cta_y + 20), "원클릭 카톡 청구", font=get_font(11, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    draw.rounded_rectangle([colB_x + 444, cta_y, colB_x + 614, cta_y + 40], radius=10, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((colB_x + 466, cta_y + 20), chr(0xf878), font=mat_font_cta, fill=(51, 65, 85), anchor='mm')
    draw.text((colB_x + 538, cta_y + 20), "1-Tap 볼트 백업", font=get_font(10.5, 'bold'), fill=(51, 65, 85), anchor='mm')
    
    draw.rounded_rectangle([colB_x + 626, cta_y, colB_x + colB_w - 28, cta_y + 40], radius=10, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw.text((colB_x + 648, cta_y + 20), chr(0xf01d5), font=get_material_icon_font(18), fill=(217, 119, 6), anchor='mm')
    draw.text((colB_x + 664 + (colB_w - 28 - 664)//2, cta_y + 12), "체크앤페이 프로 멤버십", font=get_font(8.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((colB_x + 664 + (colB_w - 28 - 664)//2, cta_y + 26), "평생 소장 라이선스 활성화", font=get_font(8.5, 'bold'), fill=(217, 119, 6), anchor='mm')
    
    # 5. Status Badges Row
    bdg_y = cta_y + 50
    draw.text((colB_x + 28, bdg_y + 6), "상태 뱃지 시스템:", font=get_font(10, 'bold'), fill=(100, 116, 139))
    badges = [
        ("0.8s 키오스크", "blue", True),
        ("D-Day 장부 정렬", "amber", True),
        ("미수금 92% 회수", "green", True),
        ("연체 경고 알림", "red", True),
        ("100% 로컬 볼트", "slate", True),
        ("Flutter 60fps", "purple", False),
    ]
    cur_bx = colB_x + 145
    for b_txt, b_thm, b_dt in badges:
        _, _, b_end, _ = draw_pill_badge(draw, left_x=cur_bx, cy=bdg_y + 14, text=b_txt, font=get_font(9.5, 'bold'), theme=b_thm, has_dot=b_dt, dark_mode=False, pad_x=8, height=24)
        cur_bx = b_end + 8
        
    draw.text((colB_x + 28, r2_y + r2_h - 18), "• 파운데이션 토큰 100% 바인딩: R8/R12/R16 라운딩, 4/8pt 스페이싱, 시맨틱 컬러가 Flutter 컴포넌트 트리에 실시간 동기화", font=get_font(9, 'regular'), fill=(100, 116, 139))
    
    draw_slide_footer(draw, 7)
    save_slide(base.convert('RGB'), 7)
    print("SAVED perfect Slide 07 (Visual Identity, App Icon & 24dp Iconography System) successfully!")


# ==============================================================
# SLIDE 08: CORE FEATURE DEEP DIVE 01 - 0.8s KIOSK ENGINE
# ==============================================================
def make_slide_08():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    lx = 100
    lw = 490
    draw_pill_badge(draw, left_x=lx, cy=78, text="08 CORE FEATURE | 0.8s KIOSK ATTENDANCE DOCK", font=get_font(10.5, 'bold'), theme='blue', pad_x=10, height=26)
    
    t1_a = "복잡한 카드 태그 없이 "
    t1_b = "번호 4자리로,"
    font_title = get_font(33, 'extrabold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((lx, 116), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((lx + w_t1_a, 116), t1_b, font=font_title, fill=(0, 81, 255))
    
    t2_a = "0.8초 만에 "
    t2_b = "출결과 차감을 완성해요."
    w_t2_a = draw.textlength(t2_a, font=font_title)
    draw.text((lx, 158), t2_a, font=font_title, fill=(0, 81, 255))
    draw.text((lx + w_t2_a, 158), t2_b, font=font_title, fill=(15, 23, 42))
    
    draw.text((lx, 210), "바코드 리더기나 지문 인식기 고장 없이, 원생이 직접 전화번호 뒤 4자리만 터치하면 즉각 인증 완결", font=get_font(13.5, 'regular'), fill=(71, 85, 105))
    
    # Left Comparison Card (Traditional vs ZeroPass)
    comp_y = 260
    comp_h = 680
    draw.rounded_rectangle([lx, comp_y, lx + lw, comp_y + comp_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=comp_y + 30, text="PARADIGM COMPARISON", font=get_font(9.5, 'bold'), theme='slate', pad_x=8, height=22)
    draw.text((lx + 24, comp_y + 58), "기존 아날로그 출결 vs 체크앤페이 원터치 키오스크", font=get_font(14.5, 'bold'), fill=(15, 23, 42))
    
    # Traditional
    draw.rounded_rectangle([lx + 24, comp_y + 95, lx + lw - 24, comp_y + 280], radius=12, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((lx + 40, comp_y + 115), "기존 종이 장부 & 바코드 카드 출결", font=get_font(13.5, 'bold'), fill=(220, 38, 38))
    t_bullets = [
        "• 종이 출석부에 손으로 이름을 적느라 원생 대기 줄 발생",
        "• 실물 카드 분실 시 재발급 비용 및 출결 누락",
        "• 수업 시작 전 15~20분 동안 강사가 출결 확인에 매달림"
    ]
    for b_idx, b in enumerate(t_bullets):
        draw.text((lx + 40, comp_y + 150 + b_idx * 38), b, font=get_font(12, 'regular'), fill=(127, 29, 29))
        
    # ZeroPass
    draw.rounded_rectangle([lx + 24, comp_y + 305, lx + lw - 24, comp_y + 645], radius=12, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx + 40, comp_y + 325), "체크앤페이 1초 원터치 키오스크 혁신", font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    z_bullets = [
        ("4자리 번호 인덱스 매칭", "SQLite 번호 역색인으로 입력 즉시 10ms 내 원생 자동 감지"),
        ("등원 / 하원 원터치 분기", "오늘 이미 등원한 원생은 하원 버튼으로 자동 스위칭"),
        ("오늘 출결 타임라인", "우측 화면에 실시간 등원 로그가 순차 렌더링되어 교차 검증"),
        ("학부모 알림 연동", "출결 즉시 등록된 연락처로 안전 도착 확인 메시지 전송")
    ]
    zy = comp_y + 365
    for z_tit, z_desc in z_bullets:
        draw.text((lx + 40, zy), "✔ " + z_tit, font=get_font(13, 'bold'), fill=(0, 82, 255))
        draw.text((lx + 40, zy + 24), z_desc, font=get_font(11.5, 'regular'), fill=(51, 65, 85))
        zy += 65

    # Center Mockup Device (Mockup 01 Pass - Toast Free)
    m1_path = f"{MOCKUP_DIR}/mockup_01_pass.png"
    if os.path.exists(m1_path):
        m1 = Image.open(m1_path).convert('RGBA')
        scale_h = 750
        dev1 = m1.resize((int(m1.width * (scale_h / m1.height)), scale_h), Image.Resampling.LANCZOS)
        pos1 = (620, 190)
        sh1, pad1 = make_shadow(dev1, blur=44, alpha=80)
        base.paste(sh1, (pos1[0] - pad1[0], pos1[1] - pad1[1]), sh1)
        base.paste(dev1, pos1, dev1)
    
    # Right Column: Flow Architecture & Metrics (x=1050 to 1820)
    rx = 1050
    rw = 770
    draw.rounded_rectangle([rx, comp_y, rx + rw, comp_y + comp_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 24, cy=comp_y + 30, text="INTERACTIVE FLOW & TELEMETRY", font=get_font(9.5, 'bold'), theme='blue', pad_x=8, height=22)
    draw.text((rx + 24, comp_y + 58), "초고속 출결 엔진의 기술적 무결성 지표", font=get_font(15, 'bold'), fill=(15, 23, 42))
    
    flow_cards = [
        ("0.8s 초고속 인증 속도", "터치 입력부터 SQLite 커밋 완료 및 화면 피드백까지 전 과정 0.8초 완료"),
        ("오인증 방지 2차 확인 모달", "동일한 뒷번호 4자리 보유 원생 감지 시 즉시 이름 선택 모달 팝업"),
        ("하원 잔여 수업 회차 자동 차감", "수강권 종류(월정기/회차)에 맞춘 실시간 자동 차감 트랜잭션"),
        ("100% 오프라인 동작 보증", "학원 인터넷 장애 시에도 멈춤 없이 SQLite 로컬 볼트에 무손실 커밋")
    ]
    
    f_y = comp_y + 95
    for f_tit, f_desc in flow_cards:
        draw.rounded_rectangle([rx + 24, f_y, rx + rw - 24, f_y + 70], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=rx + 40, cy=f_y + 24, text="ENGINE SPEC", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18)
        draw.text((rx + 140, f_y + 24), f_tit, font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((rx + 40, f_y + 50), f_desc, font=get_font(11.5, 'regular'), fill=(71, 85, 105))
        f_y += 82
        
    # Telemetry KPI Strip at Bottom of Right Box
    tel_y = comp_y + comp_h - 180
    draw.rounded_rectangle([rx + 24, tel_y, rx + rw - 24, comp_y + comp_h - 24], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((rx + 40, tel_y + 20), "CORE ENGINE TELEMETRY METRICS", font=get_font(10.5, 'bold'), fill=(0, 82, 255))
    
    kpis = [
        ("출결 인증 속도", "0.8초", "기존 45초 대비 98% 단축"),
        ("원생 식별 지연", "10ms", "SQLite B-Tree 인덱싱"),
        ("오프라인 보존율", "100%", "ACID 트랜잭션 보장"),
        ("UI 렌더링 레이턴시", "16.6ms", "Flutter 60fps 유지")
    ]
    tkw = (rw - 48 - 30) // 4
    for kidx, (k_name, k_val, k_sub) in enumerate(kpis):
        kx = rx + 40 + kidx * (tkw + 10)
        ky = tel_y + 44
        draw.text((kx, ky), k_name, font=get_font(10, 'medium'), fill=(100, 116, 139))
        draw.text((kx, ky + 24), k_val, font=get_num_font(18, 'black'), fill=(0, 82, 255))
        draw.text((kx, ky + 48), k_sub, font=get_font(8.5, 'regular'), fill=(71, 85, 105))

    draw_slide_footer(draw, 8)
    save_slide(base.convert('RGB'), 8)
    print("SAVED perfect Slide 08 (0.8s Kiosk Attendance Dock) successfully!")
