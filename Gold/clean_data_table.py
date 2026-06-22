
from logger import logger
import pandas as pd
import mysql.connector
import loading_config 
import logging
from Gold import data_type

class CleanDataTable:
    def __init__(self):
        setup_logger = logger("format_1")
        config_data = loading_config.load_config()
        self.config_data = config_data
        self.mydb = mysql.connector.connect(
            host = config_data["host"],
            user = config_data["user"],
            password= config_data["password"])
        
        self.cursor = self.mydb.cursor()

        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config_data['database']}")

        self.mydb.database = self.config_data["database"]

        logging.info(f"Using {self.config_data["database"]} Database.")
        print(f"Using {self.config_data["database"]} Database.")

    def create_table(self, cleaned_file_path, primary_keys):
        
        df = pd.read_csv(cleaned_file_path)
        
        columns_name = list(df.columns)
        
        data_types = data_type.df_to_mysql_data_type_conversion(list(df.dtypes))

        columns_data_types=",".join(f'{col} {t}' for col, t in zip(columns_name, data_types))
       
        primary_key_str = ','.join(f'{key}' for key in primary_keys)

        final_primary_key = f", PRIMARY KEY ({primary_key_str})"

        audit_columns = f"""
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        created_by VARCHAR(255) DEFAULT '{self.config_data["project_runner"]}',
        updated_by VARCHAR(255) DEFAULT '{self.config_data["project_runner"]}'
        """

        self.cursor.execute(f"USE {self.config_data["database"]}")

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.config_data["table_name"]} ( {columns_data_types} , {audit_columns} {final_primary_key})")

        self.mydb.commit()

        logging.info(f"{self.config_data["table_name"]} table created successfully and got committed.")
        print(f"{self.config_data["table_name"]} table created successfully and got committed.")


    def insert_rows(self, cleaned_data_path, primary_keys):

        df = pd.read_csv(cleaned_data_path)
        columns_name = list(df.columns)
        columns_str = ", ".join(f"`{c}`" for c in columns_name)
        values_str = ", ".join(["%s"] * len(columns_name))

        non_primary_key_columns  = [col for col in columns_name if col not in primary_keys]

        update_str = ", ".join(f"`{col}` = VALUES(`{col}`)" for col in non_primary_key_columns)

        insert_query = f""" INSERT INTO {self.config_data["table_name"]} 
                            ({columns_str}) VALUES({values_str})
                            ON DUPLICATE KEY UPDATE 
                            {update_str};
                        """
        
        for index, row in df.iterrows():
            self.cursor.execute(insert_query, list(row.values))
        logging.info(f"Rows got successfully inserted into {self.config_data["table_name"]}.")
        print(f"Rows got successfully inserted into {self.config_data["table_name"]}.")
        self.mydb.commit()

        
    def close(self):

        self.cursor.close()
        self.mydb.close()

        logging.info("MySQL connection is closed successfully.")
        print("MySQL connection is closed successfully.")
