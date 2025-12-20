
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    file = RotatingFileHandler(
        "app.log", maxBytes=10_000_000, backupCount=5
    )
    file.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file)

