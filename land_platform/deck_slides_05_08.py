import os
from PIL import Image, ImageDraw
from deck_common import *

def make_slide_05():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 5, "USER JOURNEY MAP", "User Experience Journey", "사용자 6단계 여정 맵 (User Journey Map)", "인식-정보탐색-토지선택-규제확인-설계시도 전 과정의 행동, 생각, 페인포인트, 기회요인 도출")

    rx = 80
    rw = W - 160
    ry = 260
    rh = 690
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    j_path = os.path.join(ASSETS_DIR, "part_user_journey_map.png")
    if os.path.exists(j_path):
        j_img = Image.open(j_path).convert('RGBA')
        scale = min((rw - 60) / j_img.width, (rh - 60) / j_img.height)
        nw = int(j_img.width * scale)
        nh = int(j_img.height * scale)
        j_res = j_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(j_res, (rx + (rw - nw) // 2, ry + (rh - nh) // 2), j_res)

    draw_slide_footer(draw, 5, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_05.png"), quality=95)
    print("Generated slide_05.png")

def make_slide_06():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 6, "KEY INSIGHTS", "Strategic Design Insights", "리서치 기반 4대 핵심 전략 인사이트", "정보를 하나의 흐름으로 통합, 규제와 수익성 쉬운 판단, 시각적 설계 시뮬레이션, 초보자 맞춤 UX 흐름")

    rx = 80
    rw = W - 160
    ry = 260
    rh = 690
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    ins_path = os.path.join(ASSETS_DIR, "ref_04_key_insights.png")
    if os.path.exists(ins_path):
        ins_img = Image.open(ins_path).convert('RGBA')
        scale = min((rw - 60) / ins_img.width, (rh - 60) / ins_img.height)
        nw = int(ins_img.width * scale)
        nh = int(ins_img.height * scale)
        i_res = ins_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(i_res, (rx + (rw - nw) // 2, ry + (rh - nh) // 2), i_res)

    draw_slide_footer(draw, 6, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_06.png"), quality=95)
    print("Generated slide_06.png")

def make_slide_07():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 7, "INFORMATION ARCHITECTURE", "Platform Sitemap & Hierarchy", "토지개발 플랫폼 인포메이션 아키텍처 (IA)", "홈 기반 로그인/회원가입, 시뮬레이터(시작/통계), 사용자 통계, 마이페이지, 관리자 5대 핵심 메뉴 구조")

    rx = 80
    rw = W - 160
    ry = 260
    rh = 690
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    ia_path = os.path.join(ASSETS_DIR, "ref_05_ia_tree.png")
    if os.path.exists(ia_path):
        ia_img = Image.open(ia_path).convert('RGBA')
        scale = min((rw - 60) / ia_img.width, (rh - 60) / ia_img.height)
        nw = int(ia_img.width * scale)
        nh = int(ia_img.height * scale)
        ia_res = ia_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(ia_res, (rx + (rw - nw) // 2, ry + (rh - nh) // 2), ia_res)

    draw_slide_footer(draw, 7, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_07.png"), quality=95)
    print("Generated slide_07.png")

def make_slide_08():
    img = Image.new('RGB', (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)
    draw_slide_header(draw, 8, "USER FLOW & LOGIC", "End-to-End User Flow", "원스톱 토지개발 시뮬레이션 사용자 플로우", "메인(홈) → 시뮬레이션 시작 → 대상지 선택 → 토지분석 → 시설배치 → 스마트팜 설계 → 조성비/전체매출 → 분석 보고서 제공")

    rx = 80
    rw = W - 160
    ry = 260
    rh = 690
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=CARD_LIGHT, outline=BORDER_LIGHT, width=1)
    
    uf_path = os.path.join(ASSETS_DIR, "part_user_flow.png")
    if os.path.exists(uf_path):
        uf_img = Image.open(uf_path).convert('RGBA')
        scale = min((rw - 60) / uf_img.width, (rh - 60) / uf_img.height)
        nw = int(uf_img.width * scale)
        nh = int(uf_img.height * scale)
        u_res = uf_img.resize((nw, nh), Image.Resampling.LANCZOS)
        img.paste(u_res, (rx + (rw - nw) // 2, ry + (rh - nh) // 2), u_res)

    draw_slide_footer(draw, 8, 12, dark_mode=False)
    img.save(os.path.join(OUT_DIR, "slide_08.png"), quality=95)
    print("Generated slide_08.png")

if __name__ == '__main__':
    make_slide_05()
    make_slide_06()
    make_slide_07()
    make_slide_08()
