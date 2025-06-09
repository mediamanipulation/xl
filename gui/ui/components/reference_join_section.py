"""Widgets for adding a reference workbook join."""

from tkinter import ttk
from gui.ui.utils import PAD_X, PAD_Y, FIELD_PAD


def build(app):
    frame = ttk.LabelFrame(app.root, text="Reference File Join")
    frame.pack(fill="x", padx=PAD_X, pady=(0, PAD_Y))

    inner = ttk.Frame(frame)
    inner.pack(fill="x", padx=PAD_X, pady=PAD_Y)

    ttk.Button(inner, text="Load Reference", command=app.load_reference_file).grid(row=0, column=0, padx=FIELD_PAD)

    ttk.Label(inner, text="Main Key:").grid(row=0, column=1, sticky="e")
    app.main_key_entry = ttk.Entry(inner, width=18)
    app.main_key_entry.grid(row=0, column=2, padx=FIELD_PAD)

    ttk.Label(inner, text="Ref Key:").grid(row=0, column=3, sticky="e")
    app.ref_key_entry = ttk.Entry(inner, width=18)
    app.ref_key_entry.grid(row=0, column=4, padx=FIELD_PAD)

    ttk.Label(inner, text="Ref Columns:").grid(row=0, column=5, sticky="e")
    app.ref_cols_entry = ttk.Entry(inner, width=28)
    app.ref_cols_entry.grid(row=0, column=6, padx=FIELD_PAD)

    inner.columnconfigure(6, weight=1)
    return frame
