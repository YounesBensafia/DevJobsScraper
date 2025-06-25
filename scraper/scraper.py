from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sqlite3
import pandas as pd


def save_to_db(jobs: list):
    df = pd.DataFrame(jobs)
    conn = sqlite3.connect("data/jobs.db")
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    conn.close()


def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://remoteok.com/remote-dev-jobs"
    driver.get(url)

    time.sleep(5)
    return driver



def scraper(driver):
    job_elements = driver.find_elements(By.CSS_SELECTOR, "tr.job")
    jobs = []

    for job_element in job_elements:
        try:
            title_element = job_element.find_element(
                By.CSS_SELECTOR, "h2[itemprop='title']"
            )
            title = title_element.text.strip()
        except:
            title = job_element.text.strip()

        try:
            time_element = job_element.find_element(By.CSS_SELECTOR, "td.time")
            posted = time_element.text.strip()
        except:
            posted = "N/A"

        try:
            company_element = job_element.find_element(
                By.CSS_SELECTOR, "h3[itemprop='name']"
            )
            company = company_element.text.strip()
        except:
            company = "N/A"

        try:
            tags = []

            tags_divs = job_element.find_elements(By.CLASS_NAME, "tags")

            for div in tags_divs:
                h3s = div.find_elements(By.TAG_NAME, "h3")
                tags.extend([h3.text.strip() for h3 in h3s if h3.text.strip()])
        except:
            print("Error extracting tags for job:", title)
            continue
        try:
            salary = []
            location = []

            divs = job_element.find_elements(By.CSS_SELECTOR, "div.location")

            for div in divs:
                content = div.get_attribute("textContent").strip()
                if "💰" in content:
                    salary.append(content)
                else:
                    location.append(content)

        except:
            print("Error extracting locations for job:", title)
            salary = ["Not mentioned"]
            location = ["Not mentioned"]
        try:
            link_element = job_element.find_element(By.CSS_SELECTOR, ".preventLink")
            job_link = link_element.get_attribute("href")
            link = job_link.strip()

        except:
            print("Error extracting job link for job:", title)
            link = "Not mentioned"
            continue

        try:
            logo_element = job_element.find_element(By.CSS_SELECTOR, ".logo")

            logo = logo_element.get_attribute("data-src")

            if logo and logo.startswith("/"):
                logo = "https://remoteok.com" + logo

            if not logo:
                logo = "Not mentioned"

        except:
            print("Error extracting job logo for job:", title)
            logo = "Not mentioned"

        jobs.append(
            {
                "title": title,
                "time": posted,
                "company": company,
                "tags": ", ".join(tags),
                "locations": ", ".join(location) if location else "Not mentioned",
                "salary": ", ".join(salary) if salary else "Not mentioned",
            "link": link if link else "Not mentioned",
            "logo": logo,
        }
        )
    
    driver.quit()
    return jobs


def main_scraper():
    driver_instance = driver()
    jobs = scraper(driver_instance)
    save_to_db(jobs)
