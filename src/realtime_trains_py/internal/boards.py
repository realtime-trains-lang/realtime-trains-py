# Import external libraries
import requests

from datetime import datetime
from tabulate import tabulate

# Import necessary items from other files
from realtime_trains_py.internal.details import DepartureBoardDetails, ArrivalBoardDetails
from realtime_trains_py.internal.stat_boards import NewStationBoard
from realtime_trains_py.internal.utilities import create_file, create_search_query, format_time, get_time_status


class Boards:
    def __init__(self, username: str=None, password: str=None, complexity: str="s") -> None:
        self.__username = username
        self.__password = password
        self.__complexity = complexity

    def _get_dep_board_details(self, tiploc: str, search_filter: str=None, rows: int=None, time: str=None, date: str=None) -> list | str:
        # Create a search query and get the api response using the auth details provided
        api_response = requests.get(create_search_query(tiploc, search_filter, rows, time, date), auth=(self.__username, self.__password))

        if api_response.status_code == 200:
            service_data = api_response.json()

            if service_data["services"] == None:
                raise ValueError("404: No data found.")

            if self.__complexity == "c":
                # If complexity is c, save the JSON data to a new .json file
                if date is None:
                    date = (datetime.now()).strftime("%Y/%m/%d")

                date_parts = date.split("/")

                file_name = f"{tiploc}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_dep_board_data"

                create_file(file_name, service_data)

                return f"Departure data saved to file: \n  {file_name}."
            
            departure_board: list = []
            requested_location = service_data["location"]["name"]
            count = 0 

            # For each service in the departure data, get the service data
            for service in service_data["services"]:
                service_info = get_dep_service_data(service)

                if self.__complexity.endswith("n"):
                    departure_board.append(service_info)

                else:
                    # Unpack the service details and append them to a list if complexity does not end with n
                    departure_board.append([service_info.gbtt_departure, service_info.terminus, service_info.platform, service_info.realtime_departure, service_info.service_uid])

                count += 1
                if count == rows:
                    break

            if self.__complexity.endswith("n"):
                return departure_board

            # Pint the departure info and tabulate table with the headers defined
            print(f"Departure board for {requested_location}. Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y")}.")
            print(tabulate(departure_board, tablefmt="rounded_grid", headers=["Booked Departure", "Destination", "Platform", "Actual Departure", "Service UID"]))

            return "200: Departure board printed successfully."

        elif api_response.status_code == 404:
           raise Exception("404: The data you requested could not be found.")

        elif api_response.status_code == 401 or api_response.status_code == 403:
            raise Exception(f"{api_response.status_code}: Access blocked. Check your credentials.")

        else:
            raise Exception(f"{api_response.status_code}: Failed to connect to the RTT API server. Try again in a few minutes.")

    def _get_arr_board_details(self, tiploc: str, search_filter: str=None, rows: int=None, time: str=None, date: str=None) -> list | str:
        # Create a search query and get the api response using the auth details provided
        api_response = requests.get(f"{create_search_query(tiploc, search_filter, rows, time, date)}/arrivals", auth=(self.__username, self.__password))

        if api_response.status_code == 200:
            service_data = api_response.json()

            if service_data["services"] == None:
                raise ValueError("404: No data found.")

            if self.__complexity == "c":
                # If complexity is c, save the JSON data to a new .json file
                if date is None:
                    date = (datetime.now()).strftime("%Y/%m/%d")

                date_parts = date.split("/")

                file_name = f"{tiploc}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_arr_board_data"

                create_file(file_name, service_data)

                return f"Arrival data saved to file: \n  {file_name}."
            
            arrivals_board: list = []
            requested_location = service_data["location"]["name"] 
            count = 0  

            # For each service in the arrival data, get the service data
            for service in service_data["services"]:
                service_info = get_arr_service_data(service)
                    
                if self.__complexity.endswith("n"):
                    arrivals_board.append(service_info)

                else:
                    # Unpack the service details and append them to a list if complexity does not end with n
                    arrivals_board.append([service_info.gbtt_arrival, service_info.terminus, service_info.origin, service_info.platform, service_info.realtime_arrival, service_info.service_uid])

                count += 1
                if count == rows:
                    break

            if self.__complexity.endswith("n"):
                return arrivals_board
            
            # Pint the arrival info and tabulate table with the headers defined
            print(f"Arrivals board for {requested_location}. Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")
            print(tabulate(arrivals_board, tablefmt="rounded_grid", headers=["Booked Arrival", "Destination", "Origin", "Platform", "Actual Arrival", "Service UID"]))

            return "200: Arrivals board printed successfully." 

        elif api_response.status_code == 404:
            raise Exception("404: The data you requested could not be found.")

        elif api_response.status_code == 401 or api_response.status_code == 403:
            raise Exception(f"{api_response.status_code}: Access blocked. Check your credentials.")

        else:
            raise Exception(f"{api_response.status_code}: Failed to connect to the RTT API server. Try again in a few minutes.")

    def _get_stat_board_details(self, tiploc: str, search_filter: str=None, rows: int=None, time: str=None, date: str=None) -> list | str:
        # Create a search query and get the api response using the auth details provided
        search_query = create_search_query(tiploc, search_filter, rows, time, date)

        dep_api_response = requests.get(search_query, auth=(self.__username, self.__password))
        arr_api_response = requests.get(f"{search_query}/arrivals", auth=(self.__username, self.__password))

        if dep_api_response.status_code == 200 and arr_api_response.status_code == 200:
            departures_data = dep_api_response.json()
            arrivals_data = arr_api_response.json()

            if departures_data["services"] == None or arrivals_data["services"] == None:
                raise ValueError("404: No data found.")

            if self.__complexity == "c":
                # If complexity is c, save the JSON data to new .json files
                if date is None:
                    date = (datetime.now()).strftime("%Y/%m/%d")

                date_parts = date.split("/")

                dep_file_name = f"{tiploc}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_dep_board_data"
                arr_file_name = f"{tiploc}_on_{date_parts[0]}.{date_parts[1]}.{date_parts[2]}_arr_board_data"

                create_file(dep_file_name, departures_data)
                create_file(arr_file_name, arrivals_data)

                return f"200: Departures and arrivals saved to files: \n  {dep_file_name} \n  {arr_file_name}. \n"

            # Create the station board
            new_boards = NewStationBoard(rows, departures_data, arrivals_data)
            board = new_boards._create_station_board()

            if self.__complexity.endswith("n"):
                return board
            
            return new_boards._output_formatted_board()

        elif dep_api_response.status_code == 404 or arr_api_response == 404:
            raise Exception(f"{dep_api_response.status_code} | {arr_api_response.status_code}: The data you requested could not be found.")

        elif (dep_api_response == 401 or arr_api_response == 401) or (dep_api_response == 403 or arr_api_response == 403):
            raise Exception(f"{dep_api_response.status_code} | {arr_api_response.status_code}: Access blocked. Check your credentials.")

        else:
            raise Exception(f"{dep_api_response.status_code} | {arr_api_response.status_code}: Failed to connect to the RTT API server. Try again in a few minutes.")


