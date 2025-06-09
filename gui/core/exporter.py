import pandas as pd
from tkinter import filedialog, messagebox # Keep these for UI interaction
from asteval import Interpreter

# Create a persistent asteval interpreter instance
aeval = Interpreter()

def evaluate_with_asteval(row, formula):
    """Helper function to evaluate a formula for a row using asteval."""
    try:
        return aeval(formula, symtable=row.to_dict())
    except Exception as e:
        return f"#AERR! {e}"

def export_to_excel(df, column_vars, formula_vars, ref_df, main_key, ref_key, ref_cols_input, file_path):
    """
    Exports data to Excel, evaluating formulas using pandas.eval and asteval as fallback.
    """
    selected_cols = [col for col, var in column_vars.items() if var.get()]
    if not selected_cols:
        messagebox.showwarning("No columns selected", "Select at least one column.")
        return

    if df is None:
         messagebox.showerror("Error", "No main data loaded to export.")
         return

    result = pd.DataFrame(index=df.index)

    for col in selected_cols:
        # --- Get the formula string ---
        # Get the StringVar object if it exists for this column
        formula_var_object = formula_vars.get(col)

        # Retrieve the string value from the StringVar, default to "" if object is missing
        formula = ""
        if formula_var_object:
            formula = formula_var_object.get().strip()
        # Removed the incorrect reference to tk.StringVar here

        # --- Process based on formula presence ---
        if not formula:
            # No formula, just copy the original column if it exists
            if col in df.columns:
                result[col] = df[col]
            else:
                messagebox.showwarning("Missing Column", f"Selected column '{col}' not found in the original data and has no formula.")
                result[col] = None
            continue

        # --- Formula Evaluation (remains the same) ---
        try:
            result[col] = df.eval(formula)
        except Exception as pd_eval_err:
            try:
                result[col] = df.apply(lambda row: evaluate_with_asteval(row, formula), axis=1)
            except Exception as apply_err:
                messagebox.showerror("Apply Error", f"Failed to apply formula for column '{col}': {apply_err}")
                result[col] = f"#APPLY_ERR! {apply_err}"

    # --- Reference File Join (remains the same) ---
    if ref_df is not None:
        main_key_stripped = main_key.strip()
        ref_key_stripped = ref_key.strip()
        ref_cols = [c.strip() for c in ref_cols_input.split(',') if c.strip()]

        if main_key_stripped and ref_key_stripped and ref_cols:
            if main_key_stripped not in result.columns:
                 messagebox.showerror("Join Error", f"Main join key '{main_key_stripped}' not found in the processed data.")
                 return
            if ref_key_stripped not in ref_df.columns:
                 messagebox.showerror("Join Error", f"Reference join key '{ref_key_stripped}' not found in the reference file.")
                 return

            missing_ref_cols = [c for c in ref_cols if c not in ref_df.columns]
            if missing_ref_cols:
                 messagebox.showwarning("Join Warning", f"Reference columns not found in reference file and will be skipped: {', '.join(missing_ref_cols)}")
                 ref_cols = [c for c in ref_cols if c in ref_df.columns]

            if not ref_cols:
                 messagebox.showwarning("Join Warning", "No valid reference columns specified or found for joining.")
            else:
                try:
                    ref_slice = ref_df[[ref_key_stripped] + ref_cols].copy()
                    ref_slice = ref_slice.loc[:,~ref_slice.columns.duplicated()]
                    result = result.merge(
                        ref_slice,
                        left_on=main_key_stripped,
                        right_on=ref_key_stripped,
                        how="left"
                    )
                except Exception as e:
                    messagebox.showerror("Join Error", f"Error during merge operation: {e}")
                    return

    # --- Save Output (remains the same) ---
    out_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
    if out_path:
        try:
            result.to_excel(out_path, index=False)
            messagebox.showinfo("Done", f"Data successfully exported to:\n{out_path}")
        except Exception as e:
             messagebox.showerror("Export Error", f"Failed to save the Excel file:\n{e}")