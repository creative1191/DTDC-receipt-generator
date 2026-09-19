# GitHub se Direct EXE Kaise Banaye - Step by Step

## 🚀 GitHub pe Push Karte Hi Auto EXE Banega!

Ye repo me `.github/workflows/build-exe.yml` already add hai. Iska matlab aapko kuch extra karna nahi, bas GitHub pe push karo, EXE automatic ban jayega.

### Step 1: GitHub Repo Banao
1. GitHub.com pe jao → New Repository → `DTDC_Bill_Generator` naam do
2. Public/Private select karo → Create

### Step 2: Ye Folder Push Karo
```bash
cd DTDC_Bill_Generator_Github
git init
git add .
git commit -m "Initial commit - DTDC Bill Generator with auto EXE build"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/DTDC_Bill_Generator.git
git push -u origin main
```

### Step 3: EXE Download Karo (Auto Build)
1. GitHub repo me jao → **Actions** tab pe click karo
2. **Build DTDC EXE** workflow chal raha hoga (1-2 min)
3. Complete hone ke baad → Artifacts me milega:
   - `DTDC_Bill_Generator-Windows-EXE` → Windows ke liye `.exe`
   - `DTDC_Bill_Generator-Linux-Binary` → Linux ke liye binary
4. Download karo → Extract → Double click → Chalao!

### Local PC pe Direct EXE Build (Without GitHub)

#### Windows pe:
```bat
# build_exe_windows.bat pe double click karo
# Ya command prompt me:
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name DTDC_Bill_Generator --add-data "assets;assets" --add-data "generator/templates;generator/templates" app_gui.py
# EXE milega: dist\DTDC_Bill_Generator.exe
```

#### Linux pe:
```bash
chmod +x build_exe_linux.sh
./build_exe_linux.sh
# Binary milega: ../DTDC_exe/DTDC_Bill_Generator
```

### 💡 SnipTool Feature
- Windows: `Win + Shift + S` → Capture → App me `Paste SnipTool Image (Ctrl+V)` button
- Direct clipboard se image paste ho jayegi!

### 📁 Output
- PDF: `invoices/PDF/`
- PNG HighRes: `invoices/PNG/`
- HTML: `invoices/HTML/`

Bas itna hi! GitHub Actions se aapko local build ki bhi jarurat nahi, direct GitHub se EXE download kar sakte ho.
