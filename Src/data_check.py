import json
import os

import pandas as pd
from config import TODO_LIST
from Utils.ascii import bcolors
from Utils.utils import print_log


def check_data(path, success_message, failure_message):
    exists = os.path.exists(path)
    if exists:
        print_log(success_message, True)
    else:
        print_log(failure_message, False)
    return exists


def check_country_macro_data():
    if not check_data("Data/macro", "", "[+] Check Macro data folder: NOT OK. Folder not found."):
        return False


    with open("Data/exchanges.json") as f:
        exchanges = json.load(f)
        all_countries = [exchange["CountryISO3"] for exchange in exchanges]

    macro_folder = os.listdir("Data/macro")
    countries_with_data = [country.replace("_macro.json", "") for country in macro_folder]
    missing_countries = set(all_countries) - set(countries_with_data)

    if not missing_countries:
        print_log("[+] Check Macro data: OK", True)
    else:
        num_missing_countries = len(missing_countries)
        num_all_countries = len(all_countries)
        num_found_countries = num_all_countries - num_missing_countries
        percentage = round(((num_found_countries / num_all_countries) * 100), 2)
        message = f"[+] Check Macro data: NOT OK. Data not found for {num_missing_countries} countries. [Completed {num_found_countries}/{num_all_countries} | {percentage}%]"
        print_log(message, False)
        
    return True



def print_todo_list():
    print(bcolors.WARNING + " " + bcolors.ENDC)
    print(bcolors.WARNING + "TODO LIST:" + bcolors.ENDC)
    for todo in TODO_LIST:
        print(bcolors.WARNING + "[-] " + todo + bcolors.ENDC)


def check_exchange_data():
    tasks = []
    tasks.append(check_data("Data/exchanges.json","[+] Check Exchanges data: OK.", "[+] Check Exchanges data: NOT OK. File not found."))

    return tasks

def check_macro_data():
    tasks = []
    tasks.append(check_country_macro_data())

    return tasks

def check_data_collection_status():
    print(bcolors.WARNING + " " + bcolors.ENDC)
    print(bcolors.WARNING + "Checking Data Collection Status" + bcolors.ENDC)


    tasks = []
    tasks.extend(check_exchange_data())
    tasks.extend(check_macro_data())
    tasks.extend(check_ticker_data())
    if all(tasks):
        print_log("Data Collection Status: OK", True)
        return True
    else:
        # Count number of tasks that are not completed
        num_tasks = len(tasks)
        num_completed_tasks = tasks.count(True)
        percentage = round(((num_completed_tasks / num_tasks) * 100), 2)
        message = "NOT OK. "+bcolors.ENDC+ f"[Completed {num_completed_tasks}/{num_tasks} | {percentage}%]"
        print(bcolors.WARNING + "Data Collection Status: " + bcolors.FAIL + message + bcolors.ENDC)
        return False
        

def check_stocks_data():
    tasks = []
    tasks.append(check_stock_data("Price", "[+] Check Stocks price data: {}"))
    tasks.append(check_stock_data("Financials", "[+] Check Stocks Financial data: {}"))
    tasks.append(check_stock_data("General", "[+] Check Stocks General data: {}"))

    return tasks

def check_non_stock_data():
    tasks = []
    return tasks

def check_ticker_data():
    check_data("Data/listed_tickers_by_exchange.json", "","[+] Check Listed Tickers by exchange data: NOT OK. File not found.")
    check_data("Data/delisted_tickers_by_exchange.json", "","[+] Check Delisted Tickers by exchange data: NOT OK. File not found.")
    check_data("Data/merged_tickers_by_exchange.json", "", "[+] Check Merged Tickers by exchange data: NOT OK. File not found.")
    check_data("Data/tickers.csv", "","[+] Check Tickers data (CSV): NOT OK. File not found.")

    tasks = []

    tasks.extend(check_stocks_data())
    tasks.extend(check_non_stock_data())

    return tasks

    
    
def check_stock_data(folder_name, message):
    if not check_data(f"Data/Tickers/{folder_name}", "", message.format("NOT OK. Folder not found.")):
        return False

    tickers_df = pd.read_csv("Data/tickers.csv", header=0)
    tickers_df = tickers_df[(tickers_df['Type'] == 'Common Stock') | (tickers_df['Type'] == 'Preferred Stock')]
    stocks = tickers_df["Code"].tolist()

    folder = os.listdir(f"Data/Tickers/{folder_name}")
    stocks_with_data = [ticker.replace(f"_{folder_name.lower()}.csv", "") for ticker in folder]
    missing_stocks = set(stocks) - set(stocks_with_data)

    if not missing_stocks:
        print_log(message.format("OK"), True)
        return True
    else:
        num_missing_stocks = len(missing_stocks)
        num_all_stocks = len(stocks)
        num_found_stocks = num_all_stocks - num_missing_stocks
        percentage = round(((num_found_stocks / num_all_stocks) * 100), 2)
        print_log(message.format(f"NOT OK. Data not found for all the stocks. [Completed {num_found_stocks}/{num_all_stocks} | {percentage}%]"), False)
        return False
