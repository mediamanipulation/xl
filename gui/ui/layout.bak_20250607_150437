import tkinter as tk
from tkinter import ttk, messagebox   # ← added messagebox
import os
from gui.core.config_manager import load_config


# Import the theme and utils if they're available
try:
    from gui.ui.theme import apply_theme
    from gui.ui.utils import (create_tooltip, create_section_header, 
                             create_help_button, flash_success_message)
    from gui.ui.custom_widgets import FormulaEntry, TooltipButton, ProgressDialog
    USE_ENHANCED_UI = True
except ImportError:
    # Fallback to basic UI if the enhanced modules aren't available
    USE_ENHANCED_UI = False
    
print(f"DEBUG: USE_ENHANCED_UI flag is set to: {USE_ENHANCED_UI}")
# Global constants for styling and spacing
PAD_X = 8
PAD_Y = 5
FIELD_PAD = 3

# Default color palette (used if theme module is not available)
PRIMARY_COLOR = "#1976D2"  # Material blue
SECONDARY_COLOR = "#03A9F4"  # Lighter blue
ACCENT_COLOR = "#FF9800"  # Orange accent
BG_COLOR = "#F5F5F5"  # Light grey background
TEXT_COLOR = "#212121"  # Dark text
PREVIEW_COLOR = "#607D8B"  # Blue grey for preview text

def build_layout(app):
    """
    Build the application layout with a modern look and feel.
    This function is compatible with the existing app structure.
    
    Args:
        app: The ExcelTransformerApp instance
        
    Returns:
        The updated app instance
    """
    # Apply the enhanced theme if available
    if USE_ENHANCED_UI:
        theme = apply_theme(app.root)
        app.theme = theme
    else:
        # Basic styling
        style = ttk.Style()
        style.theme_use("clam")  # Use clam theme as base (cross-platform)
        
        # Configure basic styles
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=5)
        style.configure("TEntry", padding=3)
        style.configure("TCheckbutton", background=BG_COLOR, font=("Segoe UI", 10))
        
        # Configure the root window
        app.root.configure(background=BG_COLOR)
        
        # Create a theme-like object for consistency
        app.theme = type('Theme', (), {
            'COLORS': {
                'primary': PRIMARY_COLOR,
                'secondary': SECONDARY_COLOR,
                'accent': ACCENT_COLOR,
                'bg_light': BG_COLOR,
                'text': TEXT_COLOR,
                'preview': PREVIEW_COLOR
            },
            'create_tooltip': lambda w, t: None  # No-op function
        })
        
    
    
    # Configure window properties
    app.root.title("Matrix Exporter")
    app.root.geometry("1100x700")  # Set default size
    app.root.minsize(900, 600)  # Set minimum size
    
    # Create the main layout
    create_header(app)
    create_main_file_section(app)
    create_presets_section(app)
    create_column_controls_section(app)
    create_reference_join_section(app)
    create_config_export_section(app)
    create_status_bar(app)
    
    return app


def create_header(app):
    """Create the app header with title."""
    header_frame = ttk.Frame(app.root)
    header_frame.pack(fill="x", padx=PAD_X*2, pady=PAD_Y*2)
    
    # App title
    if USE_ENHANCED_UI:
        ttk.Label(header_frame, text="Matrix Exporter", style="Header.TLabel").pack(side="left")
    else:
        title_label = ttk.Label(
            header_frame, 
            text="Matrix Exporter", 
            font=("Segoe UI", 16, "bold"),
            foreground=PRIMARY_COLOR,
            background=BG_COLOR
        )
        title_label.pack(side="left")
    
    # Version info
    version_label = ttk.Label(
        header_frame,
        text="v1.0",
        foreground=SECONDARY_COLOR,
        background=BG_COLOR,
        font=("Segoe UI", 10)
    )
    version_label.pack(side="left", padx=(5, 0), pady=(5, 0))
    
    # Add a separator below header
    separator = ttk.Separator(app.root, orient="horizontal")
    separator.pack(fill="x", padx=PAD_X, pady=(0, PAD_Y))

