import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config.config import WEBSITE_URL
import time
from src.scraper.scraping import scrape_jobs

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")    
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

def set_link(route: str = "/"):
    full_url = f"{WEBSITE_URL}{route}"
    return full_url

def scrape_emploitic(route: str):
    full_url = f"{WEBSITE_URL}{route}"
    print(f"Navigating to: {full_url}")
    driver.get(full_url)
    
    time.sleep(3)
    try:
        return(scrape_jobs(driver))

    except Exception as e:
        print(f"Error getting page content: {e}")
        return None
    

if __name__ == "__main__":
    route = "?search=developer"
    jobs = scrape_emploitic(route)
    if jobs:
        for job in jobs:
            print(job.show())
        exit()
    else:
        print("No jobs found.")
    driver.quit()
