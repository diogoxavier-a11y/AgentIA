import pandas as pd

def read_excel_vats(sheet_url, vat_col='VAT number'):
    df = pd.read_excel(sheet_url)
    vats = df[vat_col].dropna().astype(str).str.strip().tolist()
    return vats, df
