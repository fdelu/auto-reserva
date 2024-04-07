import logging
import sys
import os

LOGGING_COLORED = os.getenv("LOGGING_COLORED", False)
FORMAT = "{asctime} | {levelname} | {funcName} | {message}"

COLOR = "\033[0;35m"
COLOR_END = "\033[0m"


class AppLogger(logging.Logger):
    def __init__(self) -> None:
        super().__init__("app")
        handler = logging.StreamHandler(sys.stdout)
        fmt = FORMAT
        if LOGGING_COLORED:
            fmt = COLOR_END + COLOR + fmt + COLOR_END
        handler.setFormatter(logging.Formatter(fmt, style="{"))
        handler.setLevel(logging.DEBUG)
        self.setLevel(logging.DEBUG)
        self.addHandler(handler)
