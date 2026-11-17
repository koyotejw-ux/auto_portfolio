import os

target_path = r'd:\097.flutter_project\auto_portfolio\zeropass\deck_slides_white_05_08.py'
with open(target_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the icons_data in Slide 07 with the exact 8 production icons verified in Check & Pay
old_block = '''    icons_data = [
        ("출결 키오스크", "Icons.dialpad_rounded", 0xf6be),
        ("D-Day 수납장부", "Icons.payments_rounded", 0xf002a),
        ("원생 디렉터리", "Icons.people_rounded", 0xf0062),
        ("원클릭 청구서", "Icons.send_rounded", 0xf0161),
        ("로컬 보안볼트", "Icons.lock_rounded", 0xf878),
        ("프로 라이선스", "Icons.stars_rounded", 0xf01d5),
        ("출결 타임라인", "Icons.history_rounded", 0xf7f0),
        ("출석 인증 완료", "Icons.fact_check_rounded", 0xf735),
    ]'''

new_block = '''    icons_data = [
        ("출결 체크패스", "Icons.fact_check_rounded", 0xf735),
        ("수납 청구장부", "Icons.receipt_long_rounded", 0xf00b6),
        ("지출 세무장부", "Icons.account_balance_wallet_rounded", 0xf520),
        ("원생 디렉터리", "Icons.groups_rounded", 0xf0dc),
        ("환경설정 볼트", "Icons.tune_rounded", 0xf0244),
        ("카카오 알림톡", "Icons.chat_bubble_rounded", 0xf635),
        ("스튜디오 보안", "Icons.lock_rounded", 0xf878),
        ("프로 라이선스", "Icons.workspace_premium_rounded", 0xf0289),
    ]'''

if old_block in text:
    text = text.replace(old_block, new_block, 1)
    print("Replaced icons_data successfully!")
else:
    print("Could not find old_block in text!")

# Also verify CTA button in Card 05
old_cta_check = 'draw.text((colB_x + 50, cta_y + 20), chr(0xe156), font=mat_font_cta, fill=(255, 255, 255), anchor=\'mm\')'
new_cta_check = 'draw.text((colB_x + 50, cta_y + 20), chr(0xf735), font=mat_font_cta, fill=(255, 255, 255), anchor=\'mm\')'
if old_cta_check in text:
    text = text.replace(old_cta_check, new_cta_check, 1)
    print("Replaced CTA button icon with fact_check_rounded successfully!")

# Also verify Kiosk dial button inside card 05
old_dial_icon = 'draw.text((colB_x + 58, k1_y + 61), chr(0xf6be), font=mat_font_btn, fill=(0, 82, 255), anchor=\'mm\')'
new_dial_icon = 'draw.text((colB_x + 58, k1_y + 61), chr(0xf735), font=mat_font_btn, fill=(0, 82, 255), anchor=\'mm\')'
if old_dial_icon in text:
    text = text.replace(old_dial_icon, new_dial_icon, 1)
    print("Replaced Kiosk dial input icon successfully!")

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated deck_slides_white_05_08.py successfully!")

