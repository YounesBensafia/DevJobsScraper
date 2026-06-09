import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


def create_db():
    db_dir = os.path.dirname("./jobs.db")
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    conn = sqlite3.connect("./jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            date_posted TEXT NOT NULL,
            link TEXT NOT NULL,
            etat TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Database and table 'jobs' created successfully.")
