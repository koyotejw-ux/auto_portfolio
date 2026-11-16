import sys
from deck_slides_white_01_04 import make_slide_01, make_slide_02, make_slide_03, make_slide_04
from deck_slides_white_05_08 import make_slide_05, make_slide_06, make_slide_07, make_slide_08
from deck_slides_white_09_12 import make_slide_09, make_slide_10, make_slide_11, make_slide_12
from build_executive_zeropass_pdf import build_pdf

print("=== Starting Full Executive ZeroPass White-Theme Behance Deck Generation ===")

print("[1/12] Generating Slide 01: Hero Cover (White Style)...")
make_slide_01()

print("[2/12] Generating Slide 02: Market Research & Problem Study...")
make_slide_02()

print("[3/12] Generating Slide 03: Target & Persona Matrix...")
make_slide_03()

print("[4/12] Generating Slide 04: Information Architecture (IA)...")
make_slide_04()

print("[5/12] Generating Slide 05: User Flow & Experience Logic...")
make_slide_05()

print("[6/12] Generating Slide 06: Wireframe & Ergonomics...")
make_slide_06()

print("[7/12] Generating Slide 07: Visual Design System...")
make_slide_07()

print("[8/12] Generating Slide 08: Deep Dive 01 - Kiosk Attendance Engine...")
make_slide_08()

print("[9/12] Generating Slide 09: Deep Dive 02 - Smart D-Day Billing Ledger...")
make_slide_09()

print("[10/12] Generating Slide 10: Mobile Screens (Production Figma & Flutter)...")
make_slide_10()

print("[11/12] Generating Slide 11: Business Impact & Strategic Retrospective...")
make_slide_11()

print("[12/12] Generating Slide 12: Live Interactive Prototype (Obsidian Finale)...")
make_slide_12()

print("=== Compiling ZeroPass_Portfolio.pdf with PyMuPDF ===")
build_pdf()

print("=== All 12 White-Theme Slides & PDF Successfully Generated! ===")
