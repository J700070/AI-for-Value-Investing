import json
import logging
import os

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_api_key():
    return os.environ.get('EODHD_API_KEY')


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        return None


def write_csv_file(file_path, data, header):
    try:
        df = pd.DataFrame(data, columns=header)
        df.to_csv(file_path, index=False, encoding='utf-8')
        logging.info(f"CSV file saved to {file_path}")
    except IOError:
        logging.error(f"Error writing to file {file_path}")  


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
