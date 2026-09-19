# 🔧 Workflow Missing Fix - Action me kuch nahi dikh raha to ye karo

## Problem: GitHub Actions me workflow nahi dikh raha
Reason: `.github` folder hidden hota hai, kabhi-kabhi GitHub web upload me skip ho jata hai.

## Solution 1: Manual Workflow Create Karo (2 min - Guaranteed Work)

1. GitHub repo me jao
2. **Add file** → **Create new file** pe click karo
3. File name dalo: `.github/workflows/build-exe.yml`  (exact same)
4. Niche wala pura code copy-paste karo:

```yaml
name: Build DTDC EXE

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build Windows EXE
        run: |
          pyinstaller --onefile --windowed --name DTDC_Bill_Generator --add-data "assets;assets" --add-data "generator/templates;generator/templates" --hidden-import=weasyprint --hidden-import=barcode --hidden-import=fitz --hidden-import=PIL app_gui.py --clean -y
      - name: Upload Windows EXE
        uses: actions/upload-artifact@v4
        with:
          name: DTDC_Bill_Generator-Windows-EXE
          path: dist/DTDC_Bill_Generator.exe
```

5. **Commit changes** → Direct to main branch
6. Ab **Actions tab** me jao → Workflow dikhega!

## Solution 2: Enable Actions
- Repo → Settings → Actions → General → Allow all actions → Save

## Solution 3: Branch Check
- Aapka default branch `main` hai ya `master`? Workflow ab dono pe chalega (main, master)

## Solution 4: Manual EXE Build (Without GitHub)
- Windows pe: `build_exe_windows.bat` pe double click karo
- EXE ban jayega: `dist/DTDC_Bill_Generator.exe`

## Still Not Working?
- Is repo ke `build-exe.yml` file ko download karo aur manually `.github/workflows/` me daalo
- Ya mujhe bolo, main alag se workflow file dunga

