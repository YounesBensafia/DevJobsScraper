from abc import ABC, abstractmethod
from typing import List

from src.core.database import get_db_connection
from src.core.models import Job


class BaseScraper(ABC):
    @abstractmethod
    def scrape(self) -> List[Job]:

        pass

    def run(self):

        print(f"Starting {self.__class__.__name__}...")
        jobs = self.scrape()
        if not jobs:
            print(f"No jobs found by {self.__class__.__name__}.")
            return

        conn = get_db_connection()
        try:
            for job in jobs:
                job.save_to_db(conn)
            print(f"Successfully saved {len(jobs)} jobs from {self.__class__.__name__}.")
        finally:
            conn.close()
