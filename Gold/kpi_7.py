import loading_config
import mysql.connector
from logger import logger
import logging

# KPI 7: What is the change in exchange rate between the first and last month of each year for each currency

def kpi_7():
    setup_logger = logger("format_1")
    logging.info("Starting KPI-7 calculation.")

    config_data = loading_config.load_config()
    mydb = mysql.connector.connect(
        host = config_data["host"],
        user = config_data["user"],
        password= config_data["password"],
        database = config_data["database"])
    
    mycursor = mydb.cursor()

    query_1 = f"""
    CREATE TABLE IF NOT EXISTS kpi_7_results (
    currency VARCHAR(3),
    year INT,
    avg_rate_jan FLOAT,
    avg_rate_dec FLOAT,
    change_value FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}',
    updated_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}'
    );
    """

    
    query_2 = """
    INSERT INTO kpi_7_results
    (currency, year, avg_rate_jan, avg_rate_dec, change_value)

    WITH jan_avg AS (
    SELECT 
        currency,
        YEAR(date) AS year,
        AVG(exchange_rate) AS avg_rate_jan
    FROM currency_exchange_rate
    WHERE MONTH(date) = 1
    AND YEAR(date) < YEAR(CURDATE())
    GROUP BY currency, YEAR(date)
    ),

    dec_avg AS (
    SELECT 
        currency,
        YEAR(date) AS year,
        AVG(exchange_rate) AS avg_rate_dec
    FROM currency_exchange_rate
    WHERE MONTH(date) = 12
    AND YEAR(date) < YEAR(CURDATE())
    GROUP BY currency, YEAR(date)
    )

    SELECT 
        j.currency,
        j.year,
        j.avg_rate_jan,
        d.avg_rate_dec,
        ROUND((d.avg_rate_dec - j.avg_rate_jan), 4) AS change_value
    FROM jan_avg j
    INNER JOIN dec_avg d
    ON j.currency = d.currency
    AND j.year = d.year;
    """
    
    mycursor.execute(query_1)
    mycursor.execute("TRUNCATE TABLE kpi_7_results")
    mycursor.execute(query_2)
    mydb.commit()
    logging.info("KPI-7 is successfully created.")
    print("KPI-7 is successfully created.")