from data_check import check_data_collection_status, print_todo_list
from Src.DataCollection.modules.read_data import read_stock_tickers_from_file
from Utils.ascii import ASCII
from Utils.utils import bcolors

TODO_LIST = [
    "Check what happens with tickers without general data",
]

def print_help():
    print("Available commachecknds:")
    print("  help              - Show this help message")
    print("  check_data        - Check data collection status")
    print("  fetch_data        - Fetch data from the API")
    print("  print_todo        - Print the TODO list")
    print("  exit or quit      - Exit the program")

def main():
    _ascii = ASCII()
    print(_ascii.metis_system_init())
    print(bcolors.WARNING + "Starting Metis System" + bcolors.ENDC)

    while True:
        command = input(bcolors.BOLD + "MetisSystem> " + bcolors.ENDC).lower().strip()

        if command == "check_data":
            check_data_collection_status()
        elif command == "print_todo":
            print_todo_list()
        elif command == "fetch_data":
            tickers = read_stock_tickers_from_file()
            print("Fetching data...")
            

        elif command == "help":
            print_help()
        elif command == "exit" or command == "quit":
            print(bcolors.WARNING + "Exiting Metis System" + bcolors.ENDC)
            break
        else:
            print(bcolors.FAIL + "Unknown command. Type 'help' for a list of available commands." + bcolors.ENDC)

if __name__ == "__main__":
    main()
