from .remoteok import RemoteOKScraper
from .emploitic import EmploiticScraper

SCRAPERS = {
    "remoteok": RemoteOKScraper,
    "emploitic": EmploiticScraper
}

def get_scraper(name):

    scraper_class = SCRAPERS.get(name)
    if scraper_class:
        return scraper_class()
    return None
