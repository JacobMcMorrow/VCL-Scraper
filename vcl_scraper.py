#!/usr/bin/env python3

""""""
from spoofing import Headers
from proxies import Proxies


if __name__ == "__main__":
    headers = Headers()
    proxies = Proxies(headers)
    proxy = proxies.get_proxies("http://us.vclart.net/vcl/")
