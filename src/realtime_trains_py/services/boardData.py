from datetime import datetime
from services.utilities import validate_time, validate_date, format_time

import json
import requests


class DepartureBoardSimple():
    def __init__(self, gbtt_departure, terminus, platform, realtime_departure, service_uid):
        self.gbtt_departure = gbtt_departure
        self.terminus = terminus
        self.platform = platform
        self.realtime_departure = realtime_departure
        self.service_uid = service_uid

class DepartureBoardAdvanced():
    def __init__(self, gbtt_departure, terminus, platform, realtime_departure, service_uid):
        self.gbtt_departure = gbtt_departure
        self.terminus = terminus
        self.platform = platform
        self.realtime_departure = realtime_departure
        self.service_uid = service_uid

class Boards:
    def __init__(self, username: str = None, password: str = None, complexity: str = "s"):
        self.__username = username
        self.__password = password
        self.__complexity = complexity
        self.__date: str = (datetime.now()).strftime("%Y/%m/%d")

        self._board_url: str = "https://api.rtt.io/api/v1/json/search/"

    def _get_dep_board_details(self, tiploc, filter, rows, time, date: str = None):
        if date is None:
            date = self.__date

        if time is None:
            time = (datetime.now()).strftime("%H%M")

        if self.__complexity == "c" or (validate_date(date) and validate_time(time)):
            if filter != None:
                search_query = "/json/search/" + str(tiploc) + "/to/<toStation>" + str(filter)

            else:
                search_query = "https://api.rtt.io/api/v1/json/search/" + str(tiploc) + "/" + str(date)
            #print(search_query)
            api_response =  requests.get(search_query, auth=(self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()

                if self.__complexity == "c":
                    split_date = date.split("/")
                    file_name = "JSONs/" + tiploc + "_on_" + split_date[0] + "." + split_date[1] + "." + split_date[2] + "_arr_board_data.json"

                    with open(file_name, 'x', encoding='utf-8') as file:
                        json.dump(service_data, file, ensure_ascii = False, indent = 4)

                        return_info: str = "Board information added to new file: " + file_name

                    print(return_info)
                
                elif self.__complexity == "a":
                    pass
                    #departure_board: str = []

                    #services = service_data["services"]

                elif self.__complexity == "s":

                    departure_board: list = []
                    
                    services = service_data["services"]

                    for service in services:
                        destinations = service["locationDetail"]["destination"]
                        status = service["locationDetail"]["displayAs"]

                        try:
                            gbtt_departure = service["locationDetail"]["gbttBookedDeparture"]

                        except:
                            gbtt_departure = "Unknown"

                        try:
                            platform = service["locationDetail"]["platform"]

                        except:
                            platform = "Unknown"

                        try:
                            realtime_departure = service["locationDetail"]["realtimeDeparture"]

                        except:
                            realtime_departure = "Unknown"

                        try:
                            service_uid = service["serviceUid"]

                        except:
                            service_uid = "Unknown"


                        if status != "CANCELLED_CALL":
                            if gbtt_departure == realtime_departure:
                                realtime_departure = "On time"
                                gbtt_departure = format_time(gbtt_departure)

                            elif realtime_departure == "Unknown":
                                gbtt_departure = format_time(gbtt_departure)

                            else:
                                realtime_departure = format_time(realtime_departure)
                                realtime_departure = "Exp " + realtime_departure
                                gbtt_departure = format_time(gbtt_departure)

                        else:
                            realtime_departure = "Cancelled"
                            gbtt_departure = format_time(gbtt_departure)

                        for destination in destinations:
                            terminus = destination["description"]

                            departure_board.append(DepartureBoardSimple(gbtt_departure, terminus, platform, realtime_departure, service_uid))

                    #print(departure_board)
                    return departure_board  


            elif api_response.status_code == 404:
                raise ValueError("An unexpected error occurred. Status code:", api_response.status_code)
            
            elif api_response.status_code == 401 or api_response.status_code == 403:
                raise ValueError("Access blocked: check your credentials. Status code:", api_response.status_code)

            else:
                raise ConnectionRefusedError("Failed to connect to the RTT API server. Try again in a few minutes. Status code:", api_response.status_code)

        else: 
            raise ValueError("Invalid date or time. Date or time provided did not meet requirements or fall into the valid date/time range.")

    def _get_arr_board_details(self, tiploc, filter, rows, time, date: str = None):
        if date is None:
            date = self.__date

        if time is None:
            time = (datetime.now()).strftime("%H%M")

        if self.__complexity == "c" or (validate_date(date) and validate_time(time)):
            if filter != None:
                search_query = "/json/search/" + str(tiploc) + "/to/<toStation>" + str(filter)

            else:
                search_query = "https://api.rtt.io/api/v1/json/search/" + str(tiploc) + "/" + str(date) + "/arrivals"
            #print(search_query)
            api_response =  requests.get(search_query, auth=(self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()

                if self.__complexity == "c":
                    split_date = date.split("/")
                    file_name = "JSONs/" + tiploc + "_on_" + split_date[0] + "." + split_date[1] + "." + split_date[2] + "_arr_board_data.json"

                    with open(file_name, 'x', encoding='utf-8') as file:
                        json.dump(service_data, file, ensure_ascii = False, indent = 4)
                       
                        return_info: str = "Board information added to new file: " + file_name

                    print(return_info)
                
                elif self.__complexity == "a":
                    # data to be returned
                    pass
                
                elif self.__complexity == "s":
                    # data to be returned
                    pass


            elif api_response.status_code == 404:
                raise ValueError("An unexpected error occurred. Status code:", api_response.status_code)
            
            elif api_response.status_code == 401 or api_response.status_code == 403:
                raise ValueError("Access blocked: check your credentials. Status code:", api_response.status_code)

            else:
                raise ConnectionRefusedError("Failed to connect to the RTT API server. Try again in a few minutes. Status code:", api_response.status_code)

        else: 
            raise ValueError("Invalid date or time. Date or time provided did not meet requirements or fall into the valid date/time range.")