#!/usr/bin/env python3
""" Filtered Logger """
import re
import logging


def filter_datum(fields, redaction, message, separator):
    for field in fields:
        message = re.sub(f"{field}=[^;]*", f"{field}={redaction}", message)

    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
