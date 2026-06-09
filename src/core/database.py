import sqlite3

from .config import DB_PATH


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database with the required schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
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
        )
    """)
    conn.commit()
    conn.close()
