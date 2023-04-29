import logging
import os
from io import StringIO

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
api_token = os.environ.get('EODHD_API_KEY')

def fetch_exchanges():
    url = f'https://eodhistoricaldata.com/api/exchanges-list/?api_token={api_token}&fmt=json'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise requests.exceptions.RequestException(f'Error: {response.status_code}')

def fetch_country_macro_data(country, indicator):
    url = f'https://eodhistoricaldata.com/api/macro-indicator/{country}?api_token={api_token}&fmt=json&indicator={indicator}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_exchange_tickers(exchange_code, delisted=0):
    url = f'https://eodhistoricaldata.com/api/exchange-symbol-list/{exchange_code}?api_token={api_token}&delisted={delisted}'
    response = requests.get(url)

    if response.status_code == 200:
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        tickers = df.to_dict('records')
        return tickers
    else:
        raise requests.exceptions.RequestException(f'Error {response.status_code} for exchange {exchange_code}')

def fetch_stock_fundamental_data(ticker):
    try:
        url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token={api_token}'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error fetching fundamental data for {ticker}")
        write_ticker_to_failed_tickers(ticker)

        logging.error(f"Error: {e}")
        return None

def fetch_stock_ticker_price(ticker):
    try:
        url = f'https://eodhistoricaldata.com/api/eod/{ticker}?api_token={api_token}&period=m'
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error fetching price data for {ticker}")
        write_ticker_to_failed_tickers(ticker)

        logging.error(f"Error: {e}")
        return None

def fetch_index_price(ticker, exchange):
    try:
        url = f'https://eodhistoricaldata.com/api/eod/{ticker}.{exchange}?api_token={api_token}&period=m'
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error fetching price data for {ticker}")
        write_ticker_to_failed_tickers(ticker)

        logging.error(f"Error: {e}")
        return None

def fetch_stock_tickers(ticker):
    logging.info(f"Fetching stock tickers for {ticker}")
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token={api_token}'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    stock_tickers = [data["General"]["PrimaryTicker"]]

    for listing_index in data["General"]["Listings"]:
        stock_tickers.append(f'{data["General"]["Listings"][listing_index]["Code"]}.{data["General"]["Listings"][listing_index]["Exchange"]}')

    logging.info(f"Finished fetching stock tickers for {ticker}" )
    return list(set(stock_tickers))

def fetch_stock_sentiment_data(source, all_tickers):
    logging.info(f"Fetching stock sentiment data for source {source}")
    if source not in {"news", "tweets"}:
        logging.error(f"Invalid source {source}")
        raise ValueError(f"Invalid source {source}")
    
    url = f'https://eodhistoricaldata.com/api/{source+"-" if source == "tweets" else ""}sentiments?s={",".join(all_tickers)}&api_token={api_token}'
    response = requests.get(url)
    response.raise_for_status()

    logging.info(f"Finished fetching stock sentiment data for source {source}")
    return response.json() 


def fetch_index_constituents(index_code,exchange):
    url = f'https://eodhistoricaldata.com/api/fundamentals/{index_code}.{exchange}?api_token={api_token}'
    response = requests.get(url)
    response.raise_for_status()
    json_response = response.json()
    constituents = []
    for listing_index in json_response["Components"]:
        constituents.append(f'{json_response["Components"][listing_index]["Code"]}.{json_response["Components"][listing_index]["Exchange"]}')
    
    # Also add hitorical constituents if available
    if "HistoricalTickerComponents" in json_response:
        for listing_index in json_response["HistoricalTickerComponents"]:
            constituents.append(f'{json_response["HistoricalTickerComponents"][listing_index]["Code"]}')


    return constituents





def write_ticker_to_failed_tickers(ticker):
    failed_tickers = pd.read_csv("failed_tickers.csv", header=0)
    failed_tickers.loc[len(failed_tickers)] = [ticker]
    failed_tickers.to_csv("failed_tickers.csv", index=False)
