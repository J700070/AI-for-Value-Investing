import logging

from Src.DataCollection.common import read_json_file, write_csv_file

input_file = 'Data/merged_tickers_by_exchange.json'
output_file = 'Data/tickers.csv'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def format_tickers_to_csv():
    global input_file, output_file

    json_data = read_json_file(input_file)
    if json_data is None:
        logging.error("Could not read JSON data.")
        return

    tickers = []

    for exchange, ticker_list in json_data.items():
        for ticker_obj in ticker_list:
            ticker = ticker_obj['ticker']
            tickers.append({
                'Code': ticker['Code'],
                'Name': ticker['Name'],
                'Country': ticker['Country'],
                'Exchange': ticker['Exchange'],
                'Currency': ticker['Currency'],
                'Type': ticker['Type'],
                'Isin': ticker['Isin'],
                'Delisted': ticker_obj['delisted'],
            })

    header = ['Code', 'Name', 'Country', 'Exchange', 'Currency', 'Type', 'Isin', 'Delisted']
    write_csv_file(output_file, tickers, header)


if __name__ == '__main__':
    format_tickers_to_csv()
