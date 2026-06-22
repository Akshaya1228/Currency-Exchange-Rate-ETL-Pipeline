import calculate_file_hash
import logging
import os
from datetime import datetime
from logger import logger


def detect_file_changes(file_path, old_config_hash):
    setup_logger = logger()

    current_hash = calculate_file_hash.calculate_file_hash(file_path)
    if not os.path.exists(old_config_hash):
        return True, current_hash

    with open(old_config_hash, "r") as f:
        last_hash = f.read()
    
    if current_hash != last_hash:
        print(f"Config File has changed. date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"Config File has changed. date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True, current_hash
    else:
        return False, current_hash