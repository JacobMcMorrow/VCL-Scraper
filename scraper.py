#!/usr/bin/env python3

""""""
import os
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
        self._current_artist = None
        self._current_proxies = None

    def scrape(self):
        """"""
        self._scrape_artists()

    def _scrape_artists(self):
        """"""
        if not os.path.exists("Artists"):
            os.mkdir("Artists")

        try:
            self._current_proxies = self.proxies.get_proxies(ARTISTS_URL)
            response = requests.get(ARTISTS_URL,
                                    proxies=self._current_proxies,
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            # Tables aren't named, find a way to double check incase they move
            # things in the future.
            artist_table = soup.select("table")[4]
            artists = artist_table.select("a")

            # Look into making a generator to ease memory.
            for artist in artists:
                self._scrape_artist(artist)
            
        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")

    def _scrape_artist(self, artist):
        """"""
        self._current_artist = artist.get("href").split("/")[-2]
        # self._current_artist = "Selunca"
        print(self._current_artist)
        artist_url = BASE_URL + artist.get("href")
        # artist_url = "http://us.vclart.net/vcl/Artists/Selunca/"
        
        if not os.path.exists(os.path.join("Artists", self._current_artist)):
            os.mkdir(os.path.join("Artists", self._current_artist))

        try:
            # Multiple proxie requests is excessive. Either grab one at the
            # start or write a counter to check when to grab the next. Maybe
            # make it random.
            self._current_proxies = self.proxies.get_proxies(ARTISTS_URL)
            response = requests.get(artist_url,
                                    proxies=self._current_proxies,
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

        for row in image_rows:
            index_by_date = row.select("a")[0]
            page_url = artist_url + index_by_date.get("href")
            self._scrape_page(page_url)

    def _scrape_page(self, page_url):
        """"""
        try:
            # Multiple proxie requests is excessive. Either grab one at the
            # start or write a counter to check when to grab the next. Maybe
            # make it random.
            response = requests.get(page_url,
                                    proxies=self._current_proxies,
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            image_table = soup.select("table")[1]

            image_rows = image_table.select("img")
            # self._download_image(image_rows[0].get("alt"))

            for row in image_rows:
               self._download_image(row.get("alt"))

        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")

    def _download_image(self, image_name):
        """"""
        image_url = f"{ARTISTS_URL}{self._current_artist}/{image_name}"
        # print(image_url)
        file_name = os.path.join(self._current_artist, image_name)
        # print(file_name)

        try:
            print(f"Downloading image: {image_name}")
            response = requests.get(image_url,
                                    proxies=self._current_proxies,
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            # Move to separate function? Also, check if file already exists.
            with open(os.path.join("Artists", file_name), "wb") as image_file:
                for chunk in response.iter_content(100000):
                    image_file.write(chunk)

        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")
