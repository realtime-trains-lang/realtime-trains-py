# Import external libraries
import json

import requests

from datetime import datetime
from tabulate import tabulate

# Import necessary items from other files
from realtime_trains_py.internal.details import DefaultBoard, StationBoardDetails
from realtime_trains_py.internal.errors import APIResponseError, NoDataFound
from realtime_trains_py.internal.utilities import create_file, create_parameters


class Boards:
    def __init__(self, request_token: str, complexity: str="s") -> None:
        self.__headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {request_token}",
            }
        self.__complexity = complexity

    def _get_dep_board_details(self, tiploc: str, filter_from: str | None=None, filter_to: str | None=None, rows: int | None=None, time: str | None=None, date: str | None=None) -> DefaultBoard | None:
        # Create the parameters for the API request using the create_parameters function
        params = create_parameters(tiploc, filter_from, filter_to, rows, time, date)

        # Get the API response using the auth details provided
        api_response = requests.get("https://data.rtt.io/rtt/location", headers=self.__headers, params=params)

        if api_response.status_code == 200:
            service_data = api_response.json()

            if self.__complexity == "c":
                # If complexity is c, save the JSON data to a new .json file
                if date is None:
                    date = datetime.now().strftime("%Y/%m/%d")

                date_parts = date.split("/")

                file_name = f"{tiploc}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_dep_board_data"

                create_file(file_name, service_data)

                print(f"Departure data saved to file: \n  {file_name}.")
                return None
            
            departure_board: list = []
            requested_location = service_data["query"]["location"]["description"]

            # For each service in the departure data, get the service data
            for service in service_data["services"][:rows]:
                service_info = get_dep_service_data(service)

                if self.__complexity.endswith("n"):
                    departure_board.append(service_info)

                else:
        #       scheduled_arrival,
        #       scheduled_departure,
        #       destination,
        #       origin,
        #       platform,
        #       expected_arrival,
        #       expected_departure,
        #       service_uid,
        #       coaches
                    # Unpack the service details and append them to a list if complexity does not end with n
                    departure_board.append([
                        service_info.scheduled_arrival,
                        service_info.scheduled_departure, 
                        service_info.origin,
                        service_info.terminus, 
                        service_info.platform, 
                        service_info.coaches,
                        service_info.actual_arrival,
                        service_info.actual_departure, 
                        service_info.service_uid
                        ])

            if self.__complexity.endswith("n"):
                return DefaultBoard(departure_board, requested_location)

            # Pint the departure info and tabulate table with the headers defined
            print(f"Departure board for {requested_location}. Generated at {datetime.now().strftime('%H:%M:%S on %d/%m/%y')}.")
            print(tabulate(
                departure_board, 
                tablefmt="rounded_grid", 
                headers=[
                    "Scheduled \nArrival", 
                    "Scheduled \nDeparture",
                    "Origin",
                    "Destination", 
                    "Platform",
                    "Coaches",
                    "Actual \nArrival",
                    "Actual \nDeparture", 
                    "Service UID"
                    ]))

        elif api_response.status_code == 404:
           raise NoDataFound()

        else:
            raise APIResponseError(f"Failed to connect to the RTT API server: {api_response.status_code}")

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
    service_uid = service["scheduleMetadata"]["identity"]

    print(json.dumps(service))


    # Extract arrival data if it exists
    if "arrival" in temporal_data:
        is_cancelled = temporal_data["arrival"]["isCancelled"]
        scheduled_arrival = temporal_data["arrival"]["scheduleAdvertised"].split("T")[1]

        if is_cancelled:
            expected_arrival = "Cancelled"
        
        elif "realtimeActual" in temporal_data["arrival"]:
            expected_arrival = temporal_data["arrival"]["realtimeActual"].split("T")[1]

        elif "realtimeForecast" in temporal_data["arrival"]:
            expected_arrival = temporal_data["arrival"]["realtimeForecast"].split("T")[1]

    # Extract departure data if it exists
    if "departure" in temporal_data:
        is_cancelled = temporal_data["departure"]["isCancelled"]
        scheduled_departure = temporal_data["departure"]["scheduleAdvertised"].split("T")[1]
        if is_cancelled:
            expected_departure = "Cancelled"

        elif "realtimeActual" in temporal_data["departure"]:
            expected_departure = temporal_data["departure"]["realtimeActual"].split("T")[1]

        elif "realtimeForecast" in temporal_data["departure"]:
            expected_departure = temporal_data["departure"]["realtimeForecast"].split("T")[1]                    

    # Extract platform data if it exists
    if "platform" in location_data:
        # print(location_data)
        if "forecast" in location_data["platform"]:
            platform = location_data["platform"]["forecast"]

        else:
            platform = location_data["platform"]["actual"]

    # Extract vehicle length (coaches) data if it exists
    if "numberOfVehicles" in location_data:
        coaches = location_data["numberOfVehicles"]

    print(location_data)

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