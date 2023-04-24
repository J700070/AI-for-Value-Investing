import logging
import sys
from pathlib import Path
from typing import Any, Dict

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sys.path.append(str(Path("Src").joinpath("DataCollection", "modules")))
from read_data import read_stock_tickers_from_file

sys.path.append(str(Path("Src").joinpath("DataPreparation")))
from create_general_data_index import load_json_data


def camel_to_snake(camel_str):
    snake_str = ""
    for index, char in enumerate(camel_str):
        if index > 0 and char.isupper():
            snake_str += "_"
        snake_str += char.lower()
    return snake_str


def process_general_data(ticker: str, data: Dict[str, Any]) -> None:
    logging.info(f"Merging data from {ticker}")

    fundamental_df = create_skeleton_dataframe(ticker, data)
    fundamental_df = add_dividends_data(fundamental_df, data)
    fundamental_df = add_outstanding_shares_data(fundamental_df, data)
    fundamental_df = add_earnings_estimates_data(fundamental_df, data)
    fundamental_df = add_balance_sheet_data(fundamental_df, data)
    fundamental_df = add_cash_flow_data(fundamental_df, data)
    fundamental_df = add_income_statement_data(fundamental_df, data)

    # Remove the 2023 row if it exists
    fundamental_df = fundamental_df[fundamental_df["year"] != 2023]

    # Convert all column names from camelCase to snake_case
    fundamental_df.columns = [camel_to_snake(column) for column in fundamental_df.columns]

    fundamental_df = fundamental_df.astype(str)
    # Save the data to a CSV file
    csv_file_path = Path("Data").joinpath("Tickers", "FinancialsCSV", f"{ticker}_financials.csv")
    fundamental_df.to_csv(csv_file_path, index=False)

    logging.info(f"Saved data for {ticker} to CSV file")


def create_skeleton_dataframe(ticker: str, data: Dict[str, Any]) -> pd.DataFrame:
    dates = list(data["Financials"]["Balance_Sheet"]["yearly"].keys())
    fundamental_df = pd.DataFrame(dates, columns=["date"])
    fundamental_df["ticker"] = ticker
    fundamental_df[["year", "month", "day"]] = fundamental_df["date"].str.split("-", expand=True).astype(int)

    return fundamental_df


def add_dividends_data(df: pd.DataFrame, data: Dict[str, Any]) -> pd.DataFrame:
    dividends_data = data["SplitsDividends"]["NumberDividendsByYear"]
    dividends_df = pd.DataFrame(
        [(int(entry["Year"]), int(entry["Count"])) for entry in dividends_data.values()],
        columns=["year", "dividend_count"]
    )

    return df.merge(dividends_df, how="outer", on="year")


def add_outstanding_shares_data(df: pd.DataFrame, data: Dict[str, Any]) -> pd.DataFrame:
    shares_data = data["outstandingShares"]["annual"]
    shares_df = pd.DataFrame(
        [(int(entry["date"]), int(entry["shares"])) for entry in shares_data.values()],
        columns=["year", "outstanding_shares"]
    )

    return df.merge(shares_df, how="outer", on="year")

def add_income_statement_data(df: pd.DataFrame, data: Dict[str, Any]) -> pd.DataFrame:
    income_data = data["Financials"]["Income_Statement"]["yearly"]
    income_df = pd.DataFrame(income_data).T.reset_index(drop=True)
    income_df["year"] = income_df["date"].str.split("-", expand=True)[0].astype(int)

    # Rename columns
    column_mapping = {
        "date": "income_statement_date",
        "filing_date": "income_statement_filing_date",
        "currency_symbol": "income_statement_currency_symbol"
    }
    income_df.rename(columns=column_mapping, inplace=True)

    return df.merge(income_df, how="outer", on="year")

def add_cash_flow_data(df: pd.DataFrame, data: Dict[str, Any]) -> pd.DataFrame:
    cash_flow_data = data["Financials"]["Cash_Flow"]["yearly"]
    temp_df = pd.DataFrame(cash_flow_data).T.reset_index(drop=True)
    temp_df["year"] = temp_df["date"].str.split("-", expand=True)[0].astype(int)

    # Rename columns
    column_mapping = {
        "date": "cash_flow_date",
        "filing_date": "cash_flow_filing_date",
        "currency_symbol": "cash_flow_currency_symbol"
    }
    temp_df.rename(columns=column_mapping, inplace=True)

    return df.merge(temp_df, how="outer", on="year")

def add_balance_sheet_data(df: pd.DataFrame, data: Dict[str, Any]) -> pd.DataFrame:
    balance_sheet_data = data["Financials"]["Balance_Sheet"]["yearly"]
    temp_df = pd.DataFrame(balance_sheet_data).T.reset_index(drop=True)
    temp_df["year"] = temp_df["date"].str.split("-", expand=True)[0].astype(int)

    # Rename columns
    column_mapping = {
        "date": "balance_sheet_date",
        "filing_date": "balance_sheet_filing_date",
        "currency_symbol": "balance_sheet_currency_symbol"
    }
    temp_df.rename(columns=column_mapping, inplace=True)

    return df.merge(temp_df, how="outer", on="year")

def convert_fundamental_data_to_yearly_csv():
    logging.info("Starting data processing")
    tickers = read_stock_tickers_from_file()

    for ticker in tickers:
        try:
            logging.info(f"Processing data for {ticker}")
            data = load_json_data(ticker, financials=True)
            if data:
                process_general_data(ticker, data)
            else:
                logging.warning(f"No data found for {ticker}")
        except Exception as e:
            logging.error(f"Error processing data for {ticker}: {str(e)}")


if __name__ == "__main__":
    convert_fundamental_data_to_yearly_csv()