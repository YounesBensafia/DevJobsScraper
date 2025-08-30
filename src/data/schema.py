import sqlite3
import os
def create_db():
    db_dir = os.path.dirname("./src/data/jobs.db")
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    conn = sqlite3.connect("./src/data/jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            time TEXT NOT NULL,
            tags TEXT NOT NULL,
            location TEXT NOT NULL,
            date_posted TEXT NOT NULL,
            link TEXT NOT NULL,
            logo TEXT NOT NULL,
            etat TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database and table 'jobs' created successfully.")
if __name__ == "__main__":
    create_db()