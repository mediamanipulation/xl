# gui/app.py
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd

from gui.ui.layout import build_layout
from gui.core.presets import load_presets, apply_preset
from gui.core.formula_engine import evaluate_formula
from gui.core.exporter import export_to_excel

# alias imported helpers to avoid name-clash with our class methods
from gui.core.config_manager import (
    save_config as cfg_save,
    load_config as cfg_load,
    list_recent,
)


class ExcelTransformerApp:
    """Main Tkinter GUI application."""

    # ------------------------------------------------------------------ #
    # Initialisation                                                     #
    # ------------------------------------------------------------------ #
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Matrix Exporter")

        # state
        self.df = None
        self.ref_df = None
        self.file_path = None
        self.header_row = tk.IntVar(value=0)

        # UI‐bound dicts
        self.column_vars: dict[str, tk.BooleanVar] = {}
        self.formula_vars: dict[str, tk.StringVar] = {}
        self.preview_labels: dict[str, tk.Label] = {}

        # presets + recent configs
        self.presets_path = "presets.json"
        self.presets = load_presets(self.presets_path)
        self.recent_configs = list_recent()

        # build GUI
        build_layout(self)

    # ------------------------------------------------------------------ #
    # File + sheet handling                                              #
    # ------------------------------------------------------------------ #
    def load_main_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not path:
            return
        self.file_path = path
        xls = pd.ExcelFile(path)
        self.sheet_dropdown.configure(values=xls.sheet_names)
        self.sheet_dropdown.current(0)
        self.load_sheet()

    def load_sheet(self, *_):
        sheet_name = self.sheet_dropdown.get()
        self.df = pd.read_excel(
            self.file_path,
            sheet_name=sheet_name,
            header=self.header_row.get(),
        )

        # clear old widgets/vars
        self.column_vars.clear()
        self.formula_vars.clear()
        self.preview_labels.clear()
        for widget in self.columns_frame.winfo_children():
            widget.destroy()

        # rebuild
        for col in self.df.columns:
            self.add_column_row(col)

    # ------------------------------------------------------------------ #
    # Dynamic column-row creation                                        #
    # ------------------------------------------------------------------ #
    def add_column_row(self, col: str) -> None:
        row = tk.Frame(self.columns_frame)
        row.pack(anchor="w", pady=1, padx=5, fill="x")

        var = tk.BooleanVar()
        tk.Checkbutton(row, text=col, variable=var).grid(row=0, column=0, sticky="w")
        self.column_vars[col] = var

        f_var = tk.StringVar()
        entry = tk.Entry(row, textvariable=f_var, width=35)
        entry.grid(row=0, column=1, padx=4, sticky="ew")
        entry.bind("<KeyRelease>", lambda _e, c=col: self.update_formula_preview(c))
        self.formula_vars[col] = f_var

        preview = tk.Label(row, text="", font=("Consolas", 9), fg="gray")
        preview.grid(row=1, column=1, sticky="w")
        self.preview_labels[col] = preview

        row.grid_columnconfigure(1, weight=1)

    # ------------------------------------------------------------------ #
    # Formula preview + presets                                          #
    # ------------------------------------------------------------------ #
    def update_formula_preview(self, col: str) -> None:
        result = evaluate_formula(self.df, col, self.formula_vars[col].get().strip())
        self.preview_labels[col].config(text=result)

    def apply_preset(self):
        apply_preset(
            self.presets,
            self.preset_var.get(),
            self.column_vars,
            self.formula_vars,
            self.update_formula_preview,
        )

    # ------------------------------------------------------------------ #
    # Reference file load / export                                       #
    # ------------------------------------------------------------------ #
    def load_reference_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if path:
            self.ref_df = pd.read_excel(path)

    def export(self):
        export_to_excel(
            self.df,
            self.column_vars,
            self.formula_vars,
            self.ref_df,
            self.main_key_entry.get(),
            self.ref_key_entry.get(),
            self.ref_cols_entry.get(),
            self.file_path,
        )

    # ------------------------------------------------------------------ #
    # Config save / load                                                 #
    # ------------------------------------------------------------------ #
    def save_config(self):
        cfg = {
            "selected": [c for c, v in self.column_vars.items() if v.get()],
            "formulas": {c: v.get() for c, v in self.formula_vars.items()},
            "header_row": self.header_row.get(),
        }
        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")]
        )
        if not path:
            return
        cfg_save(cfg, path)
        self._refresh_recent_configs()
        messagebox.showinfo("Saved", f"Config saved:\n{path}")

    def load_config(self):
        path = filedialog.askopenfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")]
        )
        if not path:
            return
        try:
            cfg = cfg_load(path)
            self._apply_loaded_config(cfg)
            self._refresh_recent_configs()
            messagebox.showinfo("Loaded", f"Config loaded:\n{path}")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not load config:\n{exc}")

    # ------------------------------------------------------------------ #
    # Helpers                                                            #
    # ------------------------------------------------------------------ #
    def _apply_loaded_config(self, cfg: dict):
        """Apply a config dict to all UI elements."""
        self.header_row.set(cfg.get("header_row", 0))

        selected = set(cfg.get("selected", []))
        for col in self.column_vars:
            self.column_vars[col].set(col in selected)

        for col, formula in cfg.get("formulas", {}).items():
            if col in self.formula_vars:
                self.formula_vars[col].set(formula)
                self.update_formula_preview(col)

    def _refresh_recent_configs(self):
        """Refresh the MRU dropdown after save/load."""
        self.recent_configs = list_recent()
        if hasattr(self, "recent_combo"):
            self.recent_combo.configure(values=self.recent_configs)
