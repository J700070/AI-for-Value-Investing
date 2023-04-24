import os

import pandas as pd


def check_data_integrity():
    # Read data
    sp500_tickers = pd.read_csv("Data/Indexes/scraped_sp500_tickers.csv", usecols=["Symbol"])
    changes_to_sp500 = pd.read_csv("Data/Indexes/scraped_changes_to_SP500.csv", usecols=["Added Ticker", "Removed Ticker"]).drop(0)

    # Process tickers
    added_tickers = changes_to_sp500["Added Ticker"].tolist()
    removed_tickers = changes_to_sp500["Removed Ticker"].tolist()
    all_tickers = list(set(added_tickers + removed_tickers + sp500_tickers["Symbol"].tolist()))
    all_tickers = [str(ticker).replace(".", "-") for ticker in all_tickers]

    # Check for price data
    tickers_with_price_data = []
    missing_tickers = []
    for ticker in all_tickers:
        ticker_file_path = f"Data/Tickers/Price/{ticker}_price.csv"
        if os.path.isfile(ticker_file_path):
            tickers_with_price_data.append(ticker)
        else:
            missing_tickers.append(ticker)

    print(f"Total number of tickers: {len(all_tickers)}")
    print(f"Number of tickers with price data: {len(tickers_with_price_data)}")
    print(f"Number of tickers without price data: {len(missing_tickers)}")
    print(f"Tickers without price data: {missing_tickers}")

    return all_tickers, tickers_with_price_data, missing_tickers

def replicate_sp500():
    all_tickers, tickers_with_price_data, missing_tickers = check_data_integrity()

    


if __name__ == "__main__":
    replicate_sp500()