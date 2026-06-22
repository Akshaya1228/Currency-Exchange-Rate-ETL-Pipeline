import loading_config
import mysql.connector
from logger import logger
import logging

# KPI 5: Which currency is closest to the base currency value (i.e., closest to 1)?

def kpi_5():

    setup_logger = logger("format_1")
    logging.info("Starting KPI-5 calculation.")

    config_data = loading_config.load_config()
    mydb = mysql.connector.connect(
        host = config_data["host"],
        user = config_data["user"],
        password= config_data["password"],
        database = config_data["database"])
    
    mycursor = mydb.cursor()

    query_1 = f"""
    CREATE TABLE IF NOT EXISTS kpi_5_results (
    currency VARCHAR(3),
    avg_rate FLOAT,
    diff_from_base FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}',
    updated_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}'
    );"""

    query_2 = """
    INSERT INTO kpi_5_results (currency, avg_rate, diff_from_base)

    SELECT 
        currency,
        AVG(exchange_rate) AS avg_rate,
        ABS(AVG(exchange_rate) - 1) AS diff_from_base
    FROM currency_exchange_rate
    WHERE YEAR(date) = YEAR(CURDATE())
    AND MONTH(date) = MONTH(CURDATE())
    GROUP BY currency
    ORDER BY diff_from_base ASC
    LIMIT 1;
    """
    
    mycursor.execute(query_1)
    mycursor.execute("TRUNCATE TABLE kpi_5_results")
    mycursor.execute(query_2)
    mydb.commit()
    logging.info("KPI-5 is successfully created.")
    print("KPI-5 is successfully created.")