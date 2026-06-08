import logging
from abc import ABC, abstractmethod
from typing import List

from src.core.database import get_db_connection
from src.core.models import Job

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    @abstractmethod
    def scrape(self) -> List[Job]:

        pass

    def run(self) -> int:

        logger.info("Starting %s...", self.__class__.__name__)
        jobs = self.scrape()
        if not jobs:
            logger.info("No jobs found by %s.", self.__class__.__name__)
            return 0

        conn = get_db_connection()
        try:
            for job in jobs:
                job.save_to_db(conn)
            conn.commit()
            logger.info(
                "Successfully saved %d jobs from %s.",
                len(jobs),
                self.__class__.__name__,
            )
            return len(jobs)
        except Exception:
            conn.rollback()
            logger.exception(
                "%s failed to save jobs, rolled back.", self.__class__.__name__
            )
            raise
        finally:
            conn.close()
