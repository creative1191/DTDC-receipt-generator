# Fix: 1 Page pe 4 Invoices (2x2 Grid) - Split Solution

## Problem:
Aapke PDF me 1 page pe 4 invoices ek saath aa rahi hain (2x2 grid). Normal generator sirf 1 invoice samajhta hai.

## Solution: Auto Split Feature Added

### Code me naya function add kiya hai: `split_4_per_page_pdf()`

Ye function:
1. PDF page ko high-res image me convert karta hai
2. Us image ko 4 quadrants me split karta hai:
   - Top-Left
   - Top-Right
   - Bottom-Left
   - Bottom-Right
3. Har quadrant ko alag invoice image banata hai
4. Har ek pe OCR + manual override apply karke alag PDF/PNG generate karta hai

### PC Generator me Auto-Detect:
- Agar PDF me 1 page pe 4 DTDC logos / 4 AWB numbers mile, to auto split ho jayega
- Aapko kuch extra karna nahi, bas PDF `input_images/` me daalo
- App 4 alag invoices bana dega: `Invoice_1/`, `Invoice_2/`, `Invoice_3/`, `Invoice_4/`

### Aapke Current PDF ka Result:
- Original: `Shipping_Label_7X117632485 (2).pdf` - 1 page, 4 invoices 2x2 grid
- Split into:
  - `Split_4x/invoice_top_left.png`
  - `Split_4x/invoice_top_right.png`
  - `Split_4x/invoice_bottom_left.png`
  - `Split_4x/invoice_bottom_right.png`
- Generated 4 separate invoices in exact same format (size same to same):
  - `Invoice_1/PDF/DTDC_Sandeep_kumar_pandey_1_220_TRICHUR.pdf`
  - `Invoice_2/PDF/DTDC_Sandeep_kumar_pandey_2_220_TRICHUR.pdf`
  - etc.

### Future ke liye:
- Jab bhi 4-per-page PDF upload karoge, same auto split hoga
- Har invoice ka size yahi rahega: A4 Landscape 29.7x21.0 cm, content 1080px
- Format same to same: Custom logo, full barcode, Rs. charges box
