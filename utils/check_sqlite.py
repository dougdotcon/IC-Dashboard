import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('base.sqlite')

# Get the list of tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(f"- {table[0]}")

# For each table, get the schema and a sample of data
for table in tables:
    table_name = table[0]
    print(f"\nTable: {table_name}")
    
    # Get schema
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    print("Schema:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Get sample data
    df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", conn)
    print("\nSample data:")
    print(df)

# Close the connection
conn.close()
