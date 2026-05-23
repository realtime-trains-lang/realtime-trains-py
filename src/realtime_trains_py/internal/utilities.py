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


def connection_authorised(request_token: str) -> str | None:
    if request_token == None:
        raise AuthenticationError("Request token wasn't provided.")
    
    headers={"Accept": "application/json", "Authorization": f"Bearer {request_token}"}
    
    # Test the connection for departures at KNGX, with the auth details provided
    if requests.get("https://data.rtt.io/api/info", headers=headers).status_code != 200:
        response = requests.get("https://data.rtt.io/api/get_access_token", headers=headers)
        if response.status_code != 200:
            raise AuthenticationError("Request token provided isn't valid.")
        
        else:
            return response.json()["token"]


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
def create_parameters(tiploc: str, filter_from: str | None=None, filter_to: str | None=None, rows: int | None=None, time: str | None=None, date: str | None=None) -> dict:
    # If a date is provided and it isn't valid, raise an error
    if date is not None:
        validate_date(date)

    # If a time is provided and it isn't valid, raise an error
    if time is not None:
        validate_time(time)

    parameters = {
        "code": f"gb-nr:{tiploc.upper()}",
        "filterFrom": f"gb-nr:{filter_from.upper()}" if filter_from is not None else "",
        "filterTo" : f"gb-nr:{filter_to.upper()}" if filter_to is not None else "",
        "timeFrom": "",
        "timeTolerance": "false",
        "detailed": "false"
    }

    # Add the timeFrom parameter based on the time and date parameters provided
    if time is not None and date is None:
        parameters["timeFrom"] = time

    elif time is not None and date is not None:
        parameters["timeFrom"] = f"{date} {time}"

    elif time is None and date is not None:
        parameters["timeFrom"] = date

    return parameters


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
    if re.match("[1-9][0-9][0-9]{2}-([0][1-9]|[1][0-2])-([1-2][0-9]|[0][1-9]|[3][0-1])", date) == None:
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