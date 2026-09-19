@echo off
echo Installing...
pip install customtkinter reportlab python-barcode Pillow pyinstaller
echo Building Premium Dashboard EXE (Full Window)...
pyinstaller --onefile --windowed --name DTDC_Bill_Generator --add-data "assets;assets" --add-data "generator;generator" --collect-all barcode --hidden-import=barcode --hidden-import=barcode.writer --hidden-import=generator --hidden-import=generator.dtdc_generator --hidden-import=reportlab --hidden-import=PIL --hidden-import=customtkinter app_dashboard.py --clean -y
echo EXE built in dist\DTDC_Bill_Generator.exe - Full Window Dashboard!
pause
