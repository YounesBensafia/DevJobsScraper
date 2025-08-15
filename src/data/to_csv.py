import sqlite3
import pandas as pd

conn = sqlite3.connect('./src/data/jobs.db')

df = pd.read_sql_query("SELECT * FROM jobs", conn)

df.to_csv("./src/data/jobs.csv", index=False)

conn.close()

print("Exported jobs to jobs.csv ✅")
