import json
import sys

import requests

sys.path.append("C:\\Users\\juani\\Desktop\\AI-for-Value-Investing")

from Src.DataCollection.common import get_api_key
from Src.DataCollection.modules.fetch_data import fetch_exchanges


def save_exchanges_to_file(exchanges, file_name='Data/Exchanges/exchanges.json'):
    with open(file_name, 'w') as file:
        json.dump(exchanges, file, indent=4)

def fetch_and_save_exchanges():
    try:
        api_token = get_api_key()
        exchanges = fetch_exchanges(api_token)
        save_exchanges_to_file(exchanges)
    except requests.exceptions.RequestException as e:
        print(e)



