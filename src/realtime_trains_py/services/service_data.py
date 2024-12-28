import requests

from datetime import datetime
from tabulate import tabulate

try:
    from realtime_trains_py.services.utilities import format_time, validate_date
except:
    from services.utilities import create_file, format_time, validate_date


class ServiceSimple():
    def __init__(self, train_id, service_uid, operator, origin, destination, all_calling_points, start_time):
        self.train_id = train_id
        self.service_uid = service_uid
        self.operator = operator
        self.origin = origin
        self.destination = destination
        self.all_calling_points = all_calling_points
        self.start_time = start_time

class CallingPointsSimple():
    def __init__(self, stop_name, booked_arrival, realtime_arrival, platform, booked_departure, realtime_departure):
        self.stop_name = stop_name
        self.booked_arrival = booked_arrival
        self.realtime_arrival = realtime_arrival
        self.platform = platform
        self.booked_departure = booked_departure
        self.realtime_departure = realtime_departure

class CallingPointsAdvanced():
    def __init__(self, stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure):
        self.stop_name = stop_name
        self.booked_arrival = booked_arrival
        self.realtime_arrival = realtime_arrival
        self.platform = platform
        self.line = line
        self.booked_departure = booked_departure
        self.realtime_departure = realtime_departure

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


    def _get_service_details(self, service_uid: str, date: str | None) -> list | str:
        if date is None:
            date = (datetime.now()).strftime("%Y/%m/%d")

        if self.__complexity == "c" or validate_date(date):
            search_query = "https://api.rtt.io/api/v1/json/service/" + str(service_uid) + "/" + str(date)
            #print(search_query)
            api_response =  requests.get(search_query, auth = (self.__username, self.__password))

            if api_response.status_code == 200:
                service_data = api_response.json()
                
                if self.__complexity == "c":
                    split_date = date.split("/")
                    file_name = service_uid + "_on_" + split_date[0] + "." + split_date[1] + "." + split_date[2] + "_service_data"

                    return create_file(file_name, service_data)    
                
                try:
                    if self.__complexity == "a.p" or self.__complexity == "a":
                        return self.__advanced_prettier(service_data, service_uid)

                    elif self.__complexity == "a.n":
                        return self.__advanced_normal(service_data, service_uid)
                    
                    elif self.__complexity == "s.p" or self.__complexity == "s":
                        return self.__simple_prettier(service_data, service_uid)

                    elif self.__complexity == "s.n":
                        return self.__simple_normal(service_data, service_uid)
                
                except:
                    raise Exception("An error occurred while fetching service data.")

            elif api_response.status_code == 404:
                raise ValueError("An unexpected error occurred. Status code:", api_response.status_code)
            
            elif api_response.status_code == 401 or api_response.status_code == 403:
                raise ValueError("Access blocked: check your credentials. Status code:", api_response.status_code)

            else:
                raise ConnectionRefusedError("Failed to connect to the RTT API server. Try again in a few minutes. Status code:", api_response.status_code)
        else:
            raise ValueError("Invalid date or time. Date or time provided did not meet requirements or fall into the valid date/time range.")

    def __advanced_normal(self, service_data, service_uid) -> None | str | ServiceAdvanced:
        service_type = service_data["serviceType"]

        if service_type == "train":
            train_id = service_data["trainIdentity"]
            operator = service_data["atocName"]
            
            if "powerType" in service_data:
                power_type = service_data["powerType"]
            else:
                power_type = "unknown"

            if "trainClass" in service_data:
                train_class = service_data["trainClass"]
            else:
                train_class = "unknown"

            origins = service_data["origin"]
            for data in origins:
                origin = data["description"]
                start_time = format_time(data["publicTime"])

            destinations = service_data["destination"]
            for data in destinations:
                destination = data["description"]
                end_time = format_time(data["publicTime"])

            calling_points = service_data["locations"]
            all_calling_points: list = []

            for locations in calling_points:
                stop_name = locations["description"]
                call_type = locations["displayAs"]

                if "realtimeArrival" in locations:
                    realtime_arrival = format_time(locations["realtimeArrival"])
                else:
                    realtime_arrival = ""

                if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                    realtime_arrival = "Cancelled"

                if "gbttBookedArrival" in locations:
                    booked_arrival = format_time(locations["gbttBookedArrival"])
                else:
                    booked_arrival = ""

                if "realtimeDeparture" in locations:
                    realtime_departure = format_time(locations["realtimeDeparture"])
                else:
                    realtime_departure = ""

                if call_type == "CANCELLED_CALL" and realtime_departure != "":
                    realtime_departure = "Cancelled"

                if "gbttBookedDeparture" in locations:
                    booked_departure = format_time(locations["gbttBookedDeparture"])
                else:
                    booked_departure = ""

                if "platform" in locations:
                    platform = locations["platform"]
                else:
                    platform = "-"

                if "line" in locations:
                    line = locations["line"]
                else:
                    line = "-"

                all_calling_points.append(CallingPointsAdvanced(stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure))

            return ServiceAdvanced(train_id, service_uid, operator, origin, destination, all_calling_points, start_time, end_time, power_type, train_class)
        
        elif service_type == "bus":
            train_id = service_data["trainIdentity"]
            operator = service_data["atocName"]

            origins = service_data["origin"]
            for data in origins:
                origin = data["description"]
                start_time = format_time(data["publicTime"])

            destinations = service_data["destination"]
            for data in destinations:
                destination = data["description"]
                end_time = format_time(data["publicTime"])

            calling_points = service_data["locations"]
            all_calling_points: list = []

            for locations in calling_points:
                stop_name = locations["description"]
                call_type = locations["displayAs"]

                if "realtimeArrival" in locations:
                    realtime_arrival = format_time(locations["realtimeArrival"])
                else:
                    realtime_arrival = ""

                if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                    realtime_arrival = "Cancelled"

                if "gbttBookedArrival" in locations:
                    booked_arrival = format_time(locations["gbttBookedArrival"])
                else:
                    booked_arrival = ""

                if "realtimeDeparture" in locations:
                    realtime_departure = format_time(locations["realtimeDeparture"])
                else:
                    realtime_departure = ""

                if call_type == "CANCELLED_CALL" and realtime_departure != "":
                    realtime_departure = "Cancelled"

                if "gbttBookedDeparture" in locations:
                    booked_departure = format_time(locations["gbttBookedDeparture"])
                else:
                    booked_departure = ""

                all_calling_points.append(CallingPointsAdvanced(stop_name, booked_arrival, realtime_arrival, "BUS", "-", booked_departure, realtime_departure))

            return ServiceAdvanced(train_id, service_uid, operator, origin, destination, all_calling_points, start_time, end_time, "BUS", "BUS")
        
        else:
            raise Exception("An error occurred while fetching service data.")
        
    def __advanced_prettier(self, service_data, service_uid) -> None | str:
        service_type = service_data["serviceType"]

        if service_type == "train":
            train_id = service_data["trainIdentity"]
            operator = service_data["atocName"]

            if "powerType" in service_data:
                power_type = service_data["powerType"]
            else:
                power_type = "unknown"

            if "trainClass" in service_data:
                train_class = service_data["trainClass"]
            else:
                train_class = "unknown"

            origins = service_data["origin"]
            for data in origins:
                origin = data["description"]
                start_time = format_time(data["publicTime"])

            destinations = service_data["destination"]
            for data in destinations:
                destination = data["description"]

            calling_points = service_data["locations"]
            all_calling_points: list = []

            for locations in calling_points:
                stop_name = locations["description"]
                call_type = locations["displayAs"]

                if "realtimeArrival" in locations:
                    realtime_arrival = format_time(locations["realtimeArrival"])
                else:
                    realtime_arrival = ""

                if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                    realtime_arrival = "Cancelled"

                if "gbttBookedArrival" in locations:
                    booked_arrival = format_time(locations["gbttBookedArrival"])
                else:
                    booked_arrival = ""

                if "realtimeDeparture" in locations:
                    realtime_departure = format_time(locations["realtimeDeparture"])
                else:
                    realtime_departure = ""

                if call_type == "CANCELLED_CALL" and realtime_departure != "":
                    realtime_departure = "Cancelled"

                if "gbttBookedDeparture" in locations:
                    booked_departure = format_time(locations["gbttBookedDeparture"])
                else:
                    booked_departure = ""

                if "platform" in locations:
                    platform = locations["platform"]
                else:
                    platform = "-"

                if "line" in locations:
                    line = locations["line"]
                else:
                    line = "-"

                all_calling_points.append([stop_name, booked_arrival, realtime_arrival, platform, line, booked_departure, realtime_departure])

            print(f"{train_id} ({service_uid}) \n  {start_time} {origin} to {destination} \n  Pathed as {power_type}: train class {train_class} \n  Operated by {operator} \n\n  Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")

            print(tabulate(
                all_calling_points, 
                tablefmt = "rounded_grid", 
                headers = ["Stop Name", 
                            "Booked Arrival", 
                            "Actual Arrival", 
                            "Platform", 
                            "Line", 
                            "Booked Departure", 
                            "Actual Departure"]
                )
            )

            return "Service data returned successfully"

        elif service_type == "bus":
            train_id = service_data["trainIdentity"]
            operator = service_data["atocName"]

            origins = service_data["origin"]
            for data in origins:
                origin = data["description"]
                start_time = format_time(data["publicTime"])

            destinations = service_data["destination"]
            for data in destinations:
                destination = data["description"]

            calling_points = service_data["locations"]
            all_calling_points: list = []

            for locations in calling_points:
                stop_name = locations["description"]
                call_type = locations["displayAs"]

                if "realtimeArrival" in locations:
                    realtime_arrival = format_time(locations["realtimeArrival"])
                else:
                    realtime_arrival = ""

                if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                    realtime_arrival = "Cancelled"

                if "gbttBookedArrival" in locations:
                    booked_arrival = format_time(locations["gbttBookedArrival"])
                else:
                    booked_arrival = ""

                if "realtimeDeparture" in locations:
                    realtime_departure = format_time(locations["realtimeDeparture"])
                else:
                    realtime_departure = ""

                if call_type == "CANCELLED_CALL" and realtime_departure != "":
                    realtime_departure = "Cancelled"

                if "gbttBookedDeparture" in locations:
                    booked_departure = format_time(locations["gbttBookedDeparture"])
                else:
                    booked_departure = ""

                all_calling_points.append([stop_name, booked_arrival, realtime_arrival, "BUS", "-", booked_departure, realtime_departure])

            print(f"{train_id} ({service_uid}) \n  {start_time} {origin} to {destination} \n  Pathed as BUS: train class BUS \n  Operated by {operator} \n\n  Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")

            print(tabulate(
                all_calling_points, 
                tablefmt = "rounded_grid", 
                headers = ["Stop Name", 
                            "Booked Arrival", 
                            "Actual Arrival", 
                            "Platform", 
                            "Line", 
                            "Booked Departure", 
                            "Actual Departure"]
                )
            )

            return "Service data returned successfully"

        else:
            raise Exception("An error occurred while fetching service data.")
        
    def __simple_normal(self, service_data, service_uid) -> ServiceSimple:
        train_id = service_data["trainIdentity"]
        operator = service_data["atocName"]

        origins = service_data["origin"]
        origin = origins.pop()["description"]
        start_time = "None"

        destinations = service_data["destination"]
        destination = destinations.pop()["description"]

        calling_points = service_data["locations"]
        all_calling_points: list = []

        for locations in calling_points:
            stop_name = locations["description"]
            call_type = locations["displayAs"]

            if "realtimeArrival" in locations:
                realtime_arrival = format_time(locations["realtimeArrival"])
            else:
                realtime_arrival = ""

            if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                realtime_arrival = "Cancelled"

            if "gbttBookedArrival" in locations:
                booked_arrival = format_time(locations["gbttBookedArrival"])
            else:
                booked_arrival = ""

            if "realtimeDeparture" in locations:
                realtime_departure = format_time(locations["realtimeDeparture"])
            else:
                realtime_departure = ""

            if call_type == "CANCELLED_CALL" and realtime_departure != "":
                realtime_departure = "Cancelled"

            if "gbttBookedDeparture" in locations:
                booked_departure = format_time(locations["gbttBookedDeparture"])
            else:
                booked_departure = ""

            if start_time == "None":
                start_time = booked_departure

            if "platform" in locations:
                platform = locations["platform"]
            else:
                platform = "-"

            all_calling_points.append(CallingPointsSimple(stop_name, booked_arrival, realtime_arrival, platform, booked_departure, realtime_departure))

        return ServiceSimple(train_id, service_uid, operator, origin, destination, all_calling_points, start_time)

    def __simple_prettier(self, service_data, service_uid) -> str:
        train_id = service_data["trainIdentity"]
        operator = service_data["atocName"]

        origins = service_data["origin"]
        origin = origins.pop()["description"]
        start_time = "None"

        destinations = service_data["destination"]
        destination = destinations.pop()["description"]

        calling_points = service_data["locations"]
        all_calling_points: list = []

        for locations in calling_points:
            stop_name = locations["description"]
            call_type = locations["displayAs"]

            if "realtimeArrival" in locations:
                realtime_arrival = format_time(locations["realtimeArrival"])
            else:
                realtime_arrival = ""

            if call_type == "CANCELLED_CALL" and realtime_arrival != "":
                realtime_arrival = "Cancelled"

            if "gbttBookedArrival" in locations:
                booked_arrival = format_time(locations["gbttBookedArrival"])
            else:
                booked_arrival = ""

            if "realtimeDeparture" in locations:
                realtime_departure = format_time(locations["realtimeDeparture"])
            else:
                realtime_departure = ""

            if call_type == "CANCELLED_CALL" and realtime_departure != "":
                realtime_departure = "Cancelled"

            if "gbttBookedDeparture" in locations:
                booked_departure = format_time(locations["gbttBookedDeparture"])
            else:
                booked_departure = ""

            if start_time == "None":
                start_time = booked_departure

            if "platform" in locations:
                platform = locations["platform"]
            else:
                platform = "-"

            all_calling_points.append([stop_name, booked_arrival, realtime_arrival, platform, booked_departure, realtime_departure])

        print(f"{train_id} ({service_uid}) {start_time} {origin} to {destination}. \n Operated by {operator}. \n\n Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")
        
        print(tabulate(
            all_calling_points, 
            tablefmt = "rounded_grid", 
            headers = ["Stop Name", 
                        "Booked Arrival", 
                        "Actual Arrival", 
                        "Platform", 
                        "Booked Departure", 
                        "Actual Departure"]
            )
        )

        return "Service data returned successfully"