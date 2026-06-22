import loading_config
import mysql.connector
from logger import logger
import logging

# KPI 3: Which currency remained the top-performing currency for the longest consecutive years?

def kpi_3():

    setup_logger = logger("format_1")
    logging.info("Starting KPI-3 calculation.")

    config_data = loading_config.load_config()
    mydb = mysql.connector.connect(
        host = config_data["host"],
        user = config_data["user"],
        password= config_data["password"],
        database = config_data["database"])
    
    mycursor = mydb.cursor()

    query_1 = f""" 
    CREATE TABLE IF NOT EXISTS kpi_3_results (
    currency VARCHAR(3),
    streak_length INT,
    streak_start_year INT,
    streak_end_year INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}',
    updated_by VARCHAR(255) DEFAULT '{config_data["project_runner"]}'
    ); """

    query_2 = """
    INSERT INTO kpi_3_results
    (currency, streak_length, streak_start_year, streak_end_year)

    WITH top_per_year AS (
    SELECT 
        YEAR(e.date) AS year,
        e.currency,
        e.exchange_rate
    FROM currency_exchange_rate e
    INNER JOIN (
        SELECT 
            YEAR(date) AS year,
            MIN(exchange_rate) AS exchange_rate
        FROM currency_exchange_rate
        GROUP BY YEAR(date)
    ) min
    ON YEAR(e.date) = min.year
    AND e.exchange_rate = min.exchange_rate),

    ranked AS (
    SELECT
        year,
        currency,
        exchange_rate,
        DENSE_RANK() OVER (PARTITION BY currency ORDER BY year) AS rn
    FROM top_per_year
    ),

    diff_calculation AS (
    SELECT 
        currency,
        year,
        (year - rn) AS diff
    FROM ranked
    ),

    streaks AS (
    SELECT
        currency,
        diff,
        COUNT(*) AS streak_length,
        MIN(year) AS streak_start_year,
        MAX(year) AS streak_end_year
    FROM diff_calculation
    GROUP BY currency, diff
    ),

    max_streak_per_currency AS (
    SELECT *
    FROM (
        SELECT 
            currency,
            streak_length,
            streak_start_year,
            streak_end_year,
            ROW_NUMBER() OVER (
                PARTITION BY currency
                ORDER BY streak_length DESC, streak_start_year
            ) AS rn
        FROM streaks
    ) t
    WHERE rn = 1
    )

    SELECT 
        currency,
        streak_length,
        streak_start_year,
        streak_end_year
    FROM max_streak_per_currency;
    """
    
    mycursor.execute(query_1)
    mycursor.execute("TRUNCATE TABLE kpi_3_results")
    mycursor.execute(query_2)
    mydb.commit()
    logging.info("KPI-3 is successfully created.")
    print("KPI-3 is successfully created.")