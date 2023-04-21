import logging
from io import StringIO

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_exchanges(api_token):
    url = f'https://eodhistoricaldata.com/api/exchanges-list/?api_token={api_token}&fmt=json'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise requests.exceptions.RequestException(f'Error: {response.status_code}')

def fetch_country_macro_data(api_token, country, indicator):
    url = f'https://eodhistoricaldata.com/api/macro-indicator/{country}?api_token={api_token}&fmt=json&indicator={indicator}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_exchange_tickers(api_token, exchange_code, delisted=0):
    url = f'https://eodhistoricaldata.com/api/exchange-symbol-list/{exchange_code}?api_token={api_token}&delisted={delisted}'
    response = requests.get(url)

    if response.status_code == 200:
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        tickers = df.to_dict('records')
        return tickers
    else:
        raise requests.exceptions.RequestException(f'Error {response.status_code} for exchange {exchange_code}')

def fetch_stock_fundamental_data(api_token, ticker):
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token={api_token}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_stock_ticker_price(api_token, ticker):
    url = f'https://eodhistoricaldata.com/api/eod/{ticker}?api_token={api_token}&period=m'
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def fetch_stock_tickers(api_token, ticker):
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

def fetch_stock_sentiment_data(api_token, source, all_tickers):
    logging.info(f"Fetching stock sentiment data for source {source}")
    if source not in {"news", "tweets"}:
        logging.error(f"Invalid source {source}")
        raise ValueError(f"Invalid source {source}")
    
    url = f'https://eodhistoricaldata.com/api/{source+"-" if source == "tweets" else ""}sentiments?s={",".join(all_tickers)}&api_token={api_token}'
    response = requests.get(url)
    response.raise_for_status()

    logging.info(f"Finished fetching stock sentiment data for source {source}")
    return response.json() 
