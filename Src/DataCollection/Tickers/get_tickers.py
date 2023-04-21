import json

import requests

from Src.DataCollection.common import get_api_key
from Src.DataCollection.modules.fetch_data import fetch_exchange_tickers
from Src.DataCollection.modules.read_data import read_exchanges_from_file


def get_tickers():
    api_token = get_api_key()
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
                listed_tickers = fetch_exchange_tickers(api_token, exchange_code, delisted=0)
                listed_tickers_by_exchange[exchange_code] = listed_tickers
                print(f"Successfully fetched listed tickers for exchange {exchange_code}")
            except requests.exceptions.RequestException as e:
                print(e)

            # Fetch delisted tickers
            print(f"Fetching delisted tickers for exchange {exchange_code}")
            try:
                delisted_tickers = fetch_exchange_tickers(api_token, exchange_code, delisted=1)
                delisted_tickers_by_exchange[exchange_code] = delisted_tickers
                print(f"Successfully fetched delisted tickers for exchange {exchange_code}")
            except requests.exceptions.RequestException as e:
                print(e)

        # Save listed tickers
        with open('Data/listed_tickers_by_exchange.json', 'w') as file:
            json.dump(listed_tickers_by_exchange, file, indent=4)
        print("Saved listed tickers to 'Data/listed_tickers_by_exchange.json'")

        # Save delisted tickers
        with open('Data/delisted_tickers_by_exchange.json', 'w') as file:
            json.dump(delisted_tickers_by_exchange, file, indent=4)
        print("Saved delisted tickers to 'Data/delisted_tickers_by_exchange.json'")

    except (requests.exceptions.RequestException, ValueError) as e:
        print(e)

if __name__ == '__main__':
    get_tickers()
