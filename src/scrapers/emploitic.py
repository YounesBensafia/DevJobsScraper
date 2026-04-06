import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from src.core.config import WEBSITE_URL
from src.core.models import Job
from src.scrapers.base import BaseScraper


class EmploiticScraper(BaseScraper):
    def __init__(self):
        self.base_url = WEBSITE_URL
        self.route = "?search=developer"

    def _get_driver(self):
        from webdriver_manager.chrome import ChromeDriverManager

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--remote-allow-origins=*")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def scrape(self) -> List[Job]:
        driver = self._get_driver()
        full_url = f"{self.base_url}{self.route}"
        print(f"Navigating to: {full_url}")
        driver.get(full_url)
        time.sleep(3)

        job_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="jobs-item"]')
        jobs = []

        print(f"Found {len(job_elements)} job elements.")
        for element in job_elements:
            try:
                try:
                    title = element.find_element(By.TAG_NAME, "h2").text
                except Exception:
                    title = "N/A"

                try:
                    company = element.find_element(
                        By.CSS_SELECTOR, '[data-testid="jobs-item-company"]'
                    ).text
                except Exception:
                    company = "N/A"

                try:
                    link = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                except Exception:
                    continue

                try:
                    location_container = element.find_element(
                        By.XPATH, './/div[*[@data-testid="RoomRoundedIcon"]]'
                    )
                    location = location_container.get_attribute("textContent").strip() or "Algeria"
                except Exception:
                    location = "Algeria"

                try:
                    time_container = element.find_element(
                        By.XPATH, './/div[*[@data-testid="TimelapseRoundedIcon"]]'
                    )
                    posted_time = time_container.get_attribute("textContent").strip() or "N/A"
                except Exception:
                    posted_time = "N/A"

                jobs.append(
                    Job(
                        title=title,
                        company=company,
                        link=link,
                        locations=location,
                        time=posted_time,
                        tags="emploitic",
                    )
                )
            except Exception as e:
                print(f"Error extracting Emploitic job detaill: {e}")

        driver.quit()
        return jobs


if __name__ == "__main__":
    scraper = EmploiticScraper()
    scraper.run()
