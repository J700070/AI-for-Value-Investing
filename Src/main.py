from data_check import check_data_collection_status, print_todo_list
from Utils.ascii import ASCII
from Utils.utils import bcolors

PRINT_TODO_LIST = True

TODO_LIST = [
    "Check what happens with tickers without general data",
]


def main():
    _ascii = ASCII()
    print(_ascii.metis_system_init())
    print(bcolors.WARNING + "Starting Metis System" + bcolors.ENDC)


    # Data Collection
    check_data_collection_status()


    if(PRINT_TODO_LIST):
        print_todo_list()
        


if __name__ == "__main__":
    main()
