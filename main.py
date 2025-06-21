import time
from scraper.scraper import main_scraper
from scraper.cleaner import main_cleaner


def run_every(interval_seconds: int = 60):
    while True:
        print("🔄 Starting the job scraping process...")
        try:
            main_scraper()
            print("✅ Job scraping completed. Now cleaning the data...")
            main_cleaner()
            print("✅ Data cleaning completed. Process finished successfully.")
        except Exception as e:
            print(f"❌ Error during scheduled task: {e}")

        print(f"⏳ Waiting {interval_seconds} seconds...\n")
        time.sleep(interval_seconds)


def run():
    print("🔄 Starting the job scraping process...")
    try:
        main_scraper()
        print("✅ Job scraping completed. Now cleaning the data...")
        main_cleaner()
        print("✅ Data cleaning completed. Process finished successfully.")
    except Exception as e:
        print(f"❌ Error during scheduled task: {e}")


if __name__ == "__main__":
    run()
