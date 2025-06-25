from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
print("Allowed Origins:", origins) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "data/jobs.db"


@app.get("/")
# def get_jobs(limit: int = Query(20, le=100), offset: int = 0):
def get_jobs():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # cursor.execute(
    #     "SELECT * FROM jobs ORDER BY id ASC LIMIT ? OFFSET ?", (limit, offset)
    # )
    cursor.execute(
        "SELECT * FROM jobs ORDER BY id ASC",
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
