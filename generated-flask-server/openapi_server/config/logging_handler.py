import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_dir = "/var/log/my_app"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")
    
    handler = RotatingFileHandler(log_file, maxBytes=2000000, backupCount=10)
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[handler])
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)

    # Ensure the handler terminator is set properly
    for handler in logger.handlers:
        handler.terminator = '\n'

    return logger
