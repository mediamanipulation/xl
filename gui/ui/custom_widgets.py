import tkinter as tk
from tkinter import ttk
import re

class FormulaEntry(ttk.Frame):
    """Enhanced entry widget with syntax highlighting for formula editing."""
    
    def __init__(self, master=None, textvariable=None, **kwargs):
        # Extract the textvariable before passing kwargs to parent
        self.textvariable = textvariable
        
        # Remove textvariable from kwargs if present
        if 'textvariable' in kwargs:
            del kwargs['textvariable']
            
        # Initialize the frame
        super().__init__(master, **kwargs)
        
        # Create the entry widget
        self.entry = ttk.Entry(self, textvariable=self.textvariable)
        self.entry.pack(fill="x", expand=True)
        
        # Syntax highlighting colors
        self.colors = {
            'functions': '#0D47A1',  # Dark blue for functions
            'operators': '#D32F2F',  # Red for operators
            'brackets': '#2E7D32',   # Green for brackets
            'column_refs': '#7B1FA2', # Purple for column references
            'numbers': '#FF6F00'     # Orange for numbers
        }
        
        # Bind key events for real-time feedback
        self.entry.bind("<KeyRelease>", self.highlight_syntax)
        
    def highlight_syntax(self, event=None):
        """Apply simple syntax highlighting to the formula."""
        # This is a placeholder for actual syntax highlighting
        # In a production app, you might use a Text widget with tags instead
        # But for now, we'll just change the background color based on formula validity
        formula = self.entry.get()
        
        if formula:
            # Very basic validation
            valid = self.validate_formula(formula)
            if valid:
                self.entry.configure(style="Valid.TEntry")
            else:
                self.entry.configure(style="Invalid.TEntry")
        else:
            # Reset to default
            self.entry.configure(style="TEntry")
    
    def validate_formula(self, formula):
        """Basic validation of formula syntax."""
        # Check for balanced brackets
        if formula.count('[') != formula.count(']'):
            return False
        
        # Check for balanced parentheses
        if formula.count('(') != formula.count(')'):
            return False
        
        return True
    
    def get(self):
        """Get the formula text."""
        return self.entry.get()
    
    def set(self, value):
        """Set the formula text."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        self.highlight_syntax()


class TooltipButton(ttk.Button):
    """Button with a tooltip that appears on hover."""
    
    def __init__(self, master=None, tooltip_text="", **kwargs):
        super().__init__(master, **kwargs)
        self.tooltip_text = tooltip_text
        
        # Create the tooltip window (hidden initially)
        self.tooltip = None
        
        # Bind mouse events
        self.bind("<Enter>", self.show_tooltip)
        self.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Show the tooltip."""
        if self.tooltip_text:
            x, y, _, _ = self.bbox("insert")
            x += self.winfo_rootx() + 25
            y += self.winfo_rooty() + 25
            
            # Create the tooltip window
            self.tooltip = tk.Toplevel(self)
            self.tooltip.wm_overrideredirect(True)  # Remove window decorations
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            # Create the label with the tooltip text
            label = ttk.Label(
                self.tooltip, 
                text=self.tooltip_text,
                justify=tk.LEFT,
                background="#FFFFD0",
                relief="solid",
                borderwidth=1,
                font=("Segoe UI", 9),
                padding=(5, 2)
            )
            label.pack()
    
    def hide_tooltip(self, event=None):
        """Hide the tooltip."""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class ProgressDialog(tk.Toplevel):
    """Modal dialog showing progress with an optional cancel button."""
    
    def __init__(self, parent, title="Progress", message="Processing...", 
                 cancellable=False, on_cancel=None):
        super().__init__(parent)
        
        self.title(title)
        self.transient(parent)  # Make dialog a child of parent
        self.grab_set()  # Make dialog modal
        
        # Center the dialog on parent
        window_width = 350
        window_height = 150
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width - window_width) // 2
        y = parent_y + (parent_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.resizable(False, False)
        self.configure(bg="#F5F5F5")
        
        # Create widgets
        self.message_var = tk.StringVar(value=message)
        
        # Message label
        ttk.Label(
            self, 
            textvariable=self.message_var,
            font=("Segoe UI", 11),
            background="#F5F5F5"
        ).pack(pady=(20, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self, 
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.progress.pack(pady=10, padx=25)
        
        # Cancel button (optional)
        if cancellable and on_cancel:
            self.on_cancel = on_cancel
            ttk.Button(
                self,
                text="Cancel",
                command=self.cancel
            ).pack(pady=(10, 20))
        
        # Prevent closing with the window manager
        self.protocol("WM_DELETE_WINDOW", self.do_nothing)
        
        # Ensure dialog appears on top
        self.focus_set()
        
        # Start with 0 progress
        self.set_progress(0)
    
    def set_progress(self, value):
        """Set the progress bar value (0-100)."""
        self.progress["value"] = value
        self.update_idletasks()
    
    def set_message(self, message):
        """Update the message text."""
        self.message_var.set(message)
        self.update_idletasks()
    
    def cancel(self):
        """Cancel the operation."""
        if hasattr(self, 'on_cancel'):
            self.on_cancel()
        self.destroy()
    
    def do_nothing(self):
        """Prevent closing with the window manager."""
        pass
    
    def finish(self):
        """Complete the progress and close."""
        self.set_progress(100)
        self.update_idletasks()
        self.after(500, self.destroy)


class FileDragDrop(ttk.LabelFrame):
    """Frame that supports dragging and dropping files."""
    
    def __init__(self, master=None, on_drop=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_drop = on_drop
        
        # Create a label for instructions
        self.label = ttk.Label(
            self,
            text="Drag and drop Excel files here",
            font=("Segoe UI", 11),
            foreground="#757575",
            background="#FFFFFF",
            anchor="center"
        )
        self.label.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create a border around the label
        self.label.configure(borderwidth=2, relief="groove")
        
        # Bind events for drag and drop
        self.label.bind("<Enter>", self.on_enter)
        self.label.bind("<Leave>", self.on_leave)
        
        # These are the actual drag-and-drop event bindings
        # Note: Tkinter doesn't natively support drag and drop
        # This is a placeholder showing how you would bind the events
        # In a real implementation, you might need platform-specific code
        # or third-party libraries like tkinterdnd2
        #self.label.bind("<Drop>", self.on_file_drop)
        
    def on_enter(self, event):
        """Mouse entered the drop zone."""
        self.label.configure(foreground="#1976D2", text="Release to drop files")
    
    def on_leave(self, event):
        """Mouse left the drop zone."""
        self.label.configure(foreground="#757575", text="Drag and drop Excel files here")
    
    def on_file_drop(self, event):
        """File was dropped in the drop zone."""
        if self.on_drop:
            # In a real implementation, you would get the file path from the event
            # For now, we'll just call the callback with None
            self.on_drop(None)
        
        # Reset appearance
        self.on_leave(event)