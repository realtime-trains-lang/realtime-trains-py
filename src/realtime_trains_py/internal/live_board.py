# Import external libraries
import json

import requests
import sys
import time

from datetime import datetime

# Import necessary items from other files
from realtime_trains_py.internal.details import StationBoardDetails
from realtime_trains_py.internal.utilities import check_token, get_dep_service_data, validate_mode


class LiveBoard:
    def __init__(self, request_token: str) -> None:
        self.__headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {request_token}",
            }
        
    def __update_request_token(self, request_token: str) -> None:
        self.__headers["Authorization"] = f"Bearer {request_token}"

    def _get_live(self, tiploc: str, mode: str="LCD") -> None:  
        validate_mode(mode)

        # Output a helpful message to the user: Press Ctrl+C to close live departure board.
        sys.stdout.write("\033[1;2mPress Ctrl+C to close live departure board.\n")
        time.sleep(2)

        first_run: bool = True

        params = {
            "code": f"gb-nr:{tiploc.upper()}",
            "timeTolerance": "false",
            "detailed": "false"
        }

        while True:
            departure_board: list[StationBoardDetails] = []
            # Update the departure board every 60 seconds, on the minute
            if first_run == True or datetime.now().strftime("%S") == "00":
                first_run = False

                self.__update_request_token(check_token(request_token=self.__headers["Authorization"].split(" ")[1]))

                station_data = requests.get(f"https://data.rtt.io/rtt/location", params=params, headers=self.__headers)

                # print(station_data.status_code)
                # print(station_data.text)
                # time.sleep(5)

                if station_data.status_code == 200:
                    departure_data = station_data.json()
                    requested_location = departure_data["query"]["location"].pop("description")

                    # Get the service details
                    for service in departure_data["services"][:3]:
                        # Append new service details
                        departure_board.append(get_dep_service_data(service))

                    if mode == "DMI.Y":
                        line_one = f"\033[1;93m{requested_location} Live:\n"

                    elif mode == "DMI.W":
                        line_one = f"\033[1;39m{requested_location} Live:\n"
                        
                    else:
                        line_one = f"\033[1;34m{requested_location} Live:\n\033[1;39m"

                    line_two = line_three = line_four = line_five = ""
                    first = True
                    second = False

                    for service in departure_board:
                        if first:
                            line_two, line_three = self.__first_service(service, requested_location, mode)
                            first = False
                            second = True

                        else:
                            if second:
                                if service.terminus == requested_location:
                                    line_four += f"2nd Terminates here. Service from {service.origin}.\n"

                                else:
                                    line_four += f"2nd {service.scheduled_departure} {service.terminus} {service.platform}  {check_cancel(service.actual_departure, mode)}\n"

                                second = False

                            else:
                                if service.terminus == requested_location:
                                    line_five += f"3rd Terminates here. Service from {service.origin}.\n"
                                else:
                                    line_five += f"3rd {service.scheduled_departure} {service.terminus} {service.platform}  {check_cancel(service.actual_departure, mode)}\n"
                    
                    # Clear the screen
                    sys.stdout.write("\033c\r")
                    sys.stdout.write(f"{line_one}{line_two}{line_three}{line_four}{line_five}")
                            
                # If the data is None, display a Check timetable for services message
                else:
                    first_run = False
                    # Clear the screen
                    sys.stdout.write("\033c\r")
                    sys.stdout.write(f"\033[1;34m{tiploc} Live:\n \033[1;30mCheck timetable for services.\n")

            sys.stdout.write(f"\033[1;3m{datetime.now().strftime('         %H:%M:%S')}\033[K\r")
            time.sleep(1)

    def __first_service(self, service: StationBoardDetails, requested_location: str, mode) -> tuple:
        """
        Get the first service from the live board and print it to the screen with its subsequent calling points and service operator.
        """
        line_two = f"1st {service.scheduled_departure} {service.terminus} {service.platform}  {check_cancel(service.actual_departure, mode)}\n"

        # print(service.service_uid)
        # print(self.__headers)

        params = {
            "uniqueIdentity": f"gb-nr:{service.service_uid}:{datetime.now().strftime('%Y-%m-%d')}", 
            "timeTolerance": "false", 
            "detailed": "false"
            }

        service_api_response = requests.get(f"https://data.rtt.io/rtt/service", params=params, headers=self.__headers)
        all_service_data = service_api_response.json()["service"]

        line_three = "Calling at: "

        # print(json.dumps(all_service_data, indent=4))

        schedule_data = all_service_data["scheduleMetadata"]
        location_data = all_service_data["locations"]
        origin = all_service_data["origin"][0]["location"].pop("description")
        destination = all_service_data["destination"][0]["location"].pop("description")

        if destination == requested_location:
            line_two = f"1st Terminates here. Service from {origin}.\n"
        

        valid = False
        stops_outputted = False
        stops = len(location_data)
        coaches = 0
        stop_count = 0
        for location in location_data:
            stop_name = location["location"].pop("description")
            stop_count += 1
            if coaches == 0 and "numberOfVehicles" in location["locationMetadata"]:
                coaches = location["locationMetadata"].pop("numberOfVehicles")

            if stop_count == stops:
                if stops_outputted:
                    valid = False
                    line_three += f"{stop_name}"

                else:
                    line_three += f"{stop_name} only"
                    break

            if valid:
                stops_outputted = True
                if stop_count == stops-1:
                    line_three += f"{stop_name} & "

                else:
                    line_three += f"{stop_name}, "

            if stop_name == requested_location:
                valid = True

        operator = schedule_data["operator"].pop("name")

        if coaches > 0:
            line_three += f". A {operator} service formed of {coaches} coaches.\n"

        else:
            line_three += f". A {operator} service.\n"

        return line_two, line_three

def check_cancel(actual_departure: str, mode) -> str:
    """
    Check if the service is cancelled or delayed. Change text colour accordingly.
    If cancelled, set the text to red. If on time, set the text to green. Otherwise, set the text to yellow.
    """

    if mode != "LCD":
        if actual_departure == "Cancelled":
            return "Cancelled"

        elif actual_departure == "On time":
            return "On time"

        return f"{actual_departure}"

    else:
        if actual_departure == "Cancelled":
            return "\033[1;31mCancelled\033[1;39m"

        elif actual_departure == "On time":
            return "\033[1;32mOn time\033[1;39m"

        return f"\033[1;33m  {actual_departure}\033[1;39m"