from __future__ import annotations

import logging
from pathlib import Path


LOG_FILE = Path(__file__).resolve().parents[2] / "ecomute.log"


def _build_logger() -> logging.Logger: # This function sets up a logger for the application. It configures the logger to output INFO level logs to the console and WARNING level logs to a file. The log messages include timestamps, log levels, and the message content. If the logger already has handlers configured, it returns the existing logger to avoid adding duplicate handlers.
    logger = logging.getLogger("ecomute_logger")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO) # Set the logger to capture INFO level and above (INFO, WARNING, ERROR, CRITICAL)
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s") # Define a log message format that includes the timestamp, log level, and message content

    console_handler = logging.StreamHandler() # Create a console handler to output logs to the console
    console_handler.setLevel(logging.INFO) # Set the console handler to capture INFO level and above
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE) # Create a file handler to write logs to a file specified by LOG_FILE
    file_handler.setLevel(logging.WARNING) # Set the file handler to capture WARNING level and above (WARNING, ERROR, CRITICAL)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


logger = _build_logger()
