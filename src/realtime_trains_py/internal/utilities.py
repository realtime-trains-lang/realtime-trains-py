# Import external libraries
import json
import os, os.path
import re
import requests

from datetime import datetime

from realtime_trains_py.internal.errors import AuthenticationError, FileWriteError, InvalidComplexity, InvalidDateProvided, InvalidModeProvided, InvalidTimeProvided, InvalidUIDProvided


def complex_setup() -> None:
    # Check if realtime_trains_py_data folder exists and create it if not
    if not os.path.isdir("realtime_trains_py_data"):
        os.mkdir("realtime_trains_py_data")


def connection_authorised(username: str, password: str) -> None:
    if username == None or password == None:
        raise AuthenticationError("Username or password wasn't provided.")
    
    # Test the connection for departures at KNGX, with the auth details provided
    if requests.get("https://api.rtt.io/api/v1/json/search/KNGX", auth=(username, password)).status_code == 401:
        raise AuthenticationError("Couldn't verify your username or password.")


def create_file(name: str, contents) -> None:
    # Create file name by adding directory and type
    file_name = f"realtime_trains_py_data/{name}.json"

    # Check if file exists
    if not os.path.isfile(file_name):
        with open(file_name, "x", encoding="utf-8") as file:
            json.dump(contents, file, ensure_ascii=False, indent=4)

    else:
        raise FileWriteError(file_name)


# Create a new search query for board data requests to the API
def create_search_query(tiploc: str, search_filter: str | None=None, rows: int | None=None, time: str | None=None, date: str | None=None) -> str:
    # If a date is provided and it isn't valid, raise an error
    if date is not None:
        validate_date(date)

    # If a time is provided and it isn't valid, raise an error
    if time is not None:
        validate_time(time)

    search_query = f"https://api.rtt.io/api/v1/json/search/{tiploc}"

    # If a search filter was provided, append it to the search_query
    if search_filter is not None:
        search_query += f"/to/{search_filter.upper()}"

    if time is not None and date is None:
        search_query += f"/{(datetime.now()).strftime('%Y/%m/%d')}/{time}"

    elif date is not None:
        search_query += f"/{date}"

        if time is not None:
            search_query += f"/{time}"

    return search_query


def format_time(time: str) -> str:
    return f"{time[0]}{time[1]}:{time[2]}{time[3]}"


# Get the time status
def get_time_status(gbtt_time, actual_time, status) -> str | None:
    # Check that the status isn't cancelled
    if status != "CANCELLED_CALL":
        if gbtt_time == actual_time:
            return "On time"

        # If the realtime departure isn't null, format and add Exp
        elif actual_time != "-":
            return f"Exp {format_time(actual_time)}"

    else:
        return "Cancelled"


def validate_complexity(complexity: str) -> None:
    if complexity not in ["a", "a.n", "c", "s","s.n"]:
        raise InvalidComplexity(complexity)
    
    elif complexity == "c":
        complex_setup()


def validate_date(date: str) -> None:
    if re.match("[1-9][0-9][0-9]{2}/([0][1-9]|[1][0-2])/([1-2][0-9]|[0][1-9]|[3][0-1])", date) == None:
        raise InvalidDateProvided(date) 


def validate_mode(mode: str) -> None:
    if mode not in ["DMI.Y", "DMI.W", "LCD"]:
        raise InvalidModeProvided(mode)


def validate_time(time: str) -> None:
    if re.match("([01][0-9]|2[0-3])([0-5][0-9])", time) == None:
        raise InvalidTimeProvided(time)


def validate_uid(uid: str) -> None:
    if re.match("[A-Z][0-9]{5}", uid) == None:
        raise InvalidUIDProvided(uid)