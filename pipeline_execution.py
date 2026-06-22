from Bronze import fetch_data

from Bronze import saving_new_raw_data_to_files
import logger
from Silver import flattened
from Silver import dq_rules
from Gold import clean_data_table, kpi
from datetime import datetime
import logging
import time



def pipeline_execution(start_date, end_date, trigger):

    setup_logger_1 = logger.logger(' ')
    try:
        
        print(f"Starting the ETL pipeline and the trigger: {trigger}.")
        logging.info(f"Starting the ETL pipeline and the trigger: {trigger}.")

        # Bronze Layer;
        new_raw_data_path, metadata = fetch_data.fetch_data(start_date, end_date)
        if new_raw_data_path is None or metadata is None:
            print("Data fetching failed. Exiting the ETL pipeline.")
            logging.error("Data fetching failed. Exiting the ETL pipeline.")
            return None, None
    

        new_data_dates, amount , base_currency= saving_new_raw_data_to_files.saving_raw_data_to_files(new_raw_data_path, metadata)

        # Silver Layer:
        flattened.flatten_data(new_data_dates, amount , base_currency)
        clean_data_file_path , clean_data_rows_count , error_data_rows_count = dq_rules.rules(new_data_dates)

        if clean_data_file_path is None or clean_data_rows_count == 0:
            print("cleaned data file is empty.")
            logging.error("cleaned data file is empty.")
            return 0, error_data_rows_count
        
        # Gold Layer:
        table = clean_data_table.CleanDataTable()
        table.create_table(clean_data_file_path,primary_keys=["date", "currency"])
        table.insert_rows(clean_data_file_path, primary_keys=["date", "currency"])
        kpi.run_kpis()

        print("Pipeline execution completed.")
        logging.info("Pipeline execution completed.")
        return clean_data_rows_count, error_data_rows_count
    except Exception as error:
        print(f"An error occurred during the ETL pipeline execution: {error}")
        logging.error(f"An error occurred during the ETL pipeline execution: {error}")
        return None , None



# source /Users/akshaya1228/ELT_PROJECT_2/.venv/bin/activate 
# pip install -r requirements.txt 

