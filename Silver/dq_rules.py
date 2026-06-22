from datetime import datetime
import os
import pandas as pd
from logger import logger
import loading_config
import csv
import logging

def rules(data_dates):

    setup_logger = logger("format_1")

    clean_data = []
    error_data =[]

    config_data = loading_config.load_config()

    
    for date in data_dates:

        data_path = os.path.join(config_data["flattened_data_folder_path"],f"year_{date.year}",f"{date.strftime("%B")}",f"{date.strftime("%Y-%m-%d")}.csv")

        df = pd.read_csv(data_path)
            
        date = date.strftime("%Y-%m-%d")

        for index, row in df.iterrows():
            error = 0
            error_reason=[]
            valid_date =None
            if row["amount"] != 1.0:
                if pd.isna(row["amount"]):
                    logging.info("Invalid amount.")
                    print("Invalid amount.")
                    error_reason.append("Invalid amount")
                    error += 1
            else:
                try:
                    row["amount"] = float(row["amount"])
                    if row["amount"] != 1.0:
                        row["exchange_rate"] = row["exchange_rate"]/row["amount"]
                        row["amount"]=1.0

                        logging.info("amount value is not equal to 1.0 . The amount got corrected to 1.0 . The exchange rate got updated.")
                        print("amount value is not equal to 1.0 . The amount got corrected to 1.0 . The exchange rate got updated.")
                except:
                    logging.info("Invalid amount.")
                    print("Invalid amount.")

                    error_reason.append("Invalid amount")
                    error += 1
            

            if pd.isna(row["base_currency"]):
                logging.info("Base currency is NULL")
                print("Base currency is NULL")

                error_reason.append("Base currency is NULL")
                error+=1

            elif not isinstance(row["base_currency"],str):
                logging.info("Base currency is not string type.")
                print("Base currency is not string type.")

                error_reason.append("Base currency is not string type.")
                error += 1
        
            elif len(row["base_currency"])!=3:
                logging.info("Length of base currency is not 3.")
                print("Length of base currency is not 3.")

                error_reason.append("Length of base currency is not 3.")
                error+=1

            elif row["base_currency"] != config_data["base_currency"]:
                logging.info(f"Base currency is not {config_data["base_currency"]}")
                print(f"Base currency is not {config_data["base_currency"]}")

                error_reason.append(f"Base currency is not {config_data["base_currency"]}")
                error+=1

        
            if  pd.isna(row["date"]):
                logging.info("Date is Null")
                print("Date is Null")

                error_reason.append("Date is Null")
                error+=1
            elif row["date"] != date:
                logging.info("Date is incorrect. ")
                print("Date is incorrect. ")

                error_reason.append("Date is incorrect. ")
                error+=1
            else:
                try:
                    valid_date = datetime.strptime(row["date"], "%Y-%m-%d")
                except:
                    try:
                        valid_date = pd.to_datetime(row["date"])
                        row["date"] = valid_date.strftime("%Y-%m-%d")

                        logging.info("Date format is incorrect and got corrected")
                        print("Date format is incorrect and got corrected")

                    except:
                        logging.info("Date is invalid.")
                        print("Date is invalid.")

                        error_reason.append(f"Invalid date: {row['date']}")
                        error += 1
    
            if  not pd.isna(valid_date):
                if valid_date > datetime.now() or valid_date < datetime.strptime(config_data["start_date"], "%Y-%m-%d"):
                    logging.info("Date is not in the correct range.")
                    print("Date is not in the correct range.")

                    error_reason.append("Date is not in the correct range.")
                    error+=1

            if pd.isna(row["currency"]):
                logging.info("curreny is NULL")
                print("curreny is NULL")

                error_reason.append( "curreny is NULL")
                error+=1
            elif not isinstance(row["currency"],str):
                logging.info("currency is not string type.")
                print("currency is not string type.")

                error_reason.append("currency is not string type.")
                error+=1
        
            elif len(row["currency"])!=3:
                logging.info("Length of currency is not 3.")
                print("Length of currency is not 3.")

                error_reason.append("Length of currency is not 3.")
                error+=1

            elif row["currency"] not in config_data["currency_names"]:
                logging.info(f"currency is not the currency_names.")
                print(f"currency is not the currency_names.")

                error_reason.append(f"currency is not the currency_names.")
                error +=1                


            if pd.isna(row["exchange_rate"]) :
                logging.info("exchange rate is NULL")
                print("exchange rate is NULL")

                error_reason.append("exchange rate is NULL")
                error+=1
            elif row["exchange_rate"] <= 0:
                logging.info("exchange rate is below 0 or 0.")
                print("exchange rate is below 0 or 0.")

                error_reason.append("exchange rate is below 0 or 0.")
                error+=1
            elif not isinstance(row["exchange_rate"],float):
                try:
                    row["exchange_rate"] = float(row["exchange_rate"])
                    if row["exchange_rate"] <= 0:
                        logging.info("exchange rate is below 0 or 0.")
                        print("exchange rate is below 0 or 0.")

                        error_reason.append("exchange rate is below 0 or 0.")
                        error+=1
                        
                except:
                    logging.info("Invalid exchange rate.")
                    print("Invalid exchange rate.")

                    error_reason.append("Invalid exchange rate")
                    error += 1
        

            if error == 0:
                clean_data.append(row)

            else:
                error_data.append({
                    "date": row.get("date"),
                    "base_currency": row.get("base_currency"),
                    "currency": row.get("currency"),
                    "exchange_rate": row.get("exchange_rate"),
                    "error_reason": ", ".join(error_reason)})
            
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%B")
    date = datetime.now().strftime("%Y-%m-%d")

    cleaned_data_path = f"{config_data['cleaned_data_path']}/cleaned_data/{year}/{month}/{date}"
    error_data_path = f"{config_data['cleaned_data_path']}/error_data/{year}/{month}/{date}"

    os.makedirs(cleaned_data_path, exist_ok=True)
    os.makedirs(error_data_path, exist_ok=True)


    clean_data_name = f"clean_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    error_data_name = f"error_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    clean_data_df = pd.DataFrame(clean_data)
    error_data_df = pd.DataFrame(error_data)



    if len(clean_data_df) == 0:
        logging.info("No clean data found after applying the rules.")
        print("No clean data found after applying the rules.")
        return None, 0, len(error_data_df)
    else:
        clean_data_file_path = os.path.join(cleaned_data_path, clean_data_name)
        clean_data_df.to_csv(clean_data_file_path, index= False)
        logging.info(f"cleaned data is saved to {clean_data_name} in {config_data["cleaned_data_path"]}.")
        print(f"cleaned data is saved to {clean_data_name} in {config_data["cleaned_data_path"]}.")

    if len(error_data_df) == 0:
        logging.info("No error data found after applying the rules.")
        print("No error data found after applying the rules.")
        return clean_data_file_path , len(clean_data_df), 0
    else:
        error_data_file_path = os.path.join(error_data_path,error_data_name)
        error_data_df.to_csv(error_data_file_path, index= False)
        logging.info(f"error data is saved to {error_data_name} in {config_data["cleaned_data_path"]}.")
        print(f"error data is saved to {error_data_name} in {config_data["cleaned_data_path"]}. ")

    return clean_data_file_path , len(clean_data_df),  len(error_data_df)