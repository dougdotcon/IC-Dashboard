import pandas as pd
import sqlite3
import os
import sys

# Print current working directory
print(f"Current working directory: {os.getcwd()}")

# Path to the Excel file
excel_file = 'base.xlsx'

# Path to the SQLite database
sqlite_file = 'base.sqlite'

# Check if Excel file exists
if not os.path.exists(excel_file):
    print(f"Error: Excel file '{excel_file}' not found")
    exit(1)

print(f"Reading Excel file: {excel_file}")

# Read the Excel file
try:
    # First, let's see what sheets are in the Excel file
    xls = pd.ExcelFile(excel_file)
    print(f"Excel sheets: {xls.sheet_names}")

    # Read all sheets into a dictionary of dataframes
    dfs = {}
    for sheet_name in xls.sheet_names:
        print(f"Reading sheet: {sheet_name}")
        try:
            # Try to read with default settings
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
        except Exception as sheet_error:
            print(f"Error reading sheet '{sheet_name}': {str(sheet_error)}")
            print("Trying with different parameters...")
            try:
                # Try with explicit engine
                df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')
            except Exception as e:
                print(f"Failed to read sheet '{sheet_name}': {str(e)}")
                continue

        # Check if dataframe is empty
        if df.empty:
            print(f"Sheet '{sheet_name}' is empty, skipping")
            continue

        dfs[sheet_name] = df
        print(f"Sheet '{sheet_name}' has {len(df)} rows and {len(df.columns)} columns")
        print(f"Columns: {df.columns.tolist()}")
        print(f"First few rows:")
        print(df.head(2))  # Just show 2 rows to keep output manageable
        print("\n")

    if not dfs:
        print("No valid data found in the Excel file")
        exit(1)

    # Create a SQLite database
    print(f"Creating SQLite database: {sqlite_file}")
    conn = sqlite3.connect(sqlite_file)

    # Write each dataframe to a table in the SQLite database
    for sheet_name, df in dfs.items():
        # Clean the sheet name to use as a table name (remove spaces, special chars)
        table_name = ''.join(c if c.isalnum() else '_' for c in sheet_name)
        print(f"Writing sheet '{sheet_name}' to table '{table_name}'")

        # Handle potential issues with column names
        df.columns = [str(col).replace(' ', '_').replace('.', '_') for col in df.columns]

        # Write to SQLite
        df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()
    print("Conversion completed successfully!")

except Exception as e:
    print(f"Error: {str(e)}")
    print(f"Exception type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    exit(1)
