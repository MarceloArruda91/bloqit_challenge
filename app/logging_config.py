import logging
from logging.handlers import RotatingFileHandler
import os
import atexit


def setup_logging():
    # Create a logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # Set up the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)

    # Create a file handler which logs even debug messages
    file_handler = RotatingFileHandler(
        "logs/api.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s [in %(pathname)s:%(lineno)d]",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Flush log file handlers on exit

    atexit.register(logging.shutdown)
