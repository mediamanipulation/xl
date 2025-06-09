"""Main-file chooser + sheet selector."""

import tkinter as tk
from tkinter import ttk
from gui.ui.utils import PAD_X, PAD_Y, FIELD_PAD, BG_COLOR, create_tooltip


def build(app):
    frame = ttk.LabelFrame(app.root, text="Source File")
    frame.pack(fill="x", padx=PAD_X, pady=(0, PAD_Y))

    # --- row 1: choose file, header row, sheet ---
    row = ttk.Frame(frame)
    row.pack(fill="x", padx=PAD_X, pady=PAD_Y)

    btn = ttk.Button(row, text="Load Excel File", command=app.load_main_file)
    btn.pack(side="left")
    create_tooltip(btn, "Select the main workbook")

    ttk.Label(row, text="Header Row:").pack(side="left", padx=FIELD_PAD)
    ttk.Entry(row, textvariable=app.header_row, width=5).pack(side="left")

    ttk.Label(row, text="Sheet:").pack(side="left", padx=(PAD_X, FIELD_PAD))
    app.sheet_dropdown = ttk.Combobox(row, state="readonly", width=24)
    app.sheet_dropdown.pack(side="left")
    app.sheet_dropdown.bind("<<ComboboxSelected>>", app.load_sheet)

    return frame
