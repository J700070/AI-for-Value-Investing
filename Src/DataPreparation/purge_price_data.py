import logging
import os
import shutil
from concurrent.futures import ProcessPoolExecutor

import pandas as pd


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

def process_file(file):
    source_path = "Data/Tickers/Price/"
    purged_path = "Data/Tickers/Price/Purged_prices/"
    corrupted_path = "Data/Tickers/Price/Corrupted_prices/"
    
    file_path = os.path.join(source_path, file)

    try:
        df = pd.read_csv(file_path)
        expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted_close', 'Volume']

        if set(df.columns) == set(expected_columns):
            shutil.copy(file_path, os.path.join(purged_path, file))
            logging.info(f"File '{file}' copied to Purged_prices")
        else:
            shutil.copy(file_path, os.path.join(corrupted_path, file))
            logging.warning(f"File '{file}' copied to Corrupted_prices")
    except Exception as e:
        logging.error(f"Error processing file '{file}': {e}")
        shutil.copy(file_path, os.path.join(corrupted_path, file))

def purge_price_data():
    source_path = "Data/Tickers/Price/"
    purged_path = "Data/Tickers/Price/Purged_prices/"
    corrupted_path = "Data/Tickers/Price/Corrupted_prices/"

    os.makedirs(purged_path, exist_ok=True)
    os.makedirs(corrupted_path, exist_ok=True)

    files = os.listdir(source_path)

    with ProcessPoolExecutor() as executor:
        executor.map(process_file, files)

if __name__ == "__main__":
    setup_logging()
    purge_price_data()

