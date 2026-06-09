import logging
import sqlite3

import pandas as pd

logger = logging.getLogger(__name__)

conn = sqlite3.connect("./src/data/jobs.db")
df = pd.read_sql_query("SELECT * FROM jobs", conn)
df.to_csv("./src/data/jobs.csv", index=False)
conn.close()
logger.info("Exported jobs to jobs.csv")
