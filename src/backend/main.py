from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import asyncio
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from scraper.scraper_remoteOK import main_scraper
from src.scraper.cleaner import main_cleaner
from pathlib import Path


load_dotenv()

DB_PATH = "src/data/jobs.db"
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

async def run_scraper_loop(interval_seconds: int = 60):
    while True:
        print("Starting the job scraping process...")
        try:
            main_scraper()
            print("Job scraping completed. Now cleaning the data...")
            main_cleaner()
            print("Data cleaning completed. Process finished successfully.")
        except Exception as e:
            print(f"Error during scheduled task: {e}")

        print(f"Waiting {interval_seconds} seconds...\n")
        await asyncio.sleep(interval_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(run_scraper_loop(60))
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Background task cancelled.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_jobs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
