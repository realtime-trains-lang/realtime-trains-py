# Import external libraries
import requests
import sys
import time

from datetime import datetime

# Import necessary items from other files
from realtime_trains_py.internal.details import DepartureBoardDetails
from realtime_trains_py.internal.utilities import format_time


class LiveBoard:
    def __init__(self, username: str, password: str) -> None:
        self.__username = username
        self.__password = password

    def _get_live(self, tiploc: str) -> None:  
        # Output a helpful message to the user: Press Ctrl+C to close live departure board.
        sys.stdout.write("\033[1;2mPress Ctrl+C to close live departure board.\n")
        time.sleep(2)

        count = 0

        while True:
            departure_board = []
            if count == 0 or datetime.now().strftime("%S") == "00":
                count = 0

                departure_data = requests.get(f"https://api.rtt.io/api/v1/json/search/{tiploc}", auth=(self.__username, self.__password)).json()

                # If the data is not None, continue
                if "error" not in departure_board and departure_data["services"] != None:
                    requested_location = departure_data["location"]["name"] 

                    # Get the service details
                    for service in departure_data["services"]:
                        location_detail = service["locationDetail"] 
                        gbtt_departure = realtime_departure = service_uid = platform = ""

                        if "gbttBookedDeparture" in location_detail:
                            gbtt_departure = location_detail["gbttBookedDeparture"]
                            
                        if "platform" in location_detail:
                            platform = f"Plat {location_detail["platform"]}"
                            
                        if "realtimeDeparture" in location_detail:
                            realtime_departure = location_detail["realtimeDeparture"]
                            
                        if "serviceUid" in service:
                            service_uid = service["serviceUid"]

                        if location_detail["displayAs"] != "CANCELLED_CALL":
                            # If the gbtt departure and realtime departure are equal, set realtime departure to On time
                            if gbtt_departure == realtime_departure:
                                realtime_departure = "On time"

                            elif realtime_departure != "":
                                realtime_departure = (f"Exp {format_time(realtime_departure)}")

                        else:
                            realtime_departure = "Cancelled"

                        gbtt_departure = format_time(gbtt_departure)

                        terminus = (location_detail["destination"]).pop()["description"]

                        # Append new DepartureBoardSimple service details
                        departure_board.append(DepartureBoardDetails(gbtt_departure, terminus, platform, realtime_departure, service_uid))

                        count += 1
                        if count == 3:
                            break

                    line_one = f"\033[1;34m{requested_location} Live:\n\033[1;39m"
                    line_four = ""
                    line_five = ""
                    first = True

                    for service in departure_board:
                        if first:
                            line_two, line_three = self.__first_service(service, requested_location)
                            first = False
                            second = True

                        else:
                            if second:
                                line_four += f"2nd {service.gbtt_departure} {service.terminus} {service.platform}  {check_cancel(service.realtime_departure)}\n"
                                second = False

                            else:
                                line_five += f"3rd {service.gbtt_departure} {service.terminus} {service.platform}  {check_cancel(service.realtime_departure)}\n"
                    
                    # Clear the screen
                    sys.stdout.write("\033c\r")
                    sys.stdout.write(f"{line_one}{line_two}{line_three}{line_four}{line_five}")
                            
                # If the data is None, display a Check timetable for services message
                else:
                    count = 3
                    # Clear the screen
                    sys.stdout.write("\033c\r")
                    sys.stdout.write(f"\033[1;34m{tiploc} Live:\n \033[1;30mCheck timetable for services.\n")

            sys.stdout.write(f"\033[1;3m{datetime.now().strftime("         %H:%M:%S")}\033[K\r")
            time.sleep(1)

    def __first_service(self, service, requested_location: str) -> tuple:
        """
        Get the first service from the live board and print it to the screen with its subsequent calling points and service operator.
        """
        line_two = f"1st {service.gbtt_departure} {service.terminus} {service.platform}  {check_cancel(service.realtime_departure)}\n"

        service_api_response = requests.get(f"https://api.rtt.io/api/v1/json/service/{service.service_uid}/{(datetime.now()).strftime("%Y/%m/%d")}", auth=(self.__username, self.__password))
        service_data = service_api_response.json()

        line_three = "Calling at: "

        valid = False
        stops_outputted = False
        services = len(service_data["locations"])
        service_count = 0
        for location in service_data["locations"]:
            service_count += 1
            if service_count == services:
                if stops_outputted:
                    valid = False
                    line_three += f"{location['description']}"

                else:
                    line_three += f"{location['description']} only"
                    break

            if valid:
                stops_outputted = True
                if service_count == services-1:
                    line_three += f"{location["description"]} & "

                else:
                    line_three += f"{location["description"]}, "

            if location["description"] == requested_location:
                valid = True

        line_three += f". Operated by {service_data["atocName"]}.\n"

        return (line_two, line_three)

def check_cancel(realtime_departure: str) -> str:
    """
    Check if the service is cancelled or delayed. Change text colour accordingly.
    If cancelled, set the text to red. If on time, set the text to green. Otherwise, set the text to yellow.
    """

    if realtime_departure == "Cancelled":
        return "\033[1;31mCancelled\033[1;39m"

    elif realtime_departure == "On time":
        return "\033[1;32mOn time\033[1;39m"

    return f"\033[1;33m  {realtime_departure}\033[1;39m"