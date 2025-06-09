"""Scrollable check-box + formula editor for every column."""

import tkinter as tk
from tkinter import ttk

from gui.ui.utils import (
    PAD_X, PAD_Y, PREVIEW_COLOR, BG_COLOR, USE_ENHANCED_UI
)

# optional enhanced widget
try:
    from gui.ui.custom_widgets import FormulaEntry          # noqa: F401
except ImportError:                                         # falls back to tk.Entry
    FormulaEntry = None


def build(app):
    outer = ttk.LabelFrame(app.root, text="Column Controls")
    outer.pack(fill="both", expand=True, padx=PAD_X, pady=(0, PAD_Y))

    # ---------------- scrollable canvas -----------------
    wrapper = ttk.Frame(outer)
    wrapper.pack(fill="both", expand=True, padx=PAD_X, pady=PAD_Y)

    canvas = tk.Canvas(wrapper, borderwidth=0, highlightthickness=0, background="white")
    vbar   = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vbar.set)

    vbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    app.columns_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=app.columns_frame, anchor="nw")

    def _update_region(_):            # keep scroll-region in sync
        canvas.configure(scrollregion=canvas.bbox("all"))
    app.columns_frame.bind("<Configure>", _update_region)

    # ----------------------------------------------------
    # styled row-builder – overrides app.add_column_row
    # ----------------------------------------------------
    def add_row(col):
        row_bg = "#F9F9F9" if len(app.columns_frame.winfo_children()) % 2 else "white"
        row = tk.Frame(app.columns_frame, bg=row_bg)
        row.pack(fill="x", pady=2, padx=5)

        sel_var = tk.BooleanVar()
        tk.Checkbutton(row, text=col, variable=sel_var, bg=row_bg).grid(row=0, column=0, sticky="w")
        app.column_vars[col] = sel_var

        formula_var = tk.StringVar()
        EntryCls = FormulaEntry if (USE_ENHANCED_UI and FormulaEntry) else tk.Entry
        ent = EntryCls(row, textvariable=formula_var, width=42)
        ent.grid(row=0, column=1, sticky="ew", padx=4)
        ent.bind("<KeyRelease>", lambda _e, c=col: app.update_formula_preview(c))
        app.formula_vars[col] = formula_var

        row.grid_columnconfigure(1, weight=1)

        prev = tk.Label(row, text="", font=("Consolas", 9), fg=PREVIEW_COLOR, bg=row_bg)
        prev.grid(row=1, column=1, sticky="w", padx=4)
        app.preview_labels[col] = prev

    app.add_column_row = add_row
    return outer
