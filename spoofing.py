#!/usr/bin/env python3

""""""
from user_agent import generate_user_agent


class Headers:
    """"""

    def __init__(self):
        """"""

    def get_headers(self):
        """"""
        # Test this: Automate more options as we go. Such as referrer, maybe
        # accepts, languages.
        headers = {
            "user-agent": generate_user_agent(device_type="desktop", 
                                              os=("mac", "linux", "win")),
            "referrer": "http://us.vclart.net/",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9"
        }

        return headers