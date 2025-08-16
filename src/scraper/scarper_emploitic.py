import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config.config import WEBSITE_URL
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scraper.job import Job

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
    jobs = []
    try:
        job_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="jobs-item"]')
        for element in job_elements:
            job_info = element.text
            print(job_info)

        
        return jobs
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
