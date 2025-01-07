import requests

from datetime import datetime
from tabulate import tabulate

# Import functions from utilities
try:
    from realtime_trains_py.services.utilities import create_file, format_time, validate_date, validate_time
except:
    from services.utilities import create_file, format_time, validate_date, validate_time


# Class for Simple Departures Board
class DepartureBoard():
    def __init__(self, gbtt_departure, terminus, platform, realtime_departure, service_uid):
        self.gbtt_departure = gbtt_departure
        self.terminus = terminus
        self.platform = platform
        self.realtime_departure = realtime_departure
        self.service_uid = service_uid

# CLass for Simple Arrivals Board
class ArrivalBoard():
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


    def _get_dep_board_details(self, tiploc: str, search_filter: str = None, rows: int = None, time: str = None, date: str = None) -> list | str: 
        # If a date is provided and it isn't valid, raise an error
        if date is not None and not validate_date(date):
            raise ValueError("Invalid date. The date provided did not meet requirements or fall into the valid date range.")

        # If a time is provided and it isn't valid, raise an error
        if time is not None and not validate_time(time):
            raise ValueError("Invalid time. The time provided did not meet requirements or fall into the valid time range.")

        # Add the tiploc to the search_query
        search_query = f"https://api.rtt.io/api/v1/json/search/{tiploc}"

        # If a search filter was provided, append it to the search_query
        if search_filter is not None:
            search_query += f"/to/{search_filter}"

        # If a date was provided, append it to the search_query
        if date is not None:
            search_query +=  f"/{date}"

        # If a time was provided, append it to the search_query
        if time is not None:
            search_query += f"/{time}"

        # Get the api response using the auth details provided
        api_response =  requests.get(search_query, auth = (self.__username, self.__password))

        if api_response.status_code == 200:
            # If the status code is 200, convert the response to json
            service_data = api_response.json()

            # If the data is None, raise an error
            if service_data["services"] == None:
                raise ValueError("No data found.")

            # Select run based on complexity
            # Complex
            if self.__complexity == "c":
                if date is None:
                    # If no date was provided, set the date as now
                    date = (datetime.now()).strftime("%Y/%m/%d")

                # Split the date by each "/"
                date_parts = date.split("/")

                # Set the file name
                file_name = f"{tiploc}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_dep_board_data"

                # Create a new file
                create_file(file_name, service_data)

                return f"Arrivals saved to file: \n  {file_name}"
            
            # Advanced/Simple (Prettier)
            elif self.__complexity == "a.p" or self.__complexity == "a" or self.__complexity == "s.p" or self.__complexity == "s":
                # Create a new departure board list
                departure_board: list = []
                
                requested_location = service_data["location"]["name"] # Requested location
                count = 0 # Count

                for service in service_data["services"]:
                    location_detail = service["locationDetail"] # Details of the location
                    status = location_detail["displayAs"] # Status of service


                    # Check if booked departure is in location detail
                    if "gbttBookedDeparture" in location_detail:
                        gbtt_departure = location_detail["gbttBookedDeparture"]
                    else:
                        gbtt_departure = ""

                    # Check if platform is in location detail
                    if "platform" in location_detail:
                        platform = location_detail["platform"]

                    else:
                        platform = "-"

                    # Check if realtime departure is in location detail
                    if "realtimeDeparture" in location_detail:
                        realtime_departure = location_detail["realtimeDeparture"]

                    else:
                        realtime_departure = "-"

                    # Check if service UID is in location detail
                    if "serviceUid" in service:
                        service_uid = service["serviceUid"]

                    else:
                        service_uid = "-"


                    # Check if the status isn't cancelled
                    if status != "CANCELLED_CALL":
                        # If the gbtt departure and realtime departure are equal, set realtime departure to On Time
                        if gbtt_departure == realtime_departure:
                            realtime_departure = "On time"

                        # If the realtime departure isn't null, format and add Exp
                        elif realtime_departure != "-":
                            realtime_departure = f"Exp {format_time(realtime_departure)}"
                        
                        # Format the gbtt departure
                        gbtt_departure = format_time(gbtt_departure)

                    else:
                        # Set the realtime departure to cancelled
                        realtime_departure = "Cancelled"
                        # Format the gbtt departure
                        gbtt_departure = format_time(gbtt_departure)

                    
                    # Pop the terminus
                    terminus = (location_detail["destination"]).pop()["description"]

                    # Append the service details to a list
                    departure_board.append([gbtt_departure, terminus, platform, realtime_departure, service_uid])

                    # Add one to count
                    count += 1
                    # If the count is equal to the number of rows provided, break
                    if count == rows: break

                # Print the departure info
                print(f"Departure board for {requested_location}. Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y")}.")
                # Print the table
                print(tabulate(departure_board, tablefmt = "rounded_grid", headers = ["Booked Departure", "Destination", "Platform", "Actual Departure", "Service UID"]))

                return "Departure board printed successfully" 

            # Advanced/Simple (Normal)
            elif self.__complexity == "a.n" or self.__complexity == "s.n":
                # Create a new departure board list
                departure_board: list = []
                
                requested_location = service_data["location"]["name"] # Requested location
                count = 0 # Count

                for service in service_data["services"]:
                    location_detail = service["locationDetail"] # Details of the location
                    status = location_detail["displayAs"] # Status of service


                    # Check if booked departure is in location detail
                    if "gbttBookedDeparture" in location_detail:
                        gbtt_departure = location_detail["gbttBookedDeparture"]
                    else:
                        gbtt_departure = ""

                    # Check if platform is in location detail
                    if "platform" in location_detail:
                        platform = location_detail["platform"]

                    else:
                        platform = "-"

                    # Check if realtime departure is in location detail
                    if "realtimeDeparture" in location_detail:
                        realtime_departure = location_detail["realtimeDeparture"]

                    else:
                        realtime_departure = "-"

                    # Check if service UID is in location detail
                    if "serviceUid" in service:
                        service_uid = service["serviceUid"]

                    else:
                        service_uid = "-"


                    # Check if the status isn't cancelled
                    if status != "CANCELLED_CALL":
                        # If the gbtt departure and realtime departure are equal, set realtime departure to On Time
                        if gbtt_departure == realtime_departure:
                            realtime_departure = "On time"

                        # If the realtime departure isn't null, format and add Exp
                        elif realtime_departure != "-":
                            realtime_departure = f"Exp {format_time(realtime_departure)}"
                        
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
                    departure_board.append(DepartureBoard(gbtt_departure, terminus, platform, realtime_departure, service_uid))

                    # Add one to count
                    count += 1
                    # If the count is equal to the number of rows provided, break
                    if count == rows: break

                return departure_board 

        elif api_response.status_code == 404:
            # Raise an error if either status codes are 404 (Not found)
            raise Exception(f"The data you requested could not be found. Status codes: {api_response.status_code}")

        elif api_response.status_code == 401 or api_response.status_code == 403:
            # Raise an error if either status codes are 401 (Unauthorised) or 403 (Forbidden)
            raise Exception(f"Access blocked: check your credentials. Status code: {api_response.status_code}")

        else:
            # Raise an error for any other status codes
            raise Exception(f"Failed to connect to the RTT API server. Try again in a few minutes. Status code: {api_response.status_code}")

    def _get_arr_board_details(self, tiploc: str, search_filter: str = None, rows: int = None, time: str = None, date: str = None) -> list | str:       
        # If a date is provided and it isn't valid, raise an error
        if date is not None and not validate_date(date):
            raise ValueError("Invalid date. The date provided did not meet requirements or fall into the valid date range.")

        # If a time is provided and it isn't valid, raise an error
        if time is not None and not validate_time(time):
            raise ValueError("Invalid time. The time provided did not meet requirements or fall into the valid time range.")

        # Add the tiploc to the search_query
        search_query = f"https://api.rtt.io/api/v1/json/search/{tiploc}"

        # If a search filter was provided, append it to the search_query
        if search_filter is not None:
            search_query += f"/to/{search_filter}"

        # If a date was provided, append it to the search_query
        if date is not None:
            search_query +=  f"/{date}"

        # If a time was provided, append it to the search_query
        if time is not None:
            search_query += f"/{time}"

        # Get the api response using the auth details provided
        api_response =  requests.get(f"{search_query}/arrivals", auth = (self.__username, self.__password))

        if api_response.status_code == 200:
            # If the status code is 200, convert the response to json
            service_data = api_response.json()

            # If the data is None, raise an error
            if service_data["services"] == None:
                raise ValueError("No data found.")
            
            if self.__complexity == "c":
                if date is None:
                    # If no date was provided, set the date as now
                    date = (datetime.now()).strftime("%Y/%m/%d")

                # Split the date by each "/"
                date_parts = date.split("/")

                # Set the file name
                file_name = f"{tiploc}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_arr_board_data"

                # Create a new file
                create_file(file_name, service_data)

                return f"Arrivals saved to file: \n  {file_name}"
 
            # Advanced/Simple (Prettier)
            elif self.__complexity == "a.p" or self.__complexity == "a" or self.__complexity == "s.p" or self.__complexity == "s":
                # Create a new arrivals board list
                arrivals_board: list = []
                
                requested_location = service_data["location"]["name"] # Requested location
                count = 0 # Count

                for service in service_data["services"]:
                    location_detail = service["locationDetail"] # Details of the location
                    destinations = location_detail["destination"] # Destinations of services
                    status = location_detail["displayAs"] # Status of service

                    # Check if booked arrival is in location detail
                    if "gbttBookedArrival" in location_detail:
                        gbtt_arrival = location_detail["gbttBookedArrival"]

                    else:
                        gbtt_arrival = "-"

                    # Check if platform is in location detail
                    if "platform" in location_detail:
                        platform = location_detail["platform"]

                    else:
                        platform = "-"

                    # Check if realtime arrival is in location detail
                    if "realtimeArrival" in location_detail:
                        realtime_arrival = location_detail["realtimeArrival"]

                    else:
                        realtime_arrival = "-"

                    # Check if service UID is in location detail
                    if "serviceUid" in service:
                        service_uid = service["serviceUid"]

                    else:
                        service_uid = "-"

                    # Check if the status isn't cancelled
                    if status != "CANCELLED_CALL":
                        # If the gbtt arrival and realtime arrival are equal, set realtime arrival to On Time
                        if gbtt_arrival == realtime_arrival:
                            realtime_arrival = "On time"

                        # If the realtime arrival isn't null, format and add Exp
                        elif realtime_arrival != "-":
                            realtime_arrival = "Exp " + format_time(realtime_arrival)
                        
                        # Format the gbtt arrival
                        gbtt_arrival = format_time(gbtt_arrival)

                    else:
                        # Set the realtime arrival to cancelled
                        realtime_arrival = "Cancelled"
                        # Format the gbtt arrival
                        gbtt_arrival = format_time(gbtt_arrival)

                    # Pop the terminus
                    terminus = (location_detail["destination"]).pop()["description"]
                    
                    # Pop the origin
                    origin = (location_detail["origin"]).pop()["description"]

                    # Append the service details to a list
                    arrivals_board.append([gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid])
                
                    # Add one to count
                    count += 1
                    # If the count is equal to the number of rows provided, break
                    if count == rows: break
                    
                # Print the arrival info
                print("Arrivals board for " + requested_location + ". Generated at " + datetime.now().strftime("%H:%M:%S on %d/%m/%y."))
                # Print the table
                print(tabulate(arrivals_board, tablefmt = "rounded_grid", headers = ["Booked Arrival", "Destination", "Origin", "Platform", "Actual Arrival", "Service UID"]))

                return "Arrivals board printed successfully"
            
            # Advanced/Simple (Normal)
            elif self.__complexity == "a.n" or self.__complexity == "s.n":
                # Create a new arrivals board list
                arrivals_board: list = []
                
                requested_location = service_data["location"]["name"] # Requested location
                count = 0 # Count

                for service in service_data["services"]:
                    location_detail = service["locationDetail"] # Details of the location
                    destinations = location_detail["destination"] # Destinations of services
                    status = location_detail["displayAs"] # Status of service

                    # Check if booked arrival is in location detail
                    if "gbttBookedArrival" in location_detail:
                        gbtt_arrival = location_detail["gbttBookedArrival"]

                    else:
                        gbtt_arrival = "-"

                    # Check if platform is in location detail
                    if "platform" in location_detail:
                        platform = location_detail["platform"]

                    else:
                        platform = "-"

                    # Check if realtime arrival is in location detail
                    if "realtimeArrival" in location_detail:
                        realtime_arrival = location_detail["realtimeArrival"]

                    else:
                        realtime_arrival = "-"

                    # Check if service UID is in location detail
                    if "serviceUid" in service:
                        service_uid = service["serviceUid"]

                    else:
                        service_uid = "-"

                    # Check if the status isn't cancelled
                    if status != "CANCELLED_CALL":
                        # If the gbtt arrival and realtime arrival are equal, set realtime arrival to On Time
                        if gbtt_arrival == realtime_arrival:
                            realtime_arrival = "On time"

                        # If the realtime arrival isn't null, format and add Exp
                        elif realtime_arrival != "-":
                            realtime_arrival = "Exp " + format_time(realtime_arrival)
                        
                        # Format the gbtt arrival
                        gbtt_arrival = format_time(gbtt_arrival)

                    else:
                        # Set the realtime arrival to cancelled
                        realtime_arrival = "Cancelled"
                        # Format the gbtt arrival
                        gbtt_arrival = format_time(gbtt_arrival)

                    # Pop the terminus
                    terminus = (location_detail["destination"]).pop()["description"]
                    
                    # Pop the origin
                    origin = (location_detail["origin"]).pop()["description"]

                    # Append new ArrivalBoardSimple service details  
                    arrivals_board.append(ArrivalBoard(gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid))
                
                    # Add one to count
                    count += 1
                    # If the count is equal to the number of rows provided, break
                    if count == rows: break

                return arrivals_board
                    
        elif api_response.status_code == 404:
            # Raise an error if either status codes are 404 (Not found)
            raise Exception(f"The data you requested could not be found. Status codes: {api_response.status_code}")
        
        elif api_response.status_code == 401 or api_response.status_code == 403:
            # Raise an error if either status codes are 401 (Unauthorised) or 403 (Forbidden)
            raise Exception(f"Access blocked: check your credentials. Status code: {api_response.status_code}")

        else:
            # Raise an error for any other status codes
            raise Exception(f"Failed to connect to the RTT API server. Try again in a few minutes. Status code: {api_response.status_code}")

    def _get_stat_board_details(self, tiploc, search_filter, rows, time, date: str = None) -> list | str:
        # Check if the complexity is valid
        if self.__complexity in ["a", "a.p", "s", "s.n", "s.p"]:
            raise NotImplementedError

        # If a date is provided and it isn't valid, raise an error
        if date is not None and not validate_date(date):
            raise ValueError("Invalid date. The date provided did not meet requirements or fall into the valid date range.")

        # If a time is provided and it isn't valid, raise an error
        if time is not None and not validate_time(time):
            raise ValueError("Invalid time. The time provided did not meet requirements or fall into the valid time range.")

        # Add the tiploc to the search_query
        search_query = f"https://api.rtt.io/api/v1/json/search/{tiploc}"

        # If a search filter was provided, append it to the search_query
        if search_filter is not None:
            search_query += f"/to/{search_filter}"

        # If a date was provided, append it to the search_query
        if date is not None:
            search_query += f"/{date}"

        # If a time was provided, append it to the search_query
        if time is not None:
            search_query += f"/{time}"

        # Get the api response using the auth details provided
        dep_api_response =  requests.get(search_query, auth = (self.__username, self.__password))
        arr_api_response =  requests.get(f"{search_query}/arrivals", auth = (self.__username, self.__password))

        if dep_api_response.status_code == 200 and arr_api_response.status_code == 200:
            # If the status codes are 200, convert the responses to json
            departures_data = dep_api_response.json()
            arrivals_data = arr_api_response.json()

            # If the data is None, raise an error
            if departures_data["services"] == None or arrivals_data["services"] == None:
                raise ValueError("No data found.")
            
            if self.__complexity == "c":
                if date is None:
                    # If no date was provided, set the date as now
                    date = (datetime.now()).strftime("%Y/%m/%d")

                # Split the date by each "/"
                date_parts = date.split("/")

                # Set the file names
                dep_file_name = f"{tiploc}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_dep_board_data"
                arr_file_name = f"{tiploc}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_arr_board_data"

                # Create new files with the file names
                create_file(dep_file_name, departures_data)
                create_file(arr_file_name, arrivals_data)

                return f"Departures and arrivals saved to files: \n  {dep_file_name} \n  {arr_file_name}"

            elif self.__complexity.startswith("a"):                
                # Create new boards
                arrival_board = []
                departure_board = []
                combined_board = []

                # Iterate over each service and append it to the departure board
                for dep_service in departures_data["services"]:
                    departure_board.append(self.__create_dep_adv_service(dep_service))

                # Iterate over each service and append it to the arrival board
                for arr_service in arrivals_data["services"]:
                    arrival_board.append(self.__create_arr_adv_service(arr_service))

                # Iterate over each att in departures
                for departures in departure_board:
                    # Iterate over each att in arrivals
                    for arrivals in arrival_board:
                        # If the values at position 0 are equal, append it to the combined board
                        if departures[0] == arrivals[0]:
                            combined_board.append(arrivals[1])

                            # Delete the matching values from each board
                            departure_board.remove(departures)
                            arrival_board.remove(arrivals)

                return combined_board

            elif self.__complexity.startswith("s"):
                raise NotImplementedError("This complexity doesn't support this method yet.")

        elif dep_api_response.status_code == 404 or arr_api_response == 404:
            # Raise an error if either status codes are 404 (Not found)
            raise Exception(f"The data you requested could not be found. Status codes: {dep_api_response.status_code} {arr_api_response.status_code}")

        elif (dep_api_response == 401 or arr_api_response == 401) or (dep_api_response == 403 or arr_api_response == 403):
            # Raise an error if either status codes are 401 (Unauthorised) or 403 (Forbidden)
            raise Exception(f"Access blocked: check your credentials. Status codes: {dep_api_response.status_code} {arr_api_response.status_code}")

        else:
            # Raise an error for any other status codes
            raise Exception(f"Failed to connect to the RTT API server. Try again in a few minutes. Status codes {dep_api_response.status_code} {arr_api_response.status_code}")

    def __create_dep_adv_service(self, service):
        location_detail = service["locationDetail"]
        destination = location_detail["destination"]
        status = location_detail["displayAs"]


        if "gbttBookedDeparture" in location_detail:
            gbtt_departure = location_detail["gbttBookedDeparture"]

        else:
            gbtt_departure = "Unknown"

        if "platform" in location_detail:
            platform = location_detail["platform"]

        else:
            platform = "Unknown"

        if "realtimeDeparture" in location_detail:
            realtime_departure = location_detail["realtimeDeparture"]

        else:
            realtime_departure = "Unknown"

        if "serviceUid" in service:
            service_uid = service["serviceUid"]

        else:
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

        return service_uid, DepartureBoard(gbtt_departure, terminus, platform, realtime_departure, service_uid)

    def __create_arr_adv_service(self, service):
        location_detail = service["locationDetail"]
        destinations = location_detail["destination"]
        origins = location_detail["origin"]
        status = location_detail["displayAs"]

        if "gbttBookedArrival" in location_detail:
            gbtt_arrival = location_detail["gbttBookedArrival"]

        else:
            gbtt_arrival = "Unknown"

        if "platform" in location_detail:
            platform = location_detail["platform"]

        else:
            platform = "Unknown"

        if "realtimeArrival" in location_detail:
            realtime_arrival = location_detail["realtimeArrival"]

        else:
            realtime_arrival = "Unknown"

        if "serviceUid" in service:
            service_uid = service["serviceUid"]

        else:
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
        
        origin = origins.pop()["description"]

        return service_uid, ArrivalBoard(gbtt_arrival, terminus, origin, platform, realtime_arrival, service_uid)
    
    def __create_dep_sim_service(self, service):
        pass

    def __create_arr_sim_service(self, service):
        pass