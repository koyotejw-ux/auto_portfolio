import os
import fitz # PyMuPDF

def build_pdf():
    print("=== Building Enterprise FortuneMatch_Portfolio.pdf (1920x1080 1:1 True DPI) ===")
    
    slides_dir = r"d:\097.flutter_project\auto_portfolio\ftmt\behance_slides"
    target_pdfs = [
        r"d:\097.flutter_project\auto_portfolio\ftmt\FortuneMatch_Portfolio.pdf",
        r"d:\097.flutter_project\ftmt\portfolio\FortuneMatch_Portfolio.pdf"
    ]
    
    doc = fitz.open()
    
    # Live URLs for interactive links
    proto_url = "https://koyotejw-ux.github.io/ftmt/portfolio/index.html"
    
    for i in range(1, 13):
        slide_path = os.path.join(slides_dir, f"slide_{i:02d}.png")
        if not os.path.exists(slide_path):
            raise FileNotFoundError(f"Slide not found: {slide_path}")
            
        # Create page with exact 1920x1080 dimensions (1:1 with PNG resolution)
        page = doc.new_page(width=1920, height=1080)
        page.insert_image(fitz.Rect(0, 0, 1920, 1080), filename=slide_path)
        
        # Add rich interactive hyperlinks identical to Smart DCA PDF standard
        if i == 10:
            # Slide 10: 6 Core Mobile Mockups & Journey Links
            # Screen 1: Hub
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(130, 205, 340, 780), 'uri': proto_url})
            # Screen 2: Radar
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(420, 205, 630, 780), 'uri': proto_url})
            # Screen 3: Match
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(710, 205, 920, 780), 'uri': proto_url})
            # Screen 4: Tarot
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(1000, 205, 1210, 780), 'uri': proto_url})
            # Screen 5: Vault
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(1290, 205, 1500, 780), 'uri': proto_url})
            # Screen 6: Shop
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(1580, 205, 1790, 780), 'uri': proto_url})
            
            # Bottom Pipeline steps
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(300, 920, 500, 970), 'uri': proto_url})
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(560, 920, 770, 970), 'uri': proto_url})
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(830, 920, 1040, 970), 'uri': proto_url})
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(1100, 920, 1310, 970), 'uri': proto_url})
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(1370, 920, 1570, 970), 'uri': proto_url})
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(1630, 920, 1800, 970), 'uri': proto_url})
            
        elif i == 12:
            # Slide 12: Prototype Interactive Hub
            # Left side phone mockup
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(100, 205, 760, 850), 'uri': proto_url})
            # Left bottom spec card
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(100, 865, 760, 980), 'uri': proto_url})
            # Master launcher
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(800, 196, 1820, 348), 'uri': proto_url})
            # 4 Step cards
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(800, 365, 1820, 440), 'uri': proto_url})
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(800, 450, 1820, 525), 'uri': proto_url})
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(800, 535, 1820, 610), 'uri': proto_url})
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(800, 620, 1820, 695), 'uri': proto_url})
            # QR code card
            page.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(800, 710, 1820, 980), 'uri': proto_url})
            
        print(f"Page {i:02d} rendered into PDF (1920x1080 points, 1:1 lossless).")

    # Metadata
    doc.set_metadata({
        'title': 'FortuneMatch (포춘매치) - Behance Enterprise Case Study & UX/UI Architecture',
        'author': 'Lead UX/UI Designer & Service Planner',
        'subject': 'FortuneMatch UX/UI Portfolio Deck',
        'keywords': 'Flutter, UX/UI, Portfolio, Behance, Cosmic Luxury, Saju, Zodiac',
        'creator': 'FortuneMatch Executive Generator',
        'producer': 'PyMuPDF Enterprise 1920x1080 Pipeline'
    })
    
    for pdf_out in target_pdfs:
        os.makedirs(os.path.dirname(pdf_out), exist_ok=True)
        doc.save(pdf_out, garbage=4, deflate=True)
        print(f"Saved: {pdf_out} ({os.path.getsize(pdf_out):,} bytes)")
        
    doc.close()
    print("=== PDF Build Complete Successfully! ===")

if __name__ == '__main__':
    build_pdf()
