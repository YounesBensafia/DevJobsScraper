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

    for _, element in enumerate(job_elements):
            job_title, job_company, job_link, job_location = extract_job_details(element)
            job_date_posted = extract_job_date_posted(element)
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

def extract_job_date_posted(element):
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
    return job_date_posted

def extract_job_details(element):
    job_title, job_company, job_link = extract_job_info(element) 
    try:
        job_location = retrieve_location_info(element)
        if not job_location:
            job_location = "Algeria"
    except Exception as loc_e:
        job_location = "Algeria"
    return job_title, job_company, job_link, job_location

def retrieve_location_info(element):
    location_container = element.find_element(By.XPATH, './/div[*[@data-testid="RoomRoundedIcon"]]')
    if location_container:
        location_text = location_container.get_attribute('textContent').strip()
        if location_text:
            job_location = location_text
        else:
            job_location = "Algeria"

def extract_job_info(element):
    job_title, job_company, job_link = retrieve_job_info(element)
    return job_title,job_company,job_link

def retrieve_job_info(element):
    job_title = element.find_element(By.CLASS_NAME, "mui-1oymh71").text
    job_company = element.find_element(By.CSS_SELECTOR, '[data-testid="jobs-item-company"]').text
    job_link = element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    return job_title,job_company,job_link
                    
