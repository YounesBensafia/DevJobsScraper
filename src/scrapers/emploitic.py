import logging
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from src.core.config import EMPLOITIC_URL
from src.core.models import Job
from src.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class EmploiticScraper(BaseScraper):
    def __init__(self):
        self.base_url = EMPLOITIC_URL
        self.route = "?search=developer"
        self._driver_path = ChromeDriverManager().install()

    def _get_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--remote-allow-origins=*")

        service = Service(self._driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def scrape(self) -> List[Job]:
        driver = self._get_driver()
        try:
            full_url = f"{self.base_url}{self.route}"
            logger.info("Navigating to: %s", full_url)
            driver.get(full_url)

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="jobs-item"]')
                )
            )

            job_elements = driver.find_elements(
                By.CSS_SELECTOR, '[data-testid="jobs-item"]'
            )
            jobs = []

            logger.info("Found %d job elements.", len(job_elements))
            for element in job_elements:
                try:
                    try:
                        title = element.find_element(By.CSS_SELECTOR, "h2").text
                    except Exception:
                        title = "N/A"

                    try:
                        company = element.find_element(By.CSS_SELECTOR, "p").text
                    except Exception:
                        company = "N/A"

                    try:
                        link = element.find_element(By.CSS_SELECTOR, "a").get_attribute(
                            "href"
                        )
                    except Exception:
                        continue

                    try:
                        location_container = element.find_element(
                            By.XPATH, './/div[*[@data-testid="RoomRoundedIcon"]]'
                        )
                        location = (
                            location_container.get_attribute("textContent").strip()
                            or "Algeria"
                        )
                    except Exception:
                        location = "Algeria"

                    try:
                        time_container = element.find_element(
                            By.XPATH,
                            './/div[*[@data-testid="TimelapseRoundedIcon"]]',
                        )
                        posted_time = (
                            time_container.get_attribute("textContent").strip() or "N/A"
                        )
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
                    logger.warning("Error extracting Emploitic job detail: %s", e)

            return jobs
        finally:
            driver.quit()
