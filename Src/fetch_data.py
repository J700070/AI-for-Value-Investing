
import sys

sys.path.append("C:\\Users\\juani\\Desktop\\AI-for-Value-Investing")

from Src.DataCollection.Exchanges.fetch_exchanges import \
    fetch_and_save_exchanges


def fetch_data():
    
    # Data pipeline structure
    # 1. Fetch exchanges data -> exchanges.json
    fetch_and_save_exchanges()






if __name__ == "__main__":
    fetch_data()
