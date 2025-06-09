import tkinter as tk
from tkinter import ttk, font
import os

class MatrixTheme:
    """Theme manager for the Matrix Ingestor application."""
    
    # Theme color constants
    COLORS = {
        "primary": "#1976D2",        # Primary blue
        "primary_dark": "#0D47A1",   # Darker blue
        "primary_light": "#42A5F5",  # Lighter blue
        "secondary": "#FF9800",      # Orange accent
        "secondary_dark": "#F57C00", # Darker orange
        "secondary_light": "#FFB74D",# Lighter orange
        "success": "#4CAF50",        # Green for success
        "error": "#F44336",          # Red for errors
        "warning": "#FFC107",        # Yellow for warnings
        "info": "#2196F3",           # Blue for info
        "bg_light": "#F5F5F5",       # Light grey background
        "bg_white": "#FFFFFF",       # White background
        "bg_alt": "#F9F9F9",         # Alternate row background
        "text": "#212121",           # Main text color
        "text_secondary": "#757575", # Secondary text color
        "border": "#E0E0E0",         # Border color
        "disabled": "#BDBDBD",       # Disabled element color
        "highlight": "#E3F2FD",      # Highlight background
        "tooltip": "#FFFFD0"         # Tooltip background
    }
    
    # Font configurations
    FONTS = {
        "header": ("Segoe UI", 16, "bold"),
        "subheader": ("Segoe UI", 12, "bold"),
        "body": ("Segoe UI", 10),
        "body_bold": ("Segoe UI", 10, "bold"),
        "small": ("Segoe UI", 9),
        "tiny": ("Segoe UI", 8),
        "monospace": ("Consolas", 9)
    }
    
    def __init__(self, root):
        """Initialize the theme manager.
        
        Args:
            root: The root tkinter window
        """
        self.root = root
        self.style = ttk.Style()
        
        # Configure the theme
        self.configure_theme()
    
    def configure_theme(self):
        """Configure the application theme."""
        # Choose the best available theme as base
        self._set_base_theme()
        
        # Configure colors and styles
        self._configure_colors()
        self._configure_styles()
        
        # Set window icon if available
        self._set_window_icon()
    
    def _set_base_theme(self):
        """Set the base ttk theme."""
        # Prefer 'clam' theme as it's the most customizable cross-platform
        available_themes = self.style.theme_names()
        preferred_themes = ["clam", "vista", "xpnative", "winnative", "default"]
        
        # Use the first available preferred theme
        for theme in preferred_themes:
            if theme in available_themes:
                self.style.theme_use(theme)
                break
        
        # Configure the root window
        self.root.configure(background=self.COLORS["bg_light"])
    
    def _configure_colors(self):
        """Configure the color scheme."""
        # Set root background
        self.root.configure(background=self.COLORS["bg_light"])
        
        # Other widget colors are set in _configure_styles
    
    def _configure_styles(self):
        """Configure ttk widget styles."""
        # Frame styles
        self.style.configure("TFrame", background=self.COLORS["bg_light"])
        self.style.configure("Card.TFrame", background=self.COLORS["bg_white"], 
                            relief="raised", borderwidth=1)
        
        # Label styles
        self.style.configure("TLabel", background=self.COLORS["bg_light"], 
                            foreground=self.COLORS["text"], font=self.FONTS["body"])
        self.style.configure("Header.TLabel", background=self.COLORS["bg_light"], 
                            foreground=self.COLORS["primary"], font=self.FONTS["header"])
        self.style.configure("Subheader.TLabel", background=self.COLORS["bg_light"], 
                            foreground=self.COLORS["primary_dark"], font=self.FONTS["subheader"])
        self.style.configure("Small.TLabel", background=self.COLORS["bg_light"], 
                            foreground=self.COLORS["text_secondary"], font=self.FONTS["small"])
        
        # Button styles
        self.style.configure("TButton", font=self.FONTS["body"], padding=5)
        self.style.map("TButton", 
                      foreground=[("active", self.COLORS["primary_dark"])],
                      background=[("active", self.COLORS["highlight"])])
        
        # Primary button style
        self.style.configure("Primary.TButton", font=self.FONTS["body_bold"], padding=5)
        self.style.map("Primary.TButton", 
                      foreground=[("active", self.COLORS["primary_dark"])],
                      background=[("active", self.COLORS["highlight"])])
        
        # Success button style
        self.style.configure("Success.TButton", font=self.FONTS["body_bold"], padding=6)
        self.style.map("Success.TButton", 
                      foreground=[("active", self.COLORS["success"])],
                      background=[("active", self.COLORS["highlight"])])
        
        # Entry styles
        self.style.configure("TEntry", padding=3)
        
        # Valid and invalid entry styles for formula validation
        self.style.configure("Valid.TEntry", padding=3, fieldbackground="#E8F5E9")  # Light green
        self.style.configure("Invalid.TEntry", padding=3, fieldbackground="#FFEBEE")  # Light red
        
        # Combobox styles
        self.style.configure("TCombobox", padding=3)
        
        # Checkbutton styles
        self.style.configure("TCheckbutton", background=self.COLORS["bg_light"], 
                            font=self.FONTS["body"])
        
        # Labelframe styles
        self.style.configure("TLabelframe", background=self.COLORS["bg_light"])
        self.style.configure("TLabelframe.Label", background=self.COLORS["bg_light"], 
                            foreground=self.COLORS["primary_dark"], font=self.FONTS["body_bold"])
        
        # Separator styles
        self.style.configure("TSeparator", background=self.COLORS["border"])
        
        # Progressbar styles
        self.style.configure("TProgressbar", thickness=8)
        
        # Scrollbar styles
        self.style.configure("TScrollbar", arrowsize=13)
        
        # Notebook styles
        self.style.configure("TNotebook", background=self.COLORS["bg_light"])
        self.style.configure("TNotebook.Tab", font=self.FONTS["body"], padding=[10, 3])
        
        # Alternative row styles for listboxes, treeviews, etc.
        self.style.configure("Even.TFrame", background=self.COLORS["bg_white"])
        self.style.configure("Odd.TFrame", background=self.COLORS["bg_alt"])
    
    def _set_window_icon(self):
        """Set the application window icon if available."""
        # Check for common icon locations
        icon_paths = [
            os.path.join("assets", "icon.ico"),
            os.path.join("assets", "icon.png"),
            os.path.join("gui", "assets", "icon.ico"),
            os.path.join("gui", "assets", "icon.png")
        ]
        
        # Try to set the icon
        for path in icon_paths:
            if os.path.exists(path):
                try:
                    self.root.iconbitmap(path) if path.endswith('.ico') else None
                    # For PNG, you would need PIL/Pillow to convert to a Tkinter photo image
                    break
                except Exception:
                    pass
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget.
        
        Args:
            widget: The widget to attach the tooltip to
            text: The tooltip text
        """
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
                background=self.COLORS["tooltip"],
                relief="solid",
                borderwidth=1,
                font=self.FONTS["small"],
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
    
    def apply_alternating_row_style(self, parent, widgets):
        """Apply alternating row styles to a list of widgets.
        
        Args:
            parent: The parent widget
            widgets: A list of widgets to style
        """
        # Create alternating row styles
        for i, widget in enumerate(widgets):
            style_name = "Even.TFrame" if i % 2 == 0 else "Odd.TFrame"
            widget.configure(style=style_name)


def apply_theme(root):
    """Apply the Matrix theme to the application.
    
    Args:
        root: The root tkinter window
        
    Returns:
        The theme manager instance
    """
    theme = MatrixTheme(root)
    return theme