import os
import sys
from io import StringIO

import pandas as pd
import requests

sys.path.append("C:\\Users\\juani\\Desktop\\AI-for-Value-Investing")
from Src.DataCollection.modules.fetch_data import (fetch_index_constituents,
                                                   fetch_index_price)

START_DATE = "2000-01-03"
END_DATE = "2023-1-03"
api_token = os.environ.get('EODHD_API_KEY')

def check_data_integrity():
    # Read data
    sp500_tickers_API = fetch_index_constituents("GSPC","INDX")
    sp500_tickers_API = [ticker.replace(".US","") for ticker in sp500_tickers_API]
    sp500_tickers_API = [ticker for ticker in sp500_tickers_API if "_old" not in ticker]

    # Check for price data
    tickers_with_price_data = []
    missing_tickers = []
    for ticker in sp500_tickers_API:
        ticker_file_path = f"Data/Tickers/Price/Purged_prices/{ticker}_price.csv"
        if os.path.isfile(ticker_file_path):
            tickers_with_price_data.append(ticker)
        else:
            missing_tickers.append(ticker)

    print(f"Total number of tickers: {len(sp500_tickers_API)}")
    print(f"Number of tickers with price data: {len(tickers_with_price_data)}")
    print(f"Number of tickers without price data: {len(missing_tickers)}")
    print(f"Tickers without price data: {missing_tickers}")

    return sp500_tickers_API, tickers_with_price_data, missing_tickers

def fetch_custom_index_constituents(index_code,exchange):
    url = f'https://eodhistoricaldata.com/api/fundamentals/{index_code}.{exchange}?api_token={api_token}'
    response = requests.get(url)
    response.raise_for_status()
    components = response.json()["HistoricalTickerComponents"]
    
    columns = ["Start Date","End Date", "Ticker"]
    constituents = pd.DataFrame(columns=columns)
    for listing_index in components:
        constituents.loc[len(constituents)] = [components[listing_index]["StartDate"], components[listing_index]["EndDate"], components[listing_index]["Code"]]

    constituents["Start Date"] = pd.to_datetime(constituents["Start Date"])
    constituents["End Date"] = pd.to_datetime(constituents["End Date"])
    constituents = constituents.sort_values(by="Start Date")

    return  constituents

def get_sp500_components_by_month():
    sp500_tickers_API = fetch_custom_index_constituents("GSPC","INDX")
    
    sp500_tickers_API.sort_values(by="Start Date", inplace=True)

    # Make a dictionary with the dates from the start date to the end date as keys (only year-month) and the tickers wich constitute the index at that moment as values
    sp500_tickers_dict = {}
    for date in pd.date_range(start=START_DATE, end=END_DATE, freq="M"):
        date = date.strftime("%Y-%m")
        sp500_tickers_dict[date] = sp500_tickers_API[(sp500_tickers_API["Start Date"] <= date) & (sp500_tickers_API["End Date"] >= date)]["Ticker"].tolist()

    return sp500_tickers_dict


def replicate_sp500():
    global START_DATE
    global END_DATE 

    sp500_tickers_API, tickers_with_price_data, missing_tickers = check_data_integrity()

    # Open aggregated price data
    all_prices = pd.read_csv("Data/Tickers/Price/Aggregated_prices/all_prices.csv")
    # Filter aggregated price data
    all_prices = all_prices[all_prices["Ticker"].isin(tickers_with_price_data)]


    # We will replicate the SP500 during this period
    # First of all lets check the price of the SP500 during this period by month
    sp500_price_string = fetch_index_price("GSPC", "INDX")
    # Format to csv
    sp500_price_csv = StringIO(sp500_price_string)
    sp500_price = pd.read_csv(sp500_price_csv, header=0)
    # Format date
    sp500_price["Date"] = pd.to_datetime(sp500_price["Date"])
    # Add year, month and day columns
    sp500_price["Year"] = sp500_price["Date"].dt.year
    sp500_price["Month"] = sp500_price["Date"].dt.month
    sp500_price["Day"] = sp500_price["Date"].dt.day


    START_DATE = pd.to_datetime(START_DATE)
    END_DATE = pd.to_datetime(END_DATE)

    # Filter sp500 price data to the period we are interested in
    sp500_price = sp500_price[(sp500_price["Date"] >= START_DATE) & (sp500_price["Date"] <= END_DATE)]
    print(sp500_price.head())
    print(sp500_price.tail())
    # Lets get the CAGR of the SP500 during this period
    # First we need to get the first and last price
    first_price = sp500_price[sp500_price["Date"] == START_DATE]["Adjusted_close"].values[0]
    last_price = sp500_price[sp500_price["Date"] == END_DATE]["Adjusted_close"].values[0]
    # Calculate CAGR
    cagr = (last_price / first_price) ** (1 / (sp500_price.shape[0] / 12)) - 1

    print(f"For the period {START_DATE} to {END_DATE}")
    # Formula for CAGR: (last_price / first_price) ** (1 / (years)) - 1
    print(f"SP500 first price: {first_price}")
    print(f"SP500 last price: {last_price}")
    print(f"SP500 Months: {sp500_price.shape[0]}")
    print(f"SP500 Years: {sp500_price.shape[0] / 12}")

    print(f"SP500 CAGR: {cagr*100}%")


    #  Now lets get the portfolio composition of the SP500 for each year and month
    sp500_tickers_dict = get_sp500_components_by_month()
    
    





if __name__ == "__main__":
    replicate_sp500()