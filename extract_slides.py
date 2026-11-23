import re

path = r'd:\097.flutter_project\average_down_calculator\generate_behance_slides.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

slides = re.split(r'def make_slide_', text)
for s in slides[1:]:
    num_match = re.match(r'(\d+)', s)
    num = num_match.group(1) if num_match else '?'
    
    cat = re.search(r'category_en\s*=\s*["\']([^"\']+)["\']', s)
    tb = re.search(r'title_black\s*=\s*["\']([^"\']+)["\']', s)
    tb_alt = re.search(r'title_p1\s*=\s*["\']([^"\']+)["\']', s)
    tblue = re.search(r'title_blue\s*=\s*["\']([^"\']+)["\']', s)
    tblue_alt = re.search(r'title_p2\s*=\s*["\']([^"\']+)["\']', s)
    sub = re.search(r'subtitle_kr\s*=\s*["\']([^"\']+)["\']', s)
    sub_alt = re.search(r'sub1\s*=\s*["\']([^"\']+)["\']', s)
    
    c = cat.group(1) if cat else "SMART DCA · UX/UI"
    t1 = tb.group(1) if tb else (tb_alt.group(1) if tb_alt else "")
    t2 = tblue.group(1) if tblue else (tblue_alt.group(1) if tblue_alt else "")
    st = sub.group(1) if sub else (sub_alt.group(1) if sub_alt else "")
    print(f"Slide {num}: [{c}] {t1} + {t2} | {st}")

