import json
import logging
import os

import pandas as pd

from Src.DataCollection.modules.fetch_data import fetch_index_constituents

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        return None



def get_macro_indicator_list():
    return [
        "real_interest_rate",
        "population_total",
        "population_growth_annual",
        "inflation_consumer_prices_annual",
        "consumer_price_index",
        "gdp_current_usd",
        "gdp_per_capita_usd",
        "gdp_growth_annual",
        "debt_percent_gdp",
        "net_trades_goods_services",
        "inflation_gdp_deflator_annual",
        "agriculture_value_added_percent_gdp",
        "industry_value_added_percent_gdp",
        "services_value_added_percent_gdp",
        "exports_of_goods_services_percent_gdp",
        "imports_of_goods_services_percent_gdp",
        "gross_capital_formation_percent_gdp",
        "net_migration",
        "gni_usd",
        "gni_per_capita_usd",
        "gni_ppp_usd",
        "gni_per_capita_ppp_usd",
        "income_share_lowest_twenty",
        "life_expectancy",
        "fertility_rate",
        "prevalence_hiv_total",
        "co2_emissions_tons_per_capita",
        "surface_area_km",
        "poverty_poverty_lines_percent_population",
        "revenue_excluding_grants_percent_gdp",
        "cash_surplus_deficit_percent_gdp",
        "startup_procedures_register",
        "market_cap_domestic_companies_percent_gdp",
        "mobile_subscriptions_per_hundred",
        "internet_users_per_hundred",
        "high_technology_exports_percent_total",
        "merchandise_trade_percent_gdp",
        "total_debt_service_percent_gni",
        "unemployment_total_percent",
    ]


def check_integrity_of_tickers(ticker_list):
    # We fetch various lists of tickers from exchanges and we make sure that they are 
    # all included in "ticker_list"
    logging.info("Verifying integrity of tickers")

    # GSPC -> S&P500
    sp500_tickers = fetch_index_constituents("GSPC","INDX")
    # DJI -> Dow Jones Industrial Average
    dow_jones_tickers = fetch_index_constituents("DJI","INDX")
    # IXIC -> NASDAQ Composite
    nasdaq_composite_tickers = fetch_index_constituents("IXIC","INDX")
    # RUT -> Russell 2000
    russell_2000_tickers = fetch_index_constituents("RUT","INDX")
    # N225 -> Nikkei 225ç
    # nikkei_225_tickers = fetch_index_constituents("N225","INDX")


    # Merge all tickers
    all_tickers = sp500_tickers + dow_jones_tickers + nasdaq_composite_tickers + russell_2000_tickers # + nikkei_225_tickers

    # Remove duplicates
    all_tickers = list(set(all_tickers))

    # Replace ".US" with ""
    all_tickers = [ticker.replace(".US","") for ticker in all_tickers]

    # Remove tickers with "_old" 
    all_tickers = [ticker for ticker in all_tickers if "_old" not in ticker]

    # Check if all tickers are included in "ticker_list"
    for ticker in all_tickers:
        if ticker not in ticker_list:
            logging.warning(f"Ticker {ticker} is missing from ticker_list")
            # raise ValueError(f"Ticker {ticker} is missing from ticker_list")

 
    


