"""Detailed Excel file inspection"""
import pandas as pd

file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"

try:
    # Read with header=None to see raw structure
    df = pd.read_excel(file_path, header=None)
    print("=" * 80)
    print("RAW EXCEL STRUCTURE")
    print("=" * 80)
    print(f"\nTotal rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    
    print("\nFirst 10 rows (raw):")
    for i in range(min(10, len(df))):
        print(f"Row {i}: {list(df.iloc[i])}")
    
    # Try to identify header row
    print("\n" + "=" * 80)
    print("LOOKING FOR HEADER ROW")
    print("=" * 80)
    
    for i in range(min(5, len(df))):
        row_values = [str(val) for val in df.iloc[i] if pd.notna(val)]
        print(f"Row {i}: {row_values}")
        
        # Check if this looks like a header
        if any(keyword in ' '.join(row_values).lower() for keyword in ['school', 'district', 'province', 'trade', 'gender']):
            print(f"  ^ This might be the header row!")
    
    # Try reading with different header rows
    print("\n" + "=" * 80)
    print("TRYING DIFFERENT HEADER POSITIONS")
    print("=" * 80)
    
    for header_row in [0, 1]:
        try:
            df_test = pd.read_excel(file_path, header=header_row)
            print(f"\nWith header={header_row}:")
            print(f"Columns: {list(df_test.columns)}")
            print(f"First data row: {list(df_test.iloc[0])}")
        except Exception as e:
            print(f"Error with header={header_row}: {e}")

except Exception as e:
    print(f"Error: {e}")