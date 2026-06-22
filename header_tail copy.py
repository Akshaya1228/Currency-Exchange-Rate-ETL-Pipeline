from logger import logger
import logging
from datetime import datetime
from loading_config import load_config

setup_logger = logger(format="format_2")

def head():
    
    config_data = load_config()

    logging.info(f"Pipelie Run By : {config_data["project_runner"]}")
    print(f"Pipelie Run By : {config_data["project_runner"]}")

    logging.info(f"Project Name : {config_data["project_name"]}")
    print(f"Project Name : {config_data["project_name"]}")

    logging.info(f"Time : {datetime.now()}")
    print(f"Time : {datetime.now()}")

    logging.info("--------------------------------------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------------------------------------")

def tail():
    logging.info("******************************************** END ********************************************")
    print("******************************************** END ********************************************")