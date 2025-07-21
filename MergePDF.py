       
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
      