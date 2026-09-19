"""
DTDC Bill Generator - Core Logic - FINAL V5 FIXED
- Fixed: barcode module, libgobject, generator module, blank bill, overlap
- Supports: Single Landscape + 3 Copies Portrait (Paper Save Mode)
- Premium UI ready
"""

import base64
import os
import re
import io
import tempfile
from pathlib import Path
from datetime import datetime

# Barcode with fallback
try:
    from barcode import Code128
    from barcode.writer import ImageWriter
    BARCODE_AVAILABLE = True
except ImportError:
    Code128 = None
    ImageWriter = None
    BARCODE_AVAILABLE = False

# WeasyPrint with fallback
try:
    from weasyprint import HTML
    WEASY_AVAILABLE = True
except Exception:
    HTML = None
    WEASY_AVAILABLE = False

# ReportLab
try:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase.pdfmetrics import stringWidth
    REPORTLAB_AVAILABLE = True
except:
    REPORTLAB_AVAILABLE = False
    stringWidth = lambda t, f, s: len(t)*s*0.6

try:
    import fitz
except:
    fitz = None

try:
    from PIL import Image, ImageDraw
    try:
        import pytesseract
    except:
        pytesseract = None
    OCR_AVAILABLE = True
except:
    Image = None
    ImageDraw = None
    OCR_AVAILABLE = False
    pytesseract = None


def extract_text_from_image(image_path):
    text = ""
    if OCR_AVAILABLE and Image and pytesseract:
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
        except:
            pass
    return text


def parse_dtdc_fields(raw_text):
    data = {}
    t = raw_text or ""
    m = re.search(r'AWB\s*No\.?\s*[:\-]?\s*([A-Z0-9]{8,})', t, re.I)
    if m:
        data['awb'] = m.group(1).strip()
    m = re.search(r'\b(7[A-Z0-9]{10,})\b', t)
    if m:
        data['awb'] = m.group(1)
    m = re.search(r'Origin\s*:\s*([A-Z]+)', t, re.I)
    if m:
        data['origin'] = m.group(1).upper()
    m = re.search(r'Dest\s*:\s*([A-Z]+)', t, re.I)
    if m:
        data['dest'] = m.group(1).upper()
    m = re.search(r'PRODUCT\s*:\s*([A-Z0-9\s]+)', t, re.I)
    if m:
        data['product'] = m.group(1).strip()
    m = re.search(r'Type\s*:\s*([A-Z\-]+)', t, re.I)
    if m:
        data['type'] = m.group(1).upper()
    m = re.search(r'Mode\s*:\s*([A-Z]+)', t, re.I)
    if m:
        data['mode'] = m.group(1).upper()
    m = re.search(r'Date\s*:\s*([A-Za-z]{3}\s+[A-Za-z]{3}\s+\d{1,2}\s+\d{4})', t)
    if m:
        data['date'] = m.group(1)
    m = re.search(r'Consignee.*?Name\s*:\s*([A-Za-z0-9\s\.\-]+)', t, re.I)
    if m:
        data['consignee_name'] = m.group(1).strip()[:60]
    m = re.search(r'Consignee.*?Address\s*:\s*([^\n]+(?:\n[^\n]+){0,2})', t, re.I | re.S)
    if m:
        data['consignee_address'] = m.group(1).replace('\n',' ').strip()[:200]
    m = re.search(r'Content Specification\s*:\s*([A-Z0-9]+)', t, re.I)
    if m:
        data['content_spec'] = m.group(1).strip()
    m = re.search(r'Declared Value\s*:\s*([0-9]+|Not Applicable)', t, re.I)
    if m:
        data['declared_value'] = m.group(1)
    m = re.search(r'No Of Pieces\s*:\s*([0-9]+|Not Applicable)', t, re.I)
    if m:
        data['pieces'] = m.group(1)
    m = re.search(r'Actual Weight\s*:\s*([0-9\.]+\s*Gms|Kgs)', t, re.I)
    if m:
        data['actual_weight'] = m.group(1)
    m = re.search(r'Charged weight\s*:\s*([0-9\.]+\s*Gms|Kgs)', t, re.I)
    if m:
        data['charged_weight'] = m.group(1)
    m = re.search(r'Dim\s*:\s*([0-9xX\s\.cmCM]+|Not Applicable)', t, re.I)
    if m:
        data['dim'] = m.group(1)
    return data


