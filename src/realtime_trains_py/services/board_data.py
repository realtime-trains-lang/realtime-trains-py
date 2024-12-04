from datetime import datetime
from realtime_trains_py.services.utilities import format_time, validate_date, validate_time 
from tabulate import tabulate

import json
import requests


class DepartureBoardSimple():
    def __init__(self, gbtt_departure, terminus, platform, realtime_departure, service_uid):
        self.gbtt_departure = gbtt_departure
        self.terminus = terminus
        self.platform = platform
        self.realtime_departure = realtime_departure
        self.service_uid = service_uid

class ArrivalBoardSimple():
    def __init__(self, gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid):
        self.gbtt_arrival = gbtt_arrival
        self.terminus = terminus
        self.origin = origin
        self.platform = platform
        self.realtime_arrival = realtime_arrival
        self.service_uid = service_uid

class DepartureBoardAdvanced():
    def __init__(self, gbtt_departure, terminus, platform, realtime_departure, service_uid):
        self.gbtt_departure = gbtt_departure
        self.terminus = terminus
        self.platform = platform
        self.realtime_departure = realtime_departure
        self.service_uid = service_uid

class ArrivalBoardAdvanced():
    def __init__(self, gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid):
        self.gbtt_arrival = gbtt_arrival
        self.terminus = terminus
        self.origin = origin
        self.platform = platform
        self.realtime_arrival = realtime_arrival
        self.service_uid = service_uid


