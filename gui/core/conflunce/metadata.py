# gui/core/confluence/metadata.py

import pandas as pd

def generate_summary(file_path: str) -> str:
    """
    Generates an HTML summary of the Excel file's metadata (columns, row count).
    """
    try:
        df = pd.read_excel(file_path)
        cols = df.columns.tolist()
        summary = f"<p><b>Upload Summary:</b></p>"
        summary += f"<p><b>File:</b> {os.path.basename(file_path)}</p>"
        summary += f"<p><b>Rows:</b> {len(df)}</p>"
        summary += f"<p><b>Columns:</b> {', '.join(cols)}</p>"
        return summary
    except Exception as e:
        return f"<p><b>Upload Summary:</b> Failed to read file - {e}</p>"