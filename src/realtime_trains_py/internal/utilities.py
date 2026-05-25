# Import external libraries
import json
import os, os.path
import re
import requests

from realtime_trains_py.internal.details import StationBoardDetails
from realtime_trains_py.internal.errors import AuthenticationError, FileWriteError, InvalidComplexity, InvalidDateProvided, InvalidModeProvided, InvalidTimeProvided, InvalidUIDProvided


def complex_setup() -> None:
    # Check if realtime_trains_py_data folder exists and create it if not
    if not os.path.isdir("realtime_trains_py_data"):
        os.mkdir("realtime_trains_py_data")


def check_token(request_token: str) -> str:
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
        
    return request_token


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


def get_dep_service_data(service) -> StationBoardDetails:
    """
    Get the departure service data from the API response.
    This function extracts the relevant information from the service data and returns it as a DepartureBoardDetails object.

    It begins by setting the default values for gbtt_departure, platform, realtime_departure, and service_uid to "-".
    Then, it retrieves the location detail and status from the service data.
    It checks if the keys "gbttBookedDeparture", "platform", "realtimeArrival" and "serviceUid" are in the location detail and assigns their values to the respective variables.
    
    Finally, it returns a DepartureBoardDetails object with the formatted gbtt_departure, destination, platform, time status (aka expected arrival), and service_uid.
    """

    scheduled_arrival = expected_arrival = scheduled_departure = expected_departure = platform = "-"
    coaches = 0

    destination = service["destination"][0]["location"]["description"]
    # print(destination)
    origin = service["origin"][0]["location"]["description"]
    # print(origin)

    temporal_data = service["temporalData"]
    location_data = service["locationMetadata"]
    service_uid = service["scheduleMetadata"].pop("identity")

    # print(json.dumps(service))


    # Extract arrival data if it exists
    if "arrival" in temporal_data:
        is_cancelled = temporal_data["arrival"]["isCancelled"]
        scheduled_arrival = temporal_data["arrival"]["scheduleAdvertised"].split("T")[1][:5]

        if is_cancelled:
            expected_arrival = "Cancelled"
        
        elif "realtimeActual" in temporal_data["arrival"]:
            expected_arrival = temporal_data["arrival"]["realtimeActual"].split("T")[1][:5]
            if expected_arrival == scheduled_arrival:
                expected_arrival = "On time"

        elif "realtimeForecast" in temporal_data["arrival"]:
            expected_arrival = temporal_data["arrival"]["realtimeForecast"].split("T")[1][:5]
            if expected_departure == scheduled_departure:
                expected_departure = "On time"

    # Extract departure data if it exists
    if "departure" in temporal_data:
        is_cancelled = temporal_data["departure"]["isCancelled"]
        scheduled_departure = temporal_data["departure"]["scheduleAdvertised"].split("T")[1][:5]
        if is_cancelled:
            expected_departure = "Cancelled"

        elif "realtimeActual" in temporal_data["departure"]:
            expected_departure = temporal_data["departure"]["realtimeActual"].split("T")[1][:5]
            if expected_departure == scheduled_departure:
                expected_departure = "On time"

        elif "realtimeForecast" in temporal_data["departure"]:
            expected_departure = temporal_data["departure"]["realtimeForecast"].split("T")[1][:5] 
            if expected_departure == scheduled_departure:
                expected_departure = "On time"                   

    # Extract platform data if it exists
    if "platform" in location_data:
        # print(location_data)
        if "forecast" in location_data["platform"]:
            platform = location_data["platform"]["forecast"]

        else:
            platform = location_data["platform"]["actual"]

    # Extract vehicle length (coaches) data if it exists
    if "numberOfVehicles" in location_data:
        coaches = location_data.pop("numberOfVehicles")

    # print(location_data)

    # print(f"""
    # {scheduled_departure} (Exp: {expected_departure}) service to {destination} from platform {platform}.
    # Arrival is {scheduled_arrival} (Exp: {expected_arrival}).

    # Service {service_uid} is formed of {coaches} coaches. Service originates from {origin}.

# """)

    return StationBoardDetails(
        scheduled_arrival,
        scheduled_departure,
        destination,
        origin,
        platform,
        expected_arrival,
        expected_departure,
        service_uid,
        coaches
    )


def validate_complexity(complexity: str) -> None:
    if complexity not in ["a", "a.n", "c", "s","s.n"]:
        if complexity in ["a.p", "s.p"]:
            complexity = complexity[:-2]

        else:
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