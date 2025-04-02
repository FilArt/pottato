import sys
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import logging

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.sql import PostgresLexer

postgres = PostgresLexer()
terminal_formatter = TerminalFormatter()


class PygmentsFormatter(logging.Formatter):
    def __init__(
        self,
        fmt="{asctime} - {name}:{lineno} - {levelname} - {message}",
        datefmt="%H:%M:%S",
    ):
        self.datefmt = datefmt
        self.fmt = fmt
        logging.Formatter.__init__(self, None, datefmt)

    def format(self, record: logging.LogRecord):
        """Format the logging record with slq's syntax coloration."""
        own_records = {
            attr: val for attr, val in record.__dict__.items() if not attr.startswith("_")
        }
        message = record.getMessage()
        name = record.name
        asctime = self.formatTime(record, self.datefmt)

        if name == "tortoise.db_client":
            if (
                record.levelname == "DEBUG"
                and not message.startswith("Created connection pool")
                and not message.startswith("Closed connection pool")
            ):
                message = highlight(message, postgres, terminal_formatter).rstrip()

        own_records.update(
            {
                "message": message,
                "name": name,
                "asctime": asctime,
            }
        )

        return self.fmt.format(**own_records)


# Then replace the formatter above by the following one


def register_orm(
    app: FastAPI,
    db_url: str,
    generate_schemas: bool = False,
    print_sql: bool = False,
):
    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["pottato.services.db.models"]},
        generate_schemas=generate_schemas,
    )

    if print_sql:
        fmt = PygmentsFormatter(fmt="{asctime} - {levelname} - {message}")
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(fmt)

        # will print debug sql
        logger_db_client = logging.getLogger("tortoise.db_client")
        logger_db_client.setLevel(logging.DEBUG)
        logger_db_client.addHandler(sh)
