import asyncio
import logging
import math
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
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
                logger.info("Running %s scraper...", name)
                scraper = scraper_class()
                scraper.run()
            except Exception as e:
                logger.error("Scraper %s failed: %s", name, e)

        logger.info("Cycle completed. Cleaning data...")
        try:
            main_cleaner()
        except Exception as e:
            logger.error("Error during data cleaning: %s", e)

        logger.info("Cycle finished. Next run in 30 minutes.")
        await asyncio.sleep(1800)


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


@app.get("/jobs")
def get_jobs(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total = cursor.fetchone()[0]

        offset = (page - 1) * limit
        cursor.execute(
            "SELECT * FROM jobs ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset)
        )
        rows = cursor.fetchall()

        return {
            "data": [dict(row) for row in rows],
            "total": total,
            "page": page,
            "pages": math.ceil(total / limit) if total > 0 else 0,
        }
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
