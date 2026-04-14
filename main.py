import argparse

import uvicorn

from src.scrapers import SCRAPERS
from src.utils.cleaner import main_cleaner


def run_api():
    print("🚀 Starting API...")
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)


def run_scrapers():
    print("🔍 Starting Scrapers...")
    for name, scraper_class in SCRAPERS.items():
        try:
            print(f"Running {name}...")
            scraper = scraper_class()
            scraper.run()
        except Exception as e:
            print(f"❌ Error running {name} scraper: {e}")

    print("🧹 Cleaning data...")
    main_cleaner()
    print("✅ Done.")


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
