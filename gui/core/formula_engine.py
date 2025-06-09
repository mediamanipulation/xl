import numpy as np
import pandas as pd
from asteval import Interpreter # Import asteval

# Create a persistent asteval interpreter instance
aeval = Interpreter()

def evaluate_formula(df, col, formula):
    """
    Evaluates a formula for preview using pandas.eval and asteval as a fallback.
    """
    if not formula:
        return ""
    if df is None or df.empty:
        return "Error: No data loaded"

    try:
        # First, try pandas.eval (faster and generally safe)
        value = df.eval(formula).dropna().iloc[0]
        return f"Preview (pandas): {value}"
    except Exception as pd_eval_err:
        # If pandas.eval fails, try asteval for the first row
        try:
            # Get the first row as a dictionary for context
            first_row_dict = df.iloc[0].to_dict()

            # Evaluate using asteval, passing the row dict as symbols
            # Use a fresh interpreter or clear symtable if necessary, but
            # for previews, reusing might be okay. Be mindful of side effects
            # if formulas modify the symtable (though not typical here).
            preview = aeval(formula, symtable=first_row_dict)

            # Check if preview is NaN or None (common results of failed ops)
            if pd.isna(preview):
                 return f"Preview (asteval): NaN/None"

            return f"Preview (asteval): {preview}"
        except Exception as asteval_err:
            # Both methods failed
            # Provide a more specific error message if helpful
            # print(f"Pandas eval error: {pd_eval_err}")
            # print(f"Asteval error: {asteval_err}")
            return "Error evaluating formula"