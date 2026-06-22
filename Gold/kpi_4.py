import loading_config
import mysql.connector
from logger import logger
import logging

# KPI 4: What is the average exchange rate for each currency across the dataset?

def kpi_4():
    setup_logger = logger("format_1")
    logging.info("Starting KPI-4 calculation.")

    config_data = loading_config.load_config()
    mydb = mysql.connector.connect(
        host = config_data["host"],
        user = config_data["user"],
        password= config_data["password"],
        database = config_data["database"])
    
    mycursor = mydb.cursor()

    query_1 = f""" 
    CREATE TABLE IF NOT EXISTS kpi_4_results (
    currency VARCHAR(3),
    average_exchange_rate FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}',
    updated_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}'
    ); """

    query_2 = """
    INSERT INTO kpi_4_results (currency, average_exchange_rate)
    SELECT 
        currency,
        AVG(exchange_rate)
    FROM currency_exchange_rate
    GROUP BY currency; """
    
    mycursor.execute(query_1)
    mycursor.execute("TRUNCATE TABLE kpi_4_results")
    mycursor.execute(query_2)
    mydb.commit()
    logging.info("KPI-4 is successfully created.")
    print("KPI-4 is successfully created.")