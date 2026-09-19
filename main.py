#!/usr/bin/env python3
"""
DTDC Bill Generator - PC Version (CLI)
Usage: python main.py

Workflow:
1. Paste your DTDC shipping label image into input_images/ folder (like you do here)
2. Run this script
3. Enter Consignor Name, Address, Contact, Courier Charges
4. Get PDF + PNG + HTML in invoices/ folder
"""

import os
from pathlib import Path
from generator.dtdc_generator import extract_text_from_image, parse_dtdc_fields, generate_invoice

def main():
    print("=== DTDC Bill Generator - PC Version ===")
    print("Remembered Settings: Custom Logo = assets/DTDC_logo.png, Same Format\n")

    input_dir = Path("input_images")
    input_dir.mkdir(exist_ok=True)
    # Keep .gitkeep
    (input_dir / ".gitkeep").touch(exist_ok=True)

    # Find latest image in input_images
    images = list(input_dir.glob("*.png")) + list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg")) + list(input_dir.glob("*.pdf"))
    images = [p for p in images if p.name != ".gitkeep"]

    data = {}
    if images:
        latest = max(images, key=lambda p: p.stat().st_mtime)
        print(f"Found input image: {latest}")
        raw_text = extract_text_from_image(latest)
        parsed = parse_dtdc_fields(raw_text)
        data.update(parsed)
        print(f"OCR Extracted: {parsed}")
    else:
        print("No image found in input_images/. Please paste your shipping label image there (e.g., image.png)")
        print("Using manual entry only.")

    # Manual inputs - like you do here
    print("\n--- Enter Consignor Details (Manual Override) ---")
    consignor_name = input(f"Consignor Name [{data.get('consignor_name','Sandeep kumar pandey')}]: ").strip() or data.get('consignor_name','Sandeep kumar pandey')
    consignor_address = input(f"Consignor Address [{data.get('consignor_address','177/02, Hardua mohalla near gayatri mandir, Nagod 485446')}]: ").strip() or data.get('consignor_address','177/02, Hardua mohalla near gayatri mandir, Nagod 485446')
    consignor_phone = input(f"Consignor Contact [{data.get('consignor_phone','9179797484')}]: ").strip() or data.get('consignor_phone','9179797484')
    courier_charges = input(f"Courier Charges ₹ [{data.get('courier_charges','220')}]: ").strip() or data.get('courier_charges','220')

    data['consignor_name'] = consignor_name
    data['consignor_address'] = consignor_address
    data['consignor_phone'] = consignor_phone
    data['courier_charges'] = courier_charges

    # Ensure some defaults if OCR didn't find
    if 'origin' not in data:
        data['origin'] = input("Origin [SATNA]: ").strip() or "SATNA"
    if 'dest' not in data:
        data['dest'] = input("Dest [TRICHUR]: ").strip() or "TRICHUR"
    if 'awb' not in data:
        data['awb'] = input("AWB No [7X117632485]: ").strip() or "7X117632485"

    logo_path = "assets/DTDC_logo.png"
    output_dir = "invoices"

    print("\nGenerating invoice with your custom logo and same format...")
    result = generate_invoice(data, logo_path, output_dir)

    print("\n✅ Generated Successfully!")
    print(f"PDF: {result['pdf']}")
    print(f"PNG HighRes: {result['png_high']}")
    print(f"PNG: {result['png']}")
    print(f"HTML: {result['html']}")
    print("\nAll files are systematic in invoices/PDF, invoices/PNG, invoices/HTML")

if __name__ == "__main__":
    main()
