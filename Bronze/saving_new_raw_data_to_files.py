import json
import os
import loading_config
from logger import logger
from datetime import datetime
import logging


def saving_raw_data_to_files(raw_data_path, metadata):

    setup_logger = logger("format_1")

    with open(raw_data_path, "r") as f:
        config_data = loading_config.load_config()
        raw_data = json.load(f)

        print(f"Raw data loaded successfully from the file new_raw_data.json.")
        logging.info(f"Raw data loaded successfully from the file new_raw_data.json.")

        
        amount = raw_data["amount"]
        base_currency = raw_data["base"]
        rates = raw_data["rates"]
        dates = []
        

        for date , rows in rates.items():
            file_metadata = metadata.copy()
            file_metadata["file_date"] = datetime.strptime(date,"%Y-%m-%d").strftime("%Y-%m-%d")
            file_metadata["currency_codes"] = list(rows.keys())
            file_metadata["count_of_currencies"] = len(file_metadata["currency_codes"])

            date = datetime.strptime(date,"%Y-%m-%d")
            dates.append(date)

            file_name = f"{datetime.strftime(date, '%Y-%m-%d')}.json"

            month_folder_path = os.path.join(config_data["historic_data_folder_path"],f"year_{date.year}",f"{date.strftime("%B")}")
            
            os.makedirs(month_folder_path,exist_ok=True)

            file_path = os.path.join(month_folder_path,file_name)

            final_data = {"file_metadata": file_metadata, "data" : rows}


            with open(file_path, "w") as f:
                json.dump(final_data,f)
                logging.info(f"{file_name} is saved to Historic_raw_data folder and the currencies got are {file_metadata['count_of_currencies']}.")
                print(f"{file_name} is saved to Historic_raw_data folder and the currencies got are {file_metadata['count_of_currencies']}.")

    return dates, amount , base_currency 