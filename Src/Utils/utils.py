import re

from .ascii import bcolors


def print_log(message, status):
    if message == "":
        return

    pattern = r"\[Completed (\d+)/(\d+) \| (\d+\.\d+)%]"
    match = re.search(pattern, message)

    if match:
        x = match.group(1)
        y = match.group(2)
        z = match.group(3)

        parts = re.split(pattern, message)
        before = parts[0]

        text_in_pattern = "[Completed " + x + "/" + y + " | " + z + "%]"

    if status:
        if match:
            print(bcolors.OKGREEN + before + bcolors.ENDC + text_in_pattern)
        else:
            print(bcolors.OKGREEN + message + bcolors.ENDC)
    else:
        if match:
            print(bcolors.FAIL + before + bcolors.ENDC + text_in_pattern)
        else:
            print(bcolors.FAIL + message + bcolors.ENDC)
            print(bcolors.FAIL + message + bcolors.ENDC)
