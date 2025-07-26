import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import shutil
from tqdm import tqdm

# Main OCR Application Class
class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Text Extractor")
        
        # Variables
        self.files = []
        self.input_lang = tk.StringVar(value='eng')
        self.output_format = tk.StringVar(value='Text')

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # File Selection Button
        tk.Button(self.root, text="Select Files", command=self.select_files).pack(pady=5)

        # Language Dropdown
        langs = ['eng', 'deu', 'fra', 'spa', 'ita']  # Extend as needed
        tk.Label(self.root, text="Input Language").pack()
        ttk.Combobox(self.root, textvariable=self.input_lang, values=langs, state='readonly').pack(pady=5)

        # Output Format Dropdown
        formats = ['Text', 'HTML', 'PDF', 'XML']
        tk.Label(self.root, text="Output Format").pack()
        ttk.Combobox(self.root, textvariable=self.output_format, values=formats, state='readonly').pack(pady=5)

        # Start OCR Button
        tk.Button(self.root, text="Start OCR", command=self.start_ocr).pack(pady=10)

        # Progress Label
        self.progress_label = tk.Label(self.root, text="Waiting...")
        self.progress_label.pack(pady=5)

    def select_files(self):
        filetypes = (('Image and PDF files', '*.png *.jpg *.jpeg *.bmp *.tiff *.pdf'),)
        self.files = filedialog.askopenfilenames(filetypes=filetypes)

    def start_ocr(self):
        if not self.files:
            messagebox.showerror("Error", "No files selected!")
            return

        lang = self.input_lang.get()
        format_choice = self.output_format.get()

        for file_path in tqdm(self.files, desc="Processing Files"):
            try:
                filename, ext = os.path.splitext(os.path.basename(file_path))
                ext = ext.lower()
                
                if ext == '.pdf':
                    images = convert_from_path(file_path)
                else:
                    images = [Image.open(file_path)]

                output_content = b"" if format_choice != 'Text' else ""

                for idx, img in enumerate(images):
                    if format_choice == 'Text':
                        text = pytesseract.image_to_string(img, lang=lang)
                        output_content += text + "\n"
                    elif format_choice == 'HTML':
                        output_content += pytesseract.image_to_pdf_or_hocr(img, extension='hocr')
                    elif format_choice == 'PDF':
                        output_content += pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
                    elif format_choice == 'XML':
                        output_content += pytesseract.image_to_pdf_or_hocr(img, extension='alto')

                # Save output
                folder = os.path.dirname(file_path)
                if format_choice == 'Text':
                    output_file = os.path.join(folder, f"{filename}_output.txt")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(output_content)
                else:
                    ext_map = {'HTML': 'html', 'PDF': 'pdf', 'XML': 'xml'}
                    save_ext = ext_map[format_choice]
                    output_file = os.path.join(folder, f"{filename}_output.{save_ext}")
                    with open(output_file, 'wb') as f:
                        f.write(output_content)

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        self.progress_label.config(text="Completed!")
        messagebox.showinfo("Done", "OCR processing completed!")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
