from datetime import datetime
from realtime_trains_py.services.utilities import format_time, validate_date
from tabulate import tabulate

import json
import requests


class ServiceSimple():
    def __init__(self, train_id, service_uid, operator, origin, destination, all_calling_points, start_time):
        self.train_id = train_id
        self.service_uid = service_uid
        self.operator = operator
        self.origin = origin
        self.destination = destination
        self.all_calling_points = all_calling_points
        self.start_time = start_time

class ServiceAdvanced():
    def __init__(self, train_id, service_uid, operator, origin, destination, all_calling_points, start_time, end_time, power, train_class):
        self.train_id = train_id
        self.service_uid = service_uid
        self.operator = operator
        self.origin = origin
        self.destination = destination
        self.all_calling_points = all_calling_points
        self.start_time = start_time
        self.end_time = end_time
        self.power = power
        self.train_class = train_class


class ServiceDetails():
    def __init__(self, username: str = None, password: str = None, complexity: str = "s") -> None:
        self.__username = username
        self.__password = password
        self.__complexity = complexity
        self.__date: str = (datetime.now()).strftime("%Y/%m/%d")

        self._service_url: str = "https://api.rtt.io/api/v1/json/service/"


    def _get_service_details(self, service_uid: str, date: str | None) -> list | str:
        if date is None:
            date = self.__date

        if self.__complexity == "c" or validate_date(date):
            search_query = str(self._service_url) + str(service_uid) + "/" + str(date)
            #print(search_query)
            api_response =  requests.get(search_query, auth=(self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()

                if self.__complexity == "c":
                    split_date = date.split("/")
                    file_name = "JSONs/" + service_uid + "_on_" + split_date[0] + "." + split_date[1] + "." + split_date[2] + "_service_data.json"

                    with open(file_name, 'x', encoding='utf-8') as file:
                        json.dump(service_data, file, ensure_ascii = False, indent = 4)
                        
                        return_info: str = "Service information added to new file: " + file_name

                    return return_info 

                elif self.__complexity == "a.p" or self.__complexity == "a":
                    train_id = service_data["trainIdentity"]
                    operator = service_data["atocName"]

                    power_type = service_data["powerType"]
                    train_class = service_data["trainClass"]

                    origins = service_data["origin"]
                    for data in origins:
                        origin = data["description"]
                        start_time = data["publicTime"]
                        start_time = format_time(start_time)

                    destinations = service_data["destination"]
                    for data in destinations:
                        destination = data["description"]
                        end_time = data["publicTime"]
                        end_time = format_time(end_time)

                    calling_points = service_data["locations"]
                    all_calling_points: list = []

                    for locations in calling_points:
                        stop_name = locations["description"]
                        if "realtimeArrival" in locations:
                            realtime_arrival = locations["realtimeArrival"]
                            realtime_arrival = format_time(realtime_arrival)
                        else:
                            realtime_arrival = ""

                        if "gbttBookedArrival" in locations:
                            booked_arrival = locations["gbttBookedArrival"]
                            booked_arrival = format_time(booked_arrival)
                        else:
                            booked_arrival = ""

                        if "realtimeDeparture" in locations:
                            realtime_departure = locations["realtimeDeparture"]
                            realtime_departure = format_time(realtime_departure)
                        else:
                            realtime_departure = ""

                        if "gbttBookedDeparture" in locations:
                            booked_departure = locations["gbttBookedDeparture"]
                            booked_departure = format_time(booked_departure)
                        else:
                            booked_departure = ""

                        if "platform" in locations:
                            platform = locations["platform"]
                        else:
                            platform = "Unknown"

                        if "line" in locations:
                            line = locations["line"]
                        else:
                            line = "Unknown"

                        all_calling_points.append([stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure])

                    print(train_id + " (" + service_uid + ") \n" + start_time + " " + origin + " to " + destination + ". \nArrival at " + destination + ": " + end_time)
                    print("Pathed as " + power_type + ": train class " + train_class + ". \nOperated by " + operator) 
                    print(tabulate(all_calling_points, tablefmt = "rounded_grid", headers = ["Stop Name", "Booked Arrival", "Actual Arrival", "Platform", "Line", "Booked Departure", "Actual Departure"]))

                    return "Service data returned successfully"

                elif self.__complexity == "a.n":
                    train_id = service_data["trainIdentity"]
                    operator = service_data["atocName"]
                    power_type = service_data["powerType"]
                    train_class = service_data["trainClass"]

                    origins = service_data["origin"]
                    for data in origins:
                        origin = data["description"]
                        start_time = data["publicTime"]
                        start_time = format_time(start_time)

                    destinations = service_data["destination"]
                    for data in destinations:
                        destination = data["description"]
                        end_time = data["publicTime"]
                        end_time = format_time(end_time)

                    calling_points = service_data["locations"]
                    all_calling_points: list = []

                    for locations in calling_points:
                        stop_name = locations["description"]
                        if "realtimeArrival" in locations:
                            realtime_arrival = locations["realtimeArrival"]
                            realtime_arrival = format_time(realtime_arrival)
                        else:
                            realtime_arrival = ""

                        if "gbttBookedArrival" in locations:
                            booked_arrival = locations["gbttBookedArrival"]
                            booked_arrival = format_time(booked_arrival)
                        else:
                            booked_arrival = ""

                        if "realtimeDeparture" in locations:
                            realtime_departure = locations["realtimeDeparture"]
                            realtime_departure = format_time(realtime_departure)
                        else:
                            realtime_departure = ""

                        if "gbttBookedDeparture" in locations:
                            booked_departure = locations["gbttBookedDeparture"]
                            booked_departure = format_time(booked_departure)
                        else:
                            booked_departure = ""

                        if "platform" in locations:
                            platform = locations["platform"]
                        else:
                            platform = "Unknown"

                        if "line" in locations:
                            line = locations["line"]
                        else:
                            line = "Unknown"

                        all_calling_points.append([stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure])

                    return ServiceAdvanced(train_id, service_uid, operator, origin, destination, all_calling_points, start_time, end_time, power_type, train_class)
                  
                elif self.__complexity == "s.p" or self.__complexity == "s":
                    train_id = service_data["trainIdentity"]
                    operator = service_data["atocName"]

                    origins = service_data["origin"]
                    origin = origins.pop()["description"]
                    start_time = origins.pop()["publicTime"]
                    start_time = format_time(start_time)

                    destinations = service_data["destination"]
                    destination = destinations.pop()["description"]

                    calling_points = service_data["locations"]
                    all_calling_points: list = []

                    for locations in calling_points:
                        stop_name = locations["description"]
                        if "realtimeArrival" in locations:
                            realtime_arrival = locations["realtimeArrival"]
                            realtime_arrival = format_time(realtime_arrival)
                        else:
                            realtime_arrival = ""

                        if "gbttBookedArrival" in locations:
                            booked_arrival = locations["gbttBookedArrival"]
                            booked_arrival = format_time(booked_arrival)
                        else:
                            booked_arrival = ""

                        if "realtimeDeparture" in locations:
                            realtime_departure = locations["realtimeDeparture"]
                            realtime_departure = format_time(realtime_departure)
                        else:
                            realtime_departure = ""

                        if "gbttBookedDeparture" in locations:
                            booked_departure = locations["gbttBookedDeparture"]
                            booked_departure = format_time(booked_departure)
                        else:
                            booked_departure = ""

                        if "platform" in locations:
                            platform = locations["platform"]
                        else:
                            platform = "Unknown"

                        all_calling_points.append([stop_name, booked_arrival, realtime_arrival, platform, booked_departure, realtime_departure])

                    print(train_id + " (" + service_uid + ") " + start_time + " " + origin + " to " + destination)
                    print(tabulate(all_calling_points, tablefmt = "rounded_grid", headers = ["Stop Name", "Booked Arrival", "Actual Arrival", "Platform", "Booked Departure", "Actual Departure"]))

                    return "Service data returned successfully"

                elif self.__complexity == "s.n":
                    train_id = service_data["trainIdentity"]
                    operator = service_data["atocName"]

                    origins = service_data["origin"]
                    origin = origins.pop()["description"]
                    start_time = origins.pop()["publicTime"]
                    start_time = format_time(start_time)

                    destinations = service_data["destination"]
                    destination = destinations.pop()["description"]

                    calling_points = service_data["locations"]
                    all_calling_points: list = []

                    for locations in calling_points:
                        stop_name = locations["description"]
                        if "realtimeArrival" in locations:
                            realtime_arrival = locations["realtimeArrival"]
                            realtime_arrival = format_time(realtime_arrival)
                        else:
                            realtime_arrival = ""

                        if "gbttBookedArrival" in locations:
                            booked_arrival = locations["gbttBookedArrival"]
                            booked_arrival = format_time(booked_arrival)
                        else:
                            booked_arrival = ""

                        if "realtimeDeparture" in locations:
                            realtime_departure = locations["realtimeDeparture"]
                            realtime_departure = format_time(realtime_departure)
                        else:
                            realtime_departure = ""

                        if "gbttBookedDeparture" in locations:
                            booked_departure = locations["gbttBookedDeparture"]
                            booked_departure = format_time(booked_departure)
                        else:
                            booked_departure = ""

                        if "platform" in locations:
                            platform = locations["platform"]
                        else:
                            platform = "Unknown"

                        all_calling_points.append([stop_name, booked_arrival, realtime_arrival, platform, booked_departure, realtime_departure])

                    return ServiceSimple(train_id, service_uid, operator, origin, destination, all_calling_points, start_time)
                
                        


            elif api_response.status_code == 404:
                raise ValueError("An unexpected error occurred. Status code:", api_response.status_code)
            
            elif api_response.status_code == 401 or api_response.status_code == 403:
                raise ValueError("Access blocked: check your credentials. Status code:", api_response.status_code)

            else:
                raise ConnectionRefusedError("Failed to connect to the RTT API server. Try again in a few minutes. Status code:", api_response.status_code)
        else:
            raise ValueError("Invalid date or time. Date or time provided did not meet requirements or fall into the valid date/time range.")
