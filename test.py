import sqlite3
import pandas as pd

conn = sqlite3.connect("data/jobs.db")

cursor = conn.cursor()
cursor.execute("SELECT * FROM jobs")
rows = cursor.fetchall()

# Get column names
column_names = [description[0] for description in cursor.description]
print("Column names:", column_names)

conn.close()
