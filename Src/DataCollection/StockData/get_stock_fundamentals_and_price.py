
import json
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

sys.path.append("C:\\Users\\juani\\Desktop\\AI-for-Value-Investing")

from Src.DataCollection.modules.fetch_data import (
    fetch_stock_fundamental_data, fetch_stock_ticker_price,
    write_ticker_to_failed_tickers)
from Src.DataCollection.modules.read_data import read_stock_tickers_from_file
from Src.Utils.ascii import bcolors

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_stock_ticker(ticker):
 
    if isinstance(ticker, str) and "/" in ticker:
        return

    general_path = f'Data/Tickers/General/{ticker}_general.json'
    financials_path = f'Data/Tickers/Financials/{ticker}_financials.json'
    price_path = f'Data/Tickers/Price/{ticker}_price.csv'


    try:

        if not os.path.exists(general_path) or not os.path.exists(financials_path):
            # Check if the ticker is already in the failed tickers list
            failed_tickers = pd.read_csv('failed_tickers.csv')
            if ticker in failed_tickers['Ticker'].values:
                logging.info(f"Ticker {ticker} is in the failed tickers list. Skipping...")
                return

            logging.info(f"Fetching fundamental data for ticker {ticker}...")

            fundamental_data = fetch_stock_fundamental_data(ticker)
            if fundamental_data is None:
                return
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
            price_data = fetch_stock_ticker_price(ticker)
            if price_data is None:
                return
            # Write the price data to a csv file
            with open(f'Data/Tickers/Price/{ticker}_price.csv', 'w') as outfile:
                outfile.write(price_data)
            logging.info(f"Successfully fetched price data for ticker {ticker}")
        else:
            logging.info(f"Price data for ticker {ticker} already fetched")

    except requests.exceptions.RequestException as e:
        logging.error(bcolors.FAIL + f"Error fetching data for ticker {ticker}: {e}" + bcolors.ENDC )
        write_ticker_to_failed_tickers(ticker)
        



def fetch_stocks_data():
    stock_tickers = read_stock_tickers_from_file()
    logging.info("Fetched stock tickers from file")

    with ThreadPoolExecutor() as executor:
        for ticker in stock_tickers:
            executor.submit(process_stock_ticker, ticker).result()
    

if __name__ == '__main__':
    fetch_stocks_data()
        