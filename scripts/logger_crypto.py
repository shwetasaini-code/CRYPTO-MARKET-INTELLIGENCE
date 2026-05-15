import logging
import os

os.makedirs('logs', exist_ok=True)

LOG_FILE = 'logs/crypto_pipeline.log'

logger = logging.getLogger("crypto_pipeline")

logger.setLevel(logging.INFO)

if not logger.handlers:

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler= logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