def get_dep_service_data(service) -> DepartureBoardDetails:
    """
    Get the departure service data from the API response.
    This function extracts the relevant information from the service data and returns it as a DepartureBoardDetails object.

    It begins by setting the default values for gbtt_departure, platform, realtime_departure, and service_uid to "-".
    Then, it retrieves the location detail and status from the service data.
    It checks if the keys "gbttBookedDeparture", "platform", "realtimeArrival" and "serviceUid" are in the location detail and assigns their values to the respective variables.
    
    Finally, it returns a DepartureBoardDetails object with the formatted gbtt_departure, destination, platform, time status (aka expected arrival), and service_uid.
    """
    gbtt_departure = platform = realtime_departure = service_uid = "-"

    location_detail = service["locationDetail"] 
    status = location_detail["displayAs"] 

    if "gbttBookedDeparture" in location_detail:
        gbtt_departure = location_detail["gbttBookedDeparture"]                        

    if "platform" in location_detail:
        platform = location_detail["platform"]

    if "realtimeDeparture" in location_detail:
        realtime_departure = location_detail["realtimeDeparture"]

    if "serviceUid" in service:
        service_uid = service["serviceUid"]

    return DepartureBoardDetails(
        format_time(gbtt_departure), 
        (location_detail["destination"]).pop()["description"], 
        platform, 
        get_time_status(gbtt_departure, realtime_departure, status),
        service_uid
    )


def get_arr_service_data(service) -> ArrivalBoardDetails:
    """
    Get the arrival service data from the API response.
    This function extracts the relevant information from the service data and returns it as a ArrivalBoardDetails object.

    It begins by setting the default values for gbtt_arrival, platform, realtime_arrival, and service_uid to "-".
    Then, it retrieves the location detail and status from the service data.
    It checks if the keys "gbttBookedArrival", "platform", "realtimeArrival" and "serviceUid" are in the location detail and assigns their values to the respective variables.
    
    Finally, it returns a ArrivalBoardDetails object with the formatted gbtt_arrival, destination, origin, platform, time status (aka expected arrival), and service_uid.
    """
    gbtt_arrival = platform = realtime_arrival = service_uid = "-"
                
    location_detail = service["locationDetail"] 
    status = location_detail["displayAs"] 

    if "gbttBookedArrival" in location_detail:
        gbtt_arrival = location_detail["gbttBookedArrival"]

    if "platform" in location_detail:
        platform = location_detail["platform"]

    if "realtimeArrival" in location_detail:
        realtime_arrival = location_detail["realtimeArrival"]

    if "serviceUid" in service:
        service_uid = service["serviceUid"]

    return ArrivalBoardDetails(
        format_time(gbtt_arrival), 
        (location_detail["destination"]).pop()["description"], 
        (location_detail["origin"]).pop()["description"],
        platform, 
        get_time_status(gbtt_arrival, realtime_arrival, status),
        service_uid
    )