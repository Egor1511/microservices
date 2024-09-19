import logging
import sys
from logging.handlers import RotatingFileHandler

from app.config import settings
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("user_service")

logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
console_handler.setFormatter(console_format)

file_handler = RotatingFileHandler(settings.LOG_FILE, maxBytes=1024 * 1024 * 10, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s")
file_handler.setFormatter(file_format)

json_handler = logging.StreamHandler(sys.stdout)
json_handler.setLevel(logging.INFO)
json_format = jsonlogger.JsonFormatter()
json_handler.setFormatter(json_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(json_handler)
