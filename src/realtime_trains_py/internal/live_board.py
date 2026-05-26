# Import external libraries
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
            if first_run or datetime.now().strftime("%S") == "00":
                first_run = False

                # Check the request token (expires every 20 minutes) and update the headers with the new token
                self.__update_request_token(check_token(request_token=self.__headers["Authorization"].split(" ")[1]))

                station_data = requests.get(f"https://data.rtt.io/rtt/location", params=params, headers=self.__headers)

                if station_data.status_code == 200:
                    departure_data = station_data.json()
                    # Get the requested location name 
                    requested_location = departure_data["query"]["location"].pop("description")

                    # Get the service details for the first 3 services in the departure data and append them to a list
                    for service in departure_data["services"][:3]:
                        departure_board.append(get_dep_service_data(service))

                    # Show the first line and update colours based on the given mode
                    if mode == "DMI.Y":
                        line_one = f"\033[1;93m{requested_location} Live:\n"

                    elif mode == "DMI.W":
                        line_one = f"\033[1;39m{requested_location} Live:\n"
                        
                    else:
                        line_one = f"\033[1;34m{requested_location} Live:\n\033[1;39m"

                    line_two = line_three = line_four = line_five = ""
                    first = True
                    second = False

                    # For each service in the departure board, get the details of the first 3 services and print them to the screen 
                    for service in departure_board:
                        if first:
                            # Get the details of the first service, including subsequent calling points, service operator and number of coaches if available
                            line_two, line_three = self.__first_service(service, requested_location, mode)
                            first = False
                            second = True

                        else:
                            if second:
                                # If the service terminates at the requested location, display that it terminates here and its origin. 
                                # Otherwise, display the scheduled departure time, destination, platform and whether it's on time, delayed or cancelled.
                                if service.terminus == requested_location:
                                    line_four += f"2nd {service.scheduled_arrival} Terminates here. Service from {service.origin}.\n"

                                else:
                                    line_four += f"2nd {service.scheduled_departure} {service.terminus} {service.platform}  {check_cancel(service.expected_departure, mode)}\n"

                                second = False

                            else:
                                # If the service terminates at the requested location, display that it terminates here and its origin. 
                                # Otherwise, display the scheduled departure time, destination, platform and whether it's on time, delayed or cancelled.
                                if service.terminus == requested_location:
                                    line_five += f"3rd {service.scheduled_arrival} Terminates here. Service from {service.origin}.\n"

                                else:
                                    line_five += f"3rd {service.scheduled_departure} {service.terminus} {service.platform}  {check_cancel(service.expected_departure, mode)}\n"
                    
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
        params = {
            "uniqueIdentity": f"gb-nr:{service.service_uid}:{datetime.now().strftime('%Y-%m-%d')}", 
            "timeTolerance": "false", 
            "detailed": "false"
            }

        # Get the service data for the first service 
        service_api_response = requests.get(f"https://data.rtt.io/rtt/service", params=params, headers=self.__headers)
        all_service_data = service_api_response.json()["service"]

        line_three = "Calling at: "

        # Prepare to unpack service info
        schedule_data = all_service_data["scheduleMetadata"]
        location_data = all_service_data["locations"]
        origin = all_service_data["origin"][0]["location"].pop("description")
        destination = all_service_data["destination"][0]["location"].pop("description")

        # If the service terminates at the requested location, display that it terminates here and its origin. 
        # Otherwise, display the scheduled departure time, destination, platform and whether it's on time, delayed or cancelled.
        if destination == requested_location:
            line_two = f"1st {service.scheduled_arrival} Terminates here. Service from {origin}.\n"

        else:
            line_two = f"1st {service.scheduled_departure} {service.terminus} {service.platform}  {check_cancel(service.expected_departure, mode)}\n"

        
        can_continue = False
        stops_outputted = False
        number_of_stops = len(location_data)
        coaches = 0
        stop_count = 0 # Keep track of the number of stops added
        for location in location_data:
            # Get the name of the next stop
            stop_name = location["location"].pop("description")
            stop_count += 1
            # If a number of coaches is given in the location data, get that number to display later
            if coaches == 0 and "numberOfVehicles" in location["locationMetadata"]:
                coaches = location["locationMetadata"].pop("numberOfVehicles")

            # If the stop count is equal to the number of stops, check if any stops have been outputted. If they have, add the stop name to the 
            # end of the line without an ampersand and set can_continue to False. If they haven't, add the stop name with 'only' and break the loop.
            if stop_count == number_of_stops:
                if stops_outputted:
                    # Adds the last stop to the line without an ampersand and sets can_continue to False
                    can_continue = False
                    line_three += f"{stop_name}"

                else:
                    line_three += f"{stop_name} only"
                    break

            if can_continue:
                stops_outputted = True
                # If the stop count is one less than the number of stops, add the stop name with an ampersand. 
                # Otherwise, add the stop name with a comma.
                if stop_count == number_of_stops-1:
                    line_three += f"{stop_name} & "

                else:
                    line_three += f"{stop_name}, "

            # If the stop name is the same as the requested location, set can_continue to True to start adding stops to the line.
            if stop_name == requested_location:
                can_continue = True

        operator = schedule_data["operator"].pop("name")

        # If the number of coaches is given, add that to the end of the line. Otherwise, just display the operator.
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