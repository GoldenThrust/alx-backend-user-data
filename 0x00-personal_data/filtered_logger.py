#!/usr/bin/env python3
""" Filtered Logger """
import re
import logging
from os import getenv
from typing import List
from mysql import connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filter sensitive information in the log message."""
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*",
                         f"{field}={redaction}", message)

    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord.
        """
        message = super().format(record)
        return filter_datum(self.fields,
                            self.REDACTION, message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Get a configured logger for user_data with redacted PII."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger_streamhandler = logging.StreamHandler()
    logger_streamhandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(logger_streamhandler)
    return logger


def get_db() -> connector.connection.MySQLConnection:
    """Get a connection to the personal data database."""
    username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    hostname = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = getenv("PERSONAL_DATA_DB_NAME")

    return connector.connect(
        user=username, password=password, host=hostname, database=dbname
    )


def main():
    """Main function to execute the script."""
    logger = get_logger()

    with get_db() as db, db.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")

        name = [desc[0] for desc in cursor.description]

        for row in cursor:
            field = [f"{column}={value}" for column, value in zip(name, row)]
            fields = "; ".join(field)
            logger.info(fields)


if __name__ == "__main__":
    main()