def create_main_file_section(app):
    """Create the main file selection section."""
    file_frame = ttk.LabelFrame(app.root, text="Source File")
    file_frame.pack(padx=PAD_X, pady=(0, PAD_Y), fill="x")
    
    # Add container with padding
    file_container = ttk.Frame(file_frame)
    file_container.pack(padx=PAD_X, pady=PAD_Y, fill="x")
    
    # First row - load button and header row
    row1 = ttk.Frame(file_container)
    row1.pack(fill="x", pady=(0, PAD_Y))
    
    load_button = ttk.Button(
        row1,
        text="Load Excel File",
        command=app.load_main_file
    )
    load_button.pack(side="left", padx=(0, PAD_X))
    
    # Apply tooltip if available
    if USE_ENHANCED_UI:
        app.theme.create_tooltip(load_button, "Load a main Excel file to process")
    
    ttk.Label(row1, text="Header Row:").pack(side="left", padx=FIELD_PAD)
    header_entry = ttk.Entry(
        row1,
        textvariable=app.header_row,
        width=5
    )
    header_entry.pack(side="left", padx=FIELD_PAD)
    
    ttk.Label(row1, text="Sheet:").pack(side="left", padx=PAD_X)
    
    # Create the sheet dropdown
    app.sheet_dropdown = ttk.Combobox(row1, state="readonly", width=20)
    app.sheet_dropdown.pack(side="left", padx=FIELD_PAD)
    app.sheet_dropdown.bind("<<ComboboxSelected>>", app.load_sheet)
    
    # Display current file info if available
    if hasattr(app, 'file_path') and app.file_path:
        file_info = ttk.Label(
            file_container,
            text=f"Current file: {app.file_path}",
            foreground=SECONDARY_COLOR,
            background=BG_COLOR
        )
        file_info.pack(anchor="w", pady=(0, PAD_Y))

def create_presets_section(app):
    """Create the presets section."""
    preset_frame = ttk.LabelFrame(app.root, text="Column Presets")
    preset_frame.pack(padx=PAD_X, pady=(0, PAD_Y), fill="x")
    
    # Add container with padding
    preset_container = ttk.Frame(preset_frame)
    preset_container.pack(padx=PAD_X, pady=PAD_Y, fill="x")
    
    # Create a horizontal layout for preset controls
    preset_controls = ttk.Frame(preset_container)
    preset_controls.pack(fill="x")
    
    # Create the preset variable if it doesn't exist
    if not hasattr(app, 'preset_var'):
        app.preset_var = tk.StringVar()
    
    # Create the preset dropdown
    app.preset_dropdown = ttk.Combobox(
        preset_controls,
        state="readonly",
        textvariable=app.preset_var,
        width=30
    )
    app.preset_dropdown.pack(side="left", padx=(0, PAD_X), fill="x", expand=True)
    
    # Load presets
    if hasattr(app, 'presets') and app.presets:
        app.preset_dropdown['values'] = list(app.presets.keys())
    
    # Apply preset button
    apply_btn = ttk.Button(
        preset_controls,
        text="Apply Preset",
        command=app.apply_preset
    )
    apply_btn.pack(side="left")
    
    # Add help button if enhanced UI is available
    if USE_ENHANCED_UI:
        help_text = "Presets allow you to quickly apply predefined column selections and formulas."
        help_btn = create_help_button(preset_controls, help_text)
        help_btn.pack(side="left", padx=PAD_X)