class Boards():
    def __init__(self, username: str = None, password: str = None, complexity: str = "s") -> None:
        self.__username = username
        self.__password = password
        self.__complexity = complexity
        self.__date: str = (datetime.now()).strftime("%Y/%m/%d")

        self._board_url: str = "https://api.rtt.io/api/v1/json/search/"

    def _get_dep_board_details(self, tiploc, filter, rows, time, date: str = None) -> list | str:
        if date is None:
            new_date = self.__date

        else:
            new_date = date

        if time is None:
            new_time = (datetime.now()).strftime("%H%M")

        else:
            new_time = time

        if self.__complexity == "c" or (validate_date(new_date) and validate_time(new_time)):
            if filter != None:
                search_query = "/json/search/" + str(tiploc) + "/to/<toStation>" + str(filter)

            elif date is not None:
                search_query = "https://api.rtt.io/api/v1/json/search/" + str(tiploc) + "/" + str(date)

            else:
                search_query = "https://api.rtt.io/api/v1/json/search/" + str(tiploc)
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

                    return return_info
                
                elif self.__complexity == "a.p" or self.__complexity == "a":
                    pass
                    #departure_board: str = []

                    #services = service_data["services"]

                elif self.__complexity == "a.n":
                    pass

                elif self.__complexity == "s.p" or self.__complexity == "s":
                    departure_board: list = []
                    
                    services = service_data["services"]
                    requested_location = service_data["location"]["name"]
                    count = 0

                    for service in services:
                        destination = service["locationDetail"]["destination"]
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

                        
                        terminus = destination.pop()["description"]

                        departure_board.append([gbtt_departure, terminus, platform, realtime_departure, service_uid])

                        count += 1
                        if count == rows:
                            break

                    print("Departure board for " + requested_location)
                    print(tabulate(departure_board, tablefmt = "rounded_grid", headers = ["Booked Departure", "Destination", "Platform", "Booked Departure", "Service UID"]))

                    return "Departure board printed successfully"  

                elif self.__complexity == "s.n":

                    departure_board: list = []
                    
                    services = service_data["services"]
                    count = 0

                    for service in services:
                        destination = service["locationDetail"]["destination"]
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

                        
                        terminus = destination.pop()["description"]

                        departure_board.append(DepartureBoardSimple(gbtt_departure, terminus, platform, realtime_departure, service_uid))

                        count += 1
                        if count == rows:
                            break

                    return departure_board 


            elif api_response.status_code == 404:
                raise ValueError("An unexpected error occurred. Status code:", api_response.status_code)
            
            elif api_response.status_code == 401 or api_response.status_code == 403:
                raise ValueError("Access blocked: check your credentials. Status code:", api_response.status_code)

            else:
                raise ConnectionRefusedError("Failed to connect to the RTT API server. Try again in a few minutes. Status code:", api_response.status_code)

        else: 
            raise ValueError("Invalid date or time. Date or time provided did not meet requirements or fall into the valid date/time range.")

    def _get_arr_board_details(self, tiploc, filter, rows, time, date: str = None) -> list | str:
        if date is None:
            new_date = self.__date

        else:
            new_date = date

        if time is None:
            new_time = (datetime.now()).strftime("%H%M")

        else:
            new_time = time

        if self.__complexity == "c" or (validate_date(new_date) and validate_time(new_time)):
            if filter is not None:
                search_query = "/json/search/" + str(tiploc) + "/to/" + str(filter)

            elif date is not None:
                search_query = "https://api.rtt.io/api/v1/json/search/" + str(tiploc) + "/" + str(date) + "/arrivals"

            else:
                search_query = "https://api.rtt.io/api/v1/json/search/" + str(tiploc) + "/arrivals"
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

                    return return_info
                
                elif self.__complexity == "a.p" or self.__complexity == "a":
                    arrivals_board: list = []
                    
                    services = service_data["services"]
                    requested_location = service_data["location"]["name"]

                    count = 0

                    for service in services:
                        destinations = service["locationDetail"]["destination"]
                        origins = service["locationDetail"]["origin"]
                        status = service["locationDetail"]["displayAs"]

                        try:
                            gbtt_arrival = service["locationDetail"]["gbttBookedArrival"]

                        except:
                            gbtt_arrival = "Unknown"

                        try:
                            platform = service["locationDetail"]["platform"]

                        except:
                            platform = "Unknown"

                        try:
                            realtime_arrival = service["locationDetail"]["realtimeArrival"]

                        except:
                            realtime_arrival = "Unknown"

                        try:
                            service_uid = service["serviceUid"]

                        except:
                            service_uid = "Unknown"


                        if status != "CANCELLED_CALL":
                            if gbtt_arrival == realtime_arrival:
                                realtime_arrival = "On time"
                                gbtt_arrival = format_time(gbtt_arrival)

                            elif realtime_arrival == "Unknown":
                                gbtt_arrival = format_time(gbtt_arrival)

                            else:
                                realtime_arrival = format_time(realtime_arrival)
                                realtime_arrival = "Exp " + realtime_arrival
                                gbtt_arrival = format_time(gbtt_arrival)

                        else:
                            realtime_arrival = "Cancelled"
                            gbtt_arrival = format_time(gbtt_arrival)

                        for destination in destinations:
                            terminus = destination["description"]
                            #print(terminus)
                        
                        origin = origins.pop()["description"]

                        arrivals_board.append([gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid])
                    
                        count += 1
                        if count == rows:
                            break

                    print("Arrivals board for " + requested_location)
                    print(tabulate(arrivals_board, tablefmt = "rounded_grid", headers = ["Booked Arrival", "Destination", "Origin", "Platform", "Booked Departure", "Service UID"]))

                    return "Arrivals board printed successfully"
                
                elif self.__complexity == "a.n":
                    
                    arrivals_board: list = []
                    
                    services = service_data["services"]
                    count = 0

                    for service in services:
                        destinations = service["locationDetail"]["destination"]
                        origins = service["locationDetail"]["origin"]
                        status = service["locationDetail"]["displayAs"]

                        try:
                            gbtt_arrival = service["locationDetail"]["gbttBookedArrival"]

                        except:
                            gbtt_arrival = "Unknown"

                        try:
                            platform = service["locationDetail"]["platform"]

                        except:
                            platform = "Unknown"

                        try:
                            realtime_arrival = service["locationDetail"]["realtimeArrival"]

                        except:
                            realtime_arrival = "Unknown"

                        try:
                            service_uid = service["serviceUid"]

                        except:
                            service_uid = "Unknown"


                        if status != "CANCELLED_CALL":
                            if gbtt_arrival == realtime_arrival:
                                realtime_arrival = "On time"
                                gbtt_arrival = format_time(gbtt_arrival)

                            elif realtime_arrival == "Unknown":
                                gbtt_arrival = format_time(gbtt_arrival)

                            else:
                                realtime_arrival = format_time(realtime_arrival)
                                realtime_arrival = "Exp " + realtime_arrival
                                gbtt_arrival = format_time(gbtt_arrival)

                        else:
                            realtime_arrival = "Cancelled"
                            gbtt_arrival = format_time(gbtt_arrival)

                        for destination in destinations:
                            terminus = destination["description"]
                            #print(terminus)
                        
                        origin = origins.pop()["description"]

                        arrivals_board.append(ArrivalBoardSimple(gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid))
                    
                        count += 1
                        if count == rows:
                            break

                elif self.__complexity == "s.p" or self.__complexity == "s":
                    arrivals_board: list = []
                    
                    services = service_data["services"]
                    requested_location = service_data["location"]["name"]
                    count = 0

                    for service in services:
                        destinations = service["locationDetail"]["destination"]
                        origins = service["locationDetail"]["origin"]
                        status = service["locationDetail"]["displayAs"]

                        try:
                            gbtt_arrival = service["locationDetail"]["gbttBookedArrival"]

                        except:
                            gbtt_arrival = "Unknown"

                        try:
                            platform = service["locationDetail"]["platform"]

                        except:
                            platform = "Unknown"

                        try:
                            realtime_arrival = service["locationDetail"]["realtimeArrival"]

                        except:
                            realtime_arrival = "Unknown"

                        try:
                            service_uid = service["serviceUid"]

                        except:
                            service_uid = "Unknown"


                        if status != "CANCELLED_CALL":
                            if gbtt_arrival == realtime_arrival:
                                realtime_arrival = "On time"
                                gbtt_arrival = format_time(gbtt_arrival)

                            elif realtime_arrival == "Unknown":
                                gbtt_arrival = format_time(gbtt_arrival)

                            else:
                                realtime_arrival = format_time(realtime_arrival)
                                realtime_arrival = "Exp " + realtime_arrival
                                gbtt_arrival = format_time(gbtt_arrival)

                        else:
                            realtime_arrival = "Cancelled"
                            gbtt_arrival = format_time(gbtt_arrival)

                        for destination in destinations:
                            terminus = destination["description"]
                            #print(terminus)
                        
                        origin = origins.pop()["description"]

                        arrivals_board.append([gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid])

                        count += 1
                        if count == rows:
                            break
                    
                    print("Arrivals board for " + requested_location)
                    print(tabulate(arrivals_board, tablefmt = "rounded_grid", headers = ["Booked Arrival", "Destination", "Origin", "Platform", "Booked Departure", "Service UID"]))

                    return "Arrivals board printed successfully"

                elif self.__complexity == "s.n":

                    arrivals_board: list = []
                    
                    services = service_data["services"]
                    count = 0

                    for service in services:
                        destinations = service["locationDetail"]["destination"]
                        origins = service["locationDetail"]["origin"]
                        status = service["locationDetail"]["displayAs"]

                        try:
                            gbtt_arrival = service["locationDetail"]["gbttBookedArrival"]

                        except:
                            gbtt_arrival = "Unknown"

                        try:
                            platform = service["locationDetail"]["platform"]

                        except:
                            platform = "Unknown"

                        try:
                            realtime_arrival = service["locationDetail"]["realtimeArrival"]

                        except:
                            realtime_arrival = "Unknown"

                        try:
                            service_uid = service["serviceUid"]

                        except:
                            service_uid = "Unknown"


                        if status != "CANCELLED_CALL":
                            if gbtt_arrival == realtime_arrival:
                                realtime_arrival = "On time"
                                gbtt_arrival = format_time(gbtt_arrival)

                            elif realtime_arrival == "Unknown":
                                gbtt_arrival = format_time(gbtt_arrival)

                            else:
                                realtime_arrival = format_time(realtime_arrival)
                                realtime_arrival = "Exp " + realtime_arrival
                                gbtt_arrival = format_time(gbtt_arrival)

                        else:
                            realtime_arrival = "Cancelled"
                            gbtt_arrival = format_time(gbtt_arrival)

                        for destination in destinations:
                            terminus = destination["description"]
                            #print(terminus)
                        
                        origin = origins.pop()["description"]

                        arrivals_board.append(ArrivalBoardSimple(gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid))

                        count += 1
                        if count == rows:
                            break

                    return arrivals_board


            elif api_response.status_code == 404:
                raise ValueError("An unexpected error occurred. Status code:", api_response.status_code)
            
            elif api_response.status_code == 401 or api_response.status_code == 403:
                raise ValueError("Access blocked: check your credentials. Status code:", api_response.status_code)

            else:
                raise ConnectionRefusedError("Failed to connect to the RTT API server. Try again in a few minutes. Status code:", api_response.status_code)

        else: 
            raise ValueError("Invalid date or time. Date or time provided did not meet requirements or fall into the valid date/time range.")
        