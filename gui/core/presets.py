import json
import os

def load_presets(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def apply_preset(presets, name, column_vars, formula_vars, preview_callback):
    if name not in presets:
        return
    preset = presets[name]
    columns = preset.get("columns", [])
    formulas = preset.get("formulas", {})

    for col, var in column_vars.items():
        var.set(col in columns)
    for col, val in formulas.items():
        if col in formula_vars:
            formula_vars[col].set(val)
            preview_callback(col)
