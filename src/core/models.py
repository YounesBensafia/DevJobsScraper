from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Job:
    title: str
    company: str
    link: str
    time: Optional[str] = None
    tags: Optional[str] = None
    locations: Optional[str] = None
    logo: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    currency: Optional[str] = None

    def to_dict(self):

        return asdict(self)

    def save_to_db(self, conn):

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO jobs (title, company, time, tags, locations, link, logo, salary_from, salary_to, currency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                self.title,
                self.company,
                self.time,
                self.tags,
                self.locations,
                self.link,
                self.logo,
                self.salary_from,
                self.salary_to,
                self.currency,
            ),
        )
        conn.commit()
