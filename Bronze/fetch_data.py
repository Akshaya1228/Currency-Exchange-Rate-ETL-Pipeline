# Data Fetching Module: start and end date are passed as parameters to the function and the API is called to fetch the data. 
# The fetched data is then saved in the Bronze layer/New_raw_data as a new_raw.json file. 
# The function also returns the path of the saved file and metadata about the fetched data
# metadata includes source of the data, fetch time, base currency and amount.


import requests
import os
import json
from logger import logger
from datetime import datetime 
import loading_config
import logging


def fetch_data(start_date, end_date):
    setup_logger = logger("format_1")

    try:
        config_data = loading_config.load_config()

        response = requests.get(f"{config_data['url']}{start_date}..{end_date}?base={config_data['base_currency']}")
        
        print(f"url used to fetch the API is : {config_data['url']}{start_date}..{end_date}?base={config_data['base_currency']}")
        logging.info(f"url used to fetch the API is : {config_data['url']}{start_date}..{end_date}?base={config_data['base_currency']}")
    
        data = response.json()
        if response.status_code != 200:
            logging.error(f"Failed to fetch data from API. Status code: {response.status_code}")
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None, None

        os.makedirs(config_data["new_data_folder_path"] , exist_ok = True)

        file_name = "new_raw_data.json"

        path = os.path.join(config_data['new_data_folder_path'], file_name)

        metadata = {
            "source": config_data["source"],
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "base_currency": data["base"],
            "amount": data["amount"],
            "start_date": start_date,
            "end_date": end_date
        }

        with open(path, "w") as f:
            json.dump(data, f)
            logging.info(f"Data saved successfully to {file_name}")
            print(f"Data saved successfully to {file_name}")
        

        return path , metadata

    except Exception as error:
        logging.error(f"Error occurred while fetching data from API: {error}")
        print(f"Error occurred while fetching data from API: {error}")

        return None, None

    
