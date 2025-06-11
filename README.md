# simplyPDF 

A simple Python GUI app to convert one or more images into a single PDF. Features include image rotation correction, A4 fitting, and size compression.

# AIM
The aim of this project is to simplify and speed up the process of converting images into compressed PDF files, especially for tasks like filling out online application forms where documents are required in specific formats and under size limits. Instead of relying on multiple websites — one for converting images to PDF and another for reducing file size — this tool provides a smooth, all-in-one solution to make the process faster, easier, and more user-friendly.

## Features
- Upload multiple images
- Auto-rotation fix using EXIF
- Resize to fit A4
- Set target PDF file size
- Compresses smartly by adjusting quality
- Clean GUI using Tkinter

## How to Run
1. Make sure Python is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```

## Dependencies
- Pillow
- fpdf
- tkinter (comes pre-installed with Python)

## License
MIT
