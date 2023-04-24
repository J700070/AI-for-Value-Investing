import json
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import requests

sys.path.append("C:\\Users\\juani\\Desktop\\AI-for-Value-Investing")
from Src.DataCollection.common import get_api_key, get_macro_indicator_list
from Src.DataCollection.modules.fetch_data import fetch_country_macro_data
from Src.DataCollection.modules.read_data import read_stock_countries_from_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_country(api_token, country):
    logging.info(f"Fetching macro data for country {country}")

    if os.path.exists(f'Data/Macro/{country}_macro.json'):
        logging.info(f"Macro data for country {country} already exists")
        return

    try:
        # Create new json file for country
        macro_data = {}
        
        # Fetch macro data for each indicator
        for indicator in get_macro_indicator_list():
            macro_data[indicator] = fetch_country_macro_data(api_token, country, indicator)

        with open(f'Data/Macro/{country}_macro.json', 'w') as outfile:
            json.dump(macro_data, outfile)
    

        logging.info(f"Successfully fetched macro data for country {country}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching macro data for country {country}: {e}" )

def get_macro_data():
    api_token = get_api_key()
    stock_countries = read_stock_countries_from_file()
    logging.info("Fetched list of stock countries")

    with ThreadPoolExecutor() as executor:
        [executor.submit(process_country, api_token, country) for country in stock_countries]

if __name__ == '__main__':
    get_macro_data()
