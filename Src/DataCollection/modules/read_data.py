import json
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_stock_tickers_from_file(file_name='Data/tickers.csv'):
    df = pd.read_csv(file_name, header=0)
    
    df = df[(df['Type'] == 'Common Stock') | (df['Type'] == 'Preferred Stock')]
    stock_tickers = df["Code"].tolist()
    
    

    logging.info("Verifying if all SP500 companies are in the list of stock tickers")
    sp500_companies = pd.read_csv("Data/Indexes/sp500_companies.csv", header=0)["Symbol"].to_list()

    for company in sp500_companies:
        company = company.replace(".", "-")
        if company not in stock_tickers:
            logging.error(f"SP500 company {company} not in list of stock tickers")
            raise ValueError(f"SP500 company {company} not in list of stock tickers")
        
    logging.info("Verifying if all Nasdaq100 companies are in the list of stock tickers")
    nasdaq100_companies = pd.read_csv("Data/Indexes/nasdaq100_companies.csv", header=0)["Symbol"].to_list()

    for company in nasdaq100_companies:
        company = company.replace(".", "-")
        if company not in stock_tickers:
            logging.error(f"Nasdaq100 company {company} not in list of stock tickers")
            raise ValueError(f"Nasdaq100 company {company} not in list of stock tickers")
    
        
    logging.info("Finished reading stock tickers from file")
    return stock_tickers

def read_exchanges_from_file(file_name='Data/exchanges.json'):
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