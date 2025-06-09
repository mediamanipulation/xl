# gui/confluence/ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from .settings import save_confluence_settings, load_confluence_settings
from .uploader import upload_to_page
import os


def build_confluence_settings_dialog(app):
    """Open a dialog to configure Confluence settings."""
    dialog = tk.Toplevel(app.root)
    dialog.title("Confluence Settings")
    dialog.grab_set()
    dialog.resizable(False, False)

    tk.Label(dialog, text="Confluence Base URL:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    base_var = tk.StringVar()
    tk.Entry(dialog, textvariable=base_var, width=40).grid(row=0, column=1, padx=5, pady=5)

    tk.Label(dialog, text="API Token:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    token_var = tk.StringVar()
    tk.Entry(dialog, textvariable=token_var, width=40, show="*").grid(row=1, column=1, padx=5, pady=5)

    def save():
        base = base_var.get().strip()
        token = token_var.get().strip()
        if not base or not token:
            messagebox.showwarning("Input Error", "Both fields are required.")
            return
        save_confluence_settings(base, token)
        messagebox.showinfo("Saved", "Confluence settings saved.")
        dialog.destroy()

    ttk.Button(dialog, text="Save", command=save).grid(row=2, column=1, pady=10, sticky="e")


def attach_upload_button(parent_frame, app):
    """Attach a Confluence Upload button to an existing frame."""
    def upload():
        if app.file_path is None or not os.path.exists(app.file_path):
            messagebox.showwarning("Export Required", "Please export the Excel file first.")
            return

        settings = load_confluence_settings()
        if not settings:
            messagebox.showwarning("Settings Missing", "Please configure Confluence settings first.")
            build_confluence_settings_dialog(app)
            return

        def do_upload():
            page_id = app.simple_input_dialog("Confluence Page ID", "Enter Confluence Page ID:")
            if not page_id:
                return
            try:
                result = upload_to_page(app.file_path, page_id)
                messagebox.showinfo("Upload Success", f"File uploaded to page {page_id}")
            except Exception as e:
                messagebox.showerror("Upload Failed", str(e))
                
            print("[DEBUG] Attaching Upload to Confluence button")  

        app.root.after(100, do_upload)

    upload_btn = ttk.Button(parent_frame, text="Upload to Confluence", command=upload)
    upload_btn.pack(side="right", padx=5)
