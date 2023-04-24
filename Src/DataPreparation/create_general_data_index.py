import json
import logging
import os
import sys

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import logging

sys.path.append("C:\\Users\\juani\\Desktop\\AI-for-Value-Investing")
from Src.DataCollection.modules.read_data import read_stock_tickers_from_file


def determine_gender(officer_name):
    logging.info("Determining gender")
    if "Mr." in officer_name:
        return "Man"
    elif "Ms." in officer_name:
        return "Woman"
    else:
        return "Unknown"


def format_if_sell(amount, transaction_acquired_disposed):
    logging.info("Formatting transaction amount")
    return -amount if transaction_acquired_disposed == "D" else amount

def load_json_data(ticker, financials=False):
    logging.info(f"Loading JSON data for ticker {ticker}")
    if financials:
        file_path = os.path.join("Data", "Tickers", "Financials", f"{ticker}_financials.json")
    else:
        file_path = os.path.join("Data", "Tickers", "General", f"{ticker}_general.json")
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def process_general_data(data):
    logging.info("Processing general data")
    general_data = data["General"]

    keys_to_remove = [
        "Description", "CurrencySymbol", "CountryISO", "ISIN", "LEI", "CUSIP", "CIK",
        "EmployerIdNumber", "Phone", "WebURL", "LogoURL"
    ]

    for key in keys_to_remove:
        general_data.pop(key, None)

    return general_data


def process_listings(general_data):
    logging.info("Processing listings data")
    if "Listings" not in general_data:
        general_data["Listings"] = []
        general_data["NumberOfListing"] = 0
    else:
        listings = [listing["Exchange"] for listing in general_data['Listings'].values()]
        general_data["Listings"] = listings
        general_data["NumberOfListing"] = len(listings)


def process_officers(general_data):
    logging.info("Processing officers data")
    officers_data = general_data.pop("Officers", None)

    if officers_data is not None and len(officers_data) > 0:
        officer_data_list = [
            (
                officer["Name"], officer["Title"], officer["YearBorn"],
                determine_gender(officer["Name"])
            )
            for officer in officers_data.values()
        ]

        officer_names, officer_titles, officer_year_born, officer_genders = zip(*officer_data_list)

        general_data.update({
            "OfficerNames": officer_names,
            "OfficerTitles": officer_titles,
            "OfficerYearBorn": officer_year_born,
            "OfficerGenders": officer_genders
        })


def process_address(general_data):
    logging.info("Processing address data")
    address_data = general_data.pop("AddressData", None)

    if address_data is not None:
        general_data.update(address_data)


def process_splits_dividends(data, general_data):
    logging.info("Processing splits and dividends data")
    splits_dividends = data["SplitsDividends"]

    if len(splits_dividends["NumberDividendsByYear"]) > 0:
        dividend_count_sum = sum(entry["Count"] for entry in splits_dividends["NumberDividendsByYear"].values())
        splits_dividends["NumberDividendsByYear"] = dividend_count_sum / len(splits_dividends["NumberDividendsByYear"])

    general_data.update(splits_dividends)

def process_holders(data, general_data):
    logging.info("Processing holders data")
    

    holders_data = {}
    # Check if there are any holders
    if "Holders" in data and data["Holders"] is not None:
        for holder_type in ("Institutions", "Funds"):
            holder_data = data["Holders"].pop(holder_type, None)

            if holder_data is not None:
                holders_data.update({
                    f"{holder_type}Names": [holder["name"] for holder in holder_data.values()],
                    f"{holder_type}TotalShares": [holder["totalShares"] for holder in holder_data.values()],
                    f"{holder_type}TotalAssets": [holder["totalAssets"] for holder in holder_data.values()],
                    f"{holder_type}CurrentShares": [holder["currentShares"] for holder in holder_data.values()],
                    f"{holder_type}Change": [holder["change"] for holder in holder_data.values()],
                    f"{holder_type}ChangePercentage": [holder["change_p"] for holder in holder_data.values()],
                })

    general_data.update(holders_data)


def process_insider_transactions(data, general_data):
    logging.info("Processing insider transactions")
    insider_transactions = data.pop("InsiderTransactions", None)

    if insider_transactions is not None and len(insider_transactions) > 0:
        transactions_data = [
            (
                transaction["date"],
                format_if_sell(transaction["transactionAmount"], transaction["transactionAcquiredDisposed"]),
                transaction["transactionPrice"]
            )
            for transaction in insider_transactions.values()
        ]

        transactions_date, transactions_amount, transactions_price = zip(*transactions_data)

        general_data.update({
            "TransactionsDate": transactions_date,
            "TransactionsAmount": transactions_amount,
            "TransactionsPrice": transactions_price
        })


def process_additional_data(data, general_data):
    logging.info("Processing additional data")
    additional_data_keys = [
        "Highlights", "Valuation", "SharesStats",
        "Technicals", "AnalystRatings"
    ]

    for key in additional_data_keys:
        general_data.update(data[key])

def main():
    logging.info("Starting data processing")
    tickers = read_stock_tickers_from_file()

    df = pd.DataFrame()

    for ticker in tickers:
        try:
            logging.info(f"Processing data for {ticker}")
            data = load_json_data(ticker)
            if data:
                general_data = process_general_data(data)

                process_listings(general_data)
                process_officers(general_data)
                process_address(general_data)
                process_splits_dividends(data, general_data)
                process_holders(data, general_data)
                process_insider_transactions(data, general_data)
                process_additional_data(data, general_data)

                general_data_df = pd.DataFrame([general_data.values()], columns=general_data.keys())
                df = pd.concat([df, general_data_df])
            else:
                logging.warning(f"No data found for {ticker}")

        except Exception as e:
            logging.error(f"Error processing data for {ticker}: {str(e)}")

    output_file = "Data/Tickers/general_data.csv"
    df.to_csv(output_file, index=True)

    logging.info(f"CSV file generated: {output_file}")


if __name__ == "__main__":
    main()  