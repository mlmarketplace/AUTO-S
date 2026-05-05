import logging
import os

LOG_DIR = "_phase8/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "agent.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)