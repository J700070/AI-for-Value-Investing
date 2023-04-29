import logging
import os
import shutil
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Lock, Manager

import pandas as pd


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

def process_file(file, lock):
    source_path = "Data/Tickers/Price/"
    purged_path = "Data/Tickers/Price/Purged_prices/"
    corrupted_path = "Data/Tickers/Price/Corrupted_prices/"
    
    file_path = os.path.join(source_path, file)

    try:
        df = pd.read_csv(file_path)
        expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted_close', 'Volume']

        if set(df.columns) == set(expected_columns):
            dest_path = os.path.join(purged_path, file)
            log_msg = f"File '{file}' copied to Purged_prices"
        else:
            dest_path = os.path.join(corrupted_path, file)
            log_msg = f"File '{file}' copied to Corrupted_prices"

        with lock:
            shutil.copy(file_path, dest_path)
            logging.info(log_msg)

    except Exception as e:
        logging.error(f"Error processing file '{file}': {e}")
        with lock:
            shutil.copy(file_path, os.path.join(corrupted_path, file))

def purge_price_data():
    source_path = "Data/Tickers/Price/"
    purged_path = "Data/Tickers/Price/Purged_prices/"
    corrupted_path = "Data/Tickers/Price/Corrupted_prices/"

    os.makedirs(purged_path, exist_ok=True)
    os.makedirs(corrupted_path, exist_ok=True)

    files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]


    with Manager() as manager:
        lock = manager.Lock()
        with ProcessPoolExecutor() as executor:
            executor.map(process_file, files, [lock] * len(files))

if __name__ == "__main__":
    setup_logging()
    purge_price_data()
