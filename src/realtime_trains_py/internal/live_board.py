import requests
import sys
import time

from datetime import datetime

from realtime_trains_py.internal.details import DepartureBoardDetails
from realtime_trains_py.internal.utilities import format_time


class LiveBoard:
    def __init__(self, username: str, password: str) -> None:
        self.__username = username
        self.__password = password

    def _get_live(self, tiploc: str) -> None:  
        # Output a helpful message to the user
        sys.stdout.write("\033[1;2m")
        sys.stdout.write("Press Ctrl+C to close live departure board.\n")
        time.sleep(2)

        count = 62

        while True:
            departure_board = []
            count += 1
            if count == 63:
                # Clear the screen
                sys.stdout.write("\033c\r")
                count = 0

                departure_data = requests.get(f"https://api.rtt.io/api/v1/json/search/{tiploc}", auth=(self.__username, self.__password)).json()

                # If the data is None, raise an error
                if departure_data["services"] != None:
                    
                    requested_location = departure_data["location"]["name"] 

                    # Get the service details
                    for service in departure_data["services"]:
                        location_detail = service["locationDetail"] 

                        gbtt_departure = realtime_departure = service_uid = platform = "-"

                        if "gbttBookedDeparture" in location_detail:
                            gbtt_departure = location_detail["gbttBookedDeparture"]
                            
                        if "platform" in location_detail:
                            platform = location_detail["platform"]
                            
                        if "realtimeDeparture" in location_detail:
                            realtime_departure = location_detail["realtimeDeparture"]
                            
                        if "serviceUid" in service:
                            service_uid = service["serviceUid"]

                        if location_detail["displayAs"] != "CANCELLED_CALL":
                            # If the gbtt departure and realtime departure are equal, set realtime departure to On Time
                            if gbtt_departure == realtime_departure:
                                realtime_departure = "On time"

                            elif realtime_departure != "-":
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

                    sys.stdout.write("\033[1;34m")
                    sys.stdout.write(f"{requested_location} Live:\n")
                    sys.stdout.write("\033[1;33m")
                    first = True

                    for service in departure_board:
                        if first:
                            sys.stdout.write(f"1st {service.gbtt_departure} {service.terminus} {service.platform} ")
                            if service.realtime_departure == "Cancelled":
                                sys.stdout.write("\033[1;31m")

                            sys.stdout.write(f"{service.realtime_departure}\n")
                            sys.stdout.write("\033[1;33m")

                            service_api_response = requests.get(f"https://api.rtt.io/api/v1/json/service/{service.service_uid}/{(datetime.now()).strftime("%Y/%m/%d")}", auth=(self.__username, self.__password))
                            service_data = service_api_response.json()

                            sys.stdout.write("Calling at: ")

                            valid = False
                            for location in service_data["locations"]:
                                if location["description"] == service.terminus:
                                    valid = False
                                    sys.stdout.write(f"{location['description']}")
                    
                                if valid:
                                    sys.stdout.write(f"{location["description"]}, ")

                                if location["description"] == requested_location:
                                    valid = True

                            first = False
                            sys.stdout.write("\n")

                        else:
                            sys.stdout.write(f"{service.gbtt_departure} {service.terminus} {service.platform} ")
                            if service.realtime_departure == "Cancelled":
                                sys.stdout.write("\033[1;31m")

                            sys.stdout.write(f"{service.realtime_departure}\n")
                            sys.stdout.write("\033[1;33m")
                else:
                    sys.stdout.write("\033[1;34m")
                    sys.stdout.write(f"{tiploc} Live:\n")
                    sys.stdout.write("\033[1;33m")
                    sys.stdout.write("Check timetable for services.\n")

            sys.stdout.write("\033[1;3m")
            sys.stdout.write(datetime.now().strftime("     %H:%M:%S     "))
            sys.stdout.write("\033[K\r")
            time.sleep(1)
