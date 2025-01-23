# Import libraries
import json
import os, os.path
import re
import requests

# Create new file
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
        raise Exception("Failed to write to file (500). Perhaps the file already exists?")

# Format the time
def format_time(time: str) -> str:
    # Get the first 4 values and add a : in the middle
    return f"{time[0]}{time[1]}:{time[2]}{time[3]}"

# Test the connection to the API
def connection_authorised(username: str, password: str) -> bool:
    # Test the connection for departures at KNGX, with the auth details provided
    test = requests.get("https://api.rtt.io/api/v1/json/search/KNGX", auth=(username, password))

    # If the status code is 401, return False
    if test.status_code == 401: return False
    
    # If any other code is provided, return True
    return True

# Validate the date
def validate_date(date: str) -> bool:
    # Check if the regex pattern was found
    if re.search("[1-9][0-9][0-9]{2}/([0][1-9]|[1][0-2])/([1-2][0-9]|[0][1-9]|[3][0-1])", date) != None:
        # If found, return True
        return True
    
    # If not found, return False
    return False

# Validate the time
def validate_time(time: str) -> bool:
    # Check if the regex pattern was found
    if re.search("([01][0-9]|2[0-3])([0-5][0-9])", format_time(time)) != None:
        # If found, return True
        return True
    
    # If not found, return False
    return False

# Validate the service UID
def validate_uid(uid: str) -> bool:
    # Check if the regex pattern was found
    if re.search("[A-Z][0-9]{5}", uid) != None:
        # If found, return True
        return True
    
    # If not found, return False
    return False
