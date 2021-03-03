#!/usr/bin/env python3

from user_agent import generate_user_agent

class Headers:
    """"""

    def __init__(self):
        """"""

    def get_headers(self):
        """"""
        user_agent = generate_user_agent(device_type="desktop",
                                         os=("mac", "linux", "win"))
        return {"User-Agent": user_agent}