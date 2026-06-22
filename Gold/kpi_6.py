import loading_config
import mysql.connector
from logger import logger
import logging

# KPI 6: What is the year over year percentage change in exchange rate for each currency?

def kpi_6():
    setup_logger = logger("format_1")
    logging.info("Starting KPI-6 calculation.")

    config_data = loading_config.load_config()
    mydb = mysql.connector.connect(
        host = config_data["host"],
        user = config_data["user"],
        password= config_data["password"],
        database = config_data["database"])
    
    mycursor = mydb.cursor()

    query_1 = f"""
    CREATE TABLE IF NOT EXISTS kpi_6_results (
    currency VARCHAR(3),
    year INT,
    avg_rate FLOAT,
    prev_year_avg_rate FLOAT,
    percentage_change FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}',
    updated_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}'
    );
    """

    
    query_2 = """
    INSERT INTO kpi_6_results
    (currency, year, avg_rate, prev_year_avg_rate, percentage_change)

    WITH yearly_avg AS (
    SELECT 
        currency,
        YEAR(date) AS year,
        AVG(exchange_rate) AS avg_rate
    FROM currency_exchange_rate
    GROUP BY currency, YEAR(date)
    ),

    yearly_with_prev AS (
    SELECT 
        currency,
        year,
        avg_rate,
        LAG(avg_rate) OVER (
            PARTITION BY currency 
            ORDER BY year
        ) AS prev_year_avg_rate
    FROM yearly_avg
    )

    SELECT 
        currency,
        year,
        avg_rate,
        prev_year_avg_rate,
        (((avg_rate - prev_year_avg_rate) / NULLIF(prev_year_avg_rate, 0)) * 100
        ) AS percentage_change
    FROM yearly_with_prev
    WHERE prev_year_avg_rate IS NOT NULL;
    """
    
    mycursor.execute(query_1)
    mycursor.execute("TRUNCATE TABLE kpi_6_results")
    mycursor.execute(query_2)
    mydb.commit()
    logging.info("KPI-6 is successfully created.")
    print("KPI-6 is successfully created.")