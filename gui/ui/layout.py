"""Slim orchestrator (auto‑generated but now tweaked).
Splits widget construction across helper components in ``gui.ui.components``.

Each component module *must* expose a ``build(app)`` function that packs its
widgets into the already‑configured root window.
"""

from gui.ui.theme import apply_theme
from gui.ui import utils as U

# ---------------------------------------------------------------------------
# Import the component modules. Ensure every name below matches a real file
#   gui/ui/components/<name>.py
# ---------------------------------------------------------------------------
from gui.ui.components import (
    header,                  # header.py
    main_file_section,       # main_file_section.py
    presets_section,         # presets_section.py
    column_controls_section, # column_controls_section.py
    reference_join_section,  # reference_join_section.py
    config_export_section,   # config_export_section.py
    status_bar,              # status_bar.py
)

# ---------------------------------------------------------------------------
# Tiny debug helper – prints which component failed to build and how many
# widgets hang directly off the root afterwards. Remove when you’re happy.
# ---------------------------------------------------------------------------

def _safe_build(tag: str, fn, app):
    """Run *fn(app)* and ensure its widget gets packed.

    * Logs progress and the direct‑child count on the root.
    * If the builder returns a Tk widget that is **not** yet managed
      (``winfo_manager() == ''``), we ``pack(fill='x')`` it so the UI doesn’t
      stay blank when a component forgets to call ``pack()``.
    """
    try:
        print(f" >> building {tag}")
        widget = fn(app)

        # auto‑pack if builder forgot
        if widget is not None and hasattr(widget, "winfo_manager") and not widget.winfo_manager():
            widget.pack(fill="x", pady=2)

        print(f"    -> root now has {len(app.root.winfo_children())} direct children")

    except Exception as exc:
        # Log the failure tag once, then propagate the traceback
        print(f" !! {tag} failed: {exc}")
        raise


# ---------------------------------------------------------------------------
# Public entry point – called from gui/app.py
# ---------------------------------------------------------------------------

def build_layout(app):
    """Configure the root window, then delegate to each section builder."""
    # Enhanced theme (if available)
    if getattr(U, "USE_ENHANCED_UI", False):
        app.theme = apply_theme(app.root)

    # Basic window properties
    app.root.title("Matrix Exporter")
    app.root.geometry("1100x700")
    app.root.minsize(900, 600)

    # Build UI sections in order
    _safe_build("header",                   header.build, app)
    _safe_build("main_file_section",        main_file_section.build, app)
    _safe_build("presets_section",          presets_section.build, app)
    _safe_build("column_controls_section",  column_controls_section.build, app)
    _safe_build("reference_join_section",   reference_join_section.build, app)
    _safe_build("config_export_section",    config_export_section.build, app)
    _safe_build("status_bar",               status_bar.build, app)

    return app
