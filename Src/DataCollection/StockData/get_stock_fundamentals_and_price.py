
import json
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import requests

sys.path.append("C:\\Users\\juani\\Desktop\\AI-for-Value-Investing")

from Src.DataCollection.common import get_api_key
from Src.DataCollection.modules.fetch_data import fetch_stock_fundamental_data, fetch_stock_ticker_price
from Src.DataCollection.modules.read_data import read_stock_tickers_from_file
from Src.Utils.ascii import bcolors

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_stock_ticker(api_token, ticker):
    general_path = f'Data/Tickers/General/{ticker}_general.json'
    financials_path = f'Data/Tickers/Financials/{ticker}_financials.json'
    price_path = f'Data/Tickers/Price/{ticker}_price.csv'


    try:
        logging.info(f"Fetching fundamental data for ticker {ticker}...")

        if not os.path.exists(general_path) or not os.path.exists(financials_path):
            fundamental_data = fetch_stock_fundamental_data(api_token, ticker)

            general_keys = ['General', 'Highlights', 'Valuation', 'SharesStats', 'Technicals', 'SplitsDividends', 'AnalystRatings', 'Holders', 'InsiderTransactions']
            financials_keys = ["SplitsDividends",'outstandingShares', 'Earnings', 'Financials']

            general = {key: fundamental_data.get(key, {}) for key in general_keys}
            financials = {key: fundamental_data.get(key, {}) for key in financials_keys}

            with open(f'Data/Tickers/General/{ticker}_general.json', 'w') as outfile:
                json.dump(general, outfile)

            with open(f'Data/Tickers/Financials/{ticker}_financials.json', 'w') as outfile:
                json.dump(financials, outfile)

            logging.info(f"Successfully fetched fundamental data for ticker {ticker}")
        else :
            logging.info(f"Fundamental data for ticker {ticker} already fetched")

        logging.info(f"Fetching price data for ticker {ticker}...")

        if not os.path.exists(price_path):
            price_data = fetch_stock_ticker_price(api_token, ticker)
            # Write the price data to a csv file
            with open(f'Data/Tickers/Price/{ticker}_price.csv', 'w') as outfile:
                outfile.write(price_data)
            logging.info(f"Successfully fetched price data for ticker {ticker}")
        else:
            logging.info(f"Price data for ticker {ticker} already fetched")

    except requests.exceptions.RequestException as e:
        logging.error(bcolors.FAIL + f"Error fetching fundamental data for ticker {ticker}: {e}" + bcolors.ENDC )
        # Add the ticker to the file of failed tickers "failed_tickers.txt" appending it to the end of the file
        with open("Data/Tickers/failed_tickers.txt", "a") as failed_tickers_file:
            failed_tickers_file.write(f"{ticker} - {e} \n")



def fetch_stocks_data():
    api_token = get_api_key()
    stock_tickers = read_stock_tickers_from_file()
    logging.info("Fetched stock tickers from file")

    with ThreadPoolExecutor() as executor:
        for ticker in stock_tickers:
            executor.submit(process_stock_ticker, api_token, ticker).result()
    

        

if __name__ == '__main__':
    fetch_stocks_data()
    