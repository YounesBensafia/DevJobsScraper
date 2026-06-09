import argparse
import logging

import uvicorn

from src.scrapers import SCRAPERS
from src.utils.cleaner import main_cleaner

logger = logging.getLogger(__name__)


def run_api():
    logger.info("Starting API...")
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)


def run_scrapers():
    logger.info("Starting scrapers...")
    for name, scraper_class in SCRAPERS.items():
        try:
            logger.info("Running %s...", name)
            scraper = scraper_class()
            scraper.run()
        except Exception as e:
            logger.error("Error running %s scraper: %s", name, e)

    logger.info("Cleaning data...")
    main_cleaner()
    logger.info("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DevJobsScraper Entry Point")
    parser.add_argument(
        "mode",
        choices=["api", "scraper"],
        nargs="?",
        default="api",
        help="Mode to run: api (default) or scraper",
    )

    args = parser.parse_args()

    if args.mode == "api":
        run_api()
    elif args.mode == "scraper":
        run_scrapers()
