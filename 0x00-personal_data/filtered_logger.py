#!/usr/bin/env python3
""" Filtered Logger """
import re
import logging
from os import getenv
from typing import List
from mysql import connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields: List, redaction: str, message: str, separator: str) -> str:
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*", f"{field}={redaction}", message)

    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        string = super().format(record)
        return filter_datum(self.fields, self.REDACTION, string, self.SEPARATOR)

def get_logger() -> logging.Logger:
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger_streamhandler = logging.StreamHandler()
    logger_streamhandler.setFormatter(RedactingFormatter(PII_FIELDS))

def get_db():
    username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    hostname = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = getenv("PERSONAL_DATA_DB_NAME")

    return connector.connect(
        user=username, password=password, host=hostname, database=dbname
    )

def main():
    db = get_db()
    cursor = db.cursor()
    logger = logging.getLogger()
    cursor.execute("SELECT * FROM users;")
    


if __name__ == "__main__":
    main()