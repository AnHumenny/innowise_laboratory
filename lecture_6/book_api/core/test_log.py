import logging
import sys
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "test_run.log"

test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)

test_logger.handlers.clear()

formatter = logging.Formatter(
    "[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%H:%M:%S"
)

file_handler = logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

test_logger.addHandler(file_handler)
test_logger.addHandler(console_handler)

test_logger.propagate = False

test_logger.info("=" * 50)
test_logger.info("TEST LOGGER STARTED")
test_logger.info(f"Log file: {LOG_FILE}")
test_logger.info("=" * 50)