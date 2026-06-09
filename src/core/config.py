import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path)

DB_PATH = PROJECT_ROOT / os.getenv("DB_PATH", "src/data/jobs.db")

WEBSITE_URL = os.getenv("WEBSITE_URL", "https://emploitic.com/offres-d-emploi")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
