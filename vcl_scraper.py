#!/usr/bin/env python3

""""""
from proxies import Proxies
from scraper import Scraper
from spoofing import Headers


if __name__ == "__main__":
    headers = Headers()
    proxies = Proxies(headers)
    scraper = Scraper(headers, proxies)
    scraper.scrape()
