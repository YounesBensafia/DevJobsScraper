import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scraper.scraper_remoteOK import main_scraper


if __name__ == "__main__":
    main_scraper()
    print("Scraping completed and data saved to database.")