def generate_barcode_base64(awb):
    try:
        if BARCODE_AVAILABLE and Code128 and ImageWriter:
            writer = ImageWriter()
            code = Code128(awb, writer=writer)
            tmp = str(Path(tempfile.gettempdir()) / "dtdc_barcode")
            out = code.save(tmp, options={"module_height":15,"module_width":0.4,"quiet_zone":2,"write_text":False})
            b64 = base64.b64encode(Path(out).read_bytes()).decode()
            os.remove(out)
            return b64
        else:
            raise ImportError("Barcode not available")
    except:
        try:
            if Image and ImageDraw:
                width, height = 400, 80
                img = Image.new('RGB', (width, height), 'white')
                draw = ImageDraw.Draw(img)
                x = 10
                for char in awb:
                    w = 3 if ord(char) % 2 == 0 else 6
                    if x % 20 < 10:
                        draw.rectangle([x, 10, x+w, height-10], fill='black')
                    x += w + 2
                    if x > width-10:
                        break
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                b64 = base64.b64encode(buffer.getvalue()).decode()
                return b64
            else:
                return ""
        except:
            return ""


def get_logo_base64(logo_path):
    try:
        import sys
        if hasattr(sys, '_MEIPASS'):
            bundle_logo = Path(sys._MEIPASS) / "assets" / "DTDC_logo.png"
            if bundle_logo.exists():
                return base64.b64encode(bundle_logo.read_bytes()).decode()
            bundle_logo2 = Path(sys._MEIPASS) / "DTDC_logo.png"
            if bundle_logo2.exists():
                return base64.b64encode(bundle_logo2.read_bytes()).decode()
        if logo_path and Path(logo_path).exists():
            return base64.b64encode(Path(logo_path).read_bytes()).decode()
        for p in ["assets/DTDC_logo.png", "DTDC_System/Assets/DTDC_logo.png", "../assets/DTDC_logo.png"]:
            if Path(p).exists():
                return base64.b64encode(Path(p).read_bytes()).decode()
        return ""
    except:
        return ""


