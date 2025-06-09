"""Preset picker for column formulas/selection."""

import tkinter as tk
from tkinter import ttk
from gui.ui.utils import PAD_X, PAD_Y, create_tooltip


def build(app):
    frame = ttk.LabelFrame(app.root, text="Column Presets")
    frame.pack(fill="x", padx=PAD_X, pady=(0, PAD_Y))

    inner = ttk.Frame(frame)
    inner.pack(fill="x", padx=PAD_X, pady=PAD_Y)

    app.preset_var = tk.StringVar()
    app.preset_dropdown = ttk.Combobox(
        inner,
        textvariable=app.preset_var,
        state="readonly",
        width=32,
        values=list(app.presets.keys()),
    )
    app.preset_dropdown.pack(side="left", fill="x", expand=True)

    btn = ttk.Button(inner, text="Apply", command=app.apply_preset)
    btn.pack(side="left", padx=(PAD_X, 0))
    create_tooltip(btn, "Apply the selected preset to column checks/formulas")

    return frame
