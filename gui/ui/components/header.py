"""Header bar – shows app title + version."""

import tkinter as tk
from tkinter import ttk
from gui.ui.utils import PRIMARY_COLOR, BG_COLOR, PAD_X, PAD_Y


def build(app):
    """Create the header bar and return the outer frame."""
    frame = ttk.Frame(app.root, padding=(PAD_X * 2, PAD_Y * 2))
    frame.pack(fill="x")

    ttk.Label(
        frame,
        text="Matrix Exporter",
        font=("Segoe UI", 16, "bold"),
        foreground=PRIMARY_COLOR,
        background=BG_COLOR,
    ).pack(side="left")

    ttk.Label(
        frame,
        text="v1.0",
        font=("Segoe UI", 10),
        foreground="#03A9F4",
        background=BG_COLOR,
    ).pack(side="left", padx=(6, 0), pady=(4, 0))

    ttk.Separator(app.root, orient="horizontal").pack(fill="x", padx=PAD_X, pady=(0, PAD_Y))
    return frame