def create_column_controls_section(app):
    """Create the column controls section (scrollable)."""
    # Create a frame to hold the column controls
    columns_frame = ttk.LabelFrame(app.root, text="Column Controls")
    columns_frame.pack(padx=PAD_X, pady=(0, PAD_Y), fill="both", expand=True)
    
    # Add container with padding
    columns_container = ttk.Frame(columns_frame)
    columns_container.pack(padx=PAD_X, pady=PAD_Y, fill="both", expand=True)
    
    # Create column headers
    headers = ttk.Frame(columns_container)
    headers.pack(fill="x", pady=(0, PAD_Y))
    
    ttk.Label(
        headers,
        text="Column",
        font=("Segoe UI", 10, "bold"),
        width=20,
        background=BG_COLOR
    ).pack(side="left", padx=(5, 15))
    
    ttk.Label(
        headers,
        text="Include",
        font=("Segoe UI", 10, "bold"),
        width=10,
        background=BG_COLOR
    ).pack(side="left", padx=(0, 15))
    
    ttk.Label(
        headers,
        text="Formula/Transformation",
        font=("Segoe UI", 10, "bold"),
        background=BG_COLOR
    ).pack(side="left", fill="x", expand=True)
    
    # Create a canvas with scrollbar for the columns
    canvas_frame = ttk.Frame(columns_container)
    canvas_frame.pack(fill="both", expand=True)
    
    # Create canvas and scrollbar
    canvas = tk.Canvas(
        canvas_frame,
        borderwidth=0,
        highlightthickness=0,
        background="white"
    )
    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    
    # Create the frame that will contain the column rows
    app.columns_frame = ttk.Frame(canvas, style="TFrame")
    
    # Configure the canvas to work with the scrollbar
    app.columns_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # Create the window in the canvas
    canvas_window = canvas.create_window((0, 0), window=app.columns_frame, anchor="nw", width=canvas.winfo_reqwidth())
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
        # Enable mousewheel scrolling on Windows and Linux
    def _on_mousewheel(event):
        if event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
    # Windows
    canvas.bind_all("<MouseWheel>", _on_mousewheel)  #
    canvas.bind_all("<Shift-MouseWheel>", _on_mousewheel)  # macOS horizontal scroll
    canvas.bind_all("<Button-4>", _on_mousewheel)  # Linux up
    canvas.bind_all("<Button-5>", _on_mousewheel)  # Linux down
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down
    
    # Adjust the canvas window when the canvas is resized
    def on_canvas_resize(event):
        canvas.itemconfig(canvas_window, width=event.width)
    
    canvas.bind("<Configure>", on_canvas_resize)
    
    # Override the add_column_row method to use the new styling
    original_add_column_row = app.add_column_row
    
    def styled_add_column_row(col):
        """Enhanced version of add_column_row with better styling"""
        row_frame = tk.Frame(app.columns_frame, bg="white")
        row_frame.pack(anchor="w", pady=3, padx=5, fill="x")
        
        # Use a different background for alternating rows
        if len(app.columns_frame.winfo_children()) % 2 == 0:
            row_frame.configure(bg="#F9F9F9")
        
        var = tk.BooleanVar()
        chk = tk.Checkbutton(
            row_frame, 
            text=col, 
            variable=var,
            font=("Segoe UI", 10),
            bg=row_frame.cget("bg"),
            anchor="w",
            width=18
        )
        chk.grid(row=0, column=0, sticky="w", padx=(5, 15))
        app.column_vars[col] = var
        
        formula_var = tk.StringVar()
        
        # Use FormulaEntry if available, otherwise regular Entry
        if USE_ENHANCED_UI and 'FormulaEntry' in globals():
            entry = FormulaEntry(
                row_frame,
                textvariable=formula_var,
                width=40
            )
        else:
            entry = tk.Entry(
                row_frame, 
                textvariable=formula_var, 
                width=40,
                font=("Segoe UI", 10)
            )
            
        entry.grid(row=0, column=1, padx=4, sticky="ew")
        entry.bind("<KeyRelease>", lambda e, c=col: app.update_formula_preview(c))
        app.formula_vars[col] = formula_var
        
        # Configure the grid to make the entry expand
        row_frame.grid_columnconfigure(1, weight=1)
        
        preview_label = tk.Label(
            row_frame, 
            text="", 
            font=("Consolas", 9), 
            fg=PREVIEW_COLOR,
            bg=row_frame.cget("bg"),
            anchor="w"
        )
        preview_label.grid(row=1, column=1, sticky="w", padx=4)
        app.preview_labels[col] = preview_label
    
    # Replace the original method with our enhanced version only if we have FormulaEntry
    if USE_ENHANCED_UI:
        app.add_column_row = styled_add_column_row

