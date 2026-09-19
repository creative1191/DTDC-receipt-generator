#!/bin/bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --name DTDC_Bill_Generator --add-data "assets:assets" --add-data "generator/templates:generator/templates" --collect-all barcode --collect-all weasyprint --hidden-import=barcode --hidden-import=barcode.writer --hidden-import=barcode.charsets --hidden-import=fitz --hidden-import=PIL app_gui.py --clean -y
echo "Binary built in ../DTDC_exe/DTDC_Bill_Generator or dist/"
