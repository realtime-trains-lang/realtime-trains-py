import json
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

                count = 59

                while True:
                    departure_board = []
                    count += 1
                    if count == 60:
                        sys.stdout.write("\033c\r")
                        count = 0

                        dep_api_response = requests.get(f"https://api.rtt.io/api/v1/json/search/{tiploc}", auth=(self.__username, self.__password))

                        departure_data = dep_api_response.json()

                        # If the data is None, raise an error
                        if departure_data["services"] == None:
                            raise ValueError("404: No data found.")
                            
                        requested_location = departure_data["location"]["name"]  # Get the requested location name

                        for service in departure_data["services"]:
                            location_detail = service["locationDetail"]  # Details of the location

                            gbtt_departure = ""
                            realtime_departure = "-"
                            service_uid = "-"
                            platform = "-"

                            # Check if booked departure is in location detail
                            if "gbttBookedDeparture" in location_detail:
                                gbtt_departure = location_detail["gbttBookedDeparture"]
                                
                            # Check if platform is in location detail
                            if "platform" in location_detail:
                                platform = location_detail["platform"]
                                
                            # Check if realtime departure is in location detail
                            if "realtimeDeparture" in location_detail:
                                realtime_departure = location_detail["realtimeDeparture"]
                                
                            # Check if service UID is in location detail
                            if "serviceUid" in service:
                                service_uid = service["serviceUid"]

                            # Check if the status isn't cancelled
                            if location_detail["displayAs"] != "CANCELLED_CALL":
                                # If the gbtt departure and realtime departure are equal, set realtime departure to On Time
                                if gbtt_departure == realtime_departure:
                                    realtime_departure = "On time"

                                # If the realtime departure isn't null, format and add Exp
                                elif realtime_departure != "-":
                                    realtime_departure = (f"Exp {format_time(realtime_departure)}")

                                # Format the gbtt departure
                                gbtt_departure = format_time(gbtt_departure)

                            else:
                                # Set the realtime departure to cancelled
                                realtime_departure = "Cancelled"
                                # Format the gbtt departure
                                gbtt_departure = format_time(gbtt_departure)

                            # Pop the terminus
                            terminus = (location_detail["destination"]).pop()["description"]

                            # Append new DepartureBoardSimple service details
                            departure_board.append(DepartureBoardDetails(gbtt_departure, terminus, platform, realtime_departure, service_uid))

                            # Add one to count
                            count += 1
                            # If the count is 3, break
                            if count == 3:
                                break

                        sys.stdout.write("\033[1;34m")
                        sys.stdout.write(f"{requested_location} Live:\n")
                        first = True
                        sys.stdout.write("\033[1;33m")

                        for service in departure_board:
                            if first:
                                terminus = service.terminus
                                sys.stdout.write(f"{service.gbtt_departure} {terminus} {service.platform} ")
                                if service.realtime_departure == "Cancelled":
                                    sys.stdout.write("\033[1;31m")

                                sys.stdout.write(f"{service.realtime_departure}\n")
                                sys.stdout.write("\033[1;33m")

                                service_api_response = requests.get(f"https://api.rtt.io/api/v1/json/service/{service.service_uid}/{(datetime.now()).strftime("%Y/%m/%d")}", auth=(self.__username, self.__password))
                                service_data = service_api_response.json()

                                # Create a new calling points list
                                calling_points: list = []

                                sys.stdout.write("Calling at: ")

                                valid = False
                                for location in service_data["locations"]:
                                    if location["description"] == terminus:
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

                    sys.stdout.write("\033[1;3m")
                    sys.stdout.write(datetime.now().strftime("     %H:%M:%S     "))
                    sys.stdout.write("\033[K\r")
                    time.sleep(1)
