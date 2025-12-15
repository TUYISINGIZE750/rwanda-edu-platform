"""Inspect Excel file structure"""
import pandas as pd

file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"

try:
    df = pd.read_excel(file_path)
    print("=" * 80)
    print("EXCEL FILE STRUCTURE")
    print("=" * 80)
    print(f"\nTotal rows: {len(df)}")
    print(f"\nColumn names:\n{list(df.columns)}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nData types:\n{df.dtypes}")
except Exception as e:
    print(f"Error: {e}")
