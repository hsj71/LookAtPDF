# LookAtPDF
# 📄 PDF Utility Tool
(https://drive.google.com/file/d/1jFthVt0YJ4K49ieRTegiiHaYJVZK3x-c/view?usp=drive_link)

A simple and powerful desktop application to manage your PDF and image conversion tasks with ease.

This all-in-one tool allows you to:
- Convert images to PDF
- Merge multiple PDF files into one
- Convert PDF pages to images

Built using **Python**, **Tkinter**, and packaged as a `.exe` for Windows.

---

## ✨ Features

- 🖼️ **Images to PDF**: Select multiple images (JPG, PNG, BMP) and convert them into a single PDF file.
- 📚 **Merge PDF Files**: Choose multiple PDF files and merge them into one document.
- 📄 **PDF to Images**: Convert every page of a PDF into high-quality images (PNG/JPG).
- 🧩 **Standalone EXE**: Run the app on Windows without installing Python.
- 🎨 **Clean GUI**: Built with Tkinter for a user-friendly experience.

---

## 🖼️ Working exe file

<h3>1. Saved Images</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(591).png" alt="Saved Images" width="700"/>
</p>
<h3>2. Open LookAtPDF.exe</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(596).png" alt="Open LookAtPDF.exe" width="700"/>
</p>

<h3>3. Background Changing, Header Moving Feature</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(597).png" alt="Background Changing and Header Moving" width="700"/>
</p>

<h3>4. Select Folder to Get All Images</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(600).png" alt="Select Folder for Images" width="700"/>
</p>

<h3>5. Generate PDF</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(602).png" alt="Generate PDF" width="700"/>
</p>

<h3>6. View Generated PDF</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(603).png" alt="View Generated PDF" width="700"/>
</p>

<h3>7. Selecting PDF Files for Merging</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(605).png" alt="Select PDFs for Merging" width="700"/>
</p>

<h3>8. Merge PDF Files</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(607).png" alt="Merge PDFs" width="700"/>
</p>

<h3>9. View Merged PDF Files</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(608).png" alt="View Merged PDFs" width="700"/>
</p>

<h3>10. Select PDF to Make Images</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(611).png" alt="PDF to Images" width="700"/>
</p>

<h3>11. Show Images</h3>
<p align="center">
  <img src="https://github.com/hsj71/LookAtPDF/raw/main/Images/Screenshot%20(614).png" alt="PDF to Images" width="700"/>
</p>

---

## 🚀 Tech Stack

- **Python 3**
- **Tkinter** – for GUI
- **Pillow (PIL)** – for image processing
- **PyMuPDF (fitz)** – for PDF to image conversion
- **PyPDF2** – for merging PDF files
- **PyInstaller** – for creating the `.exe` file

---

## 🛠️ Installation & Running (From Source)

1. **Download the LookAtPDF.exe**

📋 Requirements
Windows (any version)

📋 Optinal
Python 3.7 or above (not necessary). 
virtualenv for clean dependency management (not necessary)

## Important Lib's

```
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger('tensorflow').setLevel(logging.FATAL)

import subprocess
import platform
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk,ImageDraw, ImageFont
from tkinter import Scrollbar, Canvas, Frame, Label, filedialog, Button, scrolledtext
import numpy as np
import time
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from subprocess import call
from datetime import datetime
from tkinter import simpledialog
import sys
from tkinter import filedialog, messagebox
import webbrowser
from PyPDF2 import PdfMerger 
from pdf2image import convert_from_path
from PIL import ImageTk
```
## Functional Part
```
def convert_images_to_pdf(folder_path, base_filename):
    global last_pdf_path
    image_files = [f for f in os.listdir(folder_path)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'))]
    image_files.sort()

    if not image_files:
        return "No image files found in the folder."

    image_list = []
    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)
        with Image.open(img_path) as img:
            img = img.convert('RGB')
            image_list.append(img)

    first_image = image_list.pop(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_filename = f"{base_filename}_{timestamp}.pdf"
    output_path = os.path.join(folder_path, final_filename)
    first_image.save(output_path, save_all=True, append_images=image_list)
    last_pdf_path = output_path
    return f"PDF saved successfully at:\n{output_path}"

# ---------- Button Commands ----------
def Select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def generate_pdf():
    folder = folder_var.get()
    base_filename = filename_var.get().strip()
    if not folder:
        messagebox.showwarning("Missing Folder", "Please select a folder.")
        return
    if not base_filename:
        messagebox.showwarning("Missing Filename", "Please enter a base filename.")
        return
    try:
        result = convert_images_to_pdf(folder, base_filename)
        status_label.config(text=result, fg="green")
    except Exception as e:
        status_label.config(text=f"Error: {e}", fg="red")

def Open_pdf():
    if last_pdf_path and os.path.exists(last_pdf_path):
        webbrowser.open_new(rf"file://{last_pdf_path}")
    else:
        messagebox.showinfo("No PDF", "No PDF has been generated yet.")

def open_pdf_folder():
    if last_pdf_path and os.path.exists(last_pdf_path):
        folder_path = os.path.dirname(last_pdf_path)
        try:
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", folder_path])
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open folder:\n{e}")
    else:
        messagebox.showinfo("No PDF", "No PDF has been generated yet.")
        
def merge_pdfs_in_folder():
    folder = folder_var.get()
    if not folder:
        messagebox.showwarning("Missing Folder", "Please select a folder.")
        return

    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    pdf_files.sort()

    if not pdf_files:
        messagebox.showinfo("No PDFs", "No PDF files found in the selected folder.")
        return

    merger = PdfMerger()
    try:
        for pdf in pdf_files:
            merger.append(os.path.join(folder, pdf))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        merged_pdf_name = f"merged_{timestamp}.pdf"
        output_path = os.path.join(folder, merged_pdf_name)
        merger.write(output_path)
        merger.close()

        global last_pdf_path
        last_pdf_path = output_path
        status_label.config(text=f"Merged PDF saved at:\n{output_path}", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")
      
def select_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if pdf_path:
        pdf_var.set(pdf_path)

def convert_pdf_to_images():
    global image_list
    pdf_path = pdf_var.get().strip()
    if not pdf_path or not os.path.exists(pdf_path):
        messagebox.showwarning("Invalid PDF", "Please select a valid PDF file.")
        return

    try:
        # Extract PDF name (without extension)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_folder = os.path.dirname(pdf_path)  # Same folder as the PDF

        # Use resource_path for bundled poppler bin
        poppler_dir = resource_path("poppler-24.08.0/Library/bin")  # Adjust path if needed
        images = convert_from_path(pdf_path, poppler_path=poppler_dir)
        image_list = images  # Store images for later use

        # Save each image with a proper name (pdfname_pageX.png)
        for i, img in enumerate(images):
            image_name = f"{pdf_name}_page{i + 1}.png"
            image_path = os.path.join(output_folder, image_name)
            img.save(image_path, "PNG")

        status_label.config(text=f"Converted {len(images)} pages to images.", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert PDF to images:\n{e}")
        
def show_images():
    global image_list
    if not image_list:
        messagebox.showwarning("No Images", "Please convert a PDF to images first.")
        return

    # Create a new top-level window to display the images
    image_window = tk.Toplevel(root)
    image_window.title("PDF Images")
    image_window.geometry("800x600")

    for i, img in enumerate(image_list):
        img.thumbnail((300, 300))  # Resize images to fit
        photo = ImageTk.PhotoImage(img)

        img_label = tk.Label(image_window, image=photo)
        img_label.image = photo  # Keep reference to avoid garbage collection
        img_label.grid(row=i // 3, column=i % 3, padx=10, pady=10)  # Grid layout (3 images per row)         
                 
def Refresh():
    os.execv(sys.executable, ['python'] + sys.argv)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev & PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def window():
    root.destroy()

```

# Use Cases
Combine multiple scanned images into a single PDF.

Split or rearrange content by merging selected pages.

Extract pages from a PDF as images for annotation or sharing.

---
# Credits
Created  by [Hrishikesh Jadhav]
Feel free to fork, star, or contribute to improve the tool!

---
