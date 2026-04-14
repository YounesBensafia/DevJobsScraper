from .emploitic import EmploiticScraper
from .remoteok import RemoteOKScraper

SCRAPERS = {"remoteok": RemoteOKScraper, "emploitic": EmploiticScraper}


def get_scraper(name):

    scraper_class = SCRAPERS.get(name)
    if scraper_class:
        return scraper_class()
    return None
