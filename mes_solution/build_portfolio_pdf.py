import os
from PIL import Image

slide_dir = r"d:\097.flutter_project\auto_portfolio\mes_solution\behance_slides"
pdf_path = r"d:\097.flutter_project\auto_portfolio\mes_solution\MES_Solution_Portfolio.pdf"

image_files = [os.path.join(slide_dir, f"slide_{i:02d}.png") for i in range(1, 13)]
images = []

for f in image_files:
    if os.path.exists(f):
        img = Image.open(f).convert("RGB")
        images.append(img)
    else:
        print(f"Warning: Missing {f}")

if images:
    images[0].save(pdf_path, save_all=True, append_images=images[1:], quality=95)
    print(f"Generated PDF: {pdf_path} ({len(images)} slides)")
else:
    print("No images found to generate PDF!")

