import sqlite3
import re
from src.database.schema import CREATE_JOBS_TABLE, INSERT_JOBS_TABLE, DELETE_DUPLICATES

def connect_db(db_path="src/data/jobs.db"):
    return sqlite3.connect(db_path)


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
    conn = connect_db()
    cursor = conn.cursor()
    try: 
        cursor.execute(DELETE_DUPLICATES)
    except sqlite3.OperationalError:
        pass

    cursor.execute("SELECT rowid, tags FROM jobs")
    for rowid, tags in cursor.fetchall():
        cleaned_tags = normalize_tags(tags)
        cursor.execute(
            "UPDATE jobs SET tags = ? WHERE rowid = ?", (cleaned_tags, rowid)
        )

    cursor.execute("DELETE FROM jobs WHERE time LIKE '%1yr%'")

    try:
        cursor.execute("ALTER TABLE jobs ADD COLUMN salary_from INTEGER;")
        cursor.execute("ALTER TABLE jobs ADD COLUMN salary_to INTEGER;")
        cursor.execute("ALTER TABLE jobs ADD COLUMN currency TEXT;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("SELECT rowid, salary FROM jobs")
        for rowid, raw_salary in cursor.fetchall():
            salary_from, salary_to, currency = extract_salary_parts(raw_salary)
            cursor.execute(
                "UPDATE jobs SET salary_from = ?, salary_to = ?, currency = ? WHERE rowid = ?",
                (salary_from, salary_to, currency, rowid),
            )
    except sqlite3.OperationalError:
        pass

    cursor.execute(CREATE_JOBS_TABLE)

    cursor.execute(INSERT_JOBS_TABLE)

    cursor.execute("DROP TABLE jobs;")
    cursor.execute("ALTER TABLE jobs_new RENAME TO jobs;")
    conn.commit()
    conn.close()
    print("✅ Jobs cleaned successfully.")


def main_cleaner():
    clean_jobs()

if __name__ == "__main__":
    main_cleaner()