def create_reference_join_section(app):
    """Create the reference file join section."""
    join_frame = ttk.LabelFrame(app.root, text="Reference File Join")
    join_frame.pack(padx=PAD_X, pady=(0, PAD_Y), fill="x")
    
    # Add container with padding
    join_container = ttk.Frame(join_frame)
    join_container.pack(padx=PAD_X, pady=PAD_Y, fill="x")
    
    # Load reference file button
    load_ref_button = ttk.Button(
        join_container,
        text="Load Reference File",
        command=app.load_reference_file
    )
    load_ref_button.pack(anchor="w", pady=(0, PAD_Y))
    
    # Create a two-column grid for the join parameters
    params_frame = ttk.Frame(join_container)
    params_frame.pack(fill="x", pady=(0, PAD_Y))
    
    # Configure the grid columns
    params_frame.columnconfigure(1, weight=1)
    params_frame.columnconfigure(3, weight=1)
    
    # First row: Main Key and Ref Key
    ttk.Label(
        params_frame, 
        text="Main Key:"
    ).grid(row=0, column=0, sticky="w", padx=(0, FIELD_PAD), pady=FIELD_PAD)
    
    app.main_key_entry = ttk.Entry(params_frame)
    app.main_key_entry.grid(row=0, column=1, sticky="ew", padx=FIELD_PAD, pady=FIELD_PAD)
    
    ttk.Label(
        params_frame, 
        text="Ref Key:"
    ).grid(row=0, column=2, sticky="w", padx=FIELD_PAD, pady=FIELD_PAD)
    
    app.ref_key_entry = ttk.Entry(params_frame)
    app.ref_key_entry.grid(row=0, column=3, sticky="ew", padx=FIELD_PAD, pady=FIELD_PAD)
    
    # Second row: Reference Columns
    ttk.Label(
        params_frame, 
        text="Ref Columns:"
    ).grid(row=1, column=0, sticky="w", padx=(0, FIELD_PAD), pady=FIELD_PAD)
    
    app.ref_cols_entry = ttk.Entry(params_frame)
    app.ref_cols_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=FIELD_PAD, pady=FIELD_PAD)
    
    # Add helper text
    helper_label = ttk.Label(
        join_container,
        text="Enter comma-separated column names for reference data",
        font=("Segoe UI", 9),
        foreground=PREVIEW_COLOR,
        background=BG_COLOR
    )
    helper_label.pack(anchor="w")
    
    # Add tooltips if available
    if USE_ENHANCED_UI:
        app.theme.create_tooltip(load_ref_button, "Load a reference Excel file to join with the main data")
        app.theme.create_tooltip(app.main_key_entry, "Column name in the main file to join on")
        app.theme.create_tooltip(app.ref_key_entry, "Column name in the reference file to join on")
        app.theme.create_tooltip(app.ref_cols_entry, "Comma-separated list of columns to include from the reference file")

