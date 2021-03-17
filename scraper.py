#!/usr/bin/env python3

""""""
import os
import requests
from bs4 import BeautifulSoup

from spoofing import Headers

BASE_URL = "http://us.vclart.net"
ARTISTS_URL = "http://us.vclart.net/vcl/Artists/"
AUTHORS_URL = ""

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
        # Make sure a directory for artists exists.
        if not os.path.exists("Artists"):
            os.mkdir("Artists")

        # Collect all of the artists.
        tables = self._collect_tables(ARTISTS_URL)
        artists_table = tables[4]
        artists = artists_table.select("a")

        # Look into making a generator to ease memory.
        for artist in artists:
            self._scrape_artist(artist)

        # self._scrape_artist(artists[0])

    def _scrape_artist(self, artist):
        """"""
        self._current_artist = artist.get("href").split("/")[-2]
        # self._current_artist = "Selunca"
        # self._current_artist = "Drakhenliche"
        # self._current_artist = "Drak"
        # print(self._current_artist)
        artist_url = BASE_URL + artist.get("href")
        # artist_url = "http://us.vclart.net/vcl/Artists/Selunca/"
        # artist_url = "http://us.vclart.net/vcl/Artists/Drakhenliche/"
        # artist_url = "http://us.vclart.net/vcl/Artists/Drak/"
        directory_path = os.path.join("Artists", self._current_artist)

        # Make sure a directory exists for this artist.
        if not os.path.exists(os.path.join("Artists", self._current_artist)):
            os.mkdir(os.path.join("Artists", self._current_artist))

        # Get new proxy for this artist.
        self._current_proxies = self.proxies.get_proxies(ARTISTS_URL)

        tables = self._collect_tables(artist_url)
        media_tables = tables[1:-1]

        for table in media_tables:
            if table.select("tr")[0].text.find("Artist Information") >= 0:
                print("Artist Info")
                self._collect_artist_info(artist_url, directory_path,
                                          table.select("tr"))
            elif table.select("tr")[0].text.find("Directories") >= 0:
                print("Directories")
                self._collect_directories(artist_url, directory_path,
                                          table.select("tr"))
            elif table.select("tr")[0].text.find("Images") >= 0:
                print("Images")
                self._collect_images(artist_url, directory_path,
                                     table.select("tr"))
            elif table.select("tr")[0].text.find("Files") >= 0:
                print("Files")
                self._collect_files(artist_url, directory_path,
                                    table.select("tr"))

    # Rename these to something more appropriate.
    def _collect_artist_info(self, artist_url, directory_path, table):
        """"""
        info_rows = table[1:]

        for row in info_rows:
            artist_info = row.th.contents
            lable = artist_info[0]
            contents = artist_info[1].text
            self._write_artist_info(contents, directory_path, lable)

    def _write_artist_info(self, contents, directory_path, lable):
        """"""
        file_path = os.path.join(directory_path, "Artist Info.txt")
        info_line = f"{lable}: {contents}\n"

        try:
            with open(file_path, "a") as file:
                file.write(info_line)

        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")

    def _collect_directories(self, artist_url, directory_path, table):
        """"""
        directory_rows = table[1:]

        for row in directory_rows:
            directory_info = row.select("a")[0]
            directory_name = directory_info.getText()
            directory_url = artist_url + directory_info.get("href")
            self._scrape_directory(directory_name, directory_path,
                                   directory_url)

    def _scrape_directory(self, directory_name, directory_path, directory_url):
        """"""
        directory_path = os.path.join(directory_path, directory_name)

        # Make sure a directory exists for this directory.
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

        tables = self._collect_tables(directory_url)
        media_tables = tables[1:-1]

        for table in media_tables:
            if table.select("tr")[0].text.find("Directories") >= 0:
                print("Directories/Directories")
                self._collect_directories(directory_url, directory_path,
                                          table.select("tr"))
            elif table.select("tr")[0].text.find("Images") >= 0:
                print("Directories/Images")
                self._collect_images(directory_url, directory_path,
                                     table.select("tr"))
            elif table.select("tr")[0].text.find("Files") >= 0:
                print("Directories/Files")
                self._collect_files(directory_url, directory_path,
                                    table.select("tr"))

    def _collect_files(self, url, directory_path, table):
        """"""
        file_rows = table[1:]
        directory_path = os.path.join(directory_path, "Files")

        # Make sure a directory exists for these files.
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

        for row in file_rows:
            file_content = row.select("a")
            file_name = file_content[0].text
            file_url_end = file_content[0].get("href")
            file_url = url + file_url_end
            self._download_file(directory_path, file_name, file_url)

    def _download_file(self, directory_path, file_name, file_url):
        """"""
        file_name_computer = os.path.join(directory_path, file_name)

        try:
            print(f"Downloading file: {file_name}")

            # Get file.
            response = requests.get(file_url,
                                    proxies=self._current_proxies,
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            # Move to separate function? Also, check if file already exists?
            with open(file_name_computer, "wb") as file:
                for chunk in response.iter_content(100000):
                    file.write(chunk)

        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")

    def _collect_images(self, url, directory_path, table):
        """"""
        image_rows = table[2:]
        directory_path = os.path.join(directory_path, "Images")

        # Make sure a directory exists for these images.
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

        for row in image_rows:
            index_by_date = row.select("a")[0]
            page_url = url + index_by_date.get("href")
            self._scrape_page(directory_path, url, page_url)

    def _collect_tables(self, url):
        """"""
        try:
            response = requests.get(url, proxies=self._current_proxies,
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            return soup.select("table")

        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")

    def _scrape_page(self, directory_path, image_url_base, page_url):
        """"""
        # Collect images on this page.
        tables = self._collect_tables(page_url)
        image_table = tables[1]
        images = image_table.select("img")

        for image in images:
            image_name = image.get("alt")
            self._download_image(directory_path, image_name, image_url_base)

    def _download_image(self, directory_path, image_name, image_url_base):
        """"""
        # Correct issue in names with %. Keep an eye out for other wrong
        # symbols. If this becomes too complex, move to a new function.
        if image_name.find("%") >= 0:
            edited_name = image_name
            edited_name.replace("%", "%25")
            image_url = image_url_base + edited_name
        else:
            image_url = image_url_base + image_name

        file_name = os.path.join(directory_path, image_name)

        try:
            print(f"Downloading image: {image_name}")

            # Get image.
            response = requests.get(image_url,
                                    proxies=self._current_proxies,
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            # Move to separate function? Also, check if file already exists?
            with open(file_name, "wb") as image_file:
                for chunk in response.iter_content(100000):
                    image_file.write(chunk)

        except Exception as e:
            print(e)
            # Write a better error message, come up with a set descriptive set
            # up and apply that to each file.
            print("Error connecting")
