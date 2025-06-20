from scraper.scraper import main_scraper
from scraper.cleaner import main_cleaner

if __name__ == "__main__":
    print("Starting the job scraping process...")
    main_scraper()
    print("Job scraping completed. Now cleaning the data...")
    main_cleaner()
    print("Data cleaning completed. Process finished successfully.")

