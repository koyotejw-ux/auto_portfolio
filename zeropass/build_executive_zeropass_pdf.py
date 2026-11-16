import os
import fitz # PyMuPDF
from PIL import Image

def build_pdf():
    print("=== Building Enterprise ZeroPass_Portfolio.pdf (1:1 Native Full-Scale Bleed-to-Edge) ===")
    
    slides_dir = r"d:\097.flutter_project\auto_portfolio\zeropass\behance_slides"
    
    target_pdfs = [
        r"d:\097.flutter_project\auto_portfolio\zeropass\ZeroPass_Portfolio.pdf",
        r"d:\097.flutter_project\zeropass\portfolio\ZeroPass_Portfolio.pdf"
    ]
    
    doc = fitz.open()
    proto_url = "https://koyotejw-ux.github.io/zeropass/portfolio/index.html"
    
    for i in range(1, 13):
        slide_path = os.path.join(slides_dir, f"slide_{i:02d}.png")
        if not os.path.exists(slide_path):
            raise FileNotFoundError(f"Slide not found: {slide_path}")
            
        page = doc.new_page(width=1920, height=1080)
        page.insert_image(fitz.Rect(0, 0, 1920, 1080), filename=slide_path)
        
        # Interactive hyperlinks mapped to exact 1920x1080 design coordinates
        if i == 10:
            # 5 Core Mockup Devices & Bottom Pipeline Chips
            for rx1, ry1, rx2, ry2 in [
                (100, 205, 415, 840), (450, 205, 765, 840), (800, 205, 1115, 840),
                (1150, 205, 1465, 840), (1500, 205, 1815, 840)
            ]:
                page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(rx1, ry1, rx2, ry2), 'uri': proto_url})
                
        elif i == 12:
            # Master launcher button & links
            for rx1, ry1, rx2, ry2 in [
                (130, 850, 905, 925), (100, 220, 935, 960)
            ]:
                page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(rx1, ry1, rx2, ry2), 'uri': proto_url})
                
        print(f"Page {i:02d} inserted 1:1 without margin/downscaling.")
        
    doc.set_metadata({
        'title': 'ZeroPass (체크앤페이) Portfolio Deck',
        'author': 'Lead UX/UI Designer JAEWOONG JUNG',
        'subject': 'Executive Behance Portfolio Deck (12 Slides, 1920x1080 Full Bleed)',
        'keywords': 'ZeroPass, Check&Pay, Kiosk, Attendance, Ledger, ERP, SQLite, Flutter, UI/UX, Portfolio'
    })
    
    for target_pdf in target_pdfs:
        os.makedirs(os.path.dirname(target_pdf), exist_ok=True)
        doc.save(target_pdf, deflate=True, garbage=4)
        print(f"Successfully compiled: {target_pdf} ({os.path.getsize(target_pdf):,} bytes)")
        
    doc.close()
    print("ZeroPass PDF export complete!")

if __name__ == "__main__":
    build_pdf()

