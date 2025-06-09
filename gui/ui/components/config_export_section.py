"""Save / load configuration + export button + recent list."""

import tkinter as tk
from tkinter import ttk, messagebox

from gui.ui.utils import (
    PAD_X, PAD_Y, FIELD_PAD, USE_ENHANCED_UI, create_tooltip
)
from gui.core.config_manager import load_config

# optional enhanced widget
try:
    from gui.ui.custom_widgets import TooltipButton
except ImportError:
    TooltipButton = None


def build(app):
    frame = ttk.LabelFrame(app.root, text="Configuration and Export")
    frame.pack(fill="x", padx=PAD_X, pady=(0, PAD_Y))

    row = ttk.Frame(frame)
    row.pack(fill="x", padx=PAD_X, pady=PAD_Y)

    # --- Save / Load Config ---
    ttk.Button(row, text="Save Config", command=app.save_config) \
        .pack(side="left", padx=(0, FIELD_PAD))
    ttk.Button(row, text="Load Config", command=app.load_config) \
        .pack(side="left", padx=(0, FIELD_PAD))

    # --- Recent Configs Dropdown ---
    ttk.Label(row, text="Recent:").pack(side="left", padx=(FIELD_PAD * 3, FIELD_PAD))
    app.recent_var = tk.StringVar()
    app.recent_combo = ttk.Combobox(
        row,
        textvariable=app.recent_var,
        state="readonly",
        width=48,
        values=app.recent_configs,
    )
    app.recent_combo.pack(side="left", padx=(0, PAD_X))

    def _load_recent(_):
        sel = app.recent_var.get()
        if not sel:
            return
        try:
            cfg = load_config(sel)
            app._apply_loaded_config(cfg)
        except Exception as exc:
            messagebox.showerror("Load Error", exc)

    app.recent_combo.bind("<<ComboboxSelected>>", _load_recent)

    # --- Export Button ---
    if USE_ENHANCED_UI and TooltipButton:
        export_btn = TooltipButton(
            row, text="EXPORT DATA", command=app.export,
            tooltip_text="Process data and write a new Excel file"
        )
    else:
        export_btn = ttk.Button(row, text="EXPORT DATA", command=app.export)

    export_btn.pack(side="right", padx=(FIELD_PAD, 0))
    if USE_ENHANCED_UI:
        create_tooltip(export_btn, "Generate the output Excel")

    # --- Confluence Upload Button ---
    try:
        from gui.confluence.ui import attach_upload_button
        attach_upload_button(row, app)
    except Exception as exc:
        print(f"[Confluence] Upload button attach failed: {exc}")

    return frame
