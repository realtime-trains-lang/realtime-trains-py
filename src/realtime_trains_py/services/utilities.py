import json
import os, os.path
import re

from datetime import datetime, timedelta 


def validate_uid(uid: str) -> bool:
    # Check if the regex pattern was found
    if re.search("[A-Z][0-9]{5}", uid) != None:
        # If found, return True
        return True
    else:
        # If not found, return False
        return False

def validate_date(date: str) -> bool:
    # Check if the regex pattern was found
    if re.search("[1-9][0-9][0-9]{2}/([0][1-9]|[1][0-2])/([1-2][0-9]|[0][1-9]|[3][0-1])", date) != None:
        # If found, return True
        return True
    else:
        # If not found, return False
        return False

def validate_time(time: str) -> bool:
    # Check if the regex pattern was found
    if re.search("([01][0-9]|2[0-3]):([0-5][0-9])", format_time(time)) != None:
        # If found, return True
        return True
    else:
        # If not found, return False
        return False

def get_time_delta(delta: int) -> str:
    # Get the timedelta and add it to the date now        v split the time delta
    date_delta = str(datetime.now() + timedelta(delta)).split("-")

    # Get only the day from the last value
    date_delta[2] = (str(date_delta[2]).split(" "))[0]

    return date_delta

def format_time(time: str) -> str:
    # Get the first 4 values and add a : in the middle
    return f"{time[0]}{time[1]}:{time[2]}{time[3]}"

def create_file(name: str, contents) -> None:
    # Check if folder exists
    if not os.path.isdir("realtime_trains_py_data"):

        # Create folder if it doesn't exist
        os.mkdir("realtime_trains_py_data")

    # Create file name by adding directory and file type
    file_name = f"realtime_trains_py_data/{name}.json"

    # Check if file exists
    if not os.path.isfile(file_name):
        with open(file_name, "x", encoding = "utf-8") as file:
            # Insert data into file
            json.dump(contents, file, ensure_ascii = False, indent = 4)

    else:
        raise Exception("Failed to write to file. Perhaps the file already exists?")

