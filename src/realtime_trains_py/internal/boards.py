# Import libraries
import requests

from datetime import datetime
from tabulate import tabulate

# Import functions from other files
from realtime_trains_py.internal.details import DepartureBoardDetails, ArrivalBoardDetails
from realtime_trains_py.internal.stat_boards import NewStationBoard
from realtime_trains_py.internal.utilities import create_file, create_search_query, format_time, get_time_status


# Class for creating and returning departure, arrival and station boards
class Boards:
    def __init__(self, username: str=None, password: str=None, complexity: str="s") -> None:
        self.__username = username
        self.__password = password
        self.__complexity = complexity

    # Get departure board details
    def _get_dep_board_details(self, tiploc: str, search_filter: str=None, rows: int=None, time: str=None, date: str=None) -> list | str:
        # Get the api response using the auth details provided
        api_response = requests.get(create_search_query(tiploc, search_filter, rows, time, date), auth=(self.__username, self.__password))

        if api_response.status_code == 200:
            # If the status code is 200, convert the response to json
            service_data = api_response.json()

            # If the data is None, raise an error
            if service_data["services"] == None:
                raise ValueError("404: No data found.")

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

                return f"200: Arrivals saved to file: \n  {file_name}."
            
            # Create a new departure board list
            departure_board: list = []
            requested_location = service_data["location"]["name"]  # Requested location
            count = 0  # Count

            for service in service_data["services"]:
                service_info = get_dep_service_data(service)

                if self.__complexity.endswith("n"):
                    # Append new DepartureBoardSimple service details
                    departure_board.append(service_info)

                else:
                    # Append the service details to a list
                    departure_board.append([service_info.gbtt_departure, service_info.terminus, service_info.platform, service_info.realtime_departure, service_info.service_uid])

                # Add one to count
                count += 1
                # If the count is equal to the number of rows provided, break
                if count == rows:
                    break

            if self.__complexity.endswith("n"):
                return departure_board

            # Print the departure info
            print(f"Departure board for {requested_location}. Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y")}.")

            # Print the table
            print(tabulate(departure_board, tablefmt="rounded_grid", headers=["Booked Departure", "Destination", "Platform", "Actual Departure", "Service UID"]))

            return "200: Departure board printed successfully."

        elif api_response.status_code == 404:
            # Raise an error if either status codes are 404 (Not found)
            raise Exception("404: The data you requested could not be found.")

        elif api_response.status_code == 401 or api_response.status_code == 403:
            # Raise an error if either status codes are 401 (Unauthorised) or 403 (Forbidden)
            raise Exception(f"{api_response.status_code}: Access blocked. Check your credentials.")

        else:
            # Raise an error for any other status codes
            raise Exception(f"{api_response.status_code}: Failed to connect to the RTT API server. Try again in a few minutes.")

    # Get arrival board details
    def _get_arr_board_details(self, tiploc: str, search_filter: str=None, rows: int=None, time: str=None, date: str=None) -> list | str:
        # Get the api response using the auth details provided
        api_response = requests.get(f"{create_search_query(tiploc, search_filter, rows, time, date)}/arrivals", auth=(self.__username, self.__password))

        if api_response.status_code == 200:
            # If the status code is 200, convert the response to json
            service_data = api_response.json()

            # If the data is None, raise an error
            if service_data["services"] == None:
                raise ValueError("404: No data found.")

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

                return f"200: Arrivals saved to file: \n  {file_name}."
            
            # Create a new arrivals board list
            arrivals_board: list = []
            requested_location = service_data["location"]["name"]  # Requested location
            count = 0  # Count

            for service in service_data["services"]:
                service_info = get_arr_service_data(service)
                    
                if self.__complexity.endswith("n"):
                    # Append new ArrivalBoardSimple service details
                    arrivals_board.append(service_info)

                else:
                    # Append the service details to a list
                    arrivals_board.append([service_info.gbtt_arrival, service_info.terminus, service_info.origin, service_info.platform, service_info.realtime_arrival, service_info.service_uid])

                # Add one to count
                count += 1
                # If the count is equal to the number of rows provided, break
                if count == rows:
                    break

            if self.__complexity.endswith("n"):
                return arrivals_board
            
            # Print the arrival info
            print(f"Arrivals board for {requested_location}. Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y.")}")
            # Print the table
            print(tabulate(arrivals_board, tablefmt="rounded_grid", headers=["Booked Arrival", "Destination", "Origin", "Platform", "Actual Arrival", "Service UID"]))

            return "200: Arrivals board printed successfully." 

        elif api_response.status_code == 404:
            # Raise an error if either status codes are 404 (Not found)
            raise Exception("404: The data you requested could not be found.")

        elif api_response.status_code == 401 or api_response.status_code == 403:
            # Raise an error if either status codes are 401 (Unauthorised) or 403 (Forbidden)
            raise Exception(f"{api_response.status_code}: Access blocked. Check your credentials.")

        else:
            # Raise an error for any other status codes
            raise Exception(f"{api_response.status_code}: Failed to connect to the RTT API server. Try again in a few minutes.")

    # Get station board details
    def _get_stat_board_details(self, tiploc: str, search_filter: str=None, rows: int=None, time: str=None, date: str=None) -> list | str:
        search_query = create_search_query(tiploc, search_filter, rows, time, date)

        # Get the api response using the auth details provided
        dep_api_response = requests.get(search_query, auth=(self.__username, self.__password))
        arr_api_response = requests.get(f"{search_query}/arrivals", auth=(self.__username, self.__password))

        if dep_api_response.status_code == 200 and arr_api_response.status_code == 200:
            # If the status codes are 200, convert the responses to json
            departures_data = dep_api_response.json()
            arrivals_data = arr_api_response.json()

            # If the data is None, raise an error
            if departures_data["services"] == None or arrivals_data["services"] == None:
                raise ValueError("404: No data found.")

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

                return f"200: Departures and arrivals saved to files: \n  {dep_file_name} \n  {arr_file_name}. \n"

            # Create the station board
            new_boards = NewStationBoard(rows, departures_data, arrivals_data)
            board = new_boards._create_station_board()

            if self.__complexity.endswith("n"):
                return board
            
            else:
                return new_boards._output_formatted_board()

        elif dep_api_response.status_code == 404 or arr_api_response == 404:
            # Raise an error if either status codes are 404 (Not found)
            raise Exception(f"{dep_api_response.status_code} | {arr_api_response.status_code}: The data you requested could not be found.")

        elif (dep_api_response == 401 or arr_api_response == 401) or (dep_api_response == 403 or arr_api_response == 403):
            # Raise an error if either status codes are 401 (Unauthorised) or 403 (Forbidden)
            raise Exception(f"{dep_api_response.status_code} | {arr_api_response.status_code}: Access blocked. Check your credentials.")

        else:
            # Raise an error for any other status codes
            raise Exception(f"{dep_api_response.status_code} | {arr_api_response.status_code}: Failed to connect to the RTT API server. Try again in a few minutes.")


def get_dep_service_data(service) -> DepartureBoardDetails:
    gbtt_departure = platform = realtime_departure = service_uid = "-"

    location_detail = service["locationDetail"]  # Details of the location
    status = location_detail["displayAs"]  # Status of service

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

    return DepartureBoardDetails(
        format_time(gbtt_departure), 
        (location_detail["destination"]).pop()["description"], 
        platform, 
        get_time_status(gbtt_departure, realtime_departure, status),
        service_uid
    )


def get_arr_service_data(service) -> ArrivalBoardDetails:
    gbtt_arrival = platform = realtime_arrival = service_uid = "-"
                
    location_detail = service["locationDetail"]  # Details of the location
    status = location_detail["displayAs"]  # Status of service

    # Check if booked arrival is in location detail
    if "gbttBookedArrival" in location_detail:
        gbtt_arrival = location_detail["gbttBookedArrival"]

    # Check if platform is in location detail
    if "platform" in location_detail:
        platform = location_detail["platform"]

    # Check if realtime arrival is in location detail
    if "realtimeArrival" in location_detail:
        realtime_arrival = location_detail["realtimeArrival"]

    # Check if service UID is in location detail
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