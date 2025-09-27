CREATE_JOBS_TABLE = """
        CREATE TABLE IF NOT EXISTS jobs_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            time TEXT,
            tags TEXT,
            locations TEXT,
            link TEXT UNIQUE,
            logo TEXT,
            salary_from INTEGER,
            salary_to INTEGER,
            currency TEXT
        );
    """

INSERT_JOBS_TABLE = """
        INSERT INTO jobs_new (id, title, company, time, tags, locations, link, logo, salary_from, salary_to, currency)
        SELECT rowid, title, company, time, tags, locations, link, logo, salary_from, salary_to, currency
        FROM jobs;
    """

DELETE_DUPLICATES = """
            DELETE FROM jobs
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM jobs
                GROUP BY title, company, time, tags, locations, salary, link, logo
            );
        """