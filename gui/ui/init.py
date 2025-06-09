# This file makes the gui/ui directory a Python package
# Import common UI components for easier access

try:
    from gui.ui.utils import (
        create_tooltip, show_info_message, show_error_message,
        flash_success_message, flash_error_message,
        apply_modern_theme, center_window
    )
    
    from gui.ui.theme import apply_theme
    
    from gui.ui.custom_widgets import (
        FormulaEntry, TooltipButton, ProgressDialog, FileDragDrop
    )
    
    # Indicate that enhanced UI is available
    ENHANCED_UI_AVAILABLE = True
    
except ImportError:
    # Fallback if some modules are missing
    ENHANCED_UI_AVAILABLE = False
    
    def dummy_function(*args, **kwargs):
        """Dummy function for fallback."""
        pass
    
    # Create dummy functions to prevent errors
    create_tooltip = dummy_function
    show_info_message = dummy_function
    show_error_message = dummy_function
    flash_success_message = dummy_function
    flash_error_message = dummy_function
    apply_modern_theme = dummy_function
    center_window = dummy_function