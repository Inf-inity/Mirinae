import logging
import sys

from .environment import LOG_LEVEL


class ColorFormatter(logging.Formatter):
    LEVEL_COLOURS = [
        (logging.DEBUG, '\x1b[30;1;2m'),
        (logging.INFO, '\x1b[34;1;2m'),
        (logging.WARNING, '\x1b[33;1;2m'),
        (logging.ERROR, '\x1b[31;1;2m'),
        (logging.CRITICAL, '\x1b[31;1m'),
    ]

    FORMATS = {
        level: logging.Formatter(
            f"\x1b[30;1m[{{asctime}}]\x1b[0m {color}[{{levelname:<8}}]\x1b[0m \x1b[35m{{name:<40}}>\x1b[0m {color}{{message}}\x1b[0m",
            "%Y-%m-%d %H:%M:%S",
            style="{"
        )
        for level, color in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)

        record.exc_text = None
        return output


logging_handler = logging.StreamHandler(sys.stdout)
logging_handler.setFormatter(ColorFormatter())


def get_logger(name: str) -> logging.Logger:
    """Get a logger with a given name."""

    logger: logging.Logger = logging.getLogger(name)
    logger.addHandler(logging_handler)
    logger.setLevel(LOG_LEVEL.upper())

    return logger
