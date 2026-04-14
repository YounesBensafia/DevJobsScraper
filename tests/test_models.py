import sqlite3

from src.core.models import Job


def test_job_initialization():
    job = Job(title="Senior Developer", company="Tech Corp", link="https://techcorp.com/jobs/1")
    assert job.title == "Senior Developer"
    assert job.company == "Tech Corp"
    assert job.link == "https://techcorp.com/jobs/1"
    assert job.time is None


def test_job_to_dict():
    job = Job(title="Dev", company="A", link="B", tags="python")
    d = job.to_dict()
    assert d["title"] == "Dev"
    assert d["tags"] == "python"
    assert "link" in d


def test_job_save_to_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, company TEXT, time TEXT, tags TEXT,
            locations TEXT, link TEXT UNIQUE, logo TEXT,
            salary_from INTEGER, salary_to INTEGER, currency TEXT
        )
    """)

    job = Job(title="SQL Dev", company="DB Inc", link="http://db.com")
    job.save_to_db(conn)

    cursor.execute("SELECT title, company FROM jobs")
    row = cursor.fetchone()
    assert row[0] == "SQL Dev"
    assert row[1] == "DB Inc"
    conn.close()
