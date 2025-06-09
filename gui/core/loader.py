import pandas as pd

def load_excel_sheet(file_path, sheet_name, header_row):
    return pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
