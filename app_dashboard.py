#!/usr/bin/env python3
"""
DTDC Bill Generator - Full Window Dashboard UI - Like Your Reference Image
Premium Windows 11 + Dashboard Style (Sidebar + Stats + Generator)
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from datetime import datetime

try:
    import customtkinter as ctk
    from tkinter import filedialog, messagebox
    from PIL import Image
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    USE_CUSTOM = True
except ImportError:
    print("Please install: pip install customtkinter Pillow")
    sys.exit(1)

from generator.dtdc_generator import extract_text_from_image, parse_dtdc_fields, generate_invoice, generate_3_copies_portrait

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DTDC_Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DTDC Generator - Premium Dashboard")
        self.geometry("1250x750")
        self.configure(fg_color="#f0f0f0")
        
        # Icon
        try:
            logo_path = get_resource_path("assets/DTDC_logo.png")
            if Path(logo_path).exists():
                from PIL import ImageTk
                icon_img = Image.open(logo_path)
                icon_img = icon_img.resize((32, 32), Image.Resampling.LANCZOS)
                self.icon = ImageTk.PhotoImage(icon_img)
                self.iconphoto(True, self.icon)
        except:
            pass

        self.input_image_path = None
        self.last_pdf = None

        # Main layout: Sidebar + Main
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ===== SIDEBAR (Like your image - Purple) =====
        self.sidebar = ctk.CTkFrame(self, fg_color="#7a8bff", width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Sidebar content
        ctk.CTkLabel(self.sidebar, text="≡", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(anchor="w", padx=15, pady=15)
        
        # Menu items like your image
        self.menu_buttons = []
        menus = [
            ("🏠  Dashboard", True),
            ("👤  Generate Bill", False),
            ("📝  Invoices", False),
            ("📄  3 Copies Mode", False),
            ("⚙️  Settings", False),
            ("💬  Help", False),
        ]
        
        for text, active in menus:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                fg_color="#5a6bdf" if active else "transparent",
                hover_color="#5a6bdf",
                text_color="white",
                anchor="w",
                corner_radius=0,
                font=ctk.CTkFont(size=13, weight="bold" if active else "normal"),
                height=40
            )
            btn.pack(fill="x", pady=2)
            self.menu_buttons.append(btn)

        # Bottom Sign Out like your image
        ctk.CTkFrame(self.sidebar, height=2, fg_color="#9aa8ff").pack(fill="x", pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="SIGN OUT", fg_color="#5a6bdf", hover_color="#4a5bcf", corner_radius=6, font=ctk.CTkFont(weight="bold")).pack(side="bottom", pady=20, padx=15, fill="x")

        # ===== MAIN AREA =====
        self.main = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)

        # Top Header (Light purple like your image)
        header = ctk.CTkFrame(self.main, fg_color="#c5c9ff", height=50, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        # User profile like Emily Rose in your image
        profile_frame = ctk.CTkFrame(header, fg_color="#c5c9ff")
        profile_frame.pack(side="right", padx=20, pady=8)

        # User avatar placeholder
        ctk.CTkLabel(profile_frame, text="👤", font=ctk.CTkFont(size=20), fg_color="#c5c9ff").pack(side="left", padx=5)
        ctk.CTkLabel(profile_frame, text="Dharmendra", font=ctk.CTkFont(size=13, weight="bold"), text_color="#333").pack(side="left", padx=5)
        # Toggle like your image
        ctk.CTkLabel(profile_frame, text="●", text_color="#00c853", font=ctk.CTkFont(size=16)).pack(side="left", padx=5)

        # ===== DASHBOARD CONTENT - Like your reference =====
        content = ctk.CTkScrollableFrame(self.main, fg_color="#f0f0f0")
        content.pack(fill="both", expand=True, padx=15, pady=10)

        # Stats row - OPTION 1, OPTION 2, OPTION 3 like your image
        stats_frame = ctk.CTkFrame(content, fg_color="#f0f0f0")
        stats_frame.pack(fill="x", pady=8)

        # OPTION 1 - Total Invoices
        self.create_stat_card(stats_frame, "OPTION 1", "538", "Total Invoices", "#00bcd4", 0)
        # OPTION 2
        self.create_stat_card(stats_frame, "OPTION 2", "485", "Today's Bills", "#b39ddb", 1)
        # OPTION 3
        self.create_stat_card(stats_frame, "OPTION 3", "45", "Pending", "#00bcd4", 2)
        # OPTION 1/2 bars like your image
        self.create_bar_card(stats_frame, 3)

        # Second row - USER ACTIVITY + Time + Options
        row2 = ctk.CTkFrame(content, fg_color="#f0f0f0")
        row2.pack(fill="x", pady=8)

        # USER ACTIVITY Graph Card
        activity_card = ctk.CTkFrame(row2, fg_color="white", corner_radius=12, border_width=1, border_color="#e0e0e0")
        activity_card.pack(side="left", fill="both", expand=True, padx=5)

        ctk.CTkLabel(activity_card, text="USER ACTIVITY", font=ctk.CTkFont(size=12, weight="bold"), text_color="#333").pack(anchor="w", padx=12, pady=8)
        
        # Simple graph representation
        graph_frame = ctk.CTkFrame(activity_card, fg_color="white")
        graph_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Years and line graph mockup
        for year in ["2019", "2017", "2014", "2013"]:
            ctk.CTkLabel(graph_frame, text=year, font=ctk.CTkFont(size=9), text_color="#666").pack(anchor="w")
        
        ctk.CTkLabel(graph_frame, text="1 2 3 4 5 6 7 8 9 10 11 12", font=ctk.CTkFont(size=8), text_color="#666").pack(side="bottom")
        ctk.CTkLabel(graph_frame, text="📈 Graph: Invoices per month (Mockup)", font=ctk.CTkFont(size=10), text_color="#7a8bff").pack(pady=10)

        # Time + Weather Card (01:30 and 30° like your image)
        time_card = ctk.CTkFrame(row2, fg_color="white", corner_radius=12, width=150, border_width=1, border_color="#e0e0e0")
        time_card.pack(side="left", fill="y", padx=5)
        time_card.pack_propagate(False)

        ctk.CTkFrame(time_card, fg_color="#b8baff", height=60, corner_radius=8).pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(time_card, text="01:30", font=ctk.CTkFont(size=24), text_color="white").place(x=30, y=10)
        
        ctk.CTkLabel(time_card, text="☀️  30°", font=ctk.CTkFont(size=22, weight="bold"), text_color="#333").pack(pady=15)

        # Options List Card
        opt_card = ctk.CTkFrame(row2, fg_color="white", corner_radius=12, width=200, border_width=1, border_color="#e0e0e0")
        opt_card.pack(side="left", fill="y", padx=5)
        opt_card.pack_propagate(False)

        for i, opt in enumerate(["OPTION 1", "OPTION 2", "OPTION 3", "OPTION 4"]):
            f = ctk.CTkFrame(opt_card, fg_color="white")
            f.pack(fill="x", padx=8, pady=4)
            ctk.CTkLabel(f, text="◆", text_color="#00bcd4", font=ctk.CTkFont(size=12)).pack(side="left")
            ctk.CTkLabel(f, text=f"{opt}\nLorem Ipsum", font=ctk.CTkFont(size=10), text_color="#333", justify="left").pack(side="left", padx=5)

        # Third row - OPTION 1/2 circles + COMMENT
        row3 = ctk.CTkFrame(content, fg_color="#f0f0f0")
        row3.pack(fill="x", pady=8)

        # 45% circle
        self.create_circle_card(row3, "OPTION 1", "45%", 0)
        # 80% circle
        self.create_circle_card(row3, "OPTION 2", "80%", 1)

        # COMMENT Card (Emily Rose, Mateo Clea like your image)
        comment_card = ctk.CTkFrame(row3, fg_color="white", corner_radius=12, border_width=1, border_color="#e0e0e0")
        comment_card.pack(side="left", fill="both", expand=True, padx=5)

        ctk.CTkLabel(comment_card, text="COMMENT", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=12, pady=8)

        for name in ["Dharmendra", "Sandeep"]:
            f = ctk.CTkFrame(comment_card, fg_color="white")
            f.pack(fill="x", padx=10, pady=4)
            ctk.CTkLabel(f, text="👤", font=ctk.CTkFont(size=16)).pack(side="left")
            ctk.CTkLabel(f, text=f"{name}\nLorem ipsum dolor sit amet, consectetur\nadipiscing elit, sed diam nonummy.", font=ctk.CTkFont(size=9), text_color="#666", justify="left").pack(side="left", padx=8)

        # ===== BILL GENERATOR FORM (Integrated in Dashboard) =====
        form_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12, border_width=1, border_color="#e0e0e0")
        form_card.pack(fill="x", pady=15, padx=5)

        ctk.CTkLabel(form_card, text="✨  Generate DTDC Bill - Premium", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0a2256").pack(anchor="w", padx=15, pady=(12,8))

        # Image input row
        img_row = ctk.CTkFrame(form_card, fg_color="white")
        img_row.pack(fill="x", padx=12, pady=5)

        ctk.CTkButton(img_row, text="📁 Browse Image", command=self.browse_image, fg_color="#0a2256", corner_radius=8, width=140).pack(side="left", padx=4)
        ctk.CTkButton(img_row, text="📋 Paste SnipTool (Ctrl+V)", command=self.paste_from_clipboard, fg_color="#e30613", corner_radius=8, width=180).pack(side="left", padx=4)

        self.lbl_image = ctk.CTkLabel(form_card, text="No image - Win+Shift+S → Ctrl+V", text_color="#666", font=ctk.CTkFont(size=10))
        self.lbl_image.pack(anchor="w", padx=15, pady=2)

        self.lbl_awb = ctk.CTkLabel(form_card, text="", text_color="#0a8a00", font=ctk.CTkFont(size=11, weight="bold"))
        self.lbl_awb.pack(anchor="w", padx=15, pady=2)

        # Form fields in grid
        form_grid = ctk.CTkFrame(form_card, fg_color="white")
        form_grid.pack(fill="x", padx=12, pady=8)

        ctk.CTkLabel(form_grid, text="Consignor Name:").grid(row=0, column=0, sticky="w", pady=6, padx=5)
        self.entry_name = ctk.CTkEntry(form_grid, width=350, corner_radius=8)
        self.entry_name.grid(row=0, column=1, pady=6, padx=5, sticky="ew")
        self.entry_name.insert(0, "Dharmendra kumar kushwaha")

        ctk.CTkLabel(form_grid, text="Address:").grid(row=1, column=0, sticky="w", pady=6, padx=5)
        self.entry_address = ctk.CTkEntry(form_grid, width=350, corner_radius=8)
        self.entry_address.grid(row=1, column=1, pady=6, padx=5, sticky="ew")
        self.entry_address.insert(0, "Ghatehkala post rahikwara nagod, distt satna 485446")

        ctk.CTkLabel(form_grid, text="Contact:").grid(row=2, column=0, sticky="w", pady=6, padx=5)
        self.entry_contact = ctk.CTkEntry(form_grid, width=350, corner_radius=8)
        self.entry_contact.grid(row=2, column=1, pady=6, padx=5, sticky="ew")
        self.entry_contact.insert(0, "9340264572")

        ctk.CTkLabel(form_grid, text="Courier ₹:").grid(row=3, column=0, sticky="w", pady=6, padx=5)
        self.entry_charges = ctk.CTkEntry(form_grid, width=350, corner_radius=8)
        self.entry_charges.grid(row=3, column=1, pady=6, padx=5, sticky="ew")
        self.entry_charges.insert(0, "220")

        ctk.CTkLabel(form_grid, text="AWB No:").grid(row=4, column=0, sticky="w", pady=6, padx=5)
        self.entry_awb = ctk.CTkEntry(form_grid, width=350, corner_radius=8, border_width=1.5, border_color="#0a2256")
        self.entry_awb.grid(row=4, column=1, pady=6, padx=5, sticky="ew")

        form_grid.grid_columnconfigure(1, weight=1)

        # Checkboxes
        self.var_3copies = ctk.BooleanVar(value=True)
        self.var_paper_save = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(form_card, text="1 Portrait Page me 3 Copies (Receiver, Sender, POD)", variable=self.var_3copies, font=ctk.CTkFont(size=11)).pack(anchor="w", padx=15, pady=3)
        ctk.CTkCheckBox(form_card, text="📄 Paper Save: Only Sender top, other 2 blank", variable=self.var_paper_save, font=ctk.CTkFont(size=11, weight="bold"), text_color="#0a2256").pack(anchor="w", padx=15, pady=3)

        # Generate Button - Premium
        ctk.CTkButton(form_card, text="✨  GENERATE INVOICE  (PDF + PNG) - Full Window Premium", command=self.generate, fg_color="#0a2256", hover_color="#0a3a8a", corner_radius=12, font=ctk.CTkFont(size=14, weight="bold"), height=50).pack(fill="x", padx=15, pady=12)

        # Print buttons
        self.print_frame = ctk.CTkFrame(form_card, fg_color="white")
        self.print_frame.pack(fill="x", padx=12, pady=5)

        self.btn_print = ctk.CTkButton(self.print_frame, text="🖨️  Direct Print", command=self.direct_print, fg_color="#0a8a00", corner_radius=8, width=140)
        self.btn_open = ctk.CTkButton(self.print_frame, text="📂  Open Folder", command=self.open_folder, fg_color="#555", corner_radius=8, width=140)

        self.status = ctk.CTkLabel(form_card, text="✅ Ready - Full Window Dashboard | Premium Account", text_color="#0a8a00", font=ctk.CTkFont(size=10))
        self.status.pack(pady=5)

        # Premium Account button like your image
        ctk.CTkButton(content, text="Premium Account", fg_color="#00bcd4", corner_radius=6, width=150, height=30).pack(anchor="e", pady=10, padx=10)

        self.bind('<Control-v>', lambda e: self.paste_from_clipboard())

    def create_stat_card(self, parent, opt, num, desc, color, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, width=150, border_width=1, border_color="#e0e0e0")
        card.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
        card.grid_propagate(False)
        parent.grid_columnconfigure(col, weight=1)

        ctk.CTkLabel(card, text=opt, font=ctk.CTkFont(size=10), text_color="#666").pack(anchor="w", padx=10, pady=(8,2))
        ctk.CTkLabel(card, text=num, font=ctk.CTkFont(size=12, weight="bold"), fg_color=color, text_color="white", corner_radius=4, padx=8, pady=2).pack(anchor="w", padx=10)
        ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=9), text_color="#999").pack(anchor="w", padx=10, pady=2)

    def create_bar_card(self, parent, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, width=150, border_width=1, border_color="#e0e0e0")
        card.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
        card.grid_propagate(False)
        ctk.CTkLabel(card, text="OPTION 1\nOPTION 2", font=ctk.CTkFont(size=9), justify="left").pack(padx=10, pady=10)
        # Bars
        ctk.CTkProgressBar(card, width=100, progress_color="#7a8bff").pack(pady=2)
        ctk.CTkProgressBar(card, width=80, progress_color="#9aa8ff").pack(pady=2)

    def create_circle_card(self, parent, opt, percent, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, width=150, height=150, border_width=1, border_color="#e0e0e0")
        card.grid(row=0, column=col, padx=5, pady=5)
        card.grid_propagate(False)
        ctk.CTkLabel(card, text=opt, font=ctk.CTkFont(size=10, weight="bold")).pack(pady=(10,5))
        # Circle mockup
        ctk.CTkLabel(card, text=f"◯ {percent}", font=ctk.CTkFont(size=20, weight="bold"), text_color="#7a8bff").pack(pady=20)

    def get_logo_path(self):
        import sys
        paths = [get_resource_path("assets/DTDC_logo.png"), "assets/DTDC_logo.png", str(Path(__file__).parent / "assets" / "DTDC_logo.png")]
        for p in paths:
            if Path(p).exists():
                return str(p)
        return "assets/DTDC_logo.png"

    def browse_image(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg *.pdf")])
        if path:
            self.process_new_image(path, "Browsed")

    def paste_from_clipboard(self):
        try:
            from PIL import ImageGrab
            img = ImageGrab.grabclipboard()
            if img is None:
                messagebox.showwarning("Clipboard Empty", "Win+Shift+S se capture karo fir Ctrl+V")
                return
            if isinstance(img, list):
                if len(img) > 0:
                    self.process_new_image(img[0], "Clipboard")
                    return
            save_path = Path("input_images") / f"snip_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
            save_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(save_path))
            self.process_new_image(str(save_path), "SnipTool")
        except Exception as e:
            messagebox.showerror("Paste Failed", str(e))

    def process_new_image(self, image_path, source):
        self.input_image_path = image_path
        self.lbl_image.configure(text=f"✅ {source}: {Path(image_path).name}", text_color="#0a8a00")
        try:
            raw_text = extract_text_from_image(image_path)
            if not raw_text or len(raw_text.strip()) < 10:
                try:
                    import fitz
                    if str(image_path).lower().endswith('.pdf'):
                        doc = fitz.open(image_path)
                        raw_text = ""
                        for page in doc:
                            raw_text += page.get_text("text") + "\n"
                except:
                    pass
            parsed = parse_dtdc_fields(raw_text) if raw_text else {}
            new_awb = parsed.get('awb','')
            if new_awb:
                self.entry_awb.delete(0, tk.END)
                self.entry_awb.insert(0, new_awb)
                self.lbl_awb.configure(text=f"✅ NEW Tracking: {new_awb} (Old nahi, naya!)")
        except Exception as e:
            print(f"OCR failed: {e}")

    def generate(self):
        data = {}
        img_to_use = self.input_image_path
        if not img_to_use:
            input_dir = Path("input_images")
            images = list(input_dir.glob("*.png")) + list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg")) + list(input_dir.glob("*.pdf"))
            images = [p for p in images if p.name not in [".gitkeep", "README.txt"] and p.stat().st_size > 100]
            if images:
                img_to_use = max(images, key=lambda p: p.stat().st_mtime)
        if img_to_use and Path(img_to_use).exists():
            try:
                raw = extract_text_from_image(str(img_to_use))
                if (not raw or len(raw.strip())<10) and str(img_to_use).lower().endswith('.pdf'):
                    try:
                        import fitz
                        doc = fitz.open(str(img_to_use))
                        raw = ""
                        for page in doc:
                            raw += page.get_text("text") + "\n"
                    except:
                        pass
                parsed = parse_dtdc_fields(raw) if raw else {}
                data.update(parsed)
            except:
                pass

        data['consignor_name'] = self.entry_name.get().strip() or "Dharmendra kumar kushwaha"
        data['consignor_address'] = self.entry_address.get().strip() or "Ghatehkala post rahikwara"
        data['consignor_phone'] = self.entry_contact.get().strip() or "9340264572"
        data['courier_charges'] = self.entry_charges.get().strip() or "220"
        if self.entry_awb.get().strip():
            data['awb'] = self.entry_awb.get().strip()
        if 'origin' not in data or not data['origin']:
            data['origin'] = "SATNA"
        if 'dest' not in data or not data['dest']:
            data['dest'] = "TRICHUR"
        if 'awb' not in data or not data['awb']:
            data['awb'] = self.entry_awb.get().strip() or "7X117632485"

        logo_path = self.get_logo_path()
        output_dir = "invoices"

        try:
            if self.var_3copies.get():
                if self.var_paper_save.get():
                    data['paper_save_mode'] = True
                result = generate_3_copies_portrait(data, logo_path, output_dir)
                if result and result['pdf']:
                    self.last_pdf = result['pdf']
                    self.btn_print.pack(side="left", padx=5)
                    self.btn_open.pack(side="left", padx=5)
                    self.status.configure(text=f"✅ 3 Copies Generated: {result['pdf']}")
                    messagebox.showinfo("Success", f"3 Copies Generated!\n{result['pdf']}")
                    return

            result = generate_invoice(data, logo_path, output_dir)
            if result and result['pdf']:
                self.last_pdf = result['pdf']
                self.btn_print.pack(side="left", padx=5)
                self.btn_open.pack(side="left", padx=5)
                self.status.configure(text=f"✅ Generated: {result['pdf']}")
                messagebox.showinfo("Success", f"Generated!\n{result['pdf']}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", str(e))

    def direct_print(self):
        if not self.last_pdf or not Path(self.last_pdf).exists():
            messagebox.showwarning("No PDF", "Pehle generate karo!")
            return
        pdf_path = Path(self.last_pdf).absolute()
        try:
            if platform.system() == "Windows":
                os.startfile(str(pdf_path), "print")
            elif platform.system() == "Darwin":
                subprocess.run(["open", str(pdf_path)])
            else:
                subprocess.run(["xdg-open", str(pdf_path)])
            self.open_folder()
        except:
            try:
                if platform.system() == "Windows":
                    os.startfile(str(pdf_path))
                else:
                    import webbrowser
                    webbrowser.open(str(pdf_path))
            except Exception as e:
                messagebox.showerror("Print Failed", str(e))

    def open_folder(self):
        try:
            folder = Path("invoices/PDF").absolute()
            if platform.system() == "Windows":
                os.startfile(str(folder))
            elif platform.system() == "Darwin":
                subprocess.run(["open", str(folder)])
            else:
                subprocess.run(["xdg-open", str(folder)])
        except:
            pass

if __name__ == "__main__":
    app = DTDC_Dashboard()
    app.mainloop()
