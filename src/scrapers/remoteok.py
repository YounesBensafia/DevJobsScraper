import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.core.models import Job
from src.scrapers.base import BaseScraper
from src.utils.cleaner import extract_salary_parts


class RemoteOKScraper(BaseScraper):
    def __init__(self):
        self.url = "https://remoteok.com/remote-dev-jobs"

    def _get_driver(self):
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
        )
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--remote-allow-origins=*")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def scrape(self) -> List[Job]:
        driver = self._get_driver()
        print(f"Navigating to {self.url}...")
        driver.get(self.url)
        time.sleep(5)

        job_elements = driver.find_elements(By.CSS_SELECTOR, "tr.job")
        jobs = []

        print(f"Found {len(job_elements)} job elements.")
        for job_element in job_elements:
            try:
                try:
                    title_element = job_element.find_element(
                        By.CSS_SELECTOR, "h2[itemprop='title']"
                    )
                    title = title_element.text.strip()
                except Exception:
                    title = job_element.text.strip()

                if not title:
                    continue

                try:
                    time_element = job_element.find_element(By.CSS_SELECTOR, "td.time")
                    posted = time_element.text.strip()
                except Exception:
                    posted = "N/A"

                try:
                    company_element = job_element.find_element(
                        By.CSS_SELECTOR, "h3[itemprop='name']"
                    )
                    company = company_element.text.strip()
                except Exception:
                    company = "N/A"

                tags = []
                try:
                    tags_divs = job_element.find_elements(By.CLASS_NAME, "tags")
                    for div in tags_divs:
                        h3s = div.find_elements(By.TAG_NAME, "h3")
                        tags.extend([h3.text.strip() for h3 in h3s if h3.text.strip()])
                except Exception:
                    print("Error extracting tags for job:", title)

                salary_raw = "Not mentioned"
                locations_list = []
                try:
                    divs = job_element.find_elements(By.CSS_SELECTOR, "div.location")
                    for div in divs:
                        content = div.get_attribute("textContent").strip()
                        if "💰" in content:
                            salary_raw = content
                        else:
                            locations_list.append(content)
                except Exception:
                    print("Error extracting locations for job:", title)

                try:
                    link_element = job_element.find_element(By.CSS_SELECTOR, ".preventLink")
                    link = link_element.get_attribute("href").strip()
                except Exception:
                    print("Error extracting link for job:", title)
                    continue

                try:
                    logo_element = job_element.find_element(By.CSS_SELECTOR, ".logo")
                    logo = logo_element.get_attribute("data-src")
                    if logo and logo.startswith("/"):
                        logo = "https://remoteok.com" + logo
                except Exception:
                    logo = None

                salary_from, salary_to, currency = extract_salary_parts(salary_raw)

                jobs.append(
                    Job(
                        title=title,
                        company=company,
                        link=link,
                        time=posted,
                        tags=", ".join(tags) if tags else "not mentioned",
                        locations=", ".join(locations_list) if locations_list else "Not mentioned",
                        logo=logo,
                        salary_from=salary_from,
                        salary_to=salary_to,
                        currency=currency,
                    )
                )

            except Exception as e:
                print(f"Error processing a job element: {e}")

        driver.quit()
        return jobs


if __name__ == "__main__":
    scraper = RemoteOKScraper()
    scraper.run()
