import os
import pandas as pd


def test_sp500CompaniesInData():
    """
    This function checks if there are general and financials data files
    for all S&P 500 companies in the specified directories.
    """
    # Read all S&P 500 companies from "sp500Companies.csv"
    sp500Companies = pd.read_csv("Data/sp500Companies.csv", header=0)["Symbol"].to_list()

    # Set up directories for General and Financials data
    data_dir_general = "Data/Tickers/General"
    data_dir_financials = "Data/Tickers/Financials"

    # List all files in the directories
    file_names_general = os.listdir(data_dir_general)
    file_names_financials = os.listdir(data_dir_financials)

    for company in sp500Companies:
        # Format company name for general and financials data files
        company_general = company + "_general.json"
        company_financials = company + "_financials.json"

        # Assert that the files are in the respective directories
        assert company_general in file_names_general, \
            f"General data file for {company} not found in {data_dir_general}"
        assert company_financials in file_names_financials, \
            f"Financials data file for {company} not found in {data_dir_financials}"

if __name__ == '__main__':
    test_sp500CompaniesInData()