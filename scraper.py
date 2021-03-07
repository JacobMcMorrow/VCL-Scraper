#!/usr/bin/env python3

""""""
import requests
from bs4 import BeautifulSoup

from spoofing import Headers

BASE_URL = "http://us.vclart.net"
ARTISTS_URL = "http://us.vclart.net/vcl/Artists/"
AUTHORS_URL = ""

# If this gets too bloated, split into separate scrapers.

class Scraper:
    """"""

    def __init__(self, headers, proxies):
        """"""
        self.headers = headers
        self.proxies = proxies

    def scrape(self):
        """"""
        self._scrape_artists()

    def _scrape_artists(self):
        """"""
        try:
            response = requests.get(ARTISTS_URL,
                                    proxies=self.proxies.get_proxies(ARTISTS_URL),
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            # Tables aren't named, find a way to double check incase they move
            # things in the future.
            artist_table = soup.select("table")[4]
            artists = artist_table.select("a")

            # Look into making a generator to ease memory.
            # for artist in artists:
            #     self._scrape_artist(artist)
            self._scrape_artist(artists[0])
            
        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")

    def _scrape_artist(self, artist):
        """"""
        # artist_name = artist.get("href").split("/")[-2]
        artist_name = "Selunca"
        # print(artist_name)
        # artist_url = BASE_URL + artist.get("href")
        artist_url = "http://us.vclart.net/vcl/Artists/Selunca/"
        print(artist_url)
        

        try:
            # Multiple proxie requests is excessive. Either grab one at the
            # start or write a counter to check when to grab the next. Maybe
            # make it random.
            response = requests.get(artist_url,
                                    proxies=self.proxies.get_proxies(artist_url),
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            tables = soup.select("table")[1:-1]

            for table in tables:

                if table.select("tr")[0].text.find("Directories") >= 0:
                    print("Directories")
                elif table.select("tr")[0].text.find("Images") >= 0:
                    print("Images")
                    self._collect_images(artist_url, table.select("tr"))
                elif table.select("tr")[0].text.find("Files") >= 0:
                    print("Files")

        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")


    # Rename these to something more appropriate.
    def _collect_directories(self):
        """"""
        raise NotImplementedError

    def _collect_files(self):
        """"""
        raise NotImplementedError

    def _collect_images(self, artist_url, table):
        """"""
        image_rows = table[2:]

        # for row in image_rows:
        #     index_by_date = row.select("a")[0]
        #     page_url = artist_url + index_by_date.get("href")
        #     self._scrape_page(page_url)
        index_by_date = image_rows[0].select("a")[0]
        page_url = artist_url + index_by_date.get("href")
        self._scrape_page(page_url)

    def _scrape_page(self, url):
        """"""
        try:
            # Multiple proxie requests is excessive. Either grab one at the
            # start or write a counter to check when to grab the next. Maybe
            # make it random.
            response = requests.get(artist_url,
                                    proxies=self.proxies.get_proxies(artist_url),
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")
