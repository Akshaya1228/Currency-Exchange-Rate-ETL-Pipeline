import json,  os
from logger import logger
import pandas as pd
import loading_config
import os
from datetime import datetime
import logging


def flatten_data(data_dates, amount , base_currency):

    setup_logger = logger("format_1")

    config_data = loading_config.load_config()


    for date in data_dates:

        data_path = os.path.join(config_data["historic_data_folder_path"],f"year_{date.year}",f"{date.strftime("%B")}", f"{datetime.strftime(date, "%Y-%m-%d")}.json")
        
        with open(data_path, "r") as f:
            full_data = json.load(f)
            data = full_data["data"]
            
            df = pd.DataFrame.from_dict(data, orient="index").reset_index()
            df.columns =["currency", "exchange_rate"]
            df["amount"] = amount
            df["base_currency"] = base_currency
            df["date"] = date.strftime("%Y-%m-%d")

            
            df = df[["amount", "base_currency", "date", "currency", "exchange_rate"]]
            logging.info(f"Data flattened successfully for date: {date.strftime('%Y-%m-%d')}")
            print(f"Data flattened successfully for date: {date.strftime('%Y-%m-%d')}")

            
            month_folder_path = os.path.join(config_data["flattened_data_folder_path"],f"year_{date.year}",f"{date.strftime('%B')}")

            os.makedirs(month_folder_path,exist_ok=True)

            file_name = f"{datetime.strftime(date, "%Y-%m-%d")}.csv"
    
            file_path = os.path.join(month_folder_path,file_name)

            df.to_csv(file_path, index = False)

            logging.info(f"Flattened data saved to {file_name} in {config_data['flattened_data_folder_path']} folder.")
            print(f"Flattened data saved to {file_name} in {config_data['flattened_data_folder_path']} folder.")

    return None