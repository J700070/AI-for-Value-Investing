import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor

import requests

from Src.DataCollection.common import get_api_key
from Src.DataCollection.modules.fetch_data import (fetch_stock_sentiment_data,
                                                   fetch_stock_tickers)
from Src.DataCollection.modules.read_data import read_stock_tickers_from_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_stock(api_token, stock):
    logging.info(f"Fetching sentiment data for stock {stock}")

    news_path = f'Data/Tickers/Sentiment/News/{stock}_sentiment_news.json'
    tweets_path = f'Data/Tickers/Sentiment/Tweets/{stock}_sentiment_tweets.json'

    if os.path.exists(news_path) and os.path.exists(tweets_path):
        logging.info(f"Sentiment data for stock {stock} already exists")
        return

    try:
        sentiment_data = {}
        
        all_tickers = fetch_stock_tickers(api_token, stock)

        sentiment_data["News"] = fetch_stock_sentiment_data(api_token, "news", all_tickers)

        with open(news_path, 'w') as file:
            json.dump(sentiment_data["News"], file)


        logging.info(f"Succesfully fetched sentiment data for stock {stock}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching sentiment data for stock {stock}: {e}")

def main():
    api_token = get_api_key()
    stock_list = read_stock_tickers_from_file()
    logging.info("Fetched list of stock tickers")

    with ThreadPoolExecutor() as executor:
        [executor.submit(process_stock, api_token, stock) for stock in stock_list]

if __name__ == '__main__':
    main()   