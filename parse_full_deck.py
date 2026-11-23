import os
import json
import re

path = r'd:\097.flutter_project\average_down_calculator\generate_behance_slides.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

slides_code = re.split(r'def make_slide_', text)

all_slides = []

for i in range(1, len(slides_code)):
    s = slides_code[i]
    num_m = re.match(r'(\d+)', s)
    num = int(num_m.group(1)) if num_m else i
    
    # Category
    cat_m = re.search(r'category_en\s*=\s*["\']([^"\']+)["\']', s)
    cat = cat_m.group(1) if cat_m else ("2026 CASE STUDY" if num == 1 else ("08 CORE FEATURE | 0.2s VOICE INPUT DOCK" if num == 8 else ("09 CORE FEATURE | CLOSED-FORM QUANT INVERSION" if num == 9 else f"{num:02d} SECTION")))
    
    # Title
    tb_m = re.search(r'title_black\s*=\s*["\']([^"\']+)["\']', s)
    tb_alt = re.search(r'title_p1\s*=\s*["\']([^"\']+)["\']', s)
    t1_a_m = re.search(r't1_a\s*=\s*["\']([^"\']+)["\']', s)
    
    tblue_m = re.search(r'title_blue\s*=\s*["\']([^"\']+)["\']', s)
    tblue_alt = re.search(r'title_p2\s*=\s*["\']([^"\']+)["\']', s)
    t1_b_m = re.search(r't1_b\s*=\s*["\']([^"\']+)["\']', s)
    
    sub_m = re.search(r'subtitle_kr\s*=\s*["\']([^"\']+)["\']', s)
    sub_alt = re.search(r'desc_text\s*=\s*["\']([^"\']+)["\']', s)
    sub_alt2 = re.search(r'sub1\s*=\s*["\']([^"\']+)["\']', s)
    
    title_black = tb_m.group(1) if tb_m else (tb_alt.group(1) if tb_alt else (t1_a_m.group(1) if t1_a_m else ""))
    title_blue = tblue_m.group(1) if tblue_m else (tblue_alt.group(1) if tblue_alt else (t1_b_m.group(1) if t1_b_m else ""))
    subtitle = sub_m.group(1) if sub_m else (sub_alt.group(1) if sub_alt else (sub_alt2.group(1) if sub_alt2 else ""))
    
    all_slides.append({
        'page': num,
        'category': cat,
        'titleBlack': title_black,
        'titleBlue': title_blue,
        'subtitle': subtitle,
    })

print(json.dumps(all_slides, ensure_ascii=False, indent=2))

