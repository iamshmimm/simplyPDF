# simplyPDF 

A simple Python GUI app to convert one or more images into a single PDF. Features include image rotation correction, A4 fitting, and size compression.

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
