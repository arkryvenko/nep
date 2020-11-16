import sys
from loguru import logger

LOG_FILE = "cud_audit.log"
LOG_LEVEL = "INFO"
ROTATION = "100 MB"


async def init_logger():
    logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")
    logger.add(LOG_FILE, rotation=ROTATION, level=LOG_LEVEL)
