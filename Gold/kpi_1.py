import loading_config
import mysql.connector
from logger import logger
import logging

# KPI 1: Which currency is the Strongest and weakest currency in each year?

def kpi_1():
    setup_logger = logger("format_1")
    logging.info("Starting KPI-1 calculation.")

    config_data = loading_config.load_config()
    mydb = mysql.connector.connect(
        host = config_data["host"],
        user = config_data["user"],
        password= config_data["password"],
        database = config_data["database"])
    
    mycursor = mydb.cursor()

    query_1 = f""" CREATE TABLE IF NOT EXISTS kpi_1_results (
                    amount INT,
                    base_currency VARCHAR(3),
                    year INT ,
                    date DATETIME,
                    currency VARCHAR(3),
                    exchange_rate FLOAT,
                    category ENUM('Weakest','Strongest'),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    created_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}',
                    updated_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}'
                    );
                    """
    query_2 = """
                INSERT INTO kpi_1_results
                (amount , base_currency , year , date , currency, exchange_rate ,category)
                    SELECT e.amount, e.base_currency , m.year , e.date ,  e.currency, e.exchange_rate ,
                            'Weakest' AS category
                    FROM currency_exchange_rate AS e
                    INNER JOIN (
                                SELECT YEAR(date) AS year, 
                                        MAX(exchange_rate) AS exchange_rate
                                FROM currency_exchange_rate
                                GROUP BY YEAR(date)
                                ) AS m
                    ON YEAR(e.date) = m.year
                    AND e.exchange_rate = m.exchange_rate
                    
                    UNION ALL
                    
                    SELECT e.amount, e.base_currency , m.year , e.date ,  e.currency, e.exchange_rate ,
                        'Strongest' AS category
                    FROM currency_exchange_rate AS e
                    INNER JOIN (
                            SELECT YEAR(date) AS year, 
                                    MIN(exchange_rate) AS exchange_rate
                            FROM currency_exchange_rate
                            GROUP BY YEAR(date)
                            ) AS m
                    ON YEAR(e.date) = m.year
                        AND 
                        e.exchange_rate = m.exchange_rate;
                """
    
    mycursor.execute(query_1)
    mycursor.execute("TRUNCATE TABLE kpi_1_results")
    mycursor.execute(query_2)
    mydb.commit()
    logging.info("KPI-1 is successfully created.")
    print("KPI-1 is successfully created.")