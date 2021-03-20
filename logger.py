#!/usr/bin/env python3

""""""
import os

class Logger:
    """"""

    def __init__(self, active=True):
        """"""
        self._log_active = active
        self._log_file = "vcl_scraper_log.log"

    # Include actual error/exception?
    def log_error(self, message):
        """"""
        if self._log_active:
            # Maybe add more detailed error message.
            error_message = "ERROR - " + message + "\n"

            self._log(error_message)

    def log_info(self, message):
        """"""
        if self._log_active:
            # Maybe add more detailed info message
            info_message = "INFO  - " + message + "\n"

            self._log(info_message)

    def _log(self, message):
        """"""
        try:
            with open(self._log_file, "a") as log:
                log.write(message)

        except Exception as exception:
            # Add option to shutdown logging.
            error_message = (
                f"An error of type {type(e).__name__} occured while writing "
                f"to vcl_scraper_log.log. Details: {e}"
            )

            print(error_message)