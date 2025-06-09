import tkinter as tk
from tkinter import ttk

# Global padding constants
PAD_X = 6
PAD_Y = 3
FIELD_PAD = 2

def build_layout(app):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10))
    style.configure("TCheckbutton", font=("Segoe UI", 10))

    # === Main Excel File Frame ===
    file_frame = ttk.LabelFrame(app.root, text="Main Excel File")
    file_frame.pack(padx=PAD_X, pady=(PAD_Y, 2), fill="x")

    ttk.Button(file_frame, text="Load Main Excel File", command=app.load_main_file).pack(side="left", padx=(PAD_X, FIELD_PAD), pady=PAD_Y)
    ttk.Label(file_frame, text="Header Row:").pack(side="left", padx=(FIELD_PAD, FIELD_PAD))
    ttk.Entry(file_frame, textvariable=app.header_row, width=5).pack(side="left", padx=(FIELD_PAD, PAD_X))

    app.sheet_dropdown = ttk.Combobox(file_frame, state="readonly")
    app.sheet_dropdown.pack(side="left", padx=FIELD_PAD)
    app.sheet_dropdown.bind("<<ComboboxSelected>>", app.load_sheet)

    # === Presets Frame ===
    preset_frame = ttk.LabelFrame(app.root, text="Column Presets")
    preset_frame.pack(padx=PAD_X, pady=(0, 2), fill="x")

    app.preset_var = tk.StringVar()
    app.preset_dropdown = ttk.Combobox(preset_frame, state="readonly", textvariable=app.preset_var)
    app.preset_dropdown.pack(side="left", padx=(PAD_X, FIELD_PAD))
    ttk.Button(preset_frame, text="Apply Preset", command=app.apply_preset).pack(side="left", padx=(FIELD_PAD, PAD_X))

    # === Column Controls (Check + Formula) ===
    columns_container = ttk.Frame(app.root)
    columns_container.pack(padx=PAD_X, pady=(0, PAD_Y), fill="both", expand=True)

    canvas = tk.Canvas(columns_container, borderwidth=0, highlightthickness=0, bg="#f8f8f8")
    canvas.grid_propagate(False)
    scrollbar = ttk.Scrollbar(columns_container, orient="vertical", command=canvas.yview)
    app.columns_frame = ttk.Frame(canvas, style="TFrame")
    app.column_rows = {}
    app.columns_frame.columnconfigure(1, weight=1)

    app.columns_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas_window = canvas.create_window((0, 0), window=app.columns_frame, anchor="nw", width=canvas.winfo_reqwidth())
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=0, pady=0)
    scrollbar.pack(side="right", fill="y")

    # Add consistent background color
    style.configure("TFrame", background="#f8f8f8")
    style.configure("TLabelFrame", background="#f8f8f8")
    style.configure("TCheckbutton", background="#f8f8f8")
    style.configure("TEntry", relief="flat")


    join_frame = ttk.LabelFrame(app.root, text="Reference File Join")
    join_frame.pack(padx=PAD_X, pady=(0, PAD_Y), fill="x")

    ttk.Button(join_frame, text="Load Reference File", command=app.load_reference_file).grid(row=0, column=0, padx=FIELD_PAD, pady=PAD_Y)

    ttk.Label(join_frame, text="Main Key:").grid(row=0, column=1, padx=FIELD_PAD)
    app.main_key_entry = ttk.Entry(join_frame)
    app.main_key_entry.grid(row=0, column=2, padx=FIELD_PAD)

    ttk.Label(join_frame, text="Ref Key:").grid(row=0, column=3, padx=FIELD_PAD)
    app.ref_key_entry = ttk.Entry(join_frame)
    app.ref_key_entry.grid(row=0, column=4, padx=FIELD_PAD)

    ttk.Label(join_frame, text="Ref Columns:").grid(row=0, column=5, padx=FIELD_PAD)
    app.ref_cols_entry = ttk.Entry(join_frame)
    app.ref_cols_entry.grid(row=0, column=6, padx=FIELD_PAD)

    # === Save/Load + Export Frame ===
    config_frame = ttk.LabelFrame(app.root, text="Save/Load + Export")
    config_frame.pack(padx=PAD_X, pady=(0, PAD_Y + 2), fill="x")

    ttk.Button(config_frame, text="Save Config", command=app.save_config).pack(side="left", padx=(PAD_X, FIELD_PAD))
    ttk.Button(config_frame, text="Load Config", command=app.load_config).pack(side="left", padx=FIELD_PAD)
    ttk.Button(config_frame, text="Export", command=app.export).pack(side="right", padx=(FIELD_PAD, PAD_X))
