import re

for fn in ['deck_slides_01_04.py', 'deck_slides_05_08.py', 'deck_slides_09_12.py']:
    path = 'land_platform/' + fn
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
    for m in re.finditer(r'def (make_slide_\d\d)\(\):.*?draw_slide_header\(\s*draw,\s*\d+,\s*\"([^\"]+)\",\s*\"([^\"]+)\",\s*\"([^\"]+)\"', txt, re.DOTALL):
        print(f"{m.group(1)} | {m.group(2)} | {m.group(3)}{m.group(4)}")
