from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config.config import WEBSITE_URL
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scraper.job import Job

def scrape_jobs(driver) -> list[Job]:
    job_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="jobs-item"]')
    jobs = []

    for i, element in enumerate(job_elements):
            job_title = element.find_element(By.CLASS_NAME, "mui-1oymh71").text
            job_company = element.find_element(By.CSS_SELECTOR, '[data-testid="jobs-item-company"]').text
            job_link = element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') 
            try:
                location_container = element.find_element(By.XPATH, './/div[*[@data-testid="RoomRoundedIcon"]]')
                if location_container:
                    location_text = location_container.get_attribute('textContent').strip()
                    if location_text:
                        job_location = location_text
                    else:
                        job_location = "Algeria"
            except Exception as loc_e:
                job_location = "Algeria"

            try:
                date_posted_container = element.find_element(By.XPATH, './/div[*[@data-testid="TimelapseRoundedIcon"]]')
                if date_posted_container:
                    date_posted_text = date_posted_container.get_attribute('textContent').strip()
                    if date_posted_text:
                        job_date_posted = date_posted_text
                    else:
                        job_date_posted = "N/A"
                else:
                    job_date_posted = "N/A"
            except Exception as loc_e:
                job_date_posted = "N/A"
            job =Job(
                title=job_title,
                company=job_company,
                date_posted=job_date_posted,
                        location=job_location,
                        link=job_link,
                        etat="emploitic"
                    )
            jobs.append(job)
    return jobs
                    
