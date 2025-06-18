import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('data/jobs.db')

# Get list of tables in the database
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    table_name = table[0]
    print(f"\n--- Table: {table_name} ---")
    
    # Read table data into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    
    # Display table data
    print(df)
    
    # Print column details
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    print("\nColumn details:")
    for col in columns_info:
        print(f"  {col[1]} ({col[2]})")

# Close the connection
conn.close()