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