def generate_pdf_with_reportlab(data, logo_path, pdf_path, barcode_b64, logo_b64):
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import mm
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfbase.pdfmetrics import stringWidth

        c = canvas.Canvas(str(pdf_path), pagesize=landscape(A4))
        width, height = landscape(A4)
        left = 10*mm
        bottom = 10*mm
        right = width - 10*mm
        top = height - 10*mm
        w = width - 20*mm
        h = height - 20*mm

        def draw_text_wrapped(c, text, x, y, max_width, font_name="Helvetica", font_size=8, line_height=10, bold=False):
            if bold:
                font_name = "Helvetica-Bold"
            c.setFont(font_name, font_size)
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if stringWidth(test_line, font_name, font_size) < max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            for i, line in enumerate(lines):
                c.drawString(x, y - i*line_height, line)
            return len(lines)

        c.setLineWidth(1.5)
        c.rect(left, bottom, w, h)

        col1_w = w * 0.41
        col2_w = w * 0.315
        col3_w = w * 0.275
        col1_x = left
        col2_x = left + col1_w
        col3_x = left + col1_w + col2_w

        top_h1 = 18*mm
        top_h2 = 14*mm
        top_h3 = 13*mm
        top_total = top_h1 + top_h2 + top_h3

        c.line(col2_x, top - top_total, col2_x, top)
        c.line(col3_x, top - top_total, col3_x, top)
        c.line(left, top - top_h1, right, top - top_h1)
        c.line(col2_x, top - top_h1 - top_h2, right, top - top_h1 - top_h2)

        try:
            if logo_b64:
                logo_data = base64.b64decode(logo_b64)
                logo_img = ImageReader(io.BytesIO(logo_data))
                c.drawImage(logo_img, col1_x + 3*mm, top - 14*mm, width=45*mm, height=10*mm, preserveAspectRatio=True, mask='auto')
            elif logo_path and Path(logo_path).exists():
                c.drawImage(str(logo_path), col1_x + 3*mm, top - 14*mm, width=45*mm, height=10*mm, preserveAspectRatio=True, mask='auto')
            else:
                c.setFont("Helvetica-Bold", 16)
                c.drawString(col1_x + 5*mm, top - 12*mm, "DTDC")
        except:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(col1_x + 5*mm, top - 12*mm, "DTDC")

        c.setFont("Helvetica", 7)
        c.drawString(col1_x + 55*mm, top - 6*mm, "DTDC Express Limited")
        c.drawString(col1_x + 55*mm, top - 10*mm, "Regd. Office No. 3, Victoria Road")
        c.drawString(col1_x + 55*mm, top - 14*mm, "Bengaluru - 560047")

        c.setFont("Helvetica", 8)
        c.drawCentredString(col2_x + col2_w/2, top - 7*mm, f"Origin: {data.get('origin','SATNA')}")
        c.drawCentredString(col3_x + col3_w/2, top - 7*mm, f"Dest: {data.get('dest','TRICHUR')}")
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(col2_x + col2_w/2, top - top_h1 - 7*mm, f"PRODUCT: {data.get('product','B2C PRIORITY')}")
        c.setFont("Helvetica", 8)
        c.drawCentredString(col3_x + col3_w/2, top - top_h1 - 7*mm, f"Type: {data.get('type','DOCUMENT')}")
        c.drawCentredString(col3_x + col3_w/2, top - top_h1 - top_h2 - 7*mm, f"Date: {data.get('date','Sat Sep 05 2026')}")

        mid_y_top = top - top_total
        mid_h = 42*mm
        mid_y_bottom = mid_y_top - mid_h
        c.line(left, mid_y_bottom, right, mid_y_bottom)
        c.line(col1_x + col1_w, mid_y_top, col1_x + col1_w, mid_y_bottom)

        c.setFont("Helvetica", 7.5)
        c.drawString(col1_x + 2*mm, mid_y_top - 4*mm, f"Consignor's Name: {data.get('consignor_name') or 'Sandeep kumar pandey'}")
        consignor_addr_full = data.get('consignor_address') or '177/02, Hardua mohalla near gayatri mandir, Nagod 485446'
        c.drawString(col1_x + 2*mm, mid_y_top - 9*mm, f"Consignor's Address: {consignor_addr_full[:85]}")
        c.drawString(col1_x + 2*mm, mid_y_top - 14*mm, f"{consignor_addr_full[85:170]}")
        c.drawString(col1_x + 2*mm, mid_y_top - 19*mm, f"GSTIN No.:")
        c.drawString(col1_x + 2*mm, mid_y_top - 24*mm, f"Phone: {data.get('consignor_phone') or '9179797484'}  Email :")

        c.drawString(col2_x + 2*mm, mid_y_top - 4*mm, f"Customer Ref No:")
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(col2_x + 2*mm, mid_y_top - 9*mm, f"Consignee's Name: {data.get('consignee_name') or 'MR. ANTO T K'}")
        c.setFont("Helvetica", 7.5)
        consignee_addr_full = data.get('consignee_address') or 'COCO PETROL PUMP BP, CHEMBOOTHRA PANANCHERY KERALA, TRICHUR, KERALA, 680652'
        c.drawString(col2_x + 2*mm, mid_y_top - 14*mm, f"Consignee's Address: {consignee_addr_full[:90]}")
        c.drawString(col2_x + 2*mm, mid_y_top - 19*mm, f"{consignee_addr_full[90:180]}")
        c.drawString(col2_x + 2*mm, mid_y_top - 24*mm, f"GSTIN No.:")
        c.drawString(col2_x + 2*mm, mid_y_top - 29*mm, f"Phone: {data.get('consignee_phone') or '0000000000'}  Email :")

        c.setLineWidth(1)
        charges_text = f"Courier Charges: Rs. {data.get('courier_charges','220')}"
        charges_w = stringWidth(charges_text, "Helvetica-Bold", 8) + 8*mm
        c.rect(col2_x + 2*mm, mid_y_bottom + 6*mm, charges_w, 7*mm)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(col2_x + 4*mm, mid_y_bottom + 8*mm, charges_text)

        bot_left_w = w * 0.32
        bot_mid_w = w * 0.26
        bot_right_w = w * 0.42
        bot_left_x = left
        bot_mid_x = left + bot_left_w
        bot_right_x = left + bot_left_w + bot_mid_w
        bot_top = mid_y_bottom
        bot_bottom = bottom + 8*mm

        c.line(bot_mid_x, bot_bottom, bot_mid_x, bot_top)
        c.line(bot_right_x, bot_bottom, bot_right_x, bot_top)

        left_row1 = 12*mm
        left_row2 = 15*mm
        left_row3 = 38*mm
        left_row4 = 12*mm

        y = bot_top
        c.line(bot_left_x, y - left_row1, bot_mid_x, y - left_row1)
        c.setFont("Helvetica", 7)
        c.drawString(bot_left_x + 2*mm, y - 4*mm, f"Content Specification : {data.get('content_spec','')}")
        y -= left_row1
        c.line(bot_left_x, y - left_row2, bot_mid_x, y - left_row2)
        c.drawString(bot_left_x + 2*mm, y - 4*mm, f"Paperwork Enclosed :")
        y -= left_row2
        c.line(bot_left_x, y - left_row3, bot_mid_x, y - left_row3)
        c.setFont("Helvetica", 6)
        decl_text = "I/We declare that this consignment does not contain personal mail, cash, jewellery, contraband, illegal drugs, any prohibited items and commodities which can cause safety hazards while transporting"
        draw_text_wrapped(c, decl_text, bot_left_x + 2*mm, y - 4*mm, bot_left_w - 4*mm, font_size=6, line_height=7)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(bot_left_x + bot_left_w/2, y - 28*mm, "Sender's Signature & Seal")
        c.setFont("Helvetica", 5)
        c.drawCentredString(bot_left_x + bot_left_w/2, y - 32*mm, "I have read and understood terms & conditions of carriage mentioned on website www.dtdc.in, and I agree to the same.")
        y -= left_row3
        c.line(bot_left_x, y - left_row4, bot_mid_x, y - left_row4)
        y -= left_row4
        c.setFont("Helvetica", 5.5)
        c.drawCentredString(bot_left_x + bot_left_w/2, y - 4*mm, "https://www.dtdc.in | customersupport@dtdc.com | +91-9606911811")

        mid_rows = [8*mm, 7*mm, 6*mm, 8*mm, 6*mm, 6*mm, 44*mm]
        y = bot_top
        c.setFont("Helvetica", 7)
        labels = [
            f"Declared Value: {data.get('declared_value','Not Applicable')}",
            f"No Of Pieces: {data.get('pieces','Not Applicable')}",
            f"Actual Weight: {data.get('actual_weight','100 Gms')}",
            f"Ewaybill Number:",
            f"Dim: {data.get('dim','Not Applicable')}",
            f"Charged weight: {data.get('charged_weight','500 Gms')}",
            ""
        ]
        for i, row_h in enumerate(mid_rows):
            if i < len(mid_rows)-1:
                c.line(bot_mid_x, y - row_h, bot_right_x, y - row_h)
            if i < 6:
                c.drawString(bot_mid_x + 2*mm, y - 4*mm, labels[i])
            y -= row_h

        c.setFont("Helvetica", 6.5)
        c.drawString(bot_mid_x + 2*mm, bot_bottom + 32*mm, f"Name : {data.get('sender_name','SATNA SEMARIYA CHOWK')}")
        c.drawString(bot_mid_x + 2*mm, bot_bottom + 27*mm, f"Address: {data.get('sender_addr','NEAR DASHMESH HOTEL SEMARIYA CHOWK REWA ROAD, SATN, SATNA, MADHYA PRADESH, 485001')[:45]}")
        c.drawString(bot_mid_x + 2*mm, bot_bottom + 22*mm, f"{data.get('sender_addr','')[45:90]}")
        c.drawString(bot_mid_x + 2*mm, bot_bottom + 17*mm, f"CHOWK REWA ROAD, SATN, SATNA, MADHYA PRADESH, 485001")
        c.drawString(bot_mid_x + 2*mm, bot_bottom + 12*mm, f"Phone : {data.get('sender_phone','9303592136')}")

        right_top = bot_top
        right_mid1 = 45*mm
        right_mid2 = 28*mm

        c.line(bot_right_x, right_top - right_mid1, right, right_top - right_mid1)
        c.line(bot_right_x, right_top - right_mid1 - right_mid2, right, right_top - right_mid1 - right_mid2)

        c.setFont("Helvetica", 11)
        c.drawCentredString(bot_right_x + bot_right_w/2, right_top - 6*mm, f"Mode: {data.get('mode','AIR')}")

        try:
            if barcode_b64:
                barcode_data = base64.b64decode(barcode_b64)
                barcode_img = ImageReader(io.BytesIO(barcode_data))
                c.drawImage(barcode_img, bot_right_x + 10*mm, right_top - 25*mm, width=bot_right_w - 20*mm, height=15*mm, preserveAspectRatio=True, mask='auto')
        except:
            x = bot_right_x + 15*mm
            for i in range(30):
                w_bar = 1*mm if i%2==0 else 0.5*mm
                c.rect(x, right_top - 25*mm, w_bar, 12*mm, fill=1)
                x += w_bar + 0.5*mm

        c.setFont("Helvetica", 8)
        c.drawCentredString(bot_right_x + bot_right_w/2, right_top - 32*mm, f"AWB No: {data.get('awb','7X117632485')}")

        risk_y_top = right_top - right_mid1
        risk_mid_h = right_mid2 / 2
        risk_col1_w = bot_right_w * 0.58
        risk_col2_w = bot_right_w * 0.18
        risk_col3_w = bot_right_w * 0.24
        risk_col2_x = bot_right_x + risk_col1_w
        risk_col3_x = bot_right_x + risk_col1_w + risk_col2_w

        c.line(risk_col2_x, risk_y_top - right_mid2, risk_col2_x, risk_y_top)
        c.line(risk_col3_x, risk_y_top - right_mid2, risk_col3_x, risk_y_top)
        c.line(risk_col2_x, risk_y_top - risk_mid_h, right, risk_y_top - risk_mid_h)

        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(bot_right_x + risk_col1_w/2, risk_y_top - 12*mm, "Risk Surcharge")
        c.setFont("Helvetica", 8)
        c.drawCentredString(risk_col2_x + risk_col2_w/2, risk_y_top - 7*mm, "Owner")
        c.drawCentredString(risk_col2_x + risk_col2_w/2, risk_y_top - risk_mid_h - 7*mm, "Carrier")
        c.rect(risk_col3_x + 8*mm, risk_y_top - 10*mm, 6*mm, 5*mm)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(risk_col3_x + 9.5*mm, risk_y_top - 8.5*mm, "✓")
        c.rect(risk_col3_x + 8*mm, risk_y_top - risk_mid_h - 10*mm, 6*mm, 5*mm)

        c.setFont("Helvetica", 7)
        c.drawString(bot_right_x + 2*mm, bot_bottom + 4*mm, "Remark :")

        c.setFont("Helvetica-Bold", 6)
        c.drawString(left + 2*mm, bottom + 2*mm, "THIS DOCUMENT IS NOT A TAX INVOICE. WEIGHT CAPTURED BY DTDC WILL BE USED FOR INVOICE GENERATION.")
        c.drawRightString(right - 2*mm, bottom + 2*mm, "Sender's Copy")

        c.showPage()
        c.save()
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False


def build_html(data, barcode_b64, logo_b64):
    origin = data.get('origin','SATNA')
    dest = data.get('dest','TRICHUR')
    product = data.get('product','B2C PRIORITY')
    typ = data.get('type','DOCUMENT')
    date = data.get('date', datetime.now().strftime("%a %b %d %Y"))
    mode = data.get('mode','AIR')
    awb = data.get('awb','7X117632485')
    consignor_name = data.get('consignor_name','Rahul Shrivastava')
    consignor_address = data.get('consignor_address','Near satna simariya chowk, NEAR AXIS BANK ATM, SATNA, MADHYA PRADESH, 485001')
    consignor_phone = data.get('consignor_phone','0000000000')
    consignee_name = data.get('consignee_name','MR. ANTO T K')
    consignee_address = data.get('consignee_address','COCO PETROL PUMP BP, CHEMBOOTHRA PANANCHERY KERALA, TRICHUR, KERALA, 680652')
    consignee_phone = data.get('consignee_phone','0000000000')
    content_spec = data.get('content_spec','')
    declared_value = data.get('declared_value','Not Applicable')
    pieces = data.get('pieces','Not Applicable')
    actual_weight = data.get('actual_weight','100 Gms')
    charged_weight = data.get('charged_weight','500 Gms')
    dim = data.get('dim','Not Applicable')
    courier_charges = data.get('courier_charges','220')
    sender_name = data.get('sender_name','SATNA SEMARIYA CHOWK')
    sender_addr = data.get('sender_addr','NEAR DASHMESH HOTEL SEMARIYA CHOWK REWA ROAD, SATN, SATNA, MADHYA PRADESH, 485001')
    sender_phone = data.get('sender_phone','9303592136')

    logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div class="logo">DTDC<div class="dot"></div></div>'

    template_path = Path(__file__).parent / "templates" / "dtdc_template.html"
    if template_path.exists():
        template = template_path.read_text(encoding='utf-8')
        return template.format(
            logo_html=logo_html,
            origin=origin,
            dest=dest,
            product=product,
            type=typ,
            date=date,
            consignor_name=consignor_name,
            consignor_address=consignor_address,
            consignor_phone=consignor_phone,
            consignee_name=consignee_name,
            consignee_address=consignee_address,
            consignee_phone=consignee_phone or '0000000000',
            content_spec=content_spec,
            declared_value=declared_value,
            pieces=pieces,
            actual_weight=actual_weight,
            charged_weight=charged_weight,
            dim=dim,
            mode=mode,
            awb=awb,
            courier_charges=courier_charges,
            sender_name=sender_name,
            sender_addr=sender_addr,
            sender_phone=sender_phone,
            barcode_b64=barcode_b64
        )
    else:
        return f"<html><body>{consignor_name} - {awb} - Rs. {courier_charges}</body></html>"


def generate_3_copies_portrait(data, logo_path, output_dir):
    """Generate 1 portrait page with 3 copies: Receiver, Sender, POD"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    awb = data.get('awb','7X117632485')
    barcode_b64 = generate_barcode_base64(awb)
    logo_b64 = get_logo_base64(logo_path)
    
    # Paper Save Mode check
    paper_save = data.get("paper_save_mode", False)
    
    try:
        from weasyprint import HTML
        html_template = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
  @page {{ size: A4 portrait; margin: 5mm; }}
  *{{box-sizing:border-box;margin:0;padding:0}} body{{font-family:Arial,Helvetica,sans-serif;background:#fff}}
  .page{{width:190mm; margin:0 auto}}
  .copy{{border:2px solid #000; margin-bottom:4mm; height:88mm; position:relative; page-break-inside:avoid}}
  .top{{display:grid;grid-template-columns:41% 31% 28%;grid-template-rows:16mm 10mm 8mm; height:34mm}}
  .logo-cell{{grid-row:1/4;grid-column:1/2;border-right:1.5px solid #000;border-bottom:1.5px solid #000;padding:2mm;display:flex;gap:2mm;align-items:center}}
  .logo-img{{width:28mm;height:auto}} .company{{font-size:2.2mm;line-height:2.8mm}}
  .c{{border-right:1.5px solid #000;border-bottom:1.5px solid #000;display:flex;align-items:center;justify-content:center;font-size:2.5mm}} .c-right{{border-bottom:1.5px solid #000;display:flex;align-items:center;justify-content:center;font-size:2.5mm}}
  .c-product{{grid-row:2/4;grid-column:2/3;border-right:1.5px solid #000;border-bottom:1.5px solid #000;display:flex;align-items:center;justify-content:center;font-size:2.8mm;font-weight:700}}
  .mid{{display:grid;grid-template-columns:41% 59%; height:22mm}} .mid-left,.mid-right{{border-bottom:1.5px solid #000;padding:1mm;font-size:2.2mm;line-height:2.8mm}} .mid-left{{border-right:1.5px solid #000}}
  .bottom{{display:grid;grid-template-columns:32% 26% 42%; height:32mm}} .b-left{{border-right:1.5px solid #000;display:grid;grid-template-rows:6mm 7mm 14mm 5mm}} .b-mid{{border-right:1.5px solid #000;display:grid;grid-template-rows:5mm 4mm 4mm 5mm 4mm 4mm 6mm}} .b-right{{display:grid;grid-template-rows:18mm 10mm}}
  .bl,.bm{{border-bottom:1px solid #000;padding:0.8mm;font-size:2mm;line-height:2.4mm}} .br-top{{border-bottom:1px solid #000;text-align:center;padding:1mm}} .br-mid{{border-bottom:1px solid #000;display:grid;grid-template-columns:58% 18% 24%;grid-template-rows:5mm 5mm}} .risk{{grid-row:1/3;grid-column:1/2;border-right:1px solid #000;display:flex;align-items:center;justify-content:center;font-size:3.5mm;font-weight:900}} .own-l{{grid-row:1/2;grid-column:2/3;border-right:1px solid #000;border-bottom:1px solid #000;display:flex;align-items:center;justify-content:center;font-size:2mm}} .own-c{{grid-row:1/2;grid-column:3/4;border-bottom:1px solid #000;display:flex;align-items:center;justify-content:center}} .car-l{{grid-row:2/3;grid-column:2/3;border-right:1px solid #000;display:flex;align-items:center;justify-content:center;font-size:2mm}} .car-c{{grid-row:2/3;grid-column:3/4;display:flex;align-items:center;justify-content:center}} .chk{{width:3.5mm;height:3mm;border:1px solid #000;border-radius:0.5mm;display:flex;align-items:center;justify-content:center;font-size:2.5mm}} .barcode{{width:85%;height:7mm;object-fit:contain;margin:0.5mm auto;display:block}} .awb{{font-size:2.2mm}} .mode{{font-size:3mm}} .footer{{position:absolute;bottom:0;left:0;right:0;border-top:1px solid #000;display:flex;justify-content:space-between;padding:0.5mm 1mm;font-size:1.8mm;font-weight:700}} .charges-box{{border:1px solid #000;display:inline-block;padding:0.5mm 1.5mm;font-size:2.2mm;font-weight:bold;background:#fff;margin-top:1mm}}
  .blank{{background:#f9f9f9; display:flex; align-items:center; justify-content:center; color:#999; font-size:4mm}}
</style></head><body><div class="page">
"""
        if paper_save:
            copy_list = [("Sender's Copy", data), ("Blank - Paper Save", {}), ("Blank - Paper Save", {})]
        else:
            copy_list = [("Receiver's Copy", data), ("Sender's Copy", data), ("POD Copy", data)]
        
        for copy_name, curr_data in copy_list:
            if not curr_data:
                html_template += f'<div class="copy blank"><div>Blank Copy - Paper Save Mode - {copy_name}</div><div class="footer"><span></span><span>{copy_name}</span></div></div>'
                continue
                
            html_template += f"""
  <div class="copy">
    <div class="top">
      <div class="logo-cell"><img src="data:image/png;base64,{logo_b64}" class="logo-img"><div class="company">DTDC Express Limited<br>Regd. Office No. 3, Victoria Road<br>Bengaluru - 560047</div></div>
      <div class="c">Origin: <b>{curr_data.get('origin','SATNA')}</b></div><div class="c-right">Dest: <b>{curr_data.get('dest','')}</b></div>
      <div class="c-product">PRODUCT: {curr_data.get('product','B2C PRIORITY')}</div><div class="c-right">Type: <b>{curr_data.get('type','DOCUMENT')}</b></div><div class="c-right">Date: {curr_data.get('date','')}</div>
    </div>
    <div class="mid">
      <div class="mid-left">Consignor's Name: <b>{curr_data.get('consignor_name','')}</b><br>Address: {curr_data.get('consignor_address','')}<br>Phone: <b>{curr_data.get('consignor_phone','')}</b></div>
      <div class="mid-right">Consignee's Name: <b>{curr_data.get('consignee_name','')}</b><br>Address: {curr_data.get('consignee_address','')}<br>Phone: {curr_data.get('consignee_phone') or '0000000000'} <span class="charges-box">Courier Charges: Rs. {curr_data.get('courier_charges','')}</span></div>
    </div>
    <div class="bottom">
      <div class="b-left">
        <div class="bl">Content: {curr_data.get('content_spec','')} | Declared: {curr_data.get('declared_value','')}</div>
        <div class="bl">Actual: {curr_data.get('actual_weight','')} | Charged: {curr_data.get('charged_weight','')} | Dim: {curr_data.get('dim','')}</div>
        <div class="bl" style="font-size:1.8mm">I/We declare that this consignment does not contain prohibited items<br><b>Sender's Signature & Seal</b></div>
        <div class="bl" style="font-size:1.6mm;text-align:center">https://www.dtdc.in | customersupport@dtdc.com</div>
      </div>
      <div class="b-mid">
        <div class="bm">No Of Pieces: {curr_data.get('pieces','')}</div>
        <div class="bm">Ewaybill:</div>
        <div class="bm">Name: {curr_data.get('sender_name','SATNA SEMARIYA CHOWK')}</div>
        <div class="bm" style="font-size:1.8mm">Addr: {curr_data.get('sender_addr','')[:50]}</div>
        <div class="bm">Phone: {curr_data.get('sender_phone','')}</div>
        <div class="bm">Remark:</div>
      </div>
      <div class="b-right">
        <div class="br-top"><div class="mode">Mode: <b>{curr_data.get('mode','')}</b></div><img class="barcode" src="data:image/png;base64,{barcode_b64}"><div class="awb">AWB No: <b>{curr_data.get('awb','')}</b></div></div>
        <div class="br-mid"><div class="risk">Risk Surcharge</div><div class="own-l">Owner</div><div class="own-c"><div class="chk">✓</div></div><div class="car-l">Carrier</div><div class="car-c"><div class="chk"></div></div></div>
      </div>
    </div>
    <div class="footer"><span>THIS DOCUMENT IS NOT A TAX INVOICE.</span><span>{copy_name}</span></div>
  </div>
"""
        html_template += "</div></body></html>"
        
        safe_name = data.get('consignor_name','Invoice').replace(' ','_')
        base_name = f"DTDC_{safe_name}_{data.get('courier_charges','0')}_{data.get('dest','')}_3Copies"
        pdf_path = output_dir / f"{base_name}.pdf"
        HTML(string=html_template).write_pdf(str(pdf_path))
        
        try:
            import fitz
            doc = fitz.open(str(pdf_path))
            pix = doc[0].get_pixmap(matrix=fitz.Matrix(3,3))
            png_path = output_dir / f"{base_name}_HighRes.png"
            pix.save(str(png_path))
            return {"pdf": str(pdf_path), "png": str(png_path), "copies": 3}
        except:
            return {"pdf": str(pdf_path), "png": None, "copies": 3}
    except Exception as e:
        print(f"3 copies generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_invoice(data, logo_path, output_dir):
    output_dir = Path(output_dir)
    (output_dir / "PDF").mkdir(parents=True, exist_ok=True)
    (output_dir / "PNG").mkdir(parents=True, exist_ok=True)
    (output_dir / "HTML").mkdir(parents=True, exist_ok=True)

    awb = data.get('awb','7X117632485')
    barcode_b64 = generate_barcode_base64(awb)
    logo_b64 = get_logo_base64(logo_path)

    html_content = build_html(data, barcode_b64, logo_b64)

    safe_name = data.get('consignor_name','Invoice').replace(' ','_')
    safe_dest = data.get('dest','').replace(' ','_')
    base_name = f"DTDC_{safe_name}_{data.get('courier_charges','0')}_{safe_dest}"

    html_path = output_dir / "HTML" / f"{base_name}.html"
    html_path.write_text(html_content, encoding='utf-8')

    pdf_path = output_dir / "PDF" / f"{base_name}.pdf"
    
    pdf_generated = False
    if WEASY_AVAILABLE and HTML:
        try:
            HTML(string=html_content).write_pdf(str(pdf_path))
            pdf_generated = True
        except Exception as e:
            print(f"WeasyPrint failed ({e}), trying ReportLab")
            pdf_generated = False
    
    if not pdf_generated:
        if REPORTLAB_AVAILABLE:
            pdf_generated = generate_pdf_with_reportlab(data, logo_path, pdf_path, barcode_b64, logo_b64)

    png_path = None
    png_high = None
    if pdf_generated and fitz and Path(pdf_path).exists():
        try:
            doc = fitz.open(str(pdf_path))
            page = doc[0]
            pix_high = page.get_pixmap(matrix=fitz.Matrix(3,3))
            png_high = output_dir / "PNG" / f"{base_name}_HighRes.png"
            pix_high.save(str(png_high))
            pix = page.get_pixmap(matrix=fitz.Matrix(2,2))
            png_path = output_dir / "PNG" / f"{base_name}.png"
            pix.save(str(png_path))
        except Exception as e:
            print(f"PNG from PDF failed: {e}")

    return {
        "html": str(html_path),
        "pdf": str(pdf_path) if pdf_generated else None,
        "png": str(png_path) if png_path else None,
        "png_high": str(png_high) if png_high else None
    }
