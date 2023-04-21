import json

from Src.DataCollection.common import read_json_file


def merge_listed_and_delisted_tickers(listed_tickers, delisted_tickers):
    merged_tickers = {}
    
    for exchange, tickers in listed_tickers.items():
        if exchange not in merged_tickers:
            merged_tickers[exchange] = []
        for ticker in tickers:
            merged_tickers[exchange].append({
                'ticker': ticker,
                'delisted': False
            })

    for exchange, tickers in delisted_tickers.items():
        if exchange not in merged_tickers:
            merged_tickers[exchange] = []
        for ticker in tickers:
            merged_tickers[exchange].append({
                'ticker': ticker,
                'delisted': True
            })

    return merged_tickers

def save_merged_tickers_to_json(merged_tickers, output_file):
    with open(output_file, 'w') as f:
        json.dump(merged_tickers, f, indent=2)

def main():
    listed_tickers_file = "Data/listed_tickers_by_exchange.json"
    delisted_tickers_file = "Data/delisted_tickers_by_exchange.json"
    output_file = "Data/merged_tickers_by_exchange.json"
    
    listed_tickers = read_json_file(listed_tickers_file)
    delisted_tickers = read_json_file(delisted_tickers_file)
    merged_tickers = merge_listed_and_delisted_tickers(listed_tickers, delisted_tickers)
    save_merged_tickers_to_json(merged_tickers, output_file)
    print(f"Merged tickers saved to {output_file}")

if __name__ == "__main__":
    main()
