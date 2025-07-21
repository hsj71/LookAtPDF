def resource_path(relative_path):
    """ Get absolute path to resource, works for dev & PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def Select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

       
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