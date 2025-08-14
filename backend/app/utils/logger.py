import sys
from loguru import logger

# Configure the logger
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/app.log", rotation="500 MB", level="DEBUG", enqueue=True, backtrace=True, diagnose=True)