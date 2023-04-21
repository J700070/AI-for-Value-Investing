import os
import json
import csv
import formatTickerIntoCSV as ticker_converter

def create_test_json_file(file_path):
    test_data = {
        "US": [
            {
                "ticker": {
                    "Code": "A",
                    "Name": "Agilent Technologies Inc",
                    "Country": "USA",
                    "Exchange": "NYSE",
                    "Currency": "USD",
                    "Type": "Common Stock",
                    "Isin": "US00846U1016"
                },
                "delisted": False
            }
        ],
        "LSE": [
            {
                "ticker": {
                    "Code": "0A00",
                    "Name": "Akzo Nobel N.V.",
                    "Country": "UK",
                    "Exchange": "LSE",
                    "Currency": "EUR",
                    "Type": "Common Stock",
                    "Isin": ""
                },
                "delisted": False
            }
        ]
    }
    with open(file_path, 'w') as f:
        json.dump(test_data, f)

def read_csv_file(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    return data
def test_formatTickerIntoCSV():
    test_input_file = 'Data/test_input.json'
    test_output_file = 'Data/test_output.csv'
    ticker_converter.input_file = test_input_file
    ticker_converter.output_file = test_output_file

    create_test_json_file(test_input_file)
    ticker_converter.main()
    csv_data = read_csv_file(test_output_file)

    with open(test_input_file, 'r') as f:
        json_data = json.load(f)

    total_json_items = sum(len(ticker_list) for ticker_list in json_data.values())

    assert len(csv_data) == total_json_items, f"Expected {total_json_items} items in CSV, but got {len(csv_data)} items"

    expected_data = [
        {
            'Code': 'A',
            'Name': 'Agilent Technologies Inc',
            'Country': 'USA',
            'Exchange': 'NYSE',
            'Currency': 'USD',
            'Type': 'Common Stock',
            'Isin': 'US00846U1016',
            'Delisted': 'False'
        },
        {
            'Code': '0A00',
            'Name': 'Akzo Nobel N.V.',
            'Country': 'UK',
            'Exchange': 'LSE',
            'Currency': 'EUR',
            'Type': 'Common Stock',
            'Isin': '',
            'Delisted': 'False'
        }
    ]

    assert csv_data == expected_data, f"Expected {expected_data}, but got {csv_data}"

    os.remove(test_input_file)
    os.remove(test_output_file)

if __name__ == '__main__':
    test_formatTickerIntoCSV()