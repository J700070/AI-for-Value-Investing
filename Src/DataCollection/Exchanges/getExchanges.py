import json

import requests

from Src.DataCollection.common import get_api_key
from Src.DataCollection.modules.fetch_data import fetch_exchanges


def save_exchanges_to_file(exchanges, file_name='exchanges.json'):
    with open(file_name, 'w') as file:
        json.dump(exchanges, file, indent=4)

def main():
    try:
        api_token = get_api_key()
        exchanges = fetch_exchanges(api_token)
        save_exchanges_to_file(exchanges)
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == '__main__':
    main()
