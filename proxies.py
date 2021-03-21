#!/usr/bin/env python3

""""""
import requests
from bs4 import BeautifulSoup
from itertools import cycle

from spoofing import Headers

# Global macro for now, but replace when multiple proxy sources available.
PROXIES_URL = "https://free-proxy-list.net/"

class Proxies:
    """"""

    def __init__(self, headers, logger):
        """"""
        self.headers = headers
        self.logger = logger

    def get_proxies(self, url):
        """"""
        proxies = self._check_proxies(url)

        while proxies is None:
             proxies = self._check_proxies(url)    

        return proxies

    def _check_proxies(self, url):
        """"""
        proxies = self._collect_proxies()
        # Randomize pool so we don't select the same one each call.
        proxy_pool = cycle(proxies)

        for i in range(1, 11):
            proxy = next(proxy_pool)
            print("Proxy Request #%d:" % i)

            try:
                response = requests.get(url, proxies={"https" : proxy},
                                        headers=self.headers.get_headers())
                response.raise_for_status()
                print(proxy)
                return {"https" : proxy}

            except:
                print("Skipping proxy. Connection error.")

    def _collect_proxies(self):
        """"""
        proxies = set()
        raw_proxies = self._get_raw_proxies()

        for raw_proxy in raw_proxies:
            proxies = self._process_raw_proxy(raw_proxy, proxies)

        return proxies

    def _is_secure(self, proxy_components):
        """"""
        # Consider adding check for country of origin.
        anonymous = (proxy_components[4].getText() == "elite proxy")
        https = (proxy_components[6].getText() == "yes")

        return anonymous and https

    def _get_raw_proxies(self):
        """"""
        try:
            response = requests.get(PROXIES_URL,
                                    headers=self.headers.get_headers())
            response.encode = "utf-8"
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            return soup.select("#proxylisttable tr")[1:]

        except Exception as e:
            error_message = (
                f"An error of type {type(e).__name__} occured collecting raw "
                f"proxies. Details: {e}"
            )

            self.logger.log_error(error_message)
            print(error_message)

    def _process_raw_proxy(self, raw_proxy, proxies):
        """"""
        proxy_components = raw_proxy.select("td")
        proxy = ""

        if proxy_components != [] and self._is_secure(proxy_components):
            ip_address = proxy_components[0].getText()
            port = proxy_components[1].getText()
            proxy = f"https://{ip_address}:{port}"
            proxies.add(proxy)

        return proxies
