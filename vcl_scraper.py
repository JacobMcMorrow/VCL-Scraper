#!/usr/bin/env python3

""""""
from logger import Logger
from proxies import Proxies
from scraper import Scraper
from spoofing import Headers


if __name__ == "__main__":
    headers = Headers()
    logger = Logger()
    proxies = Proxies(headers, logger)
    scraper = Scraper(headers, proxies, logger)
    scraper.scrape()
