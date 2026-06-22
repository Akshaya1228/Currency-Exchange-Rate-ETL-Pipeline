import loading_config
import mysql.connector
from logger import logger
import logging

# KPI 2: For each currency, what is the lowest and Highest exchange rate, and in which year did they occur?

def kpi_2():

    setup_logger = logger("format_1")
    logging.info("Starting KPI-2 calculation.")

    config_data = loading_config.load_config()
    mydb = mysql.connector.connect(
        host = config_data["host"],
        user = config_data["user"],
        password= config_data["password"],
        database = config_data["database"])
    
    mycursor = mydb.cursor()

    query_1 = f""" 
    CREATE TABLE IF NOT EXISTS kpi_2_results (
    amount INT,
    base_currency VARCHAR(3),
    year INT,
    date DATETIME,
    currency VARCHAR(3),
    exchange_rate FLOAT,
    category ENUM('Highest','Lowest'),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}',
    updated_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}'
    ); """

    query_2 = """
    INSERT INTO kpi_2_results
    (amount, base_currency, year, date, currency, exchange_rate, category)
    SELECT 
        e.amount,
        e.base_currency,
        YEAR(e.date) AS year,
        e.date,
        e.currency,
        e.exchange_rate,
        'Highest' AS category
    FROM currency_exchange_rate AS e
    INNER JOIN (
    SELECT currency,
           MAX(exchange_rate) AS exchange_rate
    FROM currency_exchange_rate
    GROUP BY currency
    ) AS max_rate
    ON e.currency = max_rate.currency
    AND e.exchange_rate = max_rate.exchange_rate

    UNION ALL


    SELECT 
        e.amount,
        e.base_currency,
        YEAR(e.date) AS year,
        e.date,
        e.currency,
        e.exchange_rate,
        'Lowest' AS category
    FROM currency_exchange_rate AS e
    INNER JOIN (
    SELECT currency,
           MIN(exchange_rate) AS exchange_rate
    FROM currency_exchange_rate
    GROUP BY currency
    ) AS min_rate
    ON e.currency = min_rate.currency
    AND e.exchange_rate = min_rate.exchange_rate;
    """
    
    mycursor.execute(query_1)
    mycursor.execute("TRUNCATE TABLE kpi_2_results")
    mycursor.execute(query_2)
    mydb.commit()
    logging.info("KPI-2 is successfully created.")
    print("KPI-2 is successfully created.")