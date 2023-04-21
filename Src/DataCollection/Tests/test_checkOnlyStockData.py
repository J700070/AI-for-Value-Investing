import os
import json
import pandas as pd

def test_checkOnlyStockData():
    # Read all file names in "Data/Tickers/General"
    file_names = os.listdir("Data/Tickers/General")

    # Open "Data/tickers.csv" and read all tickers (header is first row) (index is the "Code" column)
    tickers = pd.read_csv("Data/tickers.csv", header=0, index_col="Code")
    
    # For each file_name in file_names check if the ticker is in the "tickers" dataframe
    # and if its "Type" contains the word "Stock"
    for file_name in file_names:
        ticker = file_name.split("_")[0]

        try:
            assert ticker in tickers.index, f"Ticker {ticker} not found in tickers.csv"
            assert "Stock" in tickers.loc[ticker]["Type"], f"Ticker {ticker} is not a stock" + str(tickers.loc[ticker]["Type"])
        except AssertionError as e:
            print(e)
            if "is not a stock" in str(e):
                file_path = os.path.join("Data/Tickers/General", file_name)
                os.remove(file_path)
                file_path = os.path.join("Data/Tickers/Financials", file_name)
                try:
                     os.remove(file_path)
                except FileNotFoundError:
                    pass
                print(f"Deleted file: {file_path}")

    # Do the same for "Data/Tickers/Financials"
    file_names = os.listdir("Data/Tickers/Financials")

    for file_name in file_names:
        ticker = file_name.split("_")[0]

        try:
            assert ticker in tickers.index, f"Ticker {ticker} not found in tickers.csv"
            assert "Stock" in tickers.loc[ticker]["Type"], f"Ticker {ticker} is not a stock"
        except AssertionError as e:
            print(e)
            if "is not a stock" in str(e):
                file_path = os.path.join("Data/Tickers/Financials", file_name)
                os.remove(file_path)
                print(f"Deleted file: {file_path}")




if __name__ == '__main__':
    test_checkOnlyStockData()
