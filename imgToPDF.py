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
