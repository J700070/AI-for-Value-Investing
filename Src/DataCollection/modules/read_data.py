import json
import logging

import pandas as pd

from Src.DataCollection.common import check_integrity_of_tickers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_stock_tickers_from_file(file_name='Data/tickers.csv'):
    df = pd.read_csv(file_name, header=0)
    df = df[(df['Type'] == 'Common Stock') | (df['Type'] == 'Preferred Stock')]
    stock_tickers = df["Code"].tolist()
    df["stock_tickers_with_exchange"] = df["Code"] + "." + df["Exchange"]
    df["stock_tickers_with_exchange"] = df["stock_tickers_with_exchange"].str.replace("NYSE", "US")
    df["stock_tickers_with_exchange"] = df["stock_tickers_with_exchange"].str.replace("NASDAQ", "US")
    df["stock_tickers_with_exchange"] = df["stock_tickers_with_exchange"].str.replace("NYSE ARCA", "US")
    df["stock_tickers_with_exchange"] = df["stock_tickers_with_exchange"].str.replace("PINK", "US")
    df["stock_tickers_with_exchange"] = df["stock_tickers_with_exchange"].str.replace("OTC", "US")
    df["stock_tickers_with_exchange"] = df["stock_tickers_with_exchange"].str.replace(".US", "")
    stock_tickers_with_exchange = df["stock_tickers_with_exchange"].tolist()
    check_integrity_of_tickers(stock_tickers)
   
    
    logging.info("Finished reading stock tickers from file")
    return stock_tickers_with_exchange

def read_exchanges_from_file(file_name='Data/Exchanges/exchanges.json'):
    with open(file_name, 'r') as file:
        content = file.read()
        if content.strip():
            exchanges = json.loads(content)
        else:
            raise ValueError(f"File {file_name} is empty or contains invalid JSON.")
    return exchanges

def read_stock_countries_from_file(file_name='Data/Exchanges/exchanges.json'):
    with open(file_name, 'r') as file:
        data = json.load(file)
        countries = [country['CountryISO3'] for country in data if country['CountryISO3'] is not None and country['CountryISO3'] != '']
        # Return unique countries
        return list(set(countries))