def create_config_export_section(app):
    """Create the configuration and export section."""
    config_frame = ttk.LabelFrame(app.root, text="Configuration and Export")
    config_frame.pack(padx=PAD_X, pady=(0, PAD_Y), fill="x")
    
    # Add container with padding
    config_container = ttk.Frame(config_frame)
    config_container.pack(padx=PAD_X, pady=PAD_Y, fill="x")
    
    # Button row
    buttons_frame = ttk.Frame(config_container)
    buttons_frame.pack(fill="x", pady=(0, PAD_Y))
    
    # Save and load config buttons
    save_config_btn = ttk.Button(
        buttons_frame,
        text="Save Configuration",
        command=app.save_config
    )
    save_config_btn.pack(side="left", padx=(0, FIELD_PAD))
    
    load_config_btn = ttk.Button(
        buttons_frame,
        text="Load Configuration",
        command=app.load_config
    )
    load_config_btn.pack(side="left", padx=FIELD_PAD)
    
    # Use TooltipButton if available, otherwise regular Button
    if USE_ENHANCED_UI and 'TooltipButton' in globals():
        export_button = TooltipButton(
            config_container,
            text="EXPORT DATA",
            command=app.export,
            tooltip_text="Process and export data to a new Excel file"
        )
    else:
        # Export button (special styling)
        if USE_ENHANCED_UI:
            export_button = ttk.Button(
                config_container,
                text="EXPORT DATA",
                command=app.export,
                style="Success.TButton"
            )
        else:
            export_button = ttk.Button(
                config_container,
                text="EXPORT DATA",
                command=app.export
            )
    
    export_button.pack(fill="x", pady=(0, FIELD_PAD))
    
    # Apply tooltip if available# Recent-configs dropdown
    ttk.Label(config_container, text="Recent:").pack(side="left", padx=(0, FIELD_PAD))

    app.recent_var = tk.StringVar()
    app.recent_combo = ttk.Combobox(
        config_container,
        textvariable=app.recent_var,
        state="readonly",
        width=45,
        values=app.recent_configs,
    )
    app.recent_combo.pack(side="left", padx=(0, PAD_X))


    def load_from_recent(*_):
        sel = app.recent_var.get()
        if sel:
            try:
                cfg = load_config(sel)
                app._apply_loaded_config(cfg)
            except Exception as e:
                messagebox.showerror("Error", e)
    


    app.recent_combo.bind("<<ComboboxSelected>>", load_from_recent)

    
    # Add helper text
    helper_label = ttk.Label(
        config_container,
        text="Export will create a new Excel file with processed columns and applied transformations",
        font=("Segoe UI", 9),
        foreground=PREVIEW_COLOR,
        background=BG_COLOR
    )
    helper_label.pack(anchor="w")
    
    # Add tooltips if available
    if USE_ENHANCED_UI:
        app.theme.create_tooltip(save_config_btn, "Save current configuration to a file")
        app.theme.create_tooltip(load_config_btn, "Load a previously saved configuration")

def create_status_bar(app):
    """Create a status bar at the bottom of the window."""
    status_frame = ttk.Frame(app.root, style="TFrame")
    status_frame.pack(side="bottom", fill="x", padx=PAD_X, pady=PAD_Y)
    
    # Create status variable if it doesn't exist
    if not hasattr(app, 'status_var'):
        app.status_var = tk.StringVar(value="Ready")
    
    # Create status label
    status_label = ttk.Label(
        status_frame,
        textvariable=app.status_var,
        anchor="w",
        font=("Segoe UI", 9)
    )
    status_label.pack(side="left")
    
    # Add a method to update status
    def update_status(message, success=None):
        app.status_var.set(message)
        app.root.update_idletasks()
        
        # Flash success message if enhanced UI is available
        if USE_ENHANCED_UI and 'flash_success_message' in globals() and success is not None:
            if success:
                flash_success_message(app.status_var, message)
    
    # Add the method to the app
    app.update_status = update_status
    
    # Override export method to show progress dialog if available
    if USE_ENHANCED_UI and 'ProgressDialog' in globals():
        original_export = app.export
        
        def enhanced_export():
            # Show progress dialog
            progress = ProgressDialog(
                app.root,
                title="Exporting Data",
                message="Processing data..."
            )
            
            # Simulate progress
            def update_progress():
                steps = [
                    "Reading source data...",
                    "Applying transformations...",
                    "Processing formulas...",
                    "Joining with reference data...",
                    "Writing output file...",
                    "Finalizing..."
                ]
                
                for i, step in enumerate(steps):
                    progress.set_message(step)
                    progress.set_progress((i / len(steps)) * 100)
                    app.root.after(500)  # Simulate processing time
                
                # Call the original export function
                original_export()
                
                # Complete the progress
                progress.set_progress(100)
                progress.set_message("Export complete!")
                app.root.after(1000, progress.destroy)
            
            # Start progress updates
            app.root.after(100, update_progress)
        
        # Only replace the export method if we're confident it will work
        # This is a bit risky, so we'll check if the original has expected parameters
        if hasattr(app, 'column_vars') and hasattr(app, 'formula_vars'):
            app.export = enhanced_export