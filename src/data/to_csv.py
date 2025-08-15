import sqlite3
import pandas as pd

conn = sqlite3.connect('./data/jobs.db')

df = pd.read_sql_query("SELECT * FROM jobs", conn)

df.to_csv("./data/jobs.csv", index=False)

conn.close()

print("Exported jobs to jobs.csv ✅")
