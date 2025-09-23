import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.scraper.scarper_emploitic import scrape_emploitic


if __name__ == "__main__":
    jobs = scrape_emploitic(route="?search=developer")
    print(jobs[0].show())
    print("Scraping completed and data saved to database.")