import unittest
import json
import tempfile
import os
from mergeListedAndDelistedTickers import load_json_file, merge_listed_and_delisted_tickers, save_merged_tickers_to_json

# Test with Pytest

class TestMergeListedAndDelistedTickers(unittest.TestCase):

    def setUp(self):
        self.listed_data = {
            "NYSE": ["AAPL", "MSFT"],
            "NASDAQ": ["GOOGL", "AMZN"]
        }
        self.delisted_data = {
            "NYSE": ["YHOO"],
            "NASDAQ": ["TWTR"]
        }
        self.expected_merged_data = {
            "NYSE": [
                {"ticker": "AAPL", "delisted": False},
                {"ticker": "MSFT", "delisted": False},
                {"ticker": "YHOO", "delisted": True}
            ],
            "NASDAQ": [
                {"ticker": "GOOGL", "delisted": False},
                {"ticker": "AMZN", "delisted": False},
                {"ticker": "TWTR", "delisted": True}
            ]
        }

    def test_merge_listed_and_delisted_tickers(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            listed_file = os.path.join(temp_dir, 'listed.json')
            delisted_file = os.path.join(temp_dir, 'delisted.json')
            merged_file = os.path.join(temp_dir, 'merged.json')

            with open(listed_file, 'w') as f:
                json.dump(self.listed_data, f)
            with open(delisted_file, 'w') as f:
                json.dump(self.delisted_data, f)

            listed_tickers = load_json_file(listed_file)
            delisted_tickers = load_json_file(delisted_file)
            merged_tickers = merge_listed_and_delisted_tickers(listed_tickers, delisted_tickers)

            self.assertEqual(merged_tickers, self.expected_merged_data)

            save_merged_tickers_to_json(merged_tickers, merged_file)

            with open(merged_file, 'r') as f:
                loaded_merged_data = json.load(f)

            self.assertEqual(loaded_merged_data, self.expected_merged_data)

if __name__ == '__main__':
    unittest.main()
