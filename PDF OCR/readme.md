## 📄 OCR Script – Extract Text from Images

This script lets you **extract text from images using OCR (Optical Character Recognition)**. Just give it a picture with some text, and it will give you the text back — super useful for scanned documents, screenshots, handwritten notes, and more!

---

### ✨ Features

* 📷 Read and process image files (.jpg, .png, etc.)
* 🧠 Uses **Tesseract OCR** to extract printed or handwritten text
* 🖨️ Prints clean, readable output
* 💬 Can be extended for multi-language support

---

### 🧰 Built With

* [Python](https://www.python.org/)
* [pytesseract](https://github.com/madmaze/pytesseract) – Python wrapper for Google Tesseract
* [Pillow](https://pillow.readthedocs.io/) – for image loading

---

### ⚙️ Requirements

Before using the script, install:

1. **Tesseract-OCR Engine**

   * Download from: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
   * On Windows, add the Tesseract installation path to your system's PATH.

2. **Python libraries**

   ```bash
   pip install pytesseract Pillow
   ```

---

### ▶️ How to Use

1. **Put your image** file in the same folder (or give a path to it)

2. **Run the script**

   ```bash
   python ocr_script.py
   ```

3. **Enter the image file name** (e.g., `note.jpg`)

4. Get the **extracted text** printed in the terminal (and optionally saved to a text file)

---

### 📁 Example

```bash
Enter image file name: scanned_note.png  
Extracting text...  
Here’s the text from your image:
-------------------------------------
Dear John,  
Please submit the report by Friday.  
Thanks,  
Manager
-------------------------------------
```

---

### ✅ To-Do / Ideas

* Support for multiple image files at once
* Language selection (e.g., Hindi, French, etc.)
* Save output automatically to a `.txt` file
* GUI version with drag-and-drop

---

### 📝 License

Free to use, modify, and share! No attribution needed.
