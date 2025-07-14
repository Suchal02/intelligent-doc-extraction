import pdfplumber
import pandas as pd

def extract_all_tables(pdf_path: str):
    results = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table)
                    df.columns = df.iloc[0]  # promote first row to header
                    df = df[1:]  # drop header row from data
                    results.append(df)
    except Exception as e:
        print(f"⚠️ Table extraction error: {e}")

    return [df.to_dict(orient="records") for df in results]  # ✅ for Streamlit .write()
