#!/usr/bin/env python3

""""""
from proxies import Proxies
from spoofing import Headers


if __name__ == "__main__":
    headers = Headers()
    proxies = Proxies(headers)
    proxy = proxies.get_proxies("http://us.vclart.net/vcl/")
