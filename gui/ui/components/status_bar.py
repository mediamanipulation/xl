"""Bottom status bar that exposes app.update_status()."""

import tkinter as tk
from tkinter import ttk
from gui.ui.utils import PAD_X, PAD_Y, flash_success_message, PREVIEW_COLOR


def build(app):
    frame = ttk.Frame(app.root)
    frame.pack(side="bottom", fill="x", padx=PAD_X, pady=PAD_Y)

    app.status_var = tk.StringVar(value="Ready")
    ttk.Label(frame, textvariable=app.status_var, anchor="w").pack(side="left")

    def update_status(msg, success=None):
        app.status_var.set(msg)
        app.root.update_idletasks()
        if success:
            flash_success_message(app.status_var, msg)

    app.update_status = update_status
    return frame
