from logger import logger
from Gold import kpi_1 , kpi_2, kpi_3, kpi_4, kpi_5, kpi_6, kpi_7
import logging

def run_kpis():
    setup_logger = logger("format_1")
    logging.info("Starting KPI calculations.")

    kpi_1.kpi_1()
    kpi_2.kpi_2()
    kpi_3.kpi_3()
    kpi_4.kpi_4()
    kpi_5.kpi_5()
    kpi_6.kpi_6()
    kpi_7.kpi_7()
    
    logging.info("All KPIs have been calculated and stored in the database.")