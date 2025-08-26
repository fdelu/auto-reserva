import logging
import sys

COLOR_END = "\033[0m"
COLOR = "\033[0;35m"
LOG_FORMAT = (
    f"{COLOR_END}{COLOR}"
    "%(asctime)s | %(levelname)s | %(funcName)s | %(message)s"
    f"{COLOR_END}"
)


def setup_logs() -> None:
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
