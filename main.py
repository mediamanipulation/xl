import os
import sys
import tkinter as tk

# Ensure the 'gui' package is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from gui.app import ExcelTransformerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelTransformerApp(root)
    root.mainloop()
