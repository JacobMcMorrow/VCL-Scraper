#!/usr/bin/env python3

""""""
import os
import requests
from bs4 import BeautifulSoup

from spoofing import Headers

BASE_URL = "http://us.vclart.net"
ARTISTS_URL = "http://us.vclart.net/vcl/Artists/"
AUTHORS_URL = ""

# Map from invalid URL symbols to their replacement.
URL_SYMBOLS_MAP = {
    "%": "%25",
    "#": "%23",
    ",": "%2C",
    "ñ": "%F1",
    "½": "%BD",
    "'": "%27",
}

# Invalid directory name symbols.
# Update list of invalid symbols for ascii chars?
FORBIDDEN_SYMBOLS = [
    "<",
    ">",
    ":",
    "\"",
    "/",
    "\\",
    "|",
    "?",
    "*",
]

RESERVED_NAMES = [
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
]

class Scraper:
    """"""

    def __init__(self, headers, proxies, logger):
        """"""
        self.headers = headers
        self.logger = logger
        self.proxies = proxies
        self._current_artist = None
        self._current_proxies = None
        self._reserved_name_count = 0

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

        # Log the start of scraping artists.
        self.logger.log_info("Scraping artists.")

        # Look into making a generator to ease memory.
        # for artist in artists:
        #     self._scrape_artist(artist)

        self._scrape_artist(artists[0])

    def _scrape_artist(self, artist):
        """"""
        self._current_artist = artist.get("href").split("/")[-2]
        # self._current_artist = "Selunca"
        # self._current_artist = "Drakhenliche"
        # self._current_artist = "Drak"
        # self._current_artist = "Amy-Simmonds"
        # self._current_artist = "Melissa-Camic"
        # self._current_artist = "DJ-Sunny-D"
        # self._current_artist = "Michael-Angel-Pena"
        self._current_artist = "Antiroo"
        artist_url = BASE_URL + artist.get("href")
        # artist_url = "http://us.vclart.net/vcl/Artists/Selunca/"
        # artist_url = "http://us.vclart.net/vcl/Artists/Drakhenliche/"
        # artist_url = "http://us.vclart.net/vcl/Artists/Drak/"
        # artist_url = "http://us.vclart.net/vcl/Artists/Amy-Simmonds/"
        # artist_url = "http://us.vclart.net/vcl/Artists/Melissa-Camic/"
        # artist_url = "http://us.vclart.net/vcl/Artists/DJ-Sunny-D/"
        # artist_url = "http://us.vclart.net/vcl/Artists/Michael-Angel-Pena/"
        artist_url = "http://us.vclart.net/vcl/Artists/Antiroo/"
        directory_path = os.path.join("Artists", self._current_artist)

        # Make sure a directory exists for this artist.
        if not os.path.exists(os.path.join("Artists", self._current_artist)):
            os.mkdir(os.path.join("Artists", self._current_artist))

        # Indicate the start of work for this artist and log start.
        start_message = (
            f"Scraping artist: {self._current_artist} "
            f"Artist URL: {artist_url}"
        )
        print(start_message)
        self.logger.log_info(start_message)

        # Get new proxy for this artist.
        self._current_proxies = self.proxies.get_proxies(ARTISTS_URL)

        '''
        # Get tables to download images, files, collect directories and info.
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
        '''

    # Rename these to something more appropriate.
    def _collect_artist_info(self, artist_url, directory_path, table):
        """"""
        # Write the artist's name and VCL URL to the artist info file.
        self._write_artist_info(artist_url, directory_path, "VCL")

        # Select the rows that only include artist information.
        info_rows = table[1:]

        # Write each row of artist info to the artist info file.
        for row in info_rows:
            artist_info = row.th.contents
            lable = artist_info[0]
            contents = artist_info[1].text
            self._write_artist_info(contents, directory_path, lable)

    def _write_artist_info(self, contents, directory_path, lable):
        """"""
        # TODO: Make sure we're not writing the same info over and over.
        file_path = os.path.join(directory_path, "Artist Info.txt")
        info_line = f"{lable}: {contents}\n"

        try:
            with open(file_path, "a") as file:
                file.write(info_line)

        except Exception as e:
            error_message = (
                f"An error of type {type(e).__name__} occured while writing "
                f"artist info in {directory_path}. Details: {e}"
            )

            self.logger.log_error(error_message)
            print(error_message)

    def _collect_directories(self, artist_url, directory_path, table):
        """"""
        directory_rows = table[1:]

        for row in directory_rows:
            directory_info = row.select("a")[0]
            directory_name = directory_info.getText()
            directory_name = self._correct_name(directory_name)
            directory_url = artist_url + directory_info.get("href")
            self._scrape_directory(directory_name, directory_path,
                                   directory_url)

    def _correct_name(self, file_name):
        """"""
        # Remove any invalide symbols from the file name.
        for symbol in FORBIDDEN_SYMBOLS:
            if file_name.find(symbol) >= 0:
                file_name = file_name.replace(symbol, "")

        # Remove spaces and periods from the end of the file name.
        file_name = file_name.rstrip(". ")

        # Get base name
        split_file_name = file_name.split(".")
        basename = split_file_name[0]

        # Check if file name is a reserved name.
        if len(split_file_name) == 2 and basename in RESERVED_NAMES:
            extension = split_file_name[-1]
            # TODO: Improve this naming convention.
            self._reserved_name_count += 1
            file_name = f"reserved_name{self._reserved_name_count}.{extension}"

        return file_name        

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
            error_message = (
                f"An error of type {type(e).__name__} occured while downloading"
                f" the file {file_name}. Details: {e}"
            )

            self.logger.log_error(error_message)
            print(error_message)

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
            error_message = (
                f"An error of type {type(e).__name__} occured while collecting "
                f"the tables from the page {url}. Details: {e}"
            )

            self.logger.log_error(error_message)
            print(error_message)

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
        image_url = self._create_image_url(image_name, image_url_base)
        image_name = self._correct_name(image_name)
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
            error_message = (
                f"An error of type {type(e).__name__} occured while downloading"
                f" the image {image_name}. Details: {e}"
            )

            self.logger.log_error(error_message)
            print(error_message)

    def _create_image_url(self, image_name, image_url_base):
        """"""
        # Replace any invalid URL symbols found in the image names.
        for symbol in URL_SYMBOLS_MAP.keys():
            if image_name.find(symbol) >= 0:
                image_name = image_name.replace(symbol, URL_SYMBOLS_MAP[symbol])

        image_url = image_url_base + image_name

        return image_url
