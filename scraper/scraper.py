from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--headless") 
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(options=options)

url = "https://remoteok.com/remote-dev-jobs"
driver.get(url)

time.sleep(5)

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
        tags_div = job_element.find_element(By.CSS_SELECTOR, "div.tags")
        tags_elements = tags_div.find_elements(By.CSS_SELECTOR, "h3")
        tags = [tag.text.strip() for tag in tags_elements if tag.text.strip()]
    except:
        tags = []
    jobs.append({"title": title, "time": posted, "company": company, "tags": tags})

print(f"Found {len(jobs)} jobs:")
for i, job in enumerate(jobs, 1):
    print(f"{i}. Title: {job['title']}")
    print(f"   Posted: {job['time']}")
    print(f"   Company: {job['company']}")
    print("-" * 50)

driver.quit()
