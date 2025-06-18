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
        tags = []

        tags_divs = job_element.find_elements(By.CLASS_NAME, "tags")

        for div in tags_divs:
            h3s = div.find_elements(By.TAG_NAME, "h3")
            tags.extend([h3.text.strip() for h3 in h3s if h3.text.strip()])
    except:
        print("Error extracting tags for job:", title)
        exit(1)

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
        exit(1)

    jobs.append(
        {
            "title": title,
            "time": posted,
            "company": company,
            "tags": tags,
            "locations": location if location else ["Not mentioned"],
            "salary": salary if salary else ["Not mentioned"],
        }
    )

print(f"Found {len(jobs)} jobs:")
for i, job in enumerate(jobs, 1):
    print(f"{i}. Title: {job['title']}")
    print(f"   Posted: {job['time']}")
    print(f"   Company: {job['company']}")
    print(f"   Tags: {', '.join(job['tags']) if job['tags'] else 'Not mentioned'}")
    print(
        f"   Locations: {', '.join(job['locations']) if job['locations'] else 'Not mentioned'}"
    )
    print(f"   Salary: {', '.join(job['salary']) if job['salary'] else 'Not mentioned'}")
    print("-" * 50)

driver.quit()
