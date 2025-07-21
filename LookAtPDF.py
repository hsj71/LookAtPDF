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

after_id = None

def update_background():
    global current_image_index, after_id
    try:
        if root.winfo_exists() and bg_image.winfo_exists():
            current_image_index = (current_image_index + 1) % len(images)
            bg_image.config(image=images[current_image_index])
            after_id = root.after(100, update_background)
    except tk.TclError:
        pass
   
# ---------- Variables ----------
bgc1 = "#f0f0f0"
wid, hgt = 1000, 600  # Window dimensions
last_pdf_path = None  # To store last saved PDF for "Show PDF"
# ---------- PDF Conversion ----------
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

        images = convert_from_path(pdf_path)
        poppler_dir = resource_path("/poppler-24.08.0/Library/bin")  # path to poppler's bin folder
        images = convert_from_path(pdf_path, poppler_dir)
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

global folder_path
folder_path=""

root = tk.Tk()
root.title("LookAtPDF")
root.configure(bg="#f5dda2")
root.state('zoomed')

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Load and resize 50 background images (ezgif-frame-001.jpg to ezgif-frame-050.jpg)
images = []
current_image_index = 0

for i in range(1, 51):
    img_path = resource_path(f"Frame2/ezgif-frame-{i:03}.jpg")
    img = Image.open(img_path)
    img = img.resize((screen_width, screen_height), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    images.append(img)

# Background Image Label
bg_image = tk.Label(root, image=images[current_image_index])
bg_image.place(relwidth=1, relheight=1)
update_background()

# Create canvas for the bottom marquee
#bottom_canvas = tk.Canvas(root, bg="#9c9899", height=50)
#bottom_canvas.pack(side="bottom", fill="x")

# Create canvas for the top marquee
top_canvas = tk.Canvas(root, bg="white", height=50)
top_canvas.pack(side="top", fill="x")

# Text to display
text_var = "Look At PDF"
text_var2 = "Look At PDF"
# Create moving text on both canvases
#bottom_text_id = bottom_canvas.create_text(bottom_canvas.winfo_width(), 25, text=text_var2, font=('Arial', 25, 'bold'), fill='black', tags=("bottom_marquee",), anchor='w')
top_text_id = top_canvas.create_text(top_canvas.winfo_width(), 25, text=text_var, font=('Arial', 35, 'bold'), fill='black', tags=("top_marquee",), anchor='w')

def shift(canvas, tag):
    """ Function for moving the marquee effect on a given canvas """
    canvas_width = canvas.winfo_width()  # Get the updated width of the canvas
    x1, y1, x2, y2 = canvas.bbox(tag)

    # If the text moves off the canvas to the left, reset its position to the right
    if x2 < 0:
        canvas.move(tag, canvas_width + (x2 - x1), 0)
    else:
        canvas.move(tag, -4, 0)  # Move left by 2 pixels

    canvas.after(20, lambda: shift(canvas, tag))  # Recursive call for continuous motion

def update_positions():
    if top_canvas.winfo_exists():
        top_canvas.coords("top_marquee", top_canvas.winfo_width(), 25)

# Start the marquee on both canvases
root.update_idletasks()  # Ensure accurate canvas dimensions
#shift(bottom_canvas, "bottom_marquee")
shift(top_canvas, "top_marquee")

# Bind the window resize event to update marquee positions
root.bind("<Configure>", lambda event: update_positions())

#UI background color
bgc1="white"      #"#f7ed9c"
bgc2="#9cd3f7"
bgc="white"

wid=root.winfo_width()

folder_var = tk.StringVar()
filename_var = tk.StringVar(value="output")

# ---------- Variables ----------
image_list = []  # To store images converted from PDF
pdf_var = tk.StringVar()  # For storing selected PDF path
 
# Entry Fields
tk.Label(root, text="Selected Folder:", font=("times", 12, "bold"), bg=bgc1).place(x=50, y=120)
tk.Entry(root, textvariable=folder_var, width=60, font=('times', 12)).place(x=200, y=120)
tk.Label(root, text="Base PDF Name:", font=("times", 12, "bold"), bg=bgc1).place(x=50, y=170)
tk.Entry(root, textvariable=filename_var, width=60, font=('times', 12)).place(x=200, y=170)
status_label = tk.Label(root, text="", font=('times', 12), bg=bgc1, fg="blue")
status_label.place(x=50, y=260)

# Create a horizontal frame 1
frame_horizontal = tk.LabelFrame(root, text="1 Images to PDF",width=wid*0.45, height=80, bd=5, font=('times', 14, 'bold'), bg=bgc1, labelanchor="n")
frame_horizontal.place(x=wid*0.5,y=50)
tk.Button(frame_horizontal, text="Images Folder", command=Select_folder, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=2, y=1)
tk.Button(frame_horizontal, text="Generate PDF", command=generate_pdf, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=130, y=1)
tk.Button(frame_horizontal, text="Show PDF", command=Open_pdf, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=260, y=1)
tk.Button(frame_horizontal, text="Stored Folder", command=open_pdf_folder, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=480, y=1)

# Create a horizontal frame 2 
frame_horizontal2 = tk.LabelFrame(root,text="2 Merge PDFs", width=wid*0.45, height=80, bd=5, font=('times', 14, 'bold'), bg=bgc1, labelanchor="n")
frame_horizontal2.place(x=wid*0.5,y=130)
tk.Button(frame_horizontal2, text="PDF Folder", command=Select_folder, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=2, y=1)
tk.Button(frame_horizontal2, text="Combine PDF", command=merge_pdfs_in_folder, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=130, y=1)
tk.Button(frame_horizontal2, text="Show PDF", command=Open_pdf, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=260, y=1)
tk.Button(frame_horizontal2, text="Stored Folder", command=open_pdf_folder, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=480, y=1)

# Create a horizontal frame  3
frame_horizontal3 = tk.LabelFrame(root,text="3 PDF to Images", width=wid*0.45, height=80, bd=5, font=('times', 14, 'bold'), bg=bgc1, labelanchor="n")
frame_horizontal3.place(x=wid*0.5,y=210)
tk.Button(frame_horizontal3, text="Select PDF", command=select_pdf, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=2, y=1)
tk.Button(frame_horizontal3, text="Make Images", command=convert_pdf_to_images, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=130, y=1)
tk.Button(frame_horizontal3, text="Show Images", command=show_images, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=260, y=1)
tk.Button(frame_horizontal3, text="Stored Folder", command=open_pdf_folder, width=12, height=1, font=('times', 12, 'bold'), bg="white", fg="black").place(x=480, y=1)

# Store the after ID globally or as part of the window
after_id = None

def start_updating_background():
    global after_id
    after_id = root.after(1000, update_background)

def stop_updating_background():
    if after_id is not None:
        root.after_cancel(after_id)

# Call this when closing the window
def on_closing():
    stop_updating_background()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()