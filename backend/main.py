from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_PATH = "data/jobs.db"

@app.get("/jobs")
def get_all_jobs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
