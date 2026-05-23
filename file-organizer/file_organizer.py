# file_organizer_gui.py

import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def organize_files_by_type(directory, dry_run, output_box):
    if not os.path.isdir(directory):
        messagebox.showerror("Error", f"The directory '{directory}' does not exist.")
        return

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        output_box.insert(tk.END, "No files found in the directory.\n")
        return

    for file in files:
        ext = Path(file).suffix.lower().strip('.')
        if not ext:
            ext = 'no_extension'

        folder = os.path.join(directory, ext)
        src = os.path.join(directory, file)
        dest = os.path.join(folder, file)

        if dry_run:
            output_box.insert(tk.END, f"[Dry Run] Would move '{file}' to '{ext}/'\n")
        else:
            os.makedirs(folder, exist_ok=True)
            shutil.move(src, dest)
            output_box.insert(tk.END, f"Moved '{file}' to '{ext}/'\n")

    output_box.insert(tk.END, "\n✅ Done!\n")
    output_box.see(tk.END)

def browse_folder(entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry.delete(0, tk.END)
        entry.insert(0, folder_selected)

def main():
    window = tk.Tk()
    window.title("File Organizer")
    window.geometry("600x400")
    window.resizable(False, False)

    
    tk.Label(window, text="Select Folder:").pack(pady=5)
    folder_entry = tk.Entry(window, width=60)
    folder_entry.pack()
    tk.Button(window, text="Browse", command=lambda: browse_folder(folder_entry)).pack(pady=5)

    
    dry_run_var = tk.BooleanVar()
    dry_run_check = tk.Checkbutton(window, text="Dry Run (preview only)", variable=dry_run_var)
    dry_run_check.pack()

    
    output_box = scrolledtext.ScrolledText(window, width=70, height=15)
    output_box.pack(pady=10)

    
    run_button = tk.Button(window, text="Organize Files", command=lambda: organize_files_by_type(folder_entry.get(), dry_run_var.get(), output_box))
    run_button.pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    main()
