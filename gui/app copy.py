# gui/app.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import json
import os

class ExcelTransformerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Transformer Pro")

        self.df = None
        self.ref_df = None
        self.file_path = None
        self.config_path = "config.json"
        self.presets_path = "presets.json"
        self.header_row = tk.IntVar(value=0)

        self.column_vars = {}
        self.formula_vars = {}
        self.preview_labels = {}

        # === Layout: Main Excel File Controls ===
        file_frame = ttk.LabelFrame(root, text="Main Excel File")
        file_frame.pack(padx=10, pady=5, fill="x")

        tk.Button(file_frame, text="Load Main Excel File", command=self.load_main_file).pack(side="left", padx=5, pady=5)
        tk.Label(file_frame, text="Header Row:").pack(side="left")
        tk.Entry(file_frame, textvariable=self.header_row, width=5).pack(side="left", padx=5)

        self.sheet_dropdown = ttk.Combobox(file_frame, state="readonly")
        self.sheet_dropdown.pack(side="left", padx=5)
        self.sheet_dropdown.bind("<<ComboboxSelected>>", self.load_sheet)

        # === Layout: Preset Selector ===
        preset_frame = ttk.LabelFrame(root, text="Column Presets")
        preset_frame.pack(padx=10, pady=5, fill="x")

        self.preset_var = tk.StringVar()
        self.preset_dropdown = ttk.Combobox(preset_frame, state="readonly", textvariable=self.preset_var)
        self.preset_dropdown.pack(side="left", padx=5)
        tk.Button(preset_frame, text="Apply Preset", command=self.apply_preset).pack(side="left", padx=5)
        self.load_presets()

        # === Layout: Column and Formula Editor ===
        self.columns_frame = ttk.LabelFrame(root, text="Column Selection and Formulas")
        self.columns_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # === Layout: Reference Join ===
        join_frame = ttk.LabelFrame(root, text="Reference File Join")
        join_frame.pack(padx=10, pady=5, fill="x")

        tk.Button(join_frame, text="Load Reference File", command=self.load_reference_file).grid(row=0, column=0, padx=5, pady=5)

        tk.Label(join_frame, text="Main Key:").grid(row=0, column=1)
        self.main_key_entry = tk.Entry(join_frame)
        self.main_key_entry.grid(row=0, column=2)

        tk.Label(join_frame, text="Ref Key:").grid(row=0, column=3)
        self.ref_key_entry = tk.Entry(join_frame)
        self.ref_key_entry.grid(row=0, column=4)

        tk.Label(join_frame, text="Ref Columns:").grid(row=0, column=5)
        self.ref_cols_entry = tk.Entry(join_frame)
        self.ref_cols_entry.grid(row=0, column=6)

        # === Layout: Config + Export ===
        config_frame = ttk.LabelFrame(root, text="Save/Load + Export")
        config_frame.pack(padx=10, pady=10, fill="x")

        tk.Button(config_frame, text="Save Config", command=self.save_config).pack(side="left", padx=5)
        tk.Button(config_frame, text="Load Config", command=self.load_config).pack(side="left", padx=5)
        tk.Button(config_frame, text="Export", command=self.export).pack(side="right", padx=5)

    def load_main_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not path:
            return
        self.file_path = path
        xls = pd.ExcelFile(self.file_path)
        self.sheet_dropdown["values"] = xls.sheet_names
        self.sheet_dropdown.current(0)
        self.load_sheet()

    def load_sheet(self, *args):
        sheet = self.sheet_dropdown.get()
        if not sheet:
            return
        df = pd.read_excel(self.file_path, sheet_name=sheet, header=self.header_row.get())
        self.df = df
        self.column_vars.clear()
        self.formula_vars.clear()
        self.preview_labels.clear()
        for widget in self.columns_frame.winfo_children():
            widget.destroy()

        for i, col in enumerate(df.columns):
            row_frame = tk.Frame(self.columns_frame)
            row_frame.pack(anchor="w", pady=2, padx=5)

            var = tk.BooleanVar()
            chk = tk.Checkbutton(row_frame, text=col, variable=var)
            chk.grid(row=0, column=0, sticky="w")
            self.column_vars[col] = var

            formula_var = tk.StringVar()
            entry = tk.Entry(row_frame, textvariable=formula_var, width=35)
            entry.grid(row=0, column=1, padx=5)
            entry.bind("<KeyRelease>", lambda e, c=col: self.update_formula_preview(c))
            self.formula_vars[col] = formula_var

            preview_label = tk.Label(row_frame, text="", font=("Courier", 9), fg="gray")
            preview_label.grid(row=1, column=1, sticky="w")
            self.preview_labels[col] = preview_label

    def update_formula_preview(self, col):
        if self.df is None or col not in self.formula_vars:
            return
        formula = self.formula_vars[col].get().strip()
        if not formula:
            self.preview_labels[col].config(text="")
            return
        try:
            preview = self.df.eval(formula).dropna().iloc[0]
            self.preview_labels[col].config(text=f"Preview: {preview}")
        except Exception as e:
            self.preview_labels[col].config(text=f"Error")

    def load_presets(self):
        if os.path.exists(self.presets_path):
            with open(self.presets_path, "r") as f:
                self.presets = json.load(f)
            self.preset_dropdown["values"] = list(self.presets.keys())

    def apply_preset(self):
        preset_name = self.preset_var.get()
        if preset_name not in self.presets:
            return
        preset = self.presets[preset_name]
        columns = preset.get("columns", [])
        formulas = preset.get("formulas", {})

        for col, var in self.column_vars.items():
            var.set(col in columns)
        for col, val in formulas.items():
            if col in self.formula_vars:
                self.formula_vars[col].set(val)
                self.update_formula_preview(col)

    def load_reference_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if path:
            self.ref_df = pd.read_excel(path)

    def export(self):
        selected_cols = [col for col, var in self.column_vars.items() if var.get()]
        if not selected_cols:
            messagebox.showwarning("No columns selected", "Select at least one column.")
            return
        result = pd.DataFrame()
        for col in selected_cols:
            formula = self.formula_vars[col].get().strip()
            if formula:
                try:
                    result[col] = self.df.eval(formula)
                except Exception as e:
                    result[col] = f"#ERR {e}"
            else:
                result[col] = self.df[col]

        if self.ref_df is not None:
            main_key = self.main_key_entry.get().strip()
            ref_key = self.ref_key_entry.get().strip()
            ref_cols = [c.strip() for c in self.ref_cols_entry.get().split(',') if c.strip()]
            if main_key and ref_key and ref_cols:
                ref_slice = self.ref_df[[ref_key] + ref_cols]
                result = result.merge(ref_slice, left_on=main_key, right_on=ref_key, how="left")

        out_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if out_path:
            result.to_excel(out_path, index=False)
            messagebox.showinfo("Done", f"Saved to {out_path}")

    def save_config(self):
        config = {
            "selected": [col for col, var in self.column_vars.items() if var.get()],
            "formulas": {col: var.get() for col, var in self.formula_vars.items()},
            "header_row": self.header_row.get()
        }
        with open(self.config_path, "w") as f:
            json.dump(config, f)
        messagebox.showinfo("Saved", f"Config saved to {self.config_path}")

    def load_config(self):
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
            self.header_row.set(config.get("header_row", 0))
            for col in config.get("selected", []):
                if col in self.column_vars:
                    self.column_vars[col].set(True)
            for col, formula in config.get("formulas", {}).items():
                if col in self.formula_vars:
                    self.formula_vars[col].set(formula)
                    self.update_formula_preview(col)
            messagebox.showinfo("Loaded", "Config loaded.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load config: {e}")
