import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import ALLOWED_ORIGINS
from src.core.database import get_db_connection, init_db
from src.scrapers import SCRAPERS
from src.utils.cleaner import main_cleaner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_scraper_service():
    while True:
        logger.info("--- Starting Scraping Cycle ---")
        for name, scraper_class in SCRAPERS.items():
            try:
                logger.info(f"Running {name} scraper...")
                scraper = scraper_class()
                scraper.run()
            except Exception as e:
                logger.error(f"Error running {name} scraper: {e}")

        logger.info("Cycle completed. Cleaning data...")
        try:
            main_cleaner()
        except Exception as e:
            logger.error(f"Error during data cleaning: {e}")

        logger.info("Cycle finished. Next run in 60 seconds.")
        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(run_scraper_service())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Scraper background service stopped.")


app = FastAPI(title="DevJobsScraper API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_jobs():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
