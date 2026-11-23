import os
from PIL import Image

SLIDES_DIR = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/behance_slides'
PDF_PATH = 'd:/097.flutter_project/auto_portfolio/korea_history_quiz/Korea_History_Quiz_Portfolio.pdf'

slide_files = [os.path.join(SLIDES_DIR, f"slide_{i:02d}.png") for i in range(1, 13)]

images = []
for p in slide_files:
    if os.path.exists(p):
        im = Image.open(p).convert('RGB')
        images.append(im)
    else:
        print(f"Missing: {p}")

if images:
    images[0].save(
        PDF_PATH,
        save_all=True,
        append_images=images[1:],
        quality=92,
        optimize=True
    )
    print(f"Generated PDF: {PDF_PATH} ({len(images)} slides)")

