import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import os


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    """A custom handler that saves rotated log files in format:

    app.2025-12-06.log
    instead of the default:
    app.log.2025-12-06
    """

    def rotation_filename(self, default_name: str) -> str:
        """
        Convert default name ('app.log.2025-12-06')
        into desired format ('app.2025-12-06.log').
        """
        directory, filename = os.path.split(default_name)
        base, date_part = os.path.splitext(filename)

        date_str = date_part.lstrip('.')

        name, real_ext = os.path.splitext(base)

        new_filename = f"{name}.{date_str}{real_ext}"
        return os.path.join(directory, new_filename)


LOG_DIR = Path(__file__).resolve().parent / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = CustomTimedRotatingFileHandler(
    LOG_FILE,
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Logger initialized successfully.")
