# File: export_filename_customizer.py
# Location: gui/ui/components/

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from gui.confluence.settings import load_confluence_settings
from gui.confluence.uploader import upload_to_page

class ExportFilenameCustomizer(tk.Frame):
    def __init__(self, master, on_export):
        super().__init__(master)
        self.on_export = on_export

        # --- Title dropdown ---
        self.title_var = tk.StringVar()
        ttk.Label(self, text="Export Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_dropdown = ttk.Combobox(self, textvariable=self.title_var, state="readonly")
        self.title_dropdown['values'] = ["Sales_Report", "Inventory_Snapshot", "Monthly_Review"]
        self.title_dropdown.current(0)
        self.title_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # --- Date (today by default) ---
        self.date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        ttk.Label(self, text="Date:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(self, textvariable=self.date_var, width=12)
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)

        # --- Filename preview ---
        self.preview_var = tk.StringVar()
        self.update_preview()
        self.title_var.trace_add('write', lambda *_: self.update_preview())
        self.date_var.trace_add('write', lambda *_: self.update_preview())

        ttk.Label(self, text="Filename Preview:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self, textvariable=self.preview_var, foreground="gray").grid(row=1, column=1, columnspan=3, sticky="w")

        # --- Export Button ---
        ttk.Button(self, text="Export", command=self.handle_export).grid(row=2, column=3, padx=5, pady=10, sticky="e")

        # --- Upload Button ---
        ttk.Button(self, text="Upload to Confluence", command=self.handle_upload).grid(row=2, column=2, padx=5, pady=10, sticky="e")

    def update_preview(self):
        title = self.title_var.get()
        date = self.date_var.get()
        self.preview_var.set(f"{title}_{date}.xlsx")

    def handle_export(self):
        suggested_name = self.preview_var.get()
        out_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialfile=suggested_name,
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if out_path:
            self.exported_path = out_path  # Store for Confluence upload
            self.on_export(out_path)

    def handle_upload(self):
        if not hasattr(self, 'exported_path') or not self.exported_path:
            messagebox.showwarning("Missing File", "Please export the Excel file first.")
            return

        settings = load_confluence_settings()
        if not settings:
            messagebox.showwarning("No Settings", "Please configure Confluence settings first.")
            return

        page_id = tk.simpledialog.askstring("Confluence Page ID", "Enter Confluence Page ID:")
        if not page_id:
            return

        try:
            upload_to_page(self.exported_path, page_id)
            messagebox.showinfo("Success", f"Uploaded to Confluence page {page_id}")
        except Exception as e:
            messagebox.showerror("Upload Failed", str(e))

# Example usage:
if __name__ == "__main__":
    def dummy_export(path):
        messagebox.showinfo("Exporting", f"Would export to:\n{path}")

    root = tk.Tk()
    root.title("Export UI")
    ExportFilenameCustomizer(root, on_export=dummy_export).pack(padx=10, pady=10)
    root.mainloop()
