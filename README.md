# DTDC Bill Generator - PC Version

**GitHub Ready - Complete Separate Folder**

Ye wahi DTDC bill generator hai jo aap yaha use kar rahe ho, ab aapke PC ke liye.

### ✅ Features (Aapki Saved Settings Locked)
- **Custom Logo:** `assets/DTDC_logo.png` (aapka wala dark blue + red dot) hamesha use hoga
- **Same Format:** Original DTDC layout exact same - landscape, borders, barcode position, Risk Surcharge, footer sab preserved
- **Input:** Direct image paste karo `input_images/` folder me (jaise yaha karte ho)
- **Manual Override:** Sender Name, Address, Contact, Rate (₹) input karoge
- **Output:** Har baar **PDF + PNG HighRes + HTML** systematic folders me

### 📁 Folder Structure (Systematic)
```
DTDC_Bill_Generator_Github/
├── assets/
│   └── DTDC_logo.png          # Aapka custom logo (locked)
├── input_images/              # Yaha image paste karo directly
│   └── .gitkeep
├── invoices/
│   ├── PDF/                   # Generated PDFs
│   ├── PNG/                   # Generated PNGs (HighRes + Standard)
│   └── HTML/                  # Editable HTML
├── generator/
│   ├── dtdc_generator.py      # Core logic (OCR + PDF/PNG generation)
│   └── templates/
│       └── dtdc_template.html # Exact DTDC template
├── sample/
├── main.py                    # CLI version
├── app_gui.py                 # GUI version (PC - double click)
├── requirements.txt
└── README.md
```

### 🚀 Installation (PC)

1. **GitHub se clone ya zip download karo**
```bash
git clone https://github.com/your-username/DTDC_Bill_Generator.git
cd DTDC_Bill_Generator_Github
```

2. **Dependencies install**
```bash
pip install -r requirements.txt
```

3. **Tesseract OCR install (optional, for auto extraction)**
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Install and add to PATH

### 💻 Usage - 3 Tarike (SnipTool Supported!)

#### Tarika 1: GUI + SnipTool Direct Paste (Sabse Easy - Recommended)
```bash
python app_gui.py
```
- Window khulega
- **SnipTool se capture karo:** `Win + Shift + S` dabao, area select karo (image clipboard me copy ho jayega)
- **Paste SnipTool Image (Ctrl+V)** button dabao → Image direct paste ho jayega `input_images/` me!
- **Sender Name, Address, Contact, Courier Charges ₹** dalo
- **Generate Invoice PDF + PNG** click karo
- Output: `invoices/PDF/` aur `invoices/PNG/` me

#### Tarika 2: GUI Browse
- **Browse Image** click karo ya direct `input_images/` me image paste karo (jaise yaha karte ho)
- Details dalo, Generate karo

#### Tarika 3: CLI

#### Tarika 2: CLI
```bash
# Step 1: Image paste karo
# Copy your DTDC slip image to input_images/ folder
# Example: input_images/image.png

# Step 2: Run
python main.py
# Fir prompts me naam, address, contact, rate dalo
```

### 📝 Example Flow (Jaise aap yaha karte ho)

1. **Image Paste:** `input_images/image.png` (DTDC shipping label)
2. **Inputs:**
   - Consignor Name: `Sandeep kumar pandey`
   - Address: `177/02, Hardua mohalla near gayatri mandir, Nagod 485446`
   - Contact: `9179797484`
   - Courier Charges: `220`
3. **Output:**
   - `invoices/PDF/DTDC_Sandeep_220_TRICHUR.pdf`
   - `invoices/PNG/DTDC_Sandeep_220_TRICHUR_HighRes.png`

### 🔒 Remembered Settings (Locked as per your choice)
- Logo = Custom `assets/DTDC_logo.png`
- Layout = Original DTDC exact (no redesign)
- Courier Charges Box = Simple `Courier Charges: ₹ {amount}` only (no Freight/Fuel/GST breakup)
- Output = Always PDF + PNG HighRes + HTML
- OCR = Extracts Origin, Dest, Product, Type, Date, AWB, Mode, Consignee, Weight etc.
- Manual Override Priority = Your input > OCR

### 📤 GitHub Push
```bash
git init
git add .
git commit -m "DTDC Bill Generator - PC Version with custom logo"
git branch -M main
git remote add origin https://github.com/your-username/DTDC_Bill_Generator.git
git push -u origin main
```

### ❓ Need Help?
- Agar `weasyprint` install me error aaye Windows pe: `pip install weasyprint` ke liye Visual C++ chahiye ho sakta hai
- PNG generation ke liye `pymupdf` use ho raha hai

**Made for: Rahul Shrivastava / Shailendra / Sandeep workflow - Same format locked!**
