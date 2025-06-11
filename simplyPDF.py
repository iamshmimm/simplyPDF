import tkinter as tk
from tkinter import filedialog
from PIL import Image, ExifTags
from fpdf import FPDF
import tempfile
import os


def upload_and_convert():
    # Open file dialog to select multiple images
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")],
    )

    if file_paths:
        images = []
        for file_path in file_paths:
            img = Image.open(file_path)

            # Handle EXIF rotation (if exists)
            img = correct_orientation(img)

            # Convert image to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            images.append(img)

        # Ask user for target size
        target_size_window(images)


def correct_orientation(img):
    """Correct image orientation based on EXIF data."""
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = img._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)
            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # If EXIF data is not available or an error occurs, return the image as is
        pass
    return img


def generate_pdf(images, save_path, quality=95):
    pdf = FPDF(unit="pt", format="A4")
    page_width, page_height = 595, 842  # A4 size in points

    for img in images:
        pdf.add_page()
        img_width, img_height = img.size

        # Calculate the scaling factor to fit the image on an A4 page while keeping its aspect ratio
        scale_factor = min(page_width / img_width, page_height / img_height)
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)

        # Center the image on the A4 page
        x_offset = (page_width - new_width) / 2
        y_offset = (page_height - new_height) / 2

        # Save the resized image temporarily
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_img_path = temp_file.name
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            resized_img.save(temp_img_path, quality=quality)

            # Add the image to the PDF
            pdf.image(temp_img_path, x_offset, y_offset, new_width, new_height)

    pdf.output(save_path)


def target_size_window(images):
    def compress_to_target():
        target_mb = float(target_entry.get())
        target_size_bytes = target_mb * 1024 * 1024  # Convert MB to bytes

        # Check if the target size is achievable
        temp_save_path = tempfile.mktemp(suffix=".pdf")
        generate_pdf(images, temp_save_path, quality=100)
        actual_size = os.path.getsize(temp_save_path)

        if actual_size <= target_size_bytes:
            # If the original file size is already smaller or equal to the target, keep original quality
            temp_save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save PDF as",
            )

            if temp_save_path:
                generate_pdf(images, temp_save_path, quality=100)  # No quality reduction
                status_label.config(
                    text=f"PDF saved at {temp_save_path} with size {actual_size / (1024 * 1024):.2f} MB"
                )
                return
        else:
            # If the original file is too large, reduce the quality incrementally
            temp_save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save PDF as",
            )

            if not temp_save_path:
                return

            quality = 95  # Start with high quality
            while True:
                # Generate PDF with the current quality
                generate_pdf(images, temp_save_path, quality=quality)
                actual_size = os.path.getsize(temp_save_path)

                # Check if the size is within 5% of the target
                if abs(actual_size - target_size_bytes) <= target_size_bytes * 0.05 or quality <= 50:
                    break  # Stop if target is met or quality is too low

                # Adjust quality to reduce file size
                quality -= 5

            status_label.config(
                text=f"PDF saved at {temp_save_path} with size {actual_size / (1024 * 1024):.2f} MB"
            )

    # Create a new window for target size input
    compress_window = tk.Toplevel(root)
    compress_window.title("Set Target Size")

    tk.Label(compress_window, text="Enter Target PDF Size (MB):").pack(pady=10)
    target_entry = tk.Entry(compress_window)
    target_entry.pack(pady=10)

    tk.Button(compress_window, text="Generate PDF", command=compress_to_target).pack(pady=10)


# Create the main GUI application
root = tk.Tk()
root.title("Image to PDF Converter")

# Add a button to trigger the image upload and conversion
convert_button = tk.Button(
    root, text="Upload Images and Convert to PDF", command=upload_and_convert
)
convert_button.pack(pady=20)

# Add a label to show status messages
status_label = tk.Label(root, text="", fg="green")
status_label.pack(pady=10)

# Run the application
root.geometry("400x150")
root.mainloop()
