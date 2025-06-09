import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from datetime import datetime

# Color palette for a consistent look
PRIMARY_COLOR = "#1976D2"  # Material blue
SECONDARY_COLOR = "#42A5F5"  # Lighter blue
ACCENT_COLOR = "#FF9800"  # Orange accent
BG_COLOR = "#F5F5F5"  # Light grey background
TEXT_COLOR = "#212121"  # Dark text
PREVIEW_COLOR = "#607D8B"  # Blue grey for preview text
HEADER_COLOR = "#0D47A1"  # Dark blue for headers
SUCCESS_COLOR = "#4CAF50"  # Green for success indicators

def create_tooltip(widget, text):
    """Create a tooltip for a widget."""
    tooltip = None
    
    def enter(event):
        nonlocal tooltip
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        
        # Create a toplevel window
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        
        # Create the label
        label = ttk.Label(
            tooltip,
            text=text,
            justify=tk.LEFT,
            background="#FFFFD0",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9),
            padding=(5, 2)
        )
        label.pack()
    
    def leave(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None
    
    # Bind events to the widget
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)


def show_info_message(parent, title, message):
    """Show an information message with enhanced styling."""
    messagebox.showinfo(title, message)


def show_error_message(parent, title, message):
    """Show an error message with enhanced styling."""
    messagebox.showerror(title, message)


def show_warning_message(parent, title, message):
    """Show a warning message with enhanced styling."""
    messagebox.showwarning(title, message)


def show_confirmation_dialog(parent, title, message):
    """Show a confirmation dialog and return True if confirmed."""
    return messagebox.askyesno(title, message)


def create_status_bar(root, initial_message="Ready"):
    """Create a status bar at the bottom of the root window."""
    status_frame = ttk.Frame(root)
    status_frame.pack(side="bottom", fill="x", padx=5, pady=2)
    
    # Create a variable to hold the status text
    status_var = tk.StringVar(value=initial_message)
    
    # Create the status label
    status_label = ttk.Label(
        status_frame,
        textvariable=status_var,
        anchor="w",
        font=("Segoe UI", 9)
    )
    status_label.pack(side="left")
    
    # Return both the frame and the variable so they can be accessed later
    return status_frame, status_var


def flash_success_message(status_var, message, duration=3000):
    """Flash a success message in the status bar temporarily."""
    # Save the original message
    original_message = status_var.get()
    
    # Set the success message
    status_var.set(f"✓ {message}")
    
    # Schedule restoring the original message
    root = status_var.master.winfo_toplevel()
    root.after(duration, lambda: status_var.set(original_message))


def flash_error_message(status_var, message, duration=3000):
    """Flash an error message in the status bar temporarily."""
    # Save the original message
    original_message = status_var.get()
    
    # Set the error message
    status_var.set(f"❌ {message}")
    
    # Schedule restoring the original message
    root = status_var.master.winfo_toplevel()
    root.after(duration, lambda: status_var.set(original_message))


def apply_modern_theme(root):
    """Apply a modern theme to the application."""
    style = ttk.Style()
    
    # Try to use a modern-looking theme if available
    available_themes = style.theme_names()
    
    # Preferred themes in order
    preferred_themes = ["clam", "vista", "xpnative", "winnative", "default"]
    
    # Find the first available preferred theme
    for theme in preferred_themes:
        if theme in available_themes:
            style.theme_use(theme)
            break
    
    # Configure common styles
    style.configure("TFrame", background=BG_COLOR)
    style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10), padding=5)
    style.configure("TEntry", padding=3)
    style.configure("TCheckbutton", background=BG_COLOR, font=("Segoe UI", 10))
    
    # Special button styles
    style.configure("Primary.TButton",
                   font=("Segoe UI", 10, "bold"),
                   padding=5)
    
    style.configure("Success.TButton",
                   font=("Segoe UI", 11, "bold"),
                   padding=6)
    
    # Configure the root window
    root.configure(background=BG_COLOR)
    

def create_section_header(parent, text, icon=None):
    """Create a section header with an optional icon."""
    frame = ttk.Frame(parent)
    frame.pack(fill="x", padx=5, pady=(10, 5))
    
    # Add icon if provided
    if icon:
        # In a real implementation, you would load and display an icon here
        pass
    
    # Add header text
    label = ttk.Label(
        frame,
        text=text,
        font=("Segoe UI", 12, "bold"),
        foreground=HEADER_COLOR,
        background=BG_COLOR
    )
    label.pack(side="left", padx=5)
    
    # Add a separator line that fills the rest of the width
    separator = ttk.Separator(frame, orient="horizontal")
    separator.pack(side="left", fill="x", expand=True, padx=10)
    
    return frame


def center_window(window, width=None, height=None):
    """Center a window on the screen with optional size."""
    # Set size if provided
    if width and height:
        window.geometry(f"{width}x{height}")
    
    # Get window size
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    
    # Calculate position
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # Set position
    window.geometry(f"+{x}+{y}")


def create_alternating_row(parent, index):
    """Create a frame with alternating background colors based on row index."""
    bg_color = "#F9F9F9" if index % 2 == 0 else "white"
    frame = ttk.Frame(parent, style="TFrame")
    
    # Since ttk doesn't support setting background directly, we use a custom style
    style = ttk.Style()
    style_name = f"Row{index}.TFrame"
    style.configure(style_name, background=bg_color)
    frame.configure(style=style_name)
    
    return frame


def create_help_button(parent, help_text):
    """Create a help button that shows a tooltip with provided text."""
    button = ttk.Button(
        parent,
        text="?",
        width=2,
        command=lambda: show_info_message(parent, "Help", help_text)
    )
    
    # Add a tooltip to the button
    create_tooltip(button, "Click for help")
    
    return button


def save_app_settings(settings, filename="app_settings.json"):
    """Save application settings to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False


def load_app_settings(filename="app_settings.json"):
    """Load application settings from a JSON file."""
    if not os.path.exists(filename):
        return {}
    
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading settings: {e}")
        return {}


def create_backup_file(filepath, suffix="_backup"):
    """Create a backup of a file with timestamp."""
    if not os.path.exists(filepath):
        return None
    
    # Get the file name and extension
    file_dir, file_name = os.path.split(filepath)
    name, ext = os.path.splitext(file_name)
    
    # Create a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create the backup file name
    backup_name = f"{name}{suffix}_{timestamp}{ext}"
    backup_path = os.path.join(file_dir, backup_name)
    
    # Copy the file
    try:
        import shutil
        shutil.copy2(filepath, backup_path)
        return backup_path
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None