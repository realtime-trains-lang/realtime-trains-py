# Import external libraries
from datetime import datetime
from tabulate import tabulate

# Import necessary items from other files
from realtime_trains_py.internal.details import StationBoardDetails
from realtime_trains_py.internal.merge_sort import merge_sort
from realtime_trains_py.internal.utilities import format_time, get_time_status


# Class for creating station boards
class NewStationBoard:
    # Initialise the board
    def __init__(self, rows=None, departure_data=None, arrival_data=None) -> None:
        requested_location = departure_data["location"]["name"]  # Requested location

        # Compare the locations and check they're equal
        if requested_location == arrival_data["location"]["name"]:
            self._requested_location = requested_location

        else:
            raise Exception("500: An unexpected error occurred handling your request. Try again in a few minutes.")

        # Create new empty boards
        added_items = []
        arr_dep_temp = []
        arrival_board = []
        departure_board = []
        self._combined_board = []

        count = 0
        # Iterate over each service and append it to the departure board
        for dep_service in departure_data["services"]:
            departure_board.append(create_service_details(dep_service, "Departure"))
            count +=1 
            if count == rows:
                break

        count = 0
        # Iterate over each service and append it to the arrival board
        for arr_service in arrival_data["services"]:
            arrival_board.append(create_service_details(arr_service, "Arrival"))
            count +=1 
            if count == rows:
                break

        # Iterate over each item in departure board
        for departures in departure_board:
            # Iterate over each item in arrival board
            for arrivals in arrival_board:
                # If the values at position 0 are equal...
                if departures[0] == arrivals[0]:
                    # Remove any duplicates from arr_dep_temp
                    if arrivals[1] in arr_dep_temp:
                        arr_dep_temp.remove(arrivals[1])

                    if departures[1] in arr_dep_temp:
                        arr_dep_temp.remove(departures[1])

                    # Add the values that need to be inserted to the added items list
                    added_items.append(departures[1])
                    added_items.append(arrivals[1])

                    # Overwrite the departure times
                    arrivals[1].realtime_departure = departures[1].realtime_departure
                    arrivals[1].gbtt_departure = departures[1].gbtt_departure

                    # Append the arrivals to the combined board
                    self._combined_board.append(arrivals[1])

                    break

                else:
                    # Add any not found items to arr_dep_temp
                    if arrivals[1] not in arr_dep_temp and arrivals[1] not in added_items:
                        arr_dep_temp.append(arrivals[1])

                    if departures[1] not in arr_dep_temp and departures[1] not in added_items:
                        arr_dep_temp.append(departures[1])

        for services in arr_dep_temp:
            self._combined_board.append(services)

        added_items.clear()
        arr_dep_temp.clear()
        arrival_board.clear()
        departure_board.clear()

    def __extract_times(self) -> None:
        """
        Extract the times (the value we sort by) from the combined board and create a new board with the times and services.
        If the gbtt_departure is "-", set the sort time to gbtt_arrival.
        If the gbtt_arrival is "-", set the sort time to gbtt_departure.
        """
        temp_board = [] 

        for item in self._combined_board:
            if item.gbtt_departure == "-":
                temp_board.append([item.gbtt_arrival, item])

            else:
                temp_board.append([item.gbtt_departure, item])

        self._combined_board = temp_board

    def _create_station_board(self) -> list:
        self.__extract_times()
        #################################################
        # vvvv MERGE SORT ALGORITHM IS CALLED HERE vvvv #
        #################################################
        combined_board = merge_sort(self._combined_board)
        #################################################
        # ^^^^ MERGE SORT ALGORITHM IS CALLED HERE ^^^^ #
        #################################################
        self._combined_board.clear()

        for service in combined_board:
            self._combined_board.append(service[1])

        return self._combined_board

    def _output_formatted_board(self) -> str:
        out_board = [] 

        # For each service in the board, add its content to the output board
        for service in self._combined_board:
            out_board.append([service.gbtt_arrival, service.gbtt_departure, service.origin, service.terminus, service.platform, service.realtime_arrival, service.realtime_departure, service.service_uid])

        # Print the station details and the tabulate table
        print(f"Station board for {self._requested_location}. Generated at {datetime.now().strftime("%H:%M:%S on %d/%m/%y")}.")
        print(tabulate(out_board, tablefmt="rounded_grid", headers=["Booked Arrival", "Booked Departure", "Origin", "Destination", "Platform", "Actual Arrival", "Actual Departure", "Service UID"]))

        return "200: Station board printed successfully."

def create_service_details(service, type) -> tuple:
    """
    Get the service service data from the API response.
    This function extracts the relevant information from the service data and returns it as a StationBoardDetails object.

    It begins by setting the default values for gbtt_time, platform, real_time, and service_uid to "-".
    Then, it retrieves the location detail.
    It checks if the keys "gbttBooked[Departure/Arrival]", "platform", "realtime[Departure/Arrival]" and "serviceUid" are in the location detail and assigns their values to the respective variables.
    
    Finally, it returns the serviceUid and a StationBoardDetails object with the formatted gbtt_[Departure/Arrival], gbtt_[Arrival/Departure], terminus, origin, platform, realtime_[Departure/Arrival], realtime_[Arrival/Departure], and service_uid.
    """
    gbtt_time = platform = real_time = service_uid = "-"
    
    location_detail = service["locationDetail"] 

    if f"gbttBooked{type}" in location_detail:
        gbtt_time = location_detail[f"gbttBooked{type}"]
        
    if "platform" in location_detail:
        platform = location_detail["platform"]
        
    if f"realtime{type}" in location_detail:
        real_time = location_detail[f"realtime{type}"]

    if "serviceUid" in service:
        service_uid = service["serviceUid"]

    real_time = get_time_status(gbtt_time, real_time, location_detail["displayAs"]) 

    terminus = location_detail["destination"].pop()["description"]

    origin = location_detail["origin"].pop()["description"]

    # Return the service UID and Board Details
    if type == "Departure":
        return service_uid, StationBoardDetails("-", format_time(gbtt_time), terminus, origin, platform, "-", real_time, service_uid)
    
    else:
        return service_uid, StationBoardDetails(format_time(gbtt_time), "-", terminus, origin, platform, real_time, "-", service_uid)