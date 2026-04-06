import sqlite3
import re
from src.core.database import get_db_connection

def normalize_tags(tags):

    if not tags:
        return "not mentioned"
    return ", ".join(tag.strip() for tag in tags.split(","))


def extract_salary_parts(raw_salary):

    if not raw_salary or "negotiable" in raw_salary.lower():
        return None, None, None

    currency_match = re.search(r"[\$\€£]", raw_salary)
    currency = currency_match.group() if currency_match else None

    cleaned = re.sub(r"[^\d\-–]", "", raw_salary.replace("k", "000").replace(",", ""))

    parts = re.findall(r"\d+", cleaned)
    if len(parts) >= 2:
        return int(parts[0]), int(parts[1]), currency
    elif len(parts) == 1:
        return int(parts[0]), int(parts[0]), currency
    else:
        return None, None, currency


def clean_jobs():

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, tags FROM jobs")
    for row_id, tags in cursor.fetchall():
        if tags:
            cleaned_tags = normalize_tags(tags)
            cursor.execute("UPDATE jobs SET tags = ? WHERE id = ?", (cleaned_tags, row_id))

    print("Filtering old jobs...")
    cursor.execute("DELETE FROM jobs WHERE time LIKE '%1yr%'")

    conn.commit()
    conn.close()
    print("✅ Jobs cleaned successfully.")

def main_cleaner():
    clean_jobs()

if __name__ == "__main__":
    main_cleaner()
