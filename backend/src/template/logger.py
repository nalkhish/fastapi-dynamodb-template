"""This module creates a logger object that can be imported into other modules

It logs to stdout with a format that is easy to read and parse
"""
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    fmt = "%(asctime)s (%(name)s):  %(message)s"
    fmts = {
        logging.DEBUG: grey + "DEBUG" + reset + ":    " + fmt,
        logging.INFO: green + "INFO" + reset + ":    " + fmt,
        logging.WARNING: yellow + "WARNING" + reset + ":    " + fmt,
        logging.ERROR: red + "ERROR" + reset + ":    " + fmt,
        logging.CRITICAL: bold_red + "CRITICAL" + reset + ":    " + fmt,
    }

    def format(self, record: logging.LogRecord):
        log_fmt = self.fmts.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


if os.environ.get("ENVIRONMENT", default="prod") == "dev":
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
else:
    logger.debug("Not adding custom handler because ENVIRONMENT is not dev")
