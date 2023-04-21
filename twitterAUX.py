import requests
import os
import json
import csv
from io import StringIO
import pandas as pd
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI


# Open Data/exchanges.json
def read_exchanges_from_file(file_name='Data/exchanges.json'):
    with open(file_name, 'r') as file:
        content = file.read()
        if content.strip():
            exchanges = json.loads(content)
        else:
            raise ValueError(f"File {file_name} is empty or contains invalid JSON.")
    return exchanges

# Open Data/listed_ticker_by_exchange.json
def read_listed_tickers_from_file(file_name='Data/listed_tickers_by_exchange.json'):
    with open(file_name, 'r') as file:
        content = file.read()
        if content.strip():
            tickers = json.loads(content)
        else:
            raise ValueError(f"File {file_name} is empty or contains invalid JSON.")
    return tickers

# Open Data/delisted_tickers_by_exchange.json
def read_delisted_tickers_from_file(file_name='Data/delisted_tickers_by_exchange.json'):
    with open(file_name, 'r') as file:
        content = file.read()
        if content.strip():
            delisted_tickers = json.loads(content)
        else:
            raise ValueError(f"File {file_name} is empty or contains invalid JSON.")
    return delisted_tickers

def count_tickers():
    sum = 0
    tickers = read_listed_tickers_from_file()
    print("Ticker count:", len(tickers))
    for exchange in tickers:
        print(f"{exchange}: {len(tickers[exchange])}")
        sum += len(tickers[exchange])
    
    print("Sum of delisted tickers:", sum)


def main():
    # count_tickers()
    df = pd.read_csv("Data/tickers.csv")
    

    


if __name__ == '__main__':
    main()
