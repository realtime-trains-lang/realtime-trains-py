import json
import os, os.path

from datetime import datetime, timedelta 

# List of the number of days in each month
months: list = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]

def validate_date(date: str) -> bool:

    # Get the date 8 days ago
    first_valid_date = get_time_delta(-8)

    # Get the date in 81 days
    last_valid_date = get_time_delta(81)

    # Split the date into its parts (YYYY, MM, DD)
    date_items: list = date.split("/")
    month = date_items[1]

    # Check if the month is valid
    if month > "12":
        return False
    
    # Check if the day is valid
    elif months[int(month)-1] < date_items[2]:
        return False

    for i in range(0, 3):
        if first_valid_date[i] < date_items[i]:

            validation = True
            break
        else:
            validation = False

    if validation == True:
        for i in range(0, 3):
            if last_valid_date[i] > date_items[i]:
                validation = True
                break
            else:
                validation = False
    
    return validation

def validate_time(time: str) -> bool:
    time_data: list = []
    if len(time) != 4:
        return False
    
    else:
        for i in range(0, 4):
            time_data.append(int(time[i])) 

        if time_data[0] in range(-1, 2):
            if time_data[1] in range(-1, 10):
                if time_data[2] in range(-1, 6):
                    if time_data[3] in range(-1, 10):
                        return True
                
                    else:
                        return False
                else:
                    return False
            else:
                return False
            
        elif time_data[0] == 2:
            if time_data[1] in range(-1, 4):
                if time_data[2] in range(-1, 6):
                    if time_data[3] in range(-1, 10):
                        return True
                
                    else:
                        return False
                else:
                    return False
            else:
                return False
            
        else:
            return False

def get_time_delta(delta: int) -> str:
    
    # Get the timedelta and add it to the date now        v split the time delta
    date_delta = str(datetime.now() + timedelta(delta)).split("-")

    # Get only the day from the last value
    date_delta[2] = (str(date_delta[2]).split(" "))[0]

    return date_delta

def format_time(time: str) -> str:
    # Get the first 4 values and add a : in the middle
    new_time = time[0] + time[1] + ":" + time[2] + time[3]
    return new_time

def create_file(name: str, contents):
    # Check if folder exists
    if not os.path.isdir("realtime_trains_py_data"):

        # Create folder if non-existent
        os.mkdir("realtime_trains_py_data")

    # Create file name by adding directory and file type
    file_name = "realtime_trains_py_data/" + name + ".json"

    # Check if file exists
    if not os.path.isfile(file_name):
        with open(file_name, "x", encoding = "utf-8") as file:
            # Insert data into file
            json.dump(contents, file, ensure_ascii = False, indent = 4)

    else:
        raise Exception("Failed to write to file. Perhaps the file already exists?")