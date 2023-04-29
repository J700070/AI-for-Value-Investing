import json
import logging
import sys

import pandas as pd
import requests

sys.path.append("C:\\Users\\juani\\Desktop\\AI-for-Value-Investing")
from Src.DataCollection.modules.fetch_data import fetch_exchange_tickers
from Src.DataCollection.modules.read_data import read_exchanges_from_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_tickers():
    listed_tickers_file = "Data/listed_tickers_by_exchange.json"
    delisted_tickers_file = "Data/delisted_tickers_by_exchange.json"
    output_file = "Data/merged_tickers_by_exchange.json"
    csv_output_file = "Data/tickers.csv"

    try:
        exchanges = read_exchanges_from_file()
        print("Fetched exchanges from file")

        listed_tickers_by_exchange = {}
        delisted_tickers_by_exchange = {}
        for exchange in exchanges:
            exchange_code = exchange['Code']
            
            # Fetch listed tickers
            print(f"Fetching listed tickers for exchange {exchange_code}")
            try:
                listed_tickers = fetch_exchange_tickers(exchange_code, delisted=0)
                listed_tickers_by_exchange[exchange_code] = listed_tickers
                print(f"Successfully fetched listed tickers for exchange {exchange_code}")
            except requests.exceptions.RequestException as e:
                print(e)

            # Fetch delisted tickers
            print(f"Fetching delisted tickers for exchange {exchange_code}")
            try:
                delisted_tickers = fetch_exchange_tickers( exchange_code, delisted=1)
                delisted_tickers_by_exchange[exchange_code] = delisted_tickers
                print(f"Successfully fetched delisted tickers for exchange {exchange_code}")
            except requests.exceptions.RequestException as e:
                print(e)

        # Save listed tickers
        with open(listed_tickers_file, 'w') as file:
            json.dump(listed_tickers_by_exchange, file, indent=4)
        print(f"Saved listed tickers to '{listed_tickers_file}'")

        # Save delisted tickers
        with open(delisted_tickers_file, 'w') as file:
            json.dump(delisted_tickers_by_exchange, file, indent=4)
        print(f"Saved delisted tickers to '{delisted_tickers_file}'")

        # Merge listed and delisted tickers
        merged_tickers = merge_listed_and_delisted_tickers(listed_tickers_by_exchange, delisted_tickers_by_exchange)
        save_merged_tickers_to_json(merged_tickers, output_file)
        print(f"Merged tickers saved to {output_file}")

        format_tickers_to_csv(merged_tickers, csv_output_file)

    except (requests.exceptions.RequestException, ValueError) as e:
        print(e)

def merge_listed_and_delisted_tickers(listed_tickers, delisted_tickers):
    merged_tickers = {}
    
    for exchange, tickers in listed_tickers.items():
        if exchange not in merged_tickers:
            merged_tickers[exchange] = []
        for ticker in tickers:
            merged_tickers[exchange].append({
                'ticker': ticker,
                'delisted': False
            })

    for exchange, tickers in delisted_tickers.items():
        if exchange not in merged_tickers:
            merged_tickers[exchange] = []
        for ticker in tickers:
            merged_tickers[exchange].append({
                'ticker': ticker,
                'delisted': True
            })

    return merged_tickers


def save_merged_tickers_to_json(merged_tickers, output_file):
    with open(output_file, 'w') as f:
        json.dump(merged_tickers, f, indent=2)

def format_tickers_to_csv(json_data, output_file):

    if json_data is None:
        logging.error("Could not read JSON data.")
        return

    tickers = []

    for exchange, ticker_list in json_data.items():
        for ticker_obj in ticker_list:
            ticker = ticker_obj['ticker']
            tickers.append({
                'Code': ticker['Code'],
                'Name': ticker['Name'],
                'Country': ticker['Country'],
                'Exchange': ticker['Exchange'],
                'Currency': ticker['Currency'],
                'Type': ticker['Type'],
                'Isin': ticker['Isin'],
                'Delisted': ticker_obj['delisted'],
            })

    header = ['Code', 'Name', 'Country', 'Exchange', 'Currency', 'Type', 'Isin', 'Delisted']
    write_csv_file(output_file, tickers, header)

def write_csv_file(file_path, data, header):
    try:
        df = pd.DataFrame(data, columns=header)
        df.to_csv(file_path, index=False, encoding='utf-8')
        logging.info(f"CSV file saved to {file_path}")
    except IOError:
        logging.error(f"Error writing to file {file_path}")  



if __name__ == '__main__':
    get_tickers()
