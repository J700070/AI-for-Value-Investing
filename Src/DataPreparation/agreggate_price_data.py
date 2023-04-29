import logging
import sys
from pathlib import Path
from typing import Any, Dict

import pandas as pd

sys.path.append("C:\\Users\\juani\\Desktop\\AI-for-Value-Investing")
from Src.DataCollection.modules.read_data import read_stock_tickers_from_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_price_data(ticker,data,all_prices):
    data["Date"] = pd.to_datetime(data["Date"])
    data["Year"] = data["Date"].dt.year
    data["Month"] = data["Date"].dt.month
    data["Day"] = data["Date"].dt.day
    data["Ticker"] = ticker
    data = data[["Ticker","Date","Year","Month","Day", "Open", "High", "Low", "Close", "Adjusted_close", "Volume"]]
    all_prices = pd.concat([all_prices, data], ignore_index=True)
    all_prices.to_csv(Path("Data").joinpath("Tickers", "Price", "Aggregated_prices", "all_prices.csv"), index=False)
    logging.info(f"Saved data for {ticker} to CSV file")

    return all_prices

def aggregate_price_data():
    logging.info("Starting data processing")
    tickers = read_stock_tickers_from_file()

    columns = ["Ticker","Date","Year","Month","Day", "Open", "High", "Low", "Close", "Adjusted_close", "Volume"]
    all_prices = pd.DataFrame(columns=columns)
    all_prices["Date"] = pd.to_datetime(all_prices["Date"])


    for ticker in tickers:
        try:
            logging.info(f"Processing data for {ticker}")
            # Load price data from CSV file in "Data/Tickers/Price/Purged_prices/{ticker}_price.csv"
            data = pd.read_csv(Path("Data").joinpath("Tickers", "Price", "Purged_prices", f"{ticker}_price.csv"))
            all_prices = process_price_data(ticker, data,all_prices)
        except Exception as e:
            print(e)
            logging.error(f"Error processing data for {ticker}: {str(e)}")





if __name__ == "__main__":
    aggregate_price_data()