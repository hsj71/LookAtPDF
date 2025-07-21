
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