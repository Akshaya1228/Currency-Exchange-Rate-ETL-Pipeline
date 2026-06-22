import logging
import os
from datetime import datetime


def logger(format):
    log_folder_path = os.path.join("/Users/akshaya1228/ELT_PROJECT_2/elt_pipeline_logs",f"{datetime.now().strftime('%Y')}",f"{datetime.now().strftime('%B')}", f"{datetime.now().strftime('%Y-%m-%d')}")
    os.makedirs(log_folder_path, exist_ok=True)

    format_1 = "%(asctime)s | %(levelname)s | %(message)s"
    format_2 = "%(message)s"

    if format == "format_1":
        logging_format = format_1
    else:
        logging_format = format_2
        
    logging.basicConfig(
    filename=os.path.join(log_folder_path, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"),
    level=logging.INFO,
    format=logging_format
    )
